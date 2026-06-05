import sys
import os
import traceback
sys.path.append(os.environ['SONICOS_HOME']+'/6.5.4/python_lib')
#sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
from utm import Firewall
from modules.API.users import UsersettingApi
from modules.API.users import UserStatusApi
from modules.API.users import RadiusApi
from modules.API.users import LdapApi
from modules.API.users import SSOApi
from modules.API.users import UserLocalApi
from modules.API.users import UserGuestApi


ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')


###########################################User Status########################################

user_status = UserStatusApi(fw)


# aa = user_status.show_user_status()

user_status_dict = {'inactive_users': False,
                    'unauthenticated_users': True
}

# aa = user_status.user_management(**user_status_dict)



###############################################User Setting######################################

user_setting = UsersettingApi(fw)

# aa = user_setting.show_user_setting()

user_authen= {'method': 'radius',
              # 'method': 'local',
              # 'method': 'radius_local',
              # 'method': 'ldap',
              # 'method': 'ldap_local',
              'email_format': 'plain_text',
              # 'email_format': 'html',
              'format': 'numbers',
              # 'format': 'characters',
              # 'format': 'mixed',
              'Onetimepasswordlengthmin': 4,
              'Onetimepasswordlengthmax': 9
}

# aa = user_setting.user_authentication(**user_authen)

user_weblogin_dict = {'browser_redirect_via': 'reverse_dns',
                      # 'browser_redirect_via': 'interface_ip',
                      'time_in_minutes': 15,
                      'http_redirect_after_login': False
                      
}

# aa = user_setting.web_login(**user_weblogin_dict)

user_session_dict = {'age_out_time_in_minutes': 19,
                     'inactivity_time_in_minutes': 18,
                     # 'service': ['group', 'Citrix'],
                     'service': ['name', 'BGP'],
                     'originating_externally': '111111',
                     'other_unidentified': '2222222',
                     'ssoFailUserName': '3333333333',
                     'bypassSsoUserName': '44444444',
                     'inactivity_authentication': ['terminate_after', 16],
                     'inactivity_other': ['terminate_after', 17],
                     'reported_authentication': ['terminate_after', 18],
                     'reported_other': 'keep_alive',
                     'inactive_user': 
                        {'login': False,
                         'timeout': False
                        },
                     'show_user_status_window': True,
                     'disconnected_user_detect': False,
                     'period_in_seconds': 50,
                     'open_in_same_window': True,
                     'web_login_session_limit': 40
}

# aa = user_setting.user_session(**user_session_dict)

customization_dict = {'window_size_width': 400,    # 400~1280
                      'window_size_height': 260,
                      'zonetype': 
                         {'trusted': True,
                          'public': True,
                          'wireless': True,
                          'vpn': True},
                      'loginpage':
                          {'preempt': 'cccccc',
                           'status': 'ddddd'
                           },
                      'scroll_bars': False,
                      'content': 'bbbb',
                      'pocontent': 'aaaa'
}

# aa = user_setting.customization(**customization_dict)



#########################################User Radius########################################################

user_radius = RadiusApi(fw)

# aa = user_radius.show_user_radius_settings()

# aa = user_radius.show_radius_server()

# aa = user_radius.show_radius_account()

# aa = user_radius.show_radius_reporting_statistic()

# aa= user_radius.del_radius_reporting_statistic()

user_radius_settings_dict = {'local_users_only': True,
                             'group_name': 'Guest Administrators',
                             'timeout': 6,
                             'retries': 6,
                             # 'radius_attribute': 'filter-id'
                             # 'radius_attribute': 'vendor-specific'
                             'mechanism_ldap': True
                             # 'mechanism_local_only': True
}

# aa = user_radius.user_radius_settings(**user_radius_settings_dict)


add_radius_server_dict = {'host': '1.1.1.5',  # host is must
                          'enable': False,
                          'port_num': 1891,
                          'secret': 'password',
                          'send_through_vpn_tunnel': False,
                          'user_name_format': 'user_principle',
                          # user_name_format:user_name/user_principle/name_dot_domain/down_level_logon
                          }

# aa = user_radius.add_radius_server(**add_radius_server_dict)

edit_radius_server_dict = {
                          'host': '1.1.1.5',  # host is must
                          'port_num': 2001,  
                          'secret': '123abc',
                          'send_through_vpn_tunnel': True,
                          'user_name_format': 'user_name',
                          # user_name_format:user_name/user_principle/name_dot_domain/down_level_logon
                          'enable': True
}

