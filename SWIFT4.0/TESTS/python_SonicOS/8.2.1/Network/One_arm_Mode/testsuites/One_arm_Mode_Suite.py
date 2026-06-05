# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/One_arm_Mode')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW',
        'definition.init_conf_pc.TestSetup_PCs',
        'testcases.One_arm_Mode.TestGUITC01',
        'testcases.One_arm_Mode.TestGUITC02',
        'testcases.One_arm_Mode.TestGUITC05',
        'testcases.One_arm_Mode.TestGUITC06',
        'testcases.One_arm_Mode.TestGUITC07',
        'testcases.One_arm_Mode.TestTrafficTC08',
        'testcases.One_arm_Mode.TestGUITC23',
        'testcases.One_arm_Mode.TestTCPSYNfloodTC31',
        'testcases.One_arm_Mode.TestCLITC16',
        'testcases.One_arm_Mode.TestDHCPTC25',
        'testcases.One_arm_Mode.TestGAVTC11',
        'testcases.One_arm_Mode.TestSpywareTC12',
        'testcases.One_arm_Mode.TestIPSTC13',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
