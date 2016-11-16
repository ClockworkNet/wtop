#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Standard library
from __future__ import absolute_import, division, print_function
from copy import copy
from hashlib import md5 as md5
from subprocess import call
import ConfigParser
import calendar
import distutils.sysconfig
import fnmatch
import math
import os
import os.path
import random
import re
import site
import socket
import sys
import time
import urllib

# Third-party
try:
    import GeoIP
    geocoder = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
except:
    geocoder = None
try:
    import iqm
    iqm_available = True
except:
    iqm_available = False


VERSION = "0.7.11"
VERDATE = "2016 Nov 16"


LINE_BUFFERED = False
LOG_LEVEL = 1                   # 0 == quiet, 1 == normal, 2 == debug
DISC_SYNC_CNT = 100000          # number of records to hold in memory before
#                                 flushing to disk
SORT_BUFFER_LENGTH = 100000     # number of records to hold before triggering
#                                 a sort & prune operation
PROGRESS_INTERVAL = 20000       # ie warn("processed X lines...")

# randomize the disc sync and sort_buffer len to reduce the
# chance of thrashing the disks in mutlicore mode.
DISC_SYNC_CNT += (DISC_SYNC_CNT * 0.08 * random.random())
SORT_BUFFER_LENGTH += (SORT_BUFFER_LENGTH * 0.08 * random.random())

# change these defaults in your wtop.cfg file
LOG_ROOT = None
LOG_FILE = None
LOG_FILE_TYPE = None
LOG_FORMAT = None
DEFAULT_OUTPUT_FIELDS = None
MAX_REQUEST_TIME = None
MIN_RPS = None
re_robots = None
re_generic = None
re_classes = None
config = dict()

re_ip = re.compile(r"^\d+\.\d+\.\d+\.\d+$")
re_domain = re.compile(r"(?:https?://)?([^/]+)")
ipcnts = dict()
re_cmp = re.compile(r"([a-z]+)(>|<|=|\!=|\!~|\~)([^,]+)")
if iqm_available:
    re_agg = re.compile(r"(?:(avg|count|dev|iqm|max|min|miqm|sum|var)"
                        "\(([a-z\*1]+|)\)|([a-z]+))")
else:
    re_agg = re.compile(r"(?:(avg|count|dev|max|min|sum|var)"
                        "\(([a-z\*1]+|)\)|([a-z]+))")

# translate log format string into a column list and regexp
re_str = r"(\S+)"
re_str_skipped = r"\S+"
re_quot = r'((?:(?<![\\\])(?=[\\\][\\\])*[\\\]"|[^"])*)'
re_quot_skipped = r'(?:(?<![\\\])(?=[\\\][\\\])*[\\\]"|[^"])*'
re_ts = r"\[?(\S+(?:\s+[\-\+]\d+)?)\]?"
re_ts_skipped = r"\[?\S+(?:\s+[\-\+]\d+)?\]?"
re_req = r"(\S+ \S+ \S+)"
re_req_skipped = r"\S+ \S+ \S+"

# {DIRECTIVE_SYMBOL: (FIELD_NAME, REGEX_WHEN_NEEDED, REGEX_WHEN_SKIPPED)}
LOG_DIRECTIVES = {
    # ip is an odd one, since the default Apache is %h but
    "h": ("ip",         re_str, re_str_skipped),
    # HostnameLookups changes its content and %a is ALSO the ip. bleh.
    "a": ("ip",         re_str, re_str_skipped),
    "A": ("lip",        re_str, re_str_skipped),  # server (local) IP
    "l": ("auth",       re_str, re_str_skipped),
    "u": ("username",   re_str, re_str_skipped),
    "t": ("timestamp",  re_ts,  re_ts_skipped),
    "r": ("request",    re_req, re_req_skipped),
    "m": ("method",     re_str, re_str_skipped),
    "D": ("msec",       re_str, re_str_skipped),
    "F": ("fbmsec",     re_str, re_str_skipped),
    "q": ("query",      re_str, re_str_skipped),
    "s": ("status",     re_str, re_str_skipped),
    "b": ("bytes",      re_str, re_str_skipped),
    "B": ("bytes",      re_str, re_str_skipped),
    "O": ("bytes",      re_str, re_str_skipped),
    "I": ("bytes_in",   re_str, re_str_skipped),
    "v": ("domain",     re_str, re_str_skipped),  # Host header
    # actual vhost. May clobber %v
    "V": ("domain",     re_str, re_str_skipped),
    "p": ("port",       re_str, re_str_skipped),
    # todo: need generic %{foo}X parsing?
    "{ratio}n":     ("ratio",   re_quot, re_quot_skipped),
    "{host}i":      ("host",    re_quot, re_quot_skipped),
    "{referer}i":   ("ref",     re_quot, re_quot_skipped),
    "{user-agent}i": ("ua",     re_quot, re_quot_skipped),
    "ignore":       ("ignore",  re_str, re_str_skipped),
    "ignorequot":   ("ignore",  re_quot, re_quot_skipped),
}


def debug(s):
    if LOG_LEVEL < 2:
        return
    sys.stderr.write(s + "\n")
    if LINE_BUFFERED:
        sys.stderr.flush()


def warn(s):
    if LOG_LEVEL < 1:
        return
    sys.stderr.write(s + "\n")
    if LINE_BUFFERED:
        sys.stderr.flush()


