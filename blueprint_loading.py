from ambariclient.client import Ambari
from ruamel import yaml

with open("experimental_config.yaml", 'r') as cluster_setup:
	config_file = yaml.load(cluster_setup.read(), Loader=yaml.Loader)

client_ip = "ip"
name = "GrebeCluster"
bp_name = "GCBlueprint"
host_groups = config_file['host-groups']

for group in host_groups:
	group['cardinality'] = str(len(group['hosts']))

passwd = "grebeteam"

hosts = [config_file['ambari-server']['FQDN']]

for host in config_file['hosts']:
	hosts.append(host['FQDN'])

client = Ambari(client_ip, port=8080, username='admin', password='admin')

# with open("/root/.ssh/id_rsa") as f:          should not be needed
# 	ssh_key = f.read()
#
# client.bootstrap(hosts=hosts, ssh_key=ssh_key, user='root').wait()
#

client.clusters.create(name, blueprint=bp_name, host_groups=host_groups, default_password=passwd)\
	.wait(timeout=1800, interval=30)
