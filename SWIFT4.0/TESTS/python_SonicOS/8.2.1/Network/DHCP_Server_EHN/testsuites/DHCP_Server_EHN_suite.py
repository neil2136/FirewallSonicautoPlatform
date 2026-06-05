# __author__: cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Network/DHCP_Server_EHN")

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC96',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC01',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC10',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC14',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC19',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC21',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC97',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC25',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC16',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC18',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC20',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC26',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC27',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC30',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC28',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC29',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC32',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC34',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC35',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC36',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC37',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC38',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC39',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC91',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC92',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC95',
        'testcases.DHCP_Server_EHN.TestDHCPServer_TC78'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
