import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
print(sys.path.append(os.environ["PYTHON_COMMON_HOME"]))
print(sys.path.append(os.environ["PYTHON_SONICOS_HOME"]))
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Radius_client_accounting/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Radius_client_accounting')


def suite():
    testcases_list = [
        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'radius_client_accounting.Radius_configs',
        'radius_client_accounting.TC01_Radius_Client_Accounting',
        'radius_client_accounting.TC02_Radius_Client_Accounting',
        'radius_client_accounting.TC03_Radius_Client_Accounting',
        'radius_client_accounting.TC04_Radius_Client_Accounting',
        'radius_client_accounting.TC05_Radius_Client_Accounting',
        'radius_client_accounting.TC06_Radius_Client_Accounting',
        'radius_client_accounting.TC07_Radius_Client_Accounting',
        'radius_client_accounting.TC08_Radius_Client_Accounting',
        # 'radius_client_accounting.TC09_Radius_Client_Accounting',
        # 'radius_client_accounting.TC10_Radius_Client_Accounting'
       
	]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites 
       
      
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()






