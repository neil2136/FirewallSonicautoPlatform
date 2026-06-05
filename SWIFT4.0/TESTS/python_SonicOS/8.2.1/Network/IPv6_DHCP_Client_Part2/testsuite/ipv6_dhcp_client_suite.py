# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_Part2')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_pc',
        'definition.init_config_fw',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC3',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC6',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC7',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC8',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC9',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC40',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC41',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC44',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC10',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC22',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC18',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC19',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC20',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC21',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC24',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC25',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC26',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC31',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC32',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC33',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC34',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC38',
        'testcases.ipv6_dhcp_client.Test_IPv6_Client_TC39',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
