import configparser
import re
import requests
import lxml.objectify

import modules.vm_scans

CONFIG_FILE = 'qualysapi.conf'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ROOT = config['AUTHENTICATION']['api_root']
CREDENTIALS = {"username": config['AUTHENTICATION']['username'],
               "password": config['AUTHENTICATION']['password']}


class Connection:
    headers = {"X-Requested-With": "qualysapi python package"}

    def __init__(self, username, password):
        data = {"action": "login", "username": username, "password": password}
        conn = requests.post(
            API_ROOT + "fo/session/", headers=self.headers, data=data)
        if conn.status_code == requests.codes.ok:
            self.cookies = {"QualysSession": conn.cookies["QualysSession"]}
            with open('debug/cookies.txt', 'a') as f:
                f.write(str(conn.cookies["QualysSession"]) + "\n")
        else:
            print(conn.headers)
            conn.raise_for_status()

    def __del__(self):
        data = {"action": "logout"}
        requests.post(API_ROOT + "fo/session/", headers=self.headers,
                      data=data, cookies=self.cookies)

    def request(self, path, params=None):
        conn = requests.get(API_ROOT + path, headers=self.headers,
                            cookies=self.cookies, params=params)
        return lxml.objectify.fromstring(re.split("\n", conn.text, 1)[1])

    def get_scans(self, filter=None, modifiers=None):
        output = self.request("fo/scan/?action=list")
        self.scans = modules.vm_scans.get_scans(output, filter, modifiers)


if __name__ == "__main__":
    conn = Connection(**CREDENTIALS)
    conn.get_scans()
    print(conn.scans)
