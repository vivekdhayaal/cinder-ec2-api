# Copyright 2014
# The Cloudscaling Group, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
import json
import random
import uuid

from ec2api.openstack.common import timeutils
from ec2api.tests import tools


# Helper functions section

# mock helpers
def get_db_api_add_item(item_id_dict):
    def db_api_add_item(context, kind, data):
        if isinstance(item_id_dict, dict):
            item_id = item_id_dict[kind]
        else:
            item_id = item_id_dict
        data = tools.update_dict(data, {'id': item_id})
        data.setdefault('os_id')
        data.setdefault('vpc_id')
        return data
    return db_api_add_item


def get_db_api_get_items(results_dict_by_kind):
    def db_api_get_items(context, kind, *args):
        return results_dict_by_kind.get(kind)
    return db_api_get_items


def get_db_api_get_item_by_id(results_dict_by_id):
    def db_api_get_item_by_id(context, kind, item_id):
        item = results_dict_by_id.get(item_id)
        if item is not None:
            item = copy.deepcopy(item)
        return item
    return db_api_get_item_by_id


def get_neutron_create(kind, os_id, addon={}):
    def neutron_create(body):
        body = copy.deepcopy(body)
        body[kind].update(addon)
        body[kind]['id'] = os_id
        return body
    return neutron_create


# random identifier generators
def random_os_id():
    return str(uuid.uuid4())


def random_ec2_id(kind):
    return '%s-%08x' % (kind, random.randint(0, 0xffffffff))

# Plain constants section
# Constant name notation:
# [<type>[<subtype>]]<object_name>
# where
#    type - type of object the constant represents
#        ID - for identifiers, CIDR for cidrs, etc
#    subtype - type of object storage, is used for IDs only
#        EC2 - object representation to end user
#        OS - object is stored in OpenStack
#    object_name - identifies the object

# common constants
ID_OS_USER = random_os_id()
ID_OS_PROJECT = random_os_id()
TIME_ATTACH_NETWORK_INTERFACE = timeutils.isotime(None, True)


# vpc constants
ID_EC2_VPC_1 = random_ec2_id('vpc')
ID_EC2_VPC_2 = random_ec2_id('vpc')
ID_OS_ROUTER_1 = random_os_id()
ID_OS_ROUTER_2 = random_os_id()

CIDR_VPC_1 = '10.10.0.0/16'
CIDR_VPC_2 = '10.20.0.0/16'
ID_OS_PUBLIC_NETWORK = random_os_id()
NAME_OS_PUBLIC_NETWORK = 'public_external'


# internet gateway constants
ID_EC2_IGW_1 = random_ec2_id('igw')
ID_EC2_IGW_2 = random_ec2_id('igw')


# subnet constants
ID_EC2_SUBNET_1 = random_ec2_id('subnet')
ID_EC2_SUBNET_2 = random_ec2_id('subnet')
ID_OS_SUBNET_1 = random_os_id()
ID_OS_SUBNET_2 = random_os_id()
ID_OS_NETWORK_1 = random_os_id()
ID_OS_NETWORK_2 = random_os_id()

CIDR_SUBNET_1 = '10.10.1.0/24'
IP_FIRST_SUBNET_1 = '10.10.1.4'
IP_LAST_SUBNET_1 = '10.10.1.254'
IP_GATEWAY_SUBNET_1 = '10.10.1.1'
CIDR_SUBNET_2 = '10.10.2.0/24'
IP_FIRST_SUBNET_2 = '10.10.2.4'
IP_LAST_SUBNET_2 = '10.10.2.254'


# network interface constants
ID_EC2_NETWORK_INTERFACE_1 = random_ec2_id('eni')
ID_EC2_NETWORK_INTERFACE_2 = random_ec2_id('eni')
ID_EC2_NETWORK_INTERFACE_2_ATTACH = (
    ID_EC2_NETWORK_INTERFACE_2.replace('eni', 'eni-attach'))
ID_OS_PORT_1 = random_os_id()
ID_OS_PORT_2 = random_os_id()

IP_NETWORK_INTERFACE_1 = '10.10.1.4'
IP_NETWORK_INTERFACE_2 = '10.10.2.254'
IP_NETWORK_INTERFACE_2_EXT_1 = '10.10.2.4'
IP_NETWORK_INTERFACE_2_EXT_2 = '10.10.2.5'
IPS_NETWORK_INTERFACE_2 = (IP_NETWORK_INTERFACE_2,
                           IP_NETWORK_INTERFACE_2_EXT_1,
                           IP_NETWORK_INTERFACE_2_EXT_2)
DESCRIPTION_NETWORK_INTERFACE_1 = 'description1'
DESCRIPTION_NETWORK_INTERFACE_2 = 'description2'


# instance constants
ID_EC2_INSTANCE_1 = random_ec2_id('i')
ID_EC2_INSTANCE_2 = random_ec2_id('i')
ID_OS_INSTANCE_1 = random_os_id()
ID_OS_INSTANCE_2 = random_os_id()
ID_EC2_RESERVATION_1 = random_ec2_id('r')
ID_EC2_RESERVATION_2 = random_ec2_id('r')

# DHCP options constants
ID_EC2_DHCP_OPTIONS_1 = random_ec2_id('dopt')
ID_EC2_DHCP_OPTIONS_2 = random_ec2_id('dopt')


# address constants
ID_EC2_ADDRESS_1 = random_ec2_id('eipalloc')
ID_EC2_ADDRESS_2 = random_ec2_id('eipalloc')
ID_EC2_ASSOCIATION_1 = ID_EC2_ADDRESS_1.replace('eipalloc', 'eipassoc')
ID_EC2_ASSOCIATION_2 = ID_EC2_ADDRESS_2.replace('eipalloc', 'eipassoc')
ID_OS_FLOATING_IP_1 = random_os_id()
ID_OS_FLOATING_IP_2 = random_os_id()

IP_ADDRESS_1 = '192.168.1.100'
IP_ADDRESS_2 = '192.168.1.200'


# security group constants
ID_EC2_SECURITY_GROUP_1 = random_ec2_id('sg')
ID_EC2_SECURITY_GROUP_2 = random_ec2_id('sg')
ID_OS_SECURITY_GROUP_1 = random_os_id()
ID_OS_SECURITY_GROUP_2 = random_os_id()


# route table constants
ID_EC2_ROUTE_TABLE_1 = random_ec2_id('rtb')
ID_EC2_ROUTE_TABLE_2 = random_ec2_id('rtb')
ID_EC2_ROUTE_TABLE_ASSOCIATION_1 = ID_EC2_VPC_1.replace('vpc', 'rtbassoc')
ID_EC2_ROUTE_TABLE_ASSOCIATION_2 = ID_EC2_SUBNET_2.replace('subnet',
                                                           'rtbassoc')

CIDR_EXTERNAL_NETWORK = '192.168.50.0/24'


# image constants
ID_EC2_IMAGE_1 = random_ec2_id('ami')
ID_EC2_IMAGE_2 = random_ec2_id('ami')
ID_EC2_IMAGE_AKI_1 = random_ec2_id('aki')
ID_EC2_IMAGE_ARI_1 = random_ec2_id('ari')
ID_OS_IMAGE_1 = random_os_id()
ID_OS_IMAGE_2 = random_os_id()
ID_OS_IMAGE_AKI_1 = random_os_id()
ID_OS_IMAGE_ARI_1 = random_os_id()

