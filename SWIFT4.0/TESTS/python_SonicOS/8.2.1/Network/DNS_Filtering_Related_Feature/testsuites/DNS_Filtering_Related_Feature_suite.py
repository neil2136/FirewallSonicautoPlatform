# Author: xzhan
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_Related_Feature')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC.test_01_config_PC1_route',
        'definition.init_fw_configure.TestConfigFW',
        'definition.init_pc_configure.TestConfigPC.test_02_check_dns_server',
        'testcases.DNS_Filtering_Related_Feature.Test_licensed',
        'testcases.DNS_Filtering_Related_Feature.Test_DNS_Sinkhole_prior',
        'testcases.DNS_Filtering_Related_Feature.Test_DNS_Lookup_bypass',
        'testcases.DNS_Filtering_Related_Feature.Test_FQDN_bypass',
        'testcases.DNS_Filtering_Related_Feature.Test_PING_Lookup_bypass',
        'testcases.DNS_Filtering_Related_Feature.Test_Split_DNS_bypass',
        'testcases.DNS_Filtering_Related_Feature.Test_import_and_export',
        'testcases.DNS_Filtering_Related_Feature.Test_reboot'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
