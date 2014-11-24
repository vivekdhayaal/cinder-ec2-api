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


import mock
import testtools

from ec2api.api import ec2utils
from ec2api import exception
from ec2api.tests import fakes
from ec2api.tests import matchers


class EC2UtilsTestCase(testtools.TestCase):

    @mock.patch('ec2api.db.api.IMPL')
    def test_get_db_item(self, db_api):
        item = {'fake_key': 'fake_value'}
        db_api.get_item_by_id.return_value = item

        def check_normal_flow(kind, ec2_id):
            item['id'] = ec2_id
            res = ec2utils.get_db_item('fake_context', kind, ec2_id)
            self.assertThat(res, matchers.DictMatches(item))
            db_api.get_item_by_id.assert_called_once_with('fake_context',
                                                          kind, ec2_id)
            db_api.reset_mock()

        check_normal_flow('vpc', 'vpc-001234af')
        check_normal_flow('igw', 'igw-00000022')

        def check_not_found(kind, ec2_id, ex_class):
            self.assertRaises(ex_class,
                              ec2utils.get_db_item,
                              'fake_context', kind, ec2_id)
            db_api.get_item_by_id.assert_called_once_with('fake_context',
                                                          kind, ec2_id)
            db_api.reset_mock()

        db_api.get_item_by_id.return_value = None
        check_not_found('vpc', 'vpc-00000022',
                        exception.InvalidVpcIDNotFound)
        check_not_found('igw', 'igw-00000022',
                        exception.InvalidInternetGatewayIDNotFound)
        check_not_found('subnet', 'subnet-00000022',
                        exception.InvalidSubnetIDNotFound)
        check_not_found('eni', 'eni-00000022',
                        exception.InvalidNetworkInterfaceIDNotFound)
        check_not_found('dopt', 'dopt-00000022',
                        exception.InvalidDhcpOptionsIDNotFound)
        check_not_found('eipalloc', 'eipalloc-00000022',
                        exception.InvalidAllocationIDNotFound)
        check_not_found('sg', 'sg-00000022',
                        exception.InvalidGroupNotFound)
        check_not_found('rtb', 'rtb--00000022',
                        exception.InvalidRouteTableIDNotFound)
        check_not_found('i', 'i-00000022',
                        exception.InvalidInstanceIDNotFound)

    @mock.patch('ec2api.db.api.IMPL')
    def test_get_db_items(self, db_api):
        items = [{'id': fakes.random_ec2_id('fake'),
                  'fake_key': 'fake_value'},
                 {'id': fakes.random_ec2_id('fake'),
                  'fake_key': 'fake_value'}]
        db_api.get_items.return_value = items
        db_api.get_items_by_ids.return_value = items

        def check_with_no_filter(empty_filter):
            res = ec2utils.get_db_items('fake_context', 'fake', empty_filter)
            self.assertThat(res, matchers.ListMatches(items))
            db_api.get_items.assert_called_once_with('fake_context', 'fake')
            db_api.reset_mock()

        check_with_no_filter(None)
        check_with_no_filter([])

        def check_with_filter(item_ids):
            res = ec2utils.get_db_items('fake_context', 'fake', item_ids)
            self.assertThat(res, matchers.ListMatches(items))
            db_api.get_items_by_ids.assert_called_once_with(
                'fake_context', 'fake', set(item_ids))
            db_api.reset_mock()

        item_ids = [i['id'] for i in items]
        check_with_filter(item_ids)
        check_with_filter(item_ids * 2)

        def check_not_found(kind, ex_class):
            items = [{'id': fakes.random_ec2_id(kind),
                      'fake_key': 'fake_value'} for _ in range(2)]
            item_ids = [i['id'] for i in items]
            item_ids.append(fakes.random_ec2_id(kind))
            db_api.get_items_by_ids.return_value = items
            self.assertRaises(ex_class, ec2utils.get_db_items,
                              'fake_context', kind, item_ids)
            db_api.reset_mock()

        check_not_found('vpc', exception.InvalidVpcIDNotFound)
        check_not_found('igw', exception.InvalidInternetGatewayIDNotFound)
        check_not_found('subnet', exception.InvalidSubnetIDNotFound)
        check_not_found('eni', exception.InvalidNetworkInterfaceIDNotFound)
        check_not_found('dopt', exception.InvalidDhcpOptionsIDNotFound)
        check_not_found('eipalloc', exception.InvalidAllocationIDNotFound)
        check_not_found('sg', exception.InvalidGroupNotFound)
        check_not_found('rtb', exception.InvalidRouteTableIDNotFound)
        check_not_found('i', exception.InvalidInstanceIDNotFound)

    def test_validate_cidr(self):
        self.assertIsNone(ec2utils.validate_cidr('10.10.0.0/24', 'cidr'))

        def check_raise_invalid_parameter(cidr):
            self.assertRaises(exception.InvalidParameterValue,
                              ec2utils.validate_cidr, cidr, 'cidr')

        check_raise_invalid_parameter('fake')
        check_raise_invalid_parameter('10.10/24')
        check_raise_invalid_parameter('10.10.0.0.0/24')
        check_raise_invalid_parameter('10.10.0.0')
        check_raise_invalid_parameter(' 10.10.0.0/24')
        check_raise_invalid_parameter('10.10.0.0/24 ')
        check_raise_invalid_parameter('.10.10.0.0/24 ')
        check_raise_invalid_parameter('-1.10.0.0/24')
        check_raise_invalid_parameter('10.256.0.0/24')
        check_raise_invalid_parameter('10.10.0.0/33')
        check_raise_invalid_parameter('10.10.0.0/-1')

        def check_raise_invalid_vpc_range(cidr, ex_class):
            self.assertRaises(ex_class,
                              ec2utils.validate_vpc_cidr, cidr,
                              ex_class)

        check_raise_invalid_vpc_range('10.10.0.0/15',
                                      exception.InvalidSubnetRange)
        check_raise_invalid_vpc_range('10.10.0.0/29',
                                      exception.InvalidVpcRange)
