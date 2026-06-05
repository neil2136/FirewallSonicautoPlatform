# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_Network_Monitor_Part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56627',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56631',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56630',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56633',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56634',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56636',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56635',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56637',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56638',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56628',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56639',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56629',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56626',
        'testcases.ipv6_network_monitor.Test_V6NM_Policy_TC56632',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
