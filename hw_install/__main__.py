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


import argparse
import os
from ruamel import yaml
from collections import namedtuple
from hw_install import ssh_setup, setup, install_cluster
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
	print "Step %s of %s " % (str(host_list.index(host) + 2), str(len(host_list) + 1))
	print "----------------------"
	ssh_setup(host, username, password, scripts, is_ambari_server=False)
	setup(host, username, ambari_server.FQDN, etc_host, is_ambari_server=False)

print "----------------------"
print "Now installing specified cluster"
print "----------------------"

install_cluster(ambari_server, cluster_name=cluster_name, blueprint_name=blueprint_name, blueprints=blueprints,
                host_groups=host_groups, default_password=default_password)
