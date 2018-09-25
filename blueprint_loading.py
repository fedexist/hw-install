import argparse
from collections import namedtuple
from ruamel import yaml
from hw_install import hw_install

parser = argparse.ArgumentParser(description="Install cluster from blueprints")
parser.add_argument('-d', '--defaultpassword', help="This is the default password for any Hortonworks service"
                                                    " default 'secret-password'", required=True)
parser.add_argument('-c', '--configuration', help="Path to the yaml configuration file", required=True)
parser.set_defaults(defaultpassword='secret-password')

args = parser.parse_args()

configuration = args.configuration
default_password = args.defaultpassword

Host = namedtuple("Host", "IP FQDN")

with open(configuration, 'r') as cluster_setup:
    config_file = yaml.load(cluster_setup.read(), Loader=yaml.Loader)
    ambari_server = Host(IP=config_file['ambari-server']['IP'],
                         FQDN=config_file['ambari-server']['FQDN'])

    host_groups = config_file['host-groups']
    for group in host_groups:
        group['cardinality'] = str(len(group['hosts']))

    blueprints = config_file["Blueprints"]
    blueprint_name = config_file["blueprint-name"]
    cluster_name = config_file["cluster-name"]

hw_install.install_cluster(ambari_server, cluster_name=cluster_name, blueprint_name=blueprint_name,
                           blueprints=blueprints, host_groups=host_groups, default_password=default_password)
