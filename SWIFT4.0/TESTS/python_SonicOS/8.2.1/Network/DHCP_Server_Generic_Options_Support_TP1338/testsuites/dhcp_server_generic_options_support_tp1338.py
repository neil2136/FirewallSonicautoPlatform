# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/DHCP_Server_Generic_Options_Support_TP1338")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC01',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC02',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC03',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC06',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC07',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC08',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC09',
        'testcases.dhcp_server_generic_options_support_tp1338.TestBaseFunc_TC04',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
