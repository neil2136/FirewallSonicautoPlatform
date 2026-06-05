import sys
import os
import json
import subprocess

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/API_Administration')

from definition.settings import *

class Configure_WAN_AND_LAN(Test):
    uuid = 'NonTC'

    def test_01_config_interfaces(self):
        logger.info('config x1 to WAN zone.')
        x1_interface = {
            'if': 'X1',
            'zone': 'WAN',
            'ip': '13.0.0.10',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        rc = interface.config_interface(**x1_interface)
        logger.info(rc)
        logger.info("Add ssh true for WAN")

        x0_interface = {
            'if': 'X0',
            'zone': 'LAN',
            'ip': '192.168.168.168',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        rc = interface.config_interface(**x0_interface)
        logger.info(rc)
        logger.info("Add ssh true for LAN")

class Admin_001(Test):    
    uuid = "SOSAIOT-TC-46905"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"enable": true', "err:failed to retrieve firewall name")

class Admin_097(Test):
    uuid = "SOSAIOT-TC-46983"
    description = show_testcase_info(Parameter.TESTPLAN, '97', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '97')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_tls_true(self):
        admin_dict16 = {
            'tls_and_above': True
        }
        response = Admin_settings.conf_admin(**admin_dict16)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"tls_and_above": true',"err:failed to set tls_and_above as true")

class Admin_05(Test):
    uuid = "SOSAIOT-TC-46909"
    description = show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_valid_name(self):
        admin_dict1 = {
            'firewall_name': "2CB8ED693230"
        }

        response = Admin_settings.conf_admin(**admin_dict1)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"firewall_name": "2CB8ED693230"', "err:failed to give valid value to firewall")

class Admin_07(Test):
    uuid = "SOSAIOT-TC-46911"
    description = show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_domain_name(self):
        admin_dict2 = {
            'firewall_domain_name': ""
        }

        response = Admin_settings.conf_admin(**admin_dict2)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"firewall_domain_name": ""',"err:failed to set firewalls domain name")

class Admin_027(Test):
    uuid = "SOSAIOT-TC-46924"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_password_aging(self):
        admin_dict4 = {
            'aging': {}
        }
        response = Admin_settings.conf_admin(**admin_dict4)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"aging": {}', "err:failed give a valid number to password aging")

class Admin_034(Test):
    uuid = "SOSAIOT-TC-46931"
    description = show_testcase_info(Parameter.TESTPLAN, '34', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_password_num(self):
        admin_dict7 = {
            "minimum_length": 8
        }
        response = Admin_settings.conf_admin(**admin_dict7)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"minimum_length": 8', "err:failed to set minimum length ")

class Admin_049(Test):
    uuid = "SOSAIOT-TC-46935"
    description = show_testcase_info(Parameter.TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_multiple_admin(self):
        admin_dict5 = {
            'multiple_admin': True
        }
        response = Admin_settings.conf_admin(**admin_dict5)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        # Assertion.assert_regular(json.dumps(response1), '"multiple_admin": true', "err:failed")

class Admin_055(Test):
    uuid = "SOSAIOT-TC-46941"
    description = show_testcase_info(Parameter.TESTPLAN, '55', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '55')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_idle_logout(self):
        admin_dict6 = {

            'idle_logout_time': 60
        }
        response = Admin_settings.conf_admin(**admin_dict6)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"idle_logout_time": 60', "err:failed to set idle logout time")

class Admin_059(Test):
    uuid = "SOSAIOT-TC-46945"
    description = show_testcase_info(Parameter.TESTPLAN, '59', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_failures_rate(self):
        admin_dict7 = {

            'failures_rate': 3
        }
        response = Admin_settings.conf_admin(**admin_dict7)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"failures_rate": 3', "err:failed to set failures to valid num")

class Admin_073(Test):
    uuid = "SOSAIOT-TC-46959"
    description = show_testcase_info(Parameter.TESTPLAN, '73', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '73')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_enchanced_audit_log(self):
        admin_dict11 = {

            'enhanced_audit_logging': True
        }
        response = Admin_settings.conf_admin(**admin_dict11)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"enhanced_audit_logging": true',"err:failed to enable enhanced audit logging")

class Admin_089(Test):
    uuid = "SOSAIOT-TC-46975"
    description = show_testcase_info(Parameter.TESTPLAN, '89', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '89')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_table_size(self):
        admin_dict14 = {

            'dashboard_as_starting_page': True
        }
        response = Admin_settings.conf_admin(**admin_dict14)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"dashboard_as_starting_page": true', "err:failed to enable dashboard_as_starting_page")

class Admin_135(Test):
    uuid = "SOSAIOT-TC-47018"
    description = show_testcase_info(Parameter.TESTPLAN, '135', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '135')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_ssh_port(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"enable": true', "err:failed retrieve port number")

class Admin_138(Test):
    uuid = "SOSAIOT-TC-47021"
    description = show_testcase_info(Parameter.TESTPLAN, '138', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '138')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_ssh_port(self):
        admin_dict19 = {
            "ssh": {
                "port": 54022
            }
        }
        response = Admin_settings.conf_admin(**admin_dict19)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"enable": true', "err:failed to set ssh port a valid num")

class Admin_134(Test):
    uuid = "SOSAIOT-TC-47017"
    description = show_testcase_info(Parameter.TESTPLAN, '134', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '134')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_ssh_port(self):
        admin_dict19 = {
            "https_port": 443
        }
        response = Admin_settings.conf_admin(**admin_dict19)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"enable": true', "err:failed to set https port to a valid num")

class Admin_002(Test):    
    uuid = "SOSAIOT-TC-46906"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"firewall_domain_name": ""', "err:failed to retrieve firewall name")

class Admin_003(Test):    
    uuid = "SOSAIOT-TC-46907"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_firewall_min_bound(self):
        admin_json = {
            "administration": {
                "firewall_name": "1234567"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

    def test_set_firewall_max_bound(self):
        admin_json = {
            "administration": {
                "firewall_name": "1234567891234567891234567891234567891234567891234567891234567891"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_004(Test):    
    uuid = "SOSAIOT-TC-46908"
    description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_firewall_special_character(self):
        admin_json = {
            "administration": {
                "firewall_name": "!@$%^&*()"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update")

        logger.info("Firewall name reset to default name admin")
        admin_dict1 = {
            'firewall_name': "2CB8ED693230"
        }
        response = Admin_settings.conf_admin(**admin_dict1)
        logger.info(response)

class Admin_006(Test):    
    uuid = "SOSAIOT-TC-46910"
    description = show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_firewall_domain(self):
        admin_json = {
            "administration": {
                "firewall_domain_name": "######"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update")

        logger.info("Firewall name reset to default name admin")
        admin_dict1 = {
            'firewall_name': "2CB8ED693230"
        }
        response = Admin_settings.conf_admin(**admin_dict1)
        logger.info(response)

class Admin_008(Test):    
    uuid = "SOSAIOT-TC-46912"
    description = show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_name(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"name": "admin"', "err:failed to retrieve firewall name")

class Admin_009(Test):    
    uuid = "SOSAIOT-TC-46913"
    description = show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_admin_name_special(self):
        admin_json = {
            "administration": {
                "admin": { 
                    "name": "}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

def restore_fw_via_curl_cmd(int_ip):
    cmd = f"curl 'https://{int_ip}/api/sonicos/boot/current/factory-default' " + \
            "-H 'Accept: application/json, text/plain, */*' " + \
            "-H 'X-SNWL-API-Scope: extended' --data-raw '' -k"
    logger.info(cmd)
    resp = os.popen(cmd).read()
    logger.info(resp)
    return resp

def check_fw_up():
    rc = False
    for each in range(0,30):
        logger.info(f'Sleep 30s wait for fw up for the {each} time.')
        time.sleep(30)
        out = os.popen(f'ping {ip} -c 5').read()
        logger.info(out)
        if '100% packet loss' not in out:
            logger.info("fw is up...")
            rc = True
            break
        elif each == 30:
            logger.info("Firewall is not up")
    return rc

class Admin_010(Test):    
    uuid = "SOSAIOT-TC-46914"
    description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_admin_name_valid(self):
        admin_json = {
            "administration": {
                "admin": { 
                    "name": "admin"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response1 = Admin_settings.show_admin_setting()
        logger.info(response1)
        Assertion.assert_regular(json.dumps(response1), '"name": "admin"',"err:failed to set valid")

class Admin_011(Test):    
    uuid = "SOSAIOT-TC-46915"
    description = show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_factory_fw(self):
        rc = setting_obj.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: test_01_factory_fw failed")
        
    def test_02_set_password(self):
        admin_json = {
            "old_pwd": G_PASSWORD_NEW,
            "new_pwd": "1111"
        }
        response = Admin_settings.change_password(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False,"err:failed to set special character")

    def test_03_factory_reboot_fw(self):
        resp = restore_fw_via_curl_cmd('192.168.168.168')
        Assertion.assert_regular(str(resp), "SonicOS will restore to factory defaults", "ERR: test_02_factory_reboot_fw failed")

    def test_04_check_is_fw_up(self):
        rc = check_fw_up()
        Assertion.assert_equal(rc, True, "ERR: test_03_check_is_fw_up failed")

    def test_05_change_password(self):
        cmd = fw_ui.login_ui_pwd_change('password', G_PASSWORD_NEW)
        Assertion.assert_equal(cmd[0], True, "ERR : Testcase failed")
        assert cmd[0], "Testcase failed"

class Admin_012(Test):    
    uuid = "SOSAIOT-TC-46916"
    description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_set_password(self):
        admin_json = {
            "old_pwd": G_PASSWORD_NEW,
            "new_pwd": "P@ssw0rd"  
        }
        response = Admin_settings.change_password(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "err:failed to set valid")

    def test_02_changing_to_default_password(self):
        x0_interface = {
            'if': 'X0',
            'zone': 'LAN',
            'ip': '192.168.168.168',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        rc = interface.config_interface(**x0_interface)
        logger.info(rc)
        logger.info("Add ssh true for LAN")

        response = change_admin_password(pwd='P@ssw0rd', new_pwd=G_PASSWORD_NEW)
        Assertion.assert_equal(response, True, "ERR: Unable to update default password")

class Admin_013(Test):    
    uuid = "SOSAIOT-TC-46917"
    description = show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_set_password(self):
        admin_json = {
            "old_pwd": G_PASSWORD_NEW,
            "new_pwd": G_PASSWORD_NEW
        }
        response = Admin_settings.change_password(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "err:failed to set password")

class Admin_014(Test):    
    uuid = "SOSAIOT-TC-46918"
    description = show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_set_password(self):
        admin_json = {
            "old_pwd": G_PASSWORD_NEW,
            "new_pwd": "!@$%^&*"
       }
        response = Admin_settings.change_password(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "err:failed to set password")

class Admin_015(Test):    
    uuid = "SOSAIOT-TC-46919"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_set_password(self):
        admin_json = {
            "old_pwd": G_PASSWORD_NEW,
            "new_pwd": "P@ssw0rd"
        }
        response = Admin_settings.change_password(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "err:failed to set valid")

    def test_02_changing_to_default_password(self):
        response = change_admin_password(pwd='P@ssw0rd', new_pwd=G_PASSWORD_NEW)
        Assertion.assert_equal(response, True, "ERR: Unable to update default password")

class Admin_017(Test):    
    uuid = "SOSAIOT-TC-46920"
    description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"one_time_password": {}', "err:failed to retrieve firewall name")

class Admin_024(Test):    
    uuid = "SOSAIOT-TC-46921"
    description = show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"aging": {}', "err:failed to retrieve firewall name")

class Admin_025(Test):    
    uuid = "SOSAIOT-TC-46922"
    description = show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "aging": {
                        "duration": 999999
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update aging password")

class Admin_026(Test):    
    uuid = "SOSAIOT-TC-46923"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "aging": {
                        "duration": "aaa@"
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update aging password")

class Admin_028(Test):    
    uuid = "SOSAIOT-TC-46925"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "uniqueness": {
                        "count": 33
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update uniqueness count password")

class Admin_029(Test):    
    uuid = "SOSAIOT-TC-46926"
    description = show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "uniqueness": {
                        "count": "aaa@"
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update uniqueness count password")

class Admin_030(Test):    
    uuid = "SOSAIOT-TC-46927"
    description = show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "uniqueness": {
                        "count": 32
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update uniqueness count password")

class Admin_031(Test):    
    uuid = "SOSAIOT-TC-46928"
    description = show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "enforce_character_difference": True
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update enforce_character_difference password")

class Admin_032(Test):    
    uuid = "SOSAIOT-TC-46929"
    description = show_testcase_info(Parameter.TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "minimum_length": 33
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update length password")

class Admin_033(Test):    
    uuid = "SOSAIOT-TC-46930"
    description = show_testcase_info(Parameter.TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "minimum_length": "abc%"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update length password")

class Admin_036(Test):    
    uuid = "SOSAIOT-TC-46932"
    description = show_testcase_info(Parameter.TESTPLAN, '36', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "complexity": {
                        "type": "alpha-and-numeric",
                        "upper-case": 0,
                        "lower-case": 1,
                        "digit": 0,
                        "symbol": 1
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update complexity password")

class Admin_037(Test):    
    uuid = "SOSAIOT-TC-46933"
    description = show_testcase_info(Parameter.TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_set_password_aging(self):
        admin_json = {
            "administration": {
                "password": {
                    "complexity": {
                        "type": "alpha-and-numeric",
                        "upper-case": 3,
                        "lower-case": 1,
                        "digit": 1,
                        "symbol": 1
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update complexity password")

class Admin_048(Test):    
    uuid = "SOSAIOT-TC-46934"
    description = show_testcase_info(Parameter.TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"multiple_admin": False', "err:failed to retrieve firewall name")

class Admin_050(Test):    
    uuid = "SOSAIOT-TC-46936"
    description = show_testcase_info(Parameter.TESTPLAN, '50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "password": {
                    "constraints_apply_to": {
                        "builtin_admin": True,
                        "full_admins": True,
                        "limited_admins": False,
                        "local_users": False,
                        "guest_admins": False
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update password")

class Admin_051(Test):    
    uuid = "SOSAIOT-TC-46937"
    description = show_testcase_info(Parameter.TESTPLAN, '51', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "password": {
                    "constraints_apply_to": {
                        "builtin_admin": True,
                        "full_admins": True,
                        "limited_admins": True,
                        "local_users": True,
                        "guest_admins": True
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update constraints password")

class Admin_052(Test):    
    uuid = "SOSAIOT-TC-46938"
    description = show_testcase_info(Parameter.TESTPLAN, '52', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"idle_logout_time": 5,', "err:failed to retrieve firewall name")

class Admin_053(Test):    
    uuid = "SOSAIOT-TC-46939"
    description = show_testcase_info(Parameter.TESTPLAN, '53', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '53')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "idle_logout_time": 99999
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update idle logout time")

class Admin_054(Test):    
    uuid = "SOSAIOT-TC-46940"
    description = show_testcase_info(Parameter.TESTPLAN, '54', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '54')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "idle_logout_time": "a%"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update idle logout time")

class Admin_056(Test):    
    uuid = "SOSAIOT-TC-46942"
    description = show_testcase_info(Parameter.TESTPLAN, '56', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '56')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_rate": 99,
                    "failures_duration": 10,
                    "lockout_duration": 10
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update failure rate")

class Admin_057(Test):
    uuid = "SOSAIOT-TC-46943"
    description = show_testcase_info(Parameter.TESTPLAN, '57', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_rate": 100
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update failure rate")

class Admin_058(Test):    
    uuid = "SOSAIOT-TC-46944"
    description = show_testcase_info(Parameter.TESTPLAN, '58', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_rate": "a"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update failure rate")

class Admin_060(Test):    
    uuid = "SOSAIOT-TC-46946"
    description = show_testcase_info(Parameter.TESTPLAN, '60', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '60')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_duration": 241
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update failure duration")

class Admin_061(Test):    
    uuid = "SOSAIOT-TC-46947"
    description = show_testcase_info(Parameter.TESTPLAN, '61', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '61')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_duration": "a"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update failure duration")

class Admin_062(Test):    
    uuid = "SOSAIOT-TC-46948"
    description = show_testcase_info(Parameter.TESTPLAN, '62', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '62')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "failures_duration": 24
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update failure duration")

class Admin_063(Test):    
    uuid = "SOSAIOT-TC-46949"
    description = show_testcase_info(Parameter.TESTPLAN, '63', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '63')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "lockout_duration": 62
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update lockout duration")

class Admin_064(Test):    
    uuid = "SOSAIOT-TC-46950"
    description = show_testcase_info(Parameter.TESTPLAN, '64', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '64')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "lockout_duration": "a"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update lockout duration")

class Admin_065(Test):    
    uuid = "SOSAIOT-TC-46951"
    description = show_testcase_info(Parameter.TESTPLAN, '65', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '65')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "user_lockout": {
                    "lockout_duration": 55
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, True, "ERR: Unable to update lockout duration")

class Admin_066(Test):    
    uuid = "SOSAIOT-TC-46952"
    description = show_testcase_info(Parameter.TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "log_without_lockout": False
            }
        }
        resp = Admin_settings.conf_admin_update(**admin_json)

        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"log_without_lockout": false,', "err:failed to retrieve firewall name")

class Admin_067(Test):    
    uuid = "SOSAIOT-TC-46953"
    description = show_testcase_info(Parameter.TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "log_without_lockout": True
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"log_without_lockout": true,', "err:failed to retrieve firewall name")

class Admin_068(Test):    
    uuid = "SOSAIOT-TC-46954"
    description = show_testcase_info(Parameter.TESTPLAN, '68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '68')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "inter_admin_messaging": {"interval":99}
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"interval": 99', "err:Failed to retrieve firewall name")

class Admin_069(Test):    
    uuid = "SOSAIOT-TC-46955"
    description = show_testcase_info(Parameter.TESTPLAN, '69', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '69')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "inter_admin_messaging": {"interval":999}
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update inter_admin_messaging")

class Admin_070(Test):    
    uuid = "SOSAIOT-TC-46956"
    description = show_testcase_info(Parameter.TESTPLAN, '70', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '70')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "inter_admin_messaging": {"interval":"a"}
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update inter_admin_messaging")

class Admin_071(Test):    
    uuid = "SOSAIOT-TC-46957"
    description = show_testcase_info(Parameter.TESTPLAN, '71', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "inter_admin_messaging": {"interval":9}
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"interval": 9', "err:Failed to retrieve firewall name")

class Admin_072(Test):    
    uuid = "SOSAIOT-TC-46958"
    description = show_testcase_info(Parameter.TESTPLAN, '72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_get_admin_base(self):
        admin_json = {
            "enhanced_audit_logging": False
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"enhanced_audit_logging": false', "err:Failed to retrieve firewall name")

class Admin_074(Test):    
    uuid = "SOSAIOT-TC-46960"
    description = show_testcase_info(Parameter.TESTPLAN, '74', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '74')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"wireless_controller_mode": "normal-firewall"', "err:Failed to retrieve firewall name")
        
class Admin_075(Test):    
    uuid = "SOSAIOT-TC-46961"
    description = show_testcase_info(Parameter.TESTPLAN, '75', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '75')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_factory_fw(self):
        rc = setting_obj.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: test_01_factory_fw failed")
        
    def test_02_get_admin_base(self):
        admin_json = {
            "administration": {
                "wireless_controller_mode":"wireless-controller"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)

        x0_interface = {
            'if': 'X0',
            'zone': 'LAN',
            'ip': '192.168.168.168',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True
        }
        rc = interface.config_interface(**x0_interface)
        logger.info(rc)
        logger.info("Add ssh true for LAN")

        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"wireless_controller_mode": "wireless-controller"', "err:Failed to retrieve firewall name")

    def test_03_check_is_fw_up(self):
        time.sleep(60)
        rc = check_fw_up()
        Assertion.assert_equal(rc, True, "ERR: test_03_check_is_fw_up failed")

class Admin_076(Test):    
    uuid = "SOSAIOT-TC-46962"
    description = show_testcase_info(Parameter.TESTPLAN, '76', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '76')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_get_admin_base(self):
        admin_json = {
            "administration": {
                "wireless_controller_mode":"non-wireless-controller"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        time.sleep(10)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"wireless_controller_mode": "non-wireless-controller"', "err:Failed to retrieve firewall name")

    def test_02_check_is_fw_up(self):
        time.sleep(60)
        rc = check_fw_up()
        Assertion.assert_equal(rc, True, "ERR: test_03_check_is_fw_up failed")

class Admin_077(Test):    
    uuid = "SOSAIOT-TC-46963"
    description = show_testcase_info(Parameter.TESTPLAN, '77', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '77')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_get_admin_base(self):
        admin_json = {
            "administration": {
                "wireless_controller_mode":"normal-firewall"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"wireless_controller_mode": "normal-firewall"', "err:Failed to retrieve firewall name")

    def test_02_check_is_fw_up(self):
        time.sleep(60)
        rc = check_fw_up()
        Assertion.assert_equal(rc, True, "ERR: test_03_check_is_fw_up failed")

class Admin_078(Test):    
    uuid = "SOSAIOT-TC-46964"
    description = show_testcase_info(Parameter.TESTPLAN, '78', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '78')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"use_self_signed": true', "err:Failed to retrieve firewall name")

class Admin_079(Test):
    uuid = "SOSAIOT-TC-46965"
    description = show_testcase_info(Parameter.TESTPLAN, '79', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '79')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "cert_common_name": "aaa"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"cert_common_name": "aaa"', "err:Failed to retrieve firewall name")

class Admin_080(Test):    
    uuid = "SOSAIOT-TC-46966"
    description = show_testcase_info(Parameter.TESTPLAN, '80', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '80')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "cert_common_name": "mia"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"cert_common_name": "mia"', "err:Failed to retrieve firewall name")

class Admin_081(Test):    
    uuid = "SOSAIOT-TC-46967"
    description = show_testcase_info(Parameter.TESTPLAN, '81', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '81')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "cert_common_name": 123456
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update cert_common_name")

class Admin_082(Test):    
    uuid = "SOSAIOT-TC-46968"
    description = show_testcase_info(Parameter.TESTPLAN, '82', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '82')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"default_table_size": 50', "err:Failed to retrieve firewall name")
        
class Admin_083(Test):    
    uuid = "SOSAIOT-TC-46969"
    description = show_testcase_info(Parameter.TESTPLAN, '83', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '83')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "default_table_size": 49999
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update default_table_size")
        
class Admin_084(Test):    
    uuid = "SOSAIOT-TC-46970"
    description = show_testcase_info(Parameter.TESTPLAN, '84', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '84')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "default_table_size": "aaa"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update default_table_size")

class Admin_085(Test):    
    uuid = "SOSAIOT-TC-46971"
    description = show_testcase_info(Parameter.TESTPLAN, '85', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '85')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "default_table_size": 5000
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"default_table_size": 5000', "err:Failed to retrieve default_table_size")

class Admin_086(Test):    
    uuid = "SOSAIOT-TC-46972"
    description = show_testcase_info(Parameter.TESTPLAN, '86', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '86')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "refresh_interval": 301
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update refresh_interval")

class Admin_087(Test):    
    uuid = "SOSAIOT-TC-46973"
    description = show_testcase_info(Parameter.TESTPLAN, '87', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '87')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "refresh_interval": "awe"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update refresh_interval")

class Admin_088(Test):    
    uuid = "SOSAIOT-TC-46974"
    description = show_testcase_info(Parameter.TESTPLAN, '88', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '88')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "refresh_interval": 299
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"refresh_interval": 299', "err:Failed to retrieve refresh_interval")

class Admin_090(Test):    
    uuid = "SOSAIOT-TC-46976"
    description = show_testcase_info(Parameter.TESTPLAN, '90', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '90')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "form_delay": 555,
                        "button_delay": 555,
                        "text_delay": 555
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"form_delay": 555', "err:Failed to add form_delay")

class Admin_091(Test):    
    uuid = "SOSAIOT-TC-46977"
    description = show_testcase_info(Parameter.TESTPLAN, '91', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '91')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "form_delay": 55
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update form_delay")

        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "form_delay": 5555
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update form_delay")

class Admin_092(Test):    
    uuid = "SOSAIOT-TC-46978"
    description = show_testcase_info(Parameter.TESTPLAN, '92', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '92')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "form_delay": "5a5"
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update form_delay")

class Admin_093(Test):    
    uuid = "SOSAIOT-TC-46979"
    description = show_testcase_info(Parameter.TESTPLAN, '93', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '93')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "button_delay": 55
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update button_delay")

        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "button_delay": 5555
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update button_delay")

class Admin_094(Test):    
    uuid = "SOSAIOT-TC-46980"
    description = show_testcase_info(Parameter.TESTPLAN, '94', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '94')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "button_delay": "a"
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update button_delay")

class Admin_095(Test):    
    uuid = "SOSAIOT-TC-46981"
    description = show_testcase_info(Parameter.TESTPLAN, '95', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '95')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "text_delay": 55
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update text_delay")

        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "text_delay": 5555
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update text_delay")

class Admin_096(Test):    
    uuid = "SOSAIOT-TC-46982"
    description = show_testcase_info(Parameter.TESTPLAN, '96', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '96')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "web_management": {
                    "tooltip": {
                        "text_delay": "a"
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update text_delay")

class Admin_098(Test):  
    jira = 'GEN8-12164'  
    uuid = "SOSAIOT-TC-46984"
    description = show_testcase_info(Parameter.TESTPLAN, '98', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '98')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_admin_base(self):
        admin_json = {
            "administration": {
                "out_of_band_management": True
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"out_of_band_management": true', "err:Failed to add out_of_band_management")

class Admin_099(Test):
    uuid = "SOSAIOT-TC-46985"
    description = show_testcase_info(Parameter.TESTPLAN, '99', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '99')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_client_certificate_check(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"client_certificate_check": false', "err:Failed retrieve client_certificate_check")

class Admin_100(Test):    
    uuid = "SOSAIOT-TC-46986"
    description = show_testcase_info(Parameter.TESTPLAN, '100', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '100')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_get_admin_base(self):
        rs = configure_and_verify_cert_check(openstack_PC='-PC1', login_ip='192.168.168.168')
        logger.info(rs)

    def test_02_factory_fw(self):
        rc = setting_obj.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: test_01_factory_fw failed")

def send_and_recv(channel, command, wait=1, max_scrolls=30):
    logger.info(f"Sending command: {command}")
    channel.send(command + '\n')
    time.sleep(wait)
    
    output = ""
    scrolls = 0

    while scrolls < max_scrolls:
        while channel.recv_ready():
            chunk = channel.recv(5000).decode("utf-8", errors="ignore")
            output += chunk

            if '--MORE--' in chunk:
                if scrolls >= max_scrolls:
                    logger.warning("Reached max scroll limit. Sending Ctrl+C to stop output.")
                    channel.send('\x03')  # Ctrl+C to interrupt
                    time.sleep(1)
                    while channel.recv_ready():
                        output += channel.recv(5000).decode("utf-8", errors="ignore")
                    logger.info(f"Command output (truncated at {max_scrolls} scrolls):\n{output}")
                    return output
                channel.send('\n')
                scrolls += 1
                time.sleep(0.5)

        if '--MORE--' not in output:
            break
        time.sleep(0.5)

    logger.info(f"Command output:\n{output}")
    return output

def configure_and_verify_cert_check(openstack_PC, login_ip):
    hostname = Params.testbed + openstack_PC
    username = "root"
    password = "password"
    admin_password = G_PASSWORD_NEW

    result_log = ""

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password)
        logger.info(f"Connected to host: {hostname}")

        channel = ssh.invoke_shell()
        time.sleep(2)

        result_log += send_and_recv(channel, f"ssh admin@{login_ip}", wait=2)

        if "yes/no" in result_log:
            result_log += send_and_recv(channel, "yes", wait=2)
        if "password" in result_log:
            result_log += send_and_recv(channel, admin_password, wait=2)

        cmds = [
            admin_password, "configure", "yes", "administration",
            "web-management client-certificate-check",
            "web-management client-certificate-issuer AAA\\ Certificate\\ Services",
            "commit"
        ]

        for cmd in cmds:
            result_log += send_and_recv(channel, cmd, wait=2)

        if "Changes made." not in result_log and "Status returned processing command:\n    commit" not in result_log:
            raise Exception("Commit might have failed")

        result_log += "\n[✓] Commit appears successful.\n"

        verify_output = send_and_recv(channel, "show administration", wait=2)
        if "web-management client-certificate-check" in verify_output:
            result_log += "[✓] Verified: client-certificate-check is enabled.\n"
        else:
            raise Exception("Verification failed: 'client-certificate-check' not found.")

        # Disable
        disable_cmds = [
            "no web-management client-certificate-check",
            "commit"
        ]
        for cmd in disable_cmds:
            result_log += send_and_recv(channel, cmd, wait=2)

        verify_disable = send_and_recv(channel, "show administration", wait=2)
        if "no web-management client-certificate-check" in verify_disable:
            result_log += "[✓] Verified: client-certificate-check is disabled.\n"
        else:
            raise Exception("Disable failed: 'client-certificate-check' still present.")

        ssh.close()
        return result_log

    except Exception as e:
        return f"[✗] Error: {e}"

class Admin_102(Test):
    uuid = "SOSAIOT-TC-46987"
    description = show_testcase_info(Parameter.TESTPLAN, '102', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '102')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_gms(self):
        admin_json = {
            "administration": {
                "gms_management":{}
            }
        }
        res = Admin_settings.conf_admin_update(**admin_json)

        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {}', "err:Failed to retrieve gms")

class Admin_103(Test):
    uuid = "SOSAIOT-TC-46988"
    description = show_testcase_info(Parameter.TESTPLAN, '103', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '103')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {},
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to retrieve gms")

class Admin_104(Test):
    uuid = "SOSAIOT-TC-46989"
    description = show_testcase_info(Parameter.TESTPLAN, '104', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "C0EAE4CCF5E8",
                        "encryption_type": "des-md5",
                        "encryption_key": "0cf224ea209c87c8",
                        "authentication_key": "ef1f180a865b552c052c3c0b295e2458",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"ipsec_tunnel"', "err:Failed to retrieve gms")

class Admin_105(Test):
    uuid = "SOSAIOT-TC-46990"
    description = show_testcase_info(Parameter.TESTPLAN, '105', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '105')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "existing_tunnel": {
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"existing_tunnel"', "err:Failed to retrieve gms")

class Admin_106(Test):
    uuid = "SOSAIOT-TC-46991"
    description = show_testcase_info(Parameter.TESTPLAN, '106', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '106')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {},
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_107(Test):
    uuid = "SOSAIOT-TC-46992"
    description = show_testcase_info(Parameter.TESTPLAN, '107', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '107')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {123},
                        "host_name": "123",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_108(Test):
    uuid = "SOSAIOT-TC-46993"
    description = show_testcase_info(Parameter.TESTPLAN, '108', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '108')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "192.2.3.5",
                            "port": 521
                        },
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_109(Test):
    uuid = "SOSAIOT-TC-46994"
    description = show_testcase_info(Parameter.TESTPLAN, '109', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '109')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "C0EAE4CCF5E8",
                        "encryption_type": "des-md5",
                        "encryption_key": "0cf224ea209c87c8",
                        "authentication_key": "ef1f180a865b552c052c3c0b295e2458",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"ipsec_tunnel"', "err:Failed to add gms")

class Admin_110(Test):
    uuid = "SOSAIOT-TC-46995"
    description = show_testcase_info(Parameter.TESTPLAN, '110', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {},
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_111(Test):
    uuid = "SOSAIOT-TC-46996"
    description = show_testcase_info(Parameter.TESTPLAN, '111', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '111')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "existing_tunnel": {
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"existing_tunnel"', "err:Failed to add gms")

class Admin_112(Test):
    uuid = "SOSAIOT-TC-46997"
    description = show_testcase_info(Parameter.TESTPLAN, '112', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '112')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 521
                        },
                        "host_name": "hello",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_113(Test):
    uuid = "SOSAIOT-TC-46998"
    description = show_testcase_info(Parameter.TESTPLAN, '113', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '113')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 521
                        },
                        "host_name": "111",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_114(Test):
    uuid = "SOSAIOT-TC-46999"
    description = show_testcase_info(Parameter.TESTPLAN, '114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '114')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_115(Test):
    uuid = "SOSAIOT-TC-47000"
    description = show_testcase_info(Parameter.TESTPLAN, '115', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '115')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 99999,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_116(Test):
    uuid = "SOSAIOT-TC-47001"
    description = show_testcase_info(Parameter.TESTPLAN, '116', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '116')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": "aaaa",
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_117(Test):
    uuid = "SOSAIOT-TC-47002"
    description = show_testcase_info(Parameter.TESTPLAN, '117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "11.1.1.1",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {
                            "ip": "2.2.2.2"
                        }
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_118(Test):
    uuid = "SOSAIOT-TC-47003"
    description = show_testcase_info(Parameter.TESTPLAN, '118', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '118')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "11.1.1.1",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {
                            "ip": "22222"
                        }
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_119(Test):
    uuid = "SOSAIOT-TC-47004"
    description = show_testcase_info(Parameter.TESTPLAN, '119', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '119')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "11.1.1.1",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {
                            "ip": "2.2.2.2"
                        }
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"https"', "err:Failed to add gms")

class Admin_120(Test):
    uuid = "SOSAIOT-TC-47005"
    description = show_testcase_info(Parameter.TESTPLAN, '120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1234",
                            "port": 521
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {
                            "ip": "2.2.2.2"
                        }
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_121(Test):
    uuid = "SOSAIOT-TC-47006"
    description = show_testcase_info(Parameter.TESTPLAN, '121', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '121')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "https": {
                        "reporting_server": {
                            "ip": "1.2.3.4",
                            "port": 66666
                        },
                        "host_name": "1.1.1.1",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {
                            "ip": "2.2.2.2"
                        }
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_123(Test):
    uuid = "SOSAIOT-TC-47007"
    description = show_testcase_info(Parameter.TESTPLAN, '123', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '123')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "aaa",
                        "encryption_type": "des-md5",
                        "encryption_key": "@@@",
                        "authentication_key": "ef1f180a865b552c052c3c0b295e2458",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_124(Test):
    uuid = "SOSAIOT-TC-47008"
    description = show_testcase_info(Parameter.TESTPLAN, '124', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '124')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "C0EAE4CCF5E8",
                        "encryption_type": "des-md5",
                        "encryption_key": "123456",
                        "authentication_key": "aa",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_125(Test):
    uuid = "SOSAIOT-TC-47009"
    description = show_testcase_info(Parameter.TESTPLAN, '125', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '125')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "aaa",
                        "encryption_type": "des-md5",
                        "encryption_key": "@@@",
                        "authentication_key": "ef1f180a865b552c052c3c0b295e2458",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_126(Test):
    uuid = "SOSAIOT-TC-47010"
    description = show_testcase_info(Parameter.TESTPLAN, '126', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '126')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "C0EAE4CCF5E8",
                        "encryption_type": "des-md5",
                        "encryption_key": "1234567891234567",
                        "authentication_key": "1111111111111111111111111111111",
                        "host_name": "mia",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_127(Test):
    uuid = "SOSAIOT-TC-47011"
    description = show_testcase_info(Parameter.TESTPLAN, '127', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '127')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_gms(self):
        admin_json = {
            "administration": {
                "gms_management": {
                    "ipsec_tunnel": {
                        "spi": "C0EAE4CCF5E8",
                        "encryption_type": "des-md5",
                        "encryption_key": "1234567891234567",
                        "syslog_server_port": 514,
                        "heartbeat_status_only": False,
                        "behind_nat_device": {}
                    }
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"gms_management": {"ipsec_tunnel"', "err:Failed to retrieve gms")

class Admin_129(Test):
    uuid = "SOSAIOT-TC-47012"
    description = show_testcase_info(Parameter.TESTPLAN, '129', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '129')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_language(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"language_override": {"english"', "err:Failed to retrieve language")

class Admin_130(Test):
    uuid = "SOSAIOT-TC-47013"
    description = show_testcase_info(Parameter.TESTPLAN, '130', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '130')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_language(self):
        admin_json = {
            "administration": {
                "language_override": {
                    "english": False
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_131(Test):
    uuid = "SOSAIOT-TC-47014"
    description = show_testcase_info(Parameter.TESTPLAN, '131', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '131')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_get_port_https(self):
        response = Admin_settings.show_admin_setting()
        logger.info(response)
        Assertion.assert_regular(json.dumps(response), '"https_port": 443', "err:Failed to retrieve language")

class Admin_132(Test):
    uuid = "SOSAIOT-TC-47015"
    description = show_testcase_info(Parameter.TESTPLAN, '132', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '132')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_port_https(self):
        admin_json = {
            "administration": {
                "https_port": 66666
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_133(Test):
    uuid = "SOSAIOT-TC-47016"
    description = show_testcase_info(Parameter.TESTPLAN, '133', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_port_https(self):
        admin_json = {
            "administration": {
                "https_port": "a"
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_136(Test):
    uuid = "SOSAIOT-TC-47019"
    description = show_testcase_info(Parameter.TESTPLAN, '136', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '136')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_port_https(self):
        admin_json = {
            "administration": {
                "ssh": {
                    "port": 66666
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

class Admin_137(Test):
    uuid = "SOSAIOT-TC-47020"
    description = show_testcase_info(Parameter.TESTPLAN, '137', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '137')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_put_port_https(self):
        admin_json = {
            "administration": {
                "ssh": {
                    "port": "a"
                }
            }
        }
        response = Admin_settings.conf_admin_update(**admin_json)
        logger.info(response)
        Assertion.assert_equal(response, False, "ERR: Unable to update")

def change_admin_password(pwd, new_pwd):
    try:
        hostname = static_pc
        username = "root"
        password = "password"

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, username=username, password=password)
        shell = client.invoke_shell()
        time.sleep(1)
        output = shell.recv(65535).decode('utf-8')
        logger.info(output)
        shell.send('ssh-keygen -R 192.168.168.168\n')
        time.sleep(2)
        shell.send('ssh admin@192.168.168.168\n')
        time.sleep(1)
        shell.send('yes\n')
        time.sleep(1)
        shell.send(pwd + '\n')
        time.sleep(1)
        commands = [
            'configure\n',
            'yes\n',
            'administration\n',
            'admin password old-password {} new-password {} confirm-password {}\n'.format(pwd, new_pwd, new_pwd),
            'exit\n'
        ]
        for command in commands:
            shell.send(command)
            time.sleep(1)

        output = shell.recv(65535).decode('utf-8')
        logger.info(output)
        client.close()
        return True

    except Exception as e:
        logger.info("Failed to change admin password.")
        logger.info(str(e))
        return False