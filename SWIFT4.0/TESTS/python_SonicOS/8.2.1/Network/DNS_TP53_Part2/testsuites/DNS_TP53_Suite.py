# __Author__: lezhang
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_TP53_Part2/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'config.init_testbed.TestRestoreDUT',
        'testcases.DNS_TP53.TestDNS_3830207', 
        'testcases.DNS_TP53.TestDNS_3932088', 
        'testcases.DNS_TP53.TestDNS_3912897', 
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
