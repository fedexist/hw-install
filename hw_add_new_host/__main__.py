import os
from collections import namedtuple
import argparse
from ruamel import yaml
from hw_install import hw_install
from datetime import datetime
# This script is used to setup the addition of new hosts
# to an existing Ambari server


parser = argparse.ArgumentParser("Setup addition new host to existing ambari-server")
parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
                                            "(default: './helpers/')")
parser.add_argument('-c', '--configuration', help="Path to the yaml configuration file", required=True)
parser.set_defaults(username='root', password='',
                    configuration='',
                    scripts='./helpers/')
args = parser.parse_args()

Host = namedtuple("Host", "IP FQDN")

new_host_list = []
old_host_list = []
password = args.password
username = args.username
configuration = args.configuration
scripts = args.scripts
etc_host = ""
config_file = None

if not os.path.exists("%saskpass.sh" % scripts):
	print "Can't find %saskpass.sh!" % scripts
	exit(-1)

if not os.path.exists("%sssh_copy_id_script.sh" % scripts):
	print "Can't find %sssh_copy_id_script.sh!" % scripts
	exit(-1)

print "Processing configuration file"
try:
	with open(configuration, 'r') as cluster_setup:
		config_file = yaml.load(cluster_setup.read(), Loader=yaml.Loader)
		ambari_server = Host(IP=config_file['ambari-server']['IP'],
		                     FQDN=config_file['ambari-server']['FQDN'])
		old_host_list.append(ambari_server)
		etc_host = "%s %s\n" % (ambari_server.IP, ambari_server.FQDN)
		
		for old_host in config_file['hosts']:
			old_host_list.append(Host(IP=old_host['IP'], FQDN=old_host['FQDN']))
			etc_host += "%s %s\n" % (old_host['IP'], old_host['FQDN'])
			
		for new_host in config_file['new-hosts']:
			new_host_list.append(Host(IP=new_host['IP'], FQDN=new_host['FQDN']))
			etc_host += "%s %s\n" % (new_host['IP'], new_host['FQDN'])
			
except yaml.YAMLError as err:
	print "Error in configuration file!\n" + err.message
	exit(-1)
except IOError as err:
	print "Cannot find configuration file!\n" + err.message
	exit(-1)

print "Updating old hosts"
for old_host in old_host_list:
	hw_install.update(old_host, username, new_host_list)

print "Setting up new hosts"
for host in new_host_list:
	hw_install.ssh_setup(host, username, password, scripts, is_ambari_server=False)
	hw_install.setup(host, username, config_file['ambari-server']['FQDN'], etc_host, False)

# Write configuration file

print "Writing new configuration file"

with open("config" + str(datetime.now()).split('.')[0] + ".yaml", 'w') as cluster_setup:
	new_hosts = config_file.pop('new-hosts')
	for new_host in new_hosts:
		config_file['hosts'].append(new_host)
	yaml.dump(config_file, cluster_setup, Dumper=yaml.RoundTripDumper)