# aa = user_radius.edit_radius_server(**edit_radius_server_dict)


radiusserver_name = '1.1.1.5'

# cc = user_radius.del_radius_server(radiusserver_name)


########### Radius_account functions are temporarily unavailable, dts#221377###############

add_radius_account_dict = {
                          'host': '5.5.5.5',  # host is must
                          'port': 1891,
                          'enable': True,
                          'secret': 'password',
                          'user_name_format': 'user_principle',
                           # user_name_format:user_name/user_principle/name_dot_domain/down_level_logon
}

# aa = user_radius.add_radius_account(**add_radius_account_dict)

edit_radius_account_dict = {
                          'host': '5.5.5.5',   # host is must
                          'port': 1913,
                          'secret': '123pass',
                          'user_name_format': 'user_name',
                          # user_name_format:user_name/user_principle/name_dot_domain/down_level_logon
                          'enable': True
}

# aa = user_radius.edit_radius_account(**edit_radius_account_dict)


radiusaccount_name = '5.5.5.5'

# aa = user_radius.del_radius_account(radiusaccount_name)



#########################################User Radius########################################################

user_ldap = LdapApi(fw)

# aa = user_ldap.show_ldap_setting()

# aa = user_ldap.show_ldap_servers()

# aa = user_ldap.show_ldap_reporting_statistic()

# aa = user_ldap.del_ldap_reporting_statistic()

# ldapserverip = '1.2.3.5'
# aa = user_ldap.show_ldap_server_reporting_statistic(ldapserverip)

# ldapserverip = '1.2.3.5'
# aa = user_ldap.del_ldap_server_reporting_statistic(ldapserverip)

ldap_setting = {
                'version': 3,
                'require_valid_certificate': True,
                'allow_referrals': True,
                'user_authentication': False,
                'auto_configuration': False,
                'domain_search': False,
                'other_search': False,
                'local_users_only': True,
                'group_name': 'Everyone',
                # group_name:SonicWALL Administrators/Content Filtering Bypass/Limited Administrators
                # /SSLVPN Services/SonicWALL Read-Only Admins/Guest Services/
                'mirror_user_groups': 'have_members',
                'refresh': 'period',
                'minutes': 6,
                'enableradiustoldaprelay': True,
                'public_zones': True,
                'trusted_zones': True,
                'wan_zone': True,
                'wireless_zones': True,
                'vpn_zone': True,
                'RADIUSsharedsecret': '123pass',
                'vpnGroupName': '11111',
                'vpnClientGroupName': '222222',
                'l2tpGroupName': '33333',
                'internetAccessGroupName': '4444'
}

# aa = user_ldap.ldap_setting(**ldap_setting)

add_ldap_server = {
                  'role': 'primary',
                  # 'role': 'secondary',
                  'host': '6.3.3.83',
                  'enable': False,
                  'port_num': 636,
                  'use_tls': True,
                  'timeout': True,
                  'servertimeout': 5,
                  'overalloperationtimeout': 4,
                  'send_start_tls_request': True,
                  'bind' : 'distinguished_name',
                  'distinguished_name': 'test',
                  # 'bind' : 'anonymous',
                  # 'bind' : 'acct',
                  'referred_bind_with_account': 'other-servers',
                  # 'referred_bind_with_account': 'local',
                  'primary_domain': 'testdomain.com',
                  'users_tree': ['user1', 'user2', 'user3'],
                  'user_groups_tree': ['group1', 'group2', 'group3'],
                  'directory': True,
                  'schema': 'inet-org-person',
                  # six kinds of schema:
                  # microsoft-active-directory/network-information-service
                  # samba-smb/custom/Novell eDirectory/inet-org-person
                  'additional_group_id': 'test',
                  'additional_group_match': 'aaaamatch'
}

# aa = user_ldap.add_ldap_server(**add_ldap_server)

