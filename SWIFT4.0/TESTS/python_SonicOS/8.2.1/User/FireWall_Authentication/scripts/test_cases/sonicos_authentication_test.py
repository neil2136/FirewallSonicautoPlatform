from pytest_resources.common_require import *
from inputs.constants import *
from inputs.request_urls import *
from libs.fw_configuration import FWConfiguration
from libs.common_lib import CommonLib
from libs.sslvpn_portal import SSLVPNPortal
from libs.netextender_client import SSLVPNNetExtenderCLI
from libs.global_vpn_client import GlobalVPNClient
from libs.l2tp_vpn_client import L2TPVPNClient
from libs.access_rule import AccessRule
from libs.fw_login import FWLogin
from libs.mail import MailModule


# Non-Testcase to configure various settings required across different test scenarios
class test_NonTC_configure(Test2):
    uuid = 'NonTC'

    def runTest(self):
        # Set "HTTP Basic Access authentication" which enables to use API to configure the FireWall.
        url = fw_url + "/sonicui/7/m/mgmt/system/administrator"
        fw_obj = FWLogin(url=url, username=fw_username, password=fw_password)
        fw_obj.fw_enable_http_basic_access_authentication()
        # Login to FireWall API
        api_obj = FWConfiguration()
        api_obj.api_login()
        # Enable required services for X0 and X1 interfaces
        api_obj.configure_interface_services(interface='X0')
        api_obj.configure_interface_services(interface='X1')
        # Enable Multiple Admin roles required for FireWall Administration
        input_json = {
            "administration": {
                "multiple_admin": True
            }
        }
        response = api_obj.api_put(request_url=admin_config_url, data=json.dumps(input_json))
        logger.info(response)
        # Enable Members to go straight to the management UI on web login for all Administrator Groups
        for group in fw_administrator_groups:
            input_json = {
                "user": {
                    "local": {
                        "group": [
                            {
                                "name": group,
                                "to_management_on_login": True
                            }
                        ]
                    }
                }
            }
            response = api_obj.api_put(request_url=local_groups_url, data=json.dumps(input_json))
            logger.info(response)
        # Configure Auth Server
        for server in authentication_methods:
            api_obj.configure_auth_server(auth=server)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Configuring NTP Server required for TOTP
        api_obj.enable_ntp_service()
        # Configure Mail Server Settings
        api_obj.config_mail_server()
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Configuring different IPv4 and FQDN Address objects required for ULA verification
        # 1. Configure  Address object for Mail Server
        mail_server_object = {
            "address_objects": [
                {
                    "ipv4": {
                        "name": "Mail_Server",
                        "zone": "WAN",
                        "host": {
                            "ip": smtp_server_ip
                        }
                    }
                }
            ]
        }
        api_obj.add_ipv4_address_object(**mail_server_object)
        # 2. Configure  Address object for Python modules
        python_module_object = {
            "address_objects": [
                {
                    "fqdn": {
                        "name": "Python_Modules",
                        "zone": "WAN",
                        "domain": "github.io"
                    }
                }
            ]
        }
        api_obj.add_fqdn_address_object(**python_module_object)
        # 3. Configure Address object for Selenium Webdrivers
        selenium_webdriver_object = {
            "address_objects": [
                {
                    "fqdn": {
                        "name": "Selenium_Webdrivers",
                        "zone": "WAN",
                        "domain": "storage.googleapis.com"
                    }
                }
            ]
        }
        api_obj.add_fqdn_address_object(**selenium_webdriver_object)
        # 4 . Configure Address object for IP Pool Range
        ip_pool_range_object = {
            "address_objects": [
                {
                    "ipv4": {
                        "name": "IPV4 Range",
                        "zone": "SSLVPN",
                        "range": {
                            "begin": ip_pool_start,
                            "end": ip_pool_end
                        }
                    }
                }
            ]
        }
        api_obj.add_ipv4_address_object(**ip_pool_range_object)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Add access rule from LAN to WAN allowing DNS Service
        rule = {
            "name": "Test_Rule_DNS",
            "from": "LAN",
            "to": "WAN",
            "service": "DNS (Name Service)"
        }
        api_obj.add_ipv4_access_rule(**rule)
        # Add access rule from LAN to WAN allowing github resources for scripts
        rule = {
            "name": "Test_Rule_Python_Modules",
            "from": "LAN",
            "to": "WAN",
            "dst_addr": {
                "address": {
                    "name": "Python_Modules"
                }
            }
        }
        api_obj.add_ipv4_access_rule(**rule)
        # Add access rule from LAN to WAN allowing github resources for scripts
        rule = {
            "name": "Test_Rule_Selenium_Webdrivers",
            "from": "LAN",
            "to": "WAN",
            "dst_addr": {
                "address": {
                    "name": "Selenium_Webdrivers"
                }
            }
        }
        api_obj.add_ipv4_access_rule(**rule)
        # Add access rule from LAN to WAN allowing github resources for scripts
        rule = {
            "name": "Test_Rule_Mail_Server",
            "from": "LAN",
            "to": "WAN",
            "dst_addr": {
                "address": {
                    "name": "Mail_Server"
                }
            }
        }
        api_obj.add_ipv4_access_rule(**rule)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Configure SSL-VPN Server Settings
        api_obj.configure_ssl_vpn_server_base()
        ssl_vpn_json = {
            "WAN_enable": True
        }
        api_obj.configure_ssl_vpn_server_access(**ssl_vpn_json)
        # Configuring SSL-VPN Default device Profile
        ssl_vpn_default_device_profile = {
            "ipv4_network_address_name": "IPV4 Range",
            "ipv4_network_address_zone": "SSLVPN",
            "dns_primary": corp_dns,
            "tunnel_all": True,
            "route_ipv4": ["LAN Subnets"]
        }
        api_obj.configure_ssl_vpn_default_device_profile(**ssl_vpn_default_device_profile)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Configure WAN Group Policy settings for Global VPN client
        wan_group_policy_json = {
            "policy_enable": True,
            "cache_credentials": "always",
            "virtual_adaptor": "dhcp-only"
        }
        api_obj.configure_wan_group_vpn_policy(**wan_group_policy_json)
        # Configure DHCP over VPN central gateway settings
        dhcp_over_vpn_central_gateway = {
            "vpn": {
                "dhcp_over_vpn": {
                    "central": {
                        "internal_dhcp": True,
                        "global_vpn": True,
                        "remote": False,
                        "relay_ip": "0.0.0.0",
                        "send_requests": False
                    }
                }
            }
        }
        api_obj.configure_dhcp_over_vpn_central_gateway(**dhcp_over_vpn_central_gateway)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Configure L2TP Server settings
        l2tp_server_settings = {
            "vpn_enable": True,
            "dns_primary": corp_dns,
            "ip_pool_range": {
                "pool_start": ip_pool_start,
                "pool_end": ip_pool_end
            },
            "user_group": "Trusted Users"
        }
        api_obj.configure_l2tp_server_settings(**l2tp_server_settings)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Adding all the users for different authentication methods
        for auth in authentication_methods:
            api_obj.update_authentication_method(auth_method=auth)
            api_obj.add_user(auth=auth)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Update local user to support GVC client installation with a connection profile added
        api_obj.update_authentication_method(auth_method="Local")
        api_obj.update_local_user_with_options(local_user_name, vpn_access="LAN Subnets")
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Logout from the API Session
        api_obj.api_logout()
        # Installing NetExtender Client
        nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth0_ip, username=local_user_name, password=local_user_password)
        response = nx_obj.install_nx_client()
        Assertion.assert_equal(response, True, "Error: NetExtender client installation failed...")
        # Installing Global VPN Client
        gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=local_user_name, password=local_user_password)
        response = gvc_obj.install_gvc_client()
        Assertion.assert_equal(response, True, "Error: Global VPN Client installation failed...")


