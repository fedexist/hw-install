## Imports

from pyspark import SparkConf, SparkContext

from operator import add
import time
import sys
## Constants
APP_NAME = " HelloWorld of Big Data"
##OTHER FUNCTIONS/CLASSES

def main(sc):
   sc.setLogLevel("WARN")
   #f = open("/root/hw_pre_install/test.csv")
   textFile = sc.textFile("file:///root/hw-pre-install/test.csv")
   textFile = sc.serialize(f)
   textFile.saveAsTextFile("hdfs:///user/admin/testing")

if __name__ == "__main__":

   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   # Execute Main functionality
   main(sc)