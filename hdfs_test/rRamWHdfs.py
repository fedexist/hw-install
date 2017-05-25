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
	# f = open("/root/hw_install/test.csv")
	

	start = timer()
	text_file.saveAsTextFile("hdfs:///user/admin/testing/tmp")
	end = timer()
	times.append(end-start)
	process = subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm -r -f -skipTrash /user/admin/testing/tmp", shell=True)
	process.wait()
		
	text_file.saveAsTextFile("hdfs:///user/admin/testing/tmp")
	print "Scrittura su HDFS: " + str(sum(times)/len(times))


if __name__ == "__main__":
	# Configure Spark
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf=conf)
	# Execute Main functionality
	main(sc)
