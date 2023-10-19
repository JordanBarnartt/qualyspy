"""This file contains all the Qualys API URLs used by qualyspy."""

about = "/msp/about.php"
host_list_vm_detection = "/api/2.0/fo/asset/host/vm/detection/"
host_list = "/api/2.0/fo/asset/host/"
knowledgebase = "/api/2.0/fo/knowledge_base/vuln/"
ignore_vuln = "/api/2.0/fo/ignore_vuln/index.php"

gateway_auth = "/auth/"

asset_details = "/rest/2.0/get/am/asset"
all_asset_details = "/rest/2.0/search/am/asset"

create_tag = "/qps/rest/2.0/create/am/tag"
update_tag = "/qps/rest/2.0/update/am/tag"
search_tags = "/qps/rest/2.0/search/am/tag"
count_tags = "/qps/rest/2.0/count/am/tag"
delete_tag = "/qps/rest/2.0/delete/am/tag"
create_azure_connector = "/qps/rest/3.0/create/am/azureassetdataconnector"
delete_azure_connector = "/qps/rest/3.0/delete/am/azureassetdataconnector"
search_azure_connector = "/qps/rest/3.0/search/am/azureassetdataconnector"
