## Imports

from pyspark import SparkConf, SparkContext

from operator import add
import time
import sys
from timeit import default_timer as timer
## Constants
APP_NAME = " HelloWorld of Big Data"
##OTHER FUNCTIONS/CLASSES

def main(sc):
   sc.setLogLevel("WARN")
   #f = open("/root/hw_pre_install/test.csv")
   start = timer()
   textFile = sc.textFile("file:///root/hw-pre-install/test.csv")
   #textFile = sc.serialize(f)
   textFile.saveAsTextFile("hdfs:///user/admin/testing/tmp")
   end = timer()
   print end-start

if __name__ == "__main__":

   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   # Execute Main functionality
   main(sc)