# Scrive un file.
import os
import subprocess
from timeit import default_timer as timer

times = []

for x in range(0,9):
	start = timer()
	subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -put -f 2003.csv /user/admin/testing/2003.csv", shell=True)
	end = timer()
	subprocess.Popen("HADOOP_USER_NAME=hdfs hadoop fs -rm /user/admin/testing/2003.csv", shell=True)
	times.append(end-start)
	

print "Average Speed for 1.44 GB in upload: " + str(sum(times)/len(times))