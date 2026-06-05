import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke')





def suite():
    testcases_list = [
    
       'config.init_testbed.TestRestoreDUT',
       'config.init_testbed.TestUploadFirmware',
       'definition.conf_fw.TestConfigTB',
       'tunnel_interface_api.tunnelvpn_68',
       'tunnel_interface_api.tunnelvpn_70',
       'tunnel_interface_api.tunnelvpn_71',
       'tunnel_interface_api.tunnelvpn_83',
       'tunnel_interface_api.tunnelvpn_93',
       'tunnel_interface_api.tunnelvpn_94',
       'tunnel_interface_api.tunnelvpn_101',
       'tunnel_interface_api.tunnelvpn_78',
       

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'ujkumar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

