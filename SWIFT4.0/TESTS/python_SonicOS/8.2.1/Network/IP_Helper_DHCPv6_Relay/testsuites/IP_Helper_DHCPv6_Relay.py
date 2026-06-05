import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IP_Helper_DHCPv6_Relay')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IP_Helper_DHCPv6_Relay/testcases')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'IP_Helper_DHCPv6_Relay_tc.TC01_IP_Helper_DHCPv6_Relay', 
        'IP_Helper_DHCPv6_Relay_tc.TC02_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC03_IP_Helper_DHCPv6_Relay',  
        'IP_Helper_DHCPv6_Relay_tc.TC04_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC05_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC06_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC07_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC08_IP_Helper_DHCPv6_Relay', 
        'IP_Helper_DHCPv6_Relay_tc.TC09_IP_Helper_DHCPv6_Relay',    
        'IP_Helper_DHCPv6_Relay_tc.TC10_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC11_IP_Helper_DHCPv6_Relay',
        'IP_Helper_DHCPv6_Relay_tc.TC12_IP_Helper_DHCPv6_Relay',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'gkatti@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite())
    st.run()
