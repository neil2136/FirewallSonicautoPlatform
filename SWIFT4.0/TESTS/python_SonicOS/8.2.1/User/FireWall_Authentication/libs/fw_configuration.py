# This file contains all the libraries related to configuring the firewall for different settings

from libs.fw_api import *
from inputs.request_urls import *
from pytest_resources.common_require import *


class FWConfiguration(FirewallAPI):

    # Get FireWall Hardware and Firmware details
    def get_fw_details(self):
        logger.info("Getting FireWall Hardware and Firmware details...")
        response = self.api_get(request_url=firewall_details)
        logger.info(response)
        return response

    # Enable required services for network interfaces
    def configure_interface_services(self, interface):
        input_json = {
            "interfaces": [
                {
                    "ipv4": {
                        "name": interface,
                        "management": {
                            "https": True,
                            "ping": True,
                            "snmp": False,
                            "ssh": True
                        },
                        "user_login": {
                            "http": False,
                            "https": True
                        }
                    }
                }
            ]
        }
        logger.info("URL to update Network interface services is " + configure_interface_url)
        logger.info("Network interface services JSON: ")
        interface_services_json = json.dumps(input_json)
        logger.info(interface_services_json)
        response = self.api_put(configure_interface_url, data=interface_services_json)
        logger.info("Network interface services updated successfully for interface: " + interface)
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Configure Radius Authentication Server
    def configure_radius_auth_server(self):
        logger.info("Creating RADIUS Auth server..")
        json_file = open(config_jsons_base_path + r"/radius_auth.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create a RADIUS Auth server is " + radius_auth_url)
        logger.info("RADIUS Auth server JSON: ")
        radius_auth_json = json.dumps(input_json)
        logger.info(radius_auth_json)
        response = self.api_post(radius_auth_url, data=radius_auth_json)
        logger.info("RADIUS Auth server created successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Configure LDAP Authentication Server
    def configure_ldap_auth_server(self):
        logger.info("Creating LDAP Auth server..")
        json_file = open(config_jsons_base_path + r"/ldap_auth.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create a LDAP Auth server is " + ldap_auth_url)
        logger.info("LDAP Auth server JSON: ")
        ldap_auth_json = json.dumps(input_json)
        logger.info(ldap_auth_json)
        response = self.api_post(ldap_auth_url, data=ldap_auth_json)
        logger.info("LDAP Auth server created successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Configure TACACS Authentication Server
    def configure_tacacs_auth_server(self):
        logger.info("Creating TACACS Auth server..")
        json_file = open(config_jsons_base_path + r"/tacacs_auth.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create a TACACS Auth server is " + tacacs_auth_url)
        logger.info("TACACS Auth server JSON: ")
        tacacs_auth_json = json.dumps(input_json)
        logger.info(tacacs_auth_json)
        response = self.api_post(tacacs_auth_url, data=tacacs_auth_json)
        logger.info("TACACS Auth server created successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Update the Firewall authentication method
    def update_authentication_method(self, auth_method):
        auth = str(auth_method).lower()
        auth_method_json = {
            "user": {
                "auth": {
                    "auth_method": auth
                }
            }
        }
        response = self.api_put(request_url=auth_method_url, data=json.dumps(auth_method_json))
        logger.info(response)
        return response

    # Add Local User
    def add_local_user(self):
        logger.info("Creating a local user..")
        json_file = open(config_jsons_base_path + r"/local_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to add Local User is " + local_user_url)
        logger.info("Local User JSON: ")
        local_user_json = json.dumps(input_json)
        logger.info(local_user_json)
        response = self.api_post(local_user_url, data=local_user_json)
        logger.info("Local user created successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Get Local user
    def get_local_user_id(self, local_username):
        logger.info("Getting user ID of: \"" + local_username + "\"")
        local_user_url_by_name = local_user_url + '/name/' + local_username
        logger.info("URL to get a local User is " + local_user_url_by_name)
        local_users_list = self.api_get(local_user_url_by_name)
        user_id = local_users_list['user']['local']['user'][0]['uuid']
        return user_id

    # Update local user with group
    def update_local_user_with_options(self, local_username, group_name=None, vpn_access=None,
                                       mail_otp=False, totp=False):
        logger.info("Updating a local user..")
        json_file = open(config_jsons_base_path + r"/local_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if totp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'totp': True})
        if mail_otp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'otp': True})
            input_json['user']['local']['user'][0].update({'email_address': email_id})
        if group_name:
            input_json['user']['local']['user'][0]['member_of'].append({'name': group_name})
        if vpn_access:
            input_json['user']['local']['user'][0]['vpn_client_access'].append({'group': vpn_access})
        user_id = self.get_local_user_id(local_username)
        update_url = local_user_url + '/uuid/' + user_id
        logger.info("URL to update Local User is " + update_url)
        logger.info("Local User JSON: ")
        local_user_json = json.dumps(input_json)
        logger.info(local_user_json)
        response = self.api_put(update_url, data=local_user_json)
        logger.info("Local user updated successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Add LDAP User
    def add_ldap_user(self):
        logger.info("Creating an LDAP user..")
        json_file = open(config_jsons_base_path + r"/ldap_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create an LDAP User is " + ldap_user_url)
        logger.info("LDAP User JSON: ")
        ldap_user_json = json.dumps(input_json)
        logger.info(ldap_user_json)
        response = self.api_post(local_user_url, data=ldap_user_json)
        logger.info("Ldap user created successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Get LDAP user
    def get_ldap_user_id(self, ldap_username):
        logger.info("Getting user ID of: \"" + ldap_username + "\"")
        ldap_user_url_by_name = ldap_user_url + '/name/' + ldap_username + '/domain/' + ldap_user_domain
        logger.info("URL to get a LDAP User is " + ldap_user_url_by_name)
        ldap_users_list = self.api_get(ldap_user_url_by_name)
        user_id = ldap_users_list['user']['local']['user'][0]['uuid']
        return user_id

    # Update LDAP user with group
    def update_ldap_user_with_options(self, ldap_username, group_name=None, vpn_access=None,
                                      mail_otp=False, totp=False):
        logger.info("Updating a ldap user..")
        json_file = open(config_jsons_base_path + r"/ldap_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if totp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'totp': True})
        if mail_otp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'otp': True})
            input_json['user']['local']['user'][0].update({'email_address': email_id})
        if group_name:
            input_json['user']['local']['user'][0]['member_of'].append({'name': group_name})
        if vpn_access:
            input_json['user']['local']['user'][0]['vpn_client_access'].append({'group': vpn_access})
        user_id = self.get_ldap_user_id(ldap_username)
        update_url = ldap_user_url + '/uuid/' + user_id
        logger.info("URL to update LDAP User is " + update_url)
        logger.info("LDAP User JSON: ")
        ldap_user_json = json.dumps(input_json)
        logger.info(ldap_user_json)
        response = self.api_put(update_url, data=ldap_user_json)
        logger.info("LDAP user updated successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Add RADIUS User
    def add_radius_user(self):
        logger.info("Creating a RADIUS user..")
        json_file = open(config_jsons_base_path + r"/radius_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create a RADIUS User is " + radius_user_url)
        logger.info("RADIUS User JSON: ")
        radius_user_json = json.dumps(input_json)
        logger.info(radius_user_json)
        response = self.api_post(radius_user_url, data=radius_user_json)
        logger.info("RADIUS user imported successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Get RADIUS user
    def get_radius_user_id(self, radius_username):
        logger.info("Getting user ID of: \"" + radius_username + "\"")
        radius_user_url_by_name = radius_user_url + '/name/' + radius_username + '/domain/' + radius_user_domain
        logger.info("URL to get a RADIUS User is " + radius_user_url_by_name)
        radius_users_list = self.api_get(radius_user_url_by_name)
        user_id = radius_users_list['user']['local']['user'][0]['uuid']
        return user_id

    # Update RADIUS user with group
    def update_radius_user_with_options(self, radius_username, group_name=None, vpn_access=None,
                                        mail_otp=False, totp=False):
        logger.info("Updating a RADIUS user..")
        json_file = open(config_jsons_base_path + r"/radius_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if totp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'totp': True})
        if mail_otp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'otp': True})
            input_json['user']['local']['user'][0].update({'email_address': email_id})
        if group_name:
            input_json['user']['local']['user'][0]['member_of'].append({'name': group_name})
        if vpn_access:
            input_json['user']['local']['user'][0]['vpn_client_access'].append({'group': vpn_access})
        user_id = self.get_radius_user_id(radius_username)
        update_url = radius_user_url + '/uuid/' + user_id
        logger.info("URL to update RADIUS User is " + update_url)
        logger.info("RADIUS User JSON: ")
        radius_user_json = json.dumps(input_json)
        logger.info(radius_user_json)
        response = self.api_put(update_url, data=radius_user_json)
        logger.info("RADIUS user updated successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Add TACACS User
    def add_tacacs_user(self):
        logger.info("Creating a TACACS user..")
        json_file = open(config_jsons_base_path + r"/tacacs_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("URL to create a TACACS User is " + tacacs_user_url)
        logger.info("TACACS User JSON: ")
        tacacs_user_json = json.dumps(input_json)
        logger.info(tacacs_user_json)
        response = self.api_post(tacacs_user_url, data=tacacs_user_json)
        logger.info("TACACS user imported successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Get TACACS user
    def get_tacacs_user_id(self, tacacs_username):
        logger.info("Getting user ID of: \"" + tacacs_username + "\"")
        tacacs_user_url_by_name = tacacs_user_url + '/name/' + tacacs_username + '/domain/' + tacacs_user_domain
        logger.info("URL to get a TACACS User is " + tacacs_user_url_by_name)
        tacacs_users_list = self.api_get(tacacs_user_url_by_name)
        user_id = tacacs_users_list['user']['local']['user'][0]['uuid']
        return user_id

    # Update TACACS user with group
    def update_tacacs_user_with_options(self, tacacs_username, group_name=None, vpn_access=None,
                                        mail_otp=False, totp=False):
        logger.info("Updating a TACACS user..")
        json_file = open(config_jsons_base_path + r"/tacacs_user.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if totp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'totp': True})
        if mail_otp is True:
            input_json['user']['local']['user'][0]['one_time_password'].update({'otp': True})
            input_json['user']['local']['user'][0].update({'email_address': email_id})
        if group_name:
            input_json['user']['local']['user'][0]['member_of'].append({'name': group_name})
        if vpn_access:
            input_json['user']['local']['user'][0]['vpn_client_access'].append({'group': vpn_access})
        user_id = self.get_tacacs_user_id(tacacs_username)
        update_url = tacacs_user_url + '/uuid/' + user_id
        logger.info("URL to update TACACS User is " + update_url)
        logger.info("TACACS User JSON: ")
        tacacs_user_json = json.dumps(input_json)
        logger.info(tacacs_user_json)
        response = self.api_put(update_url, data=tacacs_user_json)
        logger.info("TACACS user updated successfully..")
        logger.info("Response JSON: ")
        logger.info(response)
        return response

    # Unbind TOTP Key of an User
    def unbind_totp_key_user_based_on_auth(self, url):
        logger.info("URL to Unbind TOTP key for the user is " + url)
        response = self.api_post(request_url=url)
        logger.info("Unbound TOTP Key successfully..")
        logger.info(response)
        return response

    # Configure Mail Server settings
    def config_mail_server(self):
        logger.info("URL to configure mail server is: " + mail_server_settings_url)
        json_file = open(config_jsons_base_path + r"/mail_server.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        logger.info("Mail Server JSON: ")
        mail_server_json = json.dumps(input_json)
        logger.info(mail_server_json)
        response = self.api_put(mail_server_settings_url, data=mail_server_json)
        logger.info("Configured Mail Server successfully...")
        logger.info(response)
        return response

    # Build the IPv4 access rule json
    def build_ipv4_access_rule_json(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/access_rule_ipv4.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if 'comment' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['comment'] = kwargs['comment']
        if 'from' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['from'] = kwargs['from']
        if 'to' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['to'] = kwargs['to']
        if 'action' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['action'] = kwargs['action'].lower()
        if 'name' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['name'] = kwargs['name']
        if 'tcp_timeout' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['tcp']['timeout'] = kwargs['tcp_timeout']
        if 'udp_timeout' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['udp']['timeout'] = kwargs['udp_timeout']
        if 'service' in kwargs.keys():
            dict = {
                'service': {
                    'group': kwargs['service']
                },
            }
            input_json['access_rules'][0]['ipv4'].update(dict)
        if 'schedule' in kwargs.keys():
            dict = {
                'schedule': {
                    'name': kwargs['schedule']
                },
            }
            input_json['access_rules'][0]['ipv4'].update(dict)
        if 'source_addr' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['source']['address'].update(kwargs['source_addr'])
        if 'dst_addr' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['destination'].update(kwargs['dst_addr'])
        if 'user_included' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['users']['included'] = kwargs['user_included']
        if 'user_excluded' in kwargs.keys():
            input_json['access_rules'][0]['ipv4']['users']['excluded'] = kwargs['user_excluded']
        if 'priority_mode' in kwargs.keys():
            if kwargs['priority_mode'] == 'manual':
                if 'priority_value' in kwargs.keys():
                    dict = {
                        "priority": {
                            "manual": {
                                "value": kwargs['priority_value']
                            }
                        }
                    }
                    input_json['access_rules'][0]['ipv4'].update(dict)
        return input_json

    # Configure IPv4 access rule
    def add_ipv4_access_rule(self, **kwargs):
        logger.info("URL to configure ipv4 access rule is: " + access_rule_ipv4_url)
        input_json = self.build_ipv4_access_rule_json(**kwargs)
        access_rule_ipv4_json = json.dumps(input_json)
        logger.info(access_rule_ipv4_json)
        response = self.api_post(access_rule_ipv4_url, data=access_rule_ipv4_json)
        logger.info(response)
        return response

    # Get IPv4 access rule from one zone to another zone
    def get_ipv4_access_rule_given_from_to(self, srczone, destzone):
        access_rule_url = access_rule_ipv4_from_src_to_dest_url.format(srczone, destzone)
        logger.info("URL to get ipv4 access rule from one zone to another zone is: " + access_rule_url)
        response = self.api_get(access_rule_url)
        logger.info(response)
        return response

    # Modify IPv4 access rule by uuid
    def edit_ipv4_access_rule_uuid(self, uuid, **kwargs):
        access_rule_url = access_rule_ipv4_url + '/uuid/' + uuid
        logger.info("URL to modify ipv4 access rule is: " + access_rule_url)
        input_json = self.build_ipv4_access_rule_json(**kwargs)
        access_rule_ipv4_json = json.dumps(input_json)
        logger.info(access_rule_ipv4_json)
        response = self.api_put(access_rule_url, data=access_rule_ipv4_json)
        logger.info(response)
        return response

    # Configure IPv4 Address Objects
    def add_ipv4_address_object(self, **input_json):
        logger.info("URL to configure ipv4 address object is: " + address_object_ipv4_url)
        address_object_ipv4_json = json.dumps(input_json)
        logger.info(address_object_ipv4_json)
        response = self.api_post(address_object_ipv4_url, data=address_object_ipv4_json)
        logger.info(response)
        return response

    # Configure FQDN Address Objects
    def add_fqdn_address_object(self, **input_json):
        logger.info("URL to configure fqdn address object is: " + address_object_fqdn_url)
        address_object_fqdn_json = json.dumps(input_json)
        logger.info(address_object_fqdn_json)
        response = self.api_post(address_object_fqdn_url, data=address_object_fqdn_json)
        logger.info(response)
        return response

    # Configure ssl-vpn server accesses
    def configure_ssl_vpn_server_access(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/ssl_vpn_server_access.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if 'LAN_enable' in kwargs.keys():
            input_json['ssl_vpn']['server']['access'][0]['enable'] = kwargs['LAN_enable']
        if 'WAN_enable' in kwargs.keys():
            input_json['ssl_vpn']['server']['access'][1]['enable'] = kwargs['WAN_enable']
        if 'DMZ_enable' in kwargs.keys():
            input_json['ssl_vpn']['server']['access'][2]['enable'] = kwargs['DMZ_enable']
        if 'WLAN_enable' in kwargs.keys():
            input_json['ssl_vpn']['server']['access'][3]['enable'] = kwargs['WLAN_enable']
        logger.info("URL to configure ssl-vpn server accesses is: " + ssl_vpn_server_access_url)
        ssl_vpn_server_access_json = json.dumps(input_json)
        logger.info(ssl_vpn_server_access_json)
        response = self.api_put(ssl_vpn_server_access_url, data=ssl_vpn_server_access_json)
        logger.info(response)
        return response

    # Build the SSL-VPN Server base json
    def build_ssl_vpn_server_base_json(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/ssl_vpn_server_base.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if 'port_ssl' in kwargs.keys():
            input_json['ssl_vpn']['server']['port'] = kwargs['port_ssl']
        if 'user_domain' in kwargs.keys():
            input_json['ssl_vpn']['server']['user_domain'] = kwargs['user_domain']
        if 'session_timeout' in kwargs.keys():
            input_json['ssl_vpn']['server']['session_timeout'] = kwargs['session_timeout']
        if 'use_self_signed' in kwargs.keys():
            input_json['ssl_vpn']['server']['certificate']['use_self_signed'] = kwargs['use_self_signed']
        elif 'certificate_name' in kwargs.keys():
            input_json['ssl_vpn']['server']['certificate'] = {}
            input_json['ssl_vpn']['server']['certificate']['name'] = kwargs['certificate_name']
        if 'web' in kwargs.keys():
            input_json['ssl_vpn']['server']['management']['web'] = kwargs['web']
        if 'ssh' in kwargs.keys():
            input_json['ssl_vpn']['server']['management']['ssh'] = kwargs['ssh']
        if 'default' in kwargs.keys():
            input_json['ssl_vpn']['server']['download_url'] = {}
            input_json['ssl_vpn']['server']['download_url']['default'] = kwargs['default']
        if 'mschapv2' in kwargs.keys():
            input_json['ssl_vpn']['server']['use_radius']['mschapv2'] = kwargs['mschapv2']
        if 'mschap' in kwargs.keys():
            input_json['ssl_vpn']['server']['use_radius']['mschap'] = kwargs['mschap']
        if 'inactivity_check' in kwargs.keys():
            input_json['ssl_vpn']['server']['inactivity_check'] = kwargs['inactivity_check']
        return input_json

    # Configure ssl-vpn server base settings
    def configure_ssl_vpn_server_base(self, **kwargs):
        logger.info("URL to configure ssl-vpn server base is: " + ssl_vpn_server_base_url)
        input_json = self.build_ssl_vpn_server_base_json(**kwargs)
        ssl_vpn_server_base_json = json.dumps(input_json)
        logger.info(ssl_vpn_server_base_json)
        response = self.api_put(ssl_vpn_server_base_url, data=ssl_vpn_server_base_json)
        logger.info(response)
        return response

    # Build the SSL-VPN Default device profile base json
    def build_default_device_profile_base_json(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/ssl_vpn_default_device_profile.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        search_new = []
        route_new = []

        if 'ipv4_network_address_name' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['name'] = \
                kwargs['ipv4_network_address_name']
            input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['zone'] = \
                kwargs['ipv4_network_address_zone']
        else:
            del input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']

        if 'ipv6_network_address_name' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']['name'] = \
                kwargs['ipv6_network_address_name']
            input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']['zone'] = \
                kwargs['ipv6_network_address_zone']
        else:
            del input_json['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']

        if 'dns_primary' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['primary']['value'] = kwargs[
                'dns_primary']
        if 'dns_secondary' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['secondary']['value'] = kwargs[
                'dns_secondary']
        if 'search_list' in kwargs.keys():
            for search in kwargs['search_list']:
                search_gt = {'search_list': search}
                search_new.append(search_gt)
                logger.info('The search list appended is {}'.format(search_new))
        input_json['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['search_list'] = search_new
        if 'wins_primary' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['wins']['primary']['value'] = kwargs[
                'wins_primary']
        if 'wins_secondary' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['wins']['secondary']['value'] = kwargs[
                'wins_secondary']
        if 'auto_update' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['auto_update'] = kwargs['auto_update']
        if 'exit_after_disconnect' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['exit_after_disconnect'] = kwargs[
                'exit_after_disconnect']
        if 'netbios_over_sslvpn' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['netbios_over_sslvpn'] = kwargs[
                'netbios_over_sslvpn']
        if 'touch_id_authentication' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['touch_id_authentication'] = kwargs[
                'touch_id_authentication']
        if 'fingerprint_authentication' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['fingerprint_authentication'] = kwargs[
                'fingerprint_authentication']
        if 'uninstall_after_exit' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['uninstall_after_exit'] = kwargs[
                'uninstall_after_exit']
        if 'create_connection_profile' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['create_connection_profile'] = kwargs[
                'create_connection_profile']
        if 'tunnel_all' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['routes']['tunnel_all'] = kwargs['tunnel_all']
        if 'route_ipv4' in kwargs.keys():
            for route_list in kwargs['route_ipv4']:
                if 'route_name' in kwargs.keys() and kwargs['route_name']:
                    group_append = {'name': route_list}
                else:
                    group_append = {'group': route_list}
                ipv4_append = {'ipv4': group_append}
                route_new.append(ipv4_append)
                logger.info('The route appended is {}'.format(route_new))
            input_json['ssl_vpn']['profile']['device_profile'][0]['routes']['route'] = route_new
        if 'route_ipv6' in kwargs.keys():
            for route_list in kwargs['route_ipv6']:
                if 'route_name' in kwargs.keys() and kwargs['route_name']:
                    group_append = {'name': route_list}
                else:
                    group_append = {'group': route_list}
                ipv6_append = {'ipv6': group_append}
                route_new.append(ipv6_append)
                logger.info('The route appended is {}'.format(route_new))
            input_json['ssl_vpn']['profile']['device_profile'][0]['routes']['route'] = route_new
        else:
            pass

        if 'credentials' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['credentials'] = kwargs[
                'credentials']
        elif 'user_name_only' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['user_name_only'] = kwargs[
                'user_name_only']
        elif 'cache' in kwargs.keys():
            input_json['ssl_vpn']['profile']['device_profile'][0]['client']['cache'] = kwargs['cache']

        return input_json

    # Configure ssl-vpn server base settings
    def configure_ssl_vpn_default_device_profile(self, **kwargs):
        logger.info("URL to configure ssl-vpn default device profile is: " + ssl_vpn_default_device_profile_url)
        input_json = self.build_default_device_profile_base_json(**kwargs)
        ssl_vpn_default_device_profile_json = json.dumps(input_json)
        logger.info(ssl_vpn_default_device_profile_json)
        response = self.api_put(ssl_vpn_default_device_profile_url, data=ssl_vpn_default_device_profile_json)
        logger.info(response)
        return response

    # Build the SSL-VPN Server base json
    def build_wan_group_vpn_policy_base_json(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/wan_group_vpn_policy.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if 'policy_enable' in kwargs.keys():
            input_json['vpn']['policy'][0]['ipv4']['group_vpn']['enable'] = kwargs['policy_enable']
        if 'cache_credentials' in kwargs.keys():
            input_json['vpn']['policy'][0]['ipv4']['group_vpn']['client']['cache_xauth'] = kwargs['cache_credentials']
        if 'virtual_adaptor' in kwargs.keys():
            input_json['vpn']['policy'][0]['ipv4']['group_vpn']['client']['virtual_adaptor'] = kwargs['virtual_adaptor']
        return input_json

    # Configure WAN Group VPN policy settings
    def configure_wan_group_vpn_policy(self, **kwargs):
        request_url = wan_group_vpn_policy_url.format("WAN GroupVPN")
        logger.info("URL to configure WAN Group VPN policy is: " + request_url)
        input_json = self.build_wan_group_vpn_policy_base_json(**kwargs)
        wan_group_vpn_policy_json = json.dumps(input_json)
        logger.info(wan_group_vpn_policy_json)
        response = self.api_put(request_url, data=wan_group_vpn_policy_json)
        logger.info(response)
        return response

    # Configure DHCP over VPN central gateway settings
    def configure_dhcp_over_vpn_central_gateway(self, **input_json):
        logger.info("URL to configure DHCP over VPN central gateway settings is: " + dhcp_over_vpn_central_gateway_url)
        dhcp_over_vpn_central_gateway_json = json.dumps(input_json)
        logger.info(dhcp_over_vpn_central_gateway_json)
        response = self.api_put(dhcp_over_vpn_central_gateway_url, data=dhcp_over_vpn_central_gateway_json)
        logger.info(response)
        return response

    # Build the L2TP Server Settings base json
    def build_l2tp_server_base_json(self, **kwargs):
        json_file = open(config_jsons_base_path + r"/l2tp_server.json", "r")
        input_json = json.load(json_file)
        json_file.close()
        if 'vpn_enable' in kwargs.keys():
            input_json['vpn']['l2tp_server']['enable'] = kwargs['vpn_enable']
        if 'dns_primary' in kwargs.keys():
            input_json['vpn']['l2tp_server']['dns']['primary'] = kwargs['dns_primary']
        if 'dns_secondary' in kwargs.keys():
            input_json['vpn']['l2tp_server']['dns']['secondary'] = kwargs['dns_secondary']
        if 'wins_primary' in kwargs.keys():
            input_json['vpn']['l2tp_server']['wins']['primary'] = kwargs['wins_primary']
        if 'wins_secondary' in kwargs.keys():
            input_json['vpn']['l2tp_server']['wins']['secondary'] = kwargs['wins_secondary']
        if 'ip_pool_range' in kwargs.keys():
            input_json['vpn']['l2tp_server']['ip_pool']['local']['begin'] = kwargs['ip_pool_range']['pool_start']
            input_json['vpn']['l2tp_server']['ip_pool']['local']['end'] = kwargs['ip_pool_range']['pool_end']
        if 'user_group' in kwargs.keys():
            input_json['vpn']['l2tp_server']['user_group'] = kwargs['user_group']
        return input_json

    # Configure L2TP Server settings
    def configure_l2tp_server_settings(self, **kwargs):
        logger.info("URL to configure WAN Group VPN policy is: " + l2tp_server_settings_url)
        input_json = self.build_l2tp_server_base_json(**kwargs)
        l2tp_server_settings_json = json.dumps(input_json)
        logger.info(l2tp_server_settings_json)
        response = self.api_put(l2tp_server_settings_url, data=l2tp_server_settings_json)
        logger.info(response)
        return response

    # Enabling NTP service
    def enable_ntp_service(self):
        logger.info("URL to configure ssl-vpn server base is: " + enable_ntp_service_url)
        ntp_json = {
            "time": {
                "use_ntp": True
            }
        }
        response = self.api_put(enable_ntp_service_url, data=json.dumps(ntp_json))
        logger.info(response)
        return response

    # Configuring Auth Server
    def configure_auth_server(self, auth):
        if auth == "Local":
            logger.info("Local auth server is by default configured...")
        elif auth == "LDAP":
            self.configure_ldap_auth_server()
        elif auth == "RADIUS":
            self.configure_radius_auth_server()
        elif auth == "TACACS":
            self.configure_tacacs_auth_server()
        elif auth == "LDAP-Local":
            logger.info("Both the auth servers already added...")
        elif auth == "RADIUS-Local":
            logger.info("Both the auth servers already added...")
        elif auth == "TACACS-Local":
            logger.info("Both the auth servers already added...")

    # Adding User
    def add_user(self, auth):
        if auth == "Local":
            self.add_local_user()
        elif auth == "LDAP":
            self.add_ldap_user()
        elif auth == "RADIUS":
            self.add_radius_user()
        elif auth == "TACACS":
            self.add_tacacs_user()
        elif auth == "LDAP-Local":
            logger.info("Both the users already added...")
        elif auth == "RADIUS-Local":
            logger.info("Both the users already added...")
        elif auth == "TACACS-Local":
            logger.info("Both the users already added...")

    # Updating User
    def update_user_with_options(self, auth, group_name=None, vpn_access=None, mail_otp=False, totp=False):
        if auth == "Local":
            self.update_local_user_with_options(local_username=local_user_name, group_name=group_name,
                                                vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "LDAP":
            self.update_ldap_user_with_options(ldap_username=ldap_user_name, group_name=group_name,
                                               vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "RADIUS":
            self.update_radius_user_with_options(radius_username=radius_user_name, group_name=group_name,
                                                 vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "TACACS":
            self.update_tacacs_user_with_options(tacacs_username=tacacs_user_name, group_name=group_name,
                                                 vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "LDAP-Local":
            self.update_ldap_user_with_options(ldap_username=ldap_user_name, group_name=group_name,
                                               vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
            # Apply the pending configuration changes
            self.api_post_pending()
            self.update_local_user_with_options(local_username=local_user_name, group_name=group_name,
                                                vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "RADIUS-Local":
            self.update_radius_user_with_options(radius_username=radius_user_name, group_name=group_name,
                                                 vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
            # Apply the pending configuration changes
            self.api_post_pending()
            self.update_local_user_with_options(local_username=local_user_name, group_name=group_name,
                                                vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
        elif auth == "TACACS-Local":
            self.update_tacacs_user_with_options(tacacs_username=tacacs_user_name, group_name=group_name,
                                                 vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)
            # Apply the pending configuration changes
            self.api_post_pending()
            self.update_local_user_with_options(local_username=local_user_name, group_name=group_name,
                                                vpn_access=vpn_access, mail_otp=mail_otp, totp=totp)

    # unbind totp key
    def unbind_totp_key(self, auth):
        if auth == "Local":
            unbind_totp_key_url = local_user_unbind_totp_key_url.format(local_user_name)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "LDAP":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(ldap_user_name, ldap_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "RADIUS":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(radius_user_name, radius_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "TACACS":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(tacacs_user_name, tacacs_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "LDAP-Local":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(ldap_user_name, ldap_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
            unbind_totp_key_url = local_user_unbind_totp_key_url.format(local_user_name)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "RADIUS-Local":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(radius_user_name, radius_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
            unbind_totp_key_url = local_user_unbind_totp_key_url.format(local_user_name)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
        elif auth == "TACACS-Local":
            unbind_totp_key_url = domain_user_unbind_totp_key_url.format(tacacs_user_name, tacacs_user_domain)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)
            unbind_totp_key_url = local_user_unbind_totp_key_url.format(local_user_name)
            self.unbind_totp_key_user_based_on_auth(url=unbind_totp_key_url)

