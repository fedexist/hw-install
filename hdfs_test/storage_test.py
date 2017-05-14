import subprocess
import sys
from timeit import default_timer as timer

repeat = sys.argv[0]
times = list()

if repeat == "":
	repeat = 10

for x in range(1, int(repeat)):
	start = timer()
	process = subprocess.Popen("dd bs=1M count=10240 if=/dev/urandom of=foo.dat")
	process.wait()
	end = timer()
	times.append(end - start)
	subprocess.Popen("rm -rf foo.dat")

print "Scrittura su disco media: " + str(sum(times)/len(times))
