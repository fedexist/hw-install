
This script is meant to automate the process of setup for the [installation of an Hortonworks cluster](https://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/ch_Getting_Ready.html) via Ambari.

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

    git clone https://github.com/fedexist/hw-pre-install.git
    cd hw-pre-install
    python setup.py install
    cd /wherever/you/want
	python -m hw_pre_install -p mypassword -u root -c /path/to/your-cluster.yaml -s /helper/scripts/folder/

Configuration file is a YAML file, formatted as it follow:

    ambari-server:
      IP: 192.168.1.1
      FQDN: master.localdomain
    hosts:
      - IP: 192.168.1.2
        FQDN: node1.localdomain
      - IP: 192.168.1.3
        FQDN: node2.localdomain
	
### To add a new host to  an existing cluster 

Update the YAML configuration file adding a new list with the tag ```new-hosts```, for example:
    
    # Original configuration file
    new-hosts:
      - IP: 192.168.1.35
        FQDN: new_node1.localdomain
      - IP: 192.168.1.36
        FQDN: new_node2.localdomain

Then, run

    python -m hw_add_new_host -p mypassword -u root -c /path/to/your-cluster.yaml -s /helper/scripts/folder/