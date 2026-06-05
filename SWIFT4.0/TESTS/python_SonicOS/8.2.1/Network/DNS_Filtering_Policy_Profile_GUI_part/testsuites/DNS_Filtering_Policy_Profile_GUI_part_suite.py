# Author: xzhan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Policy_Profile_GUI_part')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521074',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521075',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521076',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521078',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestBoundary_1521079',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521085',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestBoundary_1521086',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521093',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521094',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521095',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestError_1521098',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestError_1521100',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521101',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521103',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521104',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521110',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521022',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestBoundary_1521127',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestBoundary_1521128',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521129',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521130',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestError_1521131',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521132',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestSettings_1521133',
        'testcases.DNS_Filtering_Policy_Profile_GUI_part.TestError_1521134',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
