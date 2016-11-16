version 0.7.11, 2016 Nov 16
===========================

Improved
--------

- added seconds (thank you @rrazor!)
- added py.test and Travis CI (just flake8 for now)
- corrected German (thanks @windlass)

Deprecated or Known Issues
--------------------------

- iqm() and miqm() aggregation functions are unreliable when the sort LIMIT
  is less than the total number of records returned (`GitHub Issue 4`_)


version 0.7.9, 2014 Oct 03
==========================

Improved
--------

- Fixed -c/--config (`GitHub Issue 6`_)

Deprecated or Known Issues
--------------------------

- iqm() and miqm() aggregation functions are unreliable when the sort LIMIT
  is less than the total number of records returned (`GitHub Issue 4`_)


version 0.7.8, 2014 Sep 19
==========================

Improved
--------

- Added debug()
- Refactored cfg_file handling with assistance from Matt Gray
  (see `CONTRIBUTORS.rst`_)

  - Setup detects VirtualEnv and respects --user
  - Logrep/wtop search for the config if it is not specified (see help)

- Added tool chain to create `Robots Pattern`_
- Improved stdin/stdout buffering handling (`GitHub Issue 3`_)

.. _`GitHub Issue 3`: https://github.com/ClockworkNet/wtop/issues/3
.. _`Robots Pattern`: https://github.com/ClockworkNet/wtop/wiki/RobotsPattern

Deprecated or Known Issues
--------------------------

- iqm() and miqm() aggregation functions are unreliable when the sort LIMIT
  is less than the total number of records returned (`GitHub Issue 4`_)
- The -c/--config option is ignored (`GitHub Issue 6`_)

.. _`GitHub Issue 6`: https://github.com/ClockworkNet/wtop/issues/6


version 0.7.7, 2013 Oct 18
==========================

Improved
--------

- Removed not-yet-implemented help text

Deprecated or Known Issues
--------------------------

- iqm() and miqm() aggregation functions are unreliable when the sort LIMIT
  is less than the total number of records returned (`GitHub Issue 4`_)


version 0.7.6, 2013 Oct 18
==========================

Improved
--------

- Now utilizes `python-iqm`_ for iqm (interquaritle mean) and miqm (moving
  interquartile mean) aggregation functions
- MovingIQM class removed from `logrep.py`
- `setup.py` updated to use setuptools per `Python Packaging User Guide`_

.. _`python-iqm`: https://github.com/ClockworkNet/python-iqm
.. _`Python Packaging User Guide`:
   https://python-packaging-user-guide.readthedocs.org/en/latest/

Deprecated or Known Issues
--------------------------

- Help text contains not-yet-implemented IQM related options
- iqm() and miqm() aggregation functions are unreliable when the sort LIMIT
  is less than the total number of records returned (`GitHub Issue 4`_)

.. _`GitHub Issue 4`: https://github.com/ClockworkNet/wtop/issues/4


version 0.7.5, 2013 Aug 28
==========================

Improved
--------

- Corrected debian docs and patch (for building a Debian or Ubuntu package)


version 0.7.4, 2013 Aug 28
==========================

Improved
--------

- Added support for mod_logio's %O (`GitHub Issue 2`_)

.. _`GitHub Issue 2`: https://github.com/ClockworkNet/wtop/issues/2


version 0.7.3, 2013 Jul 12
==========================

Improved
--------

- Corrected mid-processing `miqm()` result. The bad result corrupted the sort
  order for `miqm()` aggravated fields with less than 1001 records.


version 0.7.2, 2013 Jul 11
==========================

Improved
--------

- Fixed `miqm()` so that each aggregated field is handled separately

Deprecated or Known Issues
--------------------------

- `miqm()` does not sort correctly in this release


version 0.7.1, 2013 Jul 10
==========================

Improved
--------

- Added `miqm()` (moving interquartile mean)

Deprecated or Known Issues
--------------------------

- `miqm()` only supports a single field in this release
- `miqm()` does not sort correctly in this release


version 0.7, 2013 Jul 07
========================

Improved
--------

- Corrected `dev()` (standard deviation) (`GitHub Issue 1`_)
- Allow escaped quotes in re-quoted patterns (`Google Code Issue 34`_)
- Corrected date handling issue introduced in 0.6.8 (`Google Code Issue 32`_)
- Added support for `%F` mod-log-firstbyte_ -- "A module for Apache 2.0 which
  allows you to log the time between each request being read and the first byte
  of the response served." (`Google Code Issue 30`_)
- Added support for ignored fields in `LOG_FORMAT` (`Google Code Issue 18`_)
- Added Debian/Ubuntu packaging directory
- Code clean-up

