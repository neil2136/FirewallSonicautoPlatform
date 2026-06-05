import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Auth_Partitions_GUI')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/User/Auth_Partitions_GUI/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'auth_partition_gui.TC01_Auth_Partition',
        'auth_partition_gui.TC02_Auth_Partition',
        'auth_partition_gui.TC03_Auth_Partition',
        'auth_partition_gui.TC04_Auth_Partition',                    
        'auth_partition_gui.TC05_Auth_Partition',
        'auth_partition_gui.TC06_Auth_Partition',               
        'auth_partition_gui.TC07_Auth_Partition',
        'auth_partition_gui.TC08_Auth_Partition',
        'auth_partition_gui.TC09_Auth_Partition',
        'auth_partition_gui.TC10_Auth_Partition',
        'auth_partition_gui.TC11_Auth_Partition',           
        'auth_partition_gui.TC12_Auth_Partition',                
        'auth_partition_gui.TC13_Auth_Partition',                   
        'auth_partition_gui.TC14_Auth_Partition',
        'auth_partition_gui.TC15_Auth_Partition',
        'auth_partition_gui.TC16_Auth_Partition',
        'auth_partition_gui.TC17_Auth_Partition',
        'auth_partition_gui.TC18_Auth_Partition'

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites



if __name__ == '__main__':
    to_users = 'sjogalekar@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()

