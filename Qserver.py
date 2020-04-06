import paramiko
import json
import logging
import datetime
import os.path

config = 'config.json'

logging.basicConfig(filename=datetime.datetime.today().strftime("%Y_%m_%d.log"), format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


class Qserver:
    """Boundary"""

    def __init__(self):
        self.data = {}
        self.parse_config()
        self.available = self.test_connection()
        self.utc_folders = []
        self.utc_files = []

    def parse_config(self):
        if os.path.exists(config):
            try:
                with open(config) as f:
                    self.data = json.load(f)
            except:
                logging.info("Could not read config.json")
        else:
            logging.info("Missing config.json")

    def test_connection(self):
        try:
            logging.info("Connection to {}".format(self.data['ip']))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.data['ip'], port=self.data['port'], username=self.data['username'], password=self.data['password'])
            ssh.close()
            logging.info("Connection OK")
            return True
        except:
            logging.error("Could not connect")
            return False

    def find_utc_folders(self):
        if self.available:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.data['ip'], port=self.data['port'], username=self.data['username'],
                        password=self.data['password'])

            stdin, stdout, stderr = ssh.exec_command("find /share/CACHEDEV1_DATA/ -type f -name *.UTC | awk -F '/' '{print $4}' | uniq")

            for folder in stdout.read().splitlines():
                self.utc_folders.append(folder.decode("utf-8"))
            ssh.close()

    def find_utc_files(self):
        if self.available:
          
            for folder in self.utc_folders:
                stdin, stdout, stderr = ssh.exec_command("find /share/CACHEDEV1_DATA/" + folder.decode(
                    "utf-8") + "/ -type f -name *.UTC | awk -F '/' '{print $6}' | tail -1")
                for file in stdout.read().splitlines():
                    self.utc_files.append(file)


a = Qserver()
print(a.test_connection())
