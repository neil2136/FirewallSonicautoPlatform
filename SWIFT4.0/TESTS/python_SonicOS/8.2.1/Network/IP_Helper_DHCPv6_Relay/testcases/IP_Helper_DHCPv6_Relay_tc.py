import sys
import os
import json
from unicodedata import name

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay')

from definition.settings import *


class TC01_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56271"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514130')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_DHCPv6_listed_under_relay_protocol(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc1 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - DHCPv6 is not listed under relay protocol")


class TC02_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56272"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514131')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_DHCPv6_relay_protocol_details(self):
        resp = status_api.show_status()
        model = resp['model']
        if model == 'TZ 80':
            static_client.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc2_tz80 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
            out = static_client.send_command(cmd)
            logger.info("login with user\n" + out)
            words =  out.split()
            res = ''.join(words[-1:])
            Assertion.assert_equal(res, 'True', "ERR: Testcase failed - DHCPv6 relay protocol details are incorrect")
        else:
            static_client.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc2 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
            out = static_client.send_command(cmd)
            logger.info("login with user\n" + out)
            words =  out.split()
            res = ''.join(words[-1:])
            Assertion.assert_equal(res, 'True', "ERR: Testcase failed - DHCPv6 relay protocol details are incorrect")


class TC03_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56273"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514132')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_and_disable_DHCPv6_Relay_Protocol(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc3 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - enable and disable DHCPv6_Relay_Protocol failed")


class TC04_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56274"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_and_disable_ip_helper(self):
        # enabling Ip_helper
        iphelper_obj.enable_iphelper()
        # verifying if ip_helper is enabled
        resp = iphelper_obj.get_iphelper_settings()
        Assertion.assert_equal(resp['ip_helper']['enable'], True, "ERR: Testcase failed - failed to enable ip_helper")

        # enabling Ip_helper
        iphelper_obj.disable_iphelper()
        resp1 = iphelper_obj.get_iphelper_settings()
        Assertion.assert_equal(resp1['ip_helper']['enable'], False, "ERR: Testcase failed - failed to disable ip_helper")


class TC05_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56275"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514134')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_DHCPv6_listed_in_Protocol_dropdown_list(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc5 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - enable and disable DHCPv6_Relay_Protocol failed")


class TC06_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56277"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514136')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc6 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - failed to add DHCPv6 relay policy")


class TC07_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56276"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514135')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_DHCPv6_relay_policy_details(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc7 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Details do not match")


class TC08_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56280"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514139')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc8 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Failed to disable DHCPv6 Relay policy")


class TC09_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56279"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514138')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc9 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Failed to enable DHCPv6 Relay policy")


class TC10_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56278"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514137')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc10 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Failed to delete DHCPv6 Relay policy")


class TC11_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56281"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514140')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc11 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Failed to configure DHCPv6 Relay policy")


class TC12_IP_Helper_DHCPv6_Relay(Test):
    uuid = "SOSAIOT-TC-56282"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514141')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_invalid_input_DHCPv6_relay_policy(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/IP_Helper_DHCPv6_Relay/definition/ui_user.py -method tc12 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words =  out.split()
        res = ''.join(words[-1:])
        Assertion.assert_equal(res, 'True', "ERR: Testcase failed - Invalid value got accepted")