ROOT_DEVICE_NAME_IMAGE_1 = '/dev/sda1'
ROOT_DEVICE_NAME_IMAGE_2 = '/dev/sdb1'

# volumes constants
ID_EC2_VOLUME_1 = random_ec2_id('vol')
ID_EC2_VOLUME_2 = random_ec2_id('vol')
ID_OS_VOLUME_1 = random_os_id()
ID_OS_VOLUME_2 = random_os_id()


# snapshots constants
ID_EC2_SNAPSHOT_1 = random_ec2_id('snap')
ID_EC2_SNAPSHOT_2 = random_ec2_id('snap')
ID_OS_SNAPSHOT_1 = random_os_id()
ID_OS_SNAPSHOT_2 = random_os_id()


# Object constants section
# Constant name notation:
# [<subtype>]<object_name>
# where
#    subtype - type of object storage, is not used for DB objects
#        EC2 - object representation to end user
#        EC2OS - object received from Nova EC2 API
#        OS - object is stored in OpenStack
#    object_name - identifies the object

# vpc objects
# 2 vpcs in normal state
DB_VPC_1 = {'id': ID_EC2_VPC_1,
            'os_id': ID_OS_ROUTER_1,
            'vpc_id': None,
            'cidr_block': CIDR_VPC_1,
            'route_table_id': ID_EC2_ROUTE_TABLE_1}
DB_VPC_2 = {'id': ID_EC2_VPC_2,
            'os_id': ID_OS_ROUTER_2,
            'vpc_id': None,
            'cidr_block': CIDR_VPC_2}

EC2_VPC_1 = {'vpcId': ID_EC2_VPC_1,
             'cidrBlock': CIDR_VPC_1,
             'isDefault': False,
             'state': 'available',
             'dhcpOptionsId': 'default'}
EC2_VPC_2 = {'vpcId': ID_EC2_VPC_2,
             'cidrBlock': CIDR_VPC_2,
             'isDefault': False,
             'state': 'available',
             'dhcpOptionsId': 'default'}

OS_ROUTER_1 = {'id': ID_OS_ROUTER_1,
               'name': ID_EC2_VPC_1}
OS_ROUTER_2 = {'id': ID_OS_ROUTER_2,
               'name': ID_EC2_VPC_2}


# internet gateway objects
# 2 internate gateway, the first is attached to the first vpc
DB_IGW_1 = {'id': ID_EC2_IGW_1,
            'os_id': None,
            'vpc_id': ID_EC2_VPC_1}
DB_IGW_2 = {'id': ID_EC2_IGW_2,
            'os_id': None,
            'vpc_id': None}

EC2_IGW_1 = {'internetGatewayId': ID_EC2_IGW_1,
             'attachmentSet': [{'vpcId': ID_EC2_VPC_1,
                                'state': 'available'}]}
EC2_IGW_2 = {'internetGatewayId': ID_EC2_IGW_2,
             'attachmentSet': []}


# subnet objects
# 2 subnets in the first vpc
DB_SUBNET_1 = {'id': ID_EC2_SUBNET_1,
               'os_id': ID_OS_SUBNET_1,
               'vpc_id': ID_EC2_VPC_1}
DB_SUBNET_2 = {'id': ID_EC2_SUBNET_2,
               'os_id': ID_OS_SUBNET_2,
               'vpc_id': ID_EC2_VPC_1}

EC2_SUBNET_1 = {'subnetId': ID_EC2_SUBNET_1,
                'state': 'available',
                'vpcId': ID_EC2_VPC_1,
                'cidrBlock': CIDR_SUBNET_1,
                'defaultForAz': False,
                'availableIpAddressCount': 253,
                'mapPublicIpOnLaunch': False}
EC2_SUBNET_2 = {'subnetId': ID_EC2_SUBNET_2,
                'state': 'available',
                'vpcId': ID_EC2_VPC_1,
                'cidrBlock': CIDR_SUBNET_2,
                'defaultForAz': False,
                'availableIpAddressCount': 253,
                'mapPublicIpOnLaunch': False}

OS_SUBNET_1 = {'id': ID_OS_SUBNET_1,
               'network_id': ID_OS_NETWORK_1,
               'name': ID_EC2_SUBNET_1,
               'ip_version': '4',
               'cidr': CIDR_SUBNET_1,
               'host_routes': [{'nexthop': IP_GATEWAY_SUBNET_1,
                                'destination': '10.10.0.0/16'},
                               {'nexthop': '127.0.0.1',
                                'destination': '0.0.0.0/0'}]}
OS_SUBNET_2 = {'id': ID_OS_SUBNET_2,
               'network_id': ID_OS_NETWORK_2,
               'name': ID_EC2_SUBNET_2,
               'ip_version': '4',
               'cidr': CIDR_SUBNET_2}
OS_NETWORK_1 = {'id': ID_OS_NETWORK_1,
                'name': ID_EC2_SUBNET_1,
                'status': 'available'}
OS_NETWORK_2 = {'id': ID_OS_NETWORK_2,
                'name': ID_EC2_SUBNET_2,
                'status': 'available'}


# network interface objects
# 2 ports in both subnets, the second is attached to the first instance
DB_NETWORK_INTERFACE_1 = {'id': ID_EC2_NETWORK_INTERFACE_1,
                          'os_id': ID_OS_PORT_1,
                          'vpc_id': ID_EC2_VPC_1,
                          'subnet_id': ID_EC2_SUBNET_1,
                          'description': DESCRIPTION_NETWORK_INTERFACE_1,
                          'private_ip_address': IP_NETWORK_INTERFACE_1}
DB_NETWORK_INTERFACE_2 = {'id': ID_EC2_NETWORK_INTERFACE_2,
                          'os_id': ID_OS_PORT_2,
                          'vpc_id': ID_EC2_VPC_1,
                          'subnet_id': ID_EC2_SUBNET_2,
                          'description': DESCRIPTION_NETWORK_INTERFACE_2,
                          'private_ip_address': IP_NETWORK_INTERFACE_2,
                          'instance_id': ID_EC2_INSTANCE_1,
                          'delete_on_termination': False,
                          'attach_time': TIME_ATTACH_NETWORK_INTERFACE}

