import argparse
import os
from collections import namedtuple
from hw_pre_install import ssh_setup, setup
from pexpect import run


# Parsing script arguments
parser = argparse.ArgumentParser(description="Set up Hortonworks cluster")
parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
parser.add_argument('-c', '--configuration', help="Path to the file containing the cluster configuration",
	                    type=file, required=True)
parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
                                            " default './helpers/")
parser.set_defaults(username='root', password='', configuration='', scripts='./helpers/')
args = parser.parse_args()
	
Host = namedtuple("Host", "IP FQDN AmbariServer")
	
host_list = []
password = args.password
username = args.username
configuration = args.configuration
scripts = args.scripts
etc_host = ""
ambari_server_fqdn = ""
	
if not os.path.exists("%saskpass.sh" % scripts):
	print "Can't find %saskpass.sh!" % scripts
	exit(-1)
	
if not os.path.exists("%sssh_copy_id_script.sh" % scripts):
	print "Can't find %sssh_copy_id_script.sh!" % scripts
	exit(-1)
	
print "Helper scripts found, now processing cluster setup"
	
with configuration as cluster_setup:
	content = cluster_setup.readlines()
	content = [x.strip('\r\n') for x in content]
	for line in content:
		split_line = line.split(" ")
		new_host = Host(IP=split_line[0],
			            FQDN=split_line[1],
			            AmbariServer=(split_line[2] == '1'))
		host_list.append(new_host)
		if new_host.AmbariServer:
			ambari_server_fqdn = new_host.FQDN
		etc_host += "%s %s\n" % (new_host.IP, new_host.FQDN)

# Save current configuration
with open('./current_etc_host.txt', 'w') as current_config:
	current_config.writelines([ambari_server_fqdn, '\n', etc_host])


print "Generating key pair"
run("ssh-keygen -q -N \"\" ", events={'\w': '\r'})

# Start setup
for host in host_list:
	ssh_setup(host, username, password, scripts)
	setup(host, username, ambari_server_fqdn, etc_host, host.AmbariServer)