def find_cfg_file():
    """Find cfg_file by searching from most accurate/specific to least.

    1. VirtualEnv + /etc/wtop.cfg
    2. PYTHONUSERBASE + /etc/wtop.cfg
    3. USER_BASE + /etc/wtop.cfg
    4. Python Lib + /etc/wtop.cfg
    5. /etc/wtop.cfg
    """
    def test_file(cfg_prefix, cfg_suffix):
        """Concatenate paths and test if resulting path is a file."""
        cfg_file = os.path.join(cfg_prefix, cfg_suffix)
        if os.path.isfile(cfg_file):
            debug("Using cfg_file: %s" % cfg_file)
            return cfg_file
        else:
            debug("Cfg_file skipped. Cfg_file not found: %s" %
                  cfg_file)
            return None

    etc_wtop_path = os.path.join("etc", "wtop.cfg")
    # VirtualEnv
    if hasattr(sys, "real_prefix"):
        cfg_file = test_file(sys.prefix, etc_wtop_path)
        if cfg_file:
            return cfg_file
    # PYTHONUSERBASE
    user_base = os.environ.get("PYTHONUSERBASE")
    if user_base:
        cfg_file = test_file(user_base, etc_wtop_path)
        if cfg_file:
            return cfg_file
    # USER_BASE
    cfg_file = test_file(site.USER_BASE, etc_wtop_path)
    if cfg_file:
        return cfg_file
    # Distutils Python Lib
    cfg_file = test_file(distutils.sysconfig.get_python_lib(), etc_wtop_path)
    if cfg_file:
        return cfg_file
    # /etc/wtop.cfg (for backwards compatibility
    cfg_file = test_file("/", "etc/wtop.cfg")
    if cfg_file:
        return cfg_file
    # fail.
    raise Exception("Cfg_file could not be found")


# yes, this is ugly.
def configure(cfg_file=None):
    global DEFAULT_OUTPUT_FIELDS, LOG_COLUMNS, LOG_FILE, LOG_FILE_TYPE
    global LOG_FORMAT, LOG_PATTERN, LOG_ROOT, MAX_REQUEST_TIME, MIN_RPS
    global config, re_classes, re_generic, re_robots

    if cfg_file is None:
        cfg_file = find_cfg_file()

    config = ConfigParser.ConfigParser()
    config.read(cfg_file)

    LOG_FILE_TYPE = config.get("main", "log_file_type")

    LOG_ROOT = config.get("main", "log_root")
    LOG_FORMAT = config.get("main", "log_format")
    DEFAULT_OUTPUT_FIELDS = config.get("main",
                                       "default_output_fields").split(",")
    MAX_REQUEST_TIME = int(config.get("wtop", "max_request_time"))
    MIN_RPS = float(config.get("wtop", "min_rps"))
    classes = list()
    for o in config.options("classes"):
        classes.append((o, config.get("classes", o)))

    # compile a godawful bunch of regexps
    re_robots = re.compile(config.get("patterns", "robots"), re.I)
    re_generic = re.compile(config.get("patterns", "generic"))
    re_classes = [(x[0], re.compile(x[1], re.I)) for x in classes]

    if LOG_FILE_TYPE == "apache":
        # these may be overridden later by the logrep command line program
        # because it knows the fields the user asked for.
        LOG_FILE = config.get("main", "log_file")
        LOG_PATTERN, LOG_COLUMNS = format2regexp(config.get("main",
                                                            "log_format"))


def flatten(x):
    result = list()
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


# lower-case some apache header options.
def lcase(s):
    if s.find("{") > -1:
        return s.lower()
    return s


# given an Apache LogFormat string and an optional list of relevant fields,
# returns a regular expression that will parse the equivalent log line and
# extract the necessary fields.
def format2regexp(fmt, relevant_fields=()):
    re_d = re.compile("%[\>\<\!,\d]*([\}\{\w\-]+)")
    directives = map(lcase, re_d.findall(fmt))
    colnames = list()
    pat = fmt
    for k in directives:
        if k not in LOG_DIRECTIVES and not k.find("{") > -1:
            continue

        field, pattern, skip_pattern = LOG_DIRECTIVES[k]
        atom = pattern
        if (not relevant_fields) or (field in relevant_fields):
            colnames.append(field)
        else:
            atom = skip_pattern

        if k.find("{") > -1:
            p = re.compile("%[\>\<\!,\d]*"+k.replace("}",
                           ".").replace("{", "."), re.I)
            pat = p.sub(atom, pat, re.I)
        else:
            pat = re.sub("%[\>\<\!,\d]*" + k, atom, pat)

    leftover = re_d.findall(pat)
    if leftover:
        warn("unrecognized format directives: %%%s" % ", %".join(leftover))

    return pat, flatten(colnames)


# NCSA log format is whimsical. often a 0 is printed as "-"
def safeint(s):
    return int(s.replace("-", "0"))


# timestamp parsing
# "...the %z escape that expands to the preferred hour/minute
#     offset is not supported by all ANSI C libraries..."
# http://docs.python.org/library/time.html
# GRRRR.
def tz2secs(s):
    plusminus = 1 if s[0] == "-" else -1
    return ((int(s[1:3])*3600) + (int(s[3:5]))*60) * plusminus


# 21/Jul/2008:18:09:00 -0700   -->   1216688940
# 03/Jan/2012:12:11:24 +0000   -->   1325592684
def apache2unixtime(t):
    return calendar.timegm(time.strptime(t[:20] + " GMT",
                           "%d/%b/%Y:%H:%M:%S %Z")) + tz2secs(t[21:26])


