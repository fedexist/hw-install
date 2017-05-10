# Imports

from pyspark import SparkConf, SparkContext

from operator import add
import time
import sys
from timeit import default_timer as timer

# Constants
APP_NAME = " HelloWorld of Big Data"


# OTHER FUNCTIONS/CLASSES


def main(sc):
	sc.setLogLevel("WARN")
	# f = open("/root/hw_pre_install/test.csv")
	start = timer()
	textFile = sc.textFile("file:///root/hw-pre-install/test.csv").cache()
	textFile.count()
	end = timer()
	
	print "Copia da Unix: " + str(end - start)

	
	start = timer()
	textFile = sc.serialize(f)
	textFile.saveAsTextFile("hdfs:///user/admin/testing/tmp")
	end = timer()
	
	print "Scrittura su HDFS: " + str(end - start)
	
	start = timer()
	textFile = sc.textFile("hdfs:///user/admin/testing/tmp").cache()
	textFile.count()
	end = timer()
	
	print "Lettura da HDFS e scrittura su RAM: " + str(end - start)


if __name__ == "__main__":
	# Configure Spark
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf=conf)
	# Execute Main functionality
	main(sc)
