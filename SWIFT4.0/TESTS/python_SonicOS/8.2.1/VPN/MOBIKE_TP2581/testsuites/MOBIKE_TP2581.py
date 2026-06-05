import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/MOBIKE_TP2581')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.MOBIKE_TP2581_TC3_4_5_6',
        'testcases.MOBIKE_TP2581_TC7_8_10',
        'testcases.MOBIKE_TP2581_TC15_16_17_18',
        'testcases.MOBIKE_TP2581_TC37_38_40',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
