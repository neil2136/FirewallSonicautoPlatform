# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_Gre4to6_Tunnel')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC02",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC01",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC03",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC05",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC13",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523876",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523877",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523878",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523879",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC2682750",
        #
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523869",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523871",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523872",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC2682749",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523870",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523873",
        "testcases.ipv6_gre4to6_tunnel.Test_GRE4to6_TC1523875",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
