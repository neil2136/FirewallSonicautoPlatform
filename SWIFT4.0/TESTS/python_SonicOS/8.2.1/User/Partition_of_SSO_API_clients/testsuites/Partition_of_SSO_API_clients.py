import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Partition_of_SSO_API_clients')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_01',
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_02', 
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_03', 
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_04',
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_05',        
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_06', 
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_07', 
        'testcases.Partition_of_SSO_API_clients.Test_Partition_of_SSO_API_clients_08'
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
