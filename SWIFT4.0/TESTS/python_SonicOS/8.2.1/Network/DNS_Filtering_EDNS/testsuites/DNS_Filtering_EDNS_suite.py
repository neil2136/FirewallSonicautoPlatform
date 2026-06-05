# Author: xzhan
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_EDNS')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_EDNS.Test_Category_to_Client',
        'testcases.DNS_Filtering_EDNS.Test_Resp_Category_Cache',
        'testcases.DNS_Filtering_EDNS.Test_Resp_Category_Sent_by_FW',
        'testcases.DNS_Filtering_EDNS.Test_without_Additional_RRs',
        'testcases.DNS_Filtering_EDNS.Test_Disable_without_RRs',
        'testcases.DNS_Filtering_EDNS.Test_Disable_Resp_Category_Cache'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
