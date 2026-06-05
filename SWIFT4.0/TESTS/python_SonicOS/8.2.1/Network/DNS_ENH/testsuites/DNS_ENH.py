import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_ENH/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.DNS_ENH.TestDNSENH_01',  
        'testcases.DNS_ENH.TestDNSENH_02', 
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
