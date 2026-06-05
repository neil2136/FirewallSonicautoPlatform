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

        # Enhanced HTTP HTTPS Redirector With DP Offload TestCases
        'enhanced_redirector.TC08_Verify_HTTP_Login_Allowed_And_HTTP_Redirect_With_No_SSO_Involved',
        'enhanced_redirector.TC09_Verify_HTTP_Login_Allowed_And_HTTPS_Redirect_With_No_SSO_Involved',
        'enhanced_redirector.TC03_Verify_Redirect_HTTP_After_Disable_DP_Offload_Diag_Page',
        'enhanced_redirector.TC04_Verify_Redirect_HTTPS_After_Disable_DP_Offload_Diag_Page',
        'enhanced_redirector.TC10_Verify_HTTP_Login_Allowed_And_HTTP_Redirect_With_No_SSO_Involved',
        'enhanced_redirector.TC11_Verify_HTTP_Login_Allowed_And_HTTPS_Redirect_With_No_SSO_Involved'
    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
