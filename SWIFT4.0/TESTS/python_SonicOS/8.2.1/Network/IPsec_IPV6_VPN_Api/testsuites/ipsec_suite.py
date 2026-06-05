import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPsec_IPV6_VPN_Api')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IPsec_IPV6_VPN_Api/testcases')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'ipsec_api.TC00_NonTC',
        'ipsec_api.TC01_create_ipv6vpnpolicy_manual',
        'ipsec_api.TC02_edit_ipv6vpnpolicy_manual',
        'ipsec_api.TC03_Delete_ipv6_vpn_policy',
        'ipsec_api.TC04_create_ipv6vpnpolicy_with_Local_IKE_ID',
        'ipsec_api.TC05_edit_ipv6policy_with_Local_IKE_ID',
        'ipsec_api.TC06_create_ipv6vpn_with_remote_ntw',
        'ipsec_api.TC07_edit_vpnpolicy_Distinguished_name',
        'ipsec_api.TC08_create_ipv6vpnpolicy_remote_add_obj',
        'ipsec_api.TC09_edit_local_ntw_addr_obj',
        'ipsec_api.TC10_create_ipv6vpn_remote_range_addr_obj',
        'ipsec_api.TC11_create_ipv6vpn_Encrypt_DES_phase2',
        'ipsec_api.TC12_edit_ipv6vpn_SHA1_phase2',
        'ipsec_api.TC13_create_ipv6vpn_DES_phase2'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

