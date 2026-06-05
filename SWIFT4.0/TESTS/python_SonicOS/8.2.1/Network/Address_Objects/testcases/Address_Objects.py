from definition.initial_parameter import *


class TestAddressObjects_01(Test):
    uuid = "SOSAIOT-TC-57761"
    description= show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Object_LAN_Host(self):
        ao_param ={
            "object_type": "host",
            "name": " TestLanHost",
            "zone": "LAN",
            "value": "172.16.1.1"
        }
        rc = address_obj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add LAN Host Address Object") 

    def test_02_Verify_New_Added_Address_Object(self):
        FALG = 0
        rc = address_obj.get_addressobject('host', object_path='name', object_name_uuid=' TestLanHost', ip_type='ipv4')
        if rc['address_objects'][0]['ipv4']['name'] == ' TestLanHost':
            logger.info("Name is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['zone'] == 'LAN':
            logger.info("Zone is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['host']['ip'] == '172.16.1.1':
            logger.info("Value is right!")
            FALG += 1
        Assertion.assert_equal(FALG, 3, "ERR: Failed To Verified LAN Host Address Object")

    def test_03_Delete_New_Added_Address_Object(self):
        rc = address_obj.delete_addressobject('host', object_path='name', object_name_uuid=' TestLanHost', ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Failed To Delete LAN Host Address Object")


class TestAddressObjects_07(Test):
    uuid = "SOSAIOT-TC-57789"
    description= show_testcase_info(Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '07')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Object_DMZ_Host(self):
        ao_param ={
            "object_type": "host",
            "name": " TestDmzHost",
            "zone": "DMZ",
            "value": "172.16.3.1"
        }
        rc = address_obj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add DMZ Host Address Object") 

    def test_02_Verify_New_Added_Address_Object(self):
        FALG = 0
        rc = address_obj.get_addressobject('host', object_path='name', object_name_uuid=' TestDmzHost', ip_type='ipv4')
        if rc['address_objects'][0]['ipv4']['name'] == ' TestDmzHost':
            logger.info("Name is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['zone'] == 'DMZ':
            logger.info("Zone is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['host']['ip'] == '172.16.3.1':
            logger.info("Value is right!")
            FALG += 1
        Assertion.assert_equal(FALG, 3, "ERR: Failed To Verified DMZ Host Address Object")

    def test_03_Delete_New_Added_Address_Object(self):
        rc = address_obj.delete_addressobject('host', object_path='name', object_name_uuid=' TestDmzHost', ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Failed To Delete DMZ Host Address Object")  


class TestAddressObjects_16(Test):
    uuid = "SOSAIOT-TC-57768"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Object_WLAN_Host(self):
        ao_param ={
            "object_type": "host",
            "name": " TestWLanHost",
            "zone": "WLAN",
            "value": "172.16.6.1"
        }
        rc = address_obj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add WLAN Host Address Object") 

    def test_02_Verify_New_Added_Address_Object(self):
        FALG = 0
        rc = address_obj.get_addressobject('host', object_path='name', object_name_uuid=' TestWLanHost', ip_type='ipv4')
        if rc['address_objects'][0]['ipv4']['name'] == ' TestWLanHost':
            logger.info("Name is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['zone'] == 'WLAN':
            logger.info("Zone is right!")
            FALG += 1
        if rc['address_objects'][0]['ipv4']['host']['ip'] == '172.16.6.1':
            logger.info("Value is right!")
            FALG += 1
        Assertion.assert_equal(FALG, 3, "ERR: Failed To Verified WLAN Host Address Object")

    def test_03_Delete_New_Added_Address_Object(self):
        rc = address_obj.delete_addressobject('host', object_path='name', object_name_uuid=' TestWLanHost', ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Failed To Delete WLAN Host Address Object")  


class TestAddressObjects_19(Test):
    uuid = "SOSAIOT-TC-57771"
    description= show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '19')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Group(self):
        ag_param = {
            'address_groups': [{
                'ipv4':{
                    'name': 'TestAddressGroupA',  
                    'address_group': {'ipv4': [
                        {'name': 'LAN Interface IP'}, 
                        {'name': 'DMZ Interface IP'}
                    ]}
                }
            }]
        }
        rc = address_group_obj.add_addressgroup(**ag_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Failed To Add Address Group") 

    def test_02_Verify_New_Added_Address_Group(self):
        FALG = 0
        rc = address_gro.get_addressgroup(group_type = 'ipv4', group_path='name', group_name_uuid='TestAddressGroupA')
        if rc['address_groups'][0]['ipv4']['name'] == 'TestAddressGroupA':
            logger.info("Name is right!")
            FALG += 1
        address_group = rc['address_groups'][0]['ipv4']['address_group']['ipv4']
        my_address_group = [address_group[0]['name'], address_group[1]['name']]
        if 'LAN Interface IP' in my_address_group:
            logger.info("Found target group1!")
            FALG += 1
        if 'DMZ Interface IP' in my_address_group:
            logger.info("Found target group2!")
            FALG += 1
        Assertion.assert_equal(FALG, 3, "ERR: Failed To Verified Address Group")

    def test_03_Delete_New_Added_Address_Group(self):
        rc = address_group_obj.del_addressgroup('TestAddressGroupA', version = 'v4')
        Assertion.assert_equal(rc, True, "ERR: Failed To Delete Address Group")   


class TestAddressObjects_25(Test):
    uuid = "SOSAIOT-TC-57778"
    description= show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '25')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Group(self):
        ag_param = {
            'address_groups': [{
                'ipv4':{
                    'name': 'TestAddressGroupA',  
                    'address_group': {'ipv4': [
                        {'name': 'LAN Interface IP'}, 
                        {'name': 'DMZ Interface IP'}
                    ]}
                }
            }]
        }
        rc = address_group_obj.add_addressgroup(**ag_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Group") 

    def test_02_Verify_New_Added_Address_Group(self):
        FALG = 0
        rc = address_gro.get_addressgroup(group_type = 'ipv4', group_path='name', group_name_uuid='TestAddressGroupA')
        if rc['address_groups'][0]['ipv4']['name'] == 'TestAddressGroupA':
            logger.info("Name is right!")
            FALG += 1
        address_group = rc['address_groups'][0]['ipv4']['address_group']['ipv4']
        my_address_group = [address_group[0]['name'], address_group[1]['name']]
        if 'LAN Interface IP' in my_address_group:
            logger.info("Found target group1!")
            FALG += 1
        if 'DMZ Interface IP' in my_address_group:
            logger.info("Found target group2!")
            FALG += 1
        Assertion.assert_equal(FALG, 3, "ERR: Failed To Verified Address Group")

    def test_03_Edit_Address_Group(self):
        ag_param = {
            'address_groups': [{
                'ipv4':{
                    'name': 'TestAddressGroupB',  
                    'address_group': {'ipv4': [
                        {'name': 'LAN Interface IP'}, 
                        {'name': 'DMZ Interface IP'},
                        {'name': 'WAN Interface IP'}
                    ]}
                }
            }]
        }
        rc = address_group_obj.edit_addressgroup(**ag_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Edit Address Group")

    def test_04_Verify_Edited_Address_Group(self):
        FALG = 0
        rc = address_gro.get_addressgroup(group_type = 'ipv4', group_path='name', group_name_uuid='TestAddressGroupB')
        if rc['address_groups'][0]['ipv4']['name'] == 'TestAddressGroupB':
            logger.info("Name is right!")
            FALG += 1
        address_group = rc['address_groups'][0]['ipv4']['address_group']['ipv4']
        my_address_group = [address_group[0]['name'], address_group[1]['name'], address_group[2]['name']]
        if 'LAN Interface IP' in my_address_group:
            logger.info("Found target group1!")
            FALG += 1
        if 'DMZ Interface IP' in my_address_group:
            logger.info("Found target group2!")
            FALG += 1
        if 'WAN Interface IP' in my_address_group:
            logger.info("Found target group3!")
            FALG += 1
        Assertion.assert_equal(FALG, 4, "ERR: Failed To Verified Edited Address Group")

    def test_05_Delete_New_Added_Address_Group(self):
        rc = address_group_obj.del_addressgroup('TestAddressGroupB', version = 'v4')
        Assertion.assert_equal(rc, True, "ERR: Failed To Delete Address Group")   