EC2_NETWORK_INTERFACE_1 = {
    'networkInterfaceId': ID_EC2_NETWORK_INTERFACE_1,
    'status': 'available',
    'vpcId': ID_EC2_VPC_1,
    'subnetId': ID_EC2_SUBNET_1,
    'description': DESCRIPTION_NETWORK_INTERFACE_1,
    'macAddress': 'fb:10:2e:b2:ba:b7',
    'privateIpAddress': IP_NETWORK_INTERFACE_1,
    'privateIpAddressesSet': [{'privateIpAddress': IP_NETWORK_INTERFACE_1,
                               'primary': True}],
    'sourceDestCheck': True,
    'ownerId': ID_OS_PROJECT,
    'requesterManaged': False,
    'groupSet': [],
    'tagSet': [],
}
EC2_NETWORK_INTERFACE_2 = {
    'networkInterfaceId': ID_EC2_NETWORK_INTERFACE_2,
    'status': 'in-use',
    'vpcId': ID_EC2_VPC_1,
    'subnetId': ID_EC2_SUBNET_2,
    'description': DESCRIPTION_NETWORK_INTERFACE_2,
    'macAddress': 'fb:10:2e:b2:ba:b7',
    'privateIpAddress': IP_NETWORK_INTERFACE_2,
    'association': {
        'associationId': ID_EC2_ASSOCIATION_2,
        'ipOwnerId': ID_OS_PROJECT,
        'publicDnsName': None,
        'publicIp': IP_ADDRESS_2,
    },
    'privateIpAddressesSet': [
        {'privateIpAddress': IP_NETWORK_INTERFACE_2,
         'primary': True,
         'association': {
             'associationId': ID_EC2_ASSOCIATION_2,
             'ipOwnerId': ID_OS_PROJECT,
             'publicDnsName': None,
             'publicIp': IP_ADDRESS_2,
         }},
        {'privateIpAddress': IP_NETWORK_INTERFACE_2_EXT_1,
         'primary': False},
        {'privateIpAddress': IP_NETWORK_INTERFACE_2_EXT_2,
         'primary': False},
    ],
    'sourceDestCheck': True,
    'ownerId': ID_OS_PROJECT,
    'requesterManaged': False,
    'attachment': {
        'status': 'attached',
        'attachTime': TIME_ATTACH_NETWORK_INTERFACE,
        'deleteOnTermination': False,
        'attachmentId': ID_EC2_NETWORK_INTERFACE_2_ATTACH,
        'instanceId': ID_EC2_INSTANCE_1,
        'instanceOwnerId': ID_OS_PROJECT,
    },
    'groupSet': [],
    'tagSet': [],
}

OS_PORT_1 = {'id': ID_OS_PORT_1,
             'network_id': ID_OS_SUBNET_1,
             'name': ID_EC2_NETWORK_INTERFACE_1,
             'status': 'DOWN',
             'mac_address': 'fb:10:2e:b2:ba:b7',
             'fixed_ips': [{'ip_address': IP_NETWORK_INTERFACE_1,
                            'subnet_id': ID_OS_SUBNET_1}],
             'device_id': None,
             'device_owner': '',
             'security_groups': []}
OS_PORT_2 = {'id': ID_OS_PORT_2,
             'network_id': ID_OS_SUBNET_2,
             'name': ID_EC2_NETWORK_INTERFACE_2,
             'status': 'ACTIVE',
             'mac_address': 'fb:10:2e:b2:ba:b7',
             'fixed_ips': [{'ip_address': IP_NETWORK_INTERFACE_2,
                            'subnet_id': ID_OS_SUBNET_2},
                           {'ip_address': IP_NETWORK_INTERFACE_2_EXT_1,
                            'subnet_id': ID_OS_SUBNET_2},
                           {'ip_address': IP_NETWORK_INTERFACE_2_EXT_2,
                            'subnet_id': ID_OS_SUBNET_2}],
             'device_id': ID_OS_INSTANCE_1,
             'device_owner': '',
             'security_groups': []}


# instance objects
DB_INSTANCE_1 = {
    'id': ID_EC2_INSTANCE_1,
    'os_id': ID_OS_INSTANCE_1,
    'vpc_id': ID_EC2_VPC_1,
    'reservation_id': ID_EC2_RESERVATION_1,
    'launch_index': 0,
}
DB_INSTANCE_2 = {
    'id': ID_EC2_INSTANCE_2,
    'os_id': ID_OS_INSTANCE_2,
    'vpc_id': None,
    'reservation_id': ID_EC2_RESERVATION_2,
    'launch_index': 0,
}

NOVADB_INSTANCE_1 = {
    'reservation_id': random_ec2_id('r'),
    'launch_index': 0,
    'kernel_id': None,
    'ramdisk_id': None,
    'root_device_name': '/dev/vda',
    'hostname': ID_EC2_INSTANCE_1,
}
NOVADB_INSTANCE_2 = {
    'reservation_id': ID_EC2_RESERVATION_2,
    'launch_index': 0,
    'kernel_id': None,
    'ramdisk_id': None,
    'root_device_name': '/dev/vda',
    'hostname': 'Server %s' % ID_OS_INSTANCE_2,
}

EC2OS_INSTANCE_1 = {
    'instanceId': ID_EC2_INSTANCE_1,
    'privateIpAddress': IP_NETWORK_INTERFACE_2,
    'fakeKey': 'fakeValue',
}
EC2OS_INSTANCE_2 = {
    'instanceId': ID_EC2_INSTANCE_2,
    'privateIpAddress': None,
    'fakeKey': 'fakeValue',
}
EC2OS_RESERVATION_1 = {
    'instancesSet': [EC2OS_INSTANCE_1],
    'fakeKey': 'fakeValue',
}
EC2OS_RESERVATION_2 = {
    'instancesSet': [EC2OS_INSTANCE_2],
    'fakeKey': 'fakeValue',
}
EC2_INSTANCE_1 = {
    'instanceId': ID_EC2_INSTANCE_1,
    'privateIpAddress': IP_NETWORK_INTERFACE_2,
    'vpcId': ID_EC2_VPC_1,
    'subnetId': ID_EC2_SUBNET_2,
    'networkInterfaceSet': [
        {'networkInterfaceId': ID_EC2_NETWORK_INTERFACE_2,
         'status': 'in-use',
         'vpcId': ID_EC2_VPC_1,
         'subnetId': ID_EC2_SUBNET_2,
         'description': DESCRIPTION_NETWORK_INTERFACE_2,
         'macAddress': 'fb:10:2e:b2:ba:b7',
         'privateIpAddress': IP_NETWORK_INTERFACE_2,
         'association': {
             'associationId': ID_EC2_ASSOCIATION_2,
             'ipOwnerId': ID_OS_PROJECT,
             'publicDnsName': None,
             'publicIp': IP_ADDRESS_2,
         },
         'privateIpAddressesSet': [
             {'privateIpAddress': IP_NETWORK_INTERFACE_2,
              'primary': True,
              'association': {
                  'associationId': ID_EC2_ASSOCIATION_2,
                  'ipOwnerId': ID_OS_PROJECT,
                  'publicDnsName': None,
                  'publicIp': IP_ADDRESS_2}},
             {'privateIpAddress': IP_NETWORK_INTERFACE_2_EXT_1,
              'primary': False},
             {'privateIpAddress': IP_NETWORK_INTERFACE_2_EXT_2,
              'primary': False},
         ],
         'attachment': {
             'status': 'attached',
             'attachTime': TIME_ATTACH_NETWORK_INTERFACE,
             'deleteOnTermination': False,
             'attachmentId': ID_EC2_NETWORK_INTERFACE_2_ATTACH,
         },
         'sourceDestCheck': True,
         'ownerId': ID_OS_PROJECT,
         'requesterManaged': False,
         'groupSet': []},
    ],
    'amiLaunchIndex': 0,
    'placement': {'availabilityZone': None},
    'dnsName': IP_ADDRESS_2,
    'instanceState': {'code': 0, 'name': 'pending'},
    'imageId': ID_EC2_IMAGE_1,
    'productCodesSet': [],
    'privateDnsName': ID_EC2_INSTANCE_1,
    'keyName': None,
    'launchTime': None,
    'rootDeviceType': 'instance-store',
    'instanceType': 'fake_flavor',
    'ipAddress': IP_ADDRESS_2,
    'rootDeviceName': '/dev/vda',
}
EC2_INSTANCE_2 = {
    'instanceId': ID_EC2_INSTANCE_2,
    'privateIpAddress': None,
    'amiLaunchIndex': 0,
    'placement': {'availabilityZone': None},
    'dnsName': None,
    'instanceState': {'code': 0, 'name': 'pending'},
    'imageId': None,
    'productCodesSet': [],
    'privateDnsName': 'Server %s' % ID_OS_INSTANCE_2,
    'keyName': None,
    'launchTime': None,
    'rootDeviceType': 'instance-store',
    'instanceType': 'fake_flavor',
    'rootDeviceName': '/dev/vda',
}
EC2_RESERVATION_1 = {
    'reservationId': ID_EC2_RESERVATION_1,
    'ownerId': ID_OS_PROJECT,
    'instancesSet': [EC2_INSTANCE_1],
}
EC2_RESERVATION_2 = {
    'reservationId': ID_EC2_RESERVATION_2,
    'ownerId': ID_OS_PROJECT,
    'groupSet': [],
    'instancesSet': [EC2_INSTANCE_2],
}