edit_ldap_server = {
                  # 'role': 'secondary',
                  'role': 'primary',
                  'host': '6.3.3.83',
                  'enable': True,
                  'directory': True,
                  'use_tls': True,
                  'port_num': 389,
                  'timeout': True,
                  'servertimeout': 6,
                  'overalloperationtimeout': 6,
                  'send_start_tls_request': False,
                  # 'bind' : 'distinguished_name',
                  # 'bind' : 'anonymous',
                  # 'bind' : 'acct',
                  # 'users_tree': ['user4', 'user5', 'user6'],
                  # 'user_groups_tree': ['group5', 'group6', 'group7'],
                  'referred_bind_with_account': 'other-servers',
                  # 'referred_bind_with_account': 'local',
                  'distinguished_name': '123',
                  'primary_domain': '111.com',
                  'schema': 'microsoft-active-directory',
                  'qualified_logon_name': 'testlogonname',
                  # 'schema': 'samba-smb',
                  # 'framed_ip_address': '192.168.168.155',
                  # 'qualified_logon_name': 'samba-smb',
                  # 'schema': 'network-information-service',
                  # 'additional_group_id': '555',
                  # 'framed_ip_address': '192.168.168.188',
                  # 'qualified_logon_name': 'ation-serv',
                  # 'schema': 'inet-org-person',
                  # 'additional_group_id': '666',
                  # 'framed_ip_address': '192.168.168.199',
                  # 'qualified_logon_name': 'inet-org-person',
                  # six kinds of schema:
                  # microsoft-active-directory/network-information-service
                  # samba-smb/custom/Novell eDirectory/inet-org-person
                  # 'additional_group_match': '7777'

}

# aa = user_ldap.edit_ldap_server(**edit_ldap_server)


del_ldapserver = '6.3.3.83'

# aa = user_ldap.del_ldap_server(del_ldapserver)



#########################################User SSO########################################################

user_sso = SSOApi(fw)

# aa = user_sso.show_sso_settings()

# aa = user_sso.show_sso_agents()


sso_settings = {
        'EnableSSOagentauthentication': True,
        'terminal_services_agent': True,
        'enablessobyradiusaccounting': True,
        'next_agent_on_no_name': False,
        'block_traffic': False,
        # 'including_for_access_rules': 'selected',
        'including_for_access_rules': 'all',
        'local_users_only': True,
        'non_domain_limited_access': False,
        'user_group_mechanism': 'ldap',
        # 'user_group_mechanism': 'local',
        'probeusersfor': 'over_tcp',
        # 'probeusersfor': 'over_netbios',
        # 'probeusersfor': 'wmi',
        'probetimeout': 10,
        'probetest_mode': True,
        'poll_rate': 10,
        'poll_same_agent': False,
        'holdtime_after_failure': 6,
        'holdtime_after_no_user': 7,
        'tsa_services_bypass': True,
        'dummy_user_name': 'test11',
        'dummy_user_timeout': 15,
        'radius_accounting_port': 1813
}

aa = user_sso.sso_settings(**sso_settings)

add_enforce_on_zone = {
                   'enforce_on_zone': ['WLAN', 'DMZ', 'VPN', 'MGMT','LAN']
}

# aa = user_sso.add_enforce_on_zone(**add_enforce_on_zone)

delete_zone = 'DMZ'
# delete_zone = 'DMZ'/'VPN'/'MGMT'/'LAN'/'WAN'
# aa = user_sso.del_enforce_on_zone(delete_zone)

#### windows_service on SSO--SSO Agents---General Setting---User names used by Windows services

add_windows_service_user_name = {
                   'windows_service_user_name': ['111', '222', '333', '444','555']
}

# aa = user_sso.add_windows_service_user_name(**add_windows_service_user_name)

delete_windows_service = '111'
# delete_windows_service = '222'/'333'/'444'/'555'
# aa = user_sso.del_windows_service_user_name(delete_windows_service)


#########sso_bypass on SSO--SSO Agents--Enforcement####

add_sso_bypass = {
            'action': 'add',
            'security_service_bypass': {
                   'service1': {
                                 "address": {
                                    "group": "All Rogue Devices"
                                 },
                                 "type": "trigger-sso"
                               },
                   'service2': {
                                 "service": {
                                    "group": "Kerberos"
                                 },
                                 "type": "trigger-sso"
                               },
                    'service3': {           
                               "service": {
                                   "group": "IGMP"
                               },
                               "type": "full-bypass"
                              },
                        
                    'service4': {
                               "address": {
                                    "name": "MGMT IP"
                                },
                               "type": "trigger-sso"
                               }
                   }
}

# aa = user_sso.sso_bypass(**add_sso_bypass)

