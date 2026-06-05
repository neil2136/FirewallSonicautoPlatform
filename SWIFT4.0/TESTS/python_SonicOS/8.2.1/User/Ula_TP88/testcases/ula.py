import sys
import os
import json
import socket
import subprocess

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88')

from definition.settings import *

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
from definition.firewall_configure import FWFunctionConfigure

fwconfigure = FWFunctionConfigure()

class TestConfigureULA(Test):
    uuid = 'NonTC'


    def test_00_ula_configure(self):
        output = fwconfigure.ula_configure()
        Assertion.assert_equal(output, True, "ERR: ula configure failed")
    def test_01_check_local_user_configure(self):
        output = userLocalapi.show_local_user_by_name(name=CaseParams.ula_user_name)
        Assertion.assert_regular(json.dumps(output), 'LAN Subnets', "ERR: check local user configure failed")

class TC01_Access_the_Internet_from_the_LAN_allow_All(Test):
    uuid = "SOSAIOT-TC-75910"
    # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524193', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524193')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    def test_02_check_ula_function(self):
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_not_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")


class TC02_User_authentication_settings_disable_Display_user_login_info_since_last_login(Test):
    uuid = "SOSAIOT-TC-75912"
    description = show_testcase_info(TESTPLAN, '1524195', description=True)['title']

   
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524195')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_display_login_info(self):
        logger.info('Select local authentication method....')
        user_auth = {

            "display_login_info": False
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"display_login_info": false',
                                 "ERR:Failed to select Local authentication method.")

    
class TC03_User_Web_Login_Settings_check_default_settings(Test):
    uuid = "SOSAIOT-TC-75913"
    description = show_testcase_info(TESTPLAN, '1524196', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524196')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_get_default_settings(self):
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"http_redirect_after_login": true', "ERR:Failed to select Local authentication method.")
              
    

class TC04_User_Web_Login_Settings_Boundry_and_negative_test_for_Show_authentication_pag_input(Test):
    uuid = "SOSAIOT-TC-75914"
    description = show_testcase_info(TESTPLAN, '1524197', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524197')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_boundary_test_min(self):
        logger.info('Select local authentication method....')
        user_auth = {
           "time_in_minutes" : 0,
           "browser_redirect_via" : 'interface_ip',
           "http_redirect_after_login" : True

        }
        
        resp,response= user_setting.web_login(**user_auth,msg=True)
        expected_message = 'Login page timeout:  Data out of bounds (min = 1, max = 255).'
        Assertion.assert_equal(resp,False,"err: failed to throw error")

    def test_02_boundary_test_max(self):
        logger.info('Select local authentication method....')
        user_auth = {
           "time_in_minutes" : 300,
           "browser_redirect_via" : 'interface_ip',
           "http_redirect_after_login" : True

        }
        
        resp,response= user_setting.web_login(**user_auth,msg=True)
        expected_message = 'Login page timeout:  Data out of bounds (min = 1, max = 255).'
        Assertion.assert_equal(resp,False,"err: failed to throw error")

class TC05_User_Web_Login_Settings_set_show_authentication_page_for_different_minutes_and_test_function(Test):
    uuid = "SOSAIOT-TC-75915"
    description = show_testcase_info(TESTPLAN, '1524198', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524198')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_authentication_page_for_different_minutes(self):
        user_auth = {
           "time_in_minutes" : 2,
           "browser_redirect_via" : 'interface_ip',
           "http_redirect_after_login" : True

        }
        
        resp= user_setting.web_login(**user_auth,msg=True)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"auth_page_timeout": 2',
        #                          "ERR:Failed to select Local authentication method.")




class TC06_User_Web_Login_Settings_redirect_the_browser(Test):
    uuid = "SOSAIOT-TC-75916"
    description = show_testcase_info(TESTPLAN, '1524199', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524199')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_redirect_the_browser(self):
        logger.info('Select local authentication method....')
        user_auth = {
           "time_in_minutes" : 1,
           "browser_redirect_via" : 'interface_ip',
           "http_redirect_after_login" : True

        }
        
        resp= user_setting.web_login(**user_auth,msg=True)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"interface_ip": true',
        #                          "ERR:Failed to select Local authentication method.")



class TC09_User_Web_Login_Settings_enable_Start_With_Policy_Banner_Before_Login_Window(Test):
    uuid = "SOSAIOT-TC-76060"
    description = show_testcase_info(TESTPLAN, '1524209', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524209')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
            "policy_banner_before_login" : True,
            'pocontent': 'Please read and accept the policy before proceeding.',
            'window_size_width': 800,
            'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
                     },
            'loginpage': {
            'field1': 'Login field 1 text',
            'field2': 'Login field 2 text'
             }
        
        }
        resp=user_setting.customization(**user_auth)
        Assertion.assert_equal(resp, True, "ERR: can't able to delete local user")

       
class TC10_User_Web_Login_Settings_disable_Start_With_Policy_Banner_Before_Login_Window(Test):
    uuid = "SOSAIOT-TC-76061"
    description = show_testcase_info(TESTPLAN, '1524210', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524210')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
            "policy_banner_before_login" : False,
            'pocontent': 'Please read and accept the policy before proceeding.',
             'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
                     },
            'loginpage': {
            'field1': 'Login field 1 text',
            'field2': 'Login field 2 text'
             }
        
        }
        resp=user_setting.customization(**user_auth)
        Assertion.assert_equal(resp, True, "ERR: can't able to delete local user")

class TC11_User_Web_Login_Settings_Policy_Banner_content_edit(Test):
    uuid = "SOSAIOT-TC-76062"
    description = show_testcase_info(TESTPLAN, '1524211', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524211')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_disable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {

            'policy_banner_before_login': True,
            'pocontent': 'Welcome to Sonicwall ',
            'window_size_width': 800,
            'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
            },
            'loginpage': {
                'field1': 'Login field 1 text',
                'field2': 'Login field 2 text'
            }
        }
        
        resp=user_setting.customization(**user_auth)
        Assertion.assert_equal(resp, True, "ERR: unable to edit policy banner")
    
    def test_02_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
            "policy_banner_before_login" : False,
            'pocontent': 'Please read and accept the policy before proceeding.',
             'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
                     },
            'loginpage': {
            'field1': 'Login field 1 text',
            'field2': 'Login field 2 text'
             }
        
        }
        resp=user_setting.customization(**user_auth)
        Assertion.assert_equal(resp, True, "ERR: can't able to delete local user")
        

