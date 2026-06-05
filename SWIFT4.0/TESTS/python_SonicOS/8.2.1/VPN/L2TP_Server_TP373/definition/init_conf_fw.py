from definition.settings import *


class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_initial_vpngw(self):
        logger.info('Restore Remote Gateway FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command = f'python3 {path} -os=1 -device="VPNGW" -testbed={Params.testbed} -if="X0" -zone="LAN" -ip={Parameter.GW_X0_IP} -cserver={consvr_gw} -cport={conport_gw} -restore=1'
        confres = PC1_Login.send_command(command)
        logger.info(confres)

    def test_02_config_interface_X2_for_GW(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.GW_X2_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = gwinterfacecli.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")

    def test_03_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway':  Parameter.X1_GW,
            'dns1':  Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    
    def test_04_config_interface_X2_vlan1(self):
        x2_vlan1_static = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': X2_VLAN1_ID,
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.add_interface(**x2_vlan1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 vlan to static failed")

    def test_05_config_interface_X1(self):
        x1_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_06_add_Local_user(self):
        user_setting_dict = {
            'apply_password_constraints': False
        }
        settingres = localuserapi.local_settings(**user_setting_dict)
        logger.info(f"disable password_constraints: {settingres}")
        for i in range(1, 4):
            add_user_dict = {
                "action": "add",
                "username": "test"+str(i),
                "userpassword": "test"+str(i),
                "member_of": ["Everyone", "Trusted Users", "SonicWALL Administrators"],
                "vpn_client_access": {"Firewalled Subnets"}
            }
            localuserapi.local_user(**add_user_dict)
        res = localuserapi.show_local_users()
        filter_tuple = ['test1', 'test2', 'test3']
        checkres = [x in str(res) for x in filter_tuple]
        logger.info(checkres)
        flag = True if all(checkres) else False
        Assertion.assert_equal(flag & settingres, True, "ERR: add user for pc1 failed")

