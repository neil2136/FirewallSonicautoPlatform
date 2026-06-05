from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': PC3_ETH1_IP,
            'dns2': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_Config_X3(self):
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

    def test_04_add_remote_ao_on_local_dut(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    @repeat_method(3)
    def test_05_register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestInitRemoteConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Init_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command1 = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X1 -zone=WAN ' \
                   f'-ip={Parameter.X1_REMOTE_IP} -restore=1 '
        confres = PC1_Login.send_command(command1)
        logger.info(confres)
        pingres = PC1_Login.ping_from_eth(ip=Parameter.X0_REMOTE_IP, eth='eth2')
        Assertion.assert_equal(pingres, True, "ERR: Restore Remote FW failed")

    def test_02_add_local_x2_network_ao_on_remote_dut(self):
        remote_x2_subnet = {
            'name': 'remote_x2_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X2_SUBNET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x2_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x0 network ao on remote dut failed")