class OSInstance(object):
    def __init__(self, instance_id, flavor=None, image=None, key_name=None,
                 created=None, tenant_id=ID_OS_PROJECT, addresses={},
                 security_groups=[], vm_state=None, host=None,
                 availability_zone=None):
        self.id = instance_id
        self.flavor = flavor
        self.image = image
        self.key_name = key_name
        self.created = created
        self.tenant_id = tenant_id
        self.addresses = addresses
        self.security_groups = security_groups
        setattr(self, 'OS-EXT-STS:vm_state', vm_state)
        setattr(self, 'OS-EXT-SRV-ATTR:host', host)
        setattr(self, 'OS-EXT-AZ:availability_zone', availability_zone)

    def get(self):
        None

    def delete(self):
        None


OS_INSTANCE_1 = OSInstance(
    ID_OS_INSTANCE_1, {'id': 'fakeFlavorId'},
    image={'id': ID_OS_IMAGE_1},
    addresses={
        ID_EC2_SUBNET_2: [{'addr': IP_NETWORK_INTERFACE_2,
                           'version': 4,
                           'OS-EXT-IPS:type': 'fixed'},
                          {'addr': IP_NETWORK_INTERFACE_2_EXT_1,
                           'version': 4,
                           'OS-EXT-IPS:type': 'fixed'},
                          {'addr': IP_NETWORK_INTERFACE_2_EXT_2,
                           'version': 4,
                           'OS-EXT-IPS:type': 'fixed'},
                          {'addr': IP_ADDRESS_2,
                           'version': 4,
                           'OS-EXT-IPS:type': 'floating'}]},
    )
OS_INSTANCE_2 = OSInstance(
    ID_OS_INSTANCE_2, {'id': 'fakeFlavorId'})

# DHCP options objects
DB_DHCP_OPTIONS_1 = {'id': ID_EC2_DHCP_OPTIONS_1,
                     'dhcp_configuration':
                     {'domain-name': ['my.domain.com'],
                      'domain-name-servers': ['8.8.8.8', '127.0.0.1']}}

DB_DHCP_OPTIONS_2 = {'id': ID_EC2_DHCP_OPTIONS_2,
                     'dhcp_configuration':
                     {'domain-name': ['my.domain.com'],
                      'domain-name-servers': ['8.8.8.8', '127.0.0.1'],
                      'netbios-name-servers': ['127.0.0.1'],
                      'netbios-node-type': [1],
                      'ntp-servers': ['127.0.0.1']}}

EC2_DHCP_OPTIONS_1 = {
    'dhcpOptionsId': ID_EC2_DHCP_OPTIONS_1,
    'dhcpConfigurationSet': [
        {'valueSet': [{'value': 'my.domain.com'}],
         'key': 'domain-name'},
        {'valueSet': [{'value': '8.8.8.8'}, {'value': '127.0.0.1'}],
         'key': 'domain-name-servers'}]}

EC2_DHCP_OPTIONS_2 = {
    'dhcpOptionsId': ID_EC2_DHCP_OPTIONS_2,
    'dhcpConfigurationSet': [
        {'valueSet': [{'value': 'my.domain.com'}],
         'key': 'domain-name'},
        {'valueSet': [{'value': '8.8.8.8'}, {'value': '127.0.0.1'}],
         'key': 'domain-name-servers'},
        {'valueSet': [{'value': 1}],
         'key': 'netbios-node-type'},
        {'valueSet': [{'value': '127.0.0.1'}],
         'key': 'ntp-servers'},
        {'valueSet': [{'value': '127.0.0.1'}],
         'key': 'netbios-name-servers'}]
}

OS_DHCP_OPTIONS_1 = {'extra_dhcp_opts': [{'opt_name': 'domain-name',
                                          'opt_value': 'my.domain.com'},
                                         {'opt_name': 'dns-servers',
                                          'opt_value': '8.8.8.8,127.0.0.1'}]}


# address objects

class NovaFloatingIp(object):

    def __init__(self, nova_ip_dict):
        self.id = nova_ip_dict['id']
        self.ip = nova_ip_dict['ip']
        self.fixed_ip = nova_ip_dict['fixed_ip']
        self.instance_id = nova_ip_dict['instance_id']

DB_ADDRESS_1 = {
    'id': ID_EC2_ADDRESS_1,
    'os_id': ID_OS_FLOATING_IP_1,
    'vpc_id': None,
    'public_ip': IP_ADDRESS_1,
}
DB_ADDRESS_2 = {
    'id': ID_EC2_ADDRESS_2,
    'os_id': ID_OS_FLOATING_IP_2,
    'vpc_id': None,
    'public_ip': IP_ADDRESS_2,
    'network_interface_id': ID_EC2_NETWORK_INTERFACE_2,
    'private_ip_address': IP_NETWORK_INTERFACE_2,
}

EC2_ADDRESS_CLASSIC_1 = {
    'publicIp': IP_ADDRESS_1,
    'domain': 'standard'
}
EC2_ADDRESS_CLASSIC_2 = {
    'publicIp': IP_ADDRESS_2,
    'instanceId': ID_EC2_INSTANCE_1,
    'domain': 'standard',
    'privateIpAddress': IP_NETWORK_INTERFACE_2
}
EC2_ADDRESS_1 = {
    'allocationId': ID_EC2_ADDRESS_1,
    'publicIp': IP_ADDRESS_1,
    'domain': 'vpc',
}
EC2_ADDRESS_2 = {
    'allocationId': ID_EC2_ADDRESS_2,
    'publicIp': IP_ADDRESS_2,
    'domain': 'vpc',
    'instanceId': ID_EC2_INSTANCE_1,
    'associationId': ID_EC2_ASSOCIATION_2,
    'networkInterfaceId': ID_EC2_NETWORK_INTERFACE_2,
    'privateIpAddress': IP_NETWORK_INTERFACE_2,
    'networkInterfaceOwnerId': ID_OS_PROJECT,
}

