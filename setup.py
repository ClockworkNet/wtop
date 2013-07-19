# vim: set fileencoding=utf-8 :
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
                   "License :: OSI Approved :: BSD License",
                   "Topic :: System :: Logging",
                   "Topic :: Utilities"],
      data_files=[(cfg_file_path, ["wtop.cfg"])],
      description="running statistics for webservers, plus powerful "
                  "log-grepping tools",
      download_url="https://github.com/ClockworkNet/wtop/releases#egg=wtop",
      license="BSD",
      long_description=long_description,
      name="wtop",
      py_modules=["logrep"],
      scripts=["wtop", "logrep", "wtop.bat", "logrep.bat"],
      url="https://github.com/ClockworkNet/wtop",
      version=logrep.VERSION,
)
