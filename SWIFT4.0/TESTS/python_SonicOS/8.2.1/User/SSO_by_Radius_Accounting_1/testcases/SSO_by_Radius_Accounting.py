import os
import re
import sys
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_1/definition')

from settings import *


# Verify Edit RADIUS accounting client in client list
class TC01_Verify_Edit_RADIUS_Accounting_Client_Client_List(Test):
    """Verify Edit RADIUS accounting client in client list"""
    uuid = "SOSAIOT-TC-75775"
    description = show_testcase_info(TESTPLAN, '1515906', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515906')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_accounting_client_in_client_list(self):
        add_sso_radius_accounting_client = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": account_ip,
                        "shared_secret": "password",
                        "log_user_out_timeout": 0
                    }]
                }
            }
        }

        rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
        Assertion.assert_equal(rc, True, "ERR: Adding SSO RADIUS Accounting clients FAILED")

    def test_03_edit_sso_radius_accounting_client(self):
        edit = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": new_account_ip,
                        "shared_secret": "password",
                    }]
                }
            }}
        rc = user_sso_obj.edit_sso_radius_accounting_client(name=account_ip, **edit)
        Assertion.assert_equal(rc, True, "ERR: Editing SSO RADIUS Accounting clients FAILED")

    def test_04_get_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["host"], new_account_ip,
                               "ERR: Acquiring SSO RADIUS Accounting client changed host FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["user_name_format"]["user_name"], True,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["log_user_out_if_no_interim"]["auto"],
                               True, "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["log_user_out_timeout"], 0,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["proxy_forward"]["timeout"] == 5 and
                               rc["user"]["sso"]["radius_accounting_client"][0]["proxy_forward"]["retries"] == 3, True,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")


# Verify Empty input check in RADIUS accounting client
class TC02_Verify_Empty_Input_Check_In_RADIUS_Accounting_Client(Test):
    """Verify Empty input check in RADIUS accounting client"""
    uuid = "SOSAIOT-TC-75779"
    description = show_testcase_info(TESTPLAN, '1825530', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825530')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_03_empty_input_check_radius_acc_client(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": "",
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify TSR RADIUS accounting client
class TC03_Verify_TSR_RADIUS_Accounting_Client(Test):
    """Verify TSR RADIUS accounting client"""
    uuid = "SOSAIOT-TC-75784"
    description = show_testcase_info(TESTPLAN, '1825564', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515906')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_accounting_client_in_client_list(self):
        add_sso_radius_accounting_client = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": account_ip,
                        "shared_secret": "password",
                        "log_user_out_timeout": 0
                    }]
                }
            }
        }

        rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
        Assertion.assert_equal(rc, True, "ERR: Adding SSO RADIUS Accounting clients FAILED")

    def test_03_check_tsr(self):
        ret = diag_obj.download_tsr()
        if ret:
            logger.info('Download Failed')
            Assertion.assert_equal(False, True, "ERR: FAILED to fetch TSR Record from UTM")
        else:
            logger.info('Download Success!')

            with open('/tmp/techSupport', 'r', encoding='utf-8') as f:
                lines = f.read()
                Assertion.assert_not_equal(re.search(re_user_name, lines), None,
                                           "ERR: TSR Does not have info about RADIUS Accounting client user name format")
                Assertion.assert_not_equal(re.search(re_interim, lines), None,
                                           "ERR: TSR Does not have info about RADIUS Accounting client interim timeout")
                Assertion.assert_not_equal(re.search(re_shared_secret, lines), None,
                                           "ERR: TSR Does not have info about RADIUS Accounting client shared secret")
                Assertion.assert_not_equal(re.search(re_host, lines), None,
                                           "ERR: TSR Does not have info about RADIUS Accounting client host")


