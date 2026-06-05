import re
import sys
import os
import json
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_REST_API')
from definition.settings_two import *

class Copy_file(Test):
    uuid = 'NonTC'

    def test_01_copy_all_files(self):
        test_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/api-test.sh"
        json_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test.json"
        json_multi_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test-multi.json"
        xml_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test.xml"
        xml_multi_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test-multi.xml"
        json_multi_users_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test-multi-users.json"
        random_user_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test-random.json"
        xml_default_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/SSO_API_TWO/test-default.xml"

        logger.info("The api-test.sh file is {}".format(test_file))
        logger.info("The JSON file is {}".format(json_file))
        logger.info("The JSON multi file is {}".format(json_multi_file))
        logger.info("The XML file is {}".format(xml_file))
        logger.info("The JSON file is {}".format(xml_multi_file))
        logger.info("The JSON file is {}".format(json_multi_users_file))

        static_client.send_command("cp " + test_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())

        static_client.send_command("cp " + json_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())

        static_client.send_command("cp " + json_multi_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())

        static_client.send_command("cp " + xml_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())

        static_client.send_command("cp " + xml_multi_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())
        
        static_client.send_command("cp " + json_multi_users_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())
        
        static_client.send_command("cp " + random_user_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())

        static_client.send_command("cp " + xml_default_file + " /root/Downloads/")
        logger.info("The file is successfully copied")
        time.sleep(10)
        os.chdir("/root/Downloads/")
        time.sleep(5)
        logger.info("The current build path is")
        logger.info(os.getcwd())
        
        logger.info("All files is successfully copied")

# GUI_001
class SSO_REST_API_1(Test):
    uuid = '1505477'
    description = show_testcase_info(Parameter.TESTPLAN, '1505477', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505477')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_add_sso_clinet(self):
        sso_client_add = {
            "host": "192.168.168.201",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "low": True
            },
            "replay_prevention": True,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.create_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"host": "192.168.168.201"', "Err:Failed to add SSO API value")

# Func_001
class SSO_REST_API_2(Test):
    uuid = '1505357'
    description = show_testcase_info(Parameter.TESTPLAN, '1505357', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505357')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_third_party_api(self):
        enable_third_party_api = {
            "third_party_api": True,
        }
        config_third_party_api = usersetting.user_method_authentication(**enable_third_party_api)
        print(config_third_party_api)
        Assertion.assert_regular(json.dumps(config_third_party_api), 'true', "ERR: :Third party API not enabled")

    def test_02_post_single_user_with_wrong_ip_remote(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip-remote": "10.0.0.1",
            "name": "user1",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"name": "user1"' , "ERR: :Client got created ")

# Func_002
class SSO_REST_API_3(Test):
    uuid = '1505378'
    description = show_testcase_info(Parameter.TESTPLAN, '1505378', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505378')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_attribute_not_supported(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.99",
            "name": "user2",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "reason": "Just testing",
            "random": "any value"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)
            
        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)

        resp = userstatus.show_user_status()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"name": "user2"', "ERR: :Client not created ")
        
# Func_003
class SSO_REST_API_4(Test):
    uuid = '1505367'
    description = show_testcase_info(Parameter.TESTPLAN, '1505367', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505367')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multi_users(self):
        os.chdir("/root/Downloads/")

        var = [
            {
                "ip": "192.168.168.100",
                "name": "multi1",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.101",
                "name": "multi2",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.102",
                "name": "multi3",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.103",
                "name": "multi4",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            }
        ]

        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)
            
        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post-multi"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi1"', "ERR: :Client not created ")
        
    def test_02_delete_multi_users_with_some_error_user_info(self):
        os.chdir("/root/Downloads/")

        var = [
            {
                "ip": "192.168.168.109",
                "name": "multi1",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.101",
                "name": "multi2",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.102",
                "name": "multi3",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "192.168.168.103",
                "name": "multi4",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            }
        ]
        
        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)
            
        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi"], shell=True)
        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi1"', "ERR: :Client got deleted ")

# Func_004
class SSO_REST_API_5(Test):
    uuid = '1505379'
    description = show_testcase_info(Parameter.TESTPLAN, '1505379', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505379')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multi_user_with_large_content(self):
        os.chdir("/root/Downloads/")
            
        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post-multi-users"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi10"', "ERR: :Client not created ")

        
    def test_02_detele_multi_user_with_large_content(self):
        os.chdir("/root/Downloads/")
            
        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi-users"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"user_name": "multi10"', "ERR: :Client not deleted ")
        
# Func_005
class SSO_REST_API_6(Test):
    uuid = '1505380'
    description = show_testcase_info(Parameter.TESTPLAN, '1505380', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505380')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_option_request_with_xml(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -x -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user1_xml"', "ERR: :Client not created ")


# Func_006
class SSO_REST_API_7(Test):
    uuid = '1505381'
    description = show_testcase_info(Parameter.TESTPLAN, '1505381', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505381')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_option_request_with_json(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.99",
            "name": "user1_json",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"name": "user1_json"', "ERR: :Client not created ")
        
# Func_007
class SSO_REST_API_8(Test):
    uuid = '1505382'
    description = show_testcase_info(Parameter.TESTPLAN, '1505382', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505382')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_request_content_type_by_default_xml(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -a low -s 1234 post-def"], shell=True)
        resp = userstatus.show_user_status_inactive()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user_xml_default"', "ERR: :Client not created ")

# Func_008
class SSO_REST_API_9(Test):
    uuid = '1505383'
    description = show_testcase_info(Parameter.TESTPLAN, '1505383', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505383')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_request_content_type_set_to_types_other_than_xml_or_json(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -r -a low -s 1234 post-random"], shell=True)
        resp = userstatus.show_user_status()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"name": "user_random"', "ERR: :Client got created ")

class SSO_REST_API_10(Test):
    uuid = '1505358'
    description = show_testcase_info(Parameter.TESTPLAN, '1505358', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505358')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_third_party_api(self):
        enable_third_party_api = {
            "third_party_api": True,
        }
        config_third_party_api = usersetting.user_method_authentication(**enable_third_party_api)
        print(config_third_party_api)
        Assertion.assert_regular(json.dumps(config_third_party_api), 'true', "ERR: :Third party API not enabled")

    def test_02_post_single_user_with_wrong_ip_remote(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip-remote": "10.0.0.2",
            "name": "user7",
            "description": "Error not supported",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        logger.info("This is response")
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"name": "user7"' , "ERR: :Client got created ")