__author__ = "Pachiyappan Velan"

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_1')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_1/definition')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_1/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        # Restoring DUT
        'config.init_testbed.TestRestoreDUT',

        # Uploading Firmware
        'config.init_testbed.TestUploadFirmware',

        # Config Interface on UTM
        'conf_fw.TestConfigTB',

        # SSO by RADIUS Accounting testcases
        'SSO_by_Radius_Accounting.TC01_Verify_Edit_RADIUS_Accounting_Client_Client_List',
        'SSO_by_Radius_Accounting.TC02_Verify_Empty_Input_Check_In_RADIUS_Accounting_Client',
        'SSO_by_Radius_Accounting.TC03_Verify_TSR_RADIUS_Accounting_Client',
        'SSO_by_Radius_Accounting.TC04_Verify_Client_Name_With_Special_Character',
        'SSO_by_Radius_Accounting.TC05_Verify_Special_Forwarding_Server_IP_Check_Radius_Acc_Client',
        'SSO_by_Radius_Accounting.TC06_Verify_Invalid_IP_Check_Radius_Acc_Client',
        'SSO_by_Radius_Accounting.TC07_Verify_Closing_RADIUS_Acc_Client_Window',
        'SSO_by_Radius_Accounting.TC08_Verify_Check_Shared_Secret_Not_Match_Error',
        'SSO_by_Radius_Accounting.TC09_Verify_Invalid_IP_Address_With_Forwarding_Server',
        'SSO_by_Radius_Accounting.TC10_Verify_Special_IP_Check_Radius_Acc_Client',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
