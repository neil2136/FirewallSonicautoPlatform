import re
import sys
import os
import json
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_REST_API')
from definition.settings import *

class Copy_file(Test):
    uuid = 'NonTC'

    def test_01_copy_all_files(self):
        test_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/api-test.sh"
        json_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/test.json"
        json_multi_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/test-multi.json"
        xml_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/test.xml"
        xml_multi_file = os.environ["PYTHON_SONICOS_HOME"] + "/User/SSO_REST_API/testcases/test-multi.xml"

        logger.info("The api-test.sh file is {}".format(test_file))
        logger.info("The JSON file is {}".format(json_file))
        logger.info("The JSON multi file is {}".format(json_multi_file))
        logger.info("The XML file is {}".format(xml_file))
        logger.info("The JSON file is {}".format(xml_multi_file))

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

        logger.info("All files is successfully copied")

# GUI_001
class SSO_REST_API_1(Test):
    uuid = "SOSAIOT-TC-75763"
    description = show_testcase_info(Parameter.TESTPLAN, '001', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '001')
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
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.create_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"host": "192.168.168.201"', "Err:Failed to add SSO API value")

# Func_001
class SSO_REST_API_2(Test):
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

    def test_02_post_single_user_with_post_json(self):
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
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user1"', "ERR: :Client not created ")

