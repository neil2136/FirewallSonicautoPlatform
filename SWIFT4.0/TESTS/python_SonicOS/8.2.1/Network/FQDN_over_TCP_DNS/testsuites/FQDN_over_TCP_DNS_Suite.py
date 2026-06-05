import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/FQDN_over_TCP_DNS")


def suite():
    testcases_list = [
        "config.init_testbed.TestRestoreDUT",
        "config.init_testbed.TestUploadFirmware",
        "definition.init_conf_pc.TestSetup_PCs",
        "definition.init_conf_fw.TestConfigFW",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Enable_TC01",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Disable_TC02",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Func_V4_TC03",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Func_V4_TC05",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Verify_Logs_TC09",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Verify_TSR_TC11",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Proxy_TC17",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_ACL_TC20",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Multi_TC07",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Multi_TC08",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Split_TC15",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Func_V6_TC04",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Func_V6_TC06",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_CLI_Set_TC12",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Reboot_TC13",
        "testcases.FQDN_over_TCP_DNS.Test_DNS_TCP_Import_EXP_TC14",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == "__main__":
    st = UnittestSuite(sys.argv, suite())
    st.run()
