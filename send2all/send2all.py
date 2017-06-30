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
import subprocess
import time
from pexpect import pxssh

def send2all(configuration,script,nm):

	args = parser.parse_args()
		
	Host = namedtuple("Host", "IP FQDN")

	host_list = []

	try:
		with open(configuration, 'r') as cluster_setup:
			config_file = yaml.load(cluster_setup.read(), Loader=yaml.Loader)
			
			for host in config_file['hosts']:
				new_host = Host(IP=host['IP'],
								FQDN=host['FQDN'])
				host_list.append(new_host)
			
	except yaml.YAMLError as err:
		print "Error in configuration file!\n" + err.message
		exit(-1)
	except IOError as err:
		print "Cannot find configuration file!\n" + err.message
		exit(-1)

	print "----------------------"
	print "Step 1 of %s " % str(len(host_list) + 1)
	print "----------------------"
	if nm == False:
		process = subprocess.Popen("%s" % script, shell=True)
		process.wait()
	else:
		print("Skipping master")
		
	for host in host_list:
		print "----------------------"
		print "Step %s of %s " % (str(host_list.index(host) + 2), str(len(host_list) + 1))
		print "----------------------"
		try:
			ssh_session = pxssh.pxssh(timeout=7200)
			print "Logging in to current host: %s" % host.FQDN
			try:
				ssh_session.login(host.FQDN, "root", ssh_key="/root/.ssh/id_rsa")
			except pxssh.ExceptionPxssh as e:
				print "Error in login: %s" % e
				exit(-1)
				
			print "Running %s" % script
			ssh_session.sendline("%s" % script)
			ssh_session.prompt()
			
			print "Logging out"
			ssh_session.logout()
		except pxssh.ExceptionPxssh as e:
			print "Error in ssh login:\n" + e.get_trace()
		except:
			print "Something went awry but not Pxssh"
