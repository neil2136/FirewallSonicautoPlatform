import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPSec/dhcp_over_vpn/dhcp_sanity_cases')

from definition.settings import *


class dhcp_central_01(Test):
    uuid = "SOSAIOT-TC-47591"
    description = show_testcase_info(Parameter.TESTPLAN, '364', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '364')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcpserver(self):
        edit_central = {
            'internal_dhcp': True,
            'global_vpn': True,
            'remote': False,
            'relay_ip': '0.0.0.0',
            'send_requests': False,

        }

        response = dhcp_settings.config_dhcpvpn_centralgw(**edit_central)
        response1 = dhcp_settings.show_dhcpovervpn_central()
        Assertion.assert_regular(json.dumps(response1), '"internal_dhcp": true, "global_vpn": true', 'ERR:failed to enable internal dhcp server for global vpn client')


class dhcp_central_02(Test):
    uuid = "SOSAIOT-TC-47592"
    description = show_testcase_info(Parameter.TESTPLAN, '757', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '757')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcpserver(self):
        edit_central = {
            'internal_dhcp': False,
            'global_vpn': False,
            'remote': True,
            'relay_ip': '0.0.0.0',
            'send_requests': False,

        }

        response = dhcp_settings.config_dhcpvpn_centralgw(**edit_central)
        response1 = dhcp_settings.show_dhcpovervpn_central()
        Assertion.assert_regular(json.dumps(response1), '"send_requests": false', 'ERR:failed to disable send request in central gateway')


class dhcp_remote_03(Test):
    uuid = "SOSAIOT-TC-47593"
    description = show_testcase_info(Parameter.TESTPLAN, '763', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '763')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcpserver(self):
        edit_remotegw = {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.2',
            'management_ip': '0.0.0.0',
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2'

        }

        response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
        response1 = dhcp_settings.show_dhcpovervpn_remote()
        Assertion.assert_regular(json.dumps(response1), '"relay_ip": "10.0.0.2"', 'ERR:failed to edit realy ip address in remote gateway')


class dhcp_remote_04(Test):
    uuid = "SOSAIOT-TC-47590"
    description = show_testcase_info(Parameter.TESTPLAN, '766', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '766')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcpserver(self):
        edit_remotegw = {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.2',
            'management_ip': '0.0.0.0',
            'block_spoof': True,
            'temp_lease': True,
            'lease_time': '2'

        }

        response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
        response1 = dhcp_settings.show_dhcpovervpn_remote()
        Assertion.assert_regular(json.dumps(response1), '"temp_lease": true', 'ERR:failed to enable temporary lease and lease time')
