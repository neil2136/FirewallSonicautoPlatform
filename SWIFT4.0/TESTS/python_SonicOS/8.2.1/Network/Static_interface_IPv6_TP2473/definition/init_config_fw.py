from definition.settings import *


class TestConfig_RemFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_restore_remote_fw(self):
        logger.info('=> restore remote FW and enable API')
        remote_conf_path = os.environ['PYTHON_COMMON_HOME'] + \
                           '/config/restore_gw_rmt_tel.py'
        cmd1 = f'python3 {remote_conf_path} ' \
            f'-os=1 --testbed={Params.testbed} ' \
            f'-device=RemoteGEN7 -if=x2 -zone=WAN ' \
            f'-ip=12.12.1.201 -restore=1'
        localhost.send_command(cmd1)
        logger.info('=> check if remote X1 is reachable')
        res = localhost.ping(f'{Parameter.REM_X3_IP}')
        logger.info(f'ping remote firewall x3 result: {res}')
        Assertion.assert_equal(res, True, 'ERR: config remote FW failed')


class TestConfig_LocalFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x0v6(self):
        res = iface_v6_api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(
            res, True, "ERR: Configure X0 IPv6 static failed")

    def test_02_config_x2v4(self):
        x2_static = {
            'if': 'X2',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        res = iface_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(res, True, 'ERR: config x2 failed')

    def test_03_config_x1v4(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        res = iface_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(res, True, 'ERR: config x1 failed')

    def test_04_config_v6_defaultWAN_to_x2(self):
        logger.info('=> config v6 WLB to X2.')
        wlb_conf_dict = {
            "failover_lb": {
                "group": [
                    {
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1,
                                "probe_type": "logical"
                            }
                        ],
                        "name": " Default LB Group IPv6",
                        "type": "basic"
                    }
                ]
            }
        }
        res = wlb_api.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(
            res, True, 'ERR: config x2 to default FLB v6 failed')

    def test_05_config_ipv6_nat_policy(self):
        res = nat_v6_api.add_nat_policy(**v6_nat_dict)
        Assertion.assert_equal(res, True, "ERR: add v6 nat policy failed")
