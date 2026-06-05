import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Log_and_Config_Profile')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Log_04', 
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_014', 
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_015',
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_016',
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_019',
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_018',
        'testcases.DNS_Filtering_Log_and_Config_Profile.TestDNS_Filtering_Config_File_021',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
