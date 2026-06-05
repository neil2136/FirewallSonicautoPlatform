from definition.settings_vpn import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    
    def test_01_Set_X0_Interface(self):
        x1_static = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.FIREWALL,
            'gateway': Parameter.X0_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': False,
            'user_https': True,
            'https_redirect': True
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Set_X1_Interface(self):
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
            'user_http': False,
            'user_https': True,
            'https_redirect': True
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    
    def test_03_Set_X2_Interface(self):
        x2_static = {
            'if': 'x2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': False,
            'user_https': True,
            'https_redirect': True
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")
    
    @repeat_method(5)
    def test_04_register_fw(self):
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_05_Config_Remote_FW(self):
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

    def test_06_Enable_Remote_FW_API(self):
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
    
    def test_07_remote_add_lan_vpn_acl(self):
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
    
    def test_08_remote_add_vpn_lan_acl(self):
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
    
    def test_09_Add_Network_Obj(self):
        address_objects.del_all_address_object()
        rc = address_objects.config_addressobject(**local_vpn_obj)
        # rc &= address_objects_cli.add_address_group(**local_group)
        r_address_objects.del_all_address_object()
        rc &= r_address_objects.config_addressobject(**remote_vpn_lan)
        rc &= r_address_objects.config_addressobject(**local_vpn_obj)
        # rc &= r_address_objects_cli.add_address_group(**remote_group)
        Assertion.assert_equal(rc, True, "ERR: Add network AO failed")
        
    def test_10_Add_VPN_Policy(self):
        r_vpn_cli.delete_allvpnpolicy()
        rc = r_vpn_cli.fw.do_cli_commands(remote_lan_vpn_cmds)
        vpn_cli.delete_allvpnpolicy()
        rc &= vpn_cli.fw.do_cli_commands(local_lan_vpn_cmds)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")
    