from distutils.core import setup

setup(
    name='wtop',
    version='0.6.1',

    data_files=[('/etc', ['wtop.cfg'])],
    scripts=['wtop', 'logrep'],
    py_modules=['logrep'],

    url="http://code.google.com/p/wtop/",
    author="Carlos Bueno",
    author_email="carlos@bueno.org"
)
