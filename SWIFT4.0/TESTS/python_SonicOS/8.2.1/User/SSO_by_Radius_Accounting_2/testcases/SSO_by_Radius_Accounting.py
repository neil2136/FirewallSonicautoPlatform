import os
import re
import sys
import time

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2/definition')

from settings import *


def del_all_sso_radius_accounting_client():
    rc = user_sso_obj.show_sso_accounting_client()
    if rc["user"]["sso"] != {}:
        for client in rc["user"]["sso"]["radius_accounting_client"]:
            rc = user_sso_obj.del_sso_radius_accounting_client(name=client["host"])
            Assertion.assert_equal(rc, True, "ERR: Deleting SSO RADIUS Accounting clients FAILED")


# Verify Add maximum RADIUS accounting client
class TC01_Verify_Add_Maximum_RADIUS_Accounting_Client_Client_List(Test):
    """Verify Add maximum RADIUS accounting client """
    uuid = "SOSAIOT-TC-75796"
    description = show_testcase_info(TESTPLAN, '1825540', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825540')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_create_max_radius_accounting_client_in_client_list(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
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
        for i in range(4):
            add_sso_radius_accounting_client["user"]["sso"]["radius_accounting_client"][0]["host"] = account_ip + str(i)
            rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
            Assertion.assert_equal(rc, True, f"ERR: Adding {i} SSO RADIUS Accounting clients FAILED")
            time.sleep(2)
        add_sso_radius_accounting_client["user"]["sso"]["radius_accounting_client"][0]["host"] = account_ip
        try:
            rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client)
        except Exception as e:
            logger.info("Adding More than max RADIUS Accounting client FAILED as expected")
        Assertion.assert_equal(rc, False, "ERR: Adding more than max limit SSO RADIUS Accounting clients PASSED")
        time.sleep(2)


# Verify Edit RADIUS accounting client by clicking the configure button
class TC02_Verify_Edit_RADIUS_Accounting_Client_UI(Test):
    """Verify Edit RADIUS accounting client by clicking the configure button"""
    uuid = "SOSAIOT-TC-75797"
    description = show_testcase_info(TESTPLAN, '1825541', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825541')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_radius_acc_client_on_ui(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": new_account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(existing_client=account_ip, radius_acc_client=radius_acc_client)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()

    def test_02_get_sso_radius_accounting_client(self):
        rc = user_sso_obj.show_sso_accounting_client()
        logger.info(rc)
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["host"], new_account_ip,
                               "ERR: Acquiring SSO RADIUS Accounting client changed host FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["user_name_format"]["user_name"], True,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["log_user_out_timeout"], 0,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")
        Assertion.assert_equal(rc["user"]["sso"]["radius_accounting_client"][0]["proxy_forward"]["timeout"] == 10 and
                               rc["user"]["sso"]["radius_accounting_client"][0]["proxy_forward"]["retries"] == 3, True,
                               "ERR: Acquiring SSO RADIUS Accounting clients user name format FAILED")


# Verify Add same RADIUS accounting client
class TC03_Verify_Add_Same_RADIUS_Accounting_Client_UI(Test):
    """Verify Add same RADIUS accounting client """
    uuid = "SOSAIOT-TC-75798"
    description = show_testcase_info(TESTPLAN, '1825543', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825543')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_same_radius_acc_client_on_ui(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client, host_exists=True, save=False)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Duplicate IP/Name of Forwarding Server Check
class TC04_Verify_Duplicate_IP_Name_Forwarding_Server_Check(Test):
    """Verify Duplicate IP/Name of Forwarding Server Check"""
    uuid = "SOSAIOT-TC-75794"
    description = show_testcase_info(TESTPLAN, '1825538', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825538')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_duplicat_ip_name_forwarding_server_check(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        sso_radius_accounting_client_json_4 = copy.deepcopy(sso_radius_accounting_client_json)
        rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_4)
        Assertion.assert_equal(rc, True, f"ERR: Adding SSO RADIUS Accounting clients FAILED")
        time.sleep(2)

        sso_radius_accounting_client_json_4["user"]["sso"]["radius_accounting_client"][0]["server"][0][
            "name"] = "10.10.10.12"
        rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_4)
        Assertion.assert_equal(rc, False,
                               f"ERR: Adding SSO RADIUS Accounting clients with duplicate forwarding IP/Name PASSED which should have FAILED")
        time.sleep(2)


