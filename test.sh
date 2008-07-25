#!/bin/sh
perl test.pl > new-test && diff last-test new-test