import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
print(sys.path.append(os.environ["PYTHON_COMMON_HOME"]))
print(sys.path.append(os.environ["PYTHON_SONICOS_HOME"]))
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/RADIUS-TP89/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/RADIUS-TP89')


def suite():
    testcases_list = [
        
        'definition.init_conf_fw.Test_init_RemoteFW',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'radius_tp89.Radius_configs',
        'radius_tp89.TC01_Radius',
        'radius_tp89.TC02_Radius',
        'radius_tp89.TC03_Radius',
        'radius_tp89.TC04_Radius',
        'radius_tp89.TC05_Radius',
        'radius_tp89.TC06_Radius',
        'radius_tp89.TC07_Radius',
        'radius_tp89.TC08_Radius',
        'radius_tp89.TC09_Radius',
        'radius_tp89.TC10_Radius',
        'radius_tp89.TC11_Radius'
	]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites 
       
      
if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()






