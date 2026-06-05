import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Network/Advance_Switch_Link_Aggregation_TP2460")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_env.TestInitConfig',
        'testcases.Advance_Switch_Link_Aggregation_TP2460.Test_1_Verify_manual_key_during_LAG_Port_cnfiguration',
        'testcases.Advance_Switch_Link_Aggregation_TP2460.Test_2_Verify_additional_VLANs_canbe_added_deleted_on_the_LAG',
        'testcases.Advance_Switch_Link_Aggregation_TP2460.Test_3_Prefs_importandExport_with_two_or_more_LAGs'
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

