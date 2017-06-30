
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


import argparse
import os
from ruamel import yaml
from collections import namedtuple
import subprocess
import time
from pexpect import pxssh
from send2all import send2all

# Parsing script arguments
parser = argparse.ArgumentParser(description="Send script to each machine")
parser.add_argument('-c', '--configuration', help="Path to the yaml configuration file", required=True)
parser.add_argument('-s', '--script', help="Script to run on each machine", required=True)
parser.add_argument('-nm', '--noMaster', help="If set the script will not run on master",
                    action="store_true")

args = parser.parse_args()
configuration = args.configuration
script = args.script
nm = args.noMaster
	
send2all(configuration,script,nm)