# 21/Jul/2008:18:09:00 -0700   -->   (2008, 7, 21, 18, 9)
def apache2dateparts(t):
    return (int(t[7:11]), time.strptime(t[3:6], "%b").tm_mon, int(t[0:2]),
            int(t[12:14]), int(t[15:17]), int(t[18:20]))


# keeps a count of seen remote IP addresses. returns
# a value for the ipcnt field.
# nb: possbile memory problem with > 10M records
# derp. IPv6?
def count_ips(ip):
    # compact the ip to 4 bytes for the ipcnts table
    ipkey = ip
    if re_ip.match(ip):  # hack: some people still have HostnameLookups on
        ipkey = socket.inet_aton(ip)
    ipcnts[ipkey] = ipcnts.get(ipkey, 0) + 1
    return ipcnts[ipkey]


# Apache's %D returns an int of microseconds. nginx's $request_time
# equivalent is a float of S.MMM, so do the Right Thing.
# returns *milli*seconds
def fix_usec(s):
    if not s or s is None:
        return 0
    if s.find(".") > -1:
        return int(float(s) * 1000)
    else:
        return int(s)/1000


# given a user-agent string, return (0, "") or (1, <MATCH>)
def parse_bots(ua):
    m = re_robots.search(ua)
    if m:
        return (1, ua[m.start():m.end()])
    return (0, "")


# "/"         --> "home"
# "/foo.jpg"  --> "img"
def classify_url(url):
    for classname, pattern in re_classes:
        if pattern.search(url):
            return classname
    m = re_generic.search(url)
    if m:
        return m.group(1)
    return "UNKNOWN"


# return domain part of a URL.
# "http://www.foo.com/bar.html"                 --> "www.foo.com"
# "example.com:8800/redirect.php?url=blah.html" --> "example.com:8800"
def domain(url):
    m = re_domain.match(url)
    if m:
        return m.group(1)
    return url


# accepts host or IP.
def geocode_country(host):
    if re_ip.match(host):
        return geocoder.country_name_by_addr(host)
    return geocoder.country_name_by_name(host)


def geocode_cc(host):
    if re_ip.match(host):
        return geocoder.country_code_by_addr(host)
    return geocoder.country_code_by_name(host)


# field massage & mapping to derived fields
# SOURCE-FIELD, (DERIVED-FIELDS), FUNCTION
# note that "class" derives from "url", which derives from "request"
col_fns = [
    ("msec",      ("msec",),            fix_usec),
    ("fbmsec",    ("fbmsec",),          fix_usec),
    ("status",    ("status",),          int),
    ("bytes",     ("bytes",),           safeint),
    ("ip",        ("ipcnt",),           count_ips),
    ("ua",        ("bot", "botname"),   parse_bots),
    ("ua",        ("uas",),             (lambda s: s[:30])),
    ("request",   ("method", "url",
                   "proto"),            (lambda s: s.split(" "))),
    ("url",       ("class",),           classify_url),
    ("timestamp", ("year", "month",
                   "day", "hour",
                   "minute", "second"), apache2dateparts),
    ("timestamp", ("ts",),              apache2unixtime),
    ("ref",       ("refdom",),          domain),
]

# only possible if the geocoding lib is loaded.
# hack: this does NOT work if HostnameLookups is on.
if geocoder:
    col_fns.append(("ip", ("country",),
                    (lambda ip: str(geocode_country(ip)))))
    col_fns.append(("ip", ("cc",), (lambda ip: str(geocode_cc(ip)))))


def listify(x):
    if not hasattr(x, "__iter__"):
        return (x,)
    return x


# apply the col_fns to the records
def field_map(log, relevant_fields, col_fns):
    # get only the column functions that are necessary
    relevant_col_fns = filter((lambda f: relevant_fields.intersection(f[1])),
                              col_fns)
    for record in log:
        for source_col, new_cols, fn in relevant_col_fns:
            record.update(dict(zip(new_cols,
                                   listify(fn(record.get(source_col, ""))))))
        yield record


# given a list of fields the user has asked for, look at the col_fns
# structure to see what parent fields they might depend on. for example,
# "year" depends on "timestamp". The idea is to only extract the fields
# from the raw log line that we actually need.
# two levels is ok for now and I'm too tired to write something recursive
def field_dependencies(requested_fields):
    deps = set(requested_fields)
    deps = set(flatten(map((lambda f: f[0:2]),
                           filter((lambda f: deps.intersection(f[1])),
                                  col_fns))))
    deps = flatten(map((lambda f: f[0:2]),
                       filter((lambda f: deps.intersection(f[1])), col_fns)))
    return set(deps + list(requested_fields))


def apache_log(loglines, LOG_PATTERN, LOG_COLUMNS, relevant_fields):
    logpat = re.compile(LOG_PATTERN)
    groups = (logpat.search(line) for line in loglines)
    tuples = (g.groups() for g in groups if g)
    log = (dict(zip(LOG_COLUMNS, t)) for t in tuples)
    log = field_map(log, relevant_fields, col_fns)
    return log


##########################################################################
# IIS-specific stuff. Can't be arsed to libraryize it.

# {"date": "2008-07-21", "time": "18:09:00"}    --> 1216688940
def iis2unixtime(r):
    return int(time.mktime(time.strptime(r["date"]+" "+r["time"],
                                         "%Y-%m-%d %H:%M:%S")))


def fix_query(q):
    if q[0] == "-":
        return ""
    return "?" + q

