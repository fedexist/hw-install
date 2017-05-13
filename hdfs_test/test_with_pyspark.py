# Imports

from pyspark import SparkConf, SparkContext

from operator import add
import time
import sys
import subprocess
from timeit import default_timer as timer

# Constants
APP_NAME = " HelloWorld of Big Data"


# OTHER FUNCTIONS/CLASSES


def main(sc):
	sc.setLogLevel("WARN")
	# f = open("/root/hw_pre_install/test.csv")
	
	times = []
	
	for x in range(0,9):
		start = timer()
		textFile = sc.textFile("file:///root/hw-pre-install/test.csv").cache()
		textFile.count()
		end = timer()
		times.append(end-start)
	print "Lettura da Unix e scrittura su RAM: " + str(sum(times)/len(times)))

	times = []
	
	for x in range(0,9):
		start = timer()
		textFile.saveAsTextFile("hdfs:///user/admin/testing/tmp")
		end = timer()
		times.append(end-start)
		process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -r -f -skipTrash /user/admin/testing/tmp", shell=True)
		process.wait()
		
	print "Scrittura su HDFS: " + str(sum(times)/len(times)))

	times = []
	
	for x in range(0,9):
		start = timer()
		textFile = sc.textFile("hdfs:///user/admin/testing/tmp").cache()
		textFile.count()
		end = timer()
		times.append(end-start)
	
	print "Lettura da HDFS e scrittura su RAM: " + str(sum(times)/len(times)))


if __name__ == "__main__":
	# Configure Spark
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf=conf)
	# Execute Main functionality
	main(sc)
