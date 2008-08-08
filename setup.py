from distutils.core import setup
import os, os.path

cfg_file_path = '/etc'  #unix, osx, etc
# for the moment, wtop.cfg will live in the Windows user's home directory.
if os.name != 'posix' and os.environ.has_key('HOME'):
    cfg_file_path = os.environ.get('HOME')

setup(
    name='wtop',
    version='0.6.2-iis-experimental',

    data_files=[(cfg_file_path, ['wtop.cfg'])],
    scripts=['wtop', 'logrep'],
    py_modules=['logrep'],

    url="http://code.google.com/p/wtop/",
    author="Carlos Bueno",
    author_email="carlos@bueno.org",

    license='New BSD',
    description='running statistics for webservers, plus powerful log-grepping tools'
)