# source cols, parsing function takes whole record. makes it hard to
# do column dependencies, but with IIS we just split on whitespace
# anyway.
iis_col_fns = [
    (("query",),                    (lambda x: fix_query(x["query"]))),
    (("url",),                      (lambda x: x["path"]+x["query"])),
    (("ts",),                       iis2unixtime),
    (("year", "month", "day"),      (lambda x: x["date"].split("-"))),
    (("hour", "minute", "second"),  (lambda x: x["time"].split(":"))),
    (("msec",),                     (lambda x: int(x["msec"]))),
    (("status",),                   (lambda x: int(x["status"]))),
    (("bytes",),                    (lambda x: int(x["bytes"]))),
    (("ipcnt",),                    (lambda x: count_ips(x["ip"]))),
    (("bot", "botname"),            (lambda x: parse_bots(x["ua"]))),
    (("uas",),                      (lambda x: x["ua"][:30])),
    (("class",),                    (lambda x: classify_url(x["url"]))),
    (("refdom",),                   (lambda x: domain(x["ref"]))),
]
if geocoder:
    iis_col_fns.append((("country",),
                        (lambda x: str(geocode_country(x["ip"])))))
    iis_col_fns.append((("cc",), (lambda x: str(geocode_cc(x["ip"])))))


def iis_field_map(log, relevant_fields, col_fns):
    # get only the column functions that are necessary
    relevant_col_fns = filter((lambda f: relevant_fields.intersection(f[0])),
                              iis_col_fns)
    for record in log:
        for new_cols, fn in relevant_col_fns:
            record.update(dict(zip(new_cols, listify(fn(record)))))
        yield record


def iis_log(loglines, relevant_fields):
    cols = ("date", "time", "s_sitename", "s_computername", "s_ip", "method",
            "path", "query", "port", "user", "ip", "proto", "ua", "cookie",
            "ref", "vhost", "status", "substatus", "win32_status", "bytes_in",
            "bytes", "msec")
    tuples = (line.split(" ") for line in loglines)
    log = (dict(zip(cols, urllib.unquote_plus(t))) for t in tuples)
    log = iis_field_map(log, relevant_fields, iis_col_fns)
    return log
##########################################################################


# this could be implemented as a -f filter, but this is faster.
def filter_by_class(reqs, include, exclude):
    for r in reqs:
        if (include and r["class"] not in include) or (exclude and
                                                       r["class"] in exclude):
            continue
        yield r


def logs_for_date(dt):
    return sorted(gen_find(LOG_FILE + "." + dt, LOG_ROOT),
                  key=(lambda x: safeint(x.split(".")[-1])))


# support for the most common rotatelogs scheme, which is to rotate at
# midnight
def todays_logs():
    gmt_midnight = int(time.time() / 86400) * 86400
    r_file = "%s%s.%d" % (LOG_ROOT, LOG_FILE, gmt_midnight)
    if os.path.isfile(r_file):
        return [r_file]
    return [LOG_ROOT + LOG_FILE]


def yesterdays_logs():
    gmt_yesterday = (int(time.time() / 86400) - 1) * 86400
    return ["%s%s.%d" % (LOG_ROOT, LOG_FILE, gmt_yesterday)]


def latest_log():
    return todays_logs()


# # these alternative functions handle Netscaler-style logs: YYYYMMDD.log.1,
# # YYYYMMDD.log.2, etc
# def logs_for_date(dt):
#     return sorted(gen_find(dt + "*.log*",LOG_ROOT),
#                    key=(lambda x: safeint(x.split(".")[-1])))
# def todays_logs():
#     return logs_for_date(time.strftime("%Y%m%d",
#                           time.localtime(time.time())))
# def yesterdays_logs():
#     return (logs_for_date(time.strftime("%Y%m%d",
#              time.localtime(time.time()-86400)))
# def latest_log():
#     return todays_logs()[-1]


# apache log funcs from David Beazley's generators talk
def gen_find(filepat, top):
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_open(filenames):
    for name in filenames:
        handle = open(name)
        yield handle
        handle.close()


def gen_cat(sources):
    for s in sources:
        for item in s:
            yield item


def gen_grep(pat, lines):
    patc = re.compile(pat)
    for line in lines:
        if patc.search(line):
            yield line


def lines_from_dir(filepat, dirname):
    names = gen_find(filepat, dirname)
    files = gen_open(names)
    lines = gen_cat(files)
    return lines


def follow(thefile):
    last_seen = time.time()
    thefile.seek(0, 2)  # Go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            # hack: if the log is silent for awhile, it may have been rotated.
            if time.time() - last_seen > 30:
                # todo: broken & stupid. necessary for netscaler
                logfile = latest_log()[0]
                warn("no input for 30 seconds. reopening (%s)" % logfile)
                thefile.close()
                thefile = open(logfile)
                thefile.seek(0, 2)
                # so we don't start going nuts on the file.
                last_seen = time.time()

            time.sleep(0.3)    # Sleep briefly
            continue

        last_seen = time.time()
        yield line


class circular_buffer(list):
    def __init__(self, length, initval=0):
        self.pointer = 0
        self += [initval] * length
        self.length = length    # actually maxlength
        self.cnt = 0            # real length

    def append(self, item):
        self.pointer %= self.length
        self.__setitem__(self.pointer, item)
        self.pointer += 1
        self.cnt = min(self.cnt+1, self.length)

    def __len__(self):
        return self.cnt


