import re
import sys
import os
import json
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_BVT')
from definition.settings import *

class Copy_file(Test):
    uuid = 'NonTC'

    def test_01_copy_all_files(self):
        test_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_BVT/testcases/api-test.sh"
        json_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_BVT/testcases/test.json"
        json_multi_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_BVT/testcases/test-multi.json"
        xml_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_BVT/testcases/test.xml"

        logger.info("The api-test.sh file is {}".format(test_file))
        logger.info("The JSON file is {}".format(json_file))
        logger.info("The JSON multi file is {}".format(json_multi_file))
        logger.info("The XML file is {}".format(xml_file))

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

        logger.info("All files is successfully copied")

class SSO_REST_API_BVT_1(Test):
    uuid = "SOSAIOT-TC-75765"
    description = show_testcase_info(Parameter.TESTPLAN, '1505482', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505482')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_sso_clinet(self):
        sso_client_add = {
            "host": "192.168.168.201",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "low": True
            },
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        sso_client.edit_sso_third_party_client(**sso_client_add)
        result = sso_client.get_sso_third_party_client()
        logger.info(f"The response is {result}")
        Assertion.assert_regular(json.dumps(result), '"low": True', "Err:Failed to edit SSO API value")

class SSO_REST_API_BVT_2(Test):
    uuid = "SOSAIOT-TC-75729"
    description = show_testcase_info(Parameter.TESTPLAN, '1505341', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505341')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_third_party_api(self):
        enable_third_party_api = {
            "third_party_api": True,
        }
        config_third_party_api = usersetting.user_method_authentication(**enable_third_party_api)
        print(config_third_party_api)
        Assertion.assert_regular(json.dumps(config_third_party_api), 'true', "ERR: :Third party API not enabled")

    def test_02_post_single_user_with_all_info(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.125",
            "name": "user1",
            "domain": "nowhere.com",
            "type": "domain",
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        logger.info(f"The response is {resp}")
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user1"', "ERR: :Client not created ")

class SSO_REST_API_BVT_3(Test):
    uuid = "SOSAIOT-TC-75730"
    description = show_testcase_info(Parameter.TESTPLAN, '1505342', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505342')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_post_xml(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -x -a low -s 1234 post"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(f"The response is {resp}")
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user2"', "ERR: :Client not created ")

class SSO_REST_API_BVT_4(Test):
    uuid = "SOSAIOT-TC-75723"
    description = show_testcase_info(Parameter.TESTPLAN, '1527434', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527434')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_third_party_api(self):
        enable_third_party_api = {
            "third_party_api": True,
        }
        config_third_party_api = usersetting.user_method_authentication(**enable_third_party_api)
        print(config_third_party_api)
        Assertion.assert_regular(json.dumps(config_third_party_api), 'true', "ERR: :Third party API not enabled")

    def test_02_post_multi_dual_ipv4_ipv6(self):
        os.chdir("/root/Downloads/")

        var = [
            {
                "ip": [ "192.168.168.100", "fd00:1111:2222:1::100" ],
                "name": "multi1",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": [ "192.168.168.102", "fd00:1111:2222:1::102" ],
                "name": "multi2",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            },
                        {
                "ip": [ "192.168.168.103", "fd00:1111:2222:1::103" ],
                "name": "multi3",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            }
        ]
        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post-multi"], shell=True)
        resp = userstatus.show_user_status()
        logger.info(f"The response is {resp}")
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi2"' , "ERR: :Client not created ")

class SSO_REST_API_BVT_5(Test):
    uuid = "SOSAIOT-TC-75724"
    description = show_testcase_info(Parameter.TESTPLAN, '1527435', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1527435')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_sso_third_party_api(self):
        enable_third_party_api = {
            "third_party_api": True,
        }
        config_third_party_api = usersetting.user_method_authentication(**enable_third_party_api)
        print(config_third_party_api)
        Assertion.assert_regular(json.dumps(config_third_party_api), 'true', "ERR: :Third party API not enabled")

    def test_02_delete_multi_dual_ipv4_ipv6(self):
        os.chdir("/root/Downloads/")

        var = [
            {
                "ip": [ "192.168.168.100", "fd00:1111:2222:1::100" ],
                "name": "multi1",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": [ "192.168.168.102", "fd00:1111:2222:1::102" ],
                "name": "multi2",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            },
                        {
                "ip": [ "192.168.168.103", "fd00:1111:2222:1::103" ],
                "name": "multi3",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            }
        ]
        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi"], shell=True)
        resp = userstatus.show_user_status()
        logger.info(f"The response is {resp}")
        Assertion.assert_not_regular(json.dumps(resp), '"name": "multi2"' , "ERR: :Client still exist")