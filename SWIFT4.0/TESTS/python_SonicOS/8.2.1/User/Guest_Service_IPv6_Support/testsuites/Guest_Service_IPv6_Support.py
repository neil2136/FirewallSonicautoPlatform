import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Guest_Service_IPv6_Support')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'testcases.Guest_Service_IPv6_Support.Test_Guest_Service_IPv6_Support_007',
        'testcases.Guest_Service_IPv6_Support.Test_Guest_Service_IPv6_Support_010',
        'testcases.Guest_Service_IPv6_Support.Test_Guest_Service_IPv6_Support_042',        
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
