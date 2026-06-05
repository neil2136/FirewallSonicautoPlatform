import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Route_Based_VPN_2335')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.Route_Based_VPN_2335_TC53',
        'testcases.Route_Based_VPN_2335_TC56_58_62_63',
        'testcases.Route_Based_VPN_2335_TC70_72',
        'testcases.Route_Based_VPN_2335_TC57',
        'testcases.Route_Based_VPN_2335_TC74',
        'testcases.Route_Based_VPN_2335_TC40',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
