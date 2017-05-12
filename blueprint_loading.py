from ambariclient.client import Ambari
from ruamel import yaml

with open("config.yaml", 'r') as cluster_setup:
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

bp = {"stack_name": "HDP", "stack_version": '2.5'}
client.blueprints(bp_name).create(Blueprints=bp, host_groups=host_groups).wait()

client.clusters.create(name, blueprint=bp_name, default_password=passwd).wait(timeout=1800, interval=30)
