import argparse
import os
import subprocess
import time
from collections import namedtuple
from pexpect import run, pxssh


# Per ogni host in host_list
def ssh_setup(current_host, _username, _password, _scripts):
	print "ssh-copy-id to current host: %s" % current_host.IP
	
	shell_command = "chmod a+x %saskpass.sh " \
	                "&& %sssh_copy_id_script.sh %s %s %s %s" \
	                % (_scripts, _scripts, _password, _username, current_host.IP, _scripts + "askpass.sh")
	
	print "Executing command: \n\t%s" % shell_command
	
	subprocess.Popen(shell_command, shell=True)
	while not os.path.exists("/%s/.ssh/authorized_keys" % _username):
		time.sleep(1)
	try:
		if not current_host.AmbariServer:
			print "scp of keys for current host"
			run("scp /%s/.ssh/id_rsa /%s/.ssh/id_rsa.pub %s@%s:/%s/.ssh/"
			    % (_username, _username, _username, current_host.IP, _username))
	except pxssh.ExceptionPxssh as e:
		print "Error in ssh login:\n" + e.get_trace()


def setup(current_host, _username, ambari_server, _etc_host):
	ssh_session = pxssh.pxssh()
	ssh_session.PROMPT = '[PEXPECT]\\$ '
	print "Logging in to current host: %s" % current_host.IP
	try:
		ssh_session.login(current_host.IP, _username, ssh_key="/%s/.ssh/id_rsa" % _username, auto_prompt_reset=False)
	except pxssh.ExceptionPxssh as e:
		print "Error in login: %s" % e
		exit(-1)
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
	ssh_session.sendline("hostnamectl set-hostname %s" % current_host.FQDN)
	print "Updating /etc/hosts"
	for etc_host_line in _etc_host.split('\n'):
		ssh_session.sendline("echo \"%s\" | cat - >> /etc/hosts" % etc_host_line)
	ssh_session.prompt()
	print "Updating /etc/sysconfig/network"
	ssh_session.sendline("echo \"NETWORKING=YES\" | cat - >> /etc/sysconfig/network")
	ssh_session.prompt()
	ssh_session.sendline("echo \"HOSTNAME=%s\" | cat - >> /etc/sysconfig/network" % current_host.FQDN)
	ssh_session.prompt()
	ssh_session.sendline("yum install -y wget && "
	                     "wget -nv http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.4.2.0/ambari.repo "
	                     "-O /etc/yum.repos.d/ambari.repo")
	ssh_session.prompt()
	if current_host.AmbariServer:
		print "Installing Ambari Server"
		ssh_session.sendline("yum install -y ambari-server")
		ssh_session.prompt()
		ssh_session.sendline("ambari-server setup --silent")
		ssh_session.prompt()
		ssh_session.sendline("ambari-server start")
		ssh_session.prompt()
	else:
		print "Installing Ambari Agent"
		ssh_session.sendline("yum install -y ambari-agent")
		ssh_session.prompt()
		ssh_session.sendline("sed -i /s/hostname=.*/hostname=%s/g /etc/ambari-agent/conf/ambari-agent.ini" % ambari_server)
		ssh_session.prompt()
		ssh_session.sendline("ambari-agent start")
		ssh_session.prompt()

	print "Logging out"
	ssh_session.logout()


if __name__ == '__main__':
	# Parsing script arguments
	parser = argparse.ArgumentParser(description="Set up Hortonworks cluster")
	parser.add_argument('-p', '--password', help='Password used for every machine of the cluster', required=True)
	parser.add_argument('-u', '--username', help='Username used for every machine of the cluster (default: root)')
	parser.add_argument('-c', '--configuration', help="Path to the file containing the cluster configuration",
	                    type=file, required=True)
	parser.add_argument('-s', '--scripts', help="Path to the helper scripts askpass.sh and ssh_copy_id_script.sh"
	                                            "(default: './')")
	parser.set_defaults(username='root', password='', configuration='', scripts='./')
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
	
	print "Generating key pair"
	run("ssh-keygen -q -N \"\" ", events={'\w': '\r'})
	
	for host in host_list:
		ssh_setup(host, username, password, scripts)
		setup(host, username, ambari_server_fqdn, etc_host)