OS_FLOATING_IP_1 = {
    'id': ID_OS_FLOATING_IP_1,
    'floating_ip_address': IP_ADDRESS_1,
    'port_id': None,
    'fixed_ip_address': None,
}
OS_FLOATING_IP_2 = {
    'id': ID_OS_FLOATING_IP_2,
    'floating_ip_address': IP_ADDRESS_2,
    'port_id': ID_OS_PORT_2,
    'fixed_ip_address': IP_NETWORK_INTERFACE_2,
}

NOVA_FLOATING_IP_1 = {
    'id': ID_OS_FLOATING_IP_1,
    'ip': IP_ADDRESS_1,
    'instance_id': None,
    'fixed_ip': None,
}
NOVA_FLOATING_IP_2 = {
    'id': ID_OS_FLOATING_IP_2,
    'ip': IP_ADDRESS_2,
    'instance_id': ID_OS_INSTANCE_1,
    'fixed_ip': IP_NETWORK_INTERFACE_2,
}


# security group objects

class NovaSecurityGroup(object):

    def __init__(self, nova_group_dict):
        self.id = nova_group_dict['id']
        self.name = nova_group_dict['name']
        self.description = nova_group_dict['description']
        self.tenant_id = ID_OS_PROJECT
        self.rules = nova_group_dict['security_group_rules']

DB_SECURITY_GROUP_1 = {
    'id': ID_EC2_SECURITY_GROUP_1,
    'os_id': ID_OS_SECURITY_GROUP_1,
    'vpc_id': ID_EC2_VPC_1,
}
DB_SECURITY_GROUP_2 = {
    'id': ID_EC2_SECURITY_GROUP_2,
    'os_id': ID_OS_SECURITY_GROUP_2,
    'vpc_id': ID_EC2_VPC_1,
}
OS_SECURITY_GROUP_RULE_1 = {
    'direction': 'ingress',
    'ethertype': 'IPv4',
    'id': random_os_id(),
    'port_range_min': 10,
    'port_range_max': 10,
    'protocol': 'tcp',
    'remote_group_id': None,
    'remote_ip_prefix': '192.168.1.0/24',
    'security_group_id': ID_OS_SECURITY_GROUP_2
}
OS_SECURITY_GROUP_RULE_2 = {
    'direction': 'egress',
    'ethertype': 'IPv4',
    'id': random_os_id(),
    'port_range_min': 10,
    'port_range_max': None,
    'protocol': 100,
    'remote_group_id': ID_OS_SECURITY_GROUP_1,
    'remote_ip_prefix': None,
    'security_group_id': ID_OS_SECURITY_GROUP_2
}
OS_SECURITY_GROUP_1 = {
    'id': ID_OS_SECURITY_GROUP_1,
    'name': 'groupname',
    'security_group_rules':
    [{'remote_group_id': None,
      'direction': 'egress',
      'remote_ip_prefix': None,
      'protocol': None,
      'port_range_max': None,
      'security_group_id': ID_OS_SECURITY_GROUP_1,
      'port_range_min': None,
      'ethertype': 'IPv4',
      'id': random_os_id()},
     {'remote_group_id': None,
      'direction': 'egress',
      'remote_ip_prefix': None,
      'protocol': None,
      'port_range_max': None,
      'security_group_id': ID_OS_SECURITY_GROUP_1,
      'port_range_min': None,
      'ethertype': 'IPv6',
      'id': random_os_id()}],
    'description': 'Group description',
    'tenant_id': ID_OS_PROJECT
}
OS_SECURITY_GROUP_2 = {
    'id': ID_OS_SECURITY_GROUP_2,
    'name': 'groupname2',
    'security_group_rules': [
        OS_SECURITY_GROUP_RULE_1,
        OS_SECURITY_GROUP_RULE_2
    ],
    'description': 'Group description',
    'tenant_id': ID_OS_PROJECT
}
NOVA_SECURITY_GROUP_RULE_1 = {
    'id': random_os_id(),
    'from_port': 10,
    'to_port': 10,
    'ip_protocol': 'tcp',
    'group': None,
    'ip_range': {'cidr': '192.168.1.0/24'},
    'parent_group_id': ID_OS_SECURITY_GROUP_2
}
NOVA_SECURITY_GROUP_RULE_2 = {
    'id': random_os_id(),
    'from_port': None,
    'to_port': None,
    'ip_protocol': 'icmp',
    'group': {'name': 'groupname'},
    'ip_range': None,
    'parent_group_id': ID_OS_SECURITY_GROUP_2
}
NOVA_SECURITY_GROUP_1 = {
    'id': ID_OS_SECURITY_GROUP_1,
    'name': 'groupname',
    'security_group_rules':
    [{'group': None,
      'ip_range': None,
      'ip_protocol': None,
      'to_port': None,
      'parent_group_id': ID_OS_SECURITY_GROUP_1,
      'from_port': None,
      'id': random_os_id()}],
    'description': 'Group description',
    'tenant_id': ID_OS_PROJECT
}
NOVA_SECURITY_GROUP_2 = {
    'id': ID_OS_SECURITY_GROUP_2,
    'name': 'groupname2',
    'security_group_rules': [
        NOVA_SECURITY_GROUP_RULE_1,
        NOVA_SECURITY_GROUP_RULE_2
    ],
    'description': 'Group description',
    'tenant_id': ID_OS_PROJECT
}
EC2_SECURITY_GROUP_1 = {
    'vpcId': ID_EC2_VPC_1,
    'groupDescription': 'Group description',
    'ipPermissions': None,
    'groupName': 'groupname',
    'ipPermissionsEgress':
    [{'toPort': -1,
      'ipProtocol': -1,
      'fromPort': -1}],
    'ownerId': ID_OS_PROJECT,
    'groupId': ID_EC2_SECURITY_GROUP_1
}
EC2_SECURITY_GROUP_2 = {
    'vpcId': ID_EC2_VPC_1,
    'groupDescription': 'Group description',
    'ipPermissions':
    [{'toPort': 10,
      'ipProtocol': 'tcp',
      'fromPort': 10,
      'ipRanges':
      [{'cidrIp': '192.168.1.0/24'}]
      }],
    'groupName': 'groupname2',
    'ipPermissionsEgress':
    [{'toPort': -1,
      'ipProtocol': 100,
      'fromPort': 10,
      'groups':
      [{'groupId': ID_EC2_SECURITY_GROUP_1,
        'groupName': 'groupname',
        'userId': ID_OS_PROJECT}]
      }],
    'ownerId': ID_OS_PROJECT,
    'groupId': ID_EC2_SECURITY_GROUP_2
}
EC2_NOVA_SECURITY_GROUP_1 = {
    'groupDescription': 'Group description',
    'ipPermissions': None,
    'groupName': 'groupname',
    'ipPermissions':
    [{'toPort': 65535,
      'ipProtocol': 'tcp',
      'fromPort': 1},
     {'toPort': 65535,
      'ipProtocol': 'udp',
      'fromPort': 1},
     {'toPort': -1,
      'ipProtocol': 'icmp',
      'fromPort': -1}],
    'ownerId': ID_OS_PROJECT,
}
EC2_NOVA_SECURITY_GROUP_2 = {
    'groupDescription': 'Group description',
    'groupName': 'groupname2',
    'ipPermissions':
    [{'toPort': 10,
      'ipProtocol': 'tcp',
      'fromPort': 10,
      'ipRanges':
      [{'cidrIp': '192.168.1.0/24'}]
      },
     {'toPort': -1,
      'ipProtocol': 'icmp',
      'fromPort': -1,
      'groups':
      [{'groupName': 'groupname',
        'userId': ID_OS_PROJECT}]
      }],
    'ownerId': ID_OS_PROJECT,
}


