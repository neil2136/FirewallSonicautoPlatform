# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ECMP')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw_part3.TestConfigFW',
        'definition.init_conf_pc_part3',
        'testcases.ecmp_part3.TestECMPBase_v4_TC003',
        'testcases.ecmp_part3.TestECMPBase_v4_TC153',
        'testcases.ecmp_part3.TestECMPBase_v6_TC068',
        'testcases.ecmp_part3.TestECMPBase_v6_TC006',
        'testcases.ecmp_part3.TestECMPBase_v6_CLI_TC165',
        'testcases.ecmp_part3.TestECMPBase_v6_TC088',
        'testcases.ecmp_part3.TestECMPBase_v6_CLI_TC171',
        'testcases.ecmp_part3.TestECMPBase_v6_TC078',
        'testcases.ecmp_part3.TestECMPBase_v6_CLI_TC177',
        'testcases.ecmp_part3.TestECMPBase_v6_TC081',
        'testcases.ecmp_part3.TestECMPBase_exp_TC220',
        'definition.init_conf_fw_part3.TestRestore',
        'testcases.ecmp_part3.TestECMPBase_exp_TC221',
        'testcases.ecmp_part3.TestECMPBase_v6_CLI_TC181',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
