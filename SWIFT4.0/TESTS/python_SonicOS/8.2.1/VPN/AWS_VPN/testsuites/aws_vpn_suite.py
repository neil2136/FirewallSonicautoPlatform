import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/AWS_VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/AWS_VPN/testcases')





def suite():
    testcases_list = [

        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'aws_vpn.delete_Address_object_and_group',
        'aws_vpn.aws_object_config',
        'aws_vpn.TC01_AWS_Config_Enter_correct_credentials_with_TLS',
        'aws_vpn.TC03_AWS_Config_Enter_correct_credentials_without_TLS',
        'aws_vpn.TC04_Reset_AWS_logs',
        'aws_vpn.TC05_Verify_that_VPCs_show_up_on_the_firewall_GUI_only_if_configured_on_AWSConsole',
        'aws_vpn.TC06_AWS_Config_Click_on_Test_Details_result_tab',
        'aws_vpn.TC07_AWSVPN_Create_VPN_Connection_with_Propagation_Connections_checkbox_checked',
        'aws_vpn.TC08_AWSVPN_Delete_VPN_Connection_on_VPC_one_customer_gateway',
        'aws_vpn.TC09_AWS_Config_Enter_wrong_credentials_for_Access_Key_ID',
        'aws_vpn.TC12_AWSObjects_Create_New_Mapping_of_type_Custom_Tag',
        'aws_vpn.TC10_AWSObjects_Create_New_Mapping_of_type_Instance_ID',
        'aws_vpn.TC11_AWSObjects_Create_New_Mapping_of_type_Subnet_ID',
        'aws_vpn.TC13_Editing_an_existing_mapping_Add_more_conditions',
        'aws_vpn.TC14_AWS_Config_Enter_wrong_region',
        'aws_vpn.TC15_AWS_Config_Check_uncheck_mask_key_checkbox',
        'aws_vpn.TC02_verify_secret_key_out_of_bounds',
      


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
