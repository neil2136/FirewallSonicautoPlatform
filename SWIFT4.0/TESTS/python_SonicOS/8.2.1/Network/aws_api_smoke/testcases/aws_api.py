import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/aws_api_smoke')

from definition.settings import *



class aws_object_config(Test):
    uuid = 'NonTC'

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
        response = addressgroup.delete_addressgroup('ipv4', 'aws_group')
        response1 = addressgroup.get_addressgroup('ipv4')
        Assertion.assert_not_regular(json.dumps(response1), ' "name": "aws_group"',
                                     "err:Failed to delete address group")

    def test_01_delete_address_object(self):
        address_object = {
            'ip_type': 'ipv4',
            'name': 'aws_object'
        }

        response = addressobject.del_addressobject(**address_object)
        response1 = addressobject.get_addressobject_by_name('aws_object')
        Assertion.assert_not_regular(json.dumps(response1), ' "name": "aws_object"',
                                     "err:Failed to delete address group")


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




class TC03_retrieve_aws_objects(Test):

    uuid = "SOSAIOT-TC-47289"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_retrieve_aws_objects(self):

        response = aws_objects.get_aws_objects()
        Assertion.assert_regular(json.dumps(response), '"mapping": true, "syncronization_interval": 180', "err:Failed to retrieve AWS objects")


class TC07_delete_aws_objects(Test):

    uuid = '1510763 '
    description = show_testcase_info(Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_delete_aws_objects(self):


        response1 = aws_objects.delete_aws_objects()
        Assertion.assert_equal(True, True, "ERR: Deletion of aws objects failed")


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
    		'region':'mumbai'
        }
        response = aws_connection.edit_aws_connection(**aws_con)
        response1 = aws_connection.get_aws_connection()
        Assertion.assert_regular(json.dumps(response1), '"region": "mumbai"',
                                 "err:Failed to update AWS connection")

    def test_create_aws_object_address_group_mapping(self):
        aws_mapping = {
            'index': 1,
            'addr_grp': 'aws_group',
            'instance_key': 'instance-state',
            'instance_value': "running"
            }

        response = group_mapping.config_grp_mapping(**aws_mapping)
        response1=group_mapping.get_aws_grp_mapping()
        Assertion.assert_regular(json.dumps(response1), '"address_group": "aws_group"', "err:Failed to create aws objects")

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
                                 "err:Failed to delete aws objects")

