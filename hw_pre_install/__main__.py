import argparse
import os
from ruamel import yaml
from collections import namedtuple
from hw_pre_install import ssh_setup, setup
from pexpect import run


# Parsing script arguments
parser = argparse.ArgumentParser(description="Set up Hortonworks cluster")
parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
parser.add_argument('-c', '--configuration', help="Path to the yaml configuration file", required=True)
parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
                                            " default './helpers/")
parser.set_defaults(username='root', password='', configuration='', scripts='./helpers/')
args = parser.parse_args()
	
Host = namedtuple("Host", "IP FQDN")

host_list = []
password = args.password
username = args.username
configuration = args.configuration
scripts = args.scripts
etc_host = ""
ambari_server = None
	
if not os.path.exists("%saskpass.sh" % scripts):
	print "Can't find %saskpass.sh!" % scripts
	exit(-1)
	
if not os.path.exists("%sssh_copy_id_script.sh" % scripts):
	print "Can't find %sssh_copy_id_script.sh!" % scripts
	exit(-1)
	
print "Helper scripts found, now processing cluster setup"

try:
	with open(configuration, 'r') as cluster_setup:
		config_file = yaml.load(cluster_setup.read(), Loader=yaml.Loader)
		ambari_server = Host(IP=config_file['ambari-server']['IP'],
		                     FQDN=config_file['ambari-server']['FQDN'])
		for host in config_file['hosts']:
			new_host = Host(IP=host['IP'],
				            FQDN=host['FQDN'])
			host_list.append(new_host)
			etc_host += "%s %s\n" % (new_host.IP, new_host.FQDN)
except yaml.YAMLError as err:
	print "Error in configuration file!\n" + err.message
	exit(-1)
except IOError as err:
	print "Cannot find configuration file!\n" + err.message
	exit(-1)

print "Generating key pair"
run("ssh-keygen -q -N \"\" ", events={'\w': '\r'})

# Start setup

# First setup ambari-server
ssh_setup(ambari_server, username, password, scripts)
setup(ambari_server, username, None, etc_host, is_ambari_server=True)

for host in host_list:
	ssh_setup(host, username, password, scripts)
	setup(host, username, ambari_server.FQDN, etc_host, is_ambari_server=False)
