#!/bin/bash
yum install zip
cd /tmp/
wget http://data.gdeltproject.org/events/2003.zip
zip 2003.zip -d ./unzipped2003

python MC1.44.py