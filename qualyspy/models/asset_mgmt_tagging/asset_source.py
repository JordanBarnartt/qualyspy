import datetime as dt
from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

__NAMESPACE__ = "http://am.oxm.api.portal.qualys.com/v3"


class AssetSourceStateCode(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    TERMINATED = "TERMINATED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    DEALLOCATED = "DEALLOCATED"
    DEALLOCATING = "DEALLOCATING"
    CREATING = "CREATING"
    STARTING = "STARTING"
    DELETING = "DELETING"
    DELETED = "DELETED"
    UPDATING = "UPDATING"
    FAILED = "FAILED"
    MOVING = "MOVING"
    PROVISIONING = "PROVISIONING"
    CREATING_IMAGE = "CREATING_IMAGE"
    TERMINATING = "TERMINATING"
    SUCCEEDED = "SUCCEEDED"
    UNSUPPORTED = "UNSUPPORTED"


class AssetSourceType(Enum):
    EC2 = "EC2"
    LDAP = "LDAP"
    AZURE = "AZURE"
    GCP = "GCP"
    IBM = "IBM"
    OCI = "OCI"
    VMWARE_VSPHERE = "VMWARE_VSPHERE"


@dataclass
class AzureTags:
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class Ec2Tags:
    class Meta:
        name = "EC2Tags"

    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class GcpTags:
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class IbmTags:
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class OciTag:
    key: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    type_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    namespace: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class OciVnic:
    oci_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ociId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    vnic_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "vnicId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    vlan_tag: Optional[int] = field(
        default=None,
        metadata={
            "name": "vlanTag",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    virtual_router_ip: Optional[str] = field(
        default=None,
        metadata={
            "name": "virtualRouterIp",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    subnet_cidr_block: Optional[str] = field(
        default=None,
        metadata={
            "name": "subnetCidrBlock",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    private_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    mac_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "macAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    vcn_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "vcnId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    vcn_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "vcnName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    vcn_compartment_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "vcnCompartmentId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    subnet_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "subnetId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    subnet_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "subnetName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )
    public_ip: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicIp",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class AssetSource:
    asset_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "assetId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    type_value: Optional[AssetSourceType] = field(
        default=None,
        metadata={
            "name": "type",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    first_discovered: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "firstDiscovered",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )
    last_updated: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "lastUpdated",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )


@dataclass
class AzureTagsQlist:
    class Meta:
        name = "AzureTagsQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[AzureTags] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[AzureTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[AzureTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[AzureTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[AzureTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class Ec2TagsQlist:
    class Meta:
        name = "Ec2TagsQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[Ec2Tags] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[Ec2Tags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[Ec2Tags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[Ec2Tags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[Ec2Tags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class GcpTagsQlist:
    class Meta:
        name = "GcpTagsQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[GcpTags] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[GcpTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[GcpTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[GcpTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[GcpTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class IbmTagsQlist:
    class Meta:
        name = "IbmTagsQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[IbmTags] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[IbmTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[IbmTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[IbmTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[IbmTags] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class OciTagsQlist:
    class Meta:
        name = "OciTagsQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[OciTag] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[OciTag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[OciTag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[OciTag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[OciTag] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class OciVnicQlist:
    class Meta:
        name = "OciVnicQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[OciVnic] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[OciVnic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[OciVnic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[OciVnic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[OciVnic] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class AssetSourceQlist:
    class Meta:
        name = "AssetSourceQList"

    count: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    list_value: List[AssetSource] = field(
        default_factory=list,
        metadata={
            "name": "list",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    set: List[AssetSource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    add: List[AssetSource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    remove: List[AssetSource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    update: List[AssetSource] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class AzureVmTags:
    tags: Optional[AzureTagsQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class Ec2InstanceTags:
    tags: Optional[Ec2TagsQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class GcpInstanceTags:
    tags: Optional[GcpTagsQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class IbmInstanceTags:
    tags: Optional[IbmTagsQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class OciInstanceTags:
    tags: Optional[OciTagsQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class OciInstanceVnic:
    vnic: Optional[OciVnicQlist] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "required": True,
        },
    )


@dataclass
class AzureAssetSourceSimple(AssetSource):
    azure_vm_tags: Optional[AzureVmTags] = field(
        default=None,
        metadata={
            "name": "azureVmTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    vm_size: Optional[str] = field(
        default=None,
        metadata={
            "name": "vmSize",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    vm_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "vmId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    offer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    state: Optional[AssetSourceStateCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    publisher: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    os_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "osType",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    subnet: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    ipv6: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    subscription_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "subscriptionId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    resource_group_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "resourceGroupName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    mac_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "macAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    virtual_network: Optional[str] = field(
        default=None,
        metadata={
            "name": "virtualNetwork",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class Ec2AssetSourceSimple(AssetSource):
    ec2_instance_tags: Optional[Ec2InstanceTags] = field(
        default=None,
        metadata={
            "name": "ec2InstanceTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    reservation_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "reservationId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    availability_zone: Optional[str] = field(
        default=None,
        metadata={
            "name": "availabilityZone",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_dns_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateDnsName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_dns_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicDnsName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    local_hostname: Optional[str] = field(
        default=None,
        metadata={
            "name": "localHostname",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    instance_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    instance_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceType",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    created_date: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "createdDate",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )
    instance_state: Optional[AssetSourceStateCode] = field(
        default=None,
        metadata={
            "name": "instanceState",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    group_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "groupId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    group_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "groupName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    spot_instance: Optional[bool] = field(
        default=None,
        metadata={
            "name": "spotInstance",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    instance_group_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceGroupId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    instance_group_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceGroupName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    key_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "keyName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    launch_time: Optional[dt.datetime] = field(
        default=None,
        metadata={
            "name": "launchTime",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
            "format": "%Y-%m-%dT%H:%M:%SZ",
        },
    )
    account_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "accountId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    placement_group_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "placementGroupName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    product_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "productCode",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    source_destination_check: Optional[bool] = field(
        default=None,
        metadata={
            "name": "sourceDestinationCheck",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    spot_instance_request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "spotInstanceRequestId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    subnet_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "subnetId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    vpc_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "vpcId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    region: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    availibility_zone: Optional[str] = field(
        default=None,
        metadata={
            "name": "availibilityZone",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    zone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    endpoint_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "endpointId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    image_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "imageId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    mac_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "macAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    monitoring_enabled: Optional[bool] = field(
        default=None,
        metadata={
            "name": "monitoringEnabled",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class GcpAssetSourceSimple(AssetSource):
    gcp_instance_tags: Optional[GcpInstanceTags] = field(
        default=None,
        metadata={
            "name": "gcpInstanceTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    instance_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "instanceId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    hostname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    machine_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "machineType",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    image_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "imageId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    zone: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    project_id_no: Optional[str] = field(
        default=None,
        metadata={
            "name": "projectIdNo",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    state: Optional[AssetSourceStateCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    project_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "projectId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    network: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    mac_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "macAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_ip_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateIpAddress",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class IbmassetSourceSimple(AssetSource):
    class Meta:
        name = "IBMAssetSourceSimple"

    ibm_instance_tags: Optional[IbmInstanceTags] = field(
        default=None,
        metadata={
            "name": "ibmInstanceTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    ibm_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "ibmId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    location: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    datacenter_id: Optional[int] = field(
        default=None,
        metadata={
            "name": "datacenterId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    device_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "deviceName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    state: Optional[AssetSourceStateCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_vlan: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicVlan",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    domain: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_vlan: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateVlan",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    public_ip: Optional[str] = field(
        default=None,
        metadata={
            "name": "publicIp",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    private_ip: Optional[str] = field(
        default=None,
        metadata={
            "name": "privateIp",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class OciAssetSourceSimple(AssetSource):
    oci_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ociId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    display_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "displayName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    compartment_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "compartmentId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    compartment_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "compartmentName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    tenant_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "tenantId",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    tenant_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "tenantName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    shape: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    state: Optional[AssetSourceStateCode] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    region: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    availability_domain: Optional[str] = field(
        default=None,
        metadata={
            "name": "availabilityDomain",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    image: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    fault_domain: Optional[str] = field(
        default=None,
        metadata={
            "name": "faultDomain",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    host_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "hostName",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    canonical_region: Optional[str] = field(
        default=None,
        metadata={
            "name": "canonicalRegion",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    oci_instance_tags: Optional[OciInstanceTags] = field(
        default=None,
        metadata={
            "name": "ociInstanceTags",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )
    oci_vnic: Optional[OciInstanceVnic] = field(
        default=None,
        metadata={
            "name": "ociVnic",
            "type": "Element",
            "namespace": "http://am.oxm.api.portal.qualys.com/v3",
        },
    )


@dataclass
class Ec2AssetSource(Ec2AssetSourceSimple):
    pass
