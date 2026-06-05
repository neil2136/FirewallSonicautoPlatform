import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/IPv6_Network_Monitor/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_env.TestConfigENV',
        'ipv6_network_monitor.Test_06_Check_Route',
        'ipv6_network_monitor.Test_10_Check_TCP_Explicit_Route',
        'ipv6_network_monitor.Test_26_IPv6_probe',
        'ipv6_network_monitor.Test_44_Verify_Monitor_Status',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()