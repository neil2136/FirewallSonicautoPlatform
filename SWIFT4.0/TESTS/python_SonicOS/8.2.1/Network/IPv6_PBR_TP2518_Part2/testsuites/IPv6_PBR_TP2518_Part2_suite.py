import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_PBR_TP2518_Part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigENV',
        'testcases.IPv6_PBR_TP2518_Part2',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()