import subprocess
import sys
from timeit import default_timer as timer

repeat = 10
times = list()

if len(sys.argv) > 1:
	repeat = int(sys.argv[1])
	

for x in range(1, int(repeat)):
	start = timer()
	process = subprocess.Popen("dd bs=1M count=10240 if=/dev/urandom of=foo.dat")
	process.wait()
	end = timer()
	times.append(end - start)
	subprocess.Popen("rm -rf foo.dat")

print "Scrittura su disco media: " + str(sum(times)/len(times))
