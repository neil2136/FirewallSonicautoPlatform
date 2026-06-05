from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_add_address_object(self):
        rc = 0
        address_object_lists =[
            {
                'name': 'lan_range',
                'zone': 'LAN',
                'object_type': 'range',
                'value': '192.168.168.169,192.168.168.171',
            },
            {
                'name': 'wan_range',
                'zone': 'WAN',
                'object_type': 'range',
                'value': '6.6.6.5,6.6.6.6',
            },
            {
                'name': 'wan_dst',
                'zone': 'WAN',
                'object_type': 'host',
                'value': WAN_HOST,
            },
            {
                'name': 'wan1',
                'zone': 'WAN',
                'object_type': 'host',
                'value': PC2_ETH0_IP,
            },
            {
                'name': 'wan2',
                'zone': 'WAN',
                'object_type': 'host',
                'value': PC3_ETH0_IP,
            },
            {
                'name': 'lan1',
                'zone': 'LAN',
                'object_type': 'host',
                'value': PC1_ETH0_IP,
            },
            {
                'name': 'lan2',
                'zone': 'LAN',
                'object_type': 'host',
                'value': PC5_ETH0_IP,
            },
            {
                'name': 'lan3',
                'zone': 'LAN',
                'object_type': 'host',
                'value': PC6_ETH0_IP,
            },
        ]

        for item in address_object_lists:
            ret = address_obj.config_addressobject(msg=True, **item )
            if ret[0]:
                rc += 1
                logger.info('Add {} address objects success.'.format(item['name']))
            elif 'Already exists' in ret[1]['status']['info'][0]['message']:
                rc += 1
                logger.info('Address Object already exists')
            else:
                logger.info('Add {} Failed'.format(item['name']))
        Assertion.assert_equal(rc, len(address_object_lists), "ERR: Add address objects failed")

    def test_03_add_address_object_group(self):
        ag_param1 = {
            'address_groups': [{
                'ipv4':{
                    'name': 'wan_group',
                    'address_object': {'ipv4': [
                        {'name': 'wan1'},
                        {'name': 'wan2'}
                    ]}
                }
            }]
        }
        rc1 = address_group_obj.add_addressgroup(**ag_param1)
        ag_param2 = {
            'address_groups': [{
                'ipv4':{
                    'name': 'lan_group',
                    'address_object': {'ipv4': [
                        {'name': 'lan1'},
                        {'name': 'lan2'},
                        {'name': 'lan3'}
                    ]}
                }
            }]
        }
        rc2 = address_group_obj.add_addressgroup(**ag_param2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Failed To Add Address object Groups")
      
    def test_04_add_nat_policy(self):
        nat_json = {
            "nat_policies": [
            {
                "ipv4": {
                    "uuid": "00000000-0000-0001-0800-2cb8ed6d8008",
                    "name": "my_nat_policy",
                    "enable": True,
                    "comment": "",
                    "dns_doctoring": False,
                    "inbound": "any",
                    "outbound": "any",
                    "source": {
                        "name": "lan_range"
                    },
                    "translated_source": {
                        "original": True
                    },
                    "destination": {
                        "name": "wan_dst"
                    },
                    "translated_destination": {
                        "name": "wan_range"
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    }
                }
                }
            ]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR:add nat policy failed")
