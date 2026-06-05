from definition.settings import *

class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_initial_vpngw(self):
        logger.info('Restore Remote Gateway FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        logger.info(path)
        command = f'python3 {path} -os=1 -device="VPNGW" -testbed={Params.testbed} -if="X0" -zone="LAN" -ip={Parameter.GW_X0_IP} -cserver={consvr_gw} -cport={conport_gw} -restore=1'
        confres = PC1_Login.send_command(command)
        logger.info(confres)
        Assertion.assert_equal(True, True, "ERR: Config X0 to static failed")

    def test_02_config_interface_X3_for_GW(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.GW_X3_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = gwinterfaceapi.config_interface(**x3_static)
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
    
    def test_04_config_interface_X1(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_config_interface_X3_vlan1(self):
        x3_vlan1_static = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID,
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceapi.add_interface(**x3_vlan1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 vlan to static failed")

    def test_06_Add_address(self):
        ao_list = [
            local_r,
            ao_base_dict,
            aogw_dict
        ]
        reslist = []
        for ao in ao_list:
            res = aoapi.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add destination ao {} result: {}'.format(ao, res))
        rc = gwaoapi.config_addressobject(**remote_r)
        reslist.append(rc)
        Assertion.assert_equal(
            all(reslist), True, "ERR: Add source and destination AO failed")

