import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups')

from definition.settings import *
from definition.conf_fw import *

class config_ldap(Test):
    uuid = 'NonTC'

    def test_01_config_ldap(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")

    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

class TC01_ldap_mirrored_group(Test):
  # Mirrored group match a user-created local group
    uuid = "SOSAIOT-TC-77163"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516143', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516143')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
    
    def test_02_ldap_settings(self):
        add_ldap_setting ={ 
            "user": {
                "ldap": {
                    
                    "protocol_version": 3,
                    "require_valid_certificate": True,
                    "local_tls_certificate": "",
                    "allow_referrals": True,
                    "allow_references": {
                        "user_authentication": False,
                        "auto_configuration": True,
                        "domain_search": True,
                        "other_search": True
                    },
                    "local_users_only": False,
                    "default_user_group": "",
                    "check_deleted_groups_method": {   
                        "read_from_servers": True
                    },
                    "mirror_user_groups": {},
                    "relay": {
                        "enable": False,
                        "clients_connect": {
                            "trusted_zones": False,
                            "wan_zone": True,
                            "public_zones": False,
                            "wireless_zones": False,
                            "vpn_zone": True
                        },
                        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
                        "legacy_user_group": { 
                            "vpn": "",
                            "vpn_client": "",
                            "l2tp": "",
                            "internet": ""
                         }
                    }
                 }
              }
            }
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {}',"failed to configure")
        time.sleep(60)

    def test_03_create_local_group(self):
        local_group={           
            "user": {
                "local": {        
                    "group": [
                        {                           
                            "name": "group1",
                            "domain": "os-autosnwl.com"
                        }
                     ]
                }
            }
        }
        local_group = user.add_local_group(**local_group)
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "group1"', "failed to get mirrored groups")
        
    def test_04_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_05_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_06_get_local_group(self):
        resp = user.show_local_groups()
        res=str(resp).replace(r"\\"," ")
        Assertion.assert_regular(json.dumps(resp), '"name": "group1", "domain": "os-autosnwl.com"', "failed to get local groups")
        Assertion.assert_regular(str(res), "'display_name': 'OS-AUTOSNWL group1'", "failed to get local groups")
        Assertion.assert_regular(json.dumps(resp), '"memberships_by_ldap_location"', "Falied to get local group domain")
    
    def test_07_delete_mirrored_group(self):
        resp = user.delete_local_group_with_domain('group1','os-autosnwl.com')
        time.sleep(5)
        out = user.show_local_groups()
        res=str(out).replace(r"\\"," ")
        Assertion.assert_not_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL group1'", "failed to get mirrored groups")             

class TC02_ldap_mirrored_group(Test):
  # Mirrored group match a user-created local group
    uuid = "SOSAIOT-TC-77165"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516145', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516145')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
    
    def test_02_ldap_settings(self):
        add_ldap_setting ={ 
            "user": {
                "ldap": {
                    
                    "protocol_version": 3,
                    "require_valid_certificate": True,
                    "local_tls_certificate": "",
                    "allow_referrals": True,
                    "allow_references": {
                        "user_authentication": False,
                        "auto_configuration": True,
                        "domain_search": True,
                        "other_search": True
                    },
                    "local_users_only": False,
                    "default_user_group": "",
                    "check_deleted_groups_method": {   
                        "read_from_servers": True
                    },
                    "mirror_user_groups": {},
                    "relay": {
                        "enable": False,
                        "clients_connect": {
                            "trusted_zones": False,
                            "wan_zone": True,
                            "public_zones": False,
                            "wireless_zones": False,
                            "vpn_zone": True
                        },
                        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
                        "legacy_user_group": { 
                            "vpn": "",
                            "vpn_client": "",
                            "l2tp": "",
                            "internet": ""
                         }
                    }
                 }
              }
            }
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {}',"failed to configure")
        time.sleep(60)

    def test_03_create_local_group(self):
        local_group={           
            "user": {
                "local": {        
                    "group": [
                        {                           
                            "name": "group1",
                            "domain": "os-autosnwl.com"
                        }
                     ]
                }
            }
        }
        local_group = user.add_local_group(**local_group)
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "group1"', "failed to get mirrored groups")
        
    def test_04_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_05_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_06_get_local_group(self):
        resp = user.show_local_groups()
        res=str(resp).replace(r"\\"," ")
        Assertion.assert_regular(json.dumps(resp), '"name": "group1", "domain": "os-autosnwl.com"', "failed to get local groups")
        Assertion.assert_regular(str(res), "'display_name': 'OS-AUTOSNWL group1'", "failed to get local groups")
        Assertion.assert_regular(json.dumps(resp), '"memberships_by_ldap_location"', "Falied to get local group domain")
    
    def test_07_delete_mirrored_group(self):
        resp = user.delete_local_group_with_domain('group1','os-autosnwl.com')
        time.sleep(5)
        out = user.show_local_groups()
        res=str(out).replace(r"\\"," ")
        Assertion.assert_not_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL group1'", "failed to get mirrored groups")   

