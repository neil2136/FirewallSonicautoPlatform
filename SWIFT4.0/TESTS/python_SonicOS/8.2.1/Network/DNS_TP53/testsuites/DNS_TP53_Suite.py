# __Author__: lezhang
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_TP53/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_dns_server',
        'definition.initial_config_fw',
        'testcases.DNS_TP53.TestDNS_01',
        'testcases.DNS_TP53.TestDNS_02',
        'testcases.DNS_TP53.TestDNS_04',
        'testcases.DNS_TP53.TestDNS_05',
        'testcases.DNS_TP53.TestDNS_06',
        'testcases.DNS_TP53.TestDNS_07',
        'testcases.DNS_TP53.TestDNS_09',
        'testcases.DNS_TP53.TestDNS_10',
        'testcases.DNS_TP53.TestDNS_11',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
