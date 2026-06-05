from definition.vpn_settings import *

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
    
    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
    
    def test_03_edit_dhcp_server_dynamic_scope(self):
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
    
    def test_04_remote_edit_dhcp_server_dynamic_scope(self):
        res = False
        x0_dhcp_scope = copy.deepcopy(dynamic_scope_base)
        x0_dhcp_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(
            r_x0_dhcp_edit_dict1)
        addres = r_dhcpserverapi.edit_dhcp_server_scope_v4(scope='dynamic', p1='172.16.1.102', p2='172.16.1.254', **x0_dhcp_scope)
        if addres:
            output = r_dhcpserverapi.get_dhcp_server_scope_dynamic()
            res = True if r_x0_dhcp_edit_dict1['from'] in str(output) else False
        else:
            logger.info('edit dhcp lease for x0 interface failed')
        Assertion.assert_equal(res, True, "ERR: Failed to edit dhcp server scope.")
    
    def test_05_remote_add_lan_vpn_acl(self):
        access_rule = {
            'name': 'Rule1',
            'from': 'LAN',
            'to': 'VPN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = r_accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")
    
    def test_06_remote_add_vpn_lan_acl(self):
        access_rule = {
            'name': 'Rule2',
            'from': 'VPN',
            'to': 'LAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True}
        }
        output = r_accessrule.add_ipv4_access_rule(**access_rule)
        Assertion.assert_equal(output, True, "ERR: Failed to add access rule")

    def test_07_Config_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN5 -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(Parameter.R_X1_IP)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')

        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    def test_08_Enable_Remote_FW_API(self):
        logger.info(" {} ".center(20, '-').format('Enable Remote Api Basic'))
        api_dict = {
            'sonicos-api': True,
            'basic': True,
        }
        rc = r_admin_cli.sonicos_api(**api_dict)
        if rc:
            logger.info('Success enable remote api basic')
        else:
            logger.info('Failed enable remote api basic')
        Assertion.assert_equal(rc, True, "ERR: Enable Remote FW basic API failed")
    
    def test_09_Add_Network_Obj(self):
        rc = address_objects.config_addressobject(**local_vpn_obj)
        rc &= address_objects_cli.add_address_group(**local_group)
        rc &= r_address_objects.config_addressobject(**remote_vpn_lan)
        rc &= r_address_objects.config_addressobject(**remote_lan_obj)
        rc &= r_address_objects_cli.add_address_group(**remote_group)
        Assertion.assert_equal(rc, True, "ERR: Add network AO failed")
        
    def test_10_Add_VPN_Policy(self):
        rc = r_vpn_cli.fw.do_cli_commands(remote_lan_vpn_cmds)
        rc &= vpn_cli.fw.do_cli_commands(local_lan_vpn_cmds)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")
    