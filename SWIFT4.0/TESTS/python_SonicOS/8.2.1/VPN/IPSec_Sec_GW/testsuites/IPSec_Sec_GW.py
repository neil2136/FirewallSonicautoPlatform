import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IPSec_Sec_GW')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw.TestConfigTB',
        'definition.conf_env.TestConfigTB',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_02',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_04',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_09',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_10',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_11',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_12',
        'testcases.IPSec_Sec_GW_TC.TestIPSec_Sec_GW_23',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
