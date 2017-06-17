import os
import argparse
import subprocess


if __name__ == '__main__':
        parser = argparse.ArgumentParser(
                description='Run all queries',
                epilog='''"So we beat on, boats against the current, borne back ceaselessly into the past."''')
        parser.add_argument('queryFolder', type=str, help='Path to folder containing the queries', default='./')
        parser.add_argument('-d', 'database', type=str, help='Path to folder containing the queries',
                            default='', required=True)
        parser.add_argument('-n', '--username', type=str, help='Path to folder containing the queries', default='admin')
        parser.add_argument('-p', '--password', type=str, help='Path to folder containing the queries',
                            default='admin', required=True)

        args = parser.parse_args()
        print os.getcwd()
        os.chdir(args.queryFolder)
        print os.getcwd()
        for current_file in reversed(os.listdir(os.getcwd())):
            with open("hive_log.txt", 'a') as logger:
                if current_file.endswith(".sql"):
                    for i in range(5):
                        print("Executing (%s) " % str(i) + os.path.join(os.getcwd(), file))
                        process = subprocess.Popen("beeline -i testbench.settings "
                                                    "-u \"jdbc:hive2://master-2.localdomain:2181,"
                                                    "master-1.localdomain:2181/%s;serviceDiscoveryMode=zooKeeper;"
                                                    "zooKeeperNamespace=hiveserver2\" "
                                                    "-n %s -p %s -f %s"
                                                    % (args.database, args.username, args.password, current_file),
                                                    shell=True, stdout=logger)
                        process.wait()
