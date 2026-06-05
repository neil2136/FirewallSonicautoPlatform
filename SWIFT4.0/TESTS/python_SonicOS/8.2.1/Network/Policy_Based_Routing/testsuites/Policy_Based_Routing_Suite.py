import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Policy_Based_Routing')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config_fw.TestConfigFW',
        'definition.initial_config_pc.TestConfigPC',
        'testcases.Policy_Based_Routing.TestPolicyBasedRouting_12', 
        'testcases.Policy_Based_Routing.TestPolicyBasedRouting_17', 
        'testcases.Policy_Based_Routing.TestPolicyBasedRouting_23',
        'testcases.Policy_Based_Routing.TestPolicyBasedRouting_27',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
