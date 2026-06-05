# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/L2TP_Server_TP373')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.L2tpServer.Test_ServerConfig_TC04',
        'testcases.L2tpServer.Test_BehindNAT_TC16',
        'testcases.L2tpServer.Test_VlanClient_TC18',
        'testcases.L2tpServer.Test_ChecksumEnforcement_TC19',
        'testcases.L2tpServer.Test_EnableAndDisable_TC06',
        'testcases.L2tpServer.Test_ConnectAndDisconnect_TC07',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
