import os
import argparse
import subprocess
import datetime


if __name__ == '__main__':
        parser = argparse.ArgumentParser(
                description='Run all queries',
                epilog='''"So we beat on, boats against the current, borne back ceaselessly into the past."''')
        parser.add_argument('-f', '--folder', type=str, help='Path to folder containing the queries', default='./')
        parser.add_argument('-d', '--database', type=str, help='Path to folder containing the queries',
                            default='', required=True)
        parser.add_argument('-n', '--username', type=str, help='Path to folder containing the queries', default='admin')
        parser.add_argument('-p', '--password', type=str, help='Path to folder containing the queries',
                            default='admin', required=True)

        args = parser.parse_args()
        print os.getcwd()
        os.chdir(args.folder)
        print os.getcwd()
        for current_file in reversed(sorted(os.listdir(os.getcwd()))):
            with open("./hive_test.log", 'a') as logger:
                if current_file.endswith(".sql"):
                    for i in range(5):
                        logger.write("%s: Executing (%s) %s\n" % (datetime.datetime.utcnow(), str(i),  current_file))
                        process = subprocess.Popen("beeline -i %s "
                                                   "-u \"jdbc:hive2://master-2.localdomain:2181,"
                                                   "master-1.localdomain:2181/%s;serviceDiscoveryMode=zooKeeper;"
                                                   "zooKeeperNamespace=hiveserver2-hive2\" "
                                                   "-n %s -p %s -f %s"
                                                   % (os.path.join(os.getcwd(), "testbench.settings"), args.database, args.username, args.password, current_file),
                                                   shell=True)
                        process.wait()
                        logger.write("%s: Finished executing (%s) %s\n" % (datetime.datetime.utcnow(), str(i), current_file))
