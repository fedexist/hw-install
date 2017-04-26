# Scrive un file.
import os
import subprocess

#for x in range(0,5)
subprocess.check_output("time HADOOP_USER_NAME=hdfs hadoop fs -put -f test /user/admin/testing/2003.csv")