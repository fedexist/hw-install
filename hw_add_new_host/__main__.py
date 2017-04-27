import os
from collections import namedtuple
import argparse
from hw_pre_install.hw_pre_install import ssh_setup, update, setup

# This script is used to setup the addition of new hosts
# to an existing Ambari server

parser = argparse.ArgumentParser("Setup addition new host to existing ambari-server")
parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
                                            "(default: './')")
parser.add_argument('-c', '--configuration', help="File containing IPs and FQDNs of the new hosts", required=True,
                    type=file)
parser.set_defaults(username='root', password='',
                    configuration='',
                    scripts='./')
args = parser.parse_args()

Host = namedtuple("Host", "IP FQDN")

new_host_list = []
old_host_list = []
password = args.password
username = args.username
configuration = args.configuration
scripts = args.scripts

if not os.path.exists("%saskpass.sh" % scripts):
	print "Can't find %saskpass.sh!" % scripts
	exit(-1)

if not os.path.exists("%sssh_copy_id_script.sh" % scripts):
	print "Can't find %sssh_copy_id_script.sh!" % scripts
	exit(-1)

with open('./current_etc_host.txt', 'r') as old_host_config:
	file_string = old_host_config.read().splitlines(True)
	ambari_server_fqdn = file_string[0].strip('\r\n')
	for line in file_string[1:]:
		split_line = line.strip('\r\n').split(' ')
		old_host = Host(IP=split_line[0], FQDN=split_line[1])
		old_host_list.append(old_host)
	current_etc_host = ''.join(file_string[1:])
	
with configuration as new_host_config:
	content = new_host_config.readlines()
	content = [x.strip('\r\n') for x in content]
	for line in content:
		split_line = line.split(" ")
		new_host = Host(IP=split_line[0],
		                FQDN=split_line[1])
		new_host_list.append(new_host)
	

for new_host in new_host_list:
	current_etc_host += "\n%s %s\n" % (new_host.IP, new_host.FQDN)


for old_host in old_host_list:
	update(old_host, username, new_host_list)

for host in new_host_list:
	ssh_setup(host, username, password, scripts)
	setup(host, username, ambari_server_fqdn, current_etc_host, False)
