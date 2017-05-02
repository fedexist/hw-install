## Imports

from pyspark import SparkConf, SparkContext

from operator import add
import sys
## Constants
APP_NAME = " HelloWorld of Big Data"
##OTHER FUNCTIONS/CLASSES

def main(sc):
   textFile = sc.textFile("file:///hw_pre_install/test.csv")
   textFile.saveAsTextFile("hdfs:///user/admin/testing/test.csv")

if __name__ == "__main__":

   # Configure Spark
   conf = SparkConf().setAppName(APP_NAME)
   conf = conf.setMaster("local[*]")
   sc   = SparkContext(conf=conf)
   # Execute Main functionality
   main(sc)