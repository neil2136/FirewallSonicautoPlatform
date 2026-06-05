import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Custom_Domain')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.DNS_Filtering_Custom_Domain.TestDNS_Filtering_Custom_Domain_01', 
        'testcases.DNS_Filtering_Custom_Domain.TestDNS_Filtering_Custom_Domain_02', 
        'testcases.DNS_Filtering_Custom_Domain.TestDNS_Filtering_Custom_Domain_03', 
        'testcases.DNS_Filtering_Custom_Domain.TestDNS_Filtering_Custom_Domain_04',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
