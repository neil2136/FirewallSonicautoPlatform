__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WAN_Failover_and_Load_Balancing_TP2201_part1')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WAN_Failover_and_Load_Balancing_TP2201_part1/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'definition.set_env.TestConfigTB_02',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_01_WAN_Failover_and_Load_Balancing_TP2201_tc_1',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_02_WAN_Failover_and_Load_Balancing_TP2201_tc_4',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_03_WAN_Failover_and_Load_Balancing_TP2201_tc_5',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_04_WAN_Failover_and_Load_Balancing_TP2201_tc_6',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_05_WAN_Failover_and_Load_Balancing_TP2201_tc_7',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_06_WAN_Failover_and_Load_Balancing_TP2201_tc_8',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_07_WAN_Failover_and_Load_Balancing_TP2201_tc_10',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_08_WAN_Failover_and_Load_Balancing_TP2201_tc_12',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_09_WAN_Failover_and_Load_Balancing_TP2201_tc_13',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_10_WAN_Failover_and_Load_Balancing_TP2201_tc_14',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_11_WAN_Failover_and_Load_Balancing_TP2201_tc_15',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_12_WAN_Failover_and_Load_Balancing_TP2201_tc_16',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_13_WAN_Failover_and_Load_Balancing_TP2201_tc_17',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_14_WAN_Failover_and_Load_Balancing_TP2201_tc_18',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_15_WAN_Failover_and_Load_Balancing_TP2201_tc_35',
        # 'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_16_WAN_Failover_and_Load_Balancing_TP2201_tc_185',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_17_WAN_Failover_and_Load_Balancing_TP2201_tc_186',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_18_WAN_Failover_and_Load_Balancing_TP2201_tc_19',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_19_WAN_Failover_and_Load_Balancing_TP2201_tc_22',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_20_WAN_Failover_and_Load_Balancing_TP2201_tc_23',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_21_WAN_Failover_and_Load_Balancing_TP2201_tc_26',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_22_WAN_Failover_and_Load_Balancing_TP2201_tc_27',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_23_WAN_Failover_and_Load_Balancing_TP2201_tc_29',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_24_WAN_Failover_and_Load_Balancing_TP2201_tc_31',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_25_WAN_Failover_and_Load_Balancing_TP2201_tc_37',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_26_WAN_Failover_and_Load_Balancing_TP2201_tc_45',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_27_WAN_Failover_and_Load_Balancing_TP2201_tc_46',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_28_WAN_Failover_and_Load_Balancing_TP2201_tc_95',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_29_WAN_Failover_and_Load_Balancing_TP2201_tc_202',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_30_WAN_Failover_and_Load_Balancing_TP2201_tc_209',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_31_WAN_Failover_and_Load_Balancing_TP2201_tc_220',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part1.Test_32_WAN_Failover_and_Load_Balancing_TP2201_tc_260',    
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