# route table objects
DB_ROUTE_TABLE_1 = {
    'id': ID_EC2_ROUTE_TABLE_1,
    'vpc_id': ID_EC2_VPC_1,
    'routes': [{'destination_cidr_block': CIDR_VPC_1,
                'gateway_id': None}],
}
DB_ROUTE_TABLE_2 = {
    'id': ID_EC2_ROUTE_TABLE_2,
    'vpc_id': ID_EC2_VPC_1,
    'routes': [{'destination_cidr_block': CIDR_VPC_1,
                'gateway_id': None},
               {'destination_cidr_block': CIDR_EXTERNAL_NETWORK,
                'network_interface_id': ID_EC2_NETWORK_INTERFACE_2},
               {'destination_cidr_block': '0.0.0.0/0',
                'gateway_id': ID_EC2_IGW_1}],
}
EC2_ROUTE_TABLE_1 = {
    'routeTableId': ID_EC2_ROUTE_TABLE_1,
    'vpcId': ID_EC2_VPC_1,
    'routeSet': [
        {'destinationCidrBlock': CIDR_VPC_1,
         'gatewayId': 'local',
         'state': 'active',
         'origin': 'CreateRouteTable'}],
    'associationSet': [
        {'routeTableAssociationId': ID_EC2_ROUTE_TABLE_ASSOCIATION_1,
         'routeTableId': ID_EC2_ROUTE_TABLE_1,
         'main': True}],
    'tagSet': [],
}
EC2_ROUTE_TABLE_2 = {
    'routeTableId': ID_EC2_ROUTE_TABLE_2,
    'vpcId': ID_EC2_VPC_1,
    'routeSet': [
        {'destinationCidrBlock': CIDR_VPC_1,
         'gatewayId': 'local',
         'state': 'active',
         'origin': 'CreateRouteTable'},
        {'destinationCidrBlock': CIDR_EXTERNAL_NETWORK,
         'instanceId': ID_EC2_INSTANCE_1,
         'instanceOwnerId': ID_OS_PROJECT,
         'networkInterfaceId': ID_EC2_NETWORK_INTERFACE_2,
         'state': 'active',
         'origin': 'CreateRoute'},
        {'destinationCidrBlock': '0.0.0.0/0',
         'gatewayId': ID_EC2_IGW_1,
         'state': 'active',
         'origin': 'CreateRoute'}],
    'tagSet': [],
}


# image objects
class OSImage(object):

    def __init__(self, image_dict):
        self.id = image_dict['id']
        self.owner = image_dict['owner']
        self.is_public = image_dict['is_public']
        self.status = image_dict['status']
        self.container_format = image_dict['container_format']
        self.name = image_dict['name']
        self.properties = copy.deepcopy(image_dict['properties'])

    def update(self, **kwargs):
        pass

EC2_IMAGE_1 = {
    'imageId': ID_EC2_IMAGE_1,
    'imageOwnerId': ID_OS_PROJECT,
    'isPublic': False,
    'imageState': 'available',
    'imageType': 'machine',
    'name': 'fake_name',
    'description': None,
    'imageLocation': 'None (fake_name)',
    'kernelId': ID_EC2_IMAGE_AKI_1,
    'ramdiskId': ID_EC2_IMAGE_ARI_1,
    'architecture': None,
    'rootDeviceType': 'instance-store',
    'rootDeviceName': ROOT_DEVICE_NAME_IMAGE_1,
    'blockDeviceMapping': [
        {'deviceName': '/dev/sdb0',
         'virtualName': 'ephemeral0'},
        {'deviceName': '/dev/sdb1',
         'ebs': {'snapshotId': ID_EC2_SNAPSHOT_1}},
        {'deviceName': '/dev/sdb2',
         'ebs': {'snapshotId': ID_EC2_VOLUME_1}},
        {'deviceName': '/dev/sdb3',
         'virtualName': 'ephemeral5'},
        {'deviceName': '/dev/sdc0',
         'virtualName': 'swap'},
        {'deviceName': '/dev/sdc1',
         'ebs': {'snapshotId': ID_EC2_SNAPSHOT_2}},
        {'deviceName': '/dev/sdc2',
         'ebs': {'snapshotId': ID_EC2_VOLUME_2}},
        {'deviceName': '/dev/sdc3',
         'virtualName': 'ephemeral6'}],
}
EC2_IMAGE_2 = {
    'imageId': ID_EC2_IMAGE_2,
    'imageOwnerId': ID_OS_PROJECT,
    'isPublic': True,
    'imageState': 'available',
    'imageType': 'machine',
    'name': None,
    'description': None,
    'imageLocation': 'None (None)',
    'architecture': None,
    'rootDeviceType': 'instance-store',
    'rootDeviceName': ROOT_DEVICE_NAME_IMAGE_2,
    'blockDeviceMapping': [
        {'deviceName': '/dev/sdb1',
         'ebs': {'snapshotId': ID_EC2_SNAPSHOT_1}}],
}


DB_IMAGE_1 = {
    'id': ID_EC2_IMAGE_1,
    'os_id': ID_OS_IMAGE_1,
    'is_public': False,
}
DB_IMAGE_2 = {
    'id': ID_EC2_IMAGE_2,
    'os_id': ID_OS_IMAGE_2,
    'is_public': True,
}

