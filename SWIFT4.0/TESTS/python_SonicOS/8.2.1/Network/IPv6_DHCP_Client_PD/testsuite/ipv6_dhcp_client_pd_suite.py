# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_DHCP_Client_PD')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_pc',
        'definition.init_config_fw',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC001',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC002',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC051',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC052',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC003',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC005',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC013',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC006',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC009',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC010',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC011',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC007',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC008',
        'testcases.ipv6_dhcp_client_pd_part1.Test_Update_PD',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC019',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC020',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC021',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC022',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC023',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC024',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC025',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC015',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC016',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC017',
        'testcases.ipv6_dhcp_client_pd_part1.Test_IPv6_PD_TC018',
        'config.init_testbed.TestRestoreDUT',
        'definition.init_config_pc',
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC101",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC012",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC102",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC103",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC104",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC105",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC107",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC111",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC112",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC114",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC115",
        "testcases.ipv6_dhcp_client_pd_part2.Test_IPv6_PD_TC113",
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
