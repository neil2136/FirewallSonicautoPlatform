# __author__: cyuan

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] +
                '/Network/NAT_Disable_Source_Port_Remap')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC1',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC2',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC3',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC5',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC6',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC11',
        'testcases.nat_disable_source_port_remap.TestNatPortRemap_TC16',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
