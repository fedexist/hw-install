# Scrive un file.
import os

with open('test', 'wb') as fout:
    fout.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large

