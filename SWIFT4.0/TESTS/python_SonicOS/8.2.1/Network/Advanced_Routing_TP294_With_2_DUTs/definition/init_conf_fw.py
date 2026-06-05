from definition.settings import *


class TestRestore_REMOTE(Test):
    uuid = 'NonTC'
    restore_Lbox_cmd = f"nohup python3 {defi_path}/script/restoreFW.py -ip {consvr_LBOX} -p {conport_LBOX} > /tmp/resotreLbox.log 2>&1 &"
    PC1_login.send_command(restore_Lbox_cmd)
    logger.info('.................Restore Lbox .................')
    Assertion.assert_equal(True, True, "ERR: Restore REMOTE failed")


class TestInit_FW(Test):
    uuid = 'NonTC'

    def test_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway':  Parameter.X1_GW,
            'dns1':  Parameter.X1_DNS1,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")


class TestInit_LBOX(Test):
    uuid = 'NonTC'

    def test_01_enabel_api(self):
        rc = False
        try:
            rc = lbox_adminconsole.sonicos_api(**api_dict)
            if rc:
                logger.info('Success enable remote api basic')
            else:
                logger.info('Failed enable remote api basic')
        except KeyError:
            logger.error('Failed enable remote api basic')
        Assertion.assert_equal(rc, True, "ERR: enable API failed")

    def test_02_config_interface_X0(self):
        x0_static = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.LBOX_X0_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = lbox_interfaceconsole.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")

    def test_03_check_X0_traffic(self):
        rc = PC1_login.ping_from_eth(Parameter.LBOX_X0_IP, 'eth3', num=2)
        Assertion.assert_equal(rc, True, "ERR: ping X0 failed")

    def test_04_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.LBOX_X1_IP,
            'gateway':  Parameter.LBOX_X1_GW,
            'dns1':  Parameter.LBOX_X1_DNS1,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = lbox_interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.LBOX_X2_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = lbox_interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

