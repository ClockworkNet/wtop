import logrep 

## For historical reasons this package is called "wtop" even though 
## wtop is a paper-thin shell on a special case of logrep.

from distutils.core import setup
import os, os.path

cfg_file_path = logrep.cfg_home()

setup(
    name='wtop',
    version=logrep.VERSION,

    data_files=[(cfg_file_path, ['wtop.cfg'])],
    scripts=['wtop', 'logrep', 'wtop.bat', 'logrep.bat'],
    py_modules=['logrep'],

    url="http://code.google.com/p/wtop/",
    author="Carlos Bueno",
    author_email="carlos@bueno.org",

    license='BSD',
    description='running statistics for webservers, plus powerful log-grepping tools'
)
