import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/SSHv2_Support_in_FIPS')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.SSHv2_Support_in_FIPS',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()