import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKEv2_Sec_GW_Part2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw.TestConfigTB',
        'definition.conf_env.TestConfigTB',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513006',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513007',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513008',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513013',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513014',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513015',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513021',
        'testcases.IKEv2_Sec_GW_Part2_TC.TestIKEv2_Sec_GW_1513022',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
