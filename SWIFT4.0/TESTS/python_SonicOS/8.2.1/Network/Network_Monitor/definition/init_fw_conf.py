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

    def test_03_add_remote_ao_on_local_dut(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X3_REMOTE_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote ao on local dut failed")

    def test_04_create_probe_target_vpn_host_pc4_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc4_eth1",
            "zone": "VPN",
            "value": PC4_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_05_create_probe_target_vpn_host_pc5_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc5_eth1",
            "zone": "VPN",
            "value": PC5_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_06_create_vpn_ao_range_include_pc4_eth1_and_pc5_eth1(self):
        probe_object_dict = {
            "object_type": "range",
            "name": "remoteproberange",
            "zone": "VPN",
            "value": f'{PC4_ETH1_IP},{PC5_ETH1_IP}'
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_07_create_vpn_ao_group_include_pc4_eth1_and_pc5_eth1(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "pc4_eth1"
                                },
                                {
                                    "name": "pc5_eth1"
                                },
                            ]
                        },
                        "name": "remoteprobgroup"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: create ao group failed")

    def test_08_create_probe_target_lan_host_pc2_eth2(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc2_eth2",
            "zone": "LAN",
            "value": PC2_ETH2_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_09_create_probe_target_wan_host_pc2_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc2_eth1",
            "zone": "WAN",
            "value": PC2_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_10_create_probe_target_lan_host_pc3_eth1(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "pc3_eth1",
            "zone": "LAN",
            "value": PC3_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_11_create_lan_ao_group_include_pc2_eth2_and_pc3_eth2(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "pc2_eth2"
                                },
                                {
                                    "name": "pc3_eth1"
                                },
                            ]
                        },
                        "name": "lanprobgroup"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: Failed To add probe ao group")

    def test_12_create_probe_target_x1_gateway_host_ao(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "x1_gw",
            "zone": "WAN",
            "value": "12.12.1.1"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_13_create_probe_target_x1_gw_unreachable_host_ao(self):
        probe_object_dict = {
            "object_type": "host",
            "name": "gw_unreachable",
            "zone": "WAN",
            "value": "12.12.1.10"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")

    def test_14_create_probe_target_with_x2_range_ao(self):
        probe_object_dict = {
            "object_type": "range",
            "name": "range_ao",
            "zone": "LAN",
            "value": "193.168.1.20,193.168.1.22"
        }
        rc = addressobjectsapi.config_addressobject(**probe_object_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To add probe address object")


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

    def test_02_add_local_x0_network_ao_on_remote_dut(self):
        remote_x3_subnet = {
            'name': 'local_x0_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'{Parameter.X0_NET},{Parameter.MASK}',
        }
        res = r_addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add local x0 network ao on remote dut failed")












