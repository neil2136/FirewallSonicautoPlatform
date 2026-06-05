# __author__: cyuan


import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/DNS_Tunnel_Detect_Part2')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC1',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC2',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC3',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC4',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC7',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC8',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC9',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC21',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC22',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC23',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC26',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC24',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC25',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC30',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC31',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC34',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC37',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC35',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC36',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC38',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC39',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC45',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC47',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC57',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC59',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC65',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC66',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC68',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC69',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC70',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC72',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC73',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC74',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC75',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC76',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC77',
        'testcases.dns_tunnel_detect_part2.TestDNSTunnel_TC84'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
