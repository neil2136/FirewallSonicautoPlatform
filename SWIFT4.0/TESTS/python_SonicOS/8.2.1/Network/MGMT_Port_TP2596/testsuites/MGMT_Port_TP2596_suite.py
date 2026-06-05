import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/MGMT_Port_TP2596')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.MGMT_Port_TP2596.Test_MGMT_Port_TP2596_01',
        'testcases.MGMT_Port_TP2596.Test_MGMT_Port_TP2596_02',
        'testcases.MGMT_Port_TP2596.Test_MGMT_Port_TP2596_03',
        'testcases.MGMT_Port_TP2596.Test_MGMT_Port_TP2596_04',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
