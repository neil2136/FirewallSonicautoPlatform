import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Proxy/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigENV',
        'dns_proxy_1.Test_check_DNS_Proxy',
        'dns_proxy_1.Test_enable_DNS_Proxy',
        'dns_proxy_1.Test_enable_DNS_cache',
        'dns_proxy_1.Test_check_dns_status_interface',
        'dns_proxy_1.Test_check_dns_status_interface_proxy',
        'dns_proxy_1.Test_DNS_Proxy_4to4_Mode',
        'dns_proxy_1.Test_Check_Default_Access_Rule',
        'dns_proxy_1.Test_Delete_Dns_Cache',
        'dns_proxy_1.Test_Flush_Cache'
        
        
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()
