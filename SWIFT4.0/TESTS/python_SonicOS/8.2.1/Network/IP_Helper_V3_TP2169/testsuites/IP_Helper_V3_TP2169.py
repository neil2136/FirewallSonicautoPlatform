__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IP_Helper_V3_TP2169')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/IP_Helper_V3_TP2169/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'testcases.IP_Helper_V3_TP2169.Test_01_IP_Helper_V3_TP2169_tc_1510517',
        'testcases.IP_Helper_V3_TP2169.Test_02_IP_Helper_V3_TP2169_tc_1510541',
        'testcases.IP_Helper_V3_TP2169.Test_03_IP_Helper_V3_TP2169_tc_1510557',
        'testcases.IP_Helper_V3_TP2169.Test_04_IP_Helper_V3_TP2169_tc_1510558',
        'testcases.IP_Helper_V3_TP2169.Test_05_IP_Helper_V3_TP2169_tc_1510560',
        'testcases.IP_Helper_V3_TP2169.Test_06_IP_Helper_V3_TP2169_tc_1510525',
        'testcases.IP_Helper_V3_TP2169.Test_07_IP_Helper_V3_TP2169_tc_1510526',
        'testcases.IP_Helper_V3_TP2169.Test_08_IP_Helper_V3_TP2169_tc_1510528',
        'testcases.IP_Helper_V3_TP2169.Test_09_IP_Helper_V3_TP2169_tc_1510530',
        'testcases.IP_Helper_V3_TP2169.Test_10_IP_Helper_V3_TP2169_tc_1510535',
        'testcases.IP_Helper_V3_TP2169.Test_11_IP_Helper_V3_TP2169_tc_1510533',
        'testcases.IP_Helper_V3_TP2169.Test_12_IP_Helper_V3_TP2169_tc_1510542',
        'testcases.IP_Helper_V3_TP2169.Test_13_IP_Helper_V3_TP2169_tc_1510547',
        'testcases.IP_Helper_V3_TP2169.Test_14_IP_Helper_V3_TP2169_tc_1510549',
        'testcases.IP_Helper_V3_TP2169.Test_15_IP_Helper_V3_TP2169_tc_1510550',
        'testcases.IP_Helper_V3_TP2169.Test_16_IP_Helper_V3_TP2169_tc_1510551',
        'testcases.IP_Helper_V3_TP2169.Test_17_IP_Helper_V3_TP2169_tc_1510552',
        'testcases.IP_Helper_V3_TP2169.Test_18_IP_Helper_V3_TP2169_tc_1510553',
        'testcases.IP_Helper_V3_TP2169.Test_19_IP_Helper_V3_TP2169_tc_1510562',
        'testcases.IP_Helper_V3_TP2169.Test_20_IP_Helper_V3_TP2169_tc_1510563',
        'testcases.IP_Helper_V3_TP2169.Test_21_IP_Helper_V3_TP2169_tc_1510564',
        'testcases.IP_Helper_V3_TP2169.Test_22_IP_Helper_V3_TP2169_tc_1510518',
        'testcases.IP_Helper_V3_TP2169.Test_23_IP_Helper_V3_TP2169_tc_1510554',
        'testcases.IP_Helper_V3_TP2169.Test_24_IP_Helper_V3_TP2169_tc_1510565',
        'testcases.IP_Helper_V3_TP2169.Test_25_IP_Helper_V3_TP2169_tc_1510534',
        'testcases.IP_Helper_V3_TP2169.Test_26_IP_Helper_V3_TP2169_tc_1510538',
        'testcases.IP_Helper_V3_TP2169.Test_27_IP_Helper_V3_TP2169_tc_1510536',
        'testcases.IP_Helper_V3_TP2169.Test_28_IP_Helper_V3_TP2169_tc_1510559',
        'testcases.IP_Helper_V3_TP2169.Test_29_IP_Helper_V3_TP2169_tc_1510539',
        'testcases.IP_Helper_V3_TP2169.Test_30_IP_Helper_V3_TP2169_tc_1510527',
        'testcases.IP_Helper_V3_TP2169.Test_31_IP_Helper_V3_TP2169_tc_1510529',
        'testcases.IP_Helper_V3_TP2169.Test_32_IP_Helper_V3_TP2169_tc_1510543',
        'testcases.IP_Helper_V3_TP2169.Test_33_IP_Helper_V3_TP2169_tc_1510544',
        'testcases.IP_Helper_V3_TP2169.Test_34_IP_Helper_V3_TP2169_tc_1510519',
        'testcases.IP_Helper_V3_TP2169.Test_35_IP_Helper_V3_TP2169_tc_1510520',
        'testcases.IP_Helper_V3_TP2169.Test_36_IP_Helper_V3_TP2169_tc_1510521',
        'testcases.IP_Helper_V3_TP2169.Test_37_IP_Helper_V3_TP2169_tc_1510522',
        'testcases.IP_Helper_V3_TP2169.Test_38_IP_Helper_V3_TP2169_tc_1510537',
        'testcases.IP_Helper_V3_TP2169.Test_39_IP_Helper_V3_TP2169_tc_1510548',
        'testcases.IP_Helper_V3_TP2169.Test_40_IP_Helper_V3_TP2169_tc_1532480',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
