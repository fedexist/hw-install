#!/bin/bash
python CreateFile.py
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/testing/
HADOOP_USER_NAME=hdfs hadoop fs -put -f test /user/admin/testing/test