# round-robin database that only reports stats for the last X given seconds.
class rrd2:
    def __init__(self, length, window):
        self.length = length
        self.window = float(window)
        self.buf = circular_buffer(length, (0, 0, 0))

    def append(self, item, msec):
        self.buf.append((time.time(), item, msec))

    def get(self):
        ts = time.time()
        items = sorted(filter((lambda x: (ts-x[0]) < self.window), self.buf))
        if items:
            return items, float(ts - items[0][0])
        else:
            return list(), 1.0

    def avg(self):
        items, mwindow = self.get()
        cnt = 0
        for item in items:
            cnt += item[1]
        return cnt / mwindow

    def stats(self):
        items, mwindow = self.get()
        cnt = 0
        msec_tot = 0
        msec_mn = 1 << 32
        msec_mx = 0
        msecs = list()

        for item in items:
            cnt += item[1]
            msec_tot += item[2]
            msec_mn = min(msec_mn, item[2])
            msec_mx = max(msec_mx, item[2])
            msecs.append(item[2])

        if not cnt:
            return (0, 0, 0, 0, "", 0, 0)

        rps = cnt / mwindow
        msec_avg = msec_tot / float(cnt)
        msec_stddev = stddev(msecs, msec_avg)
        sparkline = hist_sparkline(msecs, msec_mn, msec_mx)
        return (rps, msec_avg, cnt, msec_stddev, sparkline, msec_mn, msec_mx)


def stddev(lst, avg):
    avg = float(avg)+1
    lst_len = len(lst)+1
    sumdist = sum([(avg - r) ** 2 for r in lst])
    return math.sqrt(abs(sumdist / lst_len)) / avg


# given a list of numbers, generates a very sketchy
# ascii graph of the distribution.
def hist_sparkline(lst, mn, mx):
    sp_chars = (" ", ".", "-", "o", "O", "@", "#")
    sp_steps = len(sp_chars)
    tiles = 10
    cnts = dict()
    tot = len(lst)
    rn = mx-mn
    step = (rn / tiles) + 1

    if rn == 0:
        return sp_chars[0] * tiles

    steps = [int((x-mn)/step) for x in lst]
    for x in steps:
        cnts[x] = cnts.get(x, 0) + 1

    return "".join([sp_chars[int(round(cnts.get(x, 0)/float(tot) *
                                       (sp_steps-1)))] for x in range(tiles)])


# 8.5444    -->  "8.54"
# 0.99222   -->  ".99"
# 0.0000001 -->  "--"
def pretty_float(f):
    if f < 0.01:
        return "--"
    return ("%.2f" % f).replace("0.", ".")


# these two are suspiciously similar to gen_grep
def line_filter(lines, pat):
    r = re.compile(pat, re.I)
    for ln in lines:
        if r.search(ln):
            yield ln


def line_exclude(lines, pat):
    r = re.compile(pat, re.I)
    for ln in lines:
        if not r.search(ln):
            yield ln


# 100:1,2:desc --> limit 100, column 1 then column 2, descending order
def compile_orderby(commands):
    c = commands.split(":")
    limit = int(c[0])
    order_by = 0
    descending = True
    if len(c) > 1:
        order_by = map(int, c[1].split(","))
    if len(c) > 2:
        descending = (c[2][0].lower() == "d")
    return limit, order_by, descending


# "sum(foo),bar,max(baz)"  -->  ("sum", "foo"), (None, "bar"), ("max", "baz")
def compile_aggregates(commands):
    fields = re_agg.findall(commands)
    needed_fields = list()
    all_fields = list()
    group_by_fields = list()
    has_agg = False
    for f in fields:
        if f[1] != "":
            needed_fields.append(f[1])
            all_fields.append((f[0:2]))
            has_agg = True
        else:
            needed_fields.append(f[2])
            all_fields.append((None, f[2]))
            group_by_fields.append(f[2])

    return needed_fields, all_fields, group_by_fields, has_agg


# This is a compiler for teeny tiny pattern match language.
# Given a string like "bytes<100,msec>1000", it returns a function that
# filters iterables of dicts by those conditions, with lazy evaluation. The
# operators are
#
#  >, < =, !=    comparison
#  ~, !~         regexp, not regexp
#
#  Example:  "foo~^ba+,baz>100"
#   This returns true if the foo key matches "ba", "baa", "bar" but not "abad"
#   AND if the value of the baz key is greater than 100.
#
#  There is implicit conversion of strings that look like numbers.
#  There is also support for = and != of multiple values:
#
# todo: what about sets?
#  foo=(one,two,three)   or  foo=one|two|three
#
# sets can be emulated using a regexp, but it's not always the same result and
# is probably slower.
#  foo~one|two|three
#
#
def compile_filter(commands):
    tests = commands.split(",")
    conditions = [re_cmp.match(string).groups() for string in tests]
    cmp_operators = {"<": -1, ">": 1, "=": 0, "!=": 0}
    fields = [x[0] for x in conditions]

    # casts the "value" of the conditions to the same type as the given
    # example. "100" becomes 100 if the example value is numeric. If the
    # operator is "~", the condition is compiled to a regular expression.
    def typecast(example):
        castfns = dict([(k, type(v)) for k, v in example.iteritems()])
        ret = list()
        for key, op, value in conditions:
            if op[-1] == "~":
                ret.append((key, op, re.compile(value)))
            else:
                ret.append((key, op, castfns[key](value)))
        return ret

    # lazy eval of conditions.
    def predicate(obj, conditions):
        for key, op, value in conditions:
            if op[-1] == "~":
                if (not value.search(str(obj[key]))) != (op == "!~"):
                    return False
            elif (cmp_operators[op] == cmp(obj[key], value)) == (op == "!="):
                return False
        return True

    # the compiled function to be returned.
    def fn(lst):
        first = lst.next()
        conditions = typecast(first)
        if predicate(first, conditions):    # bleh. generators.
            yield first

        for item in lst:
            if predicate(item, conditions):
                yield item

    return fn, fields


