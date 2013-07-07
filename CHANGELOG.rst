version 0.7, 2013 Jul 07
========================

Improved
--------

- corrected `dev()` (standard deviation) (`GitHub Issue 1`_)
- allow escaped quotes in re-quoted patterns (`Google Code Issue 34`_)
- corrected date handling issue introduced in 0.6.8 (`Google Code Issue 32`_)
- addded support for `%F` mod-log-firstbyte_ -- "A module for Apache 2.0 which
  allows you to log the time between each request being read and the first byte
  of the response served." (`Google Code Issue 30`_)
- added support for ignored fields in `LOG_FORMAT` (`Google Code Issue 18`_)
- added Debian/Ubuntu packaging directory
- code clean-up

.. _`GitHub Issue 1`: https://github.com/ClockworkNet/wtop/issues/1
.. _`Google Code Issue 34`: http://code.google.com/p/wtop/issues/detail?id=34
.. _`Google Code Issue 32`: http://code.google.com/p/wtop/issues/detail?id=32
.. _`Google Code Issue 30`: http://code.google.com/p/wtop/issues/detail?id=30
.. _`Google Code Issue 18`: http://code.google.com/p/wtop/issues/detail?id=18
.. _mod-log-firstbyte: http://code.google.com/p/mod-log-firstbyte/

Deprecated or Known Issues
--------------------------

- dropped support for Python < 2.6
- dropped deprecated `-g` grep_filter
- dropped deprecated `-v` grep_exclude


version 0.6.8, 2012 Jan
==========================

Improved
--------

- corrected timestamp issue (`Google Code Issue 31`_)

.. _`Google Code Issue 31`: http://code.google.com/p/wtop/issues/detail?id=31


Deprecated or Known Issues
--------------------------

- dropped support for Python < 2.5


version 0.6.7, 2011 Jun
==========================

Improved
--------

- updated to use hashlib instead of md5 (`Google Code Issue 28`_)
- corrected domain parsing to accept httpS URLs (`Google Code Issue 27`_)
- added support for `%A` Local IP-Address (`Google Code Issue 26`_)

.. _`Google Code Issue 28`: http://code.google.com/p/wtop/issues/detail?id=28
.. _`Google Code Issue 27`: http://code.google.com/p/wtop/issues/detail?id=27
.. _`Google Code Issue 26`: http://code.google.com/p/wtop/issues/detail?id=26


version 0.6.6, 2010 Nov
==========================

Improved
--------

- `%D` microseconds handling fixes
- fixed python warnings

Deprecated or Known Issues
--------------------------

- removed curses (`Google Code Issue 23`_)

.. _`Google Code Issue 23`: http://code.google.com/p/wtop/issues/detail?id=23


version 0.6.3, 2008 Sep 01
==========================

Improved
--------

- added experimental, limited support for Micrsoft IIS logs. At the moment only
  the "W3c Extended" format is supported. In a future release there will be
  support for custom column layouts, etc. Many thanks to jbowtie for the patch.
  (`Google Code Issue 16`_)
- added transparent support for Apache logfiles created with rotatelogs_. It
  should Just Work.
- curses support in wtop mode, if available.
- minor cleanups & speedups

.. _`Google Code Issue 16`: http://code.google.com/p/wtop/issues/detail?id=16`
.. _rotatelogs: http://httpd.apache.org/docs/2.0/programs/rotatelogs.html


version 0.6.1, 2008 Jul 31
==========================

Improved
--------

- `--sort LIMIT:FIELD:DIRECTION` option for sorting and limiting aggregate
  queries.
- added long options such as `--output` for `-o` and `--filter` for `-f`.
- added aggregate functions `var()` (population variance) and `dev()` (standard
  deviation)
- experimental `--x-tmp-dir=/tmp` option when you are running aggregates over
  large (> 10 million lines) logs. If you've run out of memory trying to run a
  logrep query, try this option. If not, don't use it.
- more cleanups, getting rid of special cases, etc.
- several speedups, bugfixes, etc.


version 0.6.0, 2008 Jul 14
==========================

Improved
--------

- Added support for aggregate functions `avg()`, `min()`, `max()`, `count(*)`
  and `sum()` in grep mode.
- Added `year`, `month`, `day`, `hour` and `minute` fields for output (`-o`)
  and filters (`-f`)
- Minor speedups and cleanups.

Deprecated or Known Issues
--------------------------

- The `-g` and `-v` options are deprecated and will be removed in version 1.0
  unless there is a general uproar. `-f` filters are more accurate and
  generally faster.


version 0.5.9, 2008 Jul 10
==========================

Improved
--------

- several small bugs.
- support for Python 2.4. In earlier versions logrep required Python 2.5 or
  higher.
- added a `!~` operator to the `-f FILTER` option. You can now filter out
  fields that do not match. For example, to see 'foo.html' hits that were NOT
  referred by 'example.com'::

    -f 'url~foo.html,ref!~www.example.com'

- Added a 'botname' field: it will show the substring from the user-agent field
  it matched to determine that the request came from a robot. You can filter
  and output it just like any other.
- Added `-R` option as a shorthand for `-f 'bot=1'`. Shows only traffic that is
  probably from a robot and not a human.

Deprecated or Known Issues
--------------------------

- the `-h` option (human traffic only) has been renamed `-H`. `-h` now outputs
  the man page.


version 0.5.8, 2008 Jun 20
==========================

Improved
--------

- `-c CONFIG_FILE` for feeding wtop and logrep custom configs
- Big speedup in `apache2unixtime()`
- Skips parsing of fields you don't ask for; nice performance boost there too.
  Credit to thwartedefforts.
- support for nginx logs. You still have to set the `LOG_FORMAT` to the
  equivalent Apache format, but it works now with nginx's $request_time
  parameter. Credit to Igor S.
- Handles `%h` when Hostnamelookups is on in Apache. Hostnamelookups is usually
  not recommended, but you crazy kids want it, so it's there. Credit to Andrew
  Hedges.

Deprecated or Known Issues
--------------------------

- The `usec` field (microsecond response time) is gone. Use `msec`
  (milliseconds) instead. This is for compatibility with nginx, but
  microseconds is ridiculous for timing a remote network transaction anyway.
- no support for multiple `LOG_FORMAT`\s yet. You can use the new -c option to
  get around this.