# Verify Port number boundary test with Forwarding Server
class TC05_Verify_Port_No_Boundary_Test_With_Forwarding_Server(Test):
    """Verify Port number boundary test with Forwarding Server"""
    uuid = "SOSAIOT-TC-75791"
    description = show_testcase_info(TESTPLAN, '1825535', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825535')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_port_no_boundary_test_with_fowarding_server(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        ports = [0, 1, 2, 3000, 65535, 65536]
        for port in ports:
            del_all_sso_radius_accounting_client()
            sso_radius_accounting_client_json_5 = copy.deepcopy(sso_radius_accounting_client_json)
            sso_radius_accounting_client_json_5["user"]["sso"]["radius_accounting_client"][0]["server"][0][
                "port"] = port
            rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_5)
            time.sleep(2)
            if port in [0, 65536]:
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with port {port} PASSED")
            else:
                Assertion.assert_equal(rc, True,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with port {port} FAILED")

            time.sleep(2)


# Verify Timeout(seconds) boundary test with Forwarding Server
class TC06_Verify_Timeout_Boundary_Test_With_Forwarding_Server(Test):
    """Verify Timeout(seconds) boundary test with Forwarding Server"""
    uuid = "SOSAIOT-TC-75792"
    description = show_testcase_info(TESTPLAN, '1825536', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825536')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_timeout_boundary_test_with_fowarding_server(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        timeouts = [0, 1, 5000, 99999, 100000]
        for timeout in timeouts:
            del_all_sso_radius_accounting_client()
            sso_radius_accounting_client_json_6 = copy.deepcopy(sso_radius_accounting_client_json)
            sso_radius_accounting_client_json_6["user"]["sso"]["radius_accounting_client"][0][
                "log_user_out_timeout"] = timeout
            rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_6)
            if timeout in [100000]:
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with timeout {timeout} PASSED")
            else:
                Assertion.assert_equal(rc, True,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with timeout {timeout} FAILED")
            time.sleep(2)


# Verify Retries boundary test with Forwarding Server
class TC07_Verify_Retries_Boundary_Test_With_Forwarding_Server(Test):
    """Verify Retries boundary test with Forwarding Server"""
    uuid = "SOSAIOT-TC-75793"
    description = show_testcase_info(TESTPLAN, '1825537', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825537')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_retries_boundary_test_with_fowarding_server(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        retries = [0, 1, 5000, 65535, 65536]
        for retry in retries:
            del_all_sso_radius_accounting_client()
            sso_radius_accounting_client_json_7 = copy.deepcopy(sso_radius_accounting_client_json)
            sso_radius_accounting_client_json_7["user"]["sso"]["radius_accounting_client"][0][
                "proxy_forward"]["retries"] = retry
            rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_7)
            if retry in [0, 65536]:
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with retries {retry} PASSED")
            else:
                Assertion.assert_equal(rc, True,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with retries {retry} FAILED")
            time.sleep(2)


# Verify Interim Updt timeout boundary test with RADIUS Accounting Client
class TC08_Verify_Interim_Update_Boundary_Test_With_RADIUS_Accounting_Client(Test):
    """Verify Interim Updt timeout boundary test with RADIUS Accounting Client"""
    uuid = "SOSAIOT-TC-75789"
    description = show_testcase_info(TESTPLAN, '1825528', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825528')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_interim_update_boundary_test_with_radius_acc_client(self):
        timeouts = [0, 1, 5000, 65536, 99999, 100000]
        for timeout in timeouts:
            del_all_sso_radius_accounting_client()
            sso_radius_accounting_client_json_8 = copy.deepcopy(sso_radius_accounting_client_json)
            sso_radius_accounting_client_json_8["user"]["sso"]["radius_accounting_client"][0][
                "log_user_out_if_no_interim"] = {"enable": True}
            sso_radius_accounting_client_json_8["user"]["sso"]["radius_accounting_client"][0][
                "log_user_out_timeout"] = timeout
            rc = user_sso_obj.add_sso_radius_accounting_client(**sso_radius_accounting_client_json_8)
            if timeout in [100000]:
                Assertion.assert_equal(rc, False,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with interim update timeout {timeout} PASSED")
            else:
                Assertion.assert_equal(rc, True,
                                       f"ERR: Adding SSO RADIUS Accounting clients forwarding server ip with interim update timeout {timeout} FAILED")

            time.sleep(2)


# Verify Add RADIUS accounting client with 'Default'/specified partition
class TC09_Verify_Add_RADIUS_Accounting_Client_With_Default_Partition(Test):
    """Verify Add RADIUS accounting client with 'Default'/specified partition"""
    uuid = "SOSAIOT-TC-75785"
    description = show_testcase_info(TESTPLAN, '1515905', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1515905')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_radius_acc_client_on_ui_with_partition(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()
        rc = status_api.show_status()
        print("=============Enabling Auth-Partition===============================")
        user_auth_partition.enable_disable_auth_partition(True)
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            # "clientHost": account_ip,
            "clientHost": Hostname,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        if "TZ" not in rc["model"]:
            resp = user_sso_obj.show_sso_accounting_client()
            print(resp)
            # Assertion.assert_equal("Default" in resp, True,
            #                        "ERR: Could not found Partition details on RADIUS Accounting Client")
            partition = resp["user"]["sso"]["radius_accounting_client"][0].get("partition")
            Assertion.assert_equal(
                partition,
                "Default",
                "ERR: Partition is not set to Default on RADIUS Accounting Client"
            )
        time.sleep(20)

        # # Logout of UTM UI
        # fw_ui_obj.logout_ui()


# Verify Client Name Maxium length Check
class TC10_Verify_Client_Name_Max_Len_Check(Test):
    """Verify Client Name Maxium length Check"""
    uuid = "SOSAIOT-TC-75786"
    description = show_testcase_info(TESTPLAN, '1825524', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825524')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_radius_acc_client_with_max_len_client_name(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()

        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            "clientHost": "a" * 63 + ".com",
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Client Name exceed Maximum length Check
class TC11_Verify_Client_Name_Exceed_Max_Len_Check(Test):
    """Verify Client Name exceed Maximum length Check"""
    uuid = "SOSAIOT-TC-75787"
    description = show_testcase_info(TESTPLAN, '1825525', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825525')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_radius_acc_client_with_max_len_exceed_client_name(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()

        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            "clientHost": "a" * 64 + ".com",
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client, invalid_ip=True, save=False)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Illegal character check for Client name
class TC12_Verify_Illegal_Chars_Check_Client_Name(Test):
    """Verify Illegal character check for Client name"""
    uuid = "SOSAIOT-TC-75788"
    description = show_testcase_info(TESTPLAN, '1825527', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825527')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(2)
    def test_01_add_radius_acc_client_with_illegal_chars_client_name(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()

        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()
        for illegal_chars_name in ["bad_host$name.com", "-startwithhyphen.com"]:
            # Navigating to Device > Users > Settings
            fw_ui_obj.navigate_to_users_settings_section()

            # Click on Configure SSO edit RADIUS Accounting Client
            radius_acc_client = {
                "clientHost": illegal_chars_name,
                "agentKey": "password",
                "confirmKey": "password"
            }
            fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client, invalid_ip=True, save=False)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Javascript/SQL injection with all text field
class TC13_Verify_Js_SQL_Inj_With_All_Fields(Test):
    """Verify Javascript/SQL injection with all text field"""
    uuid = "SOSAIOT-TC-75795"
    description = show_testcase_info(TESTPLAN, '1825539', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825539')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_js_sql_inj_with_all_fields(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()

        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()
        for js_sql_inj in ["' OR '1'='1", "<script>alert('XSS')</script>", "'; DROP TABLE users; --",
                           "<img src=x onerror=alert('XSS')>", "javascript:alert('XSS')"]:
            # Navigating to Device > Users > Settings
            fw_ui_obj.navigate_to_users_settings_section()

            # Click on Configure SSO edit RADIUS Accounting Client
            radius_acc_client = {
                "clientHost": js_sql_inj,
                "agentKey": "password",
                "confirmKey": "password"
            }
            fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client, invalid_ip=True, save=False)

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Show partition option
class TC14_Verify_Show_Partition_Option(Test):
    """Verify Show partition option"""
    uuid = "SOSAIOT-TC-75790"
    description = show_testcase_info(TESTPLAN, '1825529', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1825529')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_radius_acc_client_with_max_len_client_name(self):
        # Delete all SSO RADIUS Accounting Client
        del_all_sso_radius_accounting_client()

        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigating to Device > Users > Settings
        fw_ui_obj.navigate_to_users_settings_section()

        # Click on Configure SSO edit RADIUS Accounting Client
        radius_acc_client = {
            "clientHost": account_ip,
            "agentKey": "password",
            "confirmKey": "password"
        }
        fw_ui_obj.config_radius_acc_client(radius_acc_client=radius_acc_client)

        # Assert for Partition Option
        Assertion.assert_equal(fw_ui_obj.does_page_have_text("Paritition"), False,
                               "ERR: Partition option is found in SSO-RADIUS Accounting Client")

        # Logout of UTM UI
        fw_ui_obj.logout_ui()
