import configparser
import dataclasses
import datetime
import requests
import lxml

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
        else:
            conn.raise_for_status()

    def __del__(self):
        data = {"action": "logout"}
        requests.post(API_ROOT + "fo/session/",
                      data=data, cookies=self.cookies)

    def request(self, path):
        conn = requests.get(path, headers=self.headers, cookies=self.cookies)
        return lxml.objectify(conn.text)

    def get_scans(self, filter=None, modifiers=None):
        self.scans = []
        output = self.request("o/scan/?action=list")
        for scan in output["SCAN_LIST_OUTPUT"]["RESPONSE"]["SCAN_LIST"]:
            scan_elements = {element.tag.tolower(
            ): scan[element] for element in scan}
            self.scans.append(Scan(**scan_elements))


@dataclasses.dataclass
class Scan:
    ref: str
    _type: str
    title: str
    user_login: str
    launch_datetime: datetime.datetime
    duration: datetime.timedelta
    processed: str
    target: str
    id: str = None
    scan_type: str = None
    processing_priority: str = None
    status: str = None
    asset_group_title_list: str = None
    option_profile: str = None


if __name__ == "__main__":
    conn = Connection(**CREDENTIALS)
