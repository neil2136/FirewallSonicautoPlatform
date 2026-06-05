__author__ = "Pachiyappan Velan"

import sys
import os
import unittest

from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition')
sys.path.append(os.environ['PYTHON_SONICOS_HOME'] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/testcases')


def suite():
    testcases_list = [
        # Restoring DUT
        'config.init_testbed.TestRestoreDUT',

        # Uploading Firmware
        'config.init_testbed.TestUploadFirmware',

        'init_conf_fw.Test_init_LocalFW',
        'init_conf_pc.TestSetup_PCs',
        'enhanced_redirector.TestConfigureULA',

        # # Enhanced HTTP HTTPS Redirector With DP Offload TestCases
        'enhanced_redirector.TC01_Verify_Default_Setting_Of_Three_Options_In_Diag_Page',
        'enhanced_redirector.TC02_Verify_HTTP_Port_Number_and_Changeable_In_Diag_Page',
        'enhanced_redirector.TC05_Verify_Flush_Cached_Files_For_One_Interface_Diag_Page',
        'enhanced_redirector.TC06_Verify_Flush_Cached_Files_For_All_Interface_Diag_Page',
        'enhanced_redirector.TC07_Verify_Error_Returned_For_Changing_Other_Ports_To_10281',
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
