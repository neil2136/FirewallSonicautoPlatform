import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Forged_IP_FC')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.DNS_Filtering_Forged_IP_FC.TestCheck_dns_server_1',
        'testcases.DNS_Filtering_Forged_IP_FC.TestDNS_Filtering_Forged_IP_FC_010', 
        'testcases.DNS_Filtering_Forged_IP_FC.TestDNS_Filtering_Forged_IP_FC_011', 
        'testcases.DNS_Filtering_Forged_IP_FC.TestDNS_Filtering_Forged_IP_FC_012',
        'testcases.DNS_Filtering_Forged_IP_FC.TestDNS_Filtering_Forged_IP_FC_005',
        'testcases.DNS_Filtering_Forged_IP_FC.TestDNS_Filtering_Forged_IP_FC_006', 
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