def tail_n(filename, num):
    for line in os.popen("tail -%d '%s'" % (num, filename)):
        yield line


# modes
def gen_top_stats(reqs, every=5):
    stats = dict()
    last_print = 0
    stats.setdefault("(all)", (rrd2(20000, 30), rrd2(2000, 30), rrd2(200, 30),
                     rrd2(200, 30), rrd2(200, 30)))

    for r in reqs:
        # record a hit for the given status class (2xx, 3xx, 4xx, 5xx, slow)
        # to generate rps stats
        stats.setdefault(r["class"], (rrd2(20000, 30), rrd2(2000, 30),
                         rrd2(200, 30), rrd2(200, 30), rrd2(200, 30)))

        if r["msec"] < MAX_REQUEST_TIME:
            # 200 = 0, 3xx = 1, 4xx = 2, etc
            stats[r["class"]][(r["status"]/100)-2].append(1, r["msec"])
            stats["(all)"][(r["status"]/100)-2].append(1, r["msec"])

        else:  # log it in the "slow" bucket
            stats[r["class"]][4].append(1, r["msec"])
            stats["(all)"][4].append(1, r["msec"])

        if (time.time() - last_print) > every:
            last_print = time.time()
            yield stats


def apache_top_mode(reqs):
    for stats in gen_top_stats(reqs, every=5):
        buf = list()
        buf.append("% 34s     req/s   avg   min              max     3xx     "
                   "4xx     5xx     slow" % "")
        buf.append("                   --------------------------------------"
                   "--------------------------------------------------")

        for c in sorted(stats.keys()):
            # detailed stats for "200 OK" requests, simple averages for the
            # rest
            rps, avg, cnt, stdev, sparkline, mn, mx = stats[c][0].stats()
            if rps < MIN_RPS or cnt < 2:
                continue
            x3, x4, x5, slow = map(lambda x: pretty_float(x.avg()),
                                   stats[c][1:])
            buf.append("% 34s % 9s % 5d % 4d  %s % 5d % 7s % 7s % 7s % 7s" %
                       (c, pretty_float(rps), avg, mn, sparkline, mx, x3, x4,
                        x5, slow))

        print("\n".join(buf) + "\n\n\n")


# for both tail and grep mode
def print_mode(reqs, fields):
    for r in reqs:
        print("\t".join([str(r[k]) for k in fields]))
        if LINE_BUFFERED:
            sys.stdout.flush()


# compact ids for a dict, given a list of keys to use as the unique identifier
# {"foo": bar, "a": "b"}, ("foo"), 6    --> "b\315\267^O\371"
#                                           (first 6 bytes of md5("bar"))
#
# HACK: the default byte_len of 6 (48 bits) should be fine for most
# applications. If you expect to process more than 10 to 15 million aggregate
# records (eg, grouping by url or user-agent over millions of logs) AND you
# need absolute accuracy, by all means increase the byte_len default.
def id_from_dict_keys(h, keys, byte_len=6):
    return md5(",".join([str(h[k]) for k in keys])).digest()[0:byte_len]


def keyfns(order_by):
    if order_by and len(order_by) > 1:
        key_fn = (lambda v: [v[1][i] for i in order_by])
        key_fn2 = (lambda v: [v[i] for i in order_by])
    else:
        key_fn = (lambda v: v[1][order_by[0]])
        key_fn2 = (lambda v: v[order_by[0]])
    return key_fn, key_fn2


def sort_fn(order_by, descending, limit):
    key_fn, key_fn2 = keyfns(order_by)
    return (lambda table: sorted(table.itervalues(), key=key_fn2,
                                 reverse=descending)[0:limit])


