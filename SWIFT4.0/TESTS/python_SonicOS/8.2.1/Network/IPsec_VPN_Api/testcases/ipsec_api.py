import sys
import os
import json
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPsec_VPN_Api/')
from definition.settings import *

class TC00_NonTC(Test):
    uuid = 'NonTC'

    def test_00_post_address_ip4_object(self):

        address_object1 = {
            "object_type": "range",
            "name": "sslvpn_range1",
            "zone": "SSLVPN",
            "value": "192.168.168.10,192.168.168.20"
        }
        resp = address_object.config_addressobject(**address_object1)
        resp1 = address_object.get_addressobject_by_name("sslvpn_range1", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "sslvpn_range1"', "Err: failed to create address object")

        address_object2 = {
            "object_type": "host",
            "name": "remote_address_zone",
            "zone": "LAN",
            "value": "192.168.168.11"
        }
        resp = address_object.config_addressobject(**address_object2)
        resp1 = address_object.get_addressobject_by_name("remote_address_zone", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "remote_address_zone"', "Err: failed to create address object")




class TC01_check_site_to_site_manual(Test):
    uuid = "SOSAIOT-TC-47607"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510890')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_ipv4vpnpolicy(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.10.10.89"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "remote_address_zone"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "in_spi": "0x0b910a59",
                                        "out_spi": "0xdb9d9c98",
                                        "encryption_key": "1319aa2f5cd29935deef74a9c94bdaa5",
                                        "authentication_key": "",
                                        "authentication": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }

        resp = vpn_base.add_site_to_site_ipv4(**obj)
        Assertion.assert_regular(json.dumps(resp), 'true', "err: not able to create policy")



class TC02_edit_site_to_site_vpn_local_network(Test):
    uuid = "SOSAIOT-TC-47608"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510891')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ipv4vpnpolicy_local_network(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.5.9.88"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70",
                                        "encryption": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv4("testcase1", **obj)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")



class TC03_edit_translated_local_network(Test):
    uuid = "SOSAIOT-TC-47610"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510893')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_translated_local_network(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.5.9.88"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70",
                                        "encryption": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_auto_add_rule": False,
                                "apply_nat": True,
                                "translated_network": {
                                    "local": {
                                        "name": "X0 Subnet"
                                    },
                                    "remote": {
                                        "name": "sslvpn_range1"
                                    }
                                },
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv4("testcase1", **obj)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")


class TC04_edit_translated_local_network(Test):
    uuid = "SOSAIOT-TC-47611"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510894')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Create_Address_Group(self):
        ag_param = {
            'address_groups': [{
                'ipv4':{
                    'name': 'TestAddressGroupA',
                    'address_group': {'ipv4': [
                        {'name': 'LAN Interface IP'},
                        {'name': 'DMZ Interface IP'}
                    ]}
                }
            }]
        }
        rc = address_object_group_api.add_addressgroup(**ag_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Failed To Add Address Group")

    def test_02_edit_translated_local_network(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.5.9.88"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70",
                                        "encryption": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_auto_add_rule": False,
                                "apply_nat": True,
                                "translated_network": {
                                    "local": {
                                        "group": "TestAddressGroupA"
                                    },
                                    "remote": {
                                        "group": "TestAddressGroupA"
                                    }
                                },
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv4("testcase1", **obj)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")




class TC05_edit_vpn_policy_base(Test):
    uuid = "SOSAIOT-TC-47612"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510895')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_ipsec_with_vpn_policy_base(self):
        ipv4policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "t6",
                                "enable": True,
                                "gateway": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "abcd",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-256",
                                        "dh_group": "2",
                                        "lifetime": 28800,
                                        "authentication": "sha-256"
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_gcm16_256": True
                                        },
                                        "authentication": {},
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "netbios": False,
                                "anti_replay": True,
                                "multicast": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }

        resp = vpn_base.add_site_to_site_ipv4(**ipv4policy)
        Assertion.assert_regular(json.dumps(resp), 'true', "err: not able to create policy")

    def test_02_edit_ipsec_with_vpn_policy_base_with_WAN_Zone(self):
        ipv4policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "t6",
                                "enable": True,
                                "gateway": {
                                    "primary": "",
                                    "secondary": ""
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "abcd",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-128",
                                        "dh_group": "2",
                                        "lifetime": 28800,
                                        "authentication": "sha-1"
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_gcm16_256": True
                                        },
                                        "authentication": {},
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "netbios": False,
                                "anti_replay": True,
                                "multicast": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "",
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "bound_to": {
                                    "zone": "WAN"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv4("t6", **ipv4policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

    def test_03_delete_ipv4_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("t6")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")


class TC06_create_vpn_policy_auth_md5_phase2(Test):
    uuid = "SOSAIOT-TC-47613"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510896')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_vpn_policy_auth_md5_phase2(self):
        obj={
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "t7",
                                "enable": True,
                                "gateway": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "abcd",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-256",
                                        "dh_group": "2",
                                        "lifetime": 28800,
                                        "authentication": "sha-256"
                                    },
                                    "ipsec": {
                                        "protocol": "ah",
                                        "authentication": {
                                            "md5": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "netbios": False,
                                "anti_replay": True,
                                "multicast": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "zone": "WAN"
                                }
                            }
                        }
                    }
                ]
            }
        }

        resp = vpn_base.add_site_to_site_ipv4(**obj)
        Assertion.assert_regular(json.dumps(resp), 'true', "err: not able to create policy")


