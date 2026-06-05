import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/DPD')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'definition.register_fw.TestRegisterFW',
        'bin.conf_fw.TestConfigTB',
        'definition.conf_env.TestConfigTB',
        'testcases.DPD_Disable_01_02',
        'testcases.DPD_Enable_03_04_15',
        'testcases.DPD_Enable_Keep_Alive_05_06',
        'testcases.DPD_Enable_Multi_VPN_09',
        'testcases.DPD_TC.TestDPD_10',
        'testcases.DPD_TC.TestDPD_11',
        'testcases.DPD_TC.TestDPD_12',
        'testcases.DPD_TC.TestDPD_13',
        'testcases.DPD_TC.TestDPD_07',
        'testcases.DPD_TC.TestDPD_08',
        'testcases.DPD_TC.TestDPD_14',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
