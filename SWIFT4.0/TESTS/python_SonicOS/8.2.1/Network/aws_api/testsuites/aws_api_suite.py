import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/aws_api')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/aws_api/testcases')





def suite():
    testcases_list = [

        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'aws_api.delete_Address_object_and_group',
        'aws_api.aws_object_config',
        'aws_api.TC01_get_aws_connection',
        'aws_api.TC02_edit_aws_connection',
        'aws_api.TC03_retrieve_aws_objects',
        'aws_api.TC04_update_aws_objects',
        'aws_api.TC05_update_synchronization_interval',
        'aws_api.TC06_update_monitor_region',
        'aws_api.TC07_delete_aws_objects',
        'aws_api.TC08_force_sync_aws_objects',
        'aws_api.TC09_create_aws_object_address_group_mapping',
        'aws_api.TC12_verify_retrieving_aws_group_mapping_configuration',
        'aws_api.TC13_verify_retrieving_aws_group_mapping_by_index',
        'aws_api.TC14_verify_update_aws_instancekey_configuration',
        # 'aws_api.TC17_verify_update_aws_instancekey_configuration_by_index',
        'aws_api.TC18_verify_delete_aws_group_mapping_by_index',
        'aws_api.TC19_verify_invalid_access_key',
        'aws_api.TC20_verify_invalid_secret_key',
        'aws_api.TC21_verify_secret_key_out_of_bounds',
        'aws_api.TC22_verify_synchronization_out_of_bounds',
        'aws_api.TC23_verify_updating_existing_monitor_region'


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()
