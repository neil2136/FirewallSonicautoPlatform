from definition.settings import *
from definition.utils import *


# IPHelper policy can be created using an interface and make sure the function work
class Test_Config_TC07(Test):
    uuid = "SOSAIOT-TC-56269"
    goto_teardown = True
    description = show_testcase_info(TESTPLAN, "07", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "07")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_make_sure_x2_client_can_not_get_ip_from_dhcp_server(self):
        logger.info("Check whether x2 client can get ip from firewall's dhcpv4 server... ")
        pc_login = PC2_login
        logger.info("PC2 should not get IP... ")
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: X2 still could get ip from firewall default dhcp server , please double check DHCPv4 server option")

    def test_02_add_ip_helper_dhcp_policy_from_x2_to_x3_server(self):
        logger.info("Add dhcp iphelper from X2 to X3 DHCP server... ")
        iphelper_dhcp_json = {
            'protocol': 'DHCP',
            'src': 'X2',
            'dsn': '192.168.3.30'
        }
        rc = iphelper_obj.add_iphelper_policy(**iphelper_dhcp_json)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp iphelper from X2 to X3 DHCP server failed!")

    def test_03_x2_client_can_get_ip_from_server_on_x3(self):
        logger.info("Check whether x2 client can get ip(IP range: 192.168.2.200-205)... ")
        pc_login = PC2_login
        logger.info("PC2 could get IP... ")
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: Failed to obtain IP from the server, please check the configurations")

# The test will verify that IP Helper Policy can be enabled and disabled without issue.
class Test_Config_TC10(Test):
    uuid = "SOSAIOT-TC-56266"
    description = show_testcase_info(TESTPLAN, "10", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "07")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_disable_the_dhcp_ip_helper_policy(self):
        logger.info("Disable ip helper dhcp policy... ")
        iphelper_dhcp_opt = {
            'policy': 'DHCP',
            'enable': False,
             'src': 'X2',
             'dst': '192.168.3.30'
        }
        rc = iphelper_obj.change_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable ip helper dhcp policy failed!")

    def test_02_verify_client_can_not_obtain_ip(self):
        logger.info("Check whether x2 client can get ip... ")
        pc_login = PC2_login
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: X2 still could get ip from dhcp server on x3 , please check IP Helper Policy status")

    def test_03_enable_the_dhcp_ip_helper_policy(self):
        logger.info("Enable ip helper dhcp policy... ")
        iphelper_dhcp_opt = {
            'policy': 'DHCP',
            'enable': True,
             'src': 'X2',
             'dst': '192.168.3.30'
        }
        rc = iphelper_obj.change_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper dhcp policy failed!")

    def test_04_verify_client_can_obtain_ip(self):
        logger.info("check whether x2 client can get ip... ")
        pc_login = PC2_login
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: X2 could not get ip from dhcp server on x3, please check the IP helper status!")

# The test will verify that the IP Help Policy can be deleted and functionality is removed by doing so.
class Test_Config_TC09(Test):
    uuid = "SOSAIOT-TC-56270"
    description = show_testcase_info(TESTPLAN, "09", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "07")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_delete_the_dhcp_ip_helper_policy(self):
        logger.info("delete ip helper dhcp policy... ")
        del_iphelper_policy = {
            'protocol': 'DHCP',
            'source': 'X2',
        }
        rc = iphelper_obj.delete_iphelper_policy(**del_iphelper_policy)
        Assertion.assert_equal(rc, True, "ERR: delete ip helper dhcp policy failed!")

    def test_02_verify_client_can_not_obtain_ip(self):
        logger.info("check whether x2 client can get ip... ")
        pc_login = PC2_login
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: x2 still could get ip from dhcp server on x3")

    def test_03_add_ip_helper_dhcp_policy_from_x2_to_x3_server(self):
        logger.info("add ip helper dhcp policy... ")
        iphelper_dhcp_json = {
            'protocol': 'DHCP',
            'src': 'X2',
            'dsn': '192.168.3.30'
        }
        rc = iphelper_obj.add_iphelper_policy(**iphelper_dhcp_json)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp iphelper from X2 to X3 DHCP server failed!")

    def test_04_x2_client_can_get_ip_from_server_on_x3(self):
        logger.info("check whether x2 client can get ip... ")
        pc_login = PC2_login
        output = check_ip_in_pc_eth1(pc_login)
        Assertion.assert_equal(output, True, "ERR: x2 could not get ip from dhcp server on x3")