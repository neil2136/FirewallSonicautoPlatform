import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/VPN_3rd_certification_Full')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigENV1',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_15',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_16',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_17',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_18',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_19',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_20',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_21',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_22',
        'definition.clear_env.TestClearConfEnv1',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_07',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_1',

        ## add case 33,34,35,36, case33 add level local cert, it must run before 35,36
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_33',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_34',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_01',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_02',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_35_03',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_01',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_02',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_36_03',

        'definition.clear_env.TestClearConfEnv1',
        'definition.conf_env.TestConfigENV2',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507704',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507705',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507708',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507709',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507710',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507712',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507713',
        'definition.clear_env.TestClearConfEnv2',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507691',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507693',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507694',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507700',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507720',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507723',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507724',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507711',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507692',
        'testcases.VPN_3rd_certification_Part2_TC.TestVPN_Cert_1507719',
        'testcases.VPN_3rd_certification_TC.TestVPN_Cert_10',

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
