from setuptools import setup

setup(
	name='hw_pre_install',
	version='0.0.1a',
	packages=['hw_pre_install', 'hdfs_test'],
	url='',
	license='',
	author='Federico "fedexist" D\'Ambrosio',
	author_email='fedexist@gmail.com',
	description='Script to automate the setup of an Hortonworks cluster.',
	install_requires=['pexpect']
)
