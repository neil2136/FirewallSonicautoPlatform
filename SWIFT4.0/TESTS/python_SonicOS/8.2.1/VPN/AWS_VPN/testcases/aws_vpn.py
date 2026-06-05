import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/AWS_VPN/')

from definition.settings import *

class aws_object_config(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_create_address_object(self):
        address_object = {
            "object_type": "host",
            "value": "3.108.195.134",
            "name": "aws_object",
            "zone": "WAN",

        }
        response = addressobject.config_addressobject(**address_object)
        response1 = addressobject.get_addressobject_by_name("aws_object", "ipv4")
        Assertion.assert_regular(json.dumps(response1), '"name": "aws_object"', "err:Failed to create address object")

    def test_01_create_address_group(self):
        address_group = {
            'address_groups': [{
                'ipv4': {
                    'name': 'aws_group',
                    "address_object": {
                        "ipv4": [
                            {
                                "name": "aws_object"
                            }
                        ]
                    }
                }
            }]
        }
        response1 = add_group.add_addressgroup(**address_group)
        response1 = add_group.get_addressgroup()
        Assertion.assert_regular(json.dumps(response1), '"ipv4": {"name": "aws_group"',
                                 "err:Failed to create address group")
    def test_02_edit_aws_connection(self):
        aws_con={
    		'access_id':'AKIA2QAXUGQ4EXODEIPI',
    		'password':'q1uhrjXiB+5LHnmkBEHCrtHzT9AlRiPBaACzg9v0',
    		'region':'north-virginia'
        }
        response =aws_connection.edit_aws_connection(**aws_con)
        response1=aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response1), '"region": "north-virginia"', "err:Failed to update AWS connection")

class delete_Address_object_and_group(Test):
    uuid = 'NonTC'
    def test_00_delete_address_group(self):
       
        response = addressgroup.delete_addressgroup('ipv4','aws_group')
        response1 = addressgroup.get_addressgroup('ipv4')
        Assertion.assert_not_regular(json.dumps(response1), ' "name": "aws_group"',"err:Failed to delete address group")

    def test_01_delete_address_object(self):
        address_object = {
          'ip_type': 'ipv4',
           'name': 'aws_object'
         }
         

        response = addressobject.del_addressobject(**address_object)
        response1 = addressobject.get_addressobject_by_name('aws_object')
        Assertion.assert_not_regular(json.dumps(response1), ' "name": "aws_object"',"err:Failed to delete address object")

class TC01_AWS_Config_Enter_correct_credentials_with_TLS(Test):
    uuid = "SOSAIOT-TC-48232"
    goto_teardown = True

    description = show_testcase_info(Parameter.TESTPLAN, '1524387', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524387')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_aws_connection(self):
        response = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response), '"access_key_id": "AKIA2QAXUGQ4EXODEIPI"', "err:Failed to get AWS connection")


class TC03_AWS_Config_Enter_correct_credentials_without_TLS(Test):
    uuid = "SOSAIOT-TC-48234"
    description = show_testcase_info(Parameter.TESTPLAN, '1524394', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524394')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_get_aws_connection(self):
        response = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response), '"access_key_id": "AKIA2QAXUGQ4EXODEIPI"', "err:Failed to get AWS connection")

