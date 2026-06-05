from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_configure_x1_v4(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'gateway': Parameter.NATD_X0_IP
        }
        res = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_02_create_ao(self):
        rem_net_dict = {
            'object_type': 'network',
            'name': 'rem_sub_net',
            'zone': 'VPN',
            'value': '12.12.2.0,255.255.255.0'
        }
        res = ao_api.config_addressobject(**rem_net_dict)
        Assertion.assert_equal(res, True, 'ERR: add ao for remote subnet failed.')


class TestInit_NAT_Device(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(3)
    def test_01_init_nat_device(self):
        logger.info('======restore NAT Device======')
        cmd1 = f'python3 {restore_path} --testbed={Params.testbed} -device=RemoteGen_NAT_Device'
        pc1_login.send_command(cmd1)
        logger.info('======config NAT Device X1 interface======')
        cmd2 = f'python3 {cfg_if_path} --testbed={Params.testbed} -os=1 -device=RemoteGen_NAT_Device -if=X1 ' \
            f'-zone=WAN -ip={Parameter.NATD_X1_IP} -mgmt=True'
        pc1_login.send_command(cmd2)
        logger.info('======check NAT Device status======')
        res = pc1_login.ping(Parameter.NATD_X1_IP)
        Assertion.assert_equal(res, True, 'ERR: init nat device failed.')

    @repeat_method(3)
    def test_02_config_natd_xO(self):
        x0_dict = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.NATD_X0_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_nat_api.config_interface(**x0_dict)
        Assertion.assert_equal(res, True, 'ERR: config nat device x0 failed')

    @repeat_method(3)
    def test_03_add_wan_to_lan_acl(self):
        update_ping = {
            "name": "wan_to_lan_acl_ping",
            "service": {
                "group": "Ping"
            },
        }
        update_esp = {
            "name": "wan_to_lan_acl_esp",
            "service": {
                "name": "ESP (IPSec)"
            },
        }
        acl_ping = copy.deepcopy(acl_base_dict)
        acl_ping.update(update_ping)
        acl_esp = copy.deepcopy(acl_base_dict)
        acl_esp.update(update_esp)
        res1 = acl_nat_api.config_accessrule(**acl_ping)
        res2 = acl_nat_api.config_accessrule(**acl_esp)
        Assertion.assert_equal(res1 and res2, True, 'ERR: add wan to lan acl on nat device failed.')

    def test_04_add_ao(self):
        local_x1 = {
            'object_type': 'host',
            'name': 'local_fw_x1',
            'zone': 'WAN',
            'value': '172.16.1.168'
        }
        rem_x1 = {
            'object_type': 'host',
            'name': 'rem_fw_x1',
            'zone': 'WAN',
            'value': '12.12.1.102'
        }
        res1 = ao_nat_api.config_addressobject(**local_x1)
        res2 = ao_nat_api.config_addressobject(**rem_x1)
        Assertion.assert_equal(res1 and res2, True, 'ERR: add related aos on nat device failed.')

    def test_05_add_nat_rule(self):
        nat_dict = {"nat_policies": [{"ipv4": nat_base_dict}]}
        res = nat_dev_api.add_nat_policy(**nat_dict)
        Assertion.assert_equal(res, True, 'ERR: add related nat rule on nat device failed')


class TestInit_Rem_Device(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(3)
    def test_01_init_rem_device(self):
        logger.info('======restore Remote Device======')
        cmd1 = f'python3 {restore_path} -device=RemoteGenTZ270'
        pc1_login.send_command(cmd1)
        logger.info('======config Remote Device X1 interface======')
        cmd2 = f'python3 {cfg_if_path} --testbed={Params.testbed} -os=1 -device=RemoteGenTZ270 -if=X1 ' \
            f'-zone=WAN -ip={Parameter.REM_X1_IP} -mgmt=True'
        pc1_login.send_command(cmd2)
        logger.info('======check Remote Device status======')
        res = pc1_login.ping(Parameter.REM_X1_IP)
        Assertion.assert_equal(res, True, 'ERR: init nat device failed.')

    @repeat_method(3)
    def test_02_config_rem_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.REM_X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True
        }
        res = if_rem_api.config_interface(**x2_dict)
        Assertion.assert_equal(res, True, 'ERR: config remote device x2 failed')

    def test_03_create_local_fw_subnet(self):
        local_net = {
            'object_type': 'network',
            'name': 'local_sub_net',
            'zone': 'VPN',
            'value': '192.168.168.0,255.255.255.0'
        }
        res = ao_rem_api.config_addressobject(**local_net)
        Assertion.assert_equal(res, True, 'ERR: add local fw subnet on remote device failed.')

    def test_04_change_x0_subnet(self):
        x0_static = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.16.168',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_rem_api.config_interface(**x0_static)
        Assertion.assert_equal(res, True, 'ERR: config x0 interface on remote failed')
