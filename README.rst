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

Spot-check page performance, errors, aggregate statistics, etc::

    $ logrep -o 'status,count(*),avg(msec),min(msec),max(msec)' access.log
    200 4196    244.58  3   589
    302 5   79.75   17  42
    404 1   9.00    9   9
    304 798 158.76  0   694

See how robot traffic rises and falls by day::

    $ logrep --robots-only --output \
        'botname,month,day,count(*),avg(msec),dev(msec)' --sort '30:1,2,3:asc'
    Googlebot   7   20  1090    1045.97 1.65
    Googlebot   7   21  771 3082.58 2.08
    Googlebot   7   22  1177    1278.14 1.89
    Googlebot   7   23  1134    1841.48 2.59
    Googlebot   7   24  1057    1636.69 2.81
    Googlebot   7   25  536 1210.78 2.10
    ...


Query for specific strings and conditions::

    $ logrep -f "status=200,bytes>1000,msec<1000,url~Paris" \
        -o ts,msec,bytes,url
    1213574430      125     47396   /Paris-Hilton
    1213574892      126     47391   /Paris-Hilton
    1213579556      393     23028   /Diane-Parish
    1213582392      402     19757   /Paris-Kanellakis
    1213582651      530     23751   /Paris-Bennett
    1213584996      366     19295   /Tristan-Paris
    1213586358      114     47295   /Paris-Hilton
    1213587075      227     22424   /Steve-Pariso
    ...

See `CookbookLogrep - wtop wiki`_ for additional examples.

.. _`CookbookLogrep - wtop wiki`:
   https://github.com/ClockworkNet/wtop/wiki/CookbookLogrep


Python Compatibility
--------------------

This library currently requires compatibility with:

- 2.6
- 2.7

However, additional versions are tested automatically:

.. image:: https://travis-ci.org/ClockworkNet/wtop.svg?branch=master
    :target: https://travis-ci.org/ClockworkNet/wtop


Installation
============

This will put logrep and wtop in your executable path, and drop the
default `wtop.cfg` into a location appropriate to the installation
(platform appropriate path separaters are used). It searches for the
config in the following order:

1. VirtualEnv + /etc/wtop.cfg
2. PYTHONUSERBASE + /etc/wtop.cfg
3. USER_BASE + /etc/wtop.cfg
4. Python Lib + /etc/wtop.cfg
5. /etc/wtop.cfg

Invoke `logrep -d` to see which location it used.

wtop/logrep require Python version 2.6 or greater.


From from PyPI
--------------

wtop can be installed from PyPI via pip_ like so::

    sudo pip install wtop

.. _pip: http://www.pip-installer.org/en/latest/installing.html


Install from Source
-------------------

The wtop source can be downloaded from the GitHub releases_.

This is a Python source distribution. Install it like so::

    sudo python setup.py install

.. _releases: https://github.com/ClockworkNet/wtop/releases


Debian, Ubuntu, Windows, etc.
-----------------------------

See `Install - wtop wiki`_.

.. _`Install - wtop wiki`: https://github.com/ClockworkNet/wtop/wiki/Install


Testing Quick Start
===================

1. Change directory into repository (into same directory as where this README
   resides).
2. Install virtual environment::

    mkvirtualenv -a . -r tests/requirements.txt wtop_test

   a. If installing requirements errors, update `pip`::

        pip install --upgrade pip

   b. Install requirements::

        pip install -r tests/requirements.txt

3. Run pytest::

    py.test

To test against alternate Python versions, it may be useful to create virtual
environments with an interpreter other than the one with which ``virtualenv``
was installed, e.g. for non-default python3::

    mkvirtualenv -a $(pwd) -p $(which python3) -r tests/requirements.txt wtop_test3



Changelog
=========

See `CHANGELOG.rst`_.

.. _`CHANGELOG.rst`:
   https://github.com/ClockworkNet/wtop/blob/master/CHANGELOG.rst


Contributors
============

See `CONTRIBUTORS.rst`_.

.. _`CONTRIBUTORS.rst`:
   https://github.com/ClockworkNet/wtop/blob/master/CONTRIBUTORS.rst


License
=======

See `LICENSE.txt`_ (`BSD 3-Clause License`_).

.. _`LICENSE.txt`:
   https://github.com/ClockworkNet/wtop/blob/master/LICENSE.txt
.. _`BSD 3-Clause License`: http://www.opensource.org/licenses/BSD-3-Clause
