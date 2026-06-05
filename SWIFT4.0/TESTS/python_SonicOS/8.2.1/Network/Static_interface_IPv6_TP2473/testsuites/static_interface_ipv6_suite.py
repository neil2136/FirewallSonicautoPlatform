# __author__: cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] +
                '/Network/Static_interface_IPv6_TP2473')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw.TestConfig_RemFW',
        'definition.init_config_fw.TestConfig_LocalFW',
        'definition.init_config_pc',
        'testcases.static_interface_ipv6.TestV6If_TC39',
        'testcases.static_interface_ipv6.TestV6If_TC36',
        'testcases.static_interface_ipv6.TestV6If_TC01',
        'testcases.static_interface_ipv6.TestV6If_TC11',
        'testcases.static_interface_ipv6.TestV6If_TC25',
        'testcases.static_interface_ipv6.TestV6If_TC33',
        'testcases.static_interface_ipv6.TestV6If_TC4',
        'testcases.static_interface_ipv6.TestV6If_TC9',
        'config.init_testbed.TestRestoreDUT',
        'testcases.static_interface_ipv6.TestV6If_TC24',
        'testcases.static_interface_ipv6.TestV6If_TC31',
        'testcases.static_interface_ipv6.TestV6If_TC41',
        'testcases.static_interface_ipv6.TestV6If_1533076',
        'testcases.static_interface_ipv6.TestV6If_TC10',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
