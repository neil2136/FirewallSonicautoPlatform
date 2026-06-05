# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_COMMON_HOME'])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/Network/NAT64_Policies_2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        "definition.init_config_pc",
        "definition.init_config_fw",
        "testcases.nat64_policies.Test_NAT64_TC2",
        "testcases.nat64_policies.Test_NAT64_TC7",
        "testcases.nat64_policies.Test_NAT64_TC15",
        "testcases.nat64_policies.Test_NAT64_TC18",
        "testcases.nat64_policies.Test_NAT64_TC19",
        "testcases.nat64_policies.Test_NAT64_TC20",
        "testcases.nat64_policies.Test_NAT64_TC21",
        "testcases.nat64_policies.Test_NAT64_TC79",
        "testcases.nat64_policies.Test_NAT64_TC80",
        "testcases.nat64_policies.Test_NAT64_TC50",
        "testcases.nat64_policies.Test_NAT64_TC87",
        "testcases.nat64_policies.Test_NAT64_TC51",
        "testcases.nat64_policies.Test_NAT64_TC56",
        "testcases.nat64_policies.Test_NAT64_TC57",
        "testcases.nat64_policies.Test_NAT64_TC58",
        "testcases.nat64_policies.Test_NAT64_TC61",
        "testcases.nat64_policies.Test_NAT64_TC71",
        "testcases.nat64_policies.Test_NAT64_TC73",
        "testcases.nat64_policies.Test_NAT64_TC74",
        "testcases.nat64_policies.Test_NAT64_TC88",
        "testcases.nat64_policies.Test_NAT64_TC3",
        "testcases.nat64_policies.Test_NAT64_TC92",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