class TC03_ldap_mirrored_group(Test):
  # Enable Mirror LDAP groups locally in Users&Groups tab
    
    uuid = "SOSAIOT-TC-77142"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516122', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516122')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

class TC04_ldap_mirrored_group(Test):
    # Same group name in different domain
    uuid = "SOSAIOT-TC-77143"
    

    description = show_testcase_info(Parameter.TESTPLAN, '1516123', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516123')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")
    
    def test_02_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")

    def test_03_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), "'users_tree': [{'name': 'os-autosnwl.com/Users'}]", "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), "'user_groups_tree': [{'name': 'os-autosnwl.com/Users'}]", "failed to config bind")  

    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

class TC05_ldap_mirrored_group(Test):
  # Disable Mirror LDAP groups locally in Users&Groups tab
    uuid = "SOSAIOT-TC-77153"
    description = show_testcase_info(Parameter.TESTPLAN, '1516133', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")
    
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
  
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

    def test_05_login_ui(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups/lib/ui_login.py ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)

    def test_06_get_ldap_settings(self):
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {}',"failed to configure")
      
class TC06_ldap_mirrored_group(Test):
  #  Disable LDAP or just Disable Mirror LDAP function, Mirrored group will be added to local groups and can be deleted and edited
    uuid = "SOSAIOT-TC-77161"
    description = show_testcase_info(Parameter.TESTPLAN, '1516141', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516141')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        res=str(resp).replace(r"\\"," ")
        Assertion.assert_regular(json.dumps(res), "'comment': 'Mirrored from LDAP'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'domain': 'os-autosnwl.com'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL Domain Admins'", "failed to get mirrored groups")
    
    def test_05_login_ui(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups/lib/ui_ldap.py ' + '-url ' + url + ' -user admin -pwd '+ G_PASSWORD_NEW +''
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)

    def test_06_mirrored_group(self):
        resp = user.show_local_groups()
        res=str(resp).replace(r"\\"," ")
        Assertion.assert_regular(json.dumps(res), "'comment': 'Mirrored from LDAP'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'domain': 'os-autosnwl.com'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL Domain Admins'", "failed to get mirrored groups")

    def test_07_mirrored_group(self):

        local_group ={
            "user": {   
                "local": {
                    "group": [
                        {
                            "name": "Domain Admins",
                            "comment": "",
                            "domain": "os-autosnwl.com",
                            "member": [
                                {
                                  "name": "All LDAP Users"
                                }
                            ]
                        }
                    ]
                }
            }
        } 
        resp = user.config_local_group_by_name('Domain Admins','os-autosnwl.com',**local_group)
        Assertion.assert_equal(resp, True, "ERR: failed to edit local group")
        out = user.show_local_group_by_domain_name('Domain Admins','os-autosnwl.com')
        res=str(out).replace(r"\\"," ")
        Assertion.assert_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL Domain Admins'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'domain': 'os-autosnwl.com'", "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(res), "'name': 'All LDAP Users'", "failed to get mirrored groups")

    def test_08_mirrored_group(self):
        resp = user.delete_local_group_with_domain('Domain Admins','os-autosnwl.com')
        time.sleep(5)
        out = user.show_local_groups()
        res=str(out).replace(r"\\"," ")
        Assertion.assert_not_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL Domain Admins'", "failed to get mirrored groups")

class TC07_ldap_mirrored_group(Test):
    uuid = "SOSAIOT-TC-77166"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516146', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516146')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
    

        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Computers"', "failed to get mirrored groups")
    
    def test_05_restart_fw(self):
        out=reboot_sys.restart_now()
        time.sleep(60)

    def test_06_test_ldap_server(self):
        ldap_test = {
  "user": {
    "ldap": {
      "test": {
        "name": "192.168.168.85",
        "type": {
          "connectivity_bind": True
        }
      }
    }
  }
}
        resp = ldap.test_ldap_server(**ldap_test)
        Assertion.assert_equal(resp, True,"failed to configure")

    def test_07_mirrored_group(self):
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")

        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

class TC08_ldap_mirrored_group(Test):
    # Mirror  Only groups that have member users or groups
    uuid = "SOSAIOT-TC-77174"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516155', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516155')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "have_members": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"have_members": true',"failed to configure")

    @repeat_method(5)    
    def test_04_refresh_from_ldap(self):
      resp = ldap.refresh_from_ldap()
      Assertion.assert_equal(resp, True,"failed to refresh")
       
    @repeat_method(7)
    def test_05_mirrored_group(self):
      resp = ldap.refresh_from_ldap()
      Assertion.assert_equal(resp, True,"failed to refresh")
      time.sleep(10)
      resp = user.show_local_groups()
      Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")
      Assertion.assert_not_regular(json.dumps(resp), '"name": "Protected Users"', "failed to get mirrored groups")

