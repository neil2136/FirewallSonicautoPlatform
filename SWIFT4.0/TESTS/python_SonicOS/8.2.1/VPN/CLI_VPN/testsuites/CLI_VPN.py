import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/CLI_VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/CLI_VPN/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.CLI_VPN_TC.Test_01_site_to_site_vpn',
        'testcases.CLI_VPN_TC.Test_02_site_to_group_vpn',
        'testcases.CLI_VPN_TC.Test_03_tunnel_vpn'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
