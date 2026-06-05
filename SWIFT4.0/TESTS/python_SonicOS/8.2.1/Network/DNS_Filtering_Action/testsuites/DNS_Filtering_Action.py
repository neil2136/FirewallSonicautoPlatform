import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Action')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.DNS_Filtering_Action.TestCheck_dns_server_1', 
        'testcases.DNS_Filtering_Action.TestDNS_Filtering_Action_001', 
        'testcases.DNS_Filtering_Action.TestDNS_Filtering_Action_002', 
        'testcases.DNS_Filtering_Action.TestDNS_Filtering_Action_003',
        'testcases.DNS_Filtering_Action.TestDNS_Filtering_Action_004',
        'testcases.DNS_Filtering_Action.TestDNS_Filtering_Action_005', 
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
