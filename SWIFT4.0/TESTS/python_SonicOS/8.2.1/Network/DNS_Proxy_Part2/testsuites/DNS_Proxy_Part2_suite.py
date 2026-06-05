# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Proxy_Part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.DNS_Proxy_Part2.TestGUI_1526805',
        'testcases.DNS_Proxy_Part2.TestGUI_2268490',
        'testcases.DNS_Proxy_Part2.TestGUI_1526813',
        'testcases.DNS_Proxy_Part2.TestGUI_1526831',
        'testcases.DNS_Proxy_Part2.TestFunc_1526816',
        'testcases.DNS_Proxy_Part2.TestFunc_1526823',
        'testcases.DNS_Proxy_Part2.TestFunc_1526824',
        'testcases.DNS_Proxy_Part2.TestFunc_1526825',
        'testcases.DNS_Proxy_Part2.TestFunc_1526828',
        'testcases.DNS_Proxy_Part2.TestFunc_1526827',
        'testcases.DNS_Proxy_Part2.TestGUI_1526834',
        'testcases.DNS_Proxy_Part2.TestGUI_1526835',
        'testcases.DNS_Proxy_Part2.TestGUI_1526833',
        'testcases.DNS_Proxy_Part2.TestFunc_1526810',
        'testcases.DNS_Proxy_Part2.TestFunc_1526830',
        'testcases.DNS_Proxy_Part2.TestBoundary_1526821',
        'testcases.DNS_Proxy_Part2.TestFunc_1526817',
        'testcases.DNS_Proxy_Part2.TestFunc_2694338',
        'testcases.DNS_Proxy_Part2.TestFunc_1532704',
        'testcases.DNS_Proxy_Part2.TestFunc_1526839',
        'testcases.DNS_Proxy_Part2.TestFunc_1526836',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
