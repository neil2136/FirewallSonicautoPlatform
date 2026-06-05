import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/dhcp_over_vpn/dhcp_smoke_cases/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/dhcp_over_vpn/dhcp_smoke_cases')



def suite():
    testcases_list = [
       
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
       'definition.conf_fw.TestConfigTB',
       'dhcp_api.dhcp_01',
       'dhcp_api.dhcp_02',
       'dhcp_api.dhcp_03',
       'dhcp_api.dhcp_04',
       'dhcp_api.dhcp_05',
       'dhcp_api.dhcp_06',
       'dhcp_api.dhcp_07',
       'dhcp_api.dhcp_08'

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'sbkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

