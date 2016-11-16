#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

# Standard library
from __future__ import absolute_import, division, print_function
import distutils.sysconfig
import os.path
import site
import sys

# Setup
try:
    # Third-party
    from setuptools import setup
except ImportError:
    # Standard library
    from distutils.core import setup

# Local/library specific
import logrep


# For historical reasons this package is called "wtop" even though wtop is a
# paper-thin shell on a special case of logrep.


# Install config file appropriately
cfg_file_path = "etc"
if hasattr(sys, "real_prefix"):
    cfg_file_path = os.path.join(sys.prefix, cfg_file_path)
elif "--user" in sys.argv:
    cfg_file_path = os.path.join(site.USER_BASE, cfg_file_path)
else:
    cfg_file_path = os.path.join(distutils.sysconfig.get_python_lib(),
                                 cfg_file_path)

with open('README.rst') as file:
    long_description = file.read()

setup(author="Timid Robot Zehta",
      author_email="tim@clockwork.net",
      classifiers=["Environment :: Console",
                   "Intended Audience :: System Administrators",
                   "License :: OSI Approved :: BSD License",
                   "Topic :: System :: Logging",
                   "Topic :: Utilities"],
      data_files=[(cfg_file_path, ["wtop.cfg"])],
      description="'top' for Apache and other web servers, plus powerful log"
                  "grepping",
      download_url="https://github.com/ClockworkNet/wtop/releases",
      install_requires=["python-iqm"],
      license="BSD 3-Clause License",
      long_description=long_description,
      name="wtop",
      py_modules=["logrep"],
      scripts=["wtop", "logrep", "wtop.bat", "logrep.bat"],
      url="https://github.com/ClockworkNet/wtop",
      version=logrep.VERSION)
