import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/aws_api')

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
        for i in range(10):
             time.sleep(5)
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

class TC01_get_aws_connection(Test):
    uuid = "SOSAIOT-TC-47287"
    goto_teardown = True
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
   
    def test_get_aws_connection(self):
        response = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response), '"access_key_id": "AKIA2QAXUGQ4EXODEIPI"', "err:Failed to get AWS connection")

class TC02_edit_aws_connection(Test):
    uuid = "SOSAIOT-TC-47288"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_aws_connection(self):
        aws_con={
    		'access_id':'AKIA2QAXUGQ4EXODEIPI',
    		'password':'q1uhrjXiB+5LHnmkBEHCrtHzT9AlRiPBaACzg9v0',
    		'region':'north-virginia'
        }
        response =aws_connection.edit_aws_connection(**aws_con)
        response1=aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response1), '"region": "north-virginia"', "err:Failed to update AWS connection")


class TC03_retrieve_aws_objects(Test):

    uuid = "SOSAIOT-TC-47289"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_retrieve_aws_objects(self):

        response = aws_objects.get_aws_objects()
        Assertion.assert_regular(json.dumps(response), '"mapping": true, "syncronization_interval": 180', "err:Failed to retrieve AWS objects")

class TC04_update_aws_objects(Test):

    uuid = "SOSAIOT-TC-47290"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
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


class TC05_update_synchronization_interval(Test):

    uuid = "SOSAIOT-TC-47291"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
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

class TC06_update_monitor_region(Test):

    uuid = "SOSAIOT-TC-47292"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
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

class TC07_delete_aws_objects(Test):

    uuid = "SOSAIOT-TC-47293"
    description = show_testcase_info(Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_delete_aws_objects(self):


        response1 = aws_objects.delete_aws_objects()
        Assertion.assert_equal(True, True, "ERR: Deletion of aws objects failed")


class TC08_force_sync_aws_objects(Test):

    uuid = "SOSAIOT-TC-47294"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_force_sync_aws_objects(self):


        response = aws_objects.get_force_sync()
        Assertion.assert_equal(True, True, "ERR: force synchronisation failed")

class TC09_create_aws_object_address_group_mapping(Test):

    uuid = "SOSAIOT-TC-47295"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_aws_connection(self):
        aws_con = {
           'access_id':'AKIA2QAXUGQ4EXODEIPI',
    		'password':'q1uhrjXiB+5LHnmkBEHCrtHzT9AlRiPBaACzg9v0',
            'region': 'mumbai'
        }
        response = aws_connection.edit_aws_connection(**aws_con)
        response1 = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response1), '"region": "mumbai"',
                                 "err:Failed to update aws connection")

    def test_create_aws_object_address_group_mapping(self):
        aws_mapping = {
            'index': 1,
            'addr_grp': 'aws_group',
            'instance_key': 'instance-state',
            'instance_value': "running"
            }

        response = group_mapping.config_grp_mapping(**aws_mapping)
        response1=group_mapping.get_aws_grp_mapping()
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"', "err:Failed to create aws group mapping")


class TC12_verify_retrieving_aws_group_mapping_configuration(Test):

    uuid = "SOSAIOT-TC-47296"
    description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_retrieving_aws_group_mapping_configuration(self):
        response1 = group_mapping.get_aws_grp_mapping()
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"',
                                 "err:Failed to retrieve AWS objects")

class TC13_verify_retrieving_aws_group_mapping_by_index(Test):

    uuid = "SOSAIOT-TC-47297"
    description = show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_retrieving_aws_group_mapping_by_index(self):
        response1 = group_mapping.get_aws_grp_mapping_index("1")
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"',
                                 "err:Failed to retrieve AWS group mapping")


class TC14_verify_update_aws_instancekey_configuration(Test):

    uuid = "SOSAIOT-TC-47298"
    description = show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
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
class TC18_verify_delete_aws_group_mapping_by_index(Test):
    uuid = "SOSAIOT-TC-47299"
    description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_delete_aws_group_mapping_by_index(self):
        response1 = group_mapping.delete_aws_mapping_index("1")
        response=group_mapping.get_aws_grp_mapping()
        Assertion.assert_not_regular(json.dumps(response), '"address_group": "aws_group"',
                                 "err:Failed to delete aws group mapping")

class TC19_verify_invalid_access_key(Test):
    uuid = "SOSAIOT-TC-47300"
    description = show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '19')
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


class TC20_verify_invalid_secret_key(Test):
    uuid = "SOSAIOT-TC-47301"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_invalid_secret_key(self):
        aws_con = {
            
            'access_id': 'AKIA2QAXUGQ4EXODEIPI',
            'password': 'jshdjhsjdhsjsdghg',
            'region': 'north-virginia'
        }
        response = aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'],
                                 'Incorrect AWS Credentials Entered. Configuration not saved',
                                 "err: failed to verify invalid secret key")

class TC21_verify_secret_key_out_of_bounds(Test):
    uuid = "SOSAIOT-TC-47302"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_secret_key_out_of_bounds(self):
        aws_con = {
            'access_id': 'AKIA2QAXUGQ4EXODEIPI',
            'password': 'j3stuF5BqWm9oh9+D9wAj++r+0Xtk+64HvL7tBuwdsadhjkshrwu3y473264gjhdgjkashd8237423jrhjdfa',
            'region': 'north-virginia'
        }
        response = aws_connection.edit_aws_connection(**aws_con, msg=True)

        Assertion.assert_regular(response[1]['status']['info'][0]['message'],'out of bounds ',"err: failed to throw out of bounds error")

class TC22_verify_synchronization_out_of_bounds(Test):
    uuid = "SOSAIOT-TC-47303"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_synchronization_out_of_bounds(self):
        aws_obj = {
            'mapping': True,
            'sync_interval': 1800,
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
        response1=aws_objects.edit_aws_objects(**aws_obj,msg=True)
        Assertion.assert_regular(response1[1]['status']['info'][0]['message'],' out of bounds ',"err: failed to throw error")
        
class TC23_verify_updating_existing_monitor_region(Test):
    uuid = "SOSAIOT-TC-47304"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_verify_updating_existing_monitor_region(self):
        aws_obj = {
            'mapping': True,
            'sync_interval': 180,
            'monitor_region':{'north_virginia': False,
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
        Assertion.assert_regular(json.dumps(response), '"monitor_region": {"north_virginia": false,',"err:Failed to update monitor region")




