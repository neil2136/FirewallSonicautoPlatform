import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Log/Log_Monitor_New_TP2582/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.setup_mail_server',
        'testcases.Log_Monitor_New_TP2582.TestLog_Monitor_12', 
        'testcases.Log_Monitor_New_TP2582.TestLog_Monitor_13', 
        'testcases.Log_Monitor_New_TP2582.TestLog_Monitor_16', 
        'testcases.Log_Monitor_New_TP2582.TestLog_Monitor_26', 
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