.. _`GitHub Issue 1`: https://github.com/ClockworkNet/wtop/issues/1
.. _`Google Code Issue 34`: http://code.google.com/p/wtop/issues/detail?id=34
.. _`Google Code Issue 32`: http://code.google.com/p/wtop/issues/detail?id=32
.. _`Google Code Issue 30`: http://code.google.com/p/wtop/issues/detail?id=30
.. _`Google Code Issue 18`: http://code.google.com/p/wtop/issues/detail?id=18
.. _mod-log-firstbyte: http://code.google.com/p/mod-log-firstbyte/

Deprecated or Known Issues
--------------------------

- Dropped support for Python < 2.6
- Dropped deprecated `-g` grep_filter
- Dropped deprecated `-v` grep_exclude


version 0.6.8, 2012 Jan
==========================

Improved
--------

- Corrected timestamp issue (`Google Code Issue 31`_)

.. _`Google Code Issue 31`: http://code.google.com/p/wtop/issues/detail?id=31


Deprecated or Known Issues
--------------------------

- Dropped support for Python < 2.5


version 0.6.7, 2011 Jun
==========================

Improved
--------

- Updated to use hashlib instead of md5 (`Google Code Issue 28`_)
- Corrected domain parsing to accept httpS URLs (`Google Code Issue 27`_)
- Added support for `%A` Local IP-Address (`Google Code Issue 26`_)

.. _`Google Code Issue 28`: http://code.google.com/p/wtop/issues/detail?id=28
.. _`Google Code Issue 27`: http://code.google.com/p/wtop/issues/detail?id=27
.. _`Google Code Issue 26`: http://code.google.com/p/wtop/issues/detail?id=26


version 0.6.6, 2010 Nov
==========================

Improved
--------

- `%D` microseconds handling fixes
- Fixed python warnings

Deprecated or Known Issues
--------------------------

- Removed curses (`Google Code Issue 23`_)

.. _`Google Code Issue 23`: http://code.google.com/p/wtop/issues/detail?id=23


version 0.6.3, 2008 Sep 01
==========================

Improved
--------

- Added experimental, limited support for Micrsoft IIS logs. At the moment only
  the "W3c Extended" format is supported. In a future release there will be
  support for custom column layouts, etc. Many thanks to jbowtie for the patch.
  (`Google Code Issue 16`_; see `CONTRIBUTORS.rst`_)
- Added transparent support for Apache logfiles created with rotatelogs_. It
  should Just Work.
- Curses support in wtop mode, if available.
- Minor cleanups & speedups

.. _`Google Code Issue 16`: http://code.google.com/p/wtop/issues/detail?id=16`
.. _rotatelogs: http://httpd.apache.org/docs/2.0/programs/rotatelogs.html


version 0.6.1, 2008 Jul 31
==========================

Improved
--------

- `--sort LIMIT:FIELD:DIRECTION` option for sorting and limiting aggregate
  queries.
- Added long options such as `--output` for `-o` and `--filter` for `-f`.
- Added aggregate functions `var()` (population variance) and `dev()` (standard
  deviation)
- Experimental `--x-tmp-dir=/tmp` option when you are running aggregates over
  large (> 10 million lines) logs. If you've run out of memory trying to run a
  logrep query, try this option. If not, don't use it.
- More cleanups, getting rid of special cases, etc.
- Several speedups, bugfixes, etc.


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

- Several small bugs.
- Support for Python 2.4. In earlier versions logrep required Python 2.5 or
  higher.
- Added a `!~` operator to the `-f FILTER` option. You can now filter out
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

- The `-h` option (human traffic only) has been renamed `-H`. `-h` now outputs
  the man page.


version 0.5.8, 2008 Jun 20
==========================

Improved
--------

- `-c CONFIG_FILE` for feeding wtop and logrep custom configs
- Big speedup in `apache2unixtime()`
- Skips parsing of fields you don't ask for; nice performance boost there too.
  Credit to thwartedefforts.
- Support for nginx logs. You still have to set the `LOG_FORMAT` to the
  equivalent Apache format, but it works now with nginx's $request_time
  parameter. Credit to Igor S.
- Handles `%h` when Hostnamelookups is on in Apache. Hostnamelookups is usually
  not recommended, but you crazy kids want it, so it's there. Credit to Andrew
  Hedges (see `CONTRIBUTORS.rst`_)

.. _`CONTRIBUTORS.rst`:
   https://github.com/ClockworkNet/wtop/blob/master/CONTRIBUTORS.rst

Deprecated or Known Issues
--------------------------

- The `usec` field (microsecond response time) is gone. Use `msec`
  (milliseconds) instead. This is for compatibility with nginx, but
  microseconds is ridiculous for timing a remote network transaction anyway.
- No support for multiple `LOG_FORMAT`\s yet. You can use the new -c option to
  get around this.