# Func_002
class SSO_REST_API_3(Test):
    uuid = "SOSAIOT-TC-75730"
    description = show_testcase_info(Parameter.TESTPLAN, '1505342', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505342')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_post_xml(self):
        os.chdir("/root/Downloads/")
        # os.chdir('..')
        # os.chdir(os.getcwd() + '/testcases')

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -x -a low -s 1234 post"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user2"', "ERR: :Client not created ")

# Func_005
class SSO_REST_API_4(Test):
    uuid = "SOSAIOT-TC-75731"
    description = show_testcase_info(Parameter.TESTPLAN, '1505345', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505345')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_post_json_group_lookup_true(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.96",
            "name": "user3",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": True,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        Assertion.assert_regular(json.dumps(resp), '"name": "user3"', "ERR: :Client not created ")

# Func_013
class SSO_REST_API_5(Test):
    uuid = "SOSAIOT-TC-75732"
    description = show_testcase_info(Parameter.TESTPLAN, '1505353', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505353')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_no_ip(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "",
            "name": "",
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"error": "Invalid IP address: ip: ''"', "ERR: :Client not created ")

# Func_014
class SSO_REST_API_6(Test):
    uuid = "SOSAIOT-TC-75733"
    description = show_testcase_info(Parameter.TESTPLAN, '1505354', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505354')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_wrong_ip(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "-110.10.10.86",
            "name": "user4",
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"error": "Invalid IP address', "ERR: :Client not created ")

# Func_015
class SSO_REST_API_7(Test):
    uuid = "SOSAIOT-TC-75734"
    description = show_testcase_info(Parameter.TESTPLAN, '1505355', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505355')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_wrong_type(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.97",
            "name": "user5",
            "domain": "nowhere.com",
            "type": "ujjwal",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"error": "Invalid value for attribute: type:"', "ERR: :Client not created ")

# Func_019
class SSO_REST_API_8(Test):
    uuid = "SOSAIOT-TC-75737"
    description = show_testcase_info(Parameter.TESTPLAN, '1505359', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505359')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_inactive_ip_duplicate(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.125",
            "name": "user6",
            "domain": "nowhere.com",
            "type": "domain",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user6"', "ERR: :Client not created ")

# Func_120
class SSO_REST_API_9(Test):
    uuid = "SOSAIOT-TC-75762"
    description = show_testcase_info(Parameter.TESTPLAN, '120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_post_json_active(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.98",
            "name": "user7",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        Assertion.assert_regular(json.dumps(resp), '"name": "user7"', "ERR: :Client not created ")

    def test_02_post_single_user_with_post_json_inactive(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.99",
            "name": "user8",
            "domain": "nowhere.com",
            "type": "domain",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user8"', "ERR: :Client not created ")

# Func_020
class SSO_REST_API_10(Test):
    uuid = "SOSAIOT-TC-75738"
    description = show_testcase_info(Parameter.TESTPLAN, '1505360', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505360')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_active_ip_duplicate(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.98",
            "name": "user9",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        Assertion.assert_regular(json.dumps(resp), '"name": "user9"', "ERR: :Client not created ")

# Func_021
class SSO_REST_API_11(Test):
    uuid = "SOSAIOT-TC-75739"
    description = show_testcase_info(Parameter.TESTPLAN, '1505361', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505361')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_ip_name_duplicate(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "192.168.168.99",
            "name": "user8",
            "domain": "nowhere.com",
            "type": "domain",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"message": "User user8 was already logged in"', "ERR: :Client not created ")

# Func_027
class SSO_REST_API_12(Test):
    uuid = "SOSAIOT-TC-75740"
    description = show_testcase_info(Parameter.TESTPLAN, '1505367', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505367')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multiple_user_with_post_multi_json(self):
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
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi1"', "ERR: :Client not created ")

# Func_028
class SSO_REST_API_13(Test):
    uuid = "SOSAIOT-TC-75741"
    description = show_testcase_info(Parameter.TESTPLAN, '1505368', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1505368')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multiple_user_with_post_multi_xml(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -x -a low -s 1234 post-multi"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "jdoe"', "ERR: :Client not created ")

# Func_031
class SSO_REST_API_14(Test):
    uuid = "SOSAIOT-TC-75742"
    description = show_testcase_info(Parameter.TESTPLAN, '031', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '031')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_single_user_with_delete_json(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"user_name": "user8"', "ERR: :Client not created ")

# Func_036
class SSO_REST_API_15(Test):
    uuid = "SOSAIOT-TC-75743"
    description = show_testcase_info(Parameter.TESTPLAN, '036', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '036')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_multiple_user_with_delete_json(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi"], shell=True)

        r = userstatus.show_user_status()
        resp = userstatus.show_user_status_inactive()
        logger.info(r)
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), 'Delete multiple users with json is done', "ERR: :Client not created ")

# Func_037
class SSO_REST_API_16(Test):
    uuid = "SOSAIOT-TC-75744"
    description = show_testcase_info(Parameter.TESTPLAN, '037', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '037')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_multiple_user_with_delete_xml(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -x -a low -s 1234 delete-multi"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), 'Delete multiple users with xml is done', "ERR: :Client not created ")

# Func_044
class SSO_REST_API_17(Test):
    uuid = "SOSAIOT-TC-75751"
    description = show_testcase_info(Parameter.TESTPLAN, '044', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '044')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_ip_attribute_ipv6_address(self):
        os.chdir("/root/Downloads/")

        var = {
            "ip": "fe80::f816:3eff:fe8d:d1dd:12",
            "name": "user-ipv6",
            "domain": "nowhere.com",
            "type": "domain",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user-ipv6"', "ERR: :Client not created ")

# Func_045
class SSO_REST_API_18(Test):
    uuid = "SOSAIOT-TC-75752"
    description = show_testcase_info(Parameter.TESTPLAN, '045', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '045')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_ipv4_attribute_ipv4_address(self):
        os.chdir("/root/Downloads/")

        var = {
            "ipv4": "192.168.168.108",
            "name": "user10",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status()
        Assertion.assert_regular(json.dumps(resp), '"name": "user10"', "ERR: :Client not created ")

# Func_046
class SSO_REST_API_19(Test):
    uuid = "SOSAIOT-TC-75753"
    description = show_testcase_info(Parameter.TESTPLAN, '046', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_ipv6_attribute_ipv6_address(self):
        os.chdir("/root/Downloads/")

        var = {
            "ipv6": "fe80::f816:3eff:fe8d:d1dd:14",
            "name": "user-ipv7",
            "domain": "nowhere.com",
            "type": "domain",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_regular(json.dumps(resp), '"user_name": "user-ipv7"', "ERR: :Client not created ")

# Func_047
class SSO_REST_API_20(Test):
    uuid = "SOSAIOT-TC-75754"
    description = show_testcase_info(Parameter.TESTPLAN, '047', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '047')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multiple_user_with_all_ipv6_attribute_ipv6_address(self):
        os.chdir("/root/Downloads/")

        var = [
            {
                "ipv6": "fe80::f816:3eff:fe8d:d1dd:20",
                "name": "multi5",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ipv6": "fe80::f816:3eff:fe8d:d1dd:22",
                "name": "multi6",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ipv6": "fe80::f816:3eff:fe8d:d1dd:23",
                "name": "multi7",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ipv6": "fe80::f816:3eff:fe8d:d1dd:24",
                "name": "multi8",
                "domain": "nowhere.com",
                "init-state": "active",
                "type": "domain",
                "reason": "Just testing"
            }
        ]

        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post-multi"], shell=True)
        r = userstatus.show_user_status_inactive()
        logger.info(r)
        resp = userstatus.show_user_status()
        logger.info(resp)
        Assertion.assert_regular(json.dumps(r), '"user_name": "multi5"', "ERR: :Client not created ")
        Assertion.assert_regular(json.dumps(resp), '"name": "multi8"', "ERR: :Client not created ")

# Func_052
class SSO_REST_API_21(Test):
    uuid = "SOSAIOT-TC-75759"
    description = show_testcase_info(Parameter.TESTPLAN, '052', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_multipl_euser_with_all_ipv6_attribute_ipv6_address(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi"], shell=True)

        r = userstatus.show_user_status()
        resp = userstatus.show_user_status_inactive()
        logger.info(r)
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), 'Delete multiple is done', "ERR: :Client not created ")

# Func_048
class SSO_REST_API_22(Test):
    uuid = "SOSAIOT-TC-75755"
    description = show_testcase_info(Parameter.TESTPLAN, '048', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '048')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_multiple_user_with_all_ip_attribute_some_ipv4_ipv6_address(self):
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
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "fe80::f816:3eff:fe8d:d1dd:16",
                "name": "multi3",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            },
            {
                "ip": "fe80::f816:3eff:fe8d:d1dd:18",
                "name": "multi4",
                "domain": "nowhere.com",
                "type": "domain",
                "reason": "Just testing"
            }
        ]

        with open("test-multi.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post-multi"], shell=True)
        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_regular(json.dumps(resp), '"user_name": "multi1"', "ERR: :Client not created ")

# Func_053
class SSO_REST_API_23(Test):
    uuid = "SOSAIOT-TC-75760"
    description = show_testcase_info(Parameter.TESTPLAN, '053', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '053')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_multiple_user_with_all_ip_attribute_some_ipv4_ipv6_address(self):
        os.chdir("/root/Downloads/")

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 delete-multi"], shell=True)

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), 'Delete multiple is done', "ERR: :Client not created ")

# Func_049
class SSO_REST_API_24(Test):
    uuid = "SOSAIOT-TC-75756"
    description = show_testcase_info(Parameter.TESTPLAN, '049', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '049')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_ip4_attribut_but_wrong_ipv4_address(self):
        os.chdir("/root/Downloads/")

        var = {
            "ipv4": "fe80::f816:3eff:fe8d:d1dd:24",
            "name": "user9",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"error": "Invalid IPv4 address"', "ERR: :Client not created ")

# Func_050
class SSO_REST_API_25(Test):
    uuid = "SOSAIOT-TC-75757"
    description = show_testcase_info(Parameter.TESTPLAN, '050', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '050')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_post_single_user_with_post_json(self):
        os.chdir("/root/Downloads/")

        var = {
            "ipv6": "192.168.168.67",
            "name": "user9",
            "domain": "nowhere.com",
            "type": "domain",
            "init-state": "active",
            "groups": ["group1", "group2", "group3"],
            "group-lookup": False,
            "reason": "Just testing"
        }
        with open("test.json", "w") as p:
            json.dump(var, p, indent=4)

        subprocess.run(["bash api-test.sh -f 192.168.168.168 -j -a low -s 1234 post"], shell=True)
        resp = userstatus.show_user_status_inactive()
        Assertion.assert_not_regular(json.dumps(resp), '"error": "Invalid IPv6 address"', "ERR: :Client not created ")

# Func_051
class SSO_REST_API_26(Test):
    uuid = "SOSAIOT-TC-75758"
    description = show_testcase_info(Parameter.TESTPLAN, '051', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '051')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_single_user_with_delete_json_ipv6(self):
        os.chdir("/root/Downloads/")

        userstatus.user_logout_by_inactive_user(ip='fe80::f816:3eff:fe8d:d1dd:12')

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        Assertion.assert_not_regular(json.dumps(resp), '"user_name": "user-ipv6"', "ERR: :Client not created ")

# Func_117
class SSO_REST_API_27(Test):
    uuid = "SOSAIOT-TC-75761"
    description = show_testcase_info(Parameter.TESTPLAN, '117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_single_user_active_and_inactive(self):
        os.chdir("/root/Downloads/")

        userstatus.user_logout_by_inactive_user(ip='192.168.168.125')
        userstatus.user_logout_by_inactive_user(ip='192.168.168.95')
        userstatus.user_logout_by_inactive_user(ip='fe80::f816:3eff:fe8d:d1dd:14')

        userstatus.user_logout_by_active_user(ip='192.168.168.96')
        userstatus.user_logout_by_active_user(ip='192.168.168.98')
        userstatus.user_logout_by_active_user(ip='192.168.168.108')

        resp = userstatus.show_user_status_inactive()
        logger.info(resp)
        r = userstatus.show_user_status()
        logger.info(r)
        Assertion.assert_not_regular(json.dumps(resp), '"user_name": "user2"', "ERR: :Client not created ")
        Assertion.assert_not_regular(json.dumps(r), '"name": "user10"', "ERR: :Client not created ")

# GUI_006
class SSO_REST_API_28(Test):
    uuid = "SOSAIOT-TC-75765"
    description = show_testcase_info(Parameter.TESTPLAN, '006', description=True)['title']
    jira = 'GEN7-38832'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_sso_clinet(self):
        sso_client_add = {
            "host": "192.168.168.201",
            "enable": True,
            "authentication_type": "shared-secret",
            "shared_secret": "1234",
            "security_level": {
                "high": "allow-all"
            },
            "replay_prevention": False,
            "origin_restriction": {},
            "persistent_connections": False
        }
        config_sso = sso_client.edit_sso_third_party_client(**sso_client_add)
        config_sso = sso_client.get_sso_third_party_client()
        Assertion.assert_regular(json.dumps(config_sso), '"high": "allow-all"', "Err:Failed to edit SSO API value")

# GUI_003
class SSO_REST_API_29(Test):
    uuid = "SOSAIOT-TC-75764"
    description = show_testcase_info(Parameter.TESTPLAN, '003', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '003')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_sso_clinet(self):
        config_sso = sso_client.delete_sso_third_party_client('192.168.168.201')
        Assertion.assert_not_regular(json.dumps(config_sso), '"host": "192.168.168.201"', "Err:Failed to delete SSO API value")