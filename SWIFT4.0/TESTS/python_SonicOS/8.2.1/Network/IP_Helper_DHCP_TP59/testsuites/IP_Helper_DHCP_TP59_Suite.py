# __author__: nizhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IP_Helper_DHCP_TP59')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW',
        'definition.init_conf_pc.TestSetup_PCs',
        'testcases.IP_Helper_DHCP_TP59.Test_Config_TC07',
        'testcases.IP_Helper_DHCP_TP59.Test_Config_TC10',
        'testcases.IP_Helper_DHCP_TP59.Test_Config_TC09',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