# bleh -- this fn is too long
def calculate_aggregates(reqs, agg_fields, group_by, order_by=None, limit=0,
                         descending=True, tmpfile=None):
    if iqm_available:
        miqm = iqm.MovingIQM(1000)
        diqm = iqm.DictIQM(round_digits=-1, tenth_precise=True)
    MAXINT = 1 << 64
    table = dict()
    cnt = 0
    using_disk = False
    if tmpfile:
        import shelve
        table = shelve.open(tmpfile, flag="n", writeback=True)
        using_disk = True

    # each aggregate record will start as a list of values whose
    # default depends on the agg function. Also take the opportunity
    # here to build a formatting string for printing the final results.
    fmt = ["%s"] * len(agg_fields)
    blank = [0] * (len(agg_fields) + 1)  # that +1 is for a count column
    needed_post_fns = list()
    for i, f in enumerate(agg_fields):
        op, field = f
        if op == "avg":
            fmt[i] = "%.2f"
        elif op in ("dev", "miqm", "var"):
            blank[i + 1] = (0, 0)  # sum, squared sum
            needed_post_fns.append((op, i + 1))
            fmt[i] = "%.2f"
        elif op == "iqm":
            needed_post_fns.append((op, i + 1))
            fmt[i] = "%d"
        elif op == "min":
            blank[i + 1] = MAXINT
    fmt = "\t".join(fmt)

    def agg_avg(i, r, field, table, key):
        numerator = (table[key][i] * (table[key][0]-1)) + r[field]
        denominator = float(table[key][0])
        if denominator == 0:
            return 0
        else:
            return numerator / denominator

    def agg_iqm(i, r, field, table, key):
        key = "%s-%s" % (key, i)
        diqm(key, r[field])
        return (0, 0)

    def agg_miqm(i, r, field, table, key):
        key = "%s-%s" % (key, i)
        miqm(key, r[field])
        return (0, 0)

    def agg_post_prep(i, r, field, table, key):
        sums = table[key][i][0] + r[field]
        sq_sums = table[key][i][1] + (r[field] ** 2)
        return (sums, sq_sums)

    agg_fns = {
        # the None function is for pass-through fields eg "class" in
        # "class,max(msec)"
        None: (lambda i, r, field, table, key: r[field]),
        "avg": agg_avg,
        # count(*) is always just copied from col 0
        "count": (lambda i, r, field, table, key: table[key][0]),
        "dev": agg_post_prep,
        "max": (lambda i, r, field, table, key: max(r[field], table[key][i])),
        "min": (lambda i, r, field, table, key: min(r[field], table[key][i])),
        "sum": (lambda i, r, field, table, key: table[key][i] + r[field]),
        "var": agg_post_prep,
    }
    if iqm_available:
        agg_fns["iqm"] = agg_iqm
        agg_fns["miqm"] = agg_miqm

    # post-processing for more complex aggregates
    def post_dev(key, col_idx, sums, sq_sums, count):
        count = float(count)
        numerator = (count * sq_sums) - (sums * sums)
        denominator = count * (count - 1)
        if denominator == 0:
            return 0
        else:
            return math.sqrt(numerator / denominator)

    def post_iqm(key, col_idx, sums, sq_sums, count):
        key = "%s-%s" % (key, col_idx)
        return diqm.report(key)

    def post_miqm(key, col_idx, sums, sq_sums, count):
        key = "%s-%s" % (key, col_idx)
        return miqm.report(key)

    def post_var(key, col_idx, sums, sq_sums, count):
        count = float(count)
        return (sq_sums - ((sums ** 2) / count)) / count

    post_fns = {
        "dev": post_dev,
        "var": post_var,
    }
    if iqm_available:
        post_fns["iqm"] = post_iqm
        post_fns["miqm"] = post_miqm

    # various stuff needed if we are also running a limit/sort
    if limit:
        running_list = dict()
        key_fn, key_fn2 = keyfns(order_by)

    lastt = time.time()

    for r in reqs:
        cnt += 1
        if cnt % PROGRESS_INTERVAL == 0:
            t = time.time() - lastt
            lastt = time.time()
            warn("%0.2f processed %d records..." % (t, cnt))

        key = id_from_dict_keys(r, group_by)
        if key not in table:
            table[key] = copy(blank)

        # always keep record count regardless of what the user asked for
        table[key][0] += 1
        for idx, (op, field) in enumerate(agg_fields):
            table[key][idx+1] = agg_fns[op](idx+1, r, field, table, key)

        # sort & prune periodically
        if limit:
            running_list[key] = table[key]
            if cnt % SORT_BUFFER_LENGTH:
                running_list = dict(sorted(running_list.iteritems(),
                                           key=key_fn,
                                           reverse=descending)[0:limit])

        if using_disk and cnt % DISC_SYNC_CNT == 0:
            warn("sync()ing records to disk...")
            table.sync()
            warn("done.")

    if limit:
        records = running_list
    else:
        records = table

    # todo: the arg signature is not generic. what other agg functions do
    # people want?
    if needed_post_fns:
        cnt = 0
        for k in records.iterkeys():
            for (fn, col_idx) in needed_post_fns:
                records[k][col_idx] = post_fns[fn](k, col_idx,
                                                   records[k][col_idx][0],
                                                   records[k][col_idx][1],
                                                   records[k][0])
            cnt += 1
            if using_disk and cnt % DISC_SYNC_CNT == 0:
                warn("sync()ing records to disk...")
                table.sync()

    # return the records & printing format
    # for silly reasons we have to also return the tmpfile and the table
    # object.
    return records, fmt, tmpfile, table


def agg_mode(rows, fmt):
    for row in rows:
        print(fmt % tuple(row[1:]))
        if LINE_BUFFERED:
            sys.stdout.flush()


# experimental RRDtool mode for generating timeseries graphs
def normalize(lst, total, scale):
    return [int(round((x/float(total))*scale)) for x in lst]


def create_rrd(klass, ts, step=5):
    print("creating rrd", klass, ts)
    rowcnt = 86400 / step
    call(["rrdtool", "create", "%s.rrd" % klass, "--step", "%d" % step,
          "--start", "%s" % ts, "DS:rps2xx:GAUGE:5:0:5000",
          "DS:rps3xx:GAUGE:5:0:5000", "DS:rps4xx:GAUGE:5:0:5000",
          "DS:rps5xx:GAUGE:5:0:5000", "DS:msec:GAUGE:5:0:10000",
          "RRA:AVERAGE:0.5:1:%s" % rowcnt, "RRA:AVERAGE:0.5:1:%s" % rowcnt,
          "RRA:AVERAGE:0.5:1:%s" % rowcnt, "RRA:AVERAGE:0.5:1:%s" % rowcnt,
          "RRA:AVERAGE:0.5:1:%s" % rowcnt])


