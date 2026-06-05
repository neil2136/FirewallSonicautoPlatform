# __author__: cyuan


import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/DNS_Tunnel_Detect')


def suite():
    testcase_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC13',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC20',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC28',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC29',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC27',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC32',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC33',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC40',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC42',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC43',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC44',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC64',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC82',
        'testcases.dns_tunnel_detect.TestDNSTunnel_TC83',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcase_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
