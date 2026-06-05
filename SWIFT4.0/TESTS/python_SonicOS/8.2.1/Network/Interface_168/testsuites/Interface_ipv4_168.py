import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])



def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
        'testcases.Interface.Test_Interface_06',
        'testcases.Interface.Test_Interface_08',
        'testcases.Interface.Test_Interface_12',
        'testcases.Interface.Test_Interface_13',
        'testcases.Interface.Test_Interface_14',
        'testcases.Interface.Test_Interface_19',
    ]

    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

