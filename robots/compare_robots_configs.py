#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Standard library
import argparse
import ConfigParser
import io
import re
import time


default_iterations = 100
default_old_config = "../wtop.cfg"
default_new_config = "robots_excerpt.ini"
file_user_agents = "robot_user_agents.txt"


def parser_setup():
    """Instantiate, configure, and return an argarse instance."""
    ap = argparse.ArgumentParser(description=__doc__)
    # unable to define default for files due to
    # http://bugs.python.org/issue16399
    ap.add_argument("-o", "--old-config", metavar="OLD_CONFIG", type=file,
                    help="Old config file (default: %s)" % default_old_config)
    ap.add_argument("-n", "--new-config", metavar="NEW_CONFIG", type=file,
                    help="New config file (default: %s)" % default_new_config)
    ap.add_argument("-i", "--iterations", metavar="INT", type=int,
                    default=default_iterations,
                    help="Number of benchmarking iterations (default: "
                    "%(default)s)")
    args = ap.parse_args()
    if not args.old_config:
        args.old_config = default_old_config
    if not args.new_config:
        args.new_config = default_new_config
    return args


def read_and_compile_pattern_from_file(config_file):
    """Read INI config file and compile robots regex from robots key in
    patterns section.
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_file))
    re_robots = re.compile(config.get("patterns", "robots"), re.I)
    return re_robots


def evalute_robots_pattern(re_robots):
    """Evalute robots regex for hits and misses against robots user agents
    file.
    """
    matched = 0
    missed = 0
    i = 1
    with io.open(file_user_agents, "r", encoding="utf8") as fh:
        for line in fh:
            if re_robots.search(line):
                matched += 1
                # print "+%s:" % i, line.strip()
            else:
                missed += 1
                # print "-%s:" % i, line.strip()
            i += 1
    return matched, missed


def evaluate_config(config_file, iterations):
    """Evalute config's robots pattern and benchmark duration."""
    # Reading the pattern and compling is not included in the duration. As the
    # data is quickly supplied by the file system cache, it becomes irrelevent.
    re_robots = read_and_compile_pattern_from_file(config_file)
    matched = int()
    missed = int()
    duration_total = float()
    for i in xrange(0, iterations):
        start = time.clock()
        matched, missed = evalute_robots_pattern(re_robots)
        end = time.clock()
        duration = end - start
        duration_total += duration
    return matched, missed, duration_total / iterations


def display_results(name, config_file, data, old_data=None):
    """Display results of config evaluation."""
    matched, missed, duration = data
    msg = "%s Config (%s)" % (name, config_file)
    print msg
    print "=" * len(msg)
    if old_data is None:
        print "matched: %5d" % matched
        print "missed:  %5d" % missed
        print "duration:%9.3fs" % duration
        print
    else:
        old_matched, old_missed, old_duration = old_data
        print "matched: %5d" % matched,
        if matched > old_matched:
            adj = "more"
        else:
            adj = "less"
        diff_abs = abs(old_matched - matched)
        diff_percent = diff_abs / float(old_matched) * 100
        print "     (%.0f%% %s)" % (diff_percent, adj)
        print "missed:  %5d" % missed
        print "duration:%9.3fs" % duration,
        if duration < old_duration:
            adj = "faster"
        else:
            adj = "slower"
        diff_abs = abs(old_duration - duration)
        diff_percent = diff_abs / float(old_duration) * 100
        print "(%.0f%% %s)" % (diff_percent, adj)


def main():
    # Command Line Options
    args = parser_setup()
    # Old config
    old_data = evaluate_config(args.old_config, args.iterations)
    display_results("Old", args.old_config, old_data)
    # New config
    new_data = evaluate_config(args.new_config, args.iterations)
    display_results("New", args.new_config, new_data, old_data)


if __name__ == "__main__":
    main()
