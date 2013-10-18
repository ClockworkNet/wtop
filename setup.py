#!/usr/bin/env python
try:
    # Third-party
    from setuptools import setup
except ImportError:
    # Standard library
    from distutils.core import setup
# Project
import logrep

# For historical reasons this package is called "wtop" even though wtop is a
# paper-thin shell on a special case of logrep.

cfg_file_path = logrep.cfg_home()

with open('README.rst') as file:
    long_description = file.read()

setup(
      author="Timid Robot Zehta",
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
      version=logrep.VERSION,
)
