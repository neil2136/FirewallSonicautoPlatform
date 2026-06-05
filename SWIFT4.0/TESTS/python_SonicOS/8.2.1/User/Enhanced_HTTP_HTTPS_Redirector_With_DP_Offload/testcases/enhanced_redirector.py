__author__ = "Pachiyappan Velan"

import copy
import json
import sys
import os

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition')

from settings import *


class TC00_TestNonTC_Config(Test):
    uuid = "TestNonTC"

    def test_00_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'sudo ip route add default via {Parameter.FIREWALL}',
                f'sudo ip route add 192.168.168.0/24 via {Parameter.FIREWALL}',
                'route']
        output = PC1_login.send_commands(cmds)
        res[
            'pc1'] = True if f'default via {Parameter.FIREWALL}' in output and f'192.168.168.0/24 via {Parameter.FIREWALL}' in output else False
        time.sleep(10)
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")

    def test_01_add_access_rule(self):
        access_rule_option = {
            'name': 'DNS LAN to WAN',
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'service': {"group": "DNS (Name Service)"},
            'source_addr': {"any": True},
            'dst_addr': {"any": True},
            'user_included': {"all": True},
        }
        output = access_rules_ipv4.add_ipv4_access_rule(**access_rule_option)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_02_edit_default_lan_to_wan_acl_user(self):
        res = False
        getres = access_rules.get_accessrule_via_zones(srczone='LAN', dstzone='WAN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                    logger.info(f'get target rule successful: {rule}')
                    acl_dict = copy.deepcopy(default_acl_dict)
                    acl_dict.update({"users": {
                        "included": {"group": 'Everyone'},
                        "excluded": {"none": True}
                    }})
                    res = access_rules.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                    break
        except exception as e:
            logger.info(f'get lan to wan acl failed: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: edit default lan to wan access rule to everyone user failed...")

    def test_03_add_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'dpuser',
            'userpassword': 'password',
            'member_of': ['Trusted Users', 'Everyone', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "days",
            "accountlifetime": 1,
            "prune_on_expiry": False
        }
        rc = user_local.local_user(**user_json)
        Assertion.assert_equal(rc, True, "ERR: add_local_user failed")


# GUI check for Verifying the default setting of the three options added for this feature in diag page
class TC01_Verify_Default_Setting_Of_Three_Options_In_Diag_Page(Test):
    """GUI check for Verifying the default setting of the three options added for this feature in diag page"""
    uuid = "SOSAIOT-TC-75361"
    description = show_testcase_info(Parameter.TESTPLAN, '1510621', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510621')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_default_setting_of_three_options_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Check for default setting of the three options added for this feature in diag page
        fw_ui_obj.verify_default_setting_for_dp_offload_available()

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# GUI check for Verifying the HTTP port number and it can be changed to other correct values in diag page
class TC02_Verify_HTTP_Port_Number_and_Changeable_In_Diag_Page(Test):
    """GUI check for Verifying the HTTP port number and it can be changed to other correct values in diag page"""
    uuid = "SOSAIOT-TC-75361"
    description = show_testcase_info(Parameter.TESTPLAN, '1510621', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510621')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_http_port_number_and_changable_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Check for HTTP port number and it can be changed to other correct values in diag page
        fw_ui_obj.verify_http_port_number_and_changable()

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# GUI check for Verify redirect HTTP traffic after disable offload to dp on diag page
class TC03_Verify_Redirect_HTTP_After_Disable_DP_Offload_Diag_Page(Test):
    """GUI check for Verify redirect HTTP traffic after disable offload to dp on diag page"""
    uuid = "SOSAIOT-TC-75361"
    description = show_testcase_info(Parameter.TESTPLAN, '1510621', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510621')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_http_port_number_and_changable_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Verify redirect HTTP traffic after disable offload to dp on diag page
        fw_ui_obj.verify_redirect_http_traffic_after_disable_dp_offload()

        # Logout of UTM UI
        fw_ui_obj.logout_ui()

    @repeat_method(3)
    def test_03_verify_redirect_http_works_fine(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Verify Redirect HTTP works fine
        fw_ui_obj.verify_redirect(url="http://google.com")



# GUI check for Verify redirect HTTPS traffic after disable offload to dp on diag page
class TC04_Verify_Redirect_HTTPS_After_Disable_DP_Offload_Diag_Page(Test):
    """GUI check for Verify redirect HTTPS traffic after disable offload to dp on diag page"""
    uuid = "SOSAIOT-TC-75364"
    description = show_testcase_info(Parameter.TESTPLAN, '1510624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_https_port_number_and_changable_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Verify redirect HTTP traffic after disable offload to dp on diag page
        fw_ui_obj.verify_redirect_http_traffic_after_disable_dp_offload()

        # Logout of UTM UI
        fw_ui_obj.logout_ui()

    @repeat_method(3)
    def test_03_verify_redirect_https_works_fine(self):
        # Verify Redirect HTTP works fine
        fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = 'https://12.12.1.40'
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        out = PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


# Verify Flush cached files for one interface on diag page
class TC05_Verify_Flush_Cached_Files_For_One_Interface_Diag_Page(Test):
    """Verify Flush cached files for one interface on diag page"""
    uuid = "SOSAIOT-TC-75365"
    description = show_testcase_info(Parameter.TESTPLAN, '1510625', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510625')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_verify_flush_cached_files_for_one_interface_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Verify Flush cached files for one interface on diag page
        fw_ui_obj.verify_flush_cached_files(interface="one")

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Flush cached files for all interface on diag page
class TC06_Verify_Flush_Cached_Files_For_All_Interface_Diag_Page(Test):
    """Verify Flush cached files for all interface on diag page"""
    uuid = "SOSAIOT-TC-75366"
    description = show_testcase_info(Parameter.TESTPLAN, '1510626', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510626')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_flush_cached_files_for_all_interface_in_diag_page(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Verify Flush cached files for all interface on diag page
        fw_ui_obj.verify_flush_cached_files(interface="all")

        # Logout of UTM UI
        fw_ui_obj.logout_ui()


# Verify Error returned for Change other ports to 10281
class TC07_Verify_Error_Returned_For_Changing_Other_Ports_To_10281(Test):
    """Verify Error returned for Change other ports to 10281"""
    uuid = "SOSAIOT-TC-75381"
    description = show_testcase_info(Parameter.TESTPLAN, '1510628', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510628')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_internal_tcp_port_is_10281(self):
        # Defining firewall UI obj
        fw_ui_obj = ui_obj

        # Login to UTM UI
        fw_ui_obj.login_ui()

        # Navigate to diag Internal setting page
        fw_ui_obj.navigate_to_diag_internal_settings_page()

        # Check for internal tcp port value is 10281 in diag page
        fw_ui_obj.verify_internal_tcp_port_in_diag_page()

        # Logout of UTM UI
        fw_ui_obj.logout_ui()

    def test_02_verify_error_returned_for_changing_other_ports_to_10281(self):
        admin_dict = {
            "http_port": 10281,
            "https_port": 443
        }
        rc = admin_obj.conf_admin(**admin_dict)
        Assertion.assert_equal(rc, False, "ERR: HTTP Port has changed to 10281 which is internal tcp port")
        admin_dict = {
            "http_port": 80,
            "https_port": 10281
        }
        rc = admin_obj.conf_admin(**admin_dict)
        Assertion.assert_equal(rc, False, "ERR: HTTPS Port has changed to 10281 which is internal tcp port")
        admin_dict = {
            "ssh": {"port": 10281}
        }
        rc = admin_obj.conf_admin(**admin_dict)
        Assertion.assert_equal(rc, True, "ERR: SSH Port has not changed to 10281 which is internal tcp port")
        ssl_vpn_server = {
            'port': 10281,
        }
        rc = sslvpn_server_api.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(rc, False, "Err: SSLVPN Port has changed to 10281 which is internal tcp port")


# Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website
class TC08_Verify_HTTP_Login_Allowed_And_HTTP_Redirect_With_No_SSO_Involved(Test):
    """Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website"""
    uuid = "SOSAIOT-TC-75364"
    description = show_testcase_info(Parameter.TESTPLAN, '1510624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_ula_function(self):
        fwconfigure.logout_users()
        PC4_login.send_command('pkill firefox')
        time.sleep(10)
        url = 'http://12.12.1.40'
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        PC4_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")


# Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website
class TC09_Verify_HTTP_Login_Allowed_And_HTTPS_Redirect_With_No_SSO_Involved(Test):
    """Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website"""
    uuid = "SOSAIOT-TC-75364"
    description = show_testcase_info(Parameter.TESTPLAN, '1510624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_ula_function(self):
        fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
            url = 'https://12.12.1.40'
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

# Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website
class TC10_Verify_HTTP_Login_Allowed_And_HTTP_Redirect_With_No_SSO_Involved(Test):
    """Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website"""
    uuid = "SOSAIOT-TC-75364"
    description = show_testcase_info(Parameter.TESTPLAN, '1510624', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_ula_function(self):
        fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = 'http://12.12.1.40'
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

    def test_03_check_tsr(self):
        logger.info(" Check TSR ".center(40, '-'))
        kwd = 'User Login Settings'
        reline = 'Syslog Per Server Settings' + '(.*?)' + 'Syslog Field Settings'
        server = syslog_opt['name']

        rc = syslog_lib.check_tsr(kwd,reline,server)
        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')

# Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website
class TC11_Verify_HTTP_Login_Allowed_And_HTTPS_Redirect_With_No_SSO_Involved(Test):
    """Verify redirect to policy login redirect page and after login succeeds user get redirected to the correct website"""
    uuid = "SOSAIOT-TC-75364"
    description = show_testcase_info(Parameter.TESTPLAN, '1510624', description=True)['title']

    def test_00_show_testcase_info(self):
        show+estcase_info(Parameter.TESTPLAN, '1510624')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_ula_function(self):
        fwconfigure.logout_users()
        PC2_login.send_command('pkill firefox')
        time.sleep(10)
        url = 'https://12.12.1.40'
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/User/Enhanced_HTTP_HTTPS_Redirector_With_DP_Offload/definition/ui_user.py ' + '-url ' + f'{url}' + ' -user auto_ula_test -pwd password'
        PC2_login.send_command(cmd)
        resp = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(resp), 'auto_ula_test', "err:Failed to logout")

    def test_03_check_tsr(self):
        logger.info(" Check TSR ".center(40, '-'))
        kwd = 'Server Name'
        reline = 'Syslog Per Server Settings' + '(.*?)' + 'Syslog Field Settings'
        server = syslog_opt['name']

        rc = syslog_lib.check_tsr(kwd,reline,server)
        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')