OS_IMAGE_1 = {
    'id': ID_OS_IMAGE_1,
    'owner': ID_OS_PROJECT,
    'is_public': False,
    'status': 'active',
    'container_format': 'ami',
    'name': 'fake_name',
    'properties': {
        'kernel_id': ID_OS_IMAGE_AKI_1,
        'ramdisk_id': ID_OS_IMAGE_ARI_1,
        'type': 'machine',
        'image_state': 'available',
        'mappings': json.dumps([
            {'device': '/dev/sda1', 'virtual': 'root'},
            {'device': 'sdb0', 'virtual': 'ephemeral0'},
            {'device': 'sdb1', 'virtual': 'ephemeral1'},
            {'device': 'sdb2', 'virtual': 'ephemeral2'},
            {'device': 'sdb3', 'virtual': 'ephemeral3'},
            {'device': 'sdb4', 'virtual': 'ephemeral4'},
            {'device': 'sdc0', 'virtual': 'swap'},
            {'device': 'sdc1', 'virtual': 'swap'},
            {'device': 'sdc2', 'virtual': 'swap'},
            {'device': 'sdc3', 'virtual': 'swap'},
            {'device': 'sdc4', 'virtual': 'swap'}]),
        'block_device_mapping': json.dumps([
            {'device_name': '/dev/sdb1',
             'snapshot_id': ID_OS_SNAPSHOT_1},
            {'device_name': '/dev/sdb2',
             'volume_id': ID_OS_VOLUME_1},
            {'device_name': '/dev/sdb3', 'virtual_name': 'ephemeral5'},
            {'device_name': '/dev/sdb4', 'no_device': True},
            {'device_name': '/dev/sdc1',
             'snapshot_id': ID_OS_SNAPSHOT_2},
            {'device_name': '/dev/sdc2',
             'volume_id': ID_OS_VOLUME_2},
            {'device_name': '/dev/sdc3', 'virtual_name': 'ephemeral6'},
            {'device_name': '/dev/sdc4', 'no_device': True}]),
        }
}
OS_IMAGE_2 = {
    'id': ID_OS_IMAGE_2,
    'owner': ID_OS_PROJECT,
    'is_public': True,
    'status': 'active',
    'container_format': 'ami',
    'name': None,
    'properties': {
        'type': 'machine',
        'root_device_name': '/dev/sdb1',
        'mappings': json.dumps([{'device': '/dev/sda1',
                      'virtual': 'root'}]),
        'block_device_mapping': json.dumps([
            {'device_name': '/dev/sdb1',
             'snapshot_id': ID_OS_SNAPSHOT_1}]),
    }
}


# snapshot objects
class OSSnapshot(object):

    def __init__(self, snapshot_dict):
        self.id = snapshot_dict['id']


DB_SNAPSHOT_1 = {
    'id': ID_EC2_SNAPSHOT_1,
    'os_id': ID_OS_SNAPSHOT_1,
}
DB_SNAPSHOT_2 = {
    'id': ID_EC2_SNAPSHOT_2,
    'os_id': ID_OS_SNAPSHOT_2,
}

OS_SNAPSHOT_1 = {
    'id': ID_OS_SNAPSHOT_1,
}
OS_SNAPSHOT_2 = {
    'id': ID_OS_SNAPSHOT_2,
}


# availability zone objects

class NovaAvailabilityZone(object):

    def __init__(self, nova_availability_zone_dict):
        self.zoneName = nova_availability_zone_dict['zoneName']
        self.zoneState = {'available':
            nova_availability_zone_dict['zoneState'] == 'available'}
        self.hosts = nova_availability_zone_dict['hosts']

OS_AVAILABILITY_ZONE = {'zoneName': 'nova',
                        'zoneState': 'available',
                        'hosts': {'host1': {'service1': {
                                                'active': 'True',
                                                'available': 'True',
                                                'updated_at': 'now'},
                                            'service2': {
                                                'active': 'False',
                                                'available': 'False',
                                                'updated_at': 'now'}},
                                  'host2': {'service1': {
                                                'active': 'True',
                                                'available': 'True',
                                                'updated_at': 'now'}}
                                   }}
OS_AVAILABILITY_ZONE_INTERNAL = {'zoneName': 'internal',
                                 'zoneState': 'available',
                                 'hosts': {}}
EC2_AVAILABILITY_ZONE = {'zoneName': 'nova',
                         'zoneState': 'available'}


# keypair objects

class NovaKeyPair(object):

    def __init__(self, nova_keypair_dict):
        self.name = nova_keypair_dict['name']
        self.fingerprint = nova_keypair_dict['fingerprint']
        self.private_key = nova_keypair_dict['private_key']
        self.public_key = nova_keypair_dict['public_key']

PRIVATE_KEY = (
    '-----BEGIN RSA PRIVATE KEY-----\n'
    'MIIEowIBAAKCAQEAgXvm1sZ9MDiAXvGraRFja0/WqyJ1gE6j/QPjreNryd34zBFcv2pQXLyvb'
    'gQG\nFxN4rMGNScgKgLSgHjE/TNywkT8N7aYOiRmGkzQciP5t+zf8ZdCyl+hqgoQig1uY8sV/'
    'fSxUWCB9\n8sF7Tpl0iGkWM6Wo0H/PvcwiS2+UPSzArj+b+Erb/JbBF4O8GgSmtLMeq60RuDM'
    'dJi5JYCP66HUw\njtYb/f9y1Q9nEGVcxY2v0RI1n0yOaZDKPInLKHeR/ole2QVwPZB69mBj11'
    'LErqb+jzCaSivnhy6g\nPzaSHdZaRmy1f+6ltFI1iKt+4y/iINOY0skYC1hc7IevE7j7dGQTD'
    'wIDAQABAoIBAEbD2Vfd6MM2\nzemVuHFWoHggjRjAX2k9EWCRBJifJuSPXI7imka+qqbUNCgz'
    'KMTpzlTT/wyouBy5Gp0Fmyu9nP30\ncP9FdsI04hiHLWUtcBwQ7+8RDNn6mmM0JcyWfdOIXnG'
    'hjYMQVuUaGvLM6SQ4EnsteUJh57451zBV\nDbYVRES2Fbq+j8tPQj1KuD0HhZBboNPOxo6E5n'
    'TxvMXnvuI+cb9D99lqATcb8c0zsLMl/5SKEBDc\nj72X4GPfE3Dc5/MO6L/89ms3TqF3lx8lh'
    'wFSMfFfA3Nf5xrX3gnorGe81odXBXFveqMCemvfJYxg\nS9KPkM8CMnwn6yPS3ftW5xH3nMkC'
    'gYEAvN4lQuOTy9RONCtfgZ6lhR00xfDiibOsE2jFXqXlXrZS\nunBx2WRwNuhAcYGbC4T71iC'
    'BR+LJHECpFjEFX9cKjd8xZPdIzJmwMBylPnli8IxK9UMroxF/MDNy\nnJfdPIWagIrk9VRsQH'
    'UOQW8Ab5dYJuP6c03L5xwmnFfeFnlz10MCgYEAr4Iu182bC2ppwr5AYD8T\n/QKVPZTmizbtG'
    'H/7a2+WnfNCz2u0MOo2h1rF7/SOYR8nalTTsN1z4D8cRX7YQ0P4yBtNRNiN7WH3\n+smTWztI'
    'VYvJA2RsOeP0zfGLJiFSMWLOjlqpJ7KbkEuPcxshGd+/w8upxgJeV8Dwz0ZWbY302kUC\ngYE'
    'AhneTB+CHpaNuWm5W/S46ol9850DtySSG6vq5Kv3qJFii5eKQ7Do6Op145FdmT/lKY9WYtdmd'
    '\nXeQbfpVAQlAUT5YM0NnOlv0FF/wNGkHKU4FPDPfZ5avbZjH688qb1S86JTK+eHy25d1xXNz'
    'u7oRO\nWsIN2nIVLmI4iy90C4RFGYkCgYBXpKPtwk/VkItF46nUJku+Agcy3GOQS5p0rJyJ1w'
    'yYzbykRf2S\nm7MlPpAvtqlPGLafI8MexEe0SO++SIyIcq4Oh4u7gITHcS/bfcPnQCBsD8UOu'
    '5xMAGjkWuWI4gTg\ngp3xepaUK14B3anB6l9KQ3DIvrCGH/Kq0b+vUkmgpc4LHQKBgBtul9bN'
    'KLF+LJf4JHYNFSurE8Y/\nn8FZ3dZo3T0Q3Sap9bP3ZHemoQ6QXbmpu3H4Mf+2kcNg6YKFW3p'
    'hxW3cuAcZOMHPCrpr3mCdyhF0\nKM74ANEwg8MekBJTcWZUNFv9HZDvTuhp6HSrbMnNEQogkd'
    '5PoubiusvAKpeb6NBGnLMq\n'
    '-----END RSA PRIVATE KEY-----'
)

