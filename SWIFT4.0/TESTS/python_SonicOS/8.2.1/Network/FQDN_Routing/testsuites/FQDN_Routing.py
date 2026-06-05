import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Network/FQDN_Routing")

'''
 ****add single test case to test suite****      
 ****add test cases by module ****
'''
def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_env.PreConfig_for_FQDN_Testing',
        'testcases.FQDN_Routing.Test_01_TC8_TC13_Config_Stages',
        'testcases.FQDN_Routing.Test_02_TC08_Function_Test_of_IPv4_FQDN_PBR',
        'testcases.FQDN_Routing.Test_03_TC10_Function_Test_of_FQDN_PBR_Type_FQDN_AO',
        'testcases.FQDN_Routing.Test_04_TC11_Function_Test_of_FQDN_PBR_Type_FQDN_AO_Group',
        'testcases.FQDN_Routing.Test_05_TC12_Function_Test_of_FQDN_PBR_Type_Mixed_AO_Group',
        'testcases.FQDN_Routing.Test_06_TC13_Delete_A_FQDN_PBR',
        'testcases.FQDN_Routing.Test_07_TC14_PBR_not_Work_When_Delete_One_AO_From_Dst_Group',
        'testcases.FQDN_Routing.Test_08_TC15_PBR_Works_When_Add_One_AO_to_Dst_Group',
        'testcases.FQDN_Routing.Test_09_TC17_Function_Test_FQDN_PBR_when_FQDN_AO_Include_Wildcard',
        'testcases.FQDN_Routing.Test_10_TC18_TC19_TC26_Config_Stages',
        'testcases.FQDN_Routing.Test_11_TC18_FQDN_PBR_Should_Be_Gray_Out_when_No_Host_Can_Be_Resolved',
        'testcases.FQDN_Routing.Test_12_TC19_Gray_FQDN_PBR_Should_Change_Active_Once_AO_Get_Resolved',
        'testcases.FQDN_Routing.Test_13_TC26_FQDN_PBR_Should_Work_when_New_FQDN_Get_Resolved',
        'testcases.FQDN_Routing.Test_14_TC23_Modify_FQDN_AO_When_It_Is_Used_in_PBR',
        'testcases.FQDN_Routing.Test_15_TC24_FQDN_PBR_Will_Not_Be_Interrupted_after_Its_Host_IP_Getting_Expired',
        'testcases.FQDN_Routing.Test_16_TC25_Previous_Connection_Cache_for_Expired_IP_Should_Be_Flushed',
        'testcases.FQDN_Routing.Test_17_TC27_Advertise_FQDN_Based_Policy_Route_to_Dynamic_Routing_Disabled',
        'testcases.FQDN_Routing.Test_18_TC28_TC29_Config_Stages',
        'testcases.FQDN_Routing.Test_19_TC28_Advertise_FQDN_Route_to_Dynamic_Routing_Enabled',
        'testcases.FQDN_Routing.Test_20_TC29_Advertise_FQDN_Route_to_Dynamic_Routing_Enable_then_Disable',
        'testcases.FQDN_Routing.Test_21_TC30_Add_FQDN_PBR_in_CLI',
#        'testcases.FQDN_Routing.Test_22_TC32_FQDN_PBR_Works_when_FQDN_AO_Matched_DNS_Proxy_Split_DNS_Entry',
#        'testcases.FQDN_Routing.Test_23_TC34_FQDN_PBR_Be_Updated_after_Change_Split_DNS_Entry',
        'testcases.FQDN_Routing.Test_24_TC38_Prefs_Export_and_Import_Test',
        'testcases.FQDN_Routing.Test_25_TC39_Restart_Test',
        'testcases.FQDN_Routing.Test_26_TC40_Test_TSR',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'sgao@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
