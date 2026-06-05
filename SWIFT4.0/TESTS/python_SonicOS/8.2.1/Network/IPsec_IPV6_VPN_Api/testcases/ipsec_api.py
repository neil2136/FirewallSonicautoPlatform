import sys
import os
import json
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPsec_IPV6_VPN_Api/')
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
            "value": "192.168.168.24"
        }
        resp = address_object.config_addressobject(**address_object2)
        resp1 = address_object.get_addressobject_by_name("remote_address_zone", "ipv4")
        Assertion.assert_regular(json.dumps(resp1), '"name": "remote_address_zone"',
                                 "Err: failed to create address object")

    def test_01_post_address_ip4_object(self):
        address_object2 = {
            "object_type": "host",
            "name": "object",
            "zone": "DMZ",
            "value": "1111:db8:2222:139::1"
        }
        resp = address_object.config_addressobject(**address_object2)
        resp1 = address_object.get_addressobject_by_name("object", "ipv6")
        Assertion.assert_regular(json.dumps(resp1), '"name": "object"', "Err: failed to create address object")

    def test1_create_local_cert(self):
        confPath = os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPsec_IPV6_VPN_Api/cert/'
        certPath = confPath + 'cert_local.pfx'
        cert_file = certificate.import_cert_local(cert_path="@" + certPath, name='local_cert_dpissl',
                                                  password='password')
        logger.info(cert_file)

