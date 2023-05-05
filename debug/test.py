# type: ignore

import inspect
import os
import sys


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import qualyspy.qualysapi
from qualyspy.assets import host_list_detection
from qualyspy.scan_configuration import knowledgebase

conn = qualyspy.qualysapi.Connection()
host_id = 14775

cert_qids = [38173, 38167, 38170, 38628, 38794, 38169, 38657]
host = host_list_detection.host_list_detection(conn, ids=host_id, qids=cert_qids)[0][0]
print(host)