# coordinate all the godawful rrdtool command options
def create_graph(klass, ts, length, rpslim, mseclim, type="brief"):
    print("creating graph", klass, ts)
    common = ["-s", str(ts-length), "-e", str(ts), "--color", "BACK#ffffff00",
              "--color", "SHADEA#ffffff00", "--color", "SHADEB#ffffff00",
              "--color", "CANVAS#eeeeee00", "--color", "GRID#eeeeee00",
              "--color", "MGRID#eeeeee00", "--color", "AXIS#999999",
              "--color", "ARROW#999999", "-w", "300", "--units-length", "4",
              "--no-legend", "--slope-mode"]

    if type == "brief":
        common += ["-h", "40", "-a", "PNG", "--x-grid", "none"]
    else:
        common += ["-h", "40", "-w", "750"]

    # requests / second graph
    call(["rrdtool", "graph", "%s.%s.rps.png" % (klass, type)] + common +
         ["DEF:OK=%s.rrd:rps2xx:AVERAGE" % klass,
          "AREA:OK#44ee00:OK", "DEF:REDIRECT=%s.rrd:rps3xx:AVERAGE" % klass,
          "AREA:REDIRECT#2a89ed:REDIRECT",
          "DEF:NOTFOUND=%s.rrd:rps4xx:AVERAGE" % klass,
          "AREA:NOTFOUND#f59d18:NOTFOUND",
          "DEF:ERROR=%s.rrd:rps5xx:AVERAGE" % klass,
          "AREA:ERROR#dd0000:ERROR"])

    # response time graph
    call(["rrdtool", "graph", "%s.%s.msec.png" % (klass, type)] + common +
         ["--upper-limit", str(mseclim), "--rigid", "--y-grid",
          "%s:%s" % (mseclim, mseclim), "--units-exponent", "0",
          "--slope-mode", "DEF:MSEC=%s.rrd:msec:AVERAGE" % klass,
          "AREA:MSEC#8888cc:MSEC"])


def create_rrd_page(classes, rpslim, mseclim):
    buf = list()

    buf.append("""
    <table cellspacing="0" width="920">
    <tr class="r1">
        <td align="right" width="120" ><b>All Pages</b>&nbsp;</td>
        <td colspan="2">
        <img src="all.halfday.rps.png"  />
        <img src="all.halfday.msec.png"  />
        </td></tr>
    """)

    buf.append("""
    <tr>
        <td>&nbsp;</td>
        <td align="center"><b>Traffic Volume (req/sec)</b></td>
        <td align="center"><b>Avg Response Time (msec)</b></td>
    </tr>
    """)

    i = 0
    for c in classes[1:]:
        buf.append("""
        <tr class="r%d">
            <td width="120" align="right"><b>%s</b></td>
            <td><img src="%s.brief.rps.png" /></td>
            <td><img src="%s.brief.msec.png" /></td>
        </tr>
        """ % (i % 2, c.replace("_", " "), c, c))
        i += 1

    (open("rrd.html", "w")).write("""
    <style>
        .r1 {background:#eeeeee;}
        body {font-family: arial;}
        img {padding:2px;}
    </style>
    <meta http-equiv="refresh" content="30" />
    """ + "".join(buf))


def rrd_mode(reqs, step=5, msec_max=2000, hist_steps=10, hist_scale=100,
             do_hist=False):
    last_chart = 0
    cur_time = 0
    stats = {"all": dict(count=[0, 0, 0, 0], total_msec=0,
                         hist=[0] * hist_steps)}
    classes = dict()

    rpslim = 5
    mseclim = 2000

    for r in reqs:
        if not cur_time:
            cur_time = r["ts"]

        # init the pseudo-class "all"
        if "all" not in classes:
            classes["all"] = True
            create_rrd("all", r["ts"], 1)

        r["class"] = r["class"].replace(":", "_").replace("/", "")

        # lazy init rrd file
        if r["class"] not in classes:
            create_rrd(r["class"], r["ts"], 1)
            classes[r["class"]] = True

        # time to emit some stats
        if r["ts"] >= cur_time+step:
            print(cur_time)
            for k in classes:
                if k not in stats:
                    continue
                v = stats[k]

# Not used. Strange. Disable for now.
#               if do_hist:
#                   histogram = normalize(v["hist"], v["count"][0], hist_scale)

                call(["rrdtool", "update", "%s.rrd" % k,
                      "%d:%s:%s:%s:%s:%s" %
                      (r["ts"], int(v["count"][0]/float(step)),
                       int(v["count"][1]/float(step)),
                       int(v["count"][2]/float(step)),
                       int(v["count"][3]/float(step)),
                       v["total_msec"] / (v["count"][0] + 1))])

            cur_time = r["ts"]
            stats = {"all": dict(count=[0, 0, 0, 0], total_msec=0,
                                 hist=[0] * hist_steps)}

        else:  # gather stats
            stats.setdefault(r["class"], dict(count=[0, 0, 0, 0],
                                              total_msec=0,
                                              hist=[0] * hist_steps))
            stats[r["class"]]["count"][(r["status"]/100)-2] += 1
            stats["all"]["count"][(r["status"]/100)-2] += 1

            if r["status"] < 299:
                stats[r["class"]]["total_msec"] += r["msec"]
                stats["all"]["total_msec"] += r["msec"]

                if do_hist:
                    min_msec = min(min(r["msec"],
                                   msec_max) / (msec_max/hist_steps),
                                   hist_steps - 1)
                    stats[r["class"]]["hist"][min_msec] += 1

        # time to emit some graphs
        if cur_time - last_chart > 30:
            last_chart = cur_time

            create_graph("all", cur_time, 43200, rpslim, mseclim, "halfday")

            for k in classes.keys():
                create_graph(k, cur_time, 1800, rpslim, mseclim, "brief")
            create_rrd_page(sorted(classes.keys()), rpslim, mseclim)
