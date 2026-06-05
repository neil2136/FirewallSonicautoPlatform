import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_Version2_Interface_IPv6')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]
                + '/Network/API_Version2_Interface_IPv6/testcases')
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'initial_config.TestConfigFW',
        'interface_ipv6.Test_API_Interface_IPv6_Smoke_01',
        'interface_ipv6.Test_API_Interface_IPv6_Smoke_02',
        'interface_ipv6.Test_API_Interface_IPv6_Smoke_03',
        'interface_ipv6.Test_API_Interface_IPv6_Smoke_04',
        'interface_ipv6.Test_API_Interface_IPv6_Smoke_05',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