# Testcase to verify SonicOS Authentication with all possible auth combinations across different login methods
class test_10001_sonicos_authentication(Test2):
    uuid = '10001'

    # Various Authentication scenarios
    def runTest(self):
        # Verify various authentication combinations for given login method against different authentication methods
        for login in login_methods:
            for auth in authentication_methods:
                # Update the user authentication method for given auth method
                update_user_authentication_method(auth_method=auth)
                # Verify the authentication combinations for given login method
                verify_auth_combination(login_method=login, auth_method=auth)


# Non-Testcase to consolidate and send the result mail after execution
class test_NonTC_consolidate_csv_and_mail_results(Test2):
    uuid = 'NonTC'

    def runTest(self):
        csv_obj = CSVGenerator()
        results = csv_obj.combine_all_csv_files()
        csv_obj.send_combined_results_csv(results)


# Methods for testing various authentication combinations against different web and client components

# Selecting functionality to verify auth combination for given login methods
def verify_auth_combination(login_method, auth_method):
    if login_method == "FireWall_Administration":
        firewall_administration(login_method, auth_method)
    elif login_method == "L2TP_VPN_Client":
        l2tp_vpn_client(login_method, auth_method)
    elif login_method == "SSL-VPN_Portal":
        ssl_vpn_portal(login_method, auth_method)
    elif login_method == "NetExtender_Client":
        netextender_client(login_method, auth_method)
    elif login_method == "Global_VPN_Client":
        global_vpn_client(login_method, auth_method)
    elif login_method == "ULA":
        verify_login_with_ula(login_method, auth_method)


