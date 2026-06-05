from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
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

    @repeat_method(5)
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
