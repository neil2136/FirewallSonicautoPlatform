import sys
import os
import json

import paramiko


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Radius_client_accounting')
from definition.settings import *

class Radius_configs(Test):
    uuid = "NonTC"

    def test_01_enable_radius_user_auth_method(self):
        logger.info("-------Radius Auth---------")
        user_auth = {
                "auth_method": "radius-local",
                "sso_agent": False,
                "terminal_services_agent": False,
                "radius_accounting": False,
                "third_party_api": False,
                "capture_client": False
            }
        user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "radius-local"', "ERR:Failed to select Local authentication method.")
    
    @repeat_method(4)
    def test_02_edit_access_rule(self):
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            uuid = rules['ipv4']['uuid']
            name = rules['ipv4']['name']
        accessrule = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **accessrule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "Everyone"', 'ERR: Failed to modify access rule')


class TC01_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75641"
    description = show_testcase_info(Parameter.TESTPLAN, '1527411', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527411')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_verify_radius_and_user_accounting_tab(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.navigate_to_radius_accounting_tab()
        out = uiobj.verify_radius_and_user_accounting_tab()
        Assertion.assert_equal(out, True, "ERR: testcase failed")


class TC02_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75644"
    description = show_testcase_info(Parameter.TESTPLAN, '1527414', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527414')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        logger.info("-------Radius Config---------")
        add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1814,
                'secret': 'password',
                'send_through_vpn_tunnel': True
            }

        response = Radius_user.add_radius_account(**add_radius_user)
        logger.info(response)
        response_get = Radius_user.show_radius_account()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_edit_radius_account(self):
        add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }

        response = Radius_user.edit_radius_account(**add_radius_user)
        logger.info(response)
        response_get = Radius_user.show_radius_account()
        Assertion.assert_regular(json.dumps(response_get), '"port": 1813','err: Failed to add radius server')


