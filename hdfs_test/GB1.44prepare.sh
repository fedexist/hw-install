#!/bin/bash
yum install zip
wget http://data.gdeltproject.org/events/2003.zip /tmp/2003.zip
unzip /tmp/2003.zip

python MC1.44.py