# Update User Authentication method
def update_user_authentication_method(auth_method):
    api_obj = FWConfiguration()
    # Login to FireWall API
    api_obj.api_login()
    # Update the authentication method
    api_obj.update_authentication_method(auth_method)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    # Logout of API
    api_obj.api_logout()


# Verifying FireWall Administration scenarios
def firewall_administration(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    # Update the user with different Admin Groups for testing FireWall Administration scenarios
    for group in fw_administrator_groups:
        api_obj.api_login()
        api_obj.update_user_with_options(auth=auth_method, group_name=group)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Logout of API
        api_obj.api_logout()
        logger.info("\n#####################################################################################\n")
        logger.info("\n-------------------------- Firewall Login with User as: " + group)
        logger.info("\n#####################################################################################\n")
        # 1. Valid Username and Valid Password
        fw_obj = FWLogin(fw_url, username=user_name, password=password)
        response = fw_obj.fw_unpw_login()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 2. Valid Username and Invalid Password
        fw_obj = FWLogin(fw_url, username=user_name, password=invalid_password)
        response = fw_obj.fw_unpw_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 3. Invalid Username and Valid Password
        fw_obj = FWLogin(fw_url, username=invalid_username, password=password)
        response = fw_obj.fw_unpw_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # Verify the above scenarios with second auth server which is 'Local'
        if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
            # 1a. Valid Username and Valid Password
            fw_obj = FWLogin(fw_url, username=local_user_name, password=local_user_password)
            response = fw_obj.fw_unpw_login()
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='UNPW', user=local_user_name, cred_type='Valid',
                                          result=csv_obj.response_checker(response))
            # 2a. Valid Username and Invalid Password
            fw_obj = FWLogin(fw_url, username=local_user_name, password=invalid_password)
            response = fw_obj.fw_unpw_login(expected_failure=True)
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='Password', user=local_user_name, cred_type='Invalid',
                                          result=csv_obj.response_checker(response))
            # 3a. Invalid Username and Valid Password
            fw_obj = FWLogin(fw_url, username=invalid_username, password=local_user_password)
            response = fw_obj.fw_unpw_login(expected_failure=True)
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='Username', user=invalid_username, cred_type='Invalid',
                                          result=csv_obj.response_checker(response))
        # 4. Invalid Username and Invalid Password
        fw_obj = FWLogin(fw_url, username=invalid_username, password=invalid_password)
        response = fw_obj.fw_unpw_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # Enable user with Mail OTP
        api_obj.api_login()
        api_obj.update_user_with_options(auth=auth_method, group_name=group, mail_otp=True)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Logout of API
        api_obj.api_logout()
        # 5. Valid Mail OTP
        mail_obj = MailModule()
        mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
        fw_obj = FWLogin(fw_url, username=user_name, password=password)
        response = fw_obj.fw_login_with_mail_otp()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 6. Invalid Mail OTP
        fw_obj = FWLogin(fw_url, username=user_name, password=password)
        response = fw_obj.fw_login_with_mail_otp(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # Verify the above scenarios with second auth server which is 'Local'
        if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
            # 5a. Valid Mail OTP
            mail_obj = MailModule()
            mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
            fw_obj = FWLogin(fw_url, username=local_user_name, password=local_user_password)
            response = fw_obj.fw_login_with_mail_otp()
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='Mail OTP', user=local_user_name, cred_type='Valid',
                                          result=csv_obj.response_checker(response))
            # 6a. Invalid Mail OTP
            fw_obj = FWLogin(fw_url, username=local_user_name, password=local_user_password)
            response = fw_obj.fw_login_with_mail_otp(expected_failure=True)
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='Mail OTP', user=local_user_name, cred_type='Invalid',
                                          result=csv_obj.response_checker(response))
        # Enable user with TOTP
        api_obj.api_login()
        api_obj.update_user_with_options(auth=auth_method, group_name=group, totp=True)
        # Unbind the TOTP Key
        api_obj.unbind_totp_key(auth=auth_method)
        # Apply the pending configuration changes
        api_obj.api_post_pending()
        # Logout of API
        api_obj.api_logout()
        # 7. Invalid TOTP
        fw_obj = FWLogin(fw_url, username=user_name, password=password)
        response = fw_obj.fw_login_with_totp(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 8. Valid TOTP
        fw_obj = FWLogin(fw_url, username=user_name, password=password)
        response = fw_obj.fw_login_with_totp()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # Verify the above scenarios with second auth server which is 'Local'
        if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
            # 7. Invalid TOTP
            fw_obj = FWLogin(fw_url, username=local_user_name, password=local_user_password)
            response = fw_obj.fw_login_with_totp(expected_failure=True)
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='TOTP', user=local_user_name, cred_type='Invalid',
                                          result=csv_obj.response_checker(response))
            # 8. Valid TOTP
            fw_obj = FWLogin(fw_url, username=local_user_name, password=local_user_password)
            response = fw_obj.fw_login_with_totp()
            csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                          factor='TOTP', user=local_user_name, cred_type='Valid',
                                          result=csv_obj.response_checker(response))


