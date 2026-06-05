import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/MTU_Settings')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/MTU_Settings/definition')
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] +
    '/Network/MTU_Settings/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        # 'config.init_testbed.TestRestoreDUT',
        # 'config.init_testbed.TestUploadFirmware',
        'mtu_settings.Test_01_MTU_NF_UDP_Packet_02',
        'mtu_settings.Test_02_VPN_MTU_NF_UDP_Packet_05'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
