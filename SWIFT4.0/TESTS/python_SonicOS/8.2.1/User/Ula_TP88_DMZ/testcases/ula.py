from definition.settings import *
from definition.utils import *
from definition.firewall_configure import FWFunctionConfigure

fwconfigure = FWFunctionConfigure()


class TestConfigureULA(Test):
    uuid = 'NonTC'


    def test_00_ula_configure(self):
        output = fwconfigure.ula_configure()
        Assertion.assert_equal(output, True, "ERR: ula configure failed")
        output = fwconfigure.create_user()
        output = fwconfigure.create_group()
        output = fwconfigure.add_user()
        output = fwconfigure.add_group()
        output = fwconfigure.create_user2()
        output = fwconfigure.create_group2()
        output = fwconfigure.add_user2()
    
        
    def test_01_check_local_user_configure(self):
        output = userLocalapi.show_local_user_by_name(name=CaseParams.ula_user_name)
        Assertion.assert_regular(json.dumps(output), 'LAN Subnets', "ERR: check local user configure failed")



class TC01_Access_the_Internet_from_the_DMZ_allow_Everyone(Test):
    uuid = "SOSAIOT-TC-75911"
    jira = 'GEN8-5579'
      
    description = show_testcase_info(TESTPLAN, '1524194', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524194')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_add_access_rule(self):
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

    def test_02_add_access_rule(self):
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
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        #output = fwconfigure.logout_users()
        
        #.assert_not_regular(out, 'Exception', "Failed to to verify admin preempt")



class TC02_Access_the_Internet_from_the_DMZ_allow_a_group(Test):
    uuid = "SOSAIOT-TC-75920"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524205', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524205')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_add_access_rule(self):
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
            'user_included': {"group": "group1"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
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
        output = fwconfigure.logout_users()

    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user user_test1 ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'user_test1', "err:Failed to logout")
       
   


class TC03_Access_the_Internet_from_the_DMZ_allow_a_super_group(Test):
    uuid = "SOSAIOT-TC-75926"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524216', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524216')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_add_access_rule(self):
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
            'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
           'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
        


class TC04_Access_the_Internet_from_the_DMZ_allow_a_user(Test):
    uuid = "SOSAIOT-TC-75937"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524227', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524227')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_add_access_rule(self):
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
            'user_included': {"name": "auto_ula_test"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
       



class TC05_Deny_access_to_the_Internet_from_the_DMZ(Test):
    uuid = "SOSAIOT-TC-75947"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524238', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524238')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
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
            'action': 'deny',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Trusted Users"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'deny',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        time.sleep(10)
        
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")



class TC06_Login_Redirect_upon_the_Internet_access_from_the_DMZ(Test):
    uuid = "SOSAIOT-TC-75988"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524303', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524303')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
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
            'user_included': {"group": "Trusted Users"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")



class TC07_Acceptable_Use_Policy_is_displayed_on_login_from_the_DMZ(Test):
    uuid = "SOSAIOT-TC-76002"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524318', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524318')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")


class TC08_Access_the_Internet_from_the_DMZ_allow_All(Test):
    uuid = "SOSAIOT-TC-76003"
    jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524320', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524320')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
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
            'user_included': {"all": True},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        time.sleep(10)
        
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_not_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")



class TC09_Access_the_Internet_from_the_DMZ_allow_Administrator(Test):
    uuid = "SOSAIOT-TC-76014"
    jira = 'GEN8-5579'

    description = show_testcase_info(TESTPLAN, '1524331', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524331')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
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
            'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'DMZ',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
           'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        #output = fwconfigure.logout_users()
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_DMZ/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
       


class TC10_user_authentication_settings_check_default_settings(Test):
    uuid = "SOSAIOT-TC-76017"
    
    description = show_testcase_info(TESTPLAN, '1524334', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524334')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  
    def test_01_get_default_settings(self):
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"http_redirect_after_login": true', "ERR:Failed to select Local authentication method.")
           

class TC11_user_authentication_settings_enable_Case_sensitive_user_names(Test):
    uuid = "SOSAIOT-TC-76018"
    description = show_testcase_info(TESTPLAN, '1524335', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524335')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_enable_case_sensitive(self):
        user_auth =  {
        'case_sensitive_names': True,
        'login_uniqueness': False,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"case_sensitive_names": true',
                                 "ERR:Failed to select Local authentication method.")

class TC12_user_authentication_settings_disable_enable_Case_sensitive_user_names(Test):
    uuid = "SOSAIOT-TC-76019"
    description = show_testcase_info(TESTPLAN, '1524336', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524336')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_disable_case_sensitive(self):
        user_auth =  {
        'case_sensitive_names': False,
        'login_uniqueness': False,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"case_sensitive_names": false',
                                 "ERR:Failed to select Local authentication method.")

class TC13_user_authentication_settings_enable_Enforce_login_uniqueness(Test):
    uuid = "SOSAIOT-TC-76020"
    description = show_testcase_info(TESTPLAN, '1524337', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524337')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_enable_Enforce_login_uniqueness(self):
        
        user_auth =  {
        'case_sensitive_names': False,
        'login_uniqueness': True,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"login_uniqueness": true',
                                 "ERR:Failed to select Local authentication method.")



class TC14_user_authentication_settings_disable_Enforce_login_uniqueness(Test):
    uuid = "SOSAIOT-TC-76021"
    description = show_testcase_info(TESTPLAN, '1524338', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524338')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_disable_Enforce_login_uniqueness(self):
        
        user_auth =  {
        'case_sensitive_names': False,
        'login_uniqueness': False,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"login_uniqueness": false',
                                 "ERR:Failed to select Local authentication method.")




class TC15_user_authentication_settings_enable_Force_relogin_after_password_change(Test):
    uuid = "SOSAIOT-TC-76022"
    description = show_testcase_info(TESTPLAN, '1524339', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524339')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_Enable_Force_relogin_after_password_change(self):
        
        user_auth =  {
        'case_sensitive_names': False,
        'login_uniqueness': False,
        'relogin_after_password_change': True,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"relogin_after_password_change": true',
                                 "ERR:Failed to select Local authentication method.")





class TC16_user_authentication_settings_disable_Force_relogin_after_password_change(Test):
    uuid = "SOSAIOT-TC-76023"
    description = show_testcase_info(TESTPLAN, '1524340', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524340')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_disable_Force_relogin_after_password_change(self):
        
        user_auth =  {
        'case_sensitive_names': False,
        'login_uniqueness': False,
        'relogin_after_password_change': False,
        'method': 'local',
        'email_format': 'plain_text',
        'format': 'characters',
        'min': 10,
        'max': 10
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"relogin_after_password_change": false',
                                 "ERR:Failed to select Local authentication method.")





class TC17_user_authentication_settings_enable_Display_user_login_info_since_last_login(Test):
    uuid = "SOSAIOT-TC-76024"
    description = show_testcase_info(TESTPLAN, '1524341', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524341')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    
  
    def test_01_enable_display_login_info(self):
        logger.info('Select local authentication method....')
        user_auth = {

            "display_login_info": True
        }

        user_setting.user_authentication(**user_auth)
        resp = user_setting.show_user_setting()
        Assertion.assert_regular(json.dumps(resp), '"display_login_info": true',
                                 "ERR:Failed to select Local authentication method.")