class TC09_ldap_mirrored_group(Test):
    # Mirrored LDAP groups cannot be deleted
    uuid = "SOSAIOT-TC-77176"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516157', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516157')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

    @repeat_method(7)
    def test_05_mirrored_group(self):
        resp = user.delete_local_group_with_domain('Domain Admins','os-autosnwl.com')
        Assertion.assert_regular(json.dumps(resp), 'false', "able to delete mirrored groups")
        time.sleep(5)
        out = user.show_local_groups()
        Assertion.assert_regular(json.dumps(out), '"name": "Domain Admins"', "able to delete mirrored groups")

class TC10_ldap_mirrored_group(Test):
    # Reboot with Mirror LDAP groups locally in Users&Groups tab
    uuid = "SOSAIOT-TC-77173"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516154', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516154')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

    def test_05_restart_fw(self):
        out=reboot_sys.restart_now()
        time.sleep(60)

    def test_06_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

    def test_07_add_user(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['All LDAP Users']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_user_by_name('All LDAP Users')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SonicWALL Administrators"',
                                 'err: ldap users not added to sonicwall administrators')

    def test_08_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true',
                                 'err: enable to_management_on_login failed.')

    def test_09_add_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        rule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "SonicWALL Administrators"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"',
                                 'err: access rules not updated.')

    def test_10_login(self):
        localhost.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_Mirrorred_groups/lib/ui_user.py ' + \
              '-url ' + url + ' -user test -pwd password'
        out = localhost.send_command(cmd)
        logger.info("login with user\n" + out)

        status = user_status.show_user_status_by_name('test')
        Assertion.assert_regular(json.dumps(status), '"name": "test"', "failed to get user status")
       

    # logout user
    def test_11_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC11_ldap_mirrored_group(Test):
    # TSR support
    uuid = "SOSAIOT-TC-77169"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516149', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516149')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',"ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
      resp = user.show_local_groups()
      Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")    
       
    def test_05_download_tsr(self):
      resp = diagnostic.download_tsr()
      file_path = '/tmp/techSupport'
      search_line = 'OS-AUTOSNWL\DnsAdmins (DnsAdmins@os-autosnwl.com): (mirrored from LDAP)'        
      with open(file_path) as f:
          if search_line in f.read():
              res = True
          else:
              res = False
      Assertion.assert_equal(res, True, "failed to get mirrored groups")

