import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Default_Profile')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_03', 
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_04', ###jiraGen7-25840
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_05',
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_06',
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_07',
        'testcases.DNS_Filtering_Default_Profile.TestDNS_Filtering_Default_Profile_08', ###jiraGen7-25840
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
