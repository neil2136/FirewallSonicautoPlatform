import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2')

from definition.initial_parameter import *

class TC28_add_full_management_capabilities(Test):
    uuid = "SOSAIOT-TC-75395"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': G_PASSWORD_NEW,
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')

    # create a group 'group1'
    def test_02_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            # 'one_time_password': 'otp'
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add user_test1 to group1
    def test_03_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: user_test1 not added to group1')

    # add group1 to Sonicwall administrator
    def test_04_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['group1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not added to SonicWALL Administrators')

    # add a access rule and include only 'SonicWALL Administrators'
    def test_05_add_access_rule(self):
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
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"', 'err: access rules not updated.')

    @repeat_method(5)
    def test_06_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + \
              '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('user_test1')
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")

    # logout user
    def test_07_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC29_remove_full_management_capabilities(Test):
    uuid = "SOSAIOT-TC-75395"
    description = show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # remove group1 from Sonicwall administrator
    def test_01_remove_group(self):
        member_json = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'members': ['group1']
        }
        resp = user.delete_members_from_group(**member_json)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not removed')

    @repeat_method(5)
    def test_02_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + \
              '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "user_test1"', 'failed to get user status') 

    # logout user
    def test_03_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    # del group1
    def test_04_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

    # del user_test1
    def test_05_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')

class TC30_add_read_only_management_capabilities(Test):
    uuid = "SOSAIOT-TC-75505"
    description = show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': G_PASSWORD_NEW,
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')

    # create a group 'group1'
    def test_02_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add user to group1
    def test_03_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: user_test1 not added to group1')

    # add group1 to SonicWALL Read-Only Admins
    def test_04_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Read-Only Admins',
            'domain': 'any',
            'member_of': ['group1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('SonicWALL Read-Only Admins')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not added')

    # add a access rule and include only 'SonicWALL Read-Only Admins'
    def test_05_add_access_rule(self):
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
            'user_included': {"group": "SonicWALL Read-Only Admins"},
        }
        resp = access_rules.edit_ipv4_access_rule_uuid(uuid, **rule)
        resp1 = access_rules.get_ipv4_access_rule_by_uuid(uuid)
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Read-Only Admins"', 'err: access rules not updated.')

    @repeat_method(5)
    def test_06_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('user_test1')
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_07_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC31_remove_read_only_management_capabilities(Test):
    uuid = "SOSAIOT-TC-75506"
    description = show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # remove group1 from SonicWALL Read-Only Admins
    def test_01_remove_group(self):
        member_json = {
            'groupname': 'SonicWALL Read-Only Admins',
            'domain': 'any',
            'members': ['group1']
        }
        resp = user.delete_members_from_group(**member_json)
        resp1 = user.show_local_group_by_name('SonicWALL Read-Only Admins')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not removed')

    @repeat_method(5)
    def test_02_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "user_test1"', 'failed to get user status') 

    # logout user
    def test_03_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    # del group1
    def test_05_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

    # del user_test1
    def test_06_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')

class TC63_add_bookmark(Test):
    uuid = "SOSAIOT-TC-75508"
    description = show_testcase_info(Parameter.TESTPLAN, '63', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '63')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a group 'group1'
    def test_01_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add group1 to Sonicwall administrator
    def test_02_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SSLVPN Services',
            'domain': 'any',
            'member_of': ['group1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('SSLVPN Services')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not added to SSLVPN Services')

    # add bookmark1 to group1
    def test_03_add_bookmark(self):
        bookmark = {
            'action': 'edit',
            'groupname': 'group1',
            'bookmarkname': 'bookmark1',
            'bookmarkhost': '10.5.67.4'
        }
        resp = user.group_bookmark(**bookmark)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "bookmark1"', 'err: bookmark1 not added to group1')

