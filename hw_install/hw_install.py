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


import subprocess
import time
from pexpect import pxssh
from ambariclient.client import Ambari


# Per ogni host in host_list
def ssh_setup(_current_host, _username, _password, _scripts, is_ambari_server):
	print "ssh-copy-id to current host: %s" % _current_host.IP
	
	shell_command = "%sssh_copy_id_script.sh %s %s %s %s" \
	                % (_scripts, _password, _username, _current_host.IP, _scripts + "askpass.sh")
	
	print "Executing command: \n\t%s" % shell_command
	
	subprocess.Popen("chmod 755 %sssh_copy_id_script.sh" % _scripts, shell=True)
	subprocess.Popen("chmod 755 %saskpass.sh" % _scripts, shell=True)
	subprocess.Popen(shell_command, shell=True)
	# Makes sure ssh-copy-id is actually terminated
	time.sleep(10)
	
	try:
		if not is_ambari_server:
			print "scp of keys for current host"
			process = subprocess.Popen("scp -q -o StrictHostKeyChecking=no /%s/.ssh/id_rsa /%s/.ssh/id_rsa.pub %s@%s:/%s/.ssh/"
			                           % (_username, _username, _username, _current_host.IP, _username), shell=True)
			process.wait()
	except pxssh.ExceptionPxssh as e:
		print "Error in ssh login:\n" + e.get_trace()


def setup(_current_host, _username, ambari_server, _etc_host, is_ambari_server
          # , mysql_password, default_password
         ):
	try:
		ssh_session = pxssh.pxssh(timeout=7200)
		print "Logging in to current host: %s" % _current_host.IP
		try:
			ssh_session.login(_current_host.IP, _username, ssh_key="/%s/.ssh/id_rsa" % _username)
		except pxssh.ExceptionPxssh as e:
			print "Error in login: %s" % e
			exit(-1)
		print "Increasing maximum number of file descriptors available"
		ssh_session.sendline("echo \"fs.file-max = 1000000\" | cat - >> /etc/sysctl.conf")
		ssh_session.prompt()
		ssh_session.sendline("echo \"* soft nofile 1000000\" | cat - >> /etc/security/limits.conf")
		ssh_session.prompt()
		ssh_session.sendline("echo \"* hard nofile 1000000\" | cat - >> /etc/security/limits.conf")
		ssh_session.prompt()
		ssh_session.sendline("echo \"* soft nproc 1000000\" | cat - >> /etc/security/limits.conf")
		ssh_session.prompt()
		ssh_session.sendline("echo \"* hard nproc 1000000\" | cat - >> /etc/security/limits.conf")
		ssh_session.prompt()
		print "Installing ntp and enabling ntpd"
		ssh_session.sendline("yum install -y ntp && systemctl enable ntpd && systemctl start ntpd")
		ssh_session.prompt()
		print "Disabling IP tables and firewalld"
		ssh_session.sendline("systemctl disable firewalld && service firewalld stop")
		ssh_session.prompt()
		print "Disabling SELinux and setting umask"
		ssh_session.sendline("setenforce 0 && echo umask 0022 >> /etc/profile")
		ssh_session.prompt()
		print "Setting hostname"
		ssh_session.sendline("hostnamectl set-hostname %s" % _current_host.FQDN)
		print "Updating /etc/hosts"
		ssh_session.sendline("sed -i /%s.*/d /etc/hosts" % _current_host.IP)
		ssh_session.prompt()
		for etc_host_line in _etc_host.split('\n'):
			ssh_session.sendline("echo \"%s\" | cat - >> /etc/hosts" % etc_host_line)
		ssh_session.prompt()
		print "Updating /etc/sysconfig/network"
		ssh_session.sendline("echo \"NETWORKING=YES\" | cat - >> /etc/sysconfig/network")
		ssh_session.prompt()
		ssh_session.sendline("echo \"HOSTNAME=%s\" | cat - >> /etc/sysconfig/network" % _current_host.FQDN)
		ssh_session.prompt()
		
		# ##fix dns resolution
		print "Updating ifcfg"
		ssh_session.sendline("echo \"DNS1='212.19.96.2'\" | cat - >> /etc/sysconfig/network-scripts/ifcfg-eth0")
		ssh_session.prompt()
		ssh_session.sendline("echo \"DNS2='212.19.108.1'\" | cat - >> /etc/sysconfig/network-scripts/ifcfg-eth0")
		ssh_session.prompt()
		ssh_session.sendline("echo \"DNS3='8.8.8.8'\" | cat - >> /etc/sysconfig/network-scripts/ifcfg-eth0")
		ssh_session.prompt()
		ssh_session.sendline("echo \"DNS4='8.8.4.4'\" | cat - >> /etc/sysconfig/network-scripts/ifcfg-eth0")
		ssh_session.prompt()
		ssh_session.sendline("systemctl restart network.service")
		ssh_session.prompt()
		time.sleep(5) # wait for network restart to take place
		
		ssh_session.sendline("yum install -y wget && "
		                     "wget -nv http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.4.2.0/ambari.repo "
		                     "-O /etc/yum.repos.d/ambari.repo")
		ssh_session.prompt()
		if is_ambari_server:
			print "Installing Ambari Server"
			ssh_session.sendline("yum install -y ambari-server")
			ssh_session.prompt()
			print "Setting up Ambari Silently"
			ssh_session.sendline("ambari-server setup --silent")
			ssh_session.prompt()
			print "Starting Ambari"
			ssh_session.sendline("ambari-server start")
			ssh_session.prompt()
		
		print "Installing Ambari Agent"
		ssh_session.sendline("yum install -y ambari-agent")
		ssh_session.prompt()
		ssh_session.sendline(
			"sed -i s/hostname=.*/hostname=%s/g /etc/ambari-agent/conf/ambari-agent.ini" % ambari_server)
		ssh_session.prompt()
		ssh_session.sendline("ambari-agent start")
		ssh_session.prompt()
		print "Starting mysqld, granting privileges to hive"
		# ssh_session.sendline("systemctl restart mysqld; mysql -u root -p%s -h localhost "
		#                      "-e \"GRANT ALL PRIVILEGES ON *.* TO  'hive'@'%%' IDENTIFIED BY '%s';"
		#                     "FLUSH PRIVILEGES;\"" % (mysql_password, default_password))
		# ssh_session.prompt()
		
		print "Logging out"
		ssh_session.logout()
	except pxssh.ExceptionPxssh as e:
		print "Error in ssh login:\n" + e.get_trace()
	except:
		print "Something went awry but not Pxssh"


def update(old_host, _username, new_host_list):
		ssh_session = pxssh.pxssh()
		ssh_session.login(old_host.IP, _username, ssh_key="/%s/.ssh/id_rsa" % _username)
		for new_host in new_host_list:
			ssh_session.sendline("echo \"%s %s\" | cat - >> /etc/hosts" % (new_host.IP, new_host.FQDN))
			ssh_session.prompt()
		ssh_session.logout()


def install_cluster(ambari_server, cluster_name, blueprint_name, blueprints, host_groups, default_password, configurations):
	print "Opening connection to Ambari server"
	client = Ambari(ambari_server.FQDN, port=8080, username='admin', password='admin')
	
	print "Registering specified blueprint"
	client.blueprints(blueprint_name).create(Blueprints=blueprints, host_groups=host_groups).wait()
	
	print "Creating cluster"
	client.clusters.create(cluster_name, blueprint=blueprint_name,
	                       host_groups=host_groups, default_password=default_password,
	                       configurations=configurations).wait(timeout=1800, interval=30)
