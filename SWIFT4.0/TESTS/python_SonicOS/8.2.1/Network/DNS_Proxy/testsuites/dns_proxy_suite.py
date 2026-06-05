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
        'dns_proxy.Test_18_Enable_DNS_Proxy',
        'dns_proxy.Test_19_DNS_Proxy_4to4_mode',
        'dns_proxy.Test_53_Enable_TCP_support',
        'dns_proxy.Test_58_static_DNS_cache_entry',
        'dns_proxy.Test_49_Enforcement_of_DNS_Proxy',        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
