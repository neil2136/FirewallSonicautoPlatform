# __author__: yzhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/PPPoE_Unnumbered_Interface_Part3"
)


def suite():
    testcases_list = [
        "config.init_testbed.TestRestoreDUT",
        "config.init_testbed.TestUploadFirmware",
        "definition.init_conf_pc.TestSetup_PCs",
        "definition.init_conf_fw.TestConfigFW",
        "testcases.PPPoE_Unnumbered_Interface.Test_Config_TC02",
        "testcases.PPPoE_Unnumbered_Interface.Test_MGMT_TC21",
        "testcases.PPPoE_Unnumbered_Interface.Test_Config_TC37",
        "testcases.PPPoE_Unnumbered_Interface.Test_Config_TC43",
        "testcases.PPPoE_Unnumbered_Interface.Test_Traffic_TC17",
        "testcases.PPPoE_Unnumbered_Interface.Test_DHCP_TC50",
        "testcases.PPPoE_Unnumbered_Interface.Test_DHCP_TC51",
        "testcases.PPPoE_Unnumbered_Interface.Test_Traffic_TC39",
        "testcases.PPPoE_Unnumbered_Interface.Test_Traffic_TC24",
        "testcases.PPPoE_Unnumbered_Interface.Test_Traffic_TC41",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == "__main__":
    st = UnittestSuite(sys.argv, suite())
    st.run()
