import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from asset_mgmt_tagging.asset import search_assets
from asset_mgmt_tagging.filter import make_filter
from asset_mgmt_tagging.tags import create_tag, search_tags
