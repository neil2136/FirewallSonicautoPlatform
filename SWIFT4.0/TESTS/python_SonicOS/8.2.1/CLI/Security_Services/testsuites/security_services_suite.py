import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/Security_Services')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/Security_Services/testcases')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'security_services.TC_01_Security_Services',
        'security_services.TC_02_Security_Services',
        'security_services.TC_03_Security_Services',
        'security_services.TC_04_Security_Services',
        'security_services.TC_05_Security_Services',
        # Proxy server no longer supported in gen8
        # 'security_services.TC_06_Security_Services',
        'security_services.TC_07_Security_Services',
        'security_services.TC_08_Security_Services',
        'security_services.TC_09_Security_Services',
        'security_services.TC_10_Security_Services',
        'security_services.TC_11_Security_Services',
        'security_services.TC_12_Security_Services',
 
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
