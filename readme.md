These script are meant to automate the process of setup for the [installation of an Hortonworks cluster](https://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/ch_Getting_Ready.html) via Ambari and testing of its capabilities.

It includes:

 * Passwordless SSH machines' setup
 * /etc/hosts and /etc/sysconfig/network autocomplete
 * Throughput and file integrity testing

## Command line arguments

        -h, --help          show this help message and exit
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
        -d DEFAULTPASSWORD, --defaultpassword DEFAULTPASSWORD
                            This is the default password for any Hortonworks
                            service default 'secret-password'
				

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

To test the file throughput run ```python -m hdfs_test``` with the use of the following arguments

  -h, --help            show this help message and exit
  -fr, --firstRun       With this parameter the script will prepare Hdfs
                        environment for testing
  -u URL, --URL URL     URL of the dataset to use for testing, the file must
                        be one or more CSVs in a zip or tar.gz archive or a
                        plain csv, if this parameter is not specified the
                        dataset, it is assumed to have been downloaded already
                        and present in dataset folder(default: blank)
  -z ZIP, --zip ZIP     Says what unpacker to use, zip, tar or none (default:
                        zip)
  -l, --load            Use this parameter to load the dataset to hdfs
  -t, --testing         With this parameter the script will test the reading
                        and writing throughput of the HDFS
  -f, --flush           With this parameter the script will only clean up the
                        HDFS
  -fa, --flushAll       With this parameter the script will clean up the HDFS
                        and local files
  -ti TESTITERATIONS, --testIterations TESTITERATIONS
                        Number of iterations done for testing (default: 1)
  -sa SPARKARGUMENTS, --sparkArguments SPARKARGUMENTS
                        The parameters to be sent to spark (default: "--master
                        yarn --num-executors 1 --executor-memory 1G")

For the first run, thus, use 

	python -m hdfs_test -fr
	
Then you may use 

	python -m hdfs_test -u https:\\your.url
	
	this will download the dataset on your host (suggested dataset: 'https://archive.ics.uci.edu/ml/machine-learning-databases/00344/Activity%20recognition%20exp.zip')

To test throughput on an average of two tests use
	
	python -m hdfs_test -t -ti 2
	
Example of use, first run, download dataset, load it to Hdfs and test throughput on 4 Yarn nodes with 2G each of Ram, on an average of 10 tests.

	python -m hdfs_test -fr -u 'https://archive.ics.uci.edu/ml/machine-learning-databases/00344/Activity%20recognition%20exp.zip' -z zip -l -t -ti 10 -sa "--master yarn --num-executors 4 --executor-memory 2G"
	