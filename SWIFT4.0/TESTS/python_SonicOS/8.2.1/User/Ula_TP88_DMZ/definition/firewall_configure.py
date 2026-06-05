from definition.settings import *


class FWFunctionConfigure:

    def ula_configure(self):
        user_dict = {
            'action': 'add',
            'username': CaseParams.ula_user_name,
            'userpassword': G_PASSWORD_NEW,
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone'],
        }
        res, msg = userLocalapi.local_user(msg=True, **user_dict)
        if 'Already exists' in str(msg):
            res = True
        return res
    
    def create_user(self):
        user_dict = {
            'action': 'add',
            'username': 'user_test',
            'userpassword': G_PASSWORD_NEW,
        }
        res, msg = userLocalapi.local_user(msg=True, **user_dict)
        if 'Already exists' in str(msg):
            res = True
        return res
    # create a group 'group1'
    def create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group',
            # 'one_time_password': 'otp'
        }
        resp = userLocalapi.local_group(**group_json)
        resp1 = userLocalapi.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group"', 'err: group1 not created')

    # add user_test1 to group1
    def add_user(self):
        member = {
            'action': 'add',
            'username': 'user_test',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group']
        }
        resp = userLocalapi.user_member_of(**member)
        resp1 = userLocalapi.show_local_user_by_name('user_test')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group"', 'err: user_test1 not added to group1')

    # add group1 to Sonicwall administrator
    def add_group(self):
        member = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'domain': 'any',
            'member_of': ['group']
        }
        resp = userLocalapi.group_member_of(**member)
        resp1 = userLocalapi.show_local_group_by_name('SonicWALL Administrators')
        Assertion.assert_regular(json.dumps(resp1), '"name": "group"', 'err: group1 not added to SonicWALL Administrators')

    def create_user2(self):
        user_dict = {
            'action': 'add',
            'username': 'user_test1',
            'userpassword': G_PASSWORD_NEW,
        }
        res, msg = userLocalapi.local_user(msg=True, **user_dict)
        if 'Already exists' in str(msg):
            res = True
        return res
    # create a group 'group1'
    def create_group2(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            # 'one_time_password': 'otp'
        }
        resp = userLocalapi.local_group(**group_json)
        resp1 = userLocalapi.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    # add user_test1 to group1
    def add_user2(self):
        member = {
            'action': 'add',
            'username': 'user_test1',
            'password': G_PASSWORD_NEW,
            'member_of': ['Trusted Users', 'Everyone', 'group1']
        }
        resp = userLocalapi.user_member_of(**member)
        resp1 = userLocalapi.show_local_user_by_name('user_test1')
        Assertion.assert_regular(json.dumps(resp1), '"name": "user_test1"', 'err: user_test1 not created')
    def logout_users(self):
        rc = userLocalapi.logout_all_users()
        Assertion.assert_equal(rc, True, "ERR: logout user failed")

    def deny_access_rule(self):
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

    def deny_access_rule2(self):
        
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
