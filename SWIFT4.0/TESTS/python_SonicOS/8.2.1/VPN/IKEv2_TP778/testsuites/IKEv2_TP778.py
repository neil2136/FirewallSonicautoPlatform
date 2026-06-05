import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKEv2_TP778')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw.TestConfigTB',
        'definition.conf_env',

        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_01',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_02',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_06',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_07',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_09',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_10',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_11',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_12',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_13',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_14',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_15',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_16',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_17',

        # #error test
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_21',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_22',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_23',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_24',
        'testcases.IKEv2_TP778_TC.TestIKEv2_TP778_25',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
