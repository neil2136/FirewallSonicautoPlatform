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
        'definition.init_conf_fw.TestConfigTB',
        'definition.init_conf_pc.TestSetup_PCs',
        'ula.TestConfigureULA',
        'ula.TC01_Access_the_VPN_from_the_LAN_allow_Group',
        'ula.TC02_Access_the_VPN_from_the_DMZ_allow_Everyone',
        'ula.TC03_Access_the_VPN_from_the_Custom_Zone_allow_Group',
        'ula.TC04_Access_From_Remote_End_of_the_Tunnel_Deny_All',
        'ula.TC05_Access_VPN_From_LAN_Allow_All',
        'ula.TC06_Access_VPN_From_LAN_Allow_Admin',
        'ula.TC07_Access_VPN_From_LAN_Allow_Everyone',
        'ula.TC08_Access_VPN_From_LAN_Deny_All',
        'ula.TC09_Access_VPN_From_DMZ_Allow_All',
        'ula.TC10_Access_VPN_From_DMZ_Allow_Admin',
        'ula.TC11_Access_VPN_From_DMZ_Deny_All',
        'ula.TC12_Access_VPN_From_DMZ_Allow_Super_Group',
        'ula.TC13_Access_VPN_From_DMZ_Allow_User',
        'ula.TC14_Login_Redirect_Upon_the_VPN_Access_from_Cus_Zone',
        'ula.TC15_Access_VPN_From_Cus_Zone_Allow_All',
        'ula.TC16_Access_VPN_From_Cus_Zone_Allow_Admin',
        'ula.TC17_Access_the_VPN_from_the_Cus_Zone_Allow_Everyone',
        'ula.TC18_Access_VPN_From_Cus_Zone_Allow_User',
        'ula.TC19_Access_VPN_From_Cus_Zone_Deny_All',
        'ula.TC20_Access_VPN_From_Cus_Zone_Allow_Super_Group'

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()