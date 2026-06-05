from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from scapy.autorun import autorun_get_live_interactive_session
from settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GW,
        }
        rc = interfaceipv4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_00_02_config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'gateway': Parameter.DUT_X2_GW,
        }
        rc = interfaceipv4api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_03_config_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X3_IP,
            'gateway': Parameter.DUT_X3_GW,
        }

        rc = interfaceipv4api.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_00_04_config_X4(self):
        x4_static = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X4_IP,
            'gateway': Parameter.DUT_X4_GW
        }
        rc = interfaceipv4api.config_interface(**x4_static)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static failed")

    def test_00_05_config_X5(self):
        x5_static = {
            'if': 'X5',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUT_X5_IP,
            'gateway': Parameter.DUT_X5_GW
        }
        rc = interfaceipv4api.config_interface(**x5_static)
        Assertion.assert_equal(rc, True, "ERR: Config X5 to static failed")

    def test_00_06_Add_address(self):
        ao_list = [
            gw1_ao_dict,
            gw2_ao_dict,
            gw3_ao_dict,
            gw4_ao_dict,
            dns_server_ao_dict,
            server_pc_ao_dict,
            server_network_ao_dict,
            client_range_ao_dict,
            client_network_ao_dict
        ]
        reslist = []
        for ao in ao_list:
            res = aoapi.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add destination ao {} result: {}'.format(ao, res))
        res = all(value == 1 for value in reslist)
        Assertion.assert_equal(
            res, True, "ERR: Add source and destination AO failed")
