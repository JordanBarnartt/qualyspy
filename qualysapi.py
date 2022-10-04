import configparser
import lxml.objectify
import re
import requests

CONFIG_FILE = 'qualysapi.conf'

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ROOT = config['AUTHENTICATION']['api_root']
CREDENTIALS = {"username": config['AUTHENTICATION']['username'],
               "password": config['AUTHENTICATION']['password']}


class Connection:
    headers = {"X-Requested-With": "qualysapi python package"}

    def __init__(self):
        data = {"action": "login",
                "username": CREDENTIALS["username"], "password": CREDENTIALS["password"]}
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

    def run(self, func, params=None):
        if params is not None:
            return func(self, **params)
        else:
            return func(self)