PUBLIC_KEY = ('ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDIkYwwXm8UeQXx1c2eFrDIB6b'
              '6ApI0KTKs1wezDfFdSIs93vAt4Jx1MyaR/PwqwLk2CDyFoGJBWBI9YcodLAjoRg'
              'Ovr6JigEv5V3yp+eEkeAJO0cPA21vN/KQ8Vxml68ZvvqbdqKZXc/rpFZ1OgCmHt'
              'udo96uQiRB0FM3mdE8YOTswcfkJxTvCe3axX50pYXXfIb0dn9CzC1hyQWYPXvlv'
              'qFNvr/Li7sSBycTBAh4Ar/uEigs/uOjhvzd7GpzY7qDqBVJFAmP7HiiOxoXPkKu'
              'W62Ftd')

KEY_FINGERPRINT = '2a:72:dd:aa:0d:a6:45:4d:27:4f:75:28:73:0d:a6:10:35:88:e1:ce'

OS_KEY_PAIR = {'name': 'keyname',
               'private_key': PRIVATE_KEY,
               'public_key': PUBLIC_KEY,
               'fingerprint': KEY_FINGERPRINT}

EC2_KEY_PAIR = {'keyName': 'keyname',
                'keyFingerprint': KEY_FINGERPRINT,
                'keyMaterial': PRIVATE_KEY}


# Object generator functions section

# internet gateway generator functions
def gen_db_igw(ec2_id, ec2_vpc_id=None):
    return {'id': ec2_id,
            'os_id': None,
            'vpc_id': ec2_vpc_id}


# network interface generator functions
def gen_db_network_interface(ec2_id, os_id, vpc_ec2_id, subnet_ec2_id,
                             private_ip_address, description=None,
                             instance_id=None, delete_on_termination=False):
    eni = {'id': ec2_id,
           'os_id': os_id,
           'vpc_id': vpc_ec2_id,
           'subnet_id': subnet_ec2_id,
           'description': description,
           'private_ip_address': private_ip_address}
    if instance_id:
        eni['instance_id'] = instance_id
        eni['delete_on_termination'] = delete_on_termination
        eni['attach_time'] = TIME_ATTACH_NETWORK_INTERFACE
    return eni


def gen_ec2_network_interface(ec2_network_interface_id, ec2_subnet, ips,
                              description=None, ec2_instance_id=None,
                              delete_on_termination=False,
                              for_instance_output=False,
                              ec2_subnet_id=None,
                              ec2_vpc_id=None):
    """Generate EC2 Network Interface dictionary.

    Set privateIpAddres from the first element of ips.
    If ec2_subnet_id and ec2_vpc_id are used if passed instead of getting
    appropriate values from ec2_subnet
    """
    ec2_network_interface = {
        'networkInterfaceId': ec2_network_interface_id,
        'vpcId': ec2_vpc_id if ec2_vpc_id else ec2_subnet['vpcId'],
        'subnetId': ec2_subnet_id if ec2_subnet_id else ec2_subnet['subnetId'],
        'description': description,
        'macAddress': 'fb:10:2e:b2:ba:b7',
        'privateIpAddress': ips[0],
        'privateIpAddressesSet': [{'privateIpAddress': ip,
                                   'primary': ip == ips[0]}
                                  for ip in ips],
        'sourceDestCheck': True,
        'ownerId': ID_OS_PROJECT,
        'requesterManaged': False,
        'groupSet': [],
    }
    if not ec2_instance_id:
        ec2_network_interface['status'] = 'available'
    else:
        attachment_id = ec2_network_interface_id.replace('eni', 'eni-attach')
        attachment = {'status': 'attached',
                      'attachTime': TIME_ATTACH_NETWORK_INTERFACE,
                      'deleteOnTermination': delete_on_termination,
                      'attachmentId': attachment_id}
        if not for_instance_output:
            attachment.update({
                'instanceId': ec2_instance_id,
                'instanceOwnerId': ID_OS_PROJECT})
        ec2_network_interface['status'] = 'in-use'
        ec2_network_interface['attachment'] = attachment
    return ec2_network_interface


def gen_os_port(os_id, ec2_network_interface, os_subnet_id, fixed_ips,
                os_instance_id=None):
    return {'id': os_id,
            'network_id': os_subnet_id,
            'name': ec2_network_interface['networkInterfaceId'],
            'status': 'ACTIVE' if os_instance_id else 'DOWN',
            'mac_address': 'fb:10:2e:b2:ba:b7',
            'fixed_ips': [{'ip_address': ip, 'subnet_id': os_subnet_id}
                          for ip in fixed_ips],
            'device_id': os_instance_id,
            'security_groups': []}


# instance generator functions
def gen_ec2_instance(ec2_instance_id, private_ip_address='',
                     ec2_network_interfaces=None, is_private_ip_in_vpc=True,
                     floating_ip=None):
    """Generate EC2 Instance dictionary.

    private_ip_address must be specified as IP value or None
    Set vpcId from the first ec2_network_interfaces
    If private_ip_address is not None, set subnetId from the first
    ec2_network_interfaces
    """
    ec2_instance = {'instanceId': ec2_instance_id,
                    'privateIpAddress': private_ip_address,
                    'amiLaunchIndex': 0,
                    'placement': {'availabilityZone': None},
                    'dnsName': floating_ip,
                    'instanceState': {'code': 0, 'name': 'pending'},
                    'imageId': None,
                    'productCodesSet': [],
                    'privateDnsName': ec2_instance_id,
                    'keyName': None,
                    'launchTime': None,
                    'rootDeviceType': 'instance-store',
                    'instanceType': 'fake_flavor',
                    'rootDeviceName': '/dev/vda'}
    if floating_ip is not None:
        ec2_instance['ipAddress'] = floating_ip
    if ec2_network_interfaces is not None:
        ec2_instance['networkInterfaceSet'] = (
            [ni for ni in ec2_network_interfaces])
        ec2_instance['vpcId'] = ec2_network_interfaces[0]['vpcId']
        if private_ip_address and is_private_ip_in_vpc:
            ec2_instance['subnetId'] = ec2_network_interfaces[0]['subnetId']
    return ec2_instance


def gen_ec2_reservation(ec2_reservation_id, ec2_instances):
    """Generate EC2 Reservation dictionary."""
    return {'reservationId': ec2_reservation_id,
            'ownerId': ID_OS_PROJECT,
            'instancesSet': [inst for inst in ec2_instances]}
