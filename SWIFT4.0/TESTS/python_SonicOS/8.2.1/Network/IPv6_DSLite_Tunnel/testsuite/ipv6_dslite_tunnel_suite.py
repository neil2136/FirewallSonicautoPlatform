# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_DSLite_Tunnel')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC2682744',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC2682745',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529345',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529357',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529358',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529359',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC2682743',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529346',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529348',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529350',
        'testcases.ipv6_dslite_tunnel.Test_DSLite_TC1529351',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