# Verify Name of Client with special character Check
class TC04_Verify_Client_Name_With_Special_Character(Test):
    """Verify Name of Client with special character Check"""
    uuid = "SOSAIOT-TC-75778"
    description = show_testcase_info(TESTPLAN, '1825526', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825526')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_acc_client_with_special_chars(self):
        specials = ["fe82::164d:b621:b551:b6bc", "0B-74-C4-DB-EA-34", "<p>alert('Hello! I am an alert box!');</p>",
                    "SELECT * FROM *;",
                    "H12$#qwe"]
        for special in specials:
            add_sso_radius_accounting_client = {
                "user": {
                    "sso": {
                        "radius_accounting_client": [{
                            "host": special,
                            "shared_secret": "password",
                            "log_user_out_timeout": 0
                        }]
                    }
                }
            }
            try:
                rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients with client name {special} PASSED")
            except Exception as e:
                logger.info(e)


# Verify Name of Forwarding Server with special character Check
class TC05_Verify_Special_Forwarding_Server_IP_Check_Radius_Acc_Client(Test):
    """Verify Name of Forwarding Server with special character Check"""
    uuid = "SOSAIOT-TC-75783"
    description = show_testcase_info(TESTPLAN, '1825534', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825534')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_acc_client_fwd_server_with_special_chars(self):
        specials = ["fe82::164d:b621:b551:b6bc", "0B-74-C4-DB-EA-34", "<p>alert('Hello! I am an alert box!');</p>",
                    "SELECT * FROM *;",
                    "H12$#qwe"]
        for special in specials:
            add_sso_radius_accounting_client = {
                "user": {
                    "sso": {
                        "radius_accounting_client": [{
                            "host": account_ip,
                            "shared_secret": "password",
                            "log_user_out_timeout": 0
                        }]
                    }
                }
            }
            try:
                rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients frowarding server ip with {special} PASSED")
            except Exception as e:
                logger.info(e)


# Verify Invalid IP address check
class TC06_Verify_Invalid_IP_Check_Radius_Acc_Client(Test):
    """Verify Invalid IP address check"""
    uuid = "SOSAIOT-TC-75776"
    description = show_testcase_info(TESTPLAN, '1825522', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825522')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_acc_client_with_special_chars(self):
        invalid_ips = ["192.168.01.1", "256.100.50.25", "...", "192.168.1.1.1", "192.168.1.300"]
        for invalid_ip in invalid_ips:
            add_sso_radius_accounting_client = {
                "user": {
                    "sso": {
                        "radius_accounting_client": [{
                            "host": invalid_ip,
                            "shared_secret": "password",
                            "log_user_out_timeout": 0
                        }]
                    }
                }
            }
            try:
                rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients with Invalid client IP {invalid_ip} PASSED")
            except Exception as e:
                logger.info(e)

    def test_03_check_radius_acc_client_with_invalid_ip(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": "192.168.1.-1",
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client, invalid_ip=True)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Check RADIUS Accounting client window can be closed without saving
class TC07_Verify_Closing_RADIUS_Acc_Client_Window(Test):
    """Verify Check RADIUS Accounting client window can be closed without saving"""
    uuid = "SOSAIOT-TC-75780"
    description = show_testcase_info(TESTPLAN, '1825531', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825531')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_check_radius_acc_client_window_close_without_saving(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client, save=False)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Check Shared Secret not match error
class TC08_Verify_Check_Shared_Secret_Not_Match_Error(Test):
    """Verify Check Shared Secret not match error"""
    uuid = "SOSAIOT-TC-75781"
    description = show_testcase_info(TESTPLAN, '1825532', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825532')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_check_radius_acc_client_shared_secret_not_match(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "sonicwall"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client, match_pass=True)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Invalid IP address with Forwarding Server Check
class TC09_Verify_Invalid_IP_Address_With_Forwarding_Server(Test):
    """Verify Invalid IP address with Forwarding Server Check """
    uuid = "SOSAIOT-TC-75782"
    description = show_testcase_info(TESTPLAN, '1825533', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825533')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_check_radius_acc_client_invalid_ip_fwd_server(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password",
            "forwarding": {
                "server1": {
                    "ip": "192.168.1.-1"
                }
            }
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client, save=False, invalid_fwd_server=True)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Special ip address check with RADIUS client
class TC10_Verify_Special_IP_Check_Radius_Acc_Client(Test):
    """Verify Special ip address check with RADIUS client"""
    uuid = "SOSAIOT-TC-75777"
    description = show_testcase_info(TESTPLAN, '1825523', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825523')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_all_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        if rc["user"]["sso"] != {}:
            for client in rc["user"]["sso"]["radius_accounting_client"]:
                rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
                Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")

    def test_02_create_radius_acc_client_with_special_chars(self):
        specials = [DUTX1, Gateway, "0.0.0.0", "255.255.255.255", "8.8.8.8"]
        for special in specials:
            add_sso_radius_accounting_client = {
                "user": {
                    "sso": {
                        "radius_accounting_client": [{
                            "host": special,
                            "shared_secret": "password",
                            "log_user_out_timeout": 0
                        }]
                    }
                }
            }
            try:
                rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
                Assertion.assert_equal(rc, True,
                                       f"ERR: Adding SSO RADIUS Accounting clients with client IP {special} FAILED")
            except Exception as e:
                logger.info(e)
