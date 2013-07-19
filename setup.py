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

setup(name="wtop",
      version=logrep.VERSION,
      author="Timid Robot Zehta",
      author_email="tim@clockwork.net",
      url="https://github.com/ClockworkNet/wtop",
      description="running statistics for webservers, plus powerful "
                  "log-grepping tools",
      long_description=long_description,
      download_url="https://github.com/ClockworkNet/wtop/releases",
      classifiers=["Environment :: Console",
                   "License :: OSI Approved :: BSD License",
                   "Topic :: System :: Logging",
                   "Topic :: Utilities"],
      data_files=[(cfg_file_path, ["wtop.cfg"])],
      scripts=["wtop", "logrep", "wtop.bat", "logrep.bat"],
      py_modules=["logrep"],
)
