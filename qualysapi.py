import requests
import lxml

API_ROOT = "https://qualysapi.qualys.com/api/2.0"


class connection:
    headers = {"X-Requested-With": "qualysapi python package"}

    def __init__(self, username, password):
        data = {"action": "login", "username": username, "password": password}
        conn = requests.post(
            API_ROOT + "fo/session/", headers=self.headers, data=data)
        self.cookies = {"QualysSession": conn.cookies["QualysSession"]}

    def __del__(self):
        data = {"action": "logout"}
        requests.post(API_ROOT + "fo/session/",
                      data=data, cookies=self.cookies)
        super(self.__del__)

    def request(self, path):
        conn = requests.get(path, headers=self.headers, cookies=self.cookies)
        return lxml.objectify(conn.text)

    def get_scans(self, filter=None, modifiers=None):
        self.scans = []
        
