# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/VPN/DHCP_Relay_TP28")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_conf',
        'definition.init_fw_conf',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC1',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC2',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC3',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC21',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC23',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC25',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC27',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC65',
        'testcases.dhcp_relay_tp28.TestBaseFun_TC66',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
