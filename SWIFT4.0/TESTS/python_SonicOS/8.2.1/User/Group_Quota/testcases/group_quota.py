import sys
import os
import json
import re

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/')

from definition.initial_parameter import *

class TC01_default_group_quota(Test):
    uuid = "SOSAIOT-TC-94223"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_default_group_quota(self):
        resp = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp), '"name": "Group Quota"', 'err: default group quota not available')

class TC02_delete_group_quota(Test):
    uuid = "SOSAIOT-TC-94234"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_group_quota(self):
        resp = user.delete_local_group_with_domain('Group Quota', 'any')
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "Group Quota"', 'err: failed.')

class TC03_edit_group_quota(Test):
    uuid = "SOSAIOT-TC-94245"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_edit_group(self):
        group_json = {
            'action': 'edit',
            'groupname': 'Group Quota',
            'grouptype': 'domaingroup',
            'domainname': 'any',
            'one_time_password': 'otp'
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '{"otp": true}', 'err: group quota not edited')

    # check default values disabled
    def test_02_check_default(self):
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '"session_lifetime": {}, "limit": {"receive": 0, "transmit": 0}', 'err: default values not disabled')

class TC08_custom_quota(Test):
    uuid = '5002A02-B195-11EB-B440-4612A51B9B85 '
    description = show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a group 'group1'
    def test_01_custom_quota(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'custom quota',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"', 'err: custom quota not created')

    # edit group quota
    def test_02_edit_group_quota(self):
        group_json = {
            'action': 'edit',
            'groupname': 'Group Quota',
            'grouptype': 'domaingroup',
            'domainname': 'any',
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 2,
            'transmit': 1
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '"minutes": 1', 'err: group quota not edited')
        Assertion.assert_regular(json.dumps(resp1), '"receive": 2, "transmit": 1', 'err: group quota not edited')

    # add custom quota to Group Quota
    def test_03_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'Group Quota',
            'domain': 'any',
            'member_of': ['custom quota']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"',
                                 'err: custom quota not added to Group Quota')

    # check custom quota
    def test_04_check_custom_quota(self):
        resp1 = user.show_local_group_by_name('custom quota')
        Assertion.assert_regular(json.dumps(resp1), '"minutes": 1', 'err: custom quota not updated ')
        Assertion.assert_regular(json.dumps(resp1), '"receive": 2, "transmit": 1', 'err: custom quota not updated')

    # disable all the values
    def test_05_disable(self):
        group_json = {
            'action': 'edit',
            'groupname': 'Group Quota',
            'grouptype': 'domaingroup',
            'domainname': 'any',
            'session_lifetime': True,
            'userquotalimit': True,
            'receivelimit': 0,
            'transmit': 0
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '"session_lifetime": {}', 'err: group quota not disabled')
        Assertion.assert_regular(json.dumps(resp1), '"receive": 0, "transmit": 0', 'err: group quota not disabled')

    # delete custom quota
    def test_06_delete_group_quota(self):
        resp = user.delete_local_group_no_domain('custom quota')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "custom quota"', 'err: custom quota not deleted')

class TC26_check_user_status(Test):
    uuid = '5002A02-B195-11EB-B440-4612A51B9B85 '
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # create a group 'custom quota'
    def test_01_custom_quota(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'custom quota',
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"', 'err: custom quota not created')

    # add custom quota to Group Quota
    def test_02_add_group(self):
        member = {
            'action': 'add',
            'groupname': 'Group Quota',
            'domain': 'any',
            'member_of': ['custom quota']
        }
        resp = user.group_member_of(**member)
        resp1 = user.show_local_group_by_name('Group Quota')
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"',
                                 'err: custom quota not added to Group Quota')

    # create a user 'user_test1'
    def test_03_create_user(self):
        user_json = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': 'sonicwall',
        }
        resp = user.local_user(**user_json)
        resp1 = user.show_local_users()
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')


    # edit custom quota
    def test_04_edit_group_quota(self):
        group_json = {
            'action': 'edit',
            'groupname': 'custom quota',
            'grouptype': 'locally_only',
            'quota_cycle': 'day',
            'session_lifetime': True,
            'sessionlifetimetype': 'minutes',
            'sessionlifetime': 1,
            'userquotalimit': True,
            'receivelimit': 2,
            'transmit': 2
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_group_by_name('custom quota')
        Assertion.assert_regular(json.dumps(resp1), '"quota_cycle": {"day": true}', 'err: group quota not edited')
        Assertion.assert_regular(json.dumps(resp1), '"minutes": 1', 'err: group quota not edited')
        Assertion.assert_regular(json.dumps(resp1), '"receive": 2, "transmit": 2', 'err: group quota not edited')

    # add user_test1 to 'custom quota'
    def test_05_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': 'sonicwall',
            'member_of': ['Trusted Users', 'Everyone', 'custom quota']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"', 'err: user_test1 not added to custom quota')

    # check custom quota
    def test_06_check_user(self):
        resp1 = user_status.show_local_users_quota_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"group_quota_type": "Per day"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"group_max_session": "1 Minute"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"group_max_rx": "2 MB"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"rem_rx": "2 MB"', 'err: user not updated')

    # edit custom quota
    def test_07_edit_group_quota(self):
        group_json = {
            'action': 'edit',
            'groupname': 'custom quota',
            'grouptype': 'locally_only',
            'quota_cycle': 'month',
            'session_lifetime': True,
            'sessionlifetimetype': 'hours',
            'sessionlifetime': 2,
            'userquotalimit': True,
            'receivelimit': 2000,
            'transmit': 2000
        }
        resp = user.local_group(**group_json)
        resp1 = user.show_local_group_by_name('custom quota')
        Assertion.assert_regular(json.dumps(resp1), '"quota_cycle": {"month": true}', 'err: group quota not edited')
        Assertion.assert_regular(json.dumps(resp1), '"hours": 2', 'err: group quota not edited')
        Assertion.assert_regular(json.dumps(resp1), '"receive": 2000, "transmit": 2000', 'err: group quota not edited')

    # add user_test1 to 'custom quota'
    def test_08_add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': 'sonicwall',
            'member_of': ['Trusted Users', 'Everyone', 'custom quota']
        }
        resp = user.user_member_of(**member)
        resp1 = user.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "custom quota"',
                                 'err: user_test1 not added to custom quota')

    # check custom quota
    def test_09_check_user(self):
        resp1 = user_status.show_local_users_quota_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"group_quota_type": "Per month"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"group_max_session": "2 hours"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"group_max_rx": "2000 MB"', 'err: user not updated')
        Assertion.assert_regular(json.dumps(resp1), '"rem_rx": "2000 MB"', 'err: user not updated')

    # delete custom quota
    def test_10_delete_group_quota(self):
        resp = user.delete_local_group_no_domain('custom quota')
        resp1 = user.show_local_groups()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "custom quota"', 'err: custom quota not deleted')

    # del user_test1
    def test_11_del_user(self):
        resp = user.delete_local_user_no_domain('user_test1')
        resp1 = user.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not deleted')
