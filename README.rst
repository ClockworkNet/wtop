Overview
========

wtop-clockwork is a fork of wtop_ with the goal of allowing Clockwork Active
Media Systems to maintain changes until they are included upstream.

.. _wtop: http://code.google.com/p/wtop/

wtop for running statistics
---------------------------

wtop is like "top" for your webserver. How many searches or signups are
happening per second? What is the response time histogram for your static
files? wtop shows you at a glance.


logrep for webserver log analysis
---------------------------------

wtop also comes with logrep, a powerful command-line program for ad-hoc
analysis and filtering. Spot-check page performance, errors, aggregate
statistics, etc.


Differences From Upstream
=========================

- Support for ignore fields in LOG_FORMAT (see Issue18_)
- Support for mod-log-firstbyte_ -- "A module for Apache 2.0 which allows you
  to log the time between each request being read and the first byte of the
  response served." (see Issue30_)
- **Ubuntu packaging** (``debian`` directory) without installation of DOS Batch
  scripts

.. _Issue18: http://code.google.com/p/wtop/issues/detail?id=18
.. _mod-log-firstbyte: http://code.google.com/p/mod-log-firstbyte/
.. _Issue30: http://code.google.com/p/wtop/issues/detail?id=30


Contributors
============

- http://code.google.com/u/106843027557355696420/
- https://github.com/insyte
- https://github.com/TimZehta


License
=======

- LICENSE_ (`BSD 3-Clause License`_)

.. _LICENSE: LICENSE
.. _`BSD 3-Clause License`: http://www.opensource.org/licenses/BSD-3-Clause
