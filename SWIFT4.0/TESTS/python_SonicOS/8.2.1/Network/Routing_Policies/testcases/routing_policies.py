import sys
import os
import json
import time
import paramiko
import subprocess

from definition.settings import *

class Test_01_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47698"
    description= show_testcase_info(Parameter.TESTPLAN, '1516222', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516222')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_add_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testadd",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

    def test_03_perform_GET_request_and_verify_routing_policy(self):
        resp = routing_policies_obj.get_route_policy_by_name(name='testadd')
        Assertion.assert_regular(json.dumps(resp), '"name": "testadd"', "ERR: Failed to verify route policy")


class Test_02_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47699"
    description= show_testcase_info(Parameter.TESTPLAN, '1516223', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516223')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_create_address_object_and_service_object(self):
        address_object = {
            "object_type": "host",
            "name": "source_address",
            "zone": "LAN",
            "value": "1.1.1.1"
        }
        resp = address_objects.config_addressobject(**address_object)

        address_object = {
            "object_type": "host",
            "name": "destination_address",
            "zone": "WAN",
            "value": "1.1.1.100"
        }
        resp = address_objects.config_addressobject(**address_object)

        service_object_json = {
            "object_type": "icmp",
            "name":"test_object",
            "icmp":"echo-request"
        }
        rc = service_obj.config_service_object(**service_object_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service object failed")

    def test_03_add_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testadd_source_des",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                        "name":"test_object"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "name": "source_address"
                    },
                    "destination":{
                        "name": "destination_address"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des")
        Assertion.assert_regular(json.dumps(resp), '"source": {"name": "source_address"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"name": "destination_address"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des")
        Assertion.assert_regular(json.dumps(resp), '"service": {"name": "test_object"}', "ERR: Failed to verify add routing policy service")


class Test_03_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47700"
    description= show_testcase_info(Parameter.TESTPLAN, '1516224', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516224')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_create_address_object_and_service_group(self):
        address_group = {
            'address_groups': [{
                'ipv4': {
                    'name': 'source_group',
                    "address_object": {
                        "ipv4": [
                            {
                                "name": "source_address"
                            }
                        ]
                    }
                }
            }]
        }
        response1 = add_group.add_addressgroup(**address_group)

        address_group = {
            'address_groups': [{
                'ipv4': {
                    'name': 'destination_group',
                    "address_object": {
                        "ipv4": [
                            {
                                "name": "destination_address"
                            }
                        ]
                    }
                }
            }]
        }
        response1 = add_group.add_addressgroup(**address_group)

        service_object_json = {
            "object_type": "icmp",
            "name":"test_object1",
            "icmp":"echo-request"
        }
        rc = service_obj.config_service_object(**service_object_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service object failed")

        service_group_json = {
            "name": "service_group",
            "service_object": [
                {
                    "name": "test_object"
                },
                {
                    "name": "test_object1"
                }
            ]
        }
        rc = service_group_obj.config_service_group(**service_group_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service group failed")

    def test_03_add_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testadd_source_des_grp",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                        "group":"service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "source_group"
                    },
                    "destination":{
                        "group": "destination_group"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des_grp")
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des_grp")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testadd_source_des_grp")
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "service_group"}', "ERR: Failed to verify add routing policy service")


class Test_04_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47701"
    description= show_testcase_info(Parameter.TESTPLAN, '1516225', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516225')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_get_uuid_and_edit_entry(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="testadd")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testedit",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp1 = routing_policies_obj.get_route_policy_by_name(name="testedit")
        uuid_val1 =  resp1["route_policies"][0]["ipv4"]["uuid"]

        resp = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val1)
        Assertion.assert_regular(json.dumps(resp), '"name": "testedit"', "ERR: Failed to verify edited route policy")


class Test_05_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47702"
    description= show_testcase_info(Parameter.TESTPLAN, '1516226', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516226')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_routing_policies_from_name_to_group(self):
        # add policy using name
        routing_policies_json = {
            "route_policies":[
            {
                "ipv4":{
                    "name":"testcase5",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                        "name":"test_object"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "name": "source_address"
                    },
                    "destination":{
                        "name": "destination_address"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")


        resp = routing_policies_obj.get_route_policy_by_name(name="testcase5")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testcase5edit",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                        "group":"service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "source_group"
                    },
                    "destination":{
                        "group": "destination_group"
                    },
                    "disable_on_interface_down":False,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp1 = routing_policies_obj.get_route_policy_by_name(name="testcase5edit")
        uuid_val1 =  resp1["route_policies"][0]["ipv4"]["uuid"]

        resp = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val1)
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val1)
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val1)
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "service_group"}', "ERR: Failed to verify add routing policy service")


class Test_06_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47703"
    description= show_testcase_info(Parameter.TESTPLAN, '1516227', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516227')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_routing_policies(self):
        # add route policy as group
        routing_policies_json = {
            "route_policies":[
            {
                "ipv4":{
                    "name":"testcase6",
                    "comment":"description",
                    "interface":"X0",
                    "metric":20,
                    "service":{
                        "group":"service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "source_group"
                    },
                    "destination":{
                        "group": "destination_group"
                    },
                    "disable_on_interface_down":False,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        # editing group to any
        edit_routing_policies_json = {
            "route_policies":[
            {
                "ipv4":{
                    "name":"testcase6edited",
                    "comment":"description",
                    "interface":"X0",
                    "metric":20,
                    "service":{
                        "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "any": True
                    },
                    "destination":{
                        "any": True
                    },
                    "disable_on_interface_down":False,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy(name='testcase6',**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase6edited")
        Assertion.assert_regular(json.dumps(resp), '"source": {"any": True}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase6edited")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"any": True}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase6edited")
        Assertion.assert_regular(json.dumps(resp), '"service": {"any": True}', "ERR: Failed to verify add routing policy service")


class Test_07_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47704"
    description= show_testcase_info(Parameter.TESTPLAN, '1516228', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516228')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_retriving_route_policy_using_UUID(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"retrivedata",
                    "comment":"description",
                    "interface":"X1",
                    "metric":60,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="retrivedata")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]
        print('uuid_val', uuid_val)

        rc = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val)
        Assertion.assert_regular(json.dumps(rc), '"name": "retrivedata"', "ERR: Failed to verify route policy")


class Test_08_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47705"
    description= show_testcase_info(Parameter.TESTPLAN, '1516229', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516229')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_retriving_all_route_policy(self):
         resp = routing_policies_obj.get_route_policy()
         Assertion.assert_regular(json.dumps(resp), '"name": "retrivedata"', "ERR: Failed to verify route policy")


class Test_09_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47706"
    description= show_testcase_info(Parameter.TESTPLAN, '1516230', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516230')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_delete_route_policy_by_uuid(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="retrivedata")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]

        rc = routing_policies_obj.del_route_policy_by_uuid(uuid=uuid_val)

        resp1 = routing_policies_obj.get_route_policy_by_name(name="retrivedata")
        Assertion.assert_regular(json.dumps(resp1), 'Not found', "ERR: Failed to verify route policy")


class Test_10_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47707"
    description= show_testcase_info(Parameter.TESTPLAN, '1516231', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516231')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_delete_routing_policies_by_name(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testdelbyname",
                    "comment":"description",
                    "interface":"X1",
                    "metric":40,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        rc = routing_policies_obj.del_route_policy_by_name(name='testdelbyname')

        resp1 = routing_policies_obj.get_route_policy_by_name(name="testdelbyname")
        Assertion.assert_regular(json.dumps(resp1), 'Not found', "ERR: Failed to verify route policy")



class Test_11_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47708"
    description= show_testcase_info(Parameter.TESTPLAN, '1516232', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516232')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_routing_policies_by_name(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv4":{
                    "name":"testcase11",
                    "comment":"description",
                    "interface":"X1",
                    "metric":50,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase11")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]

        edit_routing_policies_json = {
            "route_policies":[
                {
                    "ipv4":{
                        "name":"testcase11edited",
                        "comment":"description",
                        "interface":"X1",
                        "metric":50,
                        "service":{
                        "name":"test_object"
                        },
                        "gateway":{
                        "default":True
                        },
                        "source":{
                        "name": "source_address"
                        },
                        "destination":{
                        "name": "destination_address"
                        },
                        "disable_on_interface_down":True,
                        "vpn_precedence":False,
                        "probe":"",
                        "ticket":{
                        "tag1":"test1"
                        },
                        "distance":{
                        "auto":True
                        },
                        "tos":"0x00",
                        "mask":"0x00",
                        "type":"standard"
                    }
                }
            ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase11edited")
        Assertion.assert_regular(json.dumps(resp), '"source": {"name": "source_address"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase11edited")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"name": "destination_address"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase11edited")
        Assertion.assert_regular(json.dumps(resp), '"service": {"name": "test_object"}', "ERR: Failed to verify add routing policy service")


class Test_12_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47709"
    description= show_testcase_info(Parameter.TESTPLAN, '1516233', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516233')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_routing_policies_by_group(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="testcase11edited")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]
        edit_routing_policies_json = {
            "route_policies":[
                {
                    "ipv4":{
                        "name":"testcase12edit",
                        "comment":"description",
                        "interface":"X1",
                        "metric":50,
                        "service":{
                        "group":"service_group"
                        },
                        "gateway":{
                        "default":True
                        },
                        "source":{
                            "group": "source_group"
                        },
                        "destination":{
                            "group": "destination_group"
                        },
                        "disable_on_interface_down":True,
                        "vpn_precedence":False,
                        "probe":"",
                        "ticket":{
                        "tag1":"test1"
                        },
                        "distance":{
                        "auto":True
                        },
                        "tos":"0x00",
                        "mask":"0x00",
                        "type":"standard"
                    }
                }
            ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase12edit")
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase12edit")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase12edit")
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "service_group"}', "ERR: Failed to verify add routing policy service")


class Test_13_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47710"
    description= show_testcase_info(Parameter.TESTPLAN, '1516234', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516234')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_routing_policies_by_any(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="testcase12edit")
        uuid_val =  resp["route_policies"][0]["ipv4"]["uuid"]
        edit_routing_policies_json = {
            "route_policies":[
                {
                    "ipv4":{
                        "name":"testcase13edit",
                        "comment":"description",
                        "interface":"X1",
                        "metric":50,
                        "service":{
                        "any":True
                        },
                        "gateway":{
                        "default":True
                        },
                        "source":{
                            "any": True
                        },
                        "destination":{
                            "any": True
                        },
                        "disable_on_interface_down":True,
                        "vpn_precedence":False,
                        "probe":"",
                        "ticket":{
                        "tag1":"test1"
                        },
                        "distance":{
                        "auto":True
                        },
                        "tos":"0x00",
                        "mask":"0x00",
                        "type":"standard"
                    }
                }
            ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase13edit")
        Assertion.assert_regular(json.dumps(resp), '"source": {"any": True}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase13edit")
        Assertion.assert_regular(json.dumps(resp), '"destination": {"any": True}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase13edit")
        Assertion.assert_regular(json.dumps(resp), '"service": {"any": True}', "ERR: Failed to verify add routing policy service")


class Test_14_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47711"
    description= show_testcase_info(Parameter.TESTPLAN, '1516235', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516235')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_add_routing_policies_ipv6(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"add_ipv6",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

    def test_03_perform_GET_request_and_verify_routing_policy(self):
        resp = routing_policies_obj.get_route_policy_by_name(name='add_ipv6',version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"name": "add_ipv6"', "ERR: Failed to verify route policy")


class Test_15_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47712"
    description= show_testcase_info(Parameter.TESTPLAN, '1516236', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516236')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_create_ipv6_address_object_and_service_object(self):
        ipv6_ao = {
            'name': 'ipv6_ao_source',
            'zone': 'LAN',
            'object_type': 'host',
            'value': '::ffff:c0a8:0dc8',
        }
        resp = address_objects.config_addressobject(**ipv6_ao)

        ipv6_ao1 = {
            'name': 'ipv6_ao_destination',
            'zone': 'LAN',
            'object_type': 'host',
            'value': '::ffff:c0a8:0dc8',
        }
        resp = address_objects.config_addressobject(**ipv6_ao1)

        service_object_json = {
            "object_type": "icmp",
            "name":"test_objectipv6",
            "icmp":"echo-request"
        }
        rc = service_obj.config_service_object(**service_object_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service object failed")

    def test_03_add_ipv6_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"testipv6_source_des",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                        "name":"test_objectipv6"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "name": "ipv6_ao_source"
                    },
                    "destination":{
                        "name": "ipv6_ao_destination"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testipv6_source_des",version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"name": "ipv6_ao_source"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testipv6_source_des", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"name": "ipv6_ao_destination"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testipv6_source_des", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"name": "test_objectipv6"}', "ERR: Failed to verify add routing policy service")


class Test_16_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47713"
    description= show_testcase_info(Parameter.TESTPLAN, '1516237', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516237')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_create_ipv6_address_object_and_service_group(self):
        address_group = {
            'address_groups': [{
                'ipv6': {
                    'name': 'ipv6_source_group',
                    "address_object": {
                        "ipv6": [
                            {
                                "name": "ipv6_ao_source"
                            }
                        ]
                    }
                }
            }]
        }
        response1 = add_group.add_addressgroup(**address_group)

        address_group = {
            'address_groups': [{
                'ipv6': {
                    'name': 'ipv6_destination_group',
                    "address_object": {
                        "ipv6": [
                            {
                                "name": "ipv6_ao_destination"
                            }
                        ]
                    }
                }
            }]
        }
        response1 = add_group.add_addressgroup(**address_group)

        service_object_json = {
            "object_type": "icmp",
            "name":"test_objectipv6_1",
            "icmp":"echo-request"
        }
        rc = service_obj.config_service_object(**service_object_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service object failed")

        service_group_json = {
            "name": "ipv6_service_group",
            "service_object": [
                {
                    "name": "test_objectipv6"
                },
                {
                    "name": "test_objectipv6_1"
                }
            ]
        }
        rc = service_group_obj.config_service_group(**service_group_json)
        Assertion.assert_equal(rc[0], True, "ERR: Add service group failed")

    def test_03_add_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"grp_ipv6_source_des",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                        "group":"ipv6_service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "ipv6_source_group"
                    },
                    "destination":{
                        "group": "ipv6_destination_group"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="grp_ipv6_source_des", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "ipv6_source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="grp_ipv6_source_des", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "ipv6_destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="grp_ipv6_source_des", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "ipv6_service_group"}', "ERR: Failed to verify add routing policy service")


class Test_17_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47714"
    description= show_testcase_info(Parameter.TESTPLAN, '1516238', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516238')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_get_uuid_and_edit_entry(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="add_ipv6", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"edit_ipv6",
                    "comment":"description",
                    "interface":"X1",
                    "metric":10,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,version = 'v6',**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp1 = routing_policies_obj.get_route_policy_by_name(name="edit_ipv6", version = 'v6')
        uuid_val1 =  resp1["route_policies"][0]["ipv6"]["uuid"]

        resp = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val1, version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"name": "edit_ipv6"', "ERR: Failed to verify edited route policy")


class Test_18_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47715"
    description= show_testcase_info(Parameter.TESTPLAN, '1516239', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516239')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_add_ipv6_routing_policies(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6addbyname",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                    "name":"test_objectipv6"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "name": "ipv6_ao_source"
                    },
                    "destination":{
                    "name": "ipv6_ao_destination"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        # editing name to group
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6editbygrp",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                        "group":"ipv6_service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "ipv6_source_group"
                    },
                    "destination":{
                        "group": "ipv6_destination_group"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy(name='ipv6addbyname',version='v6',**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editbygrp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "ipv6_source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editbygrp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "ipv6_destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editbygrp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "ipv6_service_group"}', "ERR: Failed to verify add routing policy service")


class Test_19_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47716"
    description= show_testcase_info(Parameter.TESTPLAN, '1516240', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516240')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_ipv6_routing_policies(self):
        # add route policy with group
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"testcase19",
                    "comment":"description",
                    "interface":"X0",
                    "metric":20,
                    "service":{
                        "group":"ipv6_service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "ipv6_source_group"
                    },
                    "destination":{
                        "group": "ipv6_destination_group"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        # editing group to any
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"testcase19edit",
                    "comment":"description",
                    "interface":"X0",
                    "metric":20,
                    "service":{
                        "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "any":True
                    },
                    "destination":{
                        "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy(name='testcase19',version='v6',**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase19edit", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"any": True}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase19edit", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"any": True}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="testcase19edit", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"any": True}', "ERR: Failed to verify add routing policy service")


class Test_20_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47717"
    description= show_testcase_info(Parameter.TESTPLAN, '1516241', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516241')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_retriving_ipv6_route_policy_using_UUID(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6_retrivedata",
                    "comment":"description",
                    "interface":"X0",
                    "metric":10,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6_retrivedata", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]

        rc = routing_policies_obj.get_route_policies_by_uuid(uuid=uuid_val, version = 'v6')
        Assertion.assert_regular(json.dumps(rc), '"name": "ipv6_retrivedata"', "ERR: Failed to verify route policy")


class Test_21_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47718"
    description= show_testcase_info(Parameter.TESTPLAN, '1516242', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516242')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_retriving_all_ipv6_route_policy(self):
         resp = routing_policies_obj.get_route_policy(version = 'v6')
         Assertion.assert_regular(json.dumps(resp), '"name": "ipv6_retrivedata"', "ERR: Failed to verify route policy")


class Test_22_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47719"
    description= show_testcase_info(Parameter.TESTPLAN, '1516243', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516243')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_delete_ipv6_route_policy_by_uuid(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6_retrivedata", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]

        rc = routing_policies_obj.del_route_policy_by_uuid(uuid=uuid_val, version = 'v6')

        resp1 = routing_policies_obj.get_route_policy_by_name(name="ipv6_retrivedata", version = 'v6')
        Assertion.assert_regular(json.dumps(resp1), 'Not found', "ERR: Failed to verify route policy")


class Test_23_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47720"
    description= show_testcase_info(Parameter.TESTPLAN, '1516244', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516244')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_delete_ipv6_routing_policies_by_name(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6delbyname",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        rc = routing_policies_obj.del_route_policy_by_name(name='ipv6delbyname',version = 'v6')

        resp1 = routing_policies_obj.get_route_policy_by_name(name="ipv6delbyname",version = 'v6')
        Assertion.assert_regular(json.dumps(resp1), 'Not found', "ERR: Failed to verify route policy")


class Test_24_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47721"
    description= show_testcase_info(Parameter.TESTPLAN, '1516245', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516245')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_ipv6_routing_policies_by_uuid(self):
        routing_policies_json = {
        "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6editbyuuid",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                    "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                    "any":True
                    },
                    "destination":{
                    "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.add_route_policy(**routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Add Routing Policy Failed.")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editbyuuid", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]

        edit_routing_policies_json = {
            "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6editedbyuuid",
                    "comment":"description",
                    "interface":"X1",
                    "metric":20,
                    "service":{
                        "name":"test_objectipv6"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "name": "ipv6_ao_source"
                    },
                    "destination":{
                        "name": "ipv6_ao_destination"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,version='v6',**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")


        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuid", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"name": "ipv6_ao_source"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuid", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"name": "ipv6_ao_destination"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuid", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"name": "test_objectipv6"}', "ERR: Failed to verify add routing policy service")

    

class Test_25_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47722"
    description= show_testcase_info(Parameter.TESTPLAN, '1516246', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516246')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_ipv6_routing_policies_by_uuid(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuid", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]

        edit_routing_policies_json = {
            "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6editedbyuuidgp",
                    "comment":"description",
                    "interface":"X1",
                    "metric":70,
                    "service":{
                        "group":"ipv6_service_group"
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "group": "ipv6_source_group"
                    },
                    "destination":{
                        "group": "ipv6_destination_group"
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,version='v6',**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")


        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidgp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"group": "ipv6_source_group"}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidgp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"group": "ipv6_destination_group"}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidgp", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"group": "ipv6_service_group"}', "ERR: Failed to verify add routing policy service")


class Test_26_Routing_Policies(Test):
    uuid = "SOSAIOT-TC-47723"
    description= show_testcase_info(Parameter.TESTPLAN, '1516247', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516247')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_edit_ipv6_routing_policies_by_uuid(self):
        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidgp", version = 'v6')
        uuid_val =  resp["route_policies"][0]["ipv6"]["uuid"]

        edit_routing_policies_json = {
            "route_policies":[
            {
                "ipv6":{
                    "name":"ipv6editedbyuuidany",
                    "comment":"description",
                    "interface":"X1",
                    "metric":70,
                    "service":{
                        "any":True
                    },
                    "gateway":{
                    "default":True
                    },
                    "source":{
                        "any":True
                    },
                    "destination":{
                        "any":True
                    },
                    "disable_on_interface_down":True,
                    "vpn_precedence":False,
                    "probe":"",
                    "ticket":{
                    "tag1":"test1"
                    },
                    "distance":{
                    "auto":True
                    },
                    "tos":"0x00",
                    "mask":"0x00",
                    "type":"standard"
                }
            }
        ]
        }
        rc = routing_policies_obj.edit_route_policy_by_uuid(uuid=uuid_val,version='v6',**edit_routing_policies_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Routing Policy Failed.")


        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidany", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"source": {"any": True}', "ERR: Failed to verify add routing policy source")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidany", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"destination": {"any": True}', "ERR: Failed to add routing policy destination")

        resp = routing_policies_obj.get_route_policy_by_name(name="ipv6editedbyuuidany", version = 'v6')
        Assertion.assert_regular(json.dumps(resp), '"service": {"any": True}', "ERR: Failed to verify add routing policy service")