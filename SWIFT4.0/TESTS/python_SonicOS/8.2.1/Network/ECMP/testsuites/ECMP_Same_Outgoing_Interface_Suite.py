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
        'definition.register_fw_part2',
        'definition.init_conf_fw_part2',
        'definition.init_conf_pc_part2',
        'testcases.ecmp_part2.TestECMPBase_v4_TC038',
        'testcases.ecmp_part2.TestECMPBase_v4_TC127',
        'testcases.ecmp_part2.TestECMPBase_v4_CLI_TC144',
        'testcases.ecmp_part2.TestECMPBase_v4_CLI_TC150',
        'testcases.ecmp_part2.TestECMPBase_v4_CLI_TC156',
        'testcases.ecmp_part2.TestECMPBase_v6_TC067',
        'testcases.ecmp_part2.TestECMPBase_v6_CLI_TC162',
        'testcases.ecmp_part2.TestECMPBase_v6_CLI_TC168',
        'testcases.ecmp_part2.TestECMPBase_v6_CLI_TC174',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
