import subprocess

process = subprocess.Popen("ambari-server stop")
process.wait()