# Verifying L2TP VPN Client login scenarios
def l2tp_vpn_client(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    group = "Trusted Users"
    # Update the user with "LAN Subnets" group for testing L2TP VPN scenarios
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, vpn_access="LAN Subnets")
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # Adding L2TP VPN Connection
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=user_name, password=password)
    l2tp_obj.add_l2tp_vpn_connection()

    logger.info("\n#########################################################################################\n")
    logger.info("\n-----------------------------L2TP VPN Client Login with User-----------------------------\n")
    logger.info("\n#########################################################################################\n")
    # 1. Valid Username and Valid Password
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=user_name, password=password)
    response = l2tp_obj.connect_l2tp_vpn_connection()
    l2tp_obj.disconnect_l2tp_vpn_connection()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # 2. Valid Username and Invalid Password
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=user_name, password=invalid_password)
    response = l2tp_obj.connect_l2tp_vpn_connection(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Password', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # 3. Invalid Username and valid Password
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=password)
    response = l2tp_obj.connect_l2tp_vpn_connection(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method,group=group, auth=auth_method,
                                  factor='Username', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 1a. Valid Username and Valid Password
        l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=local_user_name, password=local_user_password)
        response = l2tp_obj.connect_l2tp_vpn_connection()
        l2tp_obj.disconnect_l2tp_vpn_connection()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 2a. Valid Username and Invalid Password
        l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=local_user_name, password=invalid_password)
        response = l2tp_obj.connect_l2tp_vpn_connection(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 3a. Invalid Username and valid Password
        l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=local_user_password)
        response = l2tp_obj.connect_l2tp_vpn_connection(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # 4. Invalid Username and Invalid Password
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=invalid_password)
    response = l2tp_obj.connect_l2tp_vpn_connection(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Remove L2TP VPN Connection
    l2tp_obj = L2TPVPNClient(hostname=fw_eth1_ip, username=user_name, password=password)
    l2tp_obj.remove_l2tp_vpn_connection()


# Verifying SSL-VPN Portal login scenarios
def ssl_vpn_portal(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    group = "SSLVPN Services"
    # Update the user with "SSLVPN Services" group for testing SSL-VPN Portal scenarios
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()

    logger.info("\n#########################################################################################\n")
    logger.info("\n----------------------------SSL-VPN Portal Login with User-------------------------------\n")
    logger.info("\n#########################################################################################\n")
    # 1. Valid Username and Valid Password
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=password)
    response = sslvpn_obj.sslvpn_portal_unpw_login()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # 2. Valid Username and Invalid Password
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=invalid_password)
    response = sslvpn_obj.sslvpn_portal_unpw_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Password', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # 3. Invalid Username and valid Password
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=invalid_username, password=password)
    response = sslvpn_obj.sslvpn_portal_unpw_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Username', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 1a. Valid Username and Valid Password
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_unpw_login()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 2a. Valid Username and Invalid Password
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=invalid_password)
        response = sslvpn_obj.sslvpn_portal_unpw_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 3a. Invalid Username and valid Password
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=invalid_username, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_unpw_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # 4. Invalid Username and Invalid Password
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=invalid_username, password=invalid_password)
    response = sslvpn_obj.sslvpn_portal_unpw_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Enable user with Mail OTP
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group, mail_otp=True)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # 5. Valid Mail OTP
    mail_obj = MailModule()
    mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=password)
    response = sslvpn_obj.sslvpn_portal_login_with_mail_otp()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Mail OTP', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # 6. Invalid Mail OTP
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=password)
    response = sslvpn_obj.sslvpn_portal_login_with_mail_otp(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Mail OTP', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 5a. Valid Mail OTP
        mail_obj = MailModule()
        mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_login_with_mail_otp()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 6a. Invalid Mail OTP
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_login_with_mail_otp(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # Enable user with TOTP
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group, totp=True)
    # Unbind the TOTP Key
    api_obj.unbind_totp_key(auth=auth_method)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # 7. Invalid TOTP
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=password)
    response = sslvpn_obj.sslvpn_portal_login_with_totp(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='TOTP', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # 8. Valid TOTP
    sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=user_name, password=password)
    response = sslvpn_obj.sslvpn_portal_login_with_totp()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='TOTP', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 7a. Invalid TOTP
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_login_with_totp(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 8a. Valid TOTP
        sslvpn_obj = SSLVPNPortal(sslvpn_portal_url, username=local_user_name, password=local_user_password)
        response = sslvpn_obj.sslvpn_portal_login_with_totp()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))


