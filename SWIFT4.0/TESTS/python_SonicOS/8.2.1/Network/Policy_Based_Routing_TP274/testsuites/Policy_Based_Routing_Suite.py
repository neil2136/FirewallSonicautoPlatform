# __Author__: lezhang

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Policy_Based_Routing_TP274')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config_fw.TestConfigFW',
        'definition.initial_config_pc.TestConfigPC',
        'testcases.Policy_Based_Routing.TestPBR_TC12',
        'testcases.Policy_Based_Routing.TestPBR_TC17',
        'testcases.Policy_Based_Routing.TestPBR_TC11',
        'testcases.Policy_Based_Routing.TestPBR_TC23',
        'testcases.Policy_Based_Routing.TestPBR_TC27',
        'testcases.Policy_Based_Routing.TestPBR_TC26',
        'testcases.Policy_Based_Routing.TestPBR_TC43',
        'testcases.Policy_Based_Routing.TestPBR_TC44',
        'testcases.Policy_Based_Routing.TestPBR_TC45',
        'testcases.Policy_Based_Routing.TestPBR_TC46',
        'testcases.Policy_Based_Routing.TestPBR_TC47',
        'testcases.Policy_Based_Routing.TestPBR_TC48',
        'testcases.Policy_Based_Routing.TestPBR_TC28',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
