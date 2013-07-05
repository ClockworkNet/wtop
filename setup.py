# vim: set fileencoding=utf-8 :
# Standard library
from distutils.core import setup
# Project
import logrep

# For historical reasons this package is called "wtop" even though wtop is a
# paper-thin shell on a special case of logrep.

cfg_file_path = logrep.cfg_home()

setup(
    name="wtop",
    version=logrep.VERSION,

    data_files=[(cfg_file_path, ["wtop.cfg"])],
    scripts=["wtop", "logrep", "wtop.bat", "logrep.bat"],
    py_modules=["logrep"],

    url="https://github.com/ClockworkNet/wtop",
    author="Timid Robot Zehta",
    author_email="tim@clockwork.net",

    license="BSD",
    description="running statistics for webservers, plus powerful "
                "log-grepping tools"
)
