import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/definition')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_tb.TestConfigTB_00',
        'definition.conf_tb.TestConfigTB_02',
        'E_cli_filename_transport.Test_01_FTP',
        'E_cli_filename_transport.Test_02_FTP',
        'E_cli_filename_transport.Test_03_FTP',
        'E_cli_filename_transport.Test_04_FTP',
        'E_cli_filename_transport.Test_05_FTP',
        'E_cli_filename_transport.Test_06_FTP',
      
    ]
    
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites
    
if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()
