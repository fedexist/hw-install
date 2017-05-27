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
##HADOOP_USER_NAME=hdfs hadoop fs -put -f ../test.csv /user/admin/testing/test.csv


def main(sc):
	sc.setLogLevel("WARN")
	# f = open("/root/hw_install/test.csv")
	
	joinable = []
	
	cmd = ['hdfs', 'dfs', '-find', 'user/admin/testing/dataset', '-name', '*.csv']
	files = subprocess.check_output(cmd).strip().split('\n')
	for path in files:
		print path
		#joinable.append(sc.textFile(path))
		
	'''text_file = sc.textFile("hdfs:///user/admin/testing/test.csv").cache()
	
	start = timer()
	text_file.saveAsTextFile("hdfs:///user/admin/testing/tmp")
	end = timer()

	print "Scrittura su HDFS: " + str(end-start)'''


if __name__ == "__main__":
	# Configure Spark
	conf = SparkConf().setAppName(APP_NAME)
	#conf = conf.setMaster("local[*]")
	sc = SparkContext(conf=conf)
	# Execute Main functionality
	main(sc)
