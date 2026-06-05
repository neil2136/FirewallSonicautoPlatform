import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/dhcp_over_vpn/dhcp_sanity_cases/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/dhcp_over_vpn/dhcp_sanity_cases')



def suite():
    testcases_list = [
      'config.init_testbed.TestRestoreDUT',
      'config.init_testbed.TestUploadFirmware',
      'definition.conf_fw.TestConfigTB',
      'dhcp_sanity.dhcp_central_01',
      'dhcp_sanity.dhcp_central_02',
      'dhcp_sanity.dhcp_remote_03',
      'dhcp_sanity.dhcp_remote_04'
    

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'ujkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