class TC12_User_Web_Login_Settings_Policy_Banner_content_example_template(Test):
    uuid = "SOSAIOT-TC-76063"
    description = show_testcase_info(TESTPLAN, '1524212', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524212')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_check_example_template(self):
         user_auth = {
            "policy_banner_before_login" : False,
            'pocontent': 'Please read and accept the policy before proceeding.',
             'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
                     },
            'loginpage': {
            'field1': 'Login field 1 text',
            'field2': 'Login field 2 text'
             }
        
        }
         resp=user_setting.customization(**user_auth)
         Assertion.assert_equal(resp, True, "ERR: can't able to delete local user")
        

class TC08_User_Web_Login_Settings_Policy_Banner_content_preview(Test):
    uuid = "SOSAIOT-TC-76064"
    description = show_testcase_info(TESTPLAN, '1524213', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524213')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_check_example_template(self):
         user_auth = {
            "policy_banner_before_login" : False,
            'pocontent': 'Please read and accept the policy before proceeding.',
             'window_size_height': 600,
            'scroll_bars': True,
            'zonetype': {
                'zone1': 'value1',
                'zone2': 'value2'
                     },
            'loginpage': {
            'field1': 'Login field 1 text',
            'field2': 'Login field 2 text'
             }
        
        }
         resp=user_setting.customization(**user_auth)
         Assertion.assert_equal(resp, True, "ERR: can't able to delete local user")
        

  # User Web Login Settings-Policy Banner preview
class TC13_User_Session_Settings_for_Web_Login_disable_Enable_login_session_limit_for_web_logins(Test):
   
    uuid = "SOSAIOT-TC-75925"
    description = show_testcase_info(TESTPLAN, '1524215', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524215')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 1
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 1',
        #                          "ERR:Failed to select Local authentication method.")


class TC14_User_Session_Settings_for_Web_Login_enable_Enable_login_session_limit_for_web_logins(Test):
   
    uuid = "SOSAIOT-TC-75927"
    description = show_testcase_info(TESTPLAN, '1524217', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524217')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 5
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 5',
        #                          "ERR:Failed to select Local authentication method.")


class TC15_User_Session_Settings_for_Web_Login_Boundary_negative_test_for_Login_session_limit(Test):
    uuid = "SOSAIOT-TC-75928"
    description = show_testcase_info(TESTPLAN, '1524218', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524218')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

   

    def test_02_boundary_test_max(self):
        logger.info('Select local authentication method....')
        user_auth = {
           "web_login_session_limit": 657768

        }
        
        resp,response= user_setting.user_session(**user_auth,msg=True)
        expected_message = 'Login page timeout:  Data out of bounds (min = 1, max = 255).'
        Assertion.assert_equal(resp,False,"err: failed to throw error")


class TC16_User_Session_Settings_for_Web_Login_function_test_for_Login_session_limit(Test):
    uuid = "SOSAIOT-TC-75929"
    # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524219', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524219')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 1
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 1',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    @repeat_method(5)
    def test_04_check_ula_function(self):
        
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd S0nic@uto'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        time.sleep(120)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC17_User_Session_Settings_for_Web_Login_disable_Show_user_login_status_window(Test):
    uuid = "SOSAIOT-TC-75930"
    description = show_testcase_info(TESTPLAN, '1524220', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524220')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
              "show_user_status_window": False,
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"show_user_status_window": false',
        #                          "ERR:Failed to select Local authentication method.")


class TC18_User_Session_Settings_for_Web_Login_Show_user_login_status_window(Test):
    uuid = "SOSAIOT-TC-75931"
    description = show_testcase_info(TESTPLAN, '1524221', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524221')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
              "show_user_status_window": True,
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"show_user_status_window": true',
                                 "ERR:Failed to select Local authentication method.")

class TC19_Session_Settings_for_Web_Login_Enable_disconnected_user_detection(Test):
    uuid = "SOSAIOT-TC-75934"
    description = show_testcase_info(TESTPLAN, '1524224', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524224')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
              "disconnected_user_detect": True,
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"disconnected_user_detect": true',
                                 "ERR:Failed to select Local authentication method.")

class TC20_User_Session_Settings_for_Web_Login_disable_disconnected_user_detection(Test):
   
    uuid = "SOSAIOT-TC-75935"
    description = show_testcase_info(TESTPLAN, '1524225', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524225')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
              "disconnected_user_detect": False,
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        # Assertion.assert_regular(json.dumps(resp), '"disconnected_user_detect": false',
        #                          "ERR:Failed to select Local authentication method.")

class TC21_User_status_page_check_default_settings(Test):
    uuid = "SOSAIOT-TC-75946"
    description = show_testcase_info(TESTPLAN, '1524237', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524237')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")


class TC22_User_status_page_enable_include_inactive_users(Test):
    uuid = "SOSAIOT-TC-75948"
    description = show_testcase_info(TESTPLAN, '1524239', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524239')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
        'inactive_users': True,
        'unauthenticated_users': False,
        }
        user_status.user_management(**user_auth)
        Assertion.assert_equal(True, True, "ERR: Failed to update")

class TC23_User_status_page_enable_show_unauthenticated_users(Test):
    uuid = "SOSAIOT-TC-75949"
    description = show_testcase_info(TESTPLAN, '2477736', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2477736')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
        'inactive_users': True,
        'unauthenticated_users': True,
        }
        user_status.user_management(**user_auth)
        Assertion.assert_equal(True, True, "ERR: Failed to update")

class TC24_User_status_page_set_different_start_value_for_items_to_view(Test):
    uuid = "SOSAIOT-TC-75950"
    description = show_testcase_info(TESTPLAN, '1524241', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524241')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
        'inactive_users': True,
        'unauthenticated_users': True,
        }
        user_status.user_management(**user_auth)
        Assertion.assert_equal(True, True, "ERR: Failed to update")

class TC25_User_status_page_check_user_status_for_logged_in_users(Test):
    uuid = "SOSAIOT-TC-75952"
    description = show_testcase_info(TESTPLAN, '1524243', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524243')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_local_user_auth_method(self):
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")

   

class TC26_User_status_page_logout_selected_users(Test):
    uuid = "SOSAIOT-TC-75973"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524288', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524288')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524219')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
   
    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    @repeat_method(5)
    def test_04_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd S0nic@uto'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        resp = user_status.logout_user_ip("192.168.168.20")
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC27_User_status_page_user_counts_button(Test):
    uuid = "SOSAIOT-TC-75954"
   # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524245', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524245')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_04_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        resp = user_status.logout_user_ip("192.168.168.20")
        time.sleep(10)
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


class TC28_Relogin_after_inactivity_timer_expired(Test):
    uuid = "SOSAIOT-TC-75984"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524299', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524299')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 1
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 1',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    @repeat_method(5)
    def test_04_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd S0nic@uto'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        time.sleep(120)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
class TC29_User_Logout_Login_session_limit_expired(Test):
    uuid = "SOSAIOT-TC-75985"
   # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524300', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524300')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524219')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 1
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 1',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    @repeat_method(5)
    def test_04_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd S0nic@uto'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        time.sleep(120)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC30_Relogin_after_Login_session_limit_expired(Test):
    uuid = "SOSAIOT-TC-75986"
    # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524300', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524300')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524219')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_enable_local_user_auth_method(self):
        logger.info('Select local authentication method....')
        user_auth = {
             "web_login_session_limit": 1
        }

        user_setting.user_session(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"web_login_session_limit": 1',
                                 "ERR:Failed to select Local authentication method.")

    def test_02_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('DMZ', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']
        access_rule_option = {
            'name': name,
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")


    @repeat_method(5)
    def test_04_check_ula_function(self):
        
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        time.sleep(80)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")