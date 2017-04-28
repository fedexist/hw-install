import argparse
import subprocess
import os
import sys
from timeit import default_timer as timer

# Parsing script arguments
parser = argparse.ArgumentParser(description="Test throughput")
parser.add_argument('-u', '--URL', help='URL of the dataset to use for testing, the file must be a single csv in a zip archive, if this parameter is not specified the dataset is assumed to have been downloaded already (default: blank)')
parser.add_argument('-f', '--flush', help="With this parameter the script will only clean up the HDFS", action="store_true")
parser.add_argument('-fa', '--flushAll', help="With this parameter the script will clean up the HDFS and local files", action="store_true")
parser.set_defaults(URL='')
args = parser.parse_args()

URL = args.URL
flush = args.flush
flushAll = args.flushAll

if (flushAll):
	process = subprocess.Popen("rm -f test.csv", shell=True)
	process.wait()
if (flush or flushAll):
	process = subprocess.Popen("sh flush.sh", shell=True)
	process.wait()
	sys.exit();
	
if (URL != ''):
	process = subprocess.Popen("yum install zip", shell=True)
	process.wait()
	process = subprocess.Popen("wget "+ URL +" -O test.zip", shell=True)
	process.wait()
	process = subprocess.Popen("unzip test.zip", shell=True)
	process.wait()
	process = subprocess.Popen("mv *.csv test.csv", shell=True)
	process.wait()
	process = subprocess.Popen("rm -f test.zip", shell=True)
	process.wait()
	
times = []

for x in range(0,9):
	start = timer()
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -put -f test.csv /user/admin/testing/test.csv", shell=True)
	process.wait()
	end = timer()
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -f -skipTrash /user/admin/testing/test.csv", shell=True)
	process.wait()
	times.append(end-start)
	
print "Average Speed for " + str(os.path.getsize("./test.csv")/pow(1024^3)) +" GB in upload: " + str(sum(times)/len(times))