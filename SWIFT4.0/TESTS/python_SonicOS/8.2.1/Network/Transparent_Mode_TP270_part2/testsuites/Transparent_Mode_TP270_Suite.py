# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Transparent_Mode_TP270_part2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.TestConfigFW',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC02',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC03',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC05',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC06',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC08',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC09',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC10',
        'testcases.Transparent_Mode_TP270.TestConfigure_TC11',
        'testcases.Transparent_Mode_TP270.TestZones_TC13',
        'testcases.Transparent_Mode_TP270.TestInterface_TC16',
        'testcases.Transparent_Mode_TP270.TestARP_TC17',
        'testcases.Transparent_Mode_TP270.TestARP_TC18',
        'testcases.Transparent_Mode_TP270.TestARP_TC19',
        'testcases.Transparent_Mode_TP270.TestPolicy_TC22',
        'testcases.Transparent_Mode_TP270.TestGroup_Func_TC01',
        'testcases.Transparent_Mode_TP270.TestDHCP_TC33',
        'testcases.Transparent_Mode_TP270.TestTSR_TC35',
        'testcases.Transparent_Mode_TP270.TestPerf_TC38',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
