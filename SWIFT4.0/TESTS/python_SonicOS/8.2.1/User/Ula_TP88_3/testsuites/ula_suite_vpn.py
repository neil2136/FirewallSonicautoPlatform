# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Ula_TP88_3/testcases')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw_vpn.TestConfigTB',
        'definition.init_conf_pc.TestSetup_PCs',
        'ula_vpn.TestConfigureULA',
        'ula_vpn.TC21_Access_VPN_From_Remote_End_Allow_Admin',
        'ula_vpn.TC22_Access_VPN_From_Remote_End_Allow_Everyone',
        'ula_vpn.TC23_Access_VPN_From_Remote_End_Allow_Group',
        'ula_vpn.TC24_Access_VPN_From_Remote_End_Allow_Super_Group',
        'ula_vpn.TC25_Access_VPN_From_Remote_End_Allow_User',
        'ula_vpn.TC26_AUP_Displayed_On_Login_From_VPN'

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()