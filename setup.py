# Copyright 2017 Federico D'Ambrosio, Edoardo Ferrante
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http : //www.apache. org / licenses / LICENSE -2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


from setuptools import setup
import os

with open("LICENSE", 'r') as license_path:
	license = license_path.read()
	
requirements_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'requirements.txt')

with open(requirements_path) as requirements_file:
	requires = requirements_file.readlines()

setup(
	name='hw_install',
	version='0.0.2',
	packages=['hw_install', 'hdfs_test', 'hw_add_new_host'],
	url='https://github.com/fedexist/hw-install',
	license=license,
	author='Federico "fedexist" D\'Ambrosio, Edoardo "fleanend" Ferrante',
	author_email='fedexist@gmail.com, edoardoferrante@hotmail.it',
	description='Script to automate the setup of an Hortonworks cluster.',
	install_requires=requires
)
