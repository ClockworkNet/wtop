Overview
=================================

wtop-clockwork is a fork of wtop_ with the goal of allowing Clockwork Active
Media Systems to maintain changes until they are included upstream.

.. _wtop: http://code.google.com/p/wtop/

wtop for running statistics
---------------------------------

wtop is like "top" for your webserver. How many searches or signups are
happening per second? What is the response time histogram for your static
files? wtop shows you at a glance.


logrep for webserver log analysis
---------------------------------

wtop also comes with logrep, a powerful command-line program for ad-hoc
analysis and filtering. Spot-check page performance, errors, aggregate
statistics, etc.


Differences From Upstream
=================================

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
=================================

- http://code.google.com/u/106843027557355696420/
- https://github.com/insyte
- https://github.com/TimBaldoni


License
=================================

wtop-clockwork is licensed under the `BSD 3-Clause License <http://www.opensource.org/licenses/BSD-3-Clause>`_

    Copyright (c) 2007-present, Carlos Bueno (carlos@bueno.org)
    Generously donated by Spock Networks, Inc.
    All rights reserved. Distributed under the "new BSD" license.

    Share and Enjoy!

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    - Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.

    - Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    - Neither the name of the holders nor the names of its contributors may be
      used to endorse or promote products derived from this software without
      specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
    ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
    LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
