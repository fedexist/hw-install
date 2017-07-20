init:
    wget https://public-repo-1.hortonworks.com/HDF/3.0.0.0/nifi-1.2.0.3.0.0.0-453-bin.zip
    unzip nifi-1.2.0.3.0.0.0-453-bin.zip -d /root/nifi/
    echo "alias nifi='/root/nifi/nifi-1.2.0.3.0.0.0-453/bin/nifi.sh'" >> .bash_profile
    source .bash_profile
    yum install -y openssl-devel
    # nifi.properties port should be changed
	pip install -r requirements.txt
	python setup.py install
	chmod 755 ./helpers/askpass.sh
	chmod 755 ./helpers/ssh_copy_id_script.sh