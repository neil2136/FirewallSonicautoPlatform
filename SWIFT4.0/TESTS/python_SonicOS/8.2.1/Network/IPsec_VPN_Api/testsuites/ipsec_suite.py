import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPsec_VPN_Api')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPsec_VPN_Api/testcases')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ipsec_api.TC00_NonTC',
        'ipsec_api.TC01_check_site_to_site_manual',
        'ipsec_api.TC02_edit_site_to_site_vpn_local_network',
        'ipsec_api.TC03_edit_translated_local_network',
        'ipsec_api.TC04_edit_translated_local_network',
        'ipsec_api.TC05_edit_vpn_policy_base',
        'ipsec_api.TC06_create_vpn_policy_auth_md5_phase2',
        'ipsec_api.TC07_edit_authentication_SHA1',
        'ipsec_api.TC08_create_ipsec_with_translated_local_ntw',
        'ipsec_api.TC09_create_ipsec_with_host_in_translated_local_ntw'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

