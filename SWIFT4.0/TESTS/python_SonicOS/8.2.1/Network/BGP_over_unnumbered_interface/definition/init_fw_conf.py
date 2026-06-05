from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_x2(self):
        x2_wan_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X2_GW,
            # 'dns1': Parameter.X1_DNS1,
            # 'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_config_X3(self):
        x3_lan_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x3 interface... ")
        rc = interfacev4api.config_interface(**x3_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_04_config_X4(self):
        x4_lan_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x4 interface... ")
        rc = interfacev4api.config_interface(**x4_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static failed")

    def test_05_add_remote_x0_ao_on_local_dut(self):
        remote_x0_subnet = {
            'name': 'remote_x0_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X0_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x0_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    def test_06_add_remote_x3_ao_on_local_dut(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    def test_07_create_vlan_interface_on_local_and_remote_dut(self):
        l_x0_vlan10_static = {
            'if': 'X0',
            'type': 'vlan',
            # 'vlan_tag': UTM_X4_VLAN1_ID,
            'vlan_tag': 10,
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.169.168',
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.DNS1,
            # 'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacev4api.add_interface(**l_x0_vlan10_static)
        Assertion.assert_equal(res, True, "ERR: Config X0 sub vlan interface on local dut failed")

    def test_08_add_remote_x0_vlan_ao_on_local_dut(self):
        remote_x0_subnet = {
            'name': 'remote_x0_vlan_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X0_REMOTE_VLAN_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x0_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote x0 vlan ao on local dut failed")

    @repeat_method(5)
    def test_09_register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestInitRemoteConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_init_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command1 = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X1 -zone=WAN ' \
                   f'-ip={Parameter.X1_REMOTE_IP} -restore=1 '
        confres = PC1_Login.send_command(command1)
        logger.info(confres)
        pingres = PC1_Login.ping_from_eth(ip=Parameter.X0_REMOTE_IP, eth='eth2')
        Assertion.assert_equal(pingres, True, "ERR: Restore Remote FW failed")

    def test_02_add_local_x0_network_ao_on_remote_dut(self):
        remote_x0_subnet = {
            'name': 'remote_x0_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X0_SUBNET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x0_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x0 network ao on remote dut failed")

    def test_03_config_X2(self):
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_REMOTE_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = r_interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_04_config_X3(self):
        x3_lan_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_REMOTE_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x3 interface... ")
        rc = r_interfacev4api.config_interface(**x3_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_05_config_X4(self):
        x4_lan_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_REMOTE_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x4 interface... ")
        rc = r_interfacev4api.config_interface(**x4_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static failed")

    def test_06_create_vlan_interface_on_local_and_remote_dut(self):
        r_x0_vlan10_static = {
            'if': 'X0',
            'type': 'vlan',
            'vlan_tag': 10,
            'zone': 'LAN',
            'mode': 'static',
            'ip': '172.16.2.101',
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = r_interfacev4api.add_interface(**r_x0_vlan10_static)
        Assertion.assert_equal(res, True, "ERR: Config X0 sub vlan interface on remote dut failed")

    def test_07_add_local_x0_network_ao_on_remote_dut(self):
        remote_x0_vlan_subnet = {
            'name': 'remote_x0_vlan_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X0_VLAN_SUBNET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x0_vlan_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x0 network ao on remote dut failed")

    def test_08_add_remote_x3_ao_on_remote_dut(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_SUBNET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")
