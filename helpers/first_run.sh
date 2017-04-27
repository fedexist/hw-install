#!/bin/sh

yum -y update
yum install -y epel-release
yum install -y python-pip
yum install -y wget
pip install setuptools