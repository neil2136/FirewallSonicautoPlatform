import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Address_Objects')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Address_Objects/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


from testcases.IPv6_AddressObj import *

def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
        'testcases.IPv6_AddressObj'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

