import sys
import os
import unittest
from runner.unittest.suite import UnittestSuite


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/aws_api_smoke')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/Network/aws_api_smoke/testcases/')





def suite():
    testcases_list = [

        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw.TestConfigTB',
        'aws_api.delete_Address_object_and_group',
        'aws_api.aws_object_config',
        'aws_api.TC01_get_aws_connection',
        'aws_api.TC03_retrieve_aws_objects',
        'aws_api.TC07_delete_aws_objects',
        'aws_api.TC18_verify_delete_aws_group_mapping_by_index',
        'aws_api.TC09_create_aws_object_address_group_mapping',


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)

    return suites


if __name__ == '__main__':
    to_users = 'ftahreen@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(),to_users,cc_users)
    st.run()
