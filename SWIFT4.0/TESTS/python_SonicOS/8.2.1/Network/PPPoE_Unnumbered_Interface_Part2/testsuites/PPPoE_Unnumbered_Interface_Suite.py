# __author__: yzhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + "/Network/PPPoE_Unnumbered_Interface_Part2"
)


def suite():
    testcases_list = [
        "config.init_testbed.TestRestoreDUT",
        "config.init_testbed.TestUploadFirmware",
        "definition.init_conf_pc.TestSetup_PCs",
        "definition.init_conf_fw.TestConfigFW",
        "testcases.PPPoE_Unnumbered_Interface.Test_Config_TC06",
        "testcases.PPPoE_Unnumbered_Interface.Test_Traffic_TC18",
        "testcases.PPPoE_Unnumbered_Interface.Test_MGMT_TC19",
        "testcases.PPPoE_Unnumbered_Interface.Test_MGMT_TC23",
        "testcases.PPPoE_Unnumbered_Interface.Test_Operate_TC25",
        "testcases.PPPoE_Unnumbered_Interface.Test_Operate_TC27",
        "testcases.PPPoE_Unnumbered_Interface.Test_Modify_Config_TC29",
        "testcases.PPPoE_Unnumbered_Interface.Test_Modify_Config_TC30",
        "testcases.PPPoE_Unnumbered_Interface.Test_Modify_Config_TC32",
        "testcases.PPPoE_Unnumbered_Interface.Test_Modify_Config_TC40",
        "testcases.PPPoE_Unnumbered_Interface.Test_Reboot_TC71",
        "testcases.PPPoE_Unnumbered_Interface.Test_TSR_TC72",
        "testcases.PPPoE_Unnumbered_Interface.Test_EXP_TC73",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == "__main__":
    st = UnittestSuite(sys.argv, suite())
    st.run()