del_sso_bypass = {
            'action': 'delete',
            'security_service_bypass': {
                   # 'service1': {
                                 # "address": {
                                    # "group": "All Rogue Devices"
                                 # },
                                 # "type": "trigger-sso"
                               # },
                   'service2': {
                                 "service": {
                                    "group": "Kerberos"
                                 },
                                 "type": "trigger-sso"
                               },
                    'service3': {           
                               "service": {
                                   "group": "IGMP"
                               },
                               "type": "full-bypass"
                              },
                        
                    # 'service4': {
                               # "address": {
                                    # "name": "MGMT IP"
                                # },
                               # "type": "trigger-sso"
                               # }
                   }
}

# aa = user_sso.sso_bypass(**del_sso_bypass)

add_sso_agent = {
                 'action': 'add',
                 'host': '1.2.2.3',
                 'port': 2258,
                 'timeout': 10,
                 'retries': 6,
                 'max_requests': 32,
                 'enable': True,
                 'number': '1Abdce'
}

# aa = user_sso.sso_agent(**add_sso_agent)

edit_sso_agent = {
                 'action': 'edit',
                 'host': '1.2.2.3',
                 'port': 2260,
                 'timeout': 9,
                 'retries': 5,
                 'max_requests': 16,
                 'enable': False,
                 'number': '1Abdce'
}

# aa = user_sso.sso_agent(**edit_sso_agent)


del_sso_agent = '1.2.2.3'
# aa = user_sso.del_sso_agent(del_sso_agent)


add_terminal_services_agent = {
                 'action': 'add',
                 'host': '1.1.1.1',
                 'port': 2259,
                 'enable': True,
                 'number': '1Abdce'
}

# aa = user_sso.terminal_services_agent(**add_terminal_services_agent)

edit_terminal_services_agent = {
                 'action': 'edit',
                 'host': '1.1.1.1',
                 'port': 2260,
                 'enable': False,
                 'number': '1Abdce'
}

# aa = user_sso.terminal_services_agent(**edit_terminal_services_agent)

del_tsa = '1.1.1.1'
# aa = user_sso.del_terminal_services_agent(del_tsa)


add_sso_radius_accounting_client = {
                 'action': 'add',
                 'host': '3.3.3.3',
                 'user_name_format': 'down_level_logon',
                 # 'user_name_format': 'user_name'/'down_level_logon'/'canonical'/'user_principle'/'sonicwall_aventail'
                 'missing_domain': 'ldap_look_up',
                 # 'missing_domain': 'local_user',
                 'proxy_forward': True,
                 'proxyforward_timeout': 15,
                 'log_user_out': 12,
                 'proxyforward_retries': 20,
                 # 'proxyforward_type': 'try_next_on_timeout',
                 'proxyforward_type': 'forward_to_all',
                 'secret': 'password',
                 'server': {
                   'server1': {
                               'serverId': 1,
                               'name': '10.10.10.100',
                               'port': 1813,
                               'shared_secret': 'password'
                              },
                   'server2': {
                              'serverId': 2,
                              'name': '10.10.10.101',
                              'port': 1816,
                              'shared_secret': 'password'
                             }
                    # 'server3': {
                              # 'serverId': 3,
                              # 'name': '10.10.10.102',
                              # 'port': 1816,
                              # 'shared_secret': 'password'
                             # },
                    # 'server4': {
                              # 'serverId': 4,
                              # 'name': '10.10.10.103',
                              # 'port': 1816,
                              # 'shared_secret': 'password'
                             # }
                }
}

# aa = user_sso.sso_radius_accounting_client(**add_sso_radius_accounting_client)

edit_sso_radius_accounting_client = {
                 'action': 'edit',
                 'host': '3.3.3.3',
                 'user_name_format': 'user_name',
                 # 'user_name_format': 'user_name'/'down_level_logon'/'canonical'/'user_principle'/'sonicwall_aventail'
                 'missing_domain': 'ldap_look_up',
                 # 'missing_domain': 'local_user',
                 'proxy_forward': True,
                 'proxyforward_timeout': 6,
                 'proxyforward_retries': 6,
                 'proxyforward_type': 'try_next_on_timeout',
                 # 'proxyforward_type': 'forward_to_all',
                 'secret': 'password',
                 'server': {
                   'server1': {
                               'serverId': 1,
                               'name': '10.10.10.100',
                               'port': 1813,
                               'shared_secret': 'password'
                              },
                   'server2': {
                              'serverId': 2,
                              'name': '10.10.10.101',
                              'port': 1816,
                              'shared_secret': 'password'
                             },
                    'server3': {
                              'serverId': 3,
                              'name': '10.10.10.102',
                              'port': 1816,
                              'shared_secret': 'password'
                             },
                    'server4': {
                              'serverId': 4,
                              'name': '10.10.10.103',
                              'port': 1816,
                              'shared_secret': 'password'
                             }
                }
}

