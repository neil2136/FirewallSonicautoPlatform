from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_pkt_mon(self):
        param = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '546,547'
            }
        }
        res = pkt_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')

    def test_02_config_x2(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, 'ERR: config X2 interface failed!')
