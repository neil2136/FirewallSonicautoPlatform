import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DHCP_Server_Options')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw.TestInitConfig',
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_01', 
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_02', 
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_03', 
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_04', 
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_07',
        'testcases.DHCP_Server_Options.TestDHCP_Server_Options_08', 
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