# aa = user_sso.sso_radius_accounting_client(**edit_sso_radius_accounting_client)


del_srac = '3.3.3.3'
# aa = user_sso.del_sso_radius_accounting_client(del_srac)


#########################################Local User and Local Group########################################################

# Some dts on user_bookmark/group_bookmark/ldap_location
# The user or group that with domain can not be added/edited,the code are ready but not merged yet


user_local = UserLocalApi(fw)

# aa = user_local.show_local_settings() 

# aa = user_local.show_local_groups()

# aa = user_local.show_local_users()


local_settings = {
                  'apply_password_constraints': False,
                   'prune_on_expiry': False
}

# aa = user_local.local_settings(**local_settings)

add_local_user = {
                'action': 'add',
                'username': '666',
                'userpassword': '123password',
                'force_password_change': True,
                'domain': 'mydomain.com',
                'one_time_password': 'totp',
                'email_address': 'wegu@sonicwall.com',
                'account_lifetime': True,
                'accountlifetime': 3,
                'lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sessionlifetime': 1,
                'sessionlifetimetype': 'days',
                'userquotalimit': True,
                'receivelimit': 50,
                'transmit': 60
}

# aa = user_local.local_user(**add_local_user)


edit_local_user_no_domain = {
                'action': 'edit',
                # 'oldusername': '666',
                'username': '666',
                'userpassword': '123password',
                'force_password_change': False,
                # 'domain': 'mydomain.com',
                'one_time_password': 'otp',
                'email_address': 'wegu@sonicwall.com',
                'account_lifetime': False,
                'accountlifetime': 2,
                'lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sessionlifetime': 1,
                'sessionlifetimetype': 'days',
                'userquotalimit': True,
                'receivelimit': 80,
                'transmit': 90
}

# aa = user_local.local_user(**edit_local_user_no_domain)

edit_local_user_with_domain = {
                'action': 'edit',
                'oldusername': '666',
                'username': '999',
                'userpassword': '123password',
                'force_password_change': False,
                'domain': 'mydomain.com',
                'one_time_password': 'otp',
                'email_address': 'wegu@sonicwall.com',
                'account_lifetime': False,
                'accountlifetime': 2,
                'lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sessionlifetime': 1,
                'sessionlifetimetype': 'days',
                'userquotalimit': True,
                'receivelimit': 80,
                'transmit': 90
}

# aa = user_local.local_user(**edit_local_user_with_domain)


username = '666'
# aa = user_local.delete_local_user_no_domain(username)


username = '444'
domainname = 'test2.com'
# aa = user_local.delete_local_user_with_domain(username, domainname)


add_member_of_user = {
                     'action': 'add',
                     'username': '666',
                     'userpassword': '111111111',
                     'member_of': ['SonicWALL Administrators', 'Limited Administrators', 'Guest Services']
}


# aa = user_local.user_member_of(**add_member_of_user)


del_member_of_user = {
                     'action': 'delete',
                     'username': '666',
                     'userpassword': '111111111',
                     'member_of': ['SonicWALL Administrators']
}
# member:SonicWALL Administrators/Content Filtering Bypass/Limited Administrators
        # /SSLVPN Services/SonicWALL Read-Only Admins/Guest Services/

# aa = user_local.user_member_of(**del_member_of_user)

add_user_vpn_client_access = {
                     'action': 'add',
                     'username': '666',
                     'userpassword': '111111111',
                     'vpn_client_access': ['All X1 Management IP', 'Capture Client Enforcement List', 
                     'All Rogue Access Points', 'X0 IPv6 Addresses', 'LAN Subnets']
}


# aa = user_local.user_vpn_client_access(**add_user_vpn_client_access)


del_user_vpn_client_access = {
                     'action': 'delete',
                     'username': '666',
                     'userpassword': '111111111',
                     'vpn_client_access': ['All X1 Management IP', 'Capture Client Enforcement List', 
                     'All Rogue Access Points']
}


