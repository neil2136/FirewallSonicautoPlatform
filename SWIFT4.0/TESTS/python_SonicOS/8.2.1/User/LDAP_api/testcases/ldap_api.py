import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/LDAP_api')

from definition.settings import *

class TC01_LDAP(Test):
    uuid = "SOSAIOT-TC-47822"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_put_User_LDAP_settings(self):
        LDAP_settings = {
            'version': 3,
            'require_valid_certificate': True,
            'local_tls_certificate': {},
            'user_authentication': True,
            'auto_configuration': False,
            'domain_search': False,
            'other_search': False,
            'local_users_only': True,
            'group_name': 'Trusted Users',
            'mirror_user_groups': {
                "all":True,
                #"have_members":True
            },
            "refresh": {
                "period": 6
            },
            #'minutes': 6,
            'enableradiustoldaprelay': True,
            'public_zones': True,
            'trusted_zones': True,
            'wan_zone': True,
            'wireless_zones': True,
            'vpn_zone': True,
            'RADIUSsharedsecret': 'password',
            'vpn': 'LegacyVPNUsers',
            'vpn_client': 'LegacyVPNClients',
            'l2tp': 'LegacyL2TPUsers',
            'internet': 'LegacyInternetAccess'
         
         }
        response = LDAP_user.ldap_setting(**LDAP_settings)
        logger.info(response) 
        response_get = LDAP_user.show_ldap_setting()                                                                
        Assertion.assert_regular(json.dumps(response_get), '"protocol_version": 3,','Failed to edit LDAP settings') 

