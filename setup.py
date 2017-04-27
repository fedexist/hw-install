from setuptools import setup

setup(
	name='hw_pre_install',
	version='0.0.1b',
	packages=['hw_pre_install', 'hdfs_test', 'hw_add_new_host'],
	url='',
	license='',
	author='Federico "fedexist" D\'Ambrosio',
	author_email='fedexist@gmail.com',
	description='Script to automate the setup of an Hortonworks cluster.',
	install_requires=['pexpect', 'ruamel.yaml']
)