class TC04_Reset_AWS_logs(Test):

    uuid = "SOSAIOT-TC-48235"
    description = show_testcase_info(Parameter.TESTPLAN, '1524398', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524398')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_update_aws_objects(self):
        aws_obj = {
            'mapping': True,
            'sync_interval': 180,
            'monitor_region':{'north_virginia': True,
                              'ohio': False,
                              'north_california': False,
                              'oregon': False,
                              'canada': False,
                              'mumbai': True,
                              'seoul': False,
                              'singapore': False,
                              'sydney': False,
                              'tokyo': False,
                              'frankfurt': False,
                              'ireland': False,
                              'london': False,
                              'paris': False,
                              'sao_paulo': False
                              }
        }
        response1=aws_objects.edit_aws_objects(**aws_obj)
        response = aws_objects.get_aws_objects()
        Assertion.assert_regular(json.dumps(response), '"mapping": true, "syncronization_interval": 180', "err:Failed to update AWS objects")


class TC05_Verify_that_VPCs_show_up_on_the_firewall_GUI_only_if_configured_on_AWSConsole(Test):

    uuid = "SOSAIOT-TC-48236"
    description = show_testcase_info(Parameter.TESTPLAN, '1524400', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524400')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_update_synchronization_interval(self):
        aws_obj = {
            'mapping': True,
            'sync_interval': 80,
            'monitor_region': {'north_virginia': True,
                               'ohio': False,
                               'north_california': False,
                               'oregon': False,
                               'canada': False,
                               'mumbai': True,
                               'seoul': False,
                               'singapore': False,
                               'sydney': False,
                               'tokyo': False,
                               'frankfurt': False,
                               'ireland': False,
                               'london': False,
                               'paris': False,
                               'sao_paulo': False
                               }
        }
        response1 = aws_objects.edit_aws_objects(**aws_obj)
        response = aws_objects.get_aws_objects()
        Assertion.assert_regular(json.dumps(response), ' "syncronization_interval": 80',
                                 "err:Failed to update synchronization-interval AWS objects")

class TC06_AWS_Config_Click_on_Test_Details_result_tab(Test):

    uuid = "SOSAIOT-TC-48237"
    description = show_testcase_info(Parameter.TESTPLAN, '1524401', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524401')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_update_monitor_region(self):
        aws_obj = {
            'mapping': True,
            'sync_interval': 180,
            'monitor_region': {'north_virginia': True,
                               'ohio': True,
                               'north_california': False,
                               'oregon': False,
                               'canada': False,
                               'mumbai': True,
                               'seoul': False,
                               'singapore': False,
                               'sydney': False,
                               'tokyo': False,
                               'frankfurt': False,
                               'ireland': False,
                               'london': False,
                               'paris': False,
                               'sao_paulo': False
                               }
        }
        response1 = aws_objects.edit_aws_objects(**aws_obj)
        response = aws_objects.get_aws_objects()
        Assertion.assert_regular(json.dumps(response), '"monitor_region": {"north_virginia": true, "ohio": true',
                                 "err:Failed to update monitor region")

class TC07_AWSVPN_Create_VPN_Connection_with_Propagation_Connections_checkbox_checked(Test):

    uuid = '1524402 '
    description = show_testcase_info(Parameter.TESTPLAN, '1524402', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524402')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_delete_aws_objects(self):


        response1 = aws_objects.delete_aws_objects()
        Assertion.assert_equal(True, True, "ERR: Deletion of aws objects failed")


class TC08_AWSVPN_Delete_VPN_Connection_on_VPC_one_customer_gateway(Test):

    uuid = "SOSAIOT-TC-48239"
    description = show_testcase_info(Parameter.TESTPLAN, '1524405', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524405')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_force_sync_aws_objects(self):


        response = aws_objects.get_force_sync()
        Assertion.assert_equal(True, True, "ERR: force synchronisation failed")

class TC09_AWS_Config_Enter_wrong_credentials_for_Access_Key_ID(Test):

    uuid = "SOSAIOT-TC-48240"
    description = show_testcase_info(Parameter.TESTPLAN, '1524408', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524408')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    def test_verify_invalid_secret_key(self):
        aws_con = {
            'access_id': 'AKIA2QAXUGQ4NG5GPCW6',
            'password': 'jshdjhsjdhsjsdghg',
            'region': 'north-virginia'
        }
        response = aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'],
                                 'Incorrect AWS Credentials Entered. Configuration not saved',
                                 "err: failed to verify invalid secret key")

class TC10_AWSObjects_Create_New_Mapping_of_type_Instance_ID(Test):

    uuid = "SOSAIOT-TC-48243"
    description = show_testcase_info(Parameter.TESTPLAN, '1524417', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524417')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_retrieving_aws_group_mapping_configuration(self):
        response1 = group_mapping.get_aws_grp_mapping()
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"',
                                 "err:Failed to retrieve AWS objects")

class TC11_AWSObjects_Create_New_Mapping_of_type_Subnet_ID(Test):

    uuid = "SOSAIOT-TC-48244"
    description = show_testcase_info(Parameter.TESTPLAN, '1524419', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524419')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_retrieving_aws_group_mapping_by_index(self):
        response1 = group_mapping.get_aws_grp_mapping_index("1")
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"',
                                 "err:Failed to retrieve AWS group mapping")


class TC12_AWSObjects_Create_New_Mapping_of_type_Custom_Tag(Test):

    uuid = "SOSAIOT-TC-48245"
    description = show_testcase_info(Parameter.TESTPLAN, '141524423', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524423')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_update_aws_instancekey_configuration(self):
        aws_mapping = {
            'index': 1,
            'addr_grp': 'aws_group',
            'instance_key': 'instance-id',
            'instance_value': "i-0f03efeacaca90daa"
            }

        response = group_mapping.edit_grp_mapping(**aws_mapping)
        response1=group_mapping.get_aws_grp_mapping()
        Assertion.assert_regular(json.dumps(response1), '"key": "instance-id", "value": "i-0f03efeacaca90daa"', "err:Failed to update aws instance key")
class TC13_Editing_an_existing_mapping_Add_more_conditions(Test):
    uuid = "SOSAIOT-TC-48247"
    description = show_testcase_info(Parameter.TESTPLAN, '1524426', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524426')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_delete_aws_group_mapping_by_index(self):
        response1 = group_mapping.delete_aws_mapping_index("1")
        response=group_mapping.get_aws_grp_mapping()
        Assertion.assert_not_regular(json.dumps(response), '"address_group": "aws_group"',
                                 "err:Failed to delete aws group mapping")

class TC14_AWS_Config_Enter_wrong_region(Test):
    uuid = "SOSAIOT-TC-48248"
    description = show_testcase_info(Parameter.TESTPLAN, '1524428', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524428')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_access_key(self):
        aws_con={
    		'access_id':'dsfshdfjdsgfhhgwyg',
    		'password':'j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuw',
    		'region':'north-virginia'
        }
        response =aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'], 'Incorrect AWS Credentials Entered. Configuration not saved',
                                 "err: failed to verify invalid access key")


class TC15_AWS_Config_Check_uncheck_mask_key_checkbox(Test):
    uuid = "SOSAIOT-TC-48249"
    description = show_testcase_info(Parameter.TESTPLAN, '1524437', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524437')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_secret_key(self):
        aws_con = {
            'access_id': 'AKIA2QAXUGQ4NG5GPCW6',
            'password': 'jshdjhsjdhsjsdghg',
            'region': 'north-virginia'
        }
        response = aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'],
                                 'Incorrect AWS Credentials Entered. Configuration not saved',
                                 "err: failed to verify invalid secret key")

class TC02_verify_secret_key_out_of_bounds(Test):
    uuid = "SOSAIOT-TC-48233"
    description = show_testcase_info(Parameter.TESTPLAN, '1524388', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524388')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_secret_key_out_of_bounds(self):
        aws_con = {
            'access_id': 'AKIA2QAXUGQ4EXODEIPI',
            'password': 'j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuwdsadhjkshrwu3y473264gjhdgjkashd8237423jrhjdfa',
            'region': 'north-virginia'
        }
        response = aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'],'out of bounds ',"err: failed to throw out of bounds error")
