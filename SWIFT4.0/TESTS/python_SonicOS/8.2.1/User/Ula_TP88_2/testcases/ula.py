from definition.settings import *
from definition.utils import *
from definition.firewall_configure import FWFunctionConfigure

fwconfigure = FWFunctionConfigure()


class TestConfigureULA(Test):
    uuid = 'NonTC'


    def test_00_ula_configure(self):
        output = fwconfigure.ula_configure()
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



class TC01_Access_the_Internet_from_the_Custom_Zone_allow_All(Test):
    uuid = "SOSAIOT-TC-75958"
    #jira = 'GEN8-5579'
      
    description = show_testcase_info(TESTPLAN, '1524249', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524200')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_not_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")



class TC02_Access_the_Internet_from_the_Custom_Zone_allow_Administrator(Test):
    uuid = "SOSAIOT-TC-75959"
    # jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524250', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524250')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
        output = fwconfigure.logout_users()
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
        

class TC03_Access_the_Internet_from_the_Custom_Zone_allow_Everyone(Test):
    uuid = "SOSAIOT-TC-75960"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524251', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524251')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
        output = fwconfigure.logout_users()
        



class TC04_Access_the_Internet_from_the_Custom_Zone_allow_a_group(Test):
    uuid = "SOSAIOT-TC-75961"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524252', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524252')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user user_test1 ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'user_test1', "err:Failed to logout")
       


class TC05_Access_the_Internet_from_the_Custom_Zone_allow_a_supergroup(Test):
    uuid = "SOSAIOT-TC-75962"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524253', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524253')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
      


class TC06_Access_the_Internet_from_the_LAN_allow_Administrator(Test):
    uuid = "SOSAIOT-TC-75963"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524254', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524254')
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
                'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'LAN',
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
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin -pwd ' + f'{G_PASSWORD_NEW}'
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
       


class TC07_Access_the_Internet_from_the_Custom_Zone_allow_a_user(Test):
    uuid = "SOSAIOT-TC-75964"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524255', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524255')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
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
            'from': 'Custom_zone1',
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
       
