
This script is meant to automate the process of setup for the [https://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/ch_Getting_Ready.html](installation of an Hortonworks cluster) via Ambari.

It includes:

 * Passwordless SSH machines' setup
 * /etc/hosts and /etc/sysconfig/network autocomplete

## Command line arguments

	  -h, --help            show this help message and exit
	  -p PASSWORD, --password PASSWORD
							Password used for every machine of the cluster
	  -u USERNAME, --username USERNAME
							Username used for every machine of the cluster
							(default: root)
	  -c CONFIGURATION, --configuration CONFIGURATION
							Path to the file containing the cluster configuration
	  -s SCRIPTS, --scripts SCRIPTS
							Path to the helper scripts askpass.sh and
							ssh_copy_id_script.sh(default: './')
							

## Usage

	python hw-pre-install.py -p mypassword -u root -c /root/cluster-setup.txt -s /root/
	
Configuration file must have a line for each machine in the cluster, each one containing machine's IP, FQDN and 0/1 whether the machine will have Ambari Server installed, for example:

	192.168.1.8 master.localdomain 1
	192.168.1.9 node1.localdomain 0
	192.168.1.10 node2.localdomain 0