# aa = user_local.user_vpn_client_access(**del_user_vpn_client_access)

add_user_bookmark = {
                   'action': 'add',
                   'username': '444',
                   'userpassword': '123password',
                   'bookmarkname': 'newbm',
                   'bookmarkhost': '192.168.168.57',
                   'service': 'rdp',
                   'screen_size': 'full-screen',
                   'colors': '16bit',
                   'application_path': 'C:\\\\Remote Applications\\\\myapp.exe',
                   'start_in_folder': 'C:\\Work\\',
                   'windows_advanced_options': {
                                    'redirect_clipboard': True,
                                    'redirect_audio': False,
                                    'auto_reconnection': True,
                                    'desktop_background': True,
                                    'window_drag': True,
                                    'animation': True,
                                    },
                   'automatic_login': 'custom',
                   'usecustomcredentialsname': '1111',
                   'usecustomcredentialspass': 'password111',
                   'usecustomcredentialsdomain': 'mydomain.com',
                   'display_on_mobile': False
}

# aa = user_local.user_bookmark(**add_user_bookmark)

add_local_group = {
                  'action': 'add',
                  # 'grouptype': 'LDAP_directory',
                  # 'groupname': 'test888',
                  # 'comment': 'test1add',
                  # 'one_time_password': 'totp',
                  # 'ldap_location': 'domain.com',
                  # 'memberships_by_ldap_location': 'at',
                  # 'grouptype': 'domaingroup',
                  # 'domainname': 'test2.com',
                  # 'groupname': 'test2',
                  # 'comment': 'test1add',
                  # 'one_time_password': 'otp',
                  'grouptype': 'locally_only',
                  'groupname': 'test5',
                  'comment': 'test1add',
                  'one_time_password': 'otp',
}

# aa = user_local.local_group(**add_local_group)


edit_local_group = {
                  'action': 'edit',
                  # 'grouptype': 'LDAP_directory',
                  # 'groupname': 'test888',
                  # 'comment': 'test89add',
                  # 'one_time_password': 'otp',
                  # 'ldap_location': '1111',
                  # 'memberships_by_ldap_location': 'at',
                  # 'grouptype': 'domaingroup',
                  # 'domainname': 'test888.com',
                  # 'groupname': 'test2',
                  # 'comment': 'test88882222add',
                  # 'one_time_password': 'totp',
                  'grouptype': 'locally_only',
                  'groupname': 'test5',
                  'comment': 'test585add',
                  'one_time_password': 'totp',
}

# aa = user_local.local_group(**edit_local_group)


groupname = 'test5'
# aa = user_local.delete_local_group_no_domain(groupname)


groupname = 'test2'
domainname = 'test2.com'
# aa = user_local.delete_local_group_with_domain(groupname,domainname)


add_member_of_group = {
                     'action': 'add',
                     'groupname': '111',
                     'member_of': ['SonicWALL Administrators', 'SonicWALL Read-Only Admins', 'Guest Services']
}
# member:SSLVPN Services/Guest Services/SonicWALL Read-Only Admins
        # /SonicWALL Administrators/"Limited Administrators/Content Filtering Bypass
# aa = user_local.group_member_of(**add_member_of_group)


del_member_of_group = {
                     'action': 'delete',
                     'groupname': '111',
                     'member_of': ['SonicWALL Administrators', 'SonicWALL Read-Only Admins']
}
# member:SSLVPN Services/Guest Services/SonicWALL Read-Only Admins
        # /SonicWALL Administrators/"Limited Administrators/Content Filtering Bypass
# aa = user_local.group_member_of(**del_member_of_group)


add_group_vpn_client_access = {
                     'action': 'add',
                     'groupname': '111',
                     'vpn_client_access': ['Social Login Pass Group', 'All U0 Management IP', 'All X6 Management IP']
}

# aa = user_local.group_vpn_client_access(**add_group_vpn_client_access)


del_group_vpn_client_access = {
                     'action': 'delete',
                     'groupname': '111',
                     'vpn_client_access': ['Social Login Pass Group',]
}

# aa = user_local.group_vpn_client_access(**del_group_vpn_client_access)


