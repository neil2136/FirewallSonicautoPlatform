# Author: xzhan
import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Filtering_ACL')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_pc_configure.TestConfigPC',
        'definition.init_fw_configure.TestConfigFW',
        'testcases.DNS_Filtering_ACL.Test_acl_auto_added',
        'testcases.DNS_Filtering_ACL.Test_acl_not_changed',
        'testcases.DNS_Filtering_ACL.Test_acl_disable_enable',
        'testcases.DNS_Filtering_ACL.Test_acl_deleted',
        'testcases.DNS_Filtering_ACL.Test_acl_changes'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
