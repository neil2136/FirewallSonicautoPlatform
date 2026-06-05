# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Client_TP54')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure',
        'definition.init_fw_configure',
        'testcases.dhcp_client.TestDHCPClient_TC01',
        'testcases.dhcp_client.TestDHCPClient_TC02',
        'testcases.dhcp_client.TestDHCPClient_TC15',
        'testcases.dhcp_client.TestDHCPClient_TC16',
        'testcases.dhcp_client.TestDHCPClient_TC18',
        'testcases.dhcp_client.TestDHCPClient_TC20',
        'testcases.dhcp_client.TestDHCPClient_TC21',
        'testcases.dhcp_client.TestDHCPClient_TC22',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