# Verifying SSL-VPN Portal login scenarios
def netextender_client(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    group = "SSLVPN Services"
    # Update the user with "SSLVPN Services" group for testing SSL-VPN Portal scenarios
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()

    logger.info("\n#########################################################################################\n")
    logger.info("\n--------------------------NetExtender Client Login with User-----------------------------\n")
    logger.info("\n#########################################################################################\n")
    # 1. Valid Username and Valid Password
    nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=user_name, password=password)
    response = nx_obj.nx_valid_login()
    nx_obj.nx_disconnect()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # 2. Valid Username and Invalid Password
    nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=user_name, password=invalid_password)
    response = nx_obj.nx_invalid_login()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Password', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # 3. Invalid Username and valid Password
    nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=invalid_username, password=password)
    response = nx_obj.nx_invalid_login()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Username', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 1a. Valid Username and Valid Password
        nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=local_user_name, password=local_user_password)
        response = nx_obj.nx_valid_login()
        nx_obj.nx_disconnect()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 2a. Valid Username and Invalid Password
        nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=local_user_name, password=invalid_password)
        response = nx_obj.nx_invalid_login()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 3a. Invalid Username and valid Password
        nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=invalid_username, password=local_user_password)
        response = nx_obj.nx_invalid_login()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # 4. Invalid Username and Invalid Password
    nx_obj = SSLVPNNetExtenderCLI(hostname=fw_eth1_ip, username=invalid_username, password=invalid_password)
    response = nx_obj.nx_invalid_login()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))


