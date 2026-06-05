import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_keep_alive')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_01',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_02',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_03',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_04',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_05',
        'testcases.VPN_keep_alive_TC.TestVPN_keep_alive_06',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