class TC03_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75642"
    description = show_testcase_info(Parameter.TESTPLAN, '1527412', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527412')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_edit_user_account_setting(self):
        user_obj = {
            "user": {
                "radius": {
                    "accounting": {
                        "include": "domain-and-local-users",
                        "data": {
                            "users_authenticated_by_web_login": True
                        }
                    }
                }
            }
        }
        resp = Radius_user.edit_user_radius_accounting(**user_obj)
        Assertion.assert_equal(resp, True, "ERR: edit user account setting failed")
        res = Radius_user.get_user_radius_accounting()
        Assertion.assert_regular(json.dumps(res), '"include": "domain-and-local-users"','err: edit user account setting failed')
        Assertion.assert_regular(json.dumps(res), '"users_authenticated_by_web_login": true','err: edit user account setting failed')

    def test_03_download_tsr(self):
        resp = diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Name / IP address:                     192.168.168.85'   
        search_line1 = 'Web users:                             yes'  
        search_line2 = 'Include domain users:                    yes'    
        search_line3 = 'Include local users:                     yes'   
        with open(file_path) as f:
            if search_line and search_line1 and search_line2 and  search_line3 in f.read():
                res = True
            else:
                res = False
        Assertion.assert_equal(res, True, "failed to get radius accounting data")


class TC04_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75645"
    description = show_testcase_info(Parameter.TESTPLAN, '1527415', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527415')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_delete_user_account(self):
        resp = Radius_user.del_radius_account('192.168.168.85')
        Assertion.assert_equal(resp, True, "ERR:delete  user account  failed")
        res = Radius_user.show_radius_account()
        Assertion.assert_not_regular(json.dumps(res), '"host": "192.168.168.85"','err: Failed to delete radius server')
        
    def test_03_download_tsr(self):
        resp = diagnostic.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'Name / IP address:                     192.168.168.85'   
        with open(file_path) as f:
            if search_line in f.read():
                res = False
            else:
                res = True
        Assertion.assert_equal(res, True, "failed to delete radius account server")


class TC05_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75643"
    description = show_testcase_info(Parameter.TESTPLAN, '1527413', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527413')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_edit_user_account_setting(self):
        user_obj = {
            "user": {
                "radius": {
                    "accounting": {
                        "include": "domain-and-local-users",
                        "data": {
                            "users_authenticated_by_web_login": True
                        }
                    }
                }
            }
        }
        resp = Radius_user.edit_user_radius_accounting(**user_obj)
        Assertion.assert_equal(resp, True, "ERR: edit user account setting failed")
        res = Radius_user.get_user_radius_accounting()
        Assertion.assert_regular(json.dumps(res), '"include": "domain-and-local-users"','err: edit user account setting failed')
        Assertion.assert_regular(json.dumps(res), '"users_authenticated_by_web_login": true','err: edit user account setting failed')

    def test_03_export_exp(self):
        resp = setting.export_setting_exp()
        Assertion.assert_equal(resp, True, "failed to export the configuration")

    def test_04_delete_user_account(self):
        resp = Radius_user.del_radius_account('192.168.168.85')
        Assertion.assert_equal(resp, True, "ERR:delete  user account  failed")
        res = Radius_user.show_radius_account()
        Assertion.assert_not_regular(json.dumps(res), '"host": "192.168.168.85"','err: Failed to delete radius server')
    
    def test_05_import_exp(self):
        out = setting.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(out, True, "failed to import the configuration")
        time.sleep(120)

    def test_06_verify_radius_and_user_account_settings(self):
        response_get = Radius_user.show_radius_account()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

        res = Radius_user.get_user_radius_accounting()
        Assertion.assert_regular(json.dumps(res), '"include": "domain-and-local-users"','err: edit user account setting failed')
        Assertion.assert_regular(json.dumps(res), '"users_authenticated_by_web_login": true','err: edit user account setting failed')


class TC06_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75646"
    description = show_testcase_info(Parameter.TESTPLAN, '1527416', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527416')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_verify_tool_tip_for_send_accounting_data_to_all_servers(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.navigate_to_radius_accounting_tab()
        out = uiobj.verify_tool_tip_for_send_accounting_data_to_all_servers()
        Assertion.assert_equal(out, True, "ERR: testcase failed")


class TC07_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75649"
    description = show_testcase_info(Parameter.TESTPLAN, '1527419', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527419')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_verify_tool_tip_for_radius_accounting_test(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.navigate_to_radius_accounting_tab()
        out = uiobj.verify_tool_tip_for_radius_accounting_test()
        Assertion.assert_equal(out, True, "ERR: testcase failed")


class TC08_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75648"
    description = show_testcase_info(Parameter.TESTPLAN, '1527418', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527418')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_test_server_connectivity(self):
        test = {
            "user": {
                "radius": {
                    "accounting": {
                        "test": {
                            "name": "192.168.168.85",
                            "user": "test",
                            "ip": "192.168.168.85"
                        }
                    }
                }
            }
        }
        res = Radius_user.test_radius_accounting_server(msg=True, **test)
        success = res[1]['status']['success']
        message = res[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, True, "ERR: test radius server failed")
        Assertion.assert_equal(message, '\nTest result: RADIUS server accepted all accounting requests', "ERR: test  user accounting failed")


class TC09_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75647"
    description = show_testcase_info(Parameter.TESTPLAN, '1527417', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527417')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_start_packet_capture(self):
        packet_cap.clear_packets()
        out = packet_cap.start_capture()
        Assertion.assert_equal(out, True,"ERR: packet capture failed")

    def test_03_test_server_connectivity(self):
        test = {
            "user": {
                "radius": {
                    "accounting": {
                        "test": {
                            "name": "192.168.168.85"
                        }
                    }
                }
            }
        }
        res = Radius_user.test_radius_accounting_server(msg= True,**test)
        success = res[1]['status']['success']
        message = res[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, True, "ERR: test radius server failed")
        Assertion.assert_equal(message, '\nTest result: RADIUS accounting server responded', "ERR: test radius server failed")
    
    def test_04_stop_packet_capture(self):
        out = packet_cap.stop_capture()
        Assertion.assert_equal(out, True, "ERR: packet capture failed")

    def test_05_verify_packet(self):
        resp = packet_cap.export_captured_packets_text_file()
        file_path = '/tmp/packetcaptute'
        search_line = 'ARP TYPE: ARP Request' 
        search_line1 = 'Sender IP Address: 192.168.168.85'
        search_line2 = 'Target IP Address: 192.168.168.168'    

        packet_content = os.popen('cat /tmp/packetcaptute').read() 

        if search_line and search_line1 and search_line2 in str(packet_content):    
           res = True
        else:
           res = False
        Assertion.assert_equal(res, True, "packets are not captured")


class TC10_Radius_Client_Accounting(Test):
    uuid = "SOSAIOT-TC-75650"
    description = show_testcase_info(Parameter.TESTPLAN, '1527420', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527420')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_radius_account(self):
        resp = Radius_user.show_radius_account_by_name('192.168.168.85')
        flag = False if ('"success": false' in json.dumps(resp)) else True
        if flag == False:
            add_radius_user = {
                'host': '192.168.168.85',
                'enable': True,
                'port': 1813,
                'secret': 'password',
                'send_through_vpn_tunnel': False
            }
            response = Radius_user.add_radius_account(**add_radius_user)
            Assertion.assert_equal(response, True, "ERR: add radius server failed")
            response_get = Radius_user.show_radius_account()
            Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.85"','err: Failed to add radius server')

    def test_02_edit_user_account_setting(self):
        user_obj = {
            "user": {
                "radius": {
                    "accounting": {
                        "include": "domain-and-local-users",
                        "data": {
                            "users_authenticated_by_web_login": True
                        }
                    }
                }
            }
        }
        resp = Radius_user.edit_user_radius_accounting(**user_obj)
        Assertion.assert_equal(resp, True, "ERR: edit user account setting failed")
        res = Radius_user.get_user_radius_accounting()
        Assertion.assert_regular(json.dumps(res), '"include": "domain-and-local-users"','err: edit user account setting failed')
        Assertion.assert_regular(json.dumps(res), '"users_authenticated_by_web_login": true','err: edit user account setting failed')

    def test_03_add_localuser(self):
        add_localuser = {
            "action": "add",
            "username": "test",
            "userpassword": "password",
            "member_of": ["Trusted Users", "Everyone"],
          }
         
        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_users() 
        Assertion.assert_regular(json.dumps(response_get), '"name": "test"', 'err: Failed to create localuser') 


    def test_04_start_packet_capture(self):
        packet_cap.clear_packets()
        out = packet_cap.start_capture()
        Assertion.assert_equal(out, True,"ERR: packet capture failed")

    def test_05_login_user1(self):
        localhost.send_command('pkill firefox')

        # login_ui
        uiobj.login_ui('https://192.168.168.168', 'test', 'password')
    
    def test_06_stop_packet_capture(self):
        out = packet_cap.stop_capture()
        Assertion.assert_equal(out, True, "ERR: packet capture failed")

    def test_07_verify_packet(self):
        resp = packet_cap.export_captured_packets_text_file()
        file_path = '/tmp/packetcaptute'
        search_line = 'Src=[192.168.168.169], Dst=[1.0.164.22]'     

        packet_content = os.popen('cat /tmp/packetcaptute').read() 
        print(packet_content)
        print("++++++++++++++++++++++++++++++++")
        # if search_line in str(packet_content):    
        #     res = True
        # else:
        #     res = False
        # Assertion.assert_equal(res, True, "packets are not captured")
  
