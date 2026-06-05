__author__ = "Pachiyappan Velan"

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        # Restoring DUT
        'config.init_testbed.TestRestoreDUT',
        #
        # # Uploading Firmware
        'config.init_testbed.TestUploadFirmware',

        'definition.conf_fw.TestConfigTB'

        # SSO by RADIUS Accounting testcases
#   Maximum RADIUS Accounting Client count differs by platform:
#   - TZ devices: max 4 clients
#   - NSA devices: higher limits (vary by model), Hence commenting below testcase
        # 'SSO_by_Radius_Accounting.TC01_Verify_Add_Maximum_RADIUS_Accounting_Client_Client_List',
        'SSO_by_Radius_Accounting.TC02_Verify_Edit_RADIUS_Accounting_Client_UI',
        'SSO_by_Radius_Accounting.TC03_Verify_Add_Same_RADIUS_Accounting_Client_UI',
        'SSO_by_Radius_Accounting.TC04_Verify_Duplicate_IP_Name_Forwarding_Server_Check',
        'SSO_by_Radius_Accounting.TC05_Verify_Port_No_Boundary_Test_With_Forwarding_Server',
        'SSO_by_Radius_Accounting.TC06_Verify_Timeout_Boundary_Test_With_Forwarding_Server',
        'SSO_by_Radius_Accounting.TC07_Verify_Retries_Boundary_Test_With_Forwarding_Server',
        'SSO_by_Radius_Accounting.TC08_Verify_Interim_Update_Boundary_Test_With_RADIUS_Accounting_Client',
        'SSO_by_Radius_Accounting.TC09_Verify_Add_RADIUS_Accounting_Client_With_Default_Partition',
        'SSO_by_Radius_Accounting.TC10_Verify_Client_Name_Max_Len_Check',
        'SSO_by_Radius_Accounting.TC11_Verify_Client_Name_Exceed_Max_Len_Check',
        'SSO_by_Radius_Accounting.TC12_Verify_Illegal_Chars_Check_Client_Name',
        'SSO_by_Radius_Accounting.TC13_Verify_Js_SQL_Inj_With_All_Fields',
        'SSO_by_Radius_Accounting.TC14_Verify_Show_Partition_Option'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
