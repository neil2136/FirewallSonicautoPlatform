from definition.initial_param import *
from lib.utils import *


class Test_ip_helper_01(Test):
    uuid = "SOSAIOT-TC-56342"
    description = show_testcase_info(Parameter.TESTPLAN, "1", description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_case_info('1')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_01_add_user_protocol(self):
        usr_protocol = {
            'name': 'TEST',
            'port1': 959,
            'port2': 277,
            'timeout': 30,
        }
        rc = iphelper.add_protocol(**usr_protocol)
        Assertion.assert_equal(rc, True, "ERR: Add ip helper protocol failed!")


class Test_ip_helper_02(Test):
    uuid = "SOSAIOT-TC-56332"
    description = show_testcase_info(Parameter.TESTPLAN, "2", description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_case_info('2')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_02_01_create_dns_iphelper_policy(self):
        iphelper_dns_opt = {
            'protocol': 'DNS',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dns ip helper policy failed!")

    def test_02_02_create_dhcp_iphelper_policy(self):
        iphelper_dhcp_opt = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp ip helper policy failed!")

    def test_02_03_disable_dhcp_policy(self):
        iphelper_dhcp_opt = {
            'policy': 'DHCP',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp ip helper policy failed!")

    def test_02_04_enable_dhcp_policy(self):
        iphelper_dhcp_opt = {
            'policy': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp ip helper policy failed!")

    def test_02_05_delete_dns_iphelper_policy(self):
        del_json = {
            'protocol': 'DNS',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete DNS ip helper policy failed!")

    def test_02_06_delete_dhcp_iphelper_policy(self):
        del_json = {
            'protocol': 'DHCP',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete dhcp ip helper policy failed!")


class Test_ip_helper_03(Test):
    uuid = "SOSAIOT-TC-56339"
    description = show_testcase_info(Parameter.TESTPLAN, "3", description=True)['title']
    jira = 'GEN7-31901'

    def test_03_00_show_testcase_info(self):
        show_case_info('3')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    #already configure X1 as WAN, add dns iphelper policy
    #steps: disable ip helper
    # 1. enable dns protocol, disable dns ip helper policy -> test traffic (failed)
    # 2. enable dns ip helper policy -> test traffic (failed)
    # 3. enable ip helper and dns policy -> test traffic (pass)
    @repeat_method(5)
    def test_03_01_enable_dns_protocol(self):
        dns_protocol_opt = {
            'protocol': 'DNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**dns_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dns protocol failed!")

    def test_03_02_create_dns_policy(self):
        iphelper_dns_opt = {
            'protocol': 'DNS',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dns ip helper policy failed!")

    def test_03_03_disable_dns_policy(self):
        iphelper_dns_opt = {
            'policy': 'DNS',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp ip helper policy failed!")

    def test_03_04_test_traffic_failed(self):
        pc2_ssh.send_command("tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "Test traffic still success while dns policy disabled!")

    def test_03_05_enable_dns_policy(self):
        iphelper_dns_opt = {
            'policy': 'DNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp ip helper policy failed!")

    def test_03_06_test_traffic_failed(self):
        pc2_ssh.send_command("tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "Test traffic still success while ip helper disabled!")

    def test_03_07_enable_iphelper(self):
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper failed!")

    @repeat_method(5)
    def test_03_08_test_traffic_pass(self):
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")

    def test_03_09_delete_dns_iphelper_policy(self):
        del_json = {
            'protocol': 'DNS',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete DNS ip helper policy failed!")


class Test_ip_helper_04(Test):
    uuid = "SOSAIOT-TC-56349"
    description = show_testcase_info(Parameter.TESTPLAN, "4", description=True)['title']
    jira = 'GEN7-31901'

    def test_04_00_show_testcase_info(self):
        show_case_info('4')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    # 1.disable dhcp server on fw (already done in conf_tb.py)
    # 2.disable dhcp protocol -> test traffic (failed)
    # 3.enable dhcp protocol -> test traffic (pass)
    def test_04_01_disable_dhcp_protocol(self):
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': False
        }
        rc = iphelper.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp protocol failed!")

    def test_04_02_create_dhcp_iphelper_policy(self):
        iphelper_dhcp_opt = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp ip helper policy failed!")

    def test_04_03_restart_dhcp_server_on_PC2(self):
        logger.info("***       Restarting DHCP Server On PC2      ***")
        out = pc2_ssh.send_command('service dhcpd restart')
        pc2_ssh.send_command('exit')
        Assertion.assert_regular(out, r'OK', "ERR: Restart DHCP on PC2 failed!")

    def test_04_04_test_dhcp_traffic_failed(self):
        rc = test_dhcp_traffic()
        kill_dhclient()
        Assertion.assert_equal(rc, False, "ERR: While dhcp protocol disabled, the dhcp traffic could still pass")

    def test_04_05_enable_api(self):
        api_dict = {
            'sonicos-api': True,               ### Bool
            'basic': True,                      ### Bool
            }
        rc = sonicos_api.sonicos_api(**api_dict)
        Assertion.assert_equal(rc, True, "ERR: Enable api failed")

    @repeat_method(5)
    def test_04_06_enable_dhcp_protocol(self):
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp protocol failed!")

    @repeat_method(5)
    def test_04_07_test_dhcp_traffic_pass(self):
        rc = test_dhcp_traffic()
        kill_dhclient()
        Assertion.assert_equal(rc, True, "ERR: Test dhcp traffic failed!")

    def test_04_08_delete_dhcp_iphelper_policy(self):
        del_json = {
            'protocol': 'DHCP',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete dhcp ip helper policy failed!")




