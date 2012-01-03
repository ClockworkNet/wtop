#!/bin/sh
rm *.tar.gz
tar -cvz -T MANIFEST -f "wtop-`./logrep -V`.tar.gz"
