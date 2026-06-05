import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_Interface')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'bin.conf_fw',
        'testcases.tunnel_interface_tc.TestTunnel_Interface_01',
        'definition.set_test_env.TestAddTunnel',
        'testcases.tunnel_interface_tc.TestTunnel_Interface_02',
        'testcases.tunnel_interface_tc.TestTunnel_Interface_03',
        #'testcases.tunnel_interface_tc.TestTunnel_Interface_04',
        'testcases.tunnel_interface_tc.TestTunnel_Interface_09',
        'definition.set_test_env.TestDelTunnel',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