# Verifying Global VPN Client login scenarios
def global_vpn_client(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    group = "Trusted Users"
    # Update the user with "LAN Subnets" under VPN Access for testing GVC scenarios
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, vpn_access="LAN Subnets")
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # Redirecting GVC logs to a local file
    gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=user_name, password=password)
    gvc_obj.export_gvc_logs()

    logger.info("\n#########################################################################################\n")
    logger.info("\n---------------------------Global VPN Client Login with User-----------------------------\n")
    logger.info("\n#########################################################################################\n")
    # 1. Valid Username and Valid Password
    gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=user_name, password=password)
    response = gvc_obj.gvc_login()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    # 2. Valid Username and Invalid Password
    gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=user_name, password=invalid_password)
    response = gvc_obj.gvc_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Password', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # 3. Invalid Username and valid Password
    gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=password)
    response = gvc_obj.gvc_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Username', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 1a. Valid Username and Valid Password
        gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=local_user_name, password=local_user_password)
        response = gvc_obj.gvc_login()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        # 2a. Valid Username and Invalid Password
        gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=local_user_name, password=invalid_password)
        response = gvc_obj.gvc_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        # 3a. Invalid Username and valid Password
        gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=local_user_password)
        response = gvc_obj.gvc_login(expected_failure=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # 4. Invalid Username and Invalid Password
    gvc_obj = GlobalVPNClient(hostname=fw_eth1_ip, username=invalid_username, password=invalid_password)
    response = gvc_obj.gvc_login(expected_failure=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))


