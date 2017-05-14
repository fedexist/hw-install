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

#!/bin/bash
python CreateFile.py
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/
HADOOP_USER_NAME=hdfs hadoop fs -mkdir /user/admin/testing/
HADOOP_USER_NAME=hdfs hadoop fs -put -f test /user/admin/testing/test