class TC07_edit_authentication_SHA1(Test):
    uuid = "SOSAIOT-TC-47609"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510892')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_authentication_SHA1(self):
        ipv4policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "t7",
                                "enable": True,
                                "gateway": {
                                    "primary": "0.0.0.0",
                                    "secondary": "0.0.0.0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "abcd",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-256",
                                        "dh_group": "2",
                                        "lifetime": 28800,
                                        "authentication": "sha-256"
                                    },
                                    "ipsec": {
                                        "protocol": "ah",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "netbios": False,
                                "anti_replay": True,
                                "multicast": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "suppress_auto_add_rule": False,
                                "apply_nat": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "zone": "WAN"
                                }
                            }
                        }
                    }
                ]
            }
        }

        resp = vpn_base.edit_site_to_site_ipv4("t7", **ipv4policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

    def test_02_delete_ipv4_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("t7")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")


class TC08_create_ipsec_with_translated_local_ntw(Test):
    uuid = "SOSAIOT-TC-47614"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510897')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ipv4_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("testcase1")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")


    def test_02_create_ipsec_with_translated_local_ntw(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase8",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.5.9.88"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70",
                                        "encryption": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_auto_add_rule": False,
                                "apply_nat": True,
                                "translated_network": {
                                    "local": {
                                        "name": "X0 Subnet"
                                    },
                                    "remote": {
                                        "name": "sslvpn_range1"
                                    }
                                },
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv4(**obj)
        Assertion.assert_regular(json.dumps(resp), 'true', "err: not able to create policy")

    def test_03_delete_ipv4_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("testcase8")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")


class TC09_create_ipsec_with_host_in_translated_local_ntw(Test):
    uuid = "SOSAIOT-TC-47615"

    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510898')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_ipsec_with_translated_local_ntw(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase9",
                                "enable": True,
                                "gateway": {
                                    "primary": "10.5.9.88"
                                },
                                "auth_method": {
                                    "manual_key": True
                                },
                                "network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70",
                                        "encryption": {}
                                    }
                                },
                                "netbios": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "user_login": {
                                    "http": False,
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "suppress_auto_add_rule": False,
                                "apply_nat": True,
                                "translated_network": {
                                    "local": {
                                        "name": "remote_address_zone"
                                    },
                                    "remote": {
                                        "name": "remote_address_zone"
                                    }
                                },
                                "permit_acceleration": False,
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "interface": "X1"
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv4(**obj)
        Assertion.assert_regular(json.dumps(resp), 'true', "err: not able to create policy")

    def test_02_delete_ipv4_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("testcase9")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")