class TC01_create_ipv6vpnpolicy_manual(Test):
    uuid = "SOSAIOT-TC-47594"
    description = show_testcase_info(Parameter.TESTPLAN, '1516109', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516109')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_ipv6vpnpolicy_manual(self):
        obj = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0"
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

class TC02_edit_ipv6vpnpolicy_manual(Test):
    uuid = "SOSAIOT-TC-47601"
    description = show_testcase_info(Parameter.TESTPLAN, '1516116', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516116')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ipv6vpnpolicy_manual(self):
        ipV6policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv4": {
                            "site_to_site": {
                                "name": "testcase1",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0"
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
                                            "name": "sslvpn_range1"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {},
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "in_spi": "0xadb169b9",
                                        "out_spi": "0xafecf046",
                                        "encryption_key": "",
                                        "authentication_key": "6e7ce00d48598dc0bf52279bddb8e41b5e805c70"
                                    }
                                },
                                "netbios": False,
                                "permit_acceleration": False,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "user_login": {
                                    "https": False
                                },
                                "default_lan_gateway": "0.0.0.0",
                                "bound_to": {
                                    "interface": "X1"
                                },
                                "suppress_auto_add_rule": False,
                                "apply_nat": True,
                                "translated_network": {
                                    "local": {
                                        "name": "sslvpn_range1"
                                    },
                                    "remote": {
                                        "name": "remote_address_zone"
                                    }
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv4("testcase1", **ipV6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

class TC03_Delete_ipv6_vpn_policy(Test):
    uuid = "SOSAIOT-TC-47606"
    description = show_testcase_info(Parameter.TESTPLAN, '1516121', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516121')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv4("testcase1")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC04_create_ipv6vpnpolicy_with_Local_IKE_ID(Test):
    uuid = "SOSAIOT-TC-47595"
    description = show_testcase_info(Parameter.TESTPLAN, '1516110', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_ipv6vpnpolicy_with_Local_IKE_ID(self):
        ipv6policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "testcase2",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "12345",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonnicwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "object"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-128",
                                        "authentication": "sha-1",
                                        "dh_group": "2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "anti_replay": True,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "local_ip": {
                                    "primary": True
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

class TC05_edit_ipv6policy_with_Local_IKE_ID(Test):
    uuid = "SOSAIOT-TC-47602"
    description = show_testcase_info(Parameter.TESTPLAN, '1516117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ipv6vpnpolicy_with_Local_IKE_ID(self):
        ipv6policy1={
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "shared_secret": {
                                        "ike_id": {
                                            "local": {
                                                "email_address": "automation@gmail.com"
                                            },
                                            "peer": {
                                                "email_address": "automation@gmail.com"
                                            }
                                        },
                                        "shared_secret": "12345"
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase2",
                                "network": {
                                    "local": {
                                        "name": "object"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv6("testcase2", **ipv6policy1)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase2")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC06_create_ipv6vpn_with_remote_ntw(Test):
    uuid = "SOSAIOT-TC-47596"
    description = show_testcase_info(Parameter.TESTPLAN, '1516111', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516111')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_ipv6vpnpolicy_with_remote_ntw(self):
        ipv6policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "testcase3",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "12345",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwallwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonnicwallwall.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "object"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-128",
                                        "authentication": "sha-1",
                                        "dh_group": "2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "anti_replay": True,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": "",
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "local_ip": {
                                    "primary": True
                                }
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

class TC07_edit_vpnpolicy_Distinguished_name(Test):
    uuid = "SOSAIOT-TC-47603"

    description = show_testcase_info(Parameter.TESTPLAN, '1516118', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516118')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_ipv6vpnpolicy_Distinguished_name(self):
        ipv6policy1 = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "certificate": {
                                        "certificate": "None",
                                        "ike_id": {
                                            "local": "distinguished-name",
                                            "peer": {
                                                "distinguished_name": "ou=gmail.com"
                                            }
                                        }
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase3",
                                "network": {
                                    "local": {
                                        "name": "object"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv6("testcase3", **ipv6policy1)
        Assertion.assert_regular(json.dumps(resp), "false", "err:not able to edit policy")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase3")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC08_create_ipv6vpnpolicy_remote_add_obj(Test):
    uuid = "SOSAIOT-TC-47597"
    description = show_testcase_info(Parameter.TESTPLAN, '1516112', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516112')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Create_Address_Group(self):
        ag_param = {
            "address_groups": [
                {
                    "ipv6": {
                        "address_object": {
                            "ipv6": [
                                {
                                    "name": "object"
                                }
                            ]
                        },
                        "name": "obj_addr_grp_ipv6"
                    }
                }
            ]
        }
        rc = address_object_group_api.add_addressgroup(**ag_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Failed To Add Address Group")
    def test_02_post_ipv6vpnpolicy_with_remote_address_obj(self):
        ipv6policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "shared_secret": {
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        },
                                        "shared_secret": "1234"
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase4",
                                "network": {
                                    "local": {
                                        "group": "obj_addr_grp_ipv6"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "group": "obj_addr_grp_ipv6"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

class TC09_edit_local_ntw_addr_obj(Test):
    uuid = "SOSAIOT-TC-47604"
    description = show_testcase_info(Parameter.TESTPLAN, '1516119', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516119')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def edit_01_local_ntw_addr_obj(self):
        ipv6policy1={
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "certificate": {
                                        "certificate": "local_cert_dpissl",
                                        "ike_id": {
                                            "local": "distinguished-name",
                                            "peer": {
                                                "distinguished_name": "ou=gmail.com"
                                            }
                                        }
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase4",
                                "network": {
                                    "local": {
                                        "name": "obj_addr_grp_ipv6"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "obj_addr_grp_ipv6"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv6("testcase4", **ipv6policy1)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase4")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC10_create_ipv6vpn_remote_range_addr_obj(Test):
    uuid = "SOSAIOT-TC-47598"
    description = show_testcase_info(Parameter.TESTPLAN, '1516113', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516113')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_address_ipv6_object(self):
        address_object2 = {
            "object_type": "range",
            "name": "object_ipv6",
            "zone": "DMZ",
            "value": "1111:db8:2222:139::1,1111:db8:2222:139::5"
        }
        resp = address_object.config_addressobject(**address_object2)
        resp1 = address_object.get_addressobject_by_name("object", "ipv6")
        Assertion.assert_regular(json.dumps(resp1), '"name": "object"', "Err: failed to create address object")

    def test_02_ipv6_remote_range_addr_obj(self):
        ipv6policy={
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "shared_secret": {
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "sonicwall.com"
                                            },
                                            "peer": {
                                                "domain_name": "sonicwall.com"
                                            }
                                        },
                                        "shared_secret": "1234"
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase5",
                                "network": {
                                    "local": {
                                        "name": "object_ipv6"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object_ipv6"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

    def test_03_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase5")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC11_create_ipv6vpn_Encrypt_DES_phase2(Test):
    uuid = "SOSAIOT-TC-47599"
    description = show_testcase_info(Parameter.TESTPLAN, '1516114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516114')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_ipv6vpn_DES_phase2(self):
        ipv6policy = {
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "testcase6",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "1234",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "s.com"
                                            },
                                            "peer": {
                                                "domain_name": "s.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "object_ipv6"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object_ipv6"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-256",
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "des": True
                                        },
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "anti_replay": True,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": ""
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

class TC12_edit_ipv6vpn_SHA1_phase2(Test):
    uuid = "SOSAIOT-TC-47605"
    description = show_testcase_info(Parameter.TESTPLAN, '1516120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ipv6vpn_SHA1_phase2(self):
        ipv6policy1={
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "name": "testcase6",
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "auth_method": {
                                    "shared_secret": {
                                        "shared_secret": "1234",
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "s.com"
                                            },
                                            "peer": {
                                                "domain_name": "s.com"
                                            }
                                        }
                                    }
                                },
                                "network": {
                                    "local": {
                                        "name": "object_ipv6"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object_ipv6"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "exchange": "ikev2",
                                        "encryption": "aes-256",
                                        "authentication": "sha-256",
                                        "dh_group": "2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "protocol": "esp",
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "perfect_forward_secrecy": {},
                                        "lifetime": 28800
                                    }
                                },
                                "anti_replay": True,
                                "management": {
                                    "https": False,
                                    "ssh": False,
                                    "snmp": False
                                },
                                "allow_sonicpointn_layer3": False,
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "suppress_trigger_packet": False,
                                "accept_hash": False,
                                "send_hash": ""
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.edit_site_to_site_ipv6("testcase6", **ipv6policy1)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to edit policy")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase6")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")

class TC13_create_ipv6vpn_DES_phase2(Test):
    uuid = "SOSAIOT-TC-47600"
    description = show_testcase_info(Parameter.TESTPLAN, '1516115', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516115')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_ipv6vpn_DES_phase2(self):
        ipv6policy ={
            "vpn": {
                "policy": [
                    {
                        "ipv6": {
                            "site_to_site": {
                                "accept_hash": False,
                                "anti_replay": True,
                                "auth_method": {
                                    "shared_secret": {
                                        "ike_id": {
                                            "local": {
                                                "domain_name": "s.com"
                                            },
                                            "peer": {
                                                "domain_name": "s.com"
                                            }
                                        },
                                        "shared_secret": "1234"
                                    }
                                },
                                "bound_to": {
                                    "zone": "WAN"
                                },
                                "enable": True,
                                "gateway": {
                                    "primary": "0:0:0:0:0:0:0:0",
                                    "secondary": "0:0:0:0:0:0:0:0"
                                },
                                "local_ip": {
                                    "primary": True
                                },
                                "management": {
                                    "https": False,
                                    "snmp": False,
                                    "ssh": False
                                },
                                "name": "testcase7",
                                "network": {
                                    "local": {
                                        "name": "object"
                                    },
                                    "remote": {
                                        "destination_network": {
                                            "name": "object"
                                        }
                                    }
                                },
                                "proposal": {
                                    "ike": {
                                        "authentication": "sha-1",
                                        "dh_group": "2",
                                        "encryption": "aes-256",
                                        "exchange": "ikev2",
                                        "lifetime": 28800
                                    },
                                    "ipsec": {
                                        "authentication": {
                                            "sha_1": True
                                        },
                                        "encryption": {
                                            "aes_128": True
                                        },
                                        "lifetime": 28800,
                                        "perfect_forward_secrecy": {},
                                        "protocol": "esp"
                                    }
                                },
                                "send_hash": "",
                                "suppress_trigger_packet": False
                            }
                        }
                    }
                ]
            }
        }
        resp = vpn_base.add_site_to_site_ipv6(**ipv6policy)
        Assertion.assert_regular(json.dumps(resp), "true", "err:not able to create policy")

    def test_02_delete_ipv6_vpn_policy(self):
        resp = vpn_base.delete_site_to_site_ipv6("testcase7")
        Assertion.assert_regular(json.dumps(resp), 'true', "err: :not able to delete policy")




