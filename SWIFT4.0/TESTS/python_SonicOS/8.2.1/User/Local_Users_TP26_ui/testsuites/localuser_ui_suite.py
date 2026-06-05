import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_TP26_ui/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_TP26_ui/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Local_Users_TP26_ui/definition')
from definition.settings import *

resp = status_api.show_status()
model = resp['model']
if not model == 'TZ 80':
    def suite():
        testcases_list = [
            'config.init_testbed.TestRestoreDUT',
            'config.init_testbed.TestUploadFirmware',
            'definition.conf_fw.TestConfigTB',
            'localuser_ui.TC01_LocalUsers',
            'localuser_ui.TC02_LocalUsers',
            'localuser_ui.TC03_LocalUsers',
            'localuser_ui.TC04_LocalUsers',
            'localuser_ui.TC05_LocalUsers',
            'localuser_ui.TC06_LocalUsers',
            'localuser_ui.TC07_LocalUsers',
            'localuser_ui.TC08_LocalUsers',
            'localuser_ui.TC09_LocalUsers',
            'localuser_ui.TC10_LocalUsers',
            'localuser_ui.TC11_LocalUsers',
            'localuser_ui.TC12_LocalUsers',
            'localuser_ui.TC13_LocalUsers',
            'localuser_ui.TC14_LocalUsers',
            'localuser_ui.TC15_LocalUsers',
            'localuser_ui.TC16_LocalUsers',
            'localuser_ui.TC17_LocalUsers',
            'localuser_ui.TC18_LocalUsers',
            'localuser_ui.TC19_LocalUsers',
            'localuser_ui.TC20_LocalUsers',
            'localuser_ui.TC21_LocalUsers',
            'localuser_ui.TC22_LocalUsers',
            'localuser_ui.TC23_LocalUsers',
            'localuser_ui.TC24_LocalUsers',
            'localuser_ui.TC25_LocalUsers',
            'localuser_ui.TC26_LocalUsers',
            'localuser_ui.TC27_LocalUsers'     
        ] 
        suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
        return suites

else:
    def suite():
        testcases_list = [
            'config.init_testbed.TestRestoreDUT',
            'config.init_testbed.TestUploadFirmware',
            'definition.conf_fw.TestConfigTB',
            'localuser_ui.TC01_LocalUsers',
            'localuser_ui.TC02_LocalUsers',
            'localuser_ui.TC03_LocalUsers',
            'localuser_ui.TC04_LocalUsers',
            'localuser_ui.TC05_LocalUsers',
            'localuser_ui.TC06_LocalUsers',
            'localuser_ui.TC07_LocalUsers',
            'localuser_ui.TC08_LocalUsers',
            'localuser_ui.TC09_LocalUsers',
            'localuser_ui.TC10_LocalUsers',
            'localuser_ui.TC11_LocalUsers',
            'localuser_ui.TC12_LocalUsers',
            'localuser_ui.TC13_LocalUsers',
            'localuser_ui.TC14_LocalUsers',
            'localuser_ui.TC15_LocalUsers',
            'localuser_ui.TC16_LocalUsers',
            'localuser_ui.TC20_LocalUsers',
            'localuser_ui.TC21_LocalUsers',
            'localuser_ui.TC22_LocalUsers',
            'localuser_ui.TC23_LocalUsers',
            'localuser_ui.TC24_LocalUsers',
            'localuser_ui.TC25_LocalUsers',
            'localuser_ui.TC26_LocalUsers',
            'localuser_ui.TC27_LocalUsers'     
        ] 
        suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
        return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()