add_group_bookmark = {
                   'action': 'add',
                   'groupname': '111',
                   'bookmarkname': 'newbm',
                   'bookmarkhost': '192.168.168.57',
                   'service': 'rdp',
                   'screen_size': 'full-screen',
                   'colors': '16bit',
                   'application_path': 'C:\\\\Remote Applications\\\\myapp.exe',
                   'start_in_folder': 'C:\\Work\\',
                   'windows_advanced_options': {
                                    'redirect_clipboard': True,
                                    'redirect_audio': False,
                                    'auto_reconnection': True,
                                    'desktop_background': True,
                                    'window_drag': True,
                                    'animation': True,
                                    },
                   'automatic_login': 'custom',
                   'usecustomcredentialsname': '1111',
                   'usecustomcredentialspass': 'password111',
                   'usecustomcredentialsdomain': 'mydomain.com',
                   'display_on_mobile': False
}

# aa = user_local.group_bookmark(**add_group_bookmark)


edit_group_bookmark = {
                   'action': 'edit',
                   'groupname': '111',
                   'bookmarkname': '111',
                   'bookmarkhost': '192.168.168.57',
                   'service': 'rdp',
                   'screen_size': 'full-screen',
                   'colors': '16bit',
                   'application_path': 'C:\\\\Remote Applications\\\\myapp.exe',
                   'start_in_folder': 'C:\\Work\\',
                   'windows_advanced_options': {
                                    'redirect_clipboard': True,
                                    'redirect_audio': False,
                                    'auto_reconnection': True,
                                    'desktop_background': True,
                                    'window_drag': True,
                                    'animation': True,
                                    },
                   'automatic_login': 'custom',
                   'usecustomcredentialsname': '1111',
                   'usecustomcredentialspass': 'password111',
                   'usecustomcredentialsdomain': 'mydomain.com',
                   'display_on_mobile': False
}

# aa = user_local.group_bookmark(**edit_group_bookmark)


###########################################User Status########################################

user_guest = UserGuestApi(fw)

# aa = user_guest.show_user_guest_settings()

add_profile = {
                'action': 'add',
                'profilename': '8777',
                'generate': True,
                'generatename': True,
                'generatepassword': False,
                'name_prefix': 'otp',
                'activate_on_login': True,
                'enable_account': True,
                'login_uniqueness': False,
                'account_lifetime': False,
                'acco_lifetime': 2,
                'acco_lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sess_lifetime': 1,
                'sess_lifetype': 'days',
                'limit': True,
                'limit_receive': 50,
                'limit_transmit': 50
}

# aa = user_guest.user_guest_profile(**add_profile)

edit_profile = {
                'action': 'edit',
                'profilename': '888',
                'generate': True,
                'generatename': False,
                'generatepassword': True,
                'name_prefix': 'otp',
                'activate_on_login': False,
                'enable_account': False,
                'login_uniqueness': True,
                'account_lifetime': False,
                'acco_lifetime': 3,
                'idle_timeout': True,
                'idle_time': 6,
                'idle_type': 'minutes',
                'acco_lifetype': 'days',
                'prune_on_expiry': False,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sess_lifetime': 2,
                'sess_lifetype': 'hours',
                'limit': True,
                'limit_receive': 60,
                'limit_transmit': 80
}

# aa = user_guest.user_guest_profile(**edit_profile)


profilename = 'nihao'
# aa = user_guest.del_user_guest_profile(profilename)



add_account = {
                'action': 'add',
                'accountname': '999',
                'password': '123pass',
                'activate_on_login': True,
                'enable_guest_service_privilege': True,
                'login_uniqueness': False,
                'account_lifetime': False,
                'acco_lifetime': 2,
                'acco_lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sess_lifetime': 1,
                'sess_lifetype': 'days',
                'limit': True,
                'limit_receive': 50,
                'limit_transmit': 50
}

# aa = user_guest.user_guest_account(**add_account)


edit_account = {
                'action': 'edit',
                'accountname': '999',
                'password': '123pass',
                'activate_on_login': False,
                'enable_guest_service_privilege': False,
                'login_uniqueness': False,
                'account_lifetime': False,
                'acco_lifetime': 2,
                'acco_lifetype': 'days',
                'prune_on_expiry': True,
                'comment': 'Newadd',
                'quota_cycle': 'day',
                'session_lifetime': True,
                'sess_lifetime': 5,
                'sess_lifetype': 'hours',
                'limit': True,
                'limit_receive': 60,
                'limit_transmit': 70
}

# aa = user_guest.user_guest_account(**edit_account)

accountname = '999'
# aa = user_guest.del_user_guest_account(accountname)


