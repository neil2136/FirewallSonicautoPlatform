__author__ = 'tcheng'
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WAN_Failover_and_Load_Balancing_TP2201_part2')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/WAN_Failover_and_Load_Balancing_TP2201_part2/definition')






def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.set_env.TestConfigTB_01',
        'bin.conf_fw.TestConfigTB',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_01_WAN_Failover_and_Load_Balancing_TP2201_tc_112',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_02_WAN_Failover_and_Load_Balancing_TP2201_tc_113',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_03_WAN_Failover_and_Load_Balancing_TP2201_tc_114',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_04_WAN_Failover_and_Load_Balancing_TP2201_tc_115',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_05_WAN_Failover_and_Load_Balancing_TP2201_tc_116',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_06_WAN_Failover_and_Load_Balancing_TP2201_tc_117',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_07_WAN_Failover_and_Load_Balancing_TP2201_tc_118',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_08_WAN_Failover_and_Load_Balancing_TP2201_tc_119',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_09_WAN_Failover_and_Load_Balancing_TP2201_tc_120',
        'testcases.WAN_Failover_and_Load_Balancing_TP2201_part2.Test_10_WAN_Failover_and_Load_Balancing_TP2201_tc_121',
    ]
 
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


    
    
if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