class TC03_LDAP(Test):
    uuid = "SOSAIOT-TC-47823"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_post_LDAP_server_settings(self):
        add_ldap_server = {
                'role': 'primary',
                'host': '10.10.10.10',
                'enable': True,
                'port_num': 636,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 10,
                'overalloperationtimeout': 6,
                'send_start_tls_request': True,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'other-servers',
                'primary_domain': 'testdomain1.com',
                'users_tree': ['test', 'testdomain1.com/users'],
                'user_groups_tree': ['testdomain1.com/groups'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service'
            }
    
        response = LDAP_user.add_ldap_server(**add_ldap_server)
        logger.info(response)
        response_get = LDAP_user.show_ldap_servers()
        Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.10"', "failed to add ldap server")

class TC07_LDAP(Test):
    uuid = "SOSAIOT-TC-47826"
    description = show_testcase_info(Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    
    def test_get_ldap_servers(self):
        
        response_get = LDAP_user.show_ldap_servers()
        logger.info(response_get)
        Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.10"', "failed to get ldap server")
           
class TC05_LDAP(Test):
    uuid = "SOSAIOT-TC-47824"
    description = show_testcase_info(Parameter.TESTPLAN, '05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_post_LDAP_server_settings(self):
        response = LDAP_user.show_ldap_server_by_name('10.10.10.10') 
        edit_ldap_server = {
                'role': 'primary',
                'host': '10.10.10.10',
                'enable': True,
                'port_num': 6365,
                'use_tls': True,
                'timeout': True,
                'servertimeout': 20,
                'overalloperationtimeout': 10,
            }
    
        response = LDAP_user.edit_ldap_server(**edit_ldap_server)
        logger.info(response)
        response_get = LDAP_user.show_ldap_server_by_name('10.10.10.10')
        Assertion.assert_regular(json.dumps(response_get), '"use_tls": true', "failed to edit ldap server")
    
class TC06_LDAP(Test):
    uuid = "SOSAIOT-TC-47825"
    description = show_testcase_info(Parameter.TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_post_LDAP_server1(self):
        add_ldap_server1 = {
                'role': 'primary',
                'host': '10.10.10.11',
                'enable': True,
                'port_num': 636,
                'use_tls': True,
                'timeout': True,
                'servertimeout': 10,
                'overalloperationtimeout': 5,
                'send_start_tls_request': False,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_1',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'local',
                'primary_domain': 'mydomain.com',
                'users_tree': ['test', 'mydomain.com/users'],
                'user_groups_tree': ['mydomain.com/groups'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service',
            }
        response = LDAP_user.add_ldap_server(**add_ldap_server1)
        logger.info(response)
        response_get = LDAP_user.show_ldap_servers()
        Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.11"', "failed to add ldap server")
    
    def test_post_LDAP_server2(self):
        add_ldap_server2 = {  
                'role': 'secondary',
                'host': '10.10.10.12',
                'enable': True,
                'port_num': 636,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 8,
                'overalloperationtimeout': 5,
                'send_start_tls_request': False,
                'bind': 'distinguished_name',
                'distinguished_name': 'ldap_auto_2',
                'bind_password': 'S0nic@uto',
                'referred_bind_with_account': 'local',
                'primary_domain': 'testdomain.com',
                'users_tree': ['test1', 'testdomain.com/users'],
                'user_groups_tree': ['testdomain.com/groups'],
                'directory': True,
                'schema': 'microsoft-active-directory/network-information-service',
            }   
        response = LDAP_user.add_ldap_server(**add_ldap_server2)
        logger.info(response)
        response_get = LDAP_user.show_ldap_servers()
        Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.12"', "failed to add ldap server")
    
class TC15_LDAP(Test):
    uuid = "SOSAIOT-TC-47827"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_put_nonexistent_LDAP_server(self): 
        response = LDAP_user.show_ldap_server_by_name('10.10.10.14') 
        edit_nonexistent_server = {  
                'role': 'secondary',
                'host': '10.10.10.14',
                'enable': True,
                'port_num': 636,
                'use_tls': True
            }        
        response = LDAP_user.edit_ldap_server(**edit_nonexistent_server)
        logger.info(response)
        response_get = LDAP_user.show_ldap_server_by_name('10.10.10.14')
        Assertion.assert_not_regular(json.dumps(response_get), 'show user ldap server 10.10.10.14 does not match"', "failed to edit ldap server")
            
        
class TC08_LDAP(Test):
    uuid = "SOSAIOT-TC-47825"
    description = show_testcase_info(Parameter.TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_put_LDAP_server1(self):
        edit_ldap_servers = {
                'role': 'primary',
                'host': '10.10.10.11',
                'enable': True,
                'port_num': 636,
                'use_tls': False,
                'timeout': True,
                'servertimeout': 15,
                'overalloperationtimeout': 7,
            }
        response = LDAP_user.edit_ldap_server(**edit_ldap_servers)
        logger.info(response)
        response_get = LDAP_user.show_ldap_servers()
        Assertion.assert_regular(json.dumps(response_get), '"use_tls": false', "failed to edit ldap server")
            
    def test_put_LDAP_server2(self):
        edit_ldap_servers = {
                'role': 'primary',
                'host': '10.10.10.12',
                'enable': True,
                'port_num': 636,
                'use_tls': True,
                'timeout': True,
                'servertimeout': 10,
                'overalloperationtimeout': 7,
            }
        response = LDAP_user.edit_ldap_server(**edit_ldap_servers)
        logger.info(response)
        response_get = LDAP_user.show_ldap_servers()
        Assertion.assert_regular(json.dumps(response_get), '"timeout": {"server": 10, "operation": 7}', "failed to edit ldap server")

class TC09_LDAP(Test):
    uuid = "SOSAIOT-TC-47828"
    description = show_testcase_info(Parameter.TESTPLAN, '1825024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_GET_User_LDAP_settings(self):
        response_get = LDAP_user.show_ldap_setting()
        Assertion.assert_regular(json.dumps(response_get), '"protocol_version": 3,','Failed to get LDAP settings')

class TC10_LDAP(Test):
    uuid = "SOSAIOT-TC-47829"
    description = show_testcase_info(Parameter.TESTPLAN, '1825025', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825025')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_GET_User_LDAP_server_using_name(self):
        response_get = LDAP_user.show_ldap_server_by_name('10.10.10.10')
        Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.10",', "Failed to get ldap server")

class TC11_LDAP(Test):
    uuid = "SOSAIOT-TC-47830"
    description = show_testcase_info(Parameter.TESTPLAN, '1825026', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825026')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap(self):
        resp = LDAP_user.del_ldap_server("10.10.10.10")
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

class TC12_LDAP(Test):
    uuid = "SOSAIOT-TC-47831"
    description = show_testcase_info(Parameter.TESTPLAN, '1825027', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825027')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_get_ldap_reporting_statistics(self):
        resp = LDAP_user.show_ldap_reporting_statistic()
        Assertion.assert_regular(json.dumps(resp), '"user_auth_failures": 0', "Failed to get ldap server")

class TC13_LDAP(Test):
    uuid = "SOSAIOT-TC-47832"
    description = show_testcase_info(Parameter.TESTPLAN, '1825028', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825028')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap_reporting_statistics(self):
        resp = LDAP_user.del_ldap_reporting_statistic()
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

class TC14_LDAP(Test):
    uuid = "SOSAIOT-TC-47833"
    description = show_testcase_info(Parameter.TESTPLAN, '1825029', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825029')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap_reporting_statistics(self):
        resp = LDAP_user.show_ldap_server_reporting_statistic('name/10.10.10.12')
        Assertion.assert_not_regular(json.dumps(resp), '"status": "init"', "Failed to get ldap server")

class TC16_LDAP(Test):
    uuid = "SOSAIOT-TC-47834"
    description = show_testcase_info(Parameter.TESTPLAN, '1825030', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825030')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ldap_reporting_statistics(self):
        resp = LDAP_user.del_ldap_server_reporting_statistic('name/10.10.10.12')
        Assertion.assert_equal(resp, True, "ERR: Failed to delete LDAP")

class TC17_LDAP(Test):
    uuid = "SOSAIOT-TC-47835"
    description = show_testcase_info(Parameter.TESTPLAN, '1825032', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825032')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_GET_User_LDAP_server_using_name(self):
        response_get = LDAP_user.show_ldap_server_by_name('fake')
        Assertion.assert_regular(json.dumps(response_get), '"command": "show user ldap server fake"', "Failed to get ldap server")

class TC18_LDAP(Test):
    uuid = "SOSAIOT-TC-47836"
    description = show_testcase_info(Parameter.TESTPLAN, '1825033', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_LDAP_with_wrong_server_name(self):
        resp = LDAP_user.del_ldap_server('fake')
        Assertion.assert_equal(resp, False, "ERR: Failed to delete LDAP")