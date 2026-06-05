# __author__: cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME']+'/Network/IPv6_VLAN_2')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.ipv6_vlan.TestV6Vlan_TC1',
        'testcases.ipv6_vlan.TestV6Vlan_TC13',
        'testcases.ipv6_vlan.TestV6Vlan_TC16',
        'testcases.ipv6_vlan.TestV6Vlan_TC17',
        'testcases.ipv6_vlan.TestV6Vlan_TC19',
        'testcases.ipv6_vlan.TestV6Vlan_TC14',
        'testcases.ipv6_vlan.TestV6Vlan_TC15',
        'testcases.ipv6_vlan.TestV6Vlan_TC23',
        'testcases.ipv6_vlan.TestV6Vlan_TC24',
        'testcases.ipv6_vlan.TestV6Vlan_TC35',
        'testcases.ipv6_vlan.TestV6Vlan_TC40',
        'testcases.ipv6_vlan.TestV6Vlan_TC41',
        'testcases.ipv6_vlan.TestV6Vlan_TC42'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()