class TC66_delete_bookmark(Test):
    uuid = "SOSAIOT-TC-75509"
    description = show_testcase_info(Parameter.TESTPLAN, '66', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # delete bookmark1 from group1
    def test_01_delete_bookmark(self):
        bookmark = {
            'action': 'delete',
            'groupname': 'group1',
            'bookmarkname': 'bookmark1',
            'bookmarkhost': '10.5.67.4'
        }
        resp = user.group_bookmark(**bookmark)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "bookmark1"', 'err: bookmark1 not deleted from group1')

    # del group1
    def test_02_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

class TC72_enable_to_management_on_login(Test):
    uuid = "SOSAIOT-TC-75510"
    description = show_testcase_info(Parameter.TESTPLAN, '72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': G_PASSWORD_NEW,
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')

    # create a group 'group1'
    def test_02_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            # 'one_time_password': 'otp'
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add user_test1 to group1
    def test_03_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: user_test1 not added to group1')

    # add group1 to Sonicwall administrator
    def test_04_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['group1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not added to SonicWALL Administrators')

    # enable to_management_on_login
    def test_05_enable(self):
        enable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': True
        }
        resp = user.group_administration_tab(**enable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": true', 'err: enable to_management_on_login failed.')

    # add a access rule and include only 'SonicWALL Administrators'
    def test_06_add_access_rule(self):
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
        Assertion.assert_regular(json.dumps(resp1), '"group": "SonicWALL Administrators"', 'err: access rules not updated.')

    @repeat_method(5)
    def test_07_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + \
              '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('user_test1')
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_08_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

class TC73_disable_to_management_on_login(Test):
    uuid = "SOSAIOT-TC-75511"
    description = show_testcase_info(Parameter.TESTPLAN, '73', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '73')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # disable to_management_on_login
    def test_01_disable(self):
        disable = {
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'to_management_on_login': False
        }
        resp = user.group_administration_tab(**disable)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), ' "to_management_on_login": false', 'err: disable to_management_on_login failed.')

    @repeat_method(5)
    def test_02_login(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://13.0.0.100"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke2/lib/ui_group.py ' + \
              '-url ' + url + ' -user user_test1 -pwd '+ G_PASSWORD_NEW +''
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        # check user status
        status = user_status.show_user_status_by_name('user_test1')
        resp = json.dumps(status)
        res = None 
        if '13.0.0.2' or '13.0.0.3' or '13.0.0.4' in resp:
            res = True
        Assertion.assert_equal(res, True, "ERR: failed to get user status")


    # logout user
    def test_03_logout(self):
        rc = user.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    # del user_test1
    def test_04_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')

class TC85_group_settings_in_TSR(Test):
    uuid = "SOSAIOT-TC-75513"
    description = show_testcase_info(Parameter.TESTPLAN, '85', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '85')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_00_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': G_PASSWORD_NEW,
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')

    # create a group 'group1'
    def test_00_02_create_group1(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add user to group1 and check tsr
    def test_00_03_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: user_test1 not added to group1')

        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('group1[\S\n ]+Members:.*user_test1', doc) else False
            Assertion.assert_equal(flag, True, "ERR: group1 config is incorrect")
            os.remove('/tmp/techSupport')

    # create a group 'group2'
    def test_00_04_create_group2(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group2',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group2"', 'err: group2 not created')

    # add group2 to Limited Administrators and check tsr
    def test_00_05_add_group2(self):
        member = {
            'action': 'add',
            'groupname': 'Limited Administrators',
            'domain': 'any',
            'member_of': ['group2']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('Limited Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group2"', 'err: group2 not added to Limited Administrators ')

        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('group2[\S\n ]+Group Memberships:.*Limited Administrators', doc) else False
            os.remove('/tmp/techSupport')
            Assertion.assert_equal(flag, True, "ERR: group2 config is incorrect")

    # create a group 'group3'
    def test_00_06_create_group3(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group3',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group3"', 'err: group3 not created')

    # add vpn access client access and check tsr
    def test_00_07_add_vpn_client(self):
        vpn = {
            'action': 'add',
            'groupname': 'group3',
            'vpn_client_access': [{"name": "X0 Subnet"}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group3')
        Assertion.assert_regular(json.dumps(resp1), '"name": "X0 Subnet"', 'err: vpn client access not added')

        output = diagnostic.download_tsr()
        with open('/tmp/techSupport', 'r') as tsr:
            doc = tsr.read()
            flag = True if re.search('group3[\S\n ]+VPN Client Networks:.*X0 Subnet', doc) else False
            os.remove('/tmp/techSupport')
            Assertion.assert_equal(flag, True, "ERR: group3 config is incorrect")

    # del group1
    def test_00_09_del_group1(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group not deleted')

    # del group2
    def test_00_10_del_group2(self):
        resp = user.delete_local_group_no_domain('group2')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group2"', 'err: group not deleted')

    # del group3
    def test_00_11_del_group3(self):
        resp = user.delete_local_group_no_domain('group3')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group3"', 'err: group not deleted')

    # del user_test1
    def test_00_12_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')

