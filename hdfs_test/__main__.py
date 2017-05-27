# Copyright 2017 Federico D'Ambrosio, Edoardo Ferrante
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http : //www.apache. org / licenses / LICENSE -2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


import argparse
import subprocess
import os
import sys
from timeit import default_timer as timer

# Parsing script arguments
parser = argparse.ArgumentParser(description="Test writing or reading throughput of HDFS")
parser.add_argument('-fr', '--firstRun', help="With this parameter the script will prepare Hdfs environment for testing",
                    action="store_true")
parser.add_argument('-u', '--URL', help='URL of the dataset to use for testing, the file must be one or more CSVs '
                                        'in a zip or tar.gz archive or a plain csv, if this parameter is not specified the dataset, it is assumed '
                                        'to have been downloaded already and present in dataset folder(default: blank)')
parser.add_argument('-z', '--zip', help="Says what unpacker to use, zip, tar or none (default: zip)")
parser.add_argument('-l', '--load', help="Use this parameter to load the dataset to hdfs",
                    action="store_true")
parser.add_argument('-t', '--testing', help="With this parameter the script will test the reading and writing throughput of the HDFS", action="store_true")
parser.add_argument('-f', '--flush', help="With this parameter the script will only clean up the HDFS",
                    action="store_true")

parser.add_argument('-fa', '--flushAll', help="With this parameter the script will clean up the HDFS and local files",
                    action="store_true")
parser.add_argument('-ti', '--testIterations',	help='Number of iterations done for testing (default: 1)')				
parser.add_argument('-sa', '--sparkArguments', help='The parameters to be sent to spark (default: "--master yarn --num-executors 1 --executor-memory 1G")')
parser.set_defaults(URL='', zip='zip', testIterations = '1', sparkArguments='--master yarn --num-executors 1 --executor-memory 1G')
args = parser.parse_args()

firstRun = args.firstRun
URL = args.URL
testing = args.testing
flush = args.flush
flushAll = args.flushAll
loading = args.load
ti = args.testIterations
sparkArguments = args.sparkArguments

if firstRun:
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/", shell=True)
	process.wait()
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/", shell=True)
	process.wait()
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/testing/", shell=True)
	process.wait()
	process = subprocess.Popen("chmod 755 /root/", shell=True)
	process.wait()


if flushAll:
	process = subprocess.Popen("rm -f test.csv", shell=True)
	process.wait()
if flush or flushAll:
	process = subprocess.Popen("sh flush.sh", shell=True)
	process.wait()
	sys.exit()
	
	
#http://static.echonest.com/millionsongsubset_full.tar.gz
#https://archive.ics.uci.edu/ml/machine-learning-databases/00344/Activity%20recognition%20exp.zip
if URL != '':
	if zip == 'zip':
		process = subprocess.Popen("yum install zip", shell=True)
		process.wait()
		process = subprocess.Popen("wget %s -O test.zip" % URL, shell=True)
		process.wait()
		process = subprocess.Popen("unzip test.zip -d ./dataset/", shell=True)
		process.wait()
		#process = subprocess.Popen("mv *.csv test.csv", shell=True)
		#process.wait()
		process = subprocess.Popen("rm -f test.zip", shell=True)
		process.wait()
	elif zip == 'tar':
		process = subprocess.Popen("yum install tar", shell=True)
		process.wait()
		process = subprocess.Popen("wget %s -O test.tar.gz" % URL, shell=True)
		process.wait()
		process = subprocess.Popen("tar -xzf test.tar.gz -C ./dataset/", shell=True)
		process.wait()
		#process = subprocess.Popen("mv *.csv test.csv", shell=True)
		#process.wait()
		process = subprocess.Popen("rm -f test.tar.gz", shell=True)
		process.wait()
	else:
		process = subprocess.Popen("wget %s -O ./dataset/test.csv" % URL, shell=True)

if loading:
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -copyFromLocal -f ./dataset /user/admin/testing/dataset", shell=True)
	process.wait()
	
times = []

if testing:

	
	for x in range(0, int(ti)):
		start = timer()
		process = subprocess.Popen("sudo -u hdfs spark-submit %s ./hdfs_test/rHdfsWRam.py" % sparkArguments, shell=True)
		process.wait()
		end = timer()
		process = subprocess.Popen("sudo -u hdfs spark-submit %s ./hdfs_test/rRamWHdfs.py" % sparkArguments, shell=True)
		process.wait()
		times.append(end-start)

