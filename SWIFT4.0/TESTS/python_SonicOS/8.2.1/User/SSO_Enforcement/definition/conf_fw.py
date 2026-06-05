from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'

    def test_01_Set_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'dns3': Parameter.X1_DNS3,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    
    def test_02_Set_X2_Interface(self):
        x2_static = {
            'if': 'x2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")
    
    @repeat_method(5)
    def test_03_register_fw(self):
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
    
    def test_04_edit_dmz_to_lan(self):
        rule = accessrule.get_ipv4_access_rule_given_from_to('DMZ', 'LAN')
        rule['access_rules'][0]['ipv4']['action'] = 'allow'
        uuid = rule['access_rules'][0]['ipv4']['uuid']
        resp = accessrule.edit_ipv4_access_rule_by_uuid(uuid, **rule)
        Assertion.assert_equal(resp, True, 'ERR: Failed to update access rule.')

    def test_05_edit_dhcp_server_dynamic_scope(self):
        res = False
        x0_dhcp_scope = copy.deepcopy(dynamic_scope_base)
        x0_dhcp_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            x0_dhcp_edit_dict1)
        addres = dhcpserverapi.edit_dhcp_server_scope_v4(scope='dynamic', p1='192.168.168.1', p2='192.168.168.167', **x0_dhcp_scope)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if x0_dhcp_edit_dict1['from'] in str(output) else False
        else:
            logger.info('edit dhcp lease for x0 interface failed')
        Assertion.assert_equal(res, True, "ERR: Failed to edit dhcp server scope.")
    
    def test_06_add_dhcp_server_dynamic_scope(self):
        res = False
        x2_dhcp_scope = copy.deepcopy(dynamic_scope_base)
        x2_dhcp_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            x2_dhcp_dict)
        addres = dhcpserverapi.add_dhcp_server_scope_dynamic(**x2_dhcp_scope)
        if addres:
            output = dhcpserverapi.get_dhcp_server_scope_dynamic()
            logger.info(f"---- {output}")
            res = True if x2_dhcp_dict['from'] in str(
                output) else False
        else:
            logger.info('add dhcp lease for x2 interface failed')
        Assertion.assert_equal(
            res, True, "ERR: Failed to add dhcp server scope.")
