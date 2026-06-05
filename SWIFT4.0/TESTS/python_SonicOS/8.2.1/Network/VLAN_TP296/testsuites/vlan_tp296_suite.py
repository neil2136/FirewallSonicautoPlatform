# __Author__: 'lezhang'
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/VLAN_TP296/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'testcases.vlan_tp296.TestVLAN_TC01',
        'testcases.vlan_tp296.TestVLAN_TC24',
        'testcases.vlan_tp296.TestVLAN_TC06',
        'testcases.vlan_tp296.TestVLAN_TC26',
        'testcases.vlan_tp296.TestVLAN_TC37',
        'testcases.vlan_tp296.TestVLAN_TC39',
        'testcases.vlan_tp296.TestVLAN_TC10',
        'testcases.vlan_tp296.TestVLAN_TC42',
        'testcases.vlan_tp296.TestVLAN_TC46',
        'definition.conf_vpn',
        'testcases.vlan_tp296.TestVLAN_TC65',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
