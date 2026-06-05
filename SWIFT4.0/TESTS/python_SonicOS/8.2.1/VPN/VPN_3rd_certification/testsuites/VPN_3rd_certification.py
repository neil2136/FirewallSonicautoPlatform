import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_3rd_certification')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_15',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_16',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_17',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_18',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_19',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_20',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_21',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_22',
        'definition.clear_env.TestClearConfEnv',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_07',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_1',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_10',

        ## add case 33,34,35,36, case33 add level local cert, it must run before 35,36
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_33',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_34',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_01',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_02',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_03',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_01',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_02',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_03',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
