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


import subprocess
import sys
from timeit import default_timer as timer

repeat = 10
times = list()

if len(sys.argv) > 1:
	repeat = int(sys.argv[1])
	

for x in range(1, repeat):
	print "Step %s of %s" % (str(x), str(repeat))
	start = timer()
	process = subprocess.Popen("dd bs=1M count=10240 if=/dev/urandom of=foo.dat", shell=True)
	process.wait()
	end = timer()
	times.append(end - start)
	print "Time elapsed: %s" % (str(end - start))
	subprocess.Popen("rm -rf foo.dat", shell=True)

print "Average time for disk writing: " + str(sum(times)/len(times))
