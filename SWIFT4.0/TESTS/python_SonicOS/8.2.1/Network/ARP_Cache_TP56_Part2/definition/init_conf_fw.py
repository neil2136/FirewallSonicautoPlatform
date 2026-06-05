from definition.settings import *
from definition.utils import *


class TestInit_FW(Test):
    uuid = 'NonTC'

    def test_01_00_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_01_01_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_get_interface_mac(self):
        res1 = Parameter.DUT_X0_MAC = get_dut_interface_mac('X0')
        logger.info(f'dut interface X0 mac is :{Parameter.DUT_X0_MAC}')

        res2 = Parameter.DUT_X1_MAC = get_dut_interface_mac('X1')
        logger.info(f'dut interface X1 mac is :{Parameter.DUT_X1_MAC}')

        res3 = Parameter.DUT_X2_MAC = get_dut_interface_mac('X2')
        logger.info(f'dut interface X2 mac is :{Parameter.DUT_X2_MAC}')

        flag = True if res1 and res2 and res3 else False

        Assertion.assert_equal(flag, True, "ERR: get interface mac failed")

    def test_04_get_pc_mac(self):  
        res1= Parameter.X0_PC_MAC = get_pc_int_mac(PC1_login,'eth0')
        logger.info(f'X0_PC_MAC is :{Parameter.X0_PC_MAC}')

        res2 = Parameter.X1_PC_MAC = get_pc_int_mac(PC1_login,'eth2')
        logger.info(f'X1_PC_MAC is :{Parameter.X1_PC_MAC}')

        res3 = Parameter.X2_PC_MAC = get_pc_int_mac(PC2_login,'eth0')
        logger.info(f'X2_PC_MAC is :{Parameter.X2_PC_MAC}')

        flag = True if res1 and res2 and res3 else False

        Assertion.assert_equal(flag, True, "ERR: get pc mac failed")

    def test_05_add_aos(self):
        tag = []
        X1_public_dict = {
            'object_type': 'host',
            'name': 'X1_public_ip',
            'zone': 'WAN',
            'value': Parameter.FAKE_WAN_IP
        }
        X2_public_dict = {
            'object_type': 'host',
            'name': 'X2_public_ip',
            'zone': 'WAN',
            'value': Parameter.FAKE_IP
        }
        lan_pc_dict = {
            'object_type': 'host',
            'name': 'lan pc',
            'zone': 'LAN',
            'value': PC1_ETH0_IP
        }
        dmz_pc_dict = {
            'object_type': 'host',
            'name': 'dmz pc',
            'zone': 'LAN',
            'value': PC2_ETH0_IP
        }
        SECONDARY_NETWORK_dict = {
            'object_type': 'network',
            'name': '2rd_net',
            'zone': 'LAN',
            'value': Parameter.SECONDARY_NETWORK + ',255.255.255.0'
        }
        SECONDARY_PC_dict = {
            'object_type': 'host',
            'name': '2rd_pc',
            'zone': 'LAN',
            'value': Parameter.SECONDARY_PC
        }
        ao_list = [
            X1_public_dict,
            lan_pc_dict,
            X2_public_dict,
            dmz_pc_dict,
            SECONDARY_NETWORK_dict,
            SECONDARY_PC_dict
        ]
        for ao in ao_list:
            rc = aoapi.config_addressobject(**ao)
            tag.append(rc)
        Assertion.assert_equal(all(tag), True, 'ERR: add aos failed')