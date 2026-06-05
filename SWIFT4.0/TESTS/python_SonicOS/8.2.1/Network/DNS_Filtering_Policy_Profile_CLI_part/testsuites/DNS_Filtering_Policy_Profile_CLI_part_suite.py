# Author: xzhan
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Policy_Profile_CLI_part')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_duplicate_profile',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_show_profiles',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_add_dns_proxy_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_add_dns_filter_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_edit_dns_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_disable_dns_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_enable_dns_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_config_conn_limit_and_max_conn',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_clone_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_show_dns_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_delete_one_dns_policy',
        'testcases.DNS_Filtering_Policy_Profile_CLI_part.Test_delete_all_dns_policy'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
