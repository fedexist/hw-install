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
parser.add_argument('-u', '--URL', help='URL of the dataset to use for testing, the file must be a single csv '
                                        'in a zip archive, if this parameter is not specified the dataset is assumed '
                                        'to have been downloaded already (default: blank)')
parser.add_argument('-r', '--reading', help="With this parameter the script will test the reading throughput of the HDFS"
                                            " instead of the default writing", action="store_true")
parser.add_argument('-f', '--flush', help="With this parameter the script will only clean up the HDFS",
                    action="store_true")
parser.add_argument('-fa', '--flushAll', help="With this parameter the script will clean up the HDFS and local files",
                    action="store_true")
parser.set_defaults(URL='')
args = parser.parse_args()

URL = args.URL
reading = args.reading
flush = args.flush
flushAll = args.flushAll

if flushAll:
	process = subprocess.Popen("rm -f test.csv", shell=True)
	process.wait()
if flush or flushAll:
	process = subprocess.Popen("sh flush.sh", shell=True)
	process.wait()
	sys.exit()
	
if URL != '':
	process = subprocess.Popen("yum install zip", shell=True)
	process.wait()
	process = subprocess.Popen("wget %s -O test.zip" % URL, shell=True)
	process.wait()
	process = subprocess.Popen("unzip test.zip", shell=True)
	process.wait()
	process = subprocess.Popen("mv *.csv test.csv", shell=True)
	process.wait()
	process = subprocess.Popen("rm -f test.zip", shell=True)
	process.wait()
	
times = []

if reading:
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -put -f test.csv /user/admin/testing/test.csv", shell=True)
	process.wait()
	process = subprocess.Popen("rm -f test.csv", shell=True)
	process.wait()
	
	for x in range(0, 9):
		start = timer()
		process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -get /user/admin/testing/test.csv test.csv", shell=True)
		process.wait()
		end = timer()
		process = subprocess.Popen("rm -f test.csv", shell=True)
		process.wait()
		times.append(end-start)
	
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -get /user/admin/testing/test.csv test.csv", shell=True)
	process.wait()
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -f -skipTrash /user/admin/testing/test.csv", shell=True)
	process.wait()
	
else:
	for x in range(0, 9):
		start = timer()
		process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -put -f test.csv /user/admin/testing/test.csv", shell=True)
		process.wait()
		end = timer()
		process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -f -skipTrash /user/admin/testing/test.csv", shell=True)
		process.wait()
		times.append(end-start)
	
print "Average Speed for %s GB: %s" \
        % (str(os.path.getsize("./test.csv")/pow(1024, 3)), str(sum(times)/len(times)))