class TC08_Deny_access_to_the_Internet_from_the_Custom_Zone(Test):
    uuid = "SOSAIOT-TC-75965"
    #jira = 'GEN8-5579'
    description = show_testcase_info(TESTPLAN, '1524256', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524256')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
            'to': 'WAN',
            'action': 'deny',
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
            'from': 'Custom_zone1',
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
        Assertion.assert_not_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")



class TC09_Access_the_Internet_from_the_LAN_allow_Everyone(Test):
    uuid = "SOSAIOT-TC-75968"
    #jira = 'GEN8-5579'

    description = show_testcase_info(TESTPLAN, '1524265', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524265')
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
            'user_included': {"group": "Everyone"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        #output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")


class TC10_Access_the_Internet_from_the_LAN_allow_a_group(Test):
    uuid = "SOSAIOT-TC-75970"
    
    description = show_testcase_info(TESTPLAN, '1524276', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524276')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_access_rule(self):
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
            'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()

    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user user_test1 ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'user_test1', "err:Failed to logout")
       
   

class TC11_Access_the_Internet_from_the_LAN_allow_a_supergroup(Test):
    uuid = "SOSAIOT-TC-75972"
    description = show_testcase_info(TESTPLAN, '1524287', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524287')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
            'user_included': {"group": "SonicWALL Administrators"}
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
           'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin ' + '-pwd ' + f'{G_PASSWORD_NEW}'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
        
class TC12_Acceptable_Use_Policy_is_displayed_on_login_from_the_LAN(Test):
    uuid = "SOSAIOT-TC-76000"
    description = show_testcase_info(TESTPLAN, '1524316', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524316')
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
            'user_included': {"group": "Everyone"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k --connect-timeout 10 --max-time 15']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")
class TC13_Acceptable_Use_Policy_is_displayed_on_login_from_the_WAN(Test):
    uuid = "SOSAIOT-TC-76001"
    description = show_testcase_info(TESTPLAN, '1524317', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524317')
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
            'user_included': {"group": "Everyone"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k --connect-timeout 10 --max-time 15']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")


class TC14_Acceptable_Use_Policy_is_displayed_on_login_from_the_Custom_Zone(Test):
    uuid = "SOSAIOT-TC-76004"
    description = show_testcase_info(TESTPLAN, '1524321', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524321')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        name = "ula_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('Custom_zone1', 'WAN')
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
            'from': 'Custom_zone1',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group": "Everyone"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_02_add_access_rule(self):
        access_rule_option = {
            'name': 'ULA Rule2',
            'from': 'Custom_zone1',
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
        PC3_login.send_command('pkill firefox')
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k --connect-timeout 10 --max-time 15']
        output = PC3_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")




class TC15_User_attempts_to_bypass_Acceptable_Use_Policy(Test):
    uuid = "SOSAIOT-TC-76005"
    description = show_testcase_info(TESTPLAN, '1524322', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524322')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
       

class TC16_Acceptable_Use_Policy_preview(Test):
    uuid = "SOSAIOT-TC-76006"
    description = show_testcase_info(TESTPLAN, '1524323', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524323')
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
            'user_included': {"group": "Everyone"}
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

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
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k --connect-timeout 10 --max-time 15']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")





class TC17_Login_session_limit_changed_by_administrator(Test):
    uuid = "SOSAIOT-TC-75992"
    description = show_testcase_info(TESTPLAN, '1524308', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524308')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_01_add_access_rule(self):
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
            'user_included': {"group": "Everyone"}
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
           'user_included': {"group": "SonicWALL Administrators"}
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        output = fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user admin -pwd sonicauto'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'admin', "err:Failed to logout")
       
   



class TC18_User_Logout_select_the_Logout_button(Test):
    uuid = "SOSAIOT-TC-75973"
    description = show_testcase_info(TESTPLAN, '1524288', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524288')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")
class TC19_User_Logout_check_logs(Test):
    uuid = "SOSAIOT-TC-75974"
    description = show_testcase_info(TESTPLAN, '1524289', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524289')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


class TC20_Cancel_logout(Test):
    uuid = "SOSAIOT-TC-75975"
    description = show_testcase_info(TESTPLAN, '1524290', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524290')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC21_User_logout_by_administrator(Test):
    uuid = "SOSAIOT-TC-75976"
    description = show_testcase_info(TESTPLAN, '1524291', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524291')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC22_Cancel_logout(Test):
    uuid = "SOSAIOT-TC-75975"
    description = show_testcase_info(TESTPLAN, '1524290', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524290')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

class TC23_Relogin_after_logout(Test):
    uuid = "SOSAIOT-TC-75977"
    description = show_testcase_info(TESTPLAN, '1524292', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524292')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


class TC24_User_Logout_Inactivity_timer_expired(Test):
    uuid = "SOSAIOT-TC-75978"
    description = show_testcase_info(TESTPLAN, '1524293', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524293')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")




class TC25_Inactivity_timer_is_reset_by_selecting_click_here_in_the_warning_message(Test):
    uuid = "SOSAIOT-TC-75979"
    description = show_testcase_info(TESTPLAN, '1524294', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524294')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")





class TC26_Inactivity_timer_is_reset_by_generating_traffic(Test):
    uuid = "SOSAIOT-TC-75980"
    description = show_testcase_info(TESTPLAN, '1524295', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524295')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")







class TC27_Login_session_limit_changed_by_user(Test):
    uuid = "SOSAIOT-TC-75994"
    description = show_testcase_info(TESTPLAN, '1524310', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524310')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")






class TC28_Login_session_unlimited_by_administrator(Test):
    uuid = "SOSAIOT-TC-75995"
    description = show_testcase_info(TESTPLAN, '1524311', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524311')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")






class TC29_Deny_access_to_the_Internet_from_the_LAN(Test):
    uuid = "SOSAIOT-TC-75993"
    description = show_testcase_info(TESTPLAN, '1524309', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524309')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


class TC30_Login_session_limited_by_user(Test):
    uuid = "SOSAIOT-TC-75996"
    description = show_testcase_info(TESTPLAN, '1524312', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524312')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


class TC31_user_status_page_logout_selected_users(Test):
    uuid = "SOSAIOT-TC-75953"
    description = show_testcase_info(TESTPLAN, '1524244', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524244')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
   
    def test_01_add_access_rule(self):
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
           'user_included': {"group": "group1"},
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
        output = fwconfigure.logout_users()


    @repeat_method(5)
    def test_02_check_ula_function(self):
        
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url='https://12.12.1.40'
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_2/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC3_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")