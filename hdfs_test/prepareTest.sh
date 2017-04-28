#!/bin/sh
yum install zip
wget $1 -O test.zip
unzip test.zip
mv *.csv test.csv
rm -f test.zip