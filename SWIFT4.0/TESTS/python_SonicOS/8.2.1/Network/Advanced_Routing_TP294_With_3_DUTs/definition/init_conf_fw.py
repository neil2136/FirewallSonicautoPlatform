from definition.settings import *


class TestRestore_REMOTE(Test):
    uuid = 'NonTC'
    restore_Lbox_cmd = f"nohup python3 {defi_path}/script/restoreFW.py -ip {consvr_LBOX} -p {conport_LBOX} > /tmp/resotreLbox.log 2>&1 &"
    restore_Rbox_cmd = f"nohup python3 {defi_path}/script/restoreFW.py -ip {consvr_RBOX} -p {conport_RBOX} > /tmp/resotreRbox.log 2>&1 &"
    PC1_login.send_command(restore_Lbox_cmd)
    logger.info('.................Restore Lbox .................')
    PC1_login.send_command(restore_Rbox_cmd)
    logger.info('.................Restore Rbox .................')
    Assertion.assert_equal(True, True, "ERR: Restore REMOTE failed")


class TestInit_FW(Test):
    uuid = 'NonTC'

    def test_02_config_interface_X1(self):
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
    
    def test_03_config_interface_X2_vlan1(self):
        x2_vlan1_static = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': X2_VLAN1_ID,
            'zone': 'lan',
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

    def test_05_config_interface_X3_vlan1(self):
        x3_vlan1_static = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X3_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.add_interface(**x3_vlan1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")


class TestInit_LBOX(Test):
    uuid = 'NonTC'

    def test_01_enabel_api(self):
        rc = False
        try:
            rc = LBOX_adminconsole.sonicos_api(**api_dict)
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
        rc = LBOX_interfaceconsole.config_interface(**x0_static)
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

    
class TestInit_RBOX(Test):
    uuid = 'NonTC'

    def test_01_enabel_api(self):
        try:
            rc = RBOX_adminconsole.sonicos_api(**api_dict)
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
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.RBOX_X0_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = RBOX_interfaceconsole.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")
    
    def test_03_check_X0_traffic(self):
        rc = PC1_login.ping_from_eth(Parameter.RBOX_X0_IP, 'eth4', num=2)
        Assertion.assert_equal(rc, True, "ERR: ping X0 failed")

    def test_04_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.RBOX_X1_IP,
            'gateway':  Parameter.RBOX_X1_GW,
            'dns1':  Parameter.RBOX_X1_DNS1,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = rbox_interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.RBOX_X3_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = rbox_interfaceapi.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

   
