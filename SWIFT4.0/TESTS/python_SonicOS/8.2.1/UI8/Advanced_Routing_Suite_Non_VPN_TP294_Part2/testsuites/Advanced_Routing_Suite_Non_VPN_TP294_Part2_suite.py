# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/UI8')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/UI8/Advanced_Routing_Suite_Non_VPN_TP294_Part2')

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'bin.init_resource.FWConfigure',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.Test_OSPFv2_edit_page',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestOSPFv2_edit_page_001', # 1531393
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestOSPFv2_edit_page_002', # 1531397
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.Test_Settings_page',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_001',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_002',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_003',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_004',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_005',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_006',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_007',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_008',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestSettings_page_009',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.Test_RIP_page',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestRIP_page_001',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestRIP_page_002',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestRIP_page_003',
        'testcases.Advanced_Routing_Suite_Non_VPN_TP294_Part2.TestRIP_page_004',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
