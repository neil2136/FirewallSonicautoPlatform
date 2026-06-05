from asyncio.log import logger
from definition.settings import *
import re

#  Address objects are auto-added in the "SonicWALL SSO Agents" group as agents are added.
class Test_SSO_Enhancements_1(Test):
    uuid = "SOSAIOT-TC-75229"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_sso_agent(self):
        enable_sso = {
            'sso_agent': True,
        }
        rc = user_settings_obj.user_method_authentication(**enable_sso)
        Assertion.assert_equal(rc, True, "SSO agent not enable")
        logger.info("SSO agent enable")

    def test_02_add_sso_agent(self):
        add_sso_agent_ip = {
            'action': 'add',
            'host': sso_ip,
            'port': sso_default_port,
            'timeout': 10,
            'max_requests': 3,
            'enable': True,
            'shared_key': '123456'
        }
        rc = user_sso_obj.sso_agent(**add_sso_agent_ip)
        Assertion.assert_equal(rc, True, "ERR: SSO agent failed to add")
        logger.info("SSO agent added successfully")
    def test_03_service_group(self):
        flag = False
        output = servicegroupapi.get_service_groups_via_name(name="SonicWALL SSO Agents")
        print(output)
        Assertion.assert_regular(json.dumps(output), 'SSO Agent 1', 'err: Failed to create localuser')
        rc = so_obj.get_serviceobject()
        logger.info(rc)
        match = re.search(r'SSO Agent 1.*?udp.*?2258.*?2258', str(rc), re.I | re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "SSO Agent 1 not found failed")

# .One "SonicWALL SSO Agent" service with the port number 2258 is shown in the Services table
class Test_SSO_Enhancements_2(Test):
    uuid = "SOSAIOT-TC-75231"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_service_group(self):
        flag = False
        output = servicegroupapi.get_service_groups_via_name(name="SonicWALL SSO Agents")
        logger.info(output)
        Assertion.assert_regular(json.dumps(output), 'SSO Agent 1', 'err: sso agent didnt add to service group')
        logger.info("sso agent found in service group")
        rc = so_obj.get_serviceobject()
        logger.info(rc)
        match = re.search(r'SSO Agent 1.*?udp.*?2258.*?2258', str(rc), re.I | re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "Err: SSO agent or port 2258 not found in service object")
        logger.info("SSO agent or port 2258 found in service object")

# Service objects are auto-added in the "SonicWALL SSO Authentication Agents" service group as agents with different port numbers are added.
class Test_SSO_Enhancements_3(Test):
    uuid = "SOSAIOT-TC-75230"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_sso_agent(self):
        add_sso_agent_ip = {
            'action': 'add',
            'host': sso_ip_2,
            'port': sso_new_port,
            'timeout': 10,
            'max_requests': 3,
            'enable': True,
            'shared_key': '123456'
        }
        rc = user_sso_obj.sso_agent(**add_sso_agent_ip)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_sso_agent_IP failed")

    def test_03_service_group(self):
        output = servicegroupapi.get_service_groups_via_name(name="SonicWALL SSO Agents")
        print(output)
        Assertion.assert_regular(json.dumps(output), 'SSO Agent 2', 'err: sso agent didnt add to service group')
        logger.info("sso agent found in service group")
        rc = so_obj.get_serviceobject()
        logger.info(rc)
        flag = False
        match = re.search(r'SSO Agent 1.*?udp.*?2258.*?2258', str(rc), re.I | re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "test_05_Verify_SSO_Agent_Service_Object failed")
        flag = False
        match = re.search(r'SSO Agent 2.*?udp.*?2256.*?2256', str(rc), re.I | re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "Err: SSO agent or port 2256 not found in service object")
        logger.info("SSO agent or port 2256 found in service object")

# Address objects are auto-deleted from the "SonicWALL SSO Agents" group as agents are deleted.
class Test_SSO_Enhancements_4(Test):
    uuid = "SOSAIOT-TC-75235"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_sso_agent(self):
        rc = user_sso_obj.del_sso_agent(name=sso_ip, port=sso_default_port)
        Assertion.assert_equal(rc, True, "ERR: SSO agent delete failed")
        logger.info(sso_ip+" deleted")

# Add a maximum number of agents.
class Test_SSO_Enhancements_5(Test):
    uuid = "SOSAIOT-TC-75234"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_sso_agent(self):
        rc = user_sso_obj.del_sso_agent(name=sso_ip_2, port=sso_new_port)
        Assertion.assert_equal(rc, True, "ERR: SSO agent delete failed")
        logger.info(sso_ip_2 + " deleted")

    def test_02_add_sso_agent_IP_max(self):
        for _ in range(8):
            ips = ".".join(str(random.randint(0, 255)) for _ in range(4))
            print(ips)
            add_sso_agent_ip = {
                     'action': 'add',
                     'host': ips,
                     'port': sso_default_port,
                     'timeout': 10,
                     'max_requests': 3,
                     'enable': True,
                     'shared_key':'123456'
            }

            rc = user_sso_obj.sso_agent(**add_sso_agent_ip)
            Assertion.assert_equal(rc, True, "ERR: test_01_add_sso_agent_IP failed")

        logger.info("Adding more then limit")
        add_sso_agent_ip = {
            'action': 'add',
            'host': "1.1.1.1",
            'port': sso_default_port,
            'timeout': 10,
            'max_requests': 3,
            'enable': True,
            'shared_key': '123456'
        }

        rc = user_sso_obj.sso_agent(**add_sso_agent_ip)
        Assertion.assert_equal(rc, False, "ERR: Adding more thn max limit didnt fail")
        # print(rc)
        # expected_error = "SSO Authentication Agent Host name / IP address: Data out of bounds (min = 0, max = 0)."
        # Assertion.assert_regular(json.dumps(rc),expected_error, "Error message not found in response")
        # logger.info(expected_error+"-> error raised")


