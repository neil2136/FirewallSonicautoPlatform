# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay_Full')

"""
pc3--(X2)DUT(X3)--------(X3)Server
pc3 as dhcpv6 client
"""

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514142",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514143",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514144",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514146",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514147",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514149",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514150",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514151",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514152",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514160",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514161",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514153",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514154",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514155",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514156",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514169",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514182",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514184",
        "testcases.dhcpv6_relay.Test_DHCPv6_Relay_TC1514157",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
