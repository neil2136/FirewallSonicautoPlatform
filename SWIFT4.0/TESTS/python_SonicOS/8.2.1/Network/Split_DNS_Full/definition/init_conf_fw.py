from definition.settings import *


class TestInit_RemFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(5)
    def test_01_restore_remote_fw(self):
        logger.info('=> restore remote FW and enable API')
        remote_conf_path = os.environ['PYTHON_COMMON_HOME'] + \
                           '/config/restore_gw_rmt_tel.py'
        command = f'python3 {remote_conf_path} -os=1 -device="RemoteGEN7" -testbed={Params.testbed} -if="X0" -zone="LAN" -ip={Parameter.REM_X0_IP} -cserver={consvr_rmt} -cport={conport_rmt} -restore=1'
        PC1_login.send_command(command)
        logger.info('=> check if remote X0 is reachable')
        res = PC1_login.ping(f'{Parameter.REM_X0_IP}')
        logger.info(f'ping remote firewall x0 result: {res}')
        Assertion.assert_equal(res, True, 'ERR: config remote FW failed')

    def test_02_config_x2(self):
        logger.info("config x2 ipv6 interface ... ")
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.REM_X2_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = rmtinterfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1, True, "ERR: Config X0 to static failed")

    def test_03_config_x3(self):
        logger.info("config x3 ipv6 interface ... ")
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REM_X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = rmtinterfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1, True, "ERR: Config X0 to static failed")

    def test_04_add_aos(self):
        (aores, msg) = rmtaoapi.config_addressobject(msg=True, **remote_r)
        if aores is False:
            aores = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(aores, True, "ERR: add ao failed")


class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_config_x0(self):
        logger.info("config x0 ipv6 interface ... ")
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(rc1, True, "ERR: Config X0 to static failed")

    def test_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x1_static)
        rc2 = interfacev6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    @repeat_method(2)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'dns1': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x2_static)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    def test_04_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    def test_05_add_aos(self):
        (aores, msg) = aoapi.config_addressobject(msg=True, **local_r)
        if aores is False:
            aores = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(aores, True, "ERR: add ao failed")



