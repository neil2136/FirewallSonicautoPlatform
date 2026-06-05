import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/tools')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/WireGuard_VPN')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/WireGuard_VPN/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
'/Network/WireGuard_VPN/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_pc',
        'conf_fw',
        'wireguard_vpn.Test_1_wg0_interface_edit_4',
        'wireguard_vpn.Test_2_wg_global_settings_enable_22',
        'wireguard_vpn.Test_3_add_wg_peer_valid_name_31',
        'wireguard_vpn.Test_4_export_wireguard_peer_41',
        'wireguard_vpn.Test_5_allow_any_address_access_52',
        'wireguard_vpn.Test_6_customer_added_address_access_53',
        'wireguard_vpn.Test_7_restart_wireguard_configure_check_59',
        'wireguard_vpn.Test_8_restart_access_check_60',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
