import os
import argparse


if __name__ == '__main__':
        parser = argparse.ArgumentParser(
                description='Run all queries',
                epilog='''"So we beat on, boats against the current, borne back ceaselessly into the past."''')
        parser.add_argument('queryFolder', type=str,
                                                help='Path to folder containing the queries', default = './')

        args = parser.parse_args()
        print os.getcwd()
        os.chdir(args.queryFolder)
        print os.getcwd()
        for file in reversed(os.listdir(os.getcwd())):
                if file.endswith(".sql"):
                        #print(os.path.join(os.getcwd(), file))
						process = subprocess.Popen("/bin/beeline -i testbench.settings -u jdbc:hive2://localhost:10000 -n admin -p admin -f %s" % file, shell=True)
						process.wait()