These script are meant to automate the process of setup for the [installation of an Hortonworks cluster](https://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/ch_Getting_Ready.html) via Ambari and testing of its capabilities.

It includes:

 * Passwordless SSH machines' setup
 * /etc/hosts and /etc/sysconfig/network autocomplete
 * Throughput and file integrity testing

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
							ssh_copy_id_script.sh(default: './helpers/')
							

## Usage

1. Install ```pip```
2. ```git clone https://github.com/fedexist/hw-install.git```
3. ```cd hw-install```
4. ```make init```

Then,

    cd /wherever/you/want/
	python -m hw_install -p mypassword -u root -c /path/to/your-cluster.yaml -s /helper/scripts/folder/ -d your-secret-password

Configuration file is a YAML file, formatted as it follows:

    cluster-name: cluster_name
    blueprint-name: blueprint_name
    Blueprints:
        stack_name: HDP
        stack_version: 2.5
    ambari-server:
      IP: 192.168.1.1
      FQDN: master.localdomain
    hosts:
      - IP: 192.168.1.2
        FQDN: node1.localdomain
      - IP: 192.168.1.3
        FQDN: node2.localdomain
    host-groups:
      - name: master
        hosts:
          - fqdn: master.localdomain
        components:
          - name: YARN_CLIENT
          - name: HDFS_CLIENT
          - name: AMBARI_SERVER

	
### To add a new host to  an existing cluster [CURRENTLY NOT WORKING]

Update the YAML configuration file adding a new list with the tag ```new-hosts```, for example:
    
    # Original configuration file
    new-hosts:
      - IP: 192.168.1.35
        FQDN: new_node1.localdomain
      - IP: 192.168.1.36
        FQDN: new_node2.localdomain

Then, run

    python -m hw_add_new_host -p mypassword -u root -c /path/to/your-cluster.yaml -s /helper/scripts/folder/
    
Your original configuration file will be overwritten with the new cluster configuration.

### To use testing scripts

Firstly, run 

	sh hdfs_test/create.sh
	
Then to check file integrity on HDFS you may run

	sh hdfs_test/test.sh
	
To test the file throughput run instead ```python -m hdfs_test``` with the use of the following arguments

	  -h, --help         show this help message and exit
	  -u URL, --URL URL  URL of the dataset to use for testing, the file must be a
						 single csv in a zip archive, if this parameter is not
						 specified, the dataset is assumed to have been downloaded
						 already (default: blank)
	  -r, --reading      With this parameter the script will test the reading
						 throughput of the HDFS instead of the default writing
	  -f, --flush        With this parameter the script will only clean up the
						 HDFS
	  -fa, --flushAll    With this parameter the script will clean up the HDFS and
						 local files

For the first run, thus, use 

	python -m hdfs_test -u https:\\your.url
	
	this will download the dataset and test the writing throughput of the hdfs (suggested dataset: http://data.gdeltproject.org/events/2003.zip)

To test again use
	
	python -m hdfs_test
	
After that to test the reading throughput use

	python -m hdfs_test -r
	