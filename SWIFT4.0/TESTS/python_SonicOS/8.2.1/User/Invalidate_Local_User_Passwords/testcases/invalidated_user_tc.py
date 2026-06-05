import re
import sys
import paramiko
from pexpect import pxssh
import time
print(sys.path)
import os
import json
import time
import logging
import unittest
from runner.unittest.suite import UnittestSuite
from networkdevice import Host
from runner.settings import Params, logger
from definition.ui_fw import FWPage

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Invalidate_Local_User_Passwords')

from definition.settings import *

class TC01_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75472"
    description = show_testcase_info(Parameter.TESTPLAN, '3365275', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365275')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'P@ssw0rdds',
            'force_password_change': True,
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_02_add_access_rule(self):
        res = accessrulecli.restore_access_rule()
        time.sleep(20)
        name = "src_1"
        resp = access_rules.get_ipv4_access_rule_given_from_to('LAN', 'WAN')
        rules_list = resp['access_rules']
        for rules in rules_list:
            if rules['ipv4']['name'] != 'Default Access Rule':
                uuid = rules['ipv4']['uuid']
                resp = access_rules.del_ipv4_access_rule_uuid(uuid)
            else:
                uuid = rules['ipv4']['uuid']
                name = rules['ipv4']['name']

        access_rule_option = {
            'name': name,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"any": True},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"group":"Everyone"},
        }
        output = access_rules.edit_ipv4_access_rule_uuid(uuid, **access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_03_add_access_rule(self):
        access_rule_option = {
            'name': 'src2',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

        fw_ui = FWPage("https://192.168.168.168", "test1", 'P@ssw0rdds')

        cmd = fw_ui.login()
        Assertion.assert_equal(cmd[0], True, "ERR: Testcase failed")
        assert cmd[0], "Testcase failed"

class TC02_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75473"
    description = show_testcase_info(Parameter.TESTPLAN, '3365276', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365276')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        fw_ui = FWPage("https://172.17.1.168", "test1", G_PASSWORD_NEW)

        cmd = fw_ui.login_failed()
        Assertion.assert_equal(cmd[0], False, "ERR: Testcase failed")

class TC03_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75474"
    description = show_testcase_info(Parameter.TESTPLAN, '3365277', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365277')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword': G_PASSWORD_NEW,
            'force_password_change': True,
            "member_of": ["Trusted Users","Everyone","SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test"', 'err: Failed to create localuser')

        result, message = switch_pc_and_login('192.168.168.168', '-PC1', ssh_user='test')
        print(message)

class TC04_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75475"
    description = show_testcase_info(Parameter.TESTPLAN, '3365278', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365278')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        resp = user_local.delete_local_user_no_domain('test')
        resp1 = user_local.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test"', 'err: user not deleted')

        user_json = {
            'action': 'add',
            'username': 'test',
            'userpassword':G_PASSWORD_NEW,
            'force_password_change': True,
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test"', 'err: Failed to create localuser')

        result, message = switch_pc_and_login('172.17.1.168', '-PC1', ssh_user='test')
        print(message)
        
        Assertion.assert_equal(result, True, "ERR: Access not denied as expected.")

class TC05_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75476"
    description = show_testcase_info(Parameter.TESTPLAN, '3365279', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365279')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test2',
            'userpassword': G_PASSWORD_NEW,
            'force_password_change': True,
            "member_of": ["Trusted Users","Everyone","SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test2"', 'err: Failed to create localuser')

        result, message = switch_pc_and_login('192.168.168.168', '-PC1', ssh_user='test2')
        print(message)

class TC06_Invalidated_User(Test):
    uuid = "SOSAIOT-TC-75477"
    description = show_testcase_info(Parameter.TESTPLAN, '3365280', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3365280')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        resp = user_local.delete_local_user_no_domain('test2')
        resp1 = user_local.show_local_users()
        Assertion.assert_not_regular(json.dumps(resp1), '"name": "test2"', 'err: user not deleted')

        user_json = {
            'action': 'add',
            'username': 'test2',
            'userpassword': G_PASSWORD_NEW,
            'force_password_change': True,
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test2"', 'err: Failed to create localuser')

        result, message = switch_pc_and_login('172.17.1.168', '-PC1', ssh_user='test2')
        print(message)
        
        Assertion.assert_equal(result, True, "ERR: Access not denied as expected.")

def wait_for_output(channel, timeout=10):
    output = ""
    end_time = time.time() + timeout
    
    while time.time() < end_time:
        if channel.recv_ready():
            output += channel.recv(4096).decode('utf-8')
            print(output, end="")
            if any(keyword in output for keyword in ["password:", "Your password has expired", "Access denied", "Welcome"]):
                break
        else:
            time.sleep(1)
    return output

def switch_pc_and_login(url, openstack_PC, ssh_user="test"):
    hostname = f"{Params.testbed}{openstack_PC}"
    username = "root"
    password = "password"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        logger.info(f"Connecting to OpenStack PC: {hostname}")
        ssh.connect(hostname, username=username, password=password)
        logger.info("Connected to OpenStack PC.")

        channel = ssh.invoke_shell()
        time.sleep(2)

        channel.send(f"ssh {ssh_user}@{url}\n")
        output = wait_for_output(channel)

        if "password:" in output:
            channel.send("password\n")
            output = wait_for_output(channel)

        if "Your password has expired" in output:
            logger.info("Password has expired. Changing password.")
            channel.send("password\n")
            time.sleep(1)
            channel.send("sonicwall\n")
            time.sleep(1)
            channel.send("sonicwall\n")
            output = wait_for_output(channel)

        if "Access denied" in output:
            logger.error("Access denied for user.")
            ssh.close()
            return False, "ERR: Access denied."

        if "Your password has been updated" in output:
            logger.info("Password updated successfully.")

        logger.info("SSH Login completed.")
        ssh.close()
        return True, "SSH Login completed and output displayed."

    except Exception as e:
        logger.error(f"SSH failed to {hostname} with error: {str(e)}")
        return False, str(e)