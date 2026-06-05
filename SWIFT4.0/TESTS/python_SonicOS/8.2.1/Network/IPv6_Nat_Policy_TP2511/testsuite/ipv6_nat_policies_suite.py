# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/IPv6_Nat_Policy_TP2511')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        "definition.init_config_fw",
        "definition.init_config_pc",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC1",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC19",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC28",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC23",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC4",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC8",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC9",
        "testcases.ipv6_nat_policies.Test_V6NAT_TC44",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
