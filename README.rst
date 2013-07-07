Overview
========

wtop for running statistics
---------------------------

wtop is like "top" for your web server. How many searches or sign-ups are
happening per second? What is the response time histogram for your static
files? wtop shows you at a glance.


logrep for webserver log analysis
---------------------------------

logrep is a powerful command-line program for ad-hoc analysis and filtering.
Spot-check page performance, errors, aggregate statistics, etc.


Installation
============

Download
--------

wtop can be downloaded from the GitHub releases_.

.. _releases: https://github.com/ClockworkNet/wtop/releases


From Source
-----------

This is a Python source distribution. Install it like so::

    sudo python setup.py install

This will put logrep and wtop in your executable path, and drop the
default wtop.cfg file into `/etc/wtop.cfg`

wtop/logrep require Python version 2.6 or greater.


Debian and Ubuntu
-----------------

See `Install - wtop wiki`_.


Windows
-------

See `Install - wtop wiki`_.

.. _`Install - wtop wiki`: https://github.com/ClockworkNet/wtop/wiki/Install


Changelog
=========

- See `<CHANGELOG.rst>`_


Contributors
============

- See `<CONTRIBUTORS.rst>`_


License
=======

- `<LICENSE>`_ (`BSD 3-Clause License`_)

.. _`BSD 3-Clause License`: http://www.opensource.org/licenses/BSD-3-Clause