# Verify resource access with ULA scenarios
def verify_login_with_ula(login_method, auth_method):
    api_obj = FWConfiguration()
    com_obj = CommonLib()
    csv_obj = CSVGenerator()
    # Selecting username and password based for the given auth method
    user_name, password = com_obj.select_valid_unpw(auth=auth_method)
    invalid_username = invalid_password = "#inval!d&"
    # Generating CSV file to update results of tested scenarios
    csv_file_name = login_method + "_" + auth_method + "_Authentication"
    csv_obj.generate_csv_file(login_method=login_method, file_name=csv_file_name)
    group = "SonicWALL Administrators"
    # Update the user with "SonicWALL Administrators" group for testing ULA scenarios
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # Configuring default LAN to WAN IPv4 access rule
    configure_ula_settings_from_lan_to_wan(enable=True)
    # Disabling the network adapter
    com_obj.disable_network_adapter(adapter_name="WAN")
    logger.info("\n#########################################################################################\n")
    logger.info("\n--------------------------------ULA verification with User-------------------------------\n")
    logger.info("\n#########################################################################################\n")
    # 1. ULA with valid UNPW
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=password)
    response = ula_obj.verify_ula_and_access_resource()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # 2. ULA with invalid Username and valid Password
    ula_obj = AccessRule(url=wan_resource_url, username=invalid_username, password=password)
    response = ula_obj.verify_ula_and_access_resource_with_expected_failure()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Username', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # 3. ULA with valid Username and invalid Password
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=invalid_password)
    response = ula_obj.verify_ula_and_access_resource_with_expected_failure()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Password', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 1. ULA with valid UNPW
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='UNPW', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        api_obj.api_login()
        api_obj.api_logout()
        # 2. ULA with invalid Username and valid Password
        ula_obj = AccessRule(url=wan_resource_url, username=invalid_username, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource_with_expected_failure()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Username', user=invalid_username, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        api_obj.api_login()
        api_obj.api_logout()
        # 3. ULA with valid Username and invalid Password
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=invalid_password)
        response = ula_obj.verify_ula_and_access_resource_with_expected_failure()
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Password', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        api_obj.api_login()
        api_obj.api_logout()
    # 4. ULA with invalid Username and invalid Password
    ula_obj = AccessRule(url=wan_resource_url, username=invalid_username, password=invalid_password)
    response = ula_obj.verify_ula_and_access_resource_with_expected_failure()
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='UNPW', user=invalid_username, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    # Enable user with Mail OTP
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group, mail_otp=True)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # 5. ULA with valid Mail OTP
    mail_obj = MailModule()
    mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=password)
    response = ula_obj.verify_ula_and_access_resource(mail_otp=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Mail OTP', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # 6. ULA with invalid Mail OTP
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=password)
    response = ula_obj.verify_ula_and_access_resource_with_expected_failure(mail_otp=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='Mail OTP', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 5. ULA with valid Mail OTP
        mail_obj = MailModule()
        mail_obj.read_all_unread_mails(smtp_username, smtp_password, smtp_server_ip)
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource(mail_otp=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))
        api_obj.api_login()
        api_obj.api_logout()
        # 6. ULA with invalid Mail OTP
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource_with_expected_failure(mail_otp=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='Mail OTP', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
    # Enable user with TOTP
    api_obj.api_login()
    api_obj.update_user_with_options(auth=auth_method, group_name=group, totp=True)
    # Unbind the TOTP Key
    api_obj.unbind_totp_key(auth=auth_method)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    api_obj.api_logout()
    # 7. ULA with invalid TOTP
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=password)
    response = ula_obj.verify_ula_and_access_resource_with_expected_failure(totp=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='TOTP', user=user_name, cred_type='Invalid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # 8. ULA with valid TOTP
    ula_obj = AccessRule(url=wan_resource_url, username=user_name, password=password)
    response = ula_obj.verify_ula_and_access_resource(totp=True)
    csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                  factor='TOTP', user=user_name, cred_type='Valid',
                                  result=csv_obj.response_checker(response))
    api_obj.api_login()
    api_obj.api_logout()
    # Verify the above scenarios with second auth server which is 'Local'
    if auth_method == "LDAP-Local" or auth_method == "RADIUS-Local" or auth_method == "TACACS-Local":
        # 7a. ULA with invalid TOTP
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource_with_expected_failure(totp=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=local_user_name, cred_type='Invalid',
                                      result=csv_obj.response_checker(response))
        api_obj.api_login()
        api_obj.api_logout()
        # 8a. ULA with valid TOTP
        ula_obj = AccessRule(url=wan_resource_url, username=local_user_name, password=local_user_password)
        response = ula_obj.verify_ula_and_access_resource(totp=True)
        csv_obj.update_results_to_csv(file_name=csv_file_name, login=login_method, group=group, auth=auth_method,
                                      factor='TOTP', user=local_user_name, cred_type='Valid',
                                      result=csv_obj.response_checker(response))

    # Enable back network adapter
    com_obj.enable_network_adapter(adapter_name="WAN")
    # Reconfiguring default LAN to WAN IPv4 access rule
    configure_ula_settings_from_lan_to_wan(enable=False)


# Configuring requirements for ULA verification
def configure_ula_settings_from_lan_to_wan(enable=False):
    api_obj = FWConfiguration()
    # Login to FireWall API
    api_obj.api_login()
    # Get the default LAN to WAN IPv4 access rule
    rules_list = api_obj.get_ipv4_access_rule_given_from_to(srczone="LAN", destzone="WAN")
    logger.info(rules_list)
    uuid = ""
    for rule in rules_list['access_rules']:
        if rule['ipv4']['auto_rule'] is True:
            uuid = rule['ipv4']['uuid']
    logger.info("The uuid of default LAN to WAN ipv4 access rule is: " + uuid)
    if enable is True:
        user_group = {
            "group": "Trusted Users"
            }
    else:
        user_group = {
            "all": True
        }
    # Modify default access rule from LAN to WAN allowing "Trusted Users" group only
    rule = {
        "name": "Default Access Rule",
        "from": "LAN",
        "to": "WAN",
        "auto_rule": True,
        "user_included": user_group
    }
    response = api_obj.edit_ipv4_access_rule_uuid(uuid, **rule)
    logger.info(response)
    # Apply the pending configuration changes
    api_obj.api_post_pending()
    # Logout from API
    api_obj.api_logout()

