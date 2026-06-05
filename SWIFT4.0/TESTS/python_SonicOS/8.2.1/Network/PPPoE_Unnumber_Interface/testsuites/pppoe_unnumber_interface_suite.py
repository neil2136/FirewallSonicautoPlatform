import sys
import os
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/PPPoE_Unnumber_Interface/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list=[
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'conf_fw.TestConfigENV',
        'pppoe_unnumber_interface.Test_12_Verify_Unnumbered_Interface',
        'pppoe_unnumber_interface.Test_15_Verify_NAT_Policy',
        'pppoe_unnumber_interface.Test_16_Verify_ping_FTP_HTTPS',
        'pppoe_unnumber_interface.Test_20_Verify_Management',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)    
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()