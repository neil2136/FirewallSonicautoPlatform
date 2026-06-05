import sys
import os
sys.argv.append(' -noapi')
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Webproxy_813/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigFW',
        'webproxy.TestWebproxy_add_lan_route',
        'webproxy.TestWebproxy_01', 'webproxy.TestWebproxy_02', 'webproxy.TestWebproxy_03', 'webproxy.TestWebproxy_12', 'webproxy.TestWebproxy_13',
        'webproxy.TestWebproxy_15', 'webproxy.TestWebproxy_11',
        'webproxy.TestWebproxy_del_lan_route',
        'webproxy.TestWebproxy_add_dmz_route',
        'webproxy.TestWebproxy_10', 'webproxy.TestWebproxy_04', 'webproxy.TestWebproxy_14',
        'webproxy.TestWebproxy_05', 'webproxy.TestWebproxy_08', 'webproxy.TestWebproxy_09',
        'webproxy.TestWebproxy_del_dmz_route',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
