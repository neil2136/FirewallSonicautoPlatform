
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(
    os.environ["PYTHON_SONICOS_HOME"] + "/User/CFS_with_User"
)


def suite():
    testcases_list = [
        "config.init_testbed.TestRestoreDUT",
        "config.init_testbed.TestUploadFirmware",
        "definition.init_conf_pc.TestSetup_PCs",
        "definition.init_conf_fw.TestConfigFW",
        "testcases.CFS_Policy_Function.Test_CFS_Profile_TC145",
        "testcases.CFS_Policy_Function.Test_CFS_Profile_TC149",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC198",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC199",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC203",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC204",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC197",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC200",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC201",
        "testcases.CFS_Policy_Function.Test_CFS_User_TC205",
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == "__main__":
    st = UnittestSuite(sys.argv, suite())
    st.run()
