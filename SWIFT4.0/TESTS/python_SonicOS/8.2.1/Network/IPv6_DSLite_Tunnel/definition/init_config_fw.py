from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_restore_remote_fw(self):
        logger.info('=> restore remote FW and enable API')
        remote_conf_path = os.environ['PYTHON_COMMON_HOME'] + \
                           '/config/restore_gw_rmt_tel.py'
        cmd1 = f'python3 {remote_conf_path} ' \
            f'-os=1 --testbed={Params.testbed} ' \
            f'-device=RemoteGEN7 -if=x2 -zone=WAN ' \
            f'-ip=12.12.1.201 -restore=1'
        pc1_login.send_command(cmd1)
        logger.info('=> check if remote X3 is reachable')
        res = pc1_login.ping(f'{Parameter.REM_X3_IP}')
        logger.info(f'ping remote firewall x3 result: {res}')
        Assertion.assert_equal(res, True, 'ERR: config remote FW failed')

    def test_02_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '12.12.1.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_register_fw(self):
        for i in range(10):
            sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_config_x2_interface(self):
        x2_static = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_config_x2_v6_on_local(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 IPv6 static failed")

    def test_06_config_x2_v6_on_remote(self):
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.REM_X2_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = rm_ifacev6_api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 IPv6 static failed")

    def test_07_addr_objs_for_routes_on_local_firewall(self):
        ao_1 = {
            "object_type": "network",
            "name": "192.168.168.0/24",
            "zone": "LAN",
            'value': "192.168.168.0,255.255.255.0",
        }
        ao_2 = {
            "object_type": "network",
            "name": "172.16.1.0/24",
            "zone": "LAN",
            'value': "172.16.1.0,255.255.255.0",
        }
        ao_3 = {
            "object_type": "network",
            "name": "12.12.3.0/24",
            "zone": "LAN",
            'value': "12.12.3.0,255.255.255.0",
        }
        for ao in (ao_1, ao_2, ao_3):
            if ao is ao_1:
                rc = rem_ao_api.config_addressobject(**ao)
            else:
                rc = ao_api.config_addressobject(**ao)
            if not rc:
                logger.error(f'add addr object <{ao["name"]}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: add address objects failed!!')

    def test_08_config_local_x1_v6(self):
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X1 IPv6 static on local firewallfailed")

    def test_09_config_remote_x1_v6(self):
        rem_x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.REM_X1_V6_IP,
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc = rm_ifacev6_api.config_interface_ipv6(**rem_x1_v6_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 IPv6 static failed")
