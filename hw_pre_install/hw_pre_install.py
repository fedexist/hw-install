import os
import subprocess
import time
from pexpect import run, pxssh


# Per ogni host in host_list
def ssh_setup(_current_host, _username, _password, _scripts):
	print "ssh-copy-id to current host: %s" % _current_host.IP
	
	shell_command = "%s/ssh_copy_id_script.sh %s %s %s %s" \
	                % (_scripts, _password, _username, _current_host.IP, _scripts + "/askpass.sh")
	
	print "Executing command: \n\t%s" % shell_command
	
	subprocess.Popen("chmod a+x %s/ssh_copy_id_script.sh" % _scripts, shell=True)
	subprocess.Popen("chmod a+x %s/askpass.sh" % _scripts, shell=True)
	subprocess.Popen(shell_command, shell=True)
	
	while not os.path.exists("/%s/.ssh/authorized_keys" % _username):
		time.sleep(1)
	try:
		if not _current_host.AmbariServer:
			print "scp of keys for current host"
			run("scp /%s/.ssh/id_rsa /%s/.ssh/id_rsa.pub %s@%s:/%s/.ssh/"
			    % (_username, _username, _username, _current_host.IP, _username))
	except pxssh.ExceptionPxssh as e:
		print "Error in ssh login:\n" + e.get_trace()


def setup(_current_host, _username, ambari_server, _etc_host, is_ambari_server):
	try:
		ssh_session = pxssh.pxssh(timeout=7200)
		# ssh_session.PROMPT = '[PEXPECT]\\$ '
		print "Logging in to current host: %s" % _current_host.IP
		try:
			ssh_session.login(_current_host.IP, _username, ssh_key="/%s/.ssh/id_rsa" % _username,
			                  # auto_prompt_reset=False
			                  )
		except pxssh.ExceptionPxssh as e:
			print "Error in login: %s" % e
			exit(-1)
		print "Increasing maximum number of file descriptors available"
		ssh_session.sendline("ulimit -n 10000")
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
		for etc_host_line in _etc_host.split('\n'):
			ssh_session.sendline("echo \"%s\" | cat - >> /etc/hosts" % etc_host_line)
		ssh_session.prompt()
		print "Updating /etc/sysconfig/network"
		ssh_session.sendline("echo \"NETWORKING=YES\" | cat - >> /etc/sysconfig/network")
		ssh_session.prompt()
		ssh_session.sendline("echo \"HOSTNAME=%s\" | cat - >> /etc/sysconfig/network" % _current_host.FQDN)
		ssh_session.prompt()
		ssh_session.sendline("wget -nv http://public-repo-1.hortonworks.com/ambari/centos7/2.x/updates/2.4.2.0/ambari.repo "
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
		else:
			print "Installing Ambari Agent"
			ssh_session.sendline("yum install -y ambari-agent")
			ssh_session.prompt()
			ssh_session.sendline(
				"sed -i s/hostname=.*/hostname=%s/g /etc/ambari-agent/conf/ambari-agent.ini" % ambari_server)
			ssh_session.prompt()
			ssh_session.sendline("ambari-agent start")
			ssh_session.prompt()
	
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
