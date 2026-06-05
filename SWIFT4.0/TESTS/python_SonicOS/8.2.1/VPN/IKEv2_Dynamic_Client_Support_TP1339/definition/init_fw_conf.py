from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_00_config_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 ipv4 address failed")

    def test_01_01_register_fw(self):
        for i in range(5):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_config_x2(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        logger.info("config x2 interface... ")
        rc = interfacev4api.config_interface(**x2_v4_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 ipv4 address failed")

    def test_03_add_pc2_eth1_host_ao(self):
        pc2_host_dict = {
            "object_type": "host",
            "name": "pc2_eth1",
            "zone": "LAN",
            "value": PC2_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**pc2_host_dict)
        Assertion.assert_equal(rc, True, "ERR: add pc2 eth1 host ao failed")

    def test_04_add_pc3_eth1_host_ao(self):
        pc3_host_dict = {
            "object_type": "host",
            "name": "pc3_eth1",
            "zone": "VPN",
            "value": PC3_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**pc3_host_dict)
        Assertion.assert_equal(rc, True, "ERR: add pc2 eth1 host ao failed")

    def test_05_add_remote_x3_network_ao_on_local_dut(self):
        remote_x2_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x2_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote x3 network ao on local dut failed")


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
            'value': f'{Parameter.X2_NET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x2_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x2 network ao on remote dut failed")
