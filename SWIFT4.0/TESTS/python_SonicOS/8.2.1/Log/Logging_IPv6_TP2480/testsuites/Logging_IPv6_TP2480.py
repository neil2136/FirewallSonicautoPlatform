__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Log/Logging_IPv6_TP2480')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Log/Logging_IPv6_TP2480/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_env.TestConfigTB_01',
        'definition.setup_env.TestConfigTB_02',
        'testcases.Logging_IPv6_TP2480.Test_01_Logging_IPv6_TP2480_tc_11',
        'testcases.Logging_IPv6_TP2480.Test_02_Logging_IPv6_TP2480_tc_12',
        'testcases.Logging_IPv6_TP2480.Test_03_Logging_IPv6_TP2480_tc_17',
        'testcases.Logging_IPv6_TP2480.Test_04_Logging_IPv6_TP2480_tc_18',
        'testcases.Logging_IPv6_TP2480.Test_05_Logging_IPv6_TP2480_tc_20',
        'testcases.Logging_IPv6_TP2480.Test_06_Logging_IPv6_TP2480_tc_27',
        'testcases.Logging_IPv6_TP2480.Test_07_Logging_IPv6_TP2480_tc_29',
        'testcases.Logging_IPv6_TP2480.Test_08_Logging_IPv6_TP2480_tc_3',
        'testcases.Logging_IPv6_TP2480.Test_09_Logging_IPv6_TP2480_tc_30',
        'testcases.Logging_IPv6_TP2480.Test_10_Logging_IPv6_TP2480_tc_35',
        'testcases.Logging_IPv6_TP2480.Test_11_Logging_IPv6_TP2480_tc_4',
        'testcases.Logging_IPv6_TP2480.Test_12_Logging_IPv6_TP2480_tc_5',
        'testcases.Logging_IPv6_TP2480.Test_13_Logging_IPv6_TP2480_tc_6',
        'testcases.Logging_IPv6_TP2480.Test_14_Logging_IPv6_TP2480_tc_7',
        'testcases.Logging_IPv6_TP2480.Test_15_Logging_IPv6_TP2480_tc_8',
        'testcases.Logging_IPv6_TP2480.Test_16_Logging_IPv6_TP2480_tc_9',
        'testcases.Logging_IPv6_TP2480.Test_17_Logging_IPv6_TP2480_tc_2',
        'testcases.Logging_IPv6_TP2480.Test_18_Logging_IPv6_TP2480_tc_37',
        'testcases.Logging_IPv6_TP2480.Test_19_Logging_IPv6_TP2480_tc_38',
        'testcases.Logging_IPv6_TP2480.Test_20_Logging_IPv6_TP2480_tc_40',
        'testcases.Logging_IPv6_TP2480.Test_21_Logging_IPv6_TP2480_tc_41',
        'testcases.Logging_IPv6_TP2480.Test_22_Logging_IPv6_TP2480_tc_43',

    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
