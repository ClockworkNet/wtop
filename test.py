#!/bin/python

# basic correctness and performance checks. Essentially we
# have a list of invocations and check the md5 of their 
# output and running time against a previously-saved run.

prefix = './logrep -c wtop.cfg'
suffix = 'access.log | md5 -q'
tests = (
    ("-o", 'url,msec,bot'),
    "-o", 'url,msec,ts'),
    "-o", 'url,msec,class'",
    "-o", 'url,msec,bot,ts,class'",
    "-f", 'url!~/q/,msec>500' -o 'url,msec,bot,ts,class'",
    "-f", 'url!~/q/,msec<500' -o 'url,msec,bot,ts,class,bytes'",
    ("-f", 'url!~/q/,msec<500,bot=1', '-o', 'url,msec,bot,ts,class,bytes'),
)


import time, os, sys, cPickle
from subprocess import call

def run_tests(tests, prefix, suffix):
    for t in tests:
        op.popen()
