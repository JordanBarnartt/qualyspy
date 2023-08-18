# QualysPy

A Python wrapper for the Qualys API.  Qualys data can be interacted with using a Python model,
loaded into a PostgreSQL database, and queryed from that database with the same model.

The Python models are intended to be a 1:1 mapping of the objects returned by the Qualys API.

This is a work in progress.  The currently supported API calls are:

-  VMDR
    - host_list_detection

## Requirements

- Python >= 3.10
- A supported version of Linux (tested on Ubuntu 22.04)
- A supported version of PostgreSQL, if you want to use the ORM features.

## Installation

```shell
python -m venv .venv
source .venv/bin/activate
pip install qualyspy
```

Then, create a config file to indicate the Qualys API URLS and credentials and, optionally,
PostgreSQL database information.  See `.qualyspy-example` for an example configuration file.  By
default, QualysPy will search for this file at ~/.qualyspy, but a different file path
can be supplied.

## Usage

Documentation is located at <https://qualyspy.readthedocs.io>.

Each Qualys API has class subclassed from QualysAPIBase.  For example, to connect to the VMDR API:

```python
from qualyspy.vmdr import VmdrAPI

api = VmdrAPI()
```

The API object has methods corresponding to the Qualys API's endpoints.

```python

host_vulns = api.host_list_detection(ids=12345)
```

To load the data into a database, use the ORM class corresponding to the API endpoint.  For the
host_list_detection endpoint:

```python
from qualyspy.vmdr import HostListDetectionORM
# Tip: You can pass echo=True to an ORM class to write the SQL commands to stdout
orm = HostListDetectionORM()
orm.load() # This may take some time, depending on how much data there is to load.
```

Finally, the data can be queryed and will be outputted in the same form as with VmdrAPI.

```python
from qualyspy.models.vmdr.host_list_vm_detection_orm import Host

# Get all hosts from the database
with orm.Session(vmdr_orm.engine) as session:
    stmt = session.query(Host)
    host_list = vmdr_orm.query(stmt)[0]
    host = host_list.host[0]
```
