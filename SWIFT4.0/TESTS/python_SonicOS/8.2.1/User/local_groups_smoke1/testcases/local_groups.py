import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/local_groups_smoke1')

from definition.initial_parameter import *

class TC04_delete_group(Test):
    uuid = "SOSAIOT-TC-75507"
    description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a group 'group1'
    def test_01_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1'
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # delete group1
    def test_02_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

class TC08_add_member_to_group(Test):
    uuid = "SOSAIOT-TC-75512"
    description = show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': 'S0nic@uto',
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
            'groupname': 'group1',
            'member_of': ['user_test1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not added to group1')

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

class TC09_multiple_members_to_group(Test):
    uuid = '1505254 '
    description = show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': 'S0nic@uto',
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

    # add user_test1, group1 to Sonicwall administrator
    def test_03_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['user_test1', 'group1']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not added to SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not added to SonicWALL Administrators')

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

class TC10_remove_member_from_group(Test):
    uuid = "SOSAIOT-TC-75498"
    description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': 'S0nic@uto',
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

    # add user_test1 to group1
    def test_03_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': 'S0nic@uto',
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: user_test1 not added to group')

    # remove user from group
    def test_04_remove_user(self):
        member_json = {
            'groupname': 'group1',
            'members': ['user_test1']
        }
        resp = user.delete_members_from_group(**member_json)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not removed from group1')

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

class TC11_remove_multiple_members_from_group(Test):
    uuid = "SOSAIOT-TC-75499"
    description = show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a user 'user_test1'
    def test_01_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': 'S0nic@uto',
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')

    # create a user 'user_test2'
    def test_02_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test2',
            'userpassword': 'S0nic@uto',
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test2"', 'err: user_test2 not created')

    # create a group 'group1'
    def test_03_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add users to group1
    def test_04_add_users(self):
        member = {
            'action': 'add',
            'groupname': 'group1',
            'member_of': ['user_test1','user_test2']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not added')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test2"', 'err: user_test2 not added')

    # remove users from group1
    def test_05_remove_user(self):
        member_json = {
            'groupname': 'group1',
            'members': ['user_test1', 'user_test2']
        }
        resp = user.delete_members_from_group(**member_json)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not removed')
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test2"', 'err: user_test2 not removed')

    # del group1
    def test_06_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

    # del user_test1
    def test_07_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')

    # del user_test2
    def test_08_del_user(self):
        resp = user.delete_local_user_no_domain('user_test2')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test2"', 'err: user_test2 not deleted')

class TC12_add_vpn_access_client(Test):
    uuid = "SOSAIOT-TC-75500"
    description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
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
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group not created')

    # add vpn access client
    def test_02_add_vpn_client(self):
        vpn = {
            'action': 'add',
            'groupname': 'group1',
            'vpn_client_access': [{"name": "X0 Subnet"}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "X0 Subnet"', 'err: vpn client not added')

    # del group1
    def test_03_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

class TC13_add_multiple_vpn_access_client(Test):
    uuid = "SOSAIOT-TC-75501"
    description = show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
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

    # add multiple network objetcs to vpn access client
    def test_02_add_vpn_client(self):
        vpn = {
            'action': 'add',
            'groupname': 'group1',
            'vpn_client_access': [{'group': 'LAN Subnets'}, {'group': 'WLAN Subnets'}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"group": "LAN Subnets"', 'err: LAN Subnets not added')
        Assertion.assert_regular(json.dumps(resp1), '"group": "WLAN Subnets"', 'err: WLAN Subnets not added')

class TC14_remove_vpn_access_client(Test):
    uuid = "SOSAIOT-TC-75502"
    description = show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # remove vpn access client
    def test_01_remove_vpn_client(self):
        vpn = {
            'action': 'delete',
            'groupname': 'group1',
            'vpn_client_access': [{"group": "LAN Subnets"}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_not_regular(json.dumps(resp1), '"group": "LAN Subnets"', 'err: LAN Subnets not removed')

    # del group1
    def test_02_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

class TC15_remove_multiple_vpn_access_client(Test):
    uuid = "SOSAIOT-TC-75503"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
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

    # add multiple network objects to vpn access client
    def test_02_add_vpn_client(self):
        vpn = {
            'action': 'add',
            'groupname': 'group1',
            'vpn_client_access': [{'group': 'LAN Subnets'}, {'group': 'WLAN Subnets'}, {'group': 'DMZ Subnets'}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_regular(json.dumps(resp1), '"group": "LAN Subnets"', 'err: LAN Subnets not added')
        Assertion.assert_regular(json.dumps(resp1), '"group": "WLAN Subnets"', 'err: WLAN Subnets not added')
        Assertion.assert_regular(json.dumps(resp1), '"group": "DMZ Subnets"', 'err: DMZ Subnets not added')

    # remove multiple network objects from vpn access client
    def test_03_remove_vpn_client(self):
        vpn = {
            'action': 'delete',
            'groupname': 'group1',
            'vpn_client_access': [{'group': 'LAN Subnets'}, {'group': 'WLAN Subnets'}]
        }
        resp = user.group_vpn_client_access(**vpn)
        resp1 = user.show_local_group_by_name('group1')
        Assertion.assert_not_regular(json.dumps(resp1), '"group": "LAN Subnets"', 'err: LAN Subnets not removed')
        Assertion.assert_not_regular(json.dumps(resp1), '"group": "WLAN Subnets"', 'err: WLAN Subnets not removed')

    # del group1
    def test_04_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

class TC26_add_group(Test):
    uuid = "SOSAIOT-TC-75504"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
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

    # del group1
    def test_02_del_group(self):
        resp = user.delete_local_group_no_domain('group1')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not deleted')

