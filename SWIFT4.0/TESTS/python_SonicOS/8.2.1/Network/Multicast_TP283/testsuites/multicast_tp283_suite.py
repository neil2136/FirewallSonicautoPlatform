# __author__: lezhang

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/Multicast_TP283")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfig_FW',
        'definition.init_conf_pc.TestConfig_PC',
        'testcases.multicast.Testmulti_TC12',
        'testcases.multicast.Testmulti_TC16',
        'testcases.multicast.Testmulti_TC17',
        'testcases.multicast.Testmulti_TC02',
        'testcases.multicast.Testmulti_TC33',
        'testcases.multicast.Testmulti_TC34',
        'testcases.multicast.Testmulti_TC38',
        'testcases.multicast.Testmulti_TC06',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
