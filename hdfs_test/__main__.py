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
parser.set_defaults(url='')
args = parser.parse_args()

url = args.url
flush = args.flush
flushAll = args.flushAll

if (flushAll):
	subprocess.Popen("rm -f test.csv", shell=True)
if (flush or flushAll):
	subprocess.Popen("sh flush.sh", shell=True)
	sys.exit();
	
if (url != ''):
	subprocess.Popen("sh prepareTest.sh "+url, shell=True)
	
times = []

for x in range(0,9):
	start = timer()
	subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -put -f test.csv /user/admin/testing/test.csv", shell=True)
	end = timer()
	subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -f -skipTrash /user/admin/testing/test.csv", shell=True)
	times.append(end-start)
	
print "Average Speed for " + str(os.path.getsize("./test.csv")/pow(1024^3)) +" GB in upload: " + str(sum(times)/len(times))