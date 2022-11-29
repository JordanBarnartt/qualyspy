import configparser
import requests
import os

CONFIG_FILE = os.path.expanduser("~/qualysapi.conf")
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_ROOT = config['AUTHENTICATION']['api_root']

headers = {"X-Requested-With": "qualysapi python package"}
data = {"action": "logout"}

with open("debug/cookies.txt", "r") as f:
    for cookie in f:
        cookies = {"QualysSession": cookie.strip("\n")}
        r = requests.post(API_ROOT + "/api/2.0/fo/session/", headers=headers,
                          data=data, cookies=cookies)
        print(r.text)
