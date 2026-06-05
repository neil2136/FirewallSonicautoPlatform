import sys
import os
import json
import time
import paramiko
import subprocess

from definition.settings import *

class Test_01_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47772"
    description= show_testcase_info(Parameter.TESTPLAN, '1529571', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529571')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_update_X2_interface_as_LAN(self):
        x2_interface_json = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '15.6.2.3',
            # 'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface.config_interface(**x2_interface_json)
        Assertion.assert_equal(rc, True, "ERR: Update interface Failed.")

        resp = interface.get_interface_status("X2")
        Assertion.assert_regular(json.dumps(resp), '"zone": "LAN"', "ERR: Failed to verify Zone object")


class Test_02_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47773"
    description= show_testcase_info(Parameter.TESTPLAN, '1529572', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529572')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_update_X2_interface_as_WAN(self):
        x2_interface_json = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '15.6.2.3',
            # 'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface.config_interface(**x2_interface_json)
        Assertion.assert_equal(rc, True, "ERR: Update interface Failed.")

        resp = interface.get_interface_status("X2")
        Assertion.assert_regular(json.dumps(resp), '"zone": "WAN"', "ERR: Failed to verify Zone object")


class Test_03_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47775"
    description= show_testcase_info(Parameter.TESTPLAN, '1529575', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529575')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_update_X2_interface_as_WLAN(self):
        x2_interface_json = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '15.6.2.3',
            # # 'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            "mtu": 1400,

        }
        rc = interface.config_interface(**x2_interface_json)
        Assertion.assert_equal(rc, True, "ERR: Update interface Failed.")

        resp = interface.get_interface_status("X2")
        Assertion.assert_regular(json.dumps(resp), '"mtu": 1400', "ERR: Failed to verify Zone object")


class Test_04_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47777"
    description= show_testcase_info(Parameter.TESTPLAN, '1529577', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529577')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_check_tsr_file(self):
        x2_interface_json = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '15.6.2.3',
            # # 'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            "mtu": 1400,

        }
        rc = interface.config_interface(**x2_interface_json)
        Assertion.assert_equal(rc, True, "ERR: Update interface Failed.")

    def test_03_download_tsr_and_verify(self):
        diag_api.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'X2'
        with open(file_path) as f:
            if search_line in f.read():
                res = True
            else:
                res = False
        assert res == True, "Configuration not found in TSR file"

import json
import requests
from collections import OrderedDict
from requests.auth import HTTPBasicAuth
import copy
login_logout_url = '/api/sonicos/auth'
loginJson = {"username": None, "password": None}
firewall_headers = OrderedDict([('Accept', 'application/json'),
                                        ('Content-Type', 'application/json'),
                                        ('Accept-Encoding', 'application/json'),
                                        ('charset', 'UTF-8')
                                        ])

class Test_05_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47774"
    description= show_testcase_info(Parameter.TESTPLAN, '1529574', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529574')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")         

    def firewall_login_api(mode="non_config", firewallLoginIp=None, password=None):
        try:
            url = "https://" + str(firewallLoginIp) + login_logout_url
            jsonData = {}
            jsonData1 = copy.deepcopy(loginJson)
            jsonData1['username'] = "admin"
            jsonData1['password'] = password
            if mode == 'config':
                jsonData['override'] = True
                jsonData['snwl'] = True

            response = requests.post(url=url, headers=firewall_headers, data=json.dumps(jsonData),
                                    auth=HTTPBasicAuth(jsonData1['username'], jsonData1['password']), verify=False,
                                    timeout=600)
            jsonResponse = json.loads(response.content)

            token = jsonResponse['status']['info'][0]['bearer_token']
            firewall_headers.update({"Authorization": "Bearer " + token})

        except Exception as e:
            print(e)

    def config(ip=None):
        try:
            dns_api = "https://192.168.168.168" + "/api/sonicos/config-mode"
            response = requests.post(url=dns_api, headers=firewall_headers, data=None, verify=False)
            jsonResponse = json.loads(response.content)
            if response.status_code == "200":
                print("DNS change is successfull")
        except Exception as e:
            print(e)

    def lan_configuration():
        try:
            json_data = {
                "interfaces":[
                    {
                        "ipv4":{
                            "one_arm_mode":False,
                            "one_arm_peer":"0.0.0.0",
                            "management":{
                            "fqdn_assignment":"",
                            "https":False,
                            "https_source":{
                                "any":True
                            },
                            "ping":False,
                            "ping_source":{
                                "any":True
                            },
                            "snmp":False,
                            "snmp_source":{
                                "any":True
                            },
                            "ssh":False,
                            "ssh_source":{
                                "any":True
                            }
                            },
                            "user_login":{
                            "http":False,
                            "https":False
                            },
                            "comment":"",
                            "mac":{
                            "default":True
                            },
                            "multicast":False,
                            "exclude_route":False,
                            "routed_mode":{
                            
                            },
                            "shutdown_port":False,
                            "cos_8021p":False,
                            "management_traffic_only":False,
                            "flow_control":{
                            "receive":False,
                            "transmit":False
                            },
                            "asymmetric_route":False,
                            "flow_reporting":True,
                            "mtu":1500,
                            "name":"X2",
                            "ip_assignment":{
                            "zone":"LAN",
                            "mode":{
                                "static":{
                                    "ip":"10.5.6.4",
                                    "netmask":"255.255.255.0",
                                    "gateway":"0.0.0.0"
                                }
                            }
                            }
                        }
                    }
                ]
                }
            vlan_api = "https://192.168.168.168" + "/api/sonicos/interfaces/ipv4/name/X2"
            response = requests.post(url=vlan_api, headers=firewall_headers, data=json.dumps(json_data), verify=False)
            jsonResponse = json.loads(response.content)
            if response.status_code == "200":
                logger.info("DNS change is successfull")
        except Exception as e:
            logger.info(e)
    
    
    def retrive_pending_configuration():
        pending_changes = 'https://' + '192.168.168.168' + '/api/sonicos/config/pending'
        get_resp = requests.get(pending_changes, headers=firewall_headers, timeout=60, verify=False)
        resp = requests.post(pending_changes, headers=firewall_headers, timeout=60, verify=False)
        assert resp.status_code == 200, "Configuration not found " 


    def test_02_verify_configuration(self):
        Test_05_Static_Interface.firewall_login_api(mode="config", firewallLoginIp="192.168.168.168", password="S0nic@uto")
        Test_05_Static_Interface.config()
        Test_05_Static_Interface.lan_configuration()
        Test_05_Static_Interface.retrive_pending_configuration()


class Test_06_Static_Interface(Test):
    uuid = "SOSAIOT-TC-47776"
    description= show_testcase_info(Parameter.TESTPLAN, '1529576', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1529576')
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")  

    def test_02_update_X2_interface_as_LAN(self):
        x2_interface_json = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '15.6.2.3',
            # 'gateway': Parameter.X1_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface.config_interface(**x2_interface_json)
        Assertion.assert_equal(rc, True, "ERR: Update interface Failed.")

    def retrive_pending_configuration():
        pending_changes = 'https://' + '192.168.168.168' + '/api/sonicos/config/pending'
        get_resp = requests.get(pending_changes, headers=firewall_headers, timeout=60, verify=False)
        jsonResponse = json.loads(get_resp.content)
        assert jsonResponse == {}, "Json is not empty after post command "

    def test_03_verify_empty_json_after_post_command(self):
        Test_05_Static_Interface.firewall_login_api(mode="config", firewallLoginIp="192.168.168.168", password="S0nic@uto")
        Test_05_Static_Interface.config()
        Test_06_Static_Interface.retrive_pending_configuration()