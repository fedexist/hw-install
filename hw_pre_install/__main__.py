import argparse
import os
from ruamel import yaml
from collections import namedtuple
from hw_pre_install import ssh_setup, setup
from ambariclient.client import Ambari
from pexpect import run


# Parsing script arguments
parser = argparse.ArgumentParser(description="Set up Hortonworks cluster")
parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
parser.add_argument('-c', '--configuration', help="Path to the yaml configuration file", required=True)
parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
                                            " default './helpers/")
parser.add_argument('-d', '--defaultpassword', help="This is the default password for any Hortonworks service"
                                                    " default 'secret-password'", required=True)
parser.set_defaults(username='root', password='', configuration='',
                    scripts='./helpers/', defaultpassword='secret-password')
args = parser.parse_args()
	
Host = namedtuple("Host", "IP FQDN")

host_list = []
password = args.password
username = args.username
configuration = args.configuration
scripts = args.scripts
default_password = args.defaultpassword
etc_host = ""
blueprint_name = ""
blueprints = ""
host_groups = {}
cluster_name = ""

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
		etc_host += "%s %s\n" % (ambari_server.IP, ambari_server.FQDN)
		for host in config_file['hosts']:
			new_host = Host(IP=host['IP'],
				            FQDN=host['FQDN'])
			host_list.append(new_host)
			etc_host += "%s %s\n" % (new_host.IP, new_host.FQDN)
			
		host_groups = config_file['host-groups']
		for group in host_groups:
			group['cardinality'] = str(len(group['hosts']))
		
		blueprints = config_file["Blueprints"]
		blueprint_name = config_file["blueprint-name"]
		cluster_name = config_file["cluster-name"]
		
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
print "----------------------"
print "Step 1 of %s " % str(len(host_list) + 1)
print "----------------------"
ssh_setup(ambari_server, username, password, scripts, is_ambari_server=True)
setup(ambari_server, username, ambari_server.FQDN, etc_host, is_ambari_server=True)

for host in host_list:
	print "----------------------"
	print "Step %s of %s " % (str(host_list.index(host) + 1), str(len(host_list) + 1))
	print "----------------------"
	ssh_setup(host, username, password, scripts, is_ambari_server=False)
	setup(host, username, ambari_server.FQDN, etc_host, is_ambari_server=False)

client = Ambari(ambari_server.FQDN, port=8080, username='admin', password='admin')
client.blueprints(blueprint_name).create(Blueprints=blueprints, host_groups=host_groups).wait()
client.clusters.create(cluster_name, blueprint=blueprint_name, default_password=default_password)\
	.wait(timeout=1800, interval=30)
