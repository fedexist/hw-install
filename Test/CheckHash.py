import hashlib
import sys

path = sys.argv[1]
hashCandidate = hashlib.md5(open(path, 'rb').read()).hexdigest()
hashTest = hashlib.md5(open('test', 'rb').read()).hexdigest()

if hashTest == hashCandidate:
    print 'File check passed!'
else:
    print 'File check failed'
