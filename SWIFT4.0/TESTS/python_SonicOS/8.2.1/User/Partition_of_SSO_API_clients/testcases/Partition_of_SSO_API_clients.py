from asyncio.log import logger
from definition.settings import *
import re


class Test_Partition_of_SSO_API_clients_01(Test):
    uuid = "SOSAIOT-TC-75176"
    
    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")
        
    def test_02_add_auth_partition(self):
        auth_partition1 = {
            "user": {
                "partitioning": {
                    "partition": [
                        {
                            "name": "test1",
                            "parent_partition": "",
                            "comment": "",
                            "domain": [{"name": "os-autosnwl.com"}
                                       ]
                        }
                    ]
                }
            }
        }
        res1 = user_auth_partition.add_auth_partition(**auth_partition1)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")


class Test_Partition_of_SSO_API_clients_02(Test):
    uuid = "SOSAIOT-TC-75177"
    
    def test_01_add_sso_clinet(self):
        sso_client_add = {
            "host": "192.168.168.201",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "low": True
            },
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.create_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"host": "192.168.168.201"', "Err:Failed to add SSO API value")

    def test_02_delete_sso_clinet(self):
        config_sso = sso_client.delete_sso_third_party_client('192.168.168.201')
        Assertion.assert_not_regular(json.dumps(config_sso), '"host": "192.168.168.201"', "Err:Failed to delete SSO API value")
                                     
class Test_Partition_of_SSO_API_clients_03(Test):
    uuid = "SOSAIOT-TC-75178"
    
    def test_01_add_split_DNS(self):
        split_dns_dict = {
            'domain': '*.os-autoswnl.com',
            'ipv4': {
                'primary': '8.8.8.8',
            },
            'local_interface': 'X1',
        }
        rc = split_dns_api.add_split_dns(**split_dns_dict)
        Assertion.assert_equal(rc, True, "ERR: add split DNS entry failed.")

    def test_02_add_sso_clinet(self):
        sso_client_add = {
            "host": "os-autoswnl.com",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "low": True
            },
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.create_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"host": "os-autoswnl.com"', "Err:Failed to add SSO API value")

    def test_03_delete_split_DNS(self):
        rc = split_dns_api.delete_split_dns(domain='*.os-autoswnl.com')
        Assertion.assert_equal(rc, True, "ERR: delete split DNS entry failed.")

class Test_Partition_of_SSO_API_clients_04(Test):
    uuid = "SOSAIOT-TC-75179"
   
    def test_01_edit_sso_clinet(self):
        sso_client_add = {
            "host": "os-autoswnl.com",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "high": "allow-all"
            },
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.edit_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"high": "allow-all"', "Err:Failed to edit SSO API value")

class Test_Partition_of_SSO_API_clients_05(Test):
    uuid = "SOSAIOT-TC-75180"
   
    def test_01_edit_auth_partition(self):
        auth_partition = {
        "user": {
            "partitioning": {
            "partition": [
                {
                "name": "test1",
                "parent_partition": "",
                "comment": "",
                "domain": [
                    
                ]
                }
            ]
            }
        }
        }
        res1 = user_auth_partition.edit_auth_partition(name="test1", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")

class Test_Partition_of_SSO_API_clients_06(Test):
    uuid = "SOSAIOT-TC-75181"
   
    def test_01_show_auth_partition(self):
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "test1"', "ERR: Failed to add partition")


class Test_Partition_of_SSO_API_clients_07(Test):
    uuid = "SOSAIOT-TC-75182"
   
    def test_01_edit_auth_partition(self):
        auth_partition = {
        "user": {
            "partitioning": {
            "partition": [
                {
                "name": "test2",
                "parent_partition": "",
                "comment": "",
                "domain": [
                    
                ]
                }
            ]
            }
        }
        }
        res1 = user_auth_partition.add_auth_partition(name="test2", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
    
    def test_02_edit_auth_sub_partition(self):
        auth_partition = {
        "user": {
        "partitioning": {
            "partition": [
            {
                "name": "subpart_test1",
                "parent_partition": "test2",
                "comment": "",
                "domain": [
                {
                    "name": "os-autosnwlpart2.com"
                }
                ]
            }
            ]
        }
        }
        }
        res1 = user_auth_partition.add_auth_partition(name="subpart_test1", **auth_partition)
        Assertion.assert_equal(res1, True, "ERR: Failed to add partition")
        resp = user_auth_partition.show_auth_partitions()
        Assertion.assert_regular(json.dumps(resp), '"name": "os-autosnwlpart2.com"', "ERR: Failed to add partition")

class Test_Partition_of_SSO_API_clients_08(Test):
    uuid = "SOSAIOT-TC-75183"
    
    def test_01_enable_auth_partition(self):
        ldap_user = user_auth_partition.enable_disable_auth_partition(enable=True)
        Assertion.assert_equal(ldap_user, True, "ERR: Failed to add LDAP")