class TC12_ldap_mirrored_group(Test):
  # Enable Mirror LDAP groups locally in Users&Groups tab
    
    uuid = "SOSAIOT-TC-77164"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516144', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516144')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap-local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap-local"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
        Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

class TC13_ldap_mirrored_group(Test):
    # export/import preference
    uuid = "SOSAIOT-TC-77167"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516147', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516147')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_02_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/Users'],
                'user_groups_tree': ['os-autosnwl.com/Users'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_03_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")
        
    def test_04_mirrored_group(self):
      resp = user.show_local_groups()
      Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

    def test_05_export_exp(self):
      resp = setting.export_setting_exp()
      Assertion.assert_equal(resp, True, "failed to export the configuration")

    def test_06_restart_fw(self):
      response = setting.boot_fw(mode=2)
      Assertion.assert_equal(response, True, "failed to do factory default")
      time.sleep(120)
    
    def test_07_import_exp(self):
      out = setting.import_setting_exp('/tmp/test.exp')
      Assertion.assert_equal(out, True, "failed to import the configuration")
      time.sleep(120)

    def test_08_mirrored_group_settings(self):
      resp = ldap.show_ldap_setting()
      Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")

      resp = user.show_local_groups()
      Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"name": "Domain Admins"', "failed to get mirrored groups")

class TC14_ldap_mirrored_group(Test):
    #  Exclude groups in these sub-trees can be showed in Mirror groups
    uuid = "SOSAIOT-TC-77172"
    
    description = show_testcase_info(Parameter.TESTPLAN, '1516153', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516153')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_delete_mirrored_group(self):
        output = user.show_local_groups()
        search_line = "'name': 'Groups1'"

        if search_line in json.dumps(output):
            resp = user.delete_local_group_with_domain('Groups1','os-autosnwl.com')
            time.sleep(5)
            out = user.show_local_groups()
            res=str(out).replace(r"\\"," ")
            Assertion.assert_not_regular(json.dumps(res), "'display_name': 'OS-AUTOSNWL Groups1'", "failed to get mirrored groups")        

    def test_02_config_authentication(self):
        user_auth = {
            "auth_method": "ldap",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }

        ldap_auth = user_settings.user_method_authentication(**user_auth)
        resp = user_settings.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "ldap"',
                                 "ERR:LDAP method is not selected successfully")
        
    def test_03_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Users', 'os-autosnwl.com/User'],
                'user_groups_tree': ['os-autosnwl.com/User'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }

            ldap_user = ldap.add_ldap_server(**add_ldap_server)
            resp = ldap.show_ldap_servers()
            Assertion.assert_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to config ldap server")

            Assertion.assert_regular(json.dumps(resp), '"bind": {"acct": {"name": "test"', "failed to config bind")

    def test_04_config_ldapuser(self):
        resp = ldap.show_ldap_server_by_name('192.168.168.85')
        ldap_server = {
                'role': 'primary',
                'host': '192.168.168.85',
                'enable': True,
                'port_num': 389,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 5,
                'overalloperationtimeout': 4,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'os-autosnwl.com',
                'users_tree': ['Groups', 'os-autosnwl.com/Groups'],
                'user_groups_tree': ['os-autosnwl.com/Groups'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }
        ldap_user = ldap.edit_ldap_server(**ldap_server)
        Assertion.assert_equal(ldap_user, True, "ERR: edit ldapuser failed")
        resp = ldap.show_ldap_servers()
        res=str(resp).replace(r"/"," ")
        Assertion.assert_regular(json.dumps(res), "'name': 'Groups'", "failed to config ldap server") 
        Assertion.assert_regular(json.dumps(res), "'name': 'os-autosnwl.com Groups'", "failed to config ldap server") 

    def test_05_ldap_settings(self):
        add_ldap_setting = {
  "user": {
    "ldap": {
      "protocol_version": 3,
      "require_valid_certificate": True,
      "local_tls_certificate": "",
      "allow_referrals": True,
      "allow_references": {
        "user_authentication": False,
        "auto_configuration": True,
        "domain_search": True,
        "other_search": True
      },
      "local_users_only": False,
      "default_user_group": "",
      "check_deleted_groups_method": {
        "read_from_servers": True
      },
      "mirror_user_groups": {
        "refresh": {
          "period": 5
        },
        "all": True
      },
      "relay": {
        "enable": False,
        "clients_connect": {
          "trusted_zones": False,
          "wan_zone": True,
          "public_zones": False,
          "wireless_zones": False,
          "vpn_zone": True
        },
        "shared_secret": "6,130dc051d6f1cae4f30bc65a8b7eebf34cfdf9784374ac46c6bc4e915a8fca6caf4ddf952d1ef9df014c8827703ca0a6f4d04a9c1533f4fc0255ad414301718a",
        "legacy_user_group": {
          "vpn": "",
          "vpn_client": "",
          "l2tp": "",
          "internet": ""
        }
      }
    }
  }
}
        ldap_user = ldap.config_ldap_setting(**add_ldap_setting)
        resp = ldap.show_ldap_setting()
        Assertion.assert_regular(json.dumps(resp), '"mirror_user_groups": {"all": true',"failed to configure")

    def test_06_exclude_group_subtree(self):
      sub_tree = {
          "user": {
              "ldap": {                 
                  "exclude_tree": [    
                      {
                          "subTree": "os-autosnwl.com/Groups"
                      }
                  ]
               }
          }
      }
      resp = ldap.exclude_sub_trees(**sub_tree)
      Assertion.assert_equal(resp, True, "failed to to exclude groups")
      time.sleep(300)
      res = ldap.refresh_from_ldap()
      Assertion.assert_equal(res, True, "failed to to exclude groups")
      time.sleep(60)

    def test_07_mirrored_group(self):
      resp = user.show_local_groups()
      Assertion.assert_not_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_not_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_not_regular(json.dumps(resp), '"name": "Groups1"', "failed to get mirrored groups")
    
    def test_08_delete_exclude_group_subtree(self):
      subtree = {
          "user": {
              "ldap": {                 
                  "exclude_tree": [    
                      {
                          "subTree": "os-autosnwl.com/Groups"
                      }
                  ]
               }
          }
      }
      resp = ldap.delete_exclude_sub_trees(**subtree)
      Assertion.assert_equal(resp, True, "failed to to exclude groups")

    def test_09_exclude_group_subtree(self):
      sub_tree_1 = {
          "user": {
              "ldap": {                 
                  "exclude_tree": [    
                      {
                          "subTree": "os-autosnwl.com/Groups/Groups1"
                      }
                  ]
               }
          }
      }
      resp = ldap.exclude_sub_trees(**sub_tree_1)
      Assertion.assert_equal(resp, True, "failed to to exclude groups")
      time.sleep(60)
      res = ldap.refresh_from_ldap()
      Assertion.assert_equal(res, True, "failed to to exclude groups")
      time.sleep(60)

    def test_10_mirrored_group(self):
      resp = user.show_local_groups()
      Assertion.assert_regular(json.dumps(resp), '"comment": "Mirrored from LDAP"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"domain": "os-autosnwl.com"', "failed to get mirrored groups")
      Assertion.assert_regular(json.dumps(resp), '"name": "Groups1"', "failed to get mirrored groups")

    def test_11_delete_exclude_group_subtree(self):
      sub_tree_2 = {
          "user": {
              "ldap": {                 
                  "exclude_tree": [    
                      {
                          "subTree": "os-autosnwl.com/Groups/Groups1"
                      }
                  ]
               }
          }
      }
      resp = ldap.delete_exclude_sub_trees(**sub_tree_2)
      Assertion.assert_equal(resp, True, "failed to to exclude groups")

class delete_ldap(Test):
    uuid = 'NonTC'

    def test_01_delete_ldap(self):
        ldap_user = ldap.del_ldap_server('192.168.168.85')
        resp = ldap.show_ldap_servers()
        Assertion.assert_not_regular(json.dumps(resp), '"host": "192.168.168.85"', "failed to delete ldap server")

    












    


 