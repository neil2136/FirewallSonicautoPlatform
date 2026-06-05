import sys
import os
sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
# sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
import modules.CLI.users
from utm import Firewall


ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')


###################################User Status######################################

userstatus = modules.CLI.users.UsersStatusCli(fw)


# aa = userstatus.show_users_status()

show_user_status = {
    'show_type': 'name',
    'show_username': 'test',
    # 'show_type': 'cli',
    # 'show_type': 'at',
    # 'at': '192.168.168.168',
}

# aa = userstatus.show_user_status_detailed(**show_user_status)

# aa = userstatus.show_unauthenticated_users()

# aa = userstatus.show_inactive_users()

status_setting = {
                 'include inactive-users': True,
                 'include unauthenticated-users': True
}

# aa = userstatus.status_setting(**status_setting)


usersname = 'guest1'

# aa = userstatus.logout_local_users_name(usersname)


usersip = '192.168.168.1'

# aa = userstatus.logout_local_users_ip(usersip)


###################################User Settings######################################

usersetting = modules.CLI.users.UsersSettingsCli(fw)


authen_setting = { 'method': 'ldap',
                # method:ldap | ldap-local | local | radius | radius-local
                'case-sensitive-names': True,
                'login-uniqueness': True,
                'relogin-after-password-change': True,
                'one-time-password email-format': 'html',
                'one-time-password format': 'characters',
                'one-time-password length': ['4','9']
}

# aa = usersetting.authen_setting(**authen_setting)


weblogin_setting_dict = { 'auth-page-timeout': '10',
                          'browser-redirect-via': 'interface-ip',
                   # browser-redirect-via: host-name | interface-ip | name-from-certificate|reverse-dns
                          'http-redirect-after-login': True
}

# aa = usersetting.weblogin_setting(**weblogin_setting_dict)

                     
auth_bypass_dict = { 
                   # 'action': 'add',
                   # 'rule-auth-bypass-http-url': 'www.163.com',
                   'action': 'delete',
                   'no rule-auth-bypass-http-url': 'www.163.com',
}

# aa = usersetting.auth_bypass(**auth_bypass_dict)


user_sessions_dict = { 'inactivity-timeout': '26',
                       'prevent-inactivity-logout service': ['group', 'ICMP'],
                       'log-user-name': ['bypass-sso', 'oriExternUser'],
                       'user-connections-logout inactivity': ['authentication',['terminate after','8']],
                       'user-connections-logout reported': ['other','keep-alive'],
                       'show-user-status-window': '50',
                       # 'show-user-status-window': False,
                       # 'disconnected-user-detect': '80',
                       'disconnected-user-detect': False,
                       'inactive-user login': True,
                       'inactive-user timeout': True,
                       'age-out': '25',
                       'web-login-session-limit': '15',
                       'open-in-same-window': True                     
}   

# aa = usersetting.user_sessions(**user_sessions_dict)
                      
user_customization_dict = { 'policy-banner': True,
                            'policy-banner content': '123456',
                            'window-size': ['480', '350'],
                            'scroll-bars': True,
                            'content': '22356',
                            'acceptable-use-policy': True,
                            'aup-on-zones': ['trusted', 'wan', 'vpn'],
                            'customize-login-page': ['preempt', 'test']
}

# aa = usersetting.user_customization(**user_customization_dict)

###################################Radius server and Radius accounting Settings######################################

userradius = modules.CLI.users.UserRadiusCli(fw)


radius_server_setting = {  
                    'timeout': '10',
                    'retries': '5',
                    'local-users-only': True,
                    'user-group-mechanism': 'ldap',
                    'default-user-group': 'Guest Services',
                # default-user-group:SonicWALL Administrators/Content Filtering Bypass
                # /Limited Administrators/SSLVPN Services/SonicWALL Read-Only Admins/
                # Guest Services/Everyone/Guest Administrators/Trusted Users
}

# aa = userradius.radius_server_settings(**radius_server_setting)


add_radius_server_dict = { 
                       'action': 'add',
                       'server': '1.2.3.4',
                       'enable': True,
                       'host': '192.168.168.1',
                       'port': '1819',
                       'shared-secret': '123password',
                       'user-name-format': 'user-name',
# user-name-format:down-level-logon/name-dot-domain/user-name/user-principle
                       'send-through-vpn-tunnel': True
}

# aa = userradius.radius_server(**add_radius_server_dict)


edit_radius_server = {
                       'action': 'edit',
                       'server': '192.168.168.1',
                       'enable': False,
                       'host': '4.3.2.1',
                       'port': '1819',
                       'shared-secret': '123password',
                       'user-name-format': 'user-principle',
# user-name-format:down-level-logon/name-dot-domain/user-name/user-principle
                       'send-through-vpn-tunnel': True
}

# aa = userradius.radius_server(**edit_radius_server)


test_radius_server = {'testmethod': 'authentication',
                      'radiusserver': '4.3.2.1',
                      'username': 'user1',
                      'password': 'pwd1234'
}

# aa = userradius.test_radius_server(**test_radius_server)


radiusserver = '4.3.2.1'

# aa = userradius.del_radius_server(radiusserver)

###########Delete all radius servers#######

# aa = userradius.del_all_radius_servers()


radius_accounting_settings = {
                     'data': 'all-servers',
                     'include': 'domain-users',
                     'interim-updates': '15',
                     'timeout': '10',
                     'retries': '5'
}

# aa = userradius.radius_accounting_settings(**radius_accounting_settings)

add_radius_accounting = { 
                       'action': 'add',
                       'server': '1.2.3.4',
                       'enable': True,
                       'host': '192.168.168.1',
                       'port': '1819',
                       'shared-secret': '123password',
                       'user-name-format': 'user-name',
# user-name-format:down-level-logon/name-dot-domain/user-name/user-principle
}

# aa = userradius.radius_accounting_server(**add_radius_accounting)


edit_radius_accounting = {
                       'action': 'edit',
                       'server': '192.168.168.1',
                       'enable': False,
                       'host': '4.3.2.1',
                       'port': '1819',
                       'shared-secret': '123password',
                       'user-name-format': 'user-principle',
# user-name-format:down-level-logon/name-dot-domain/user-name/user-principle
}

# aa = userradius.radius_accounting_server(**edit_radius_accounting)

accountingserver = '4.3.2.1'

# aa = userradius.del_radius_accounting_server(accountingserver)

###########Delete all radius accounting servers#######

# aa = userradius.del_all_radius_accounting_servers()

test_radius_accounting_server = {
                      'testmethod': 'useraccounting',
                      'radiusserver': '4.3.2.1',
                      'username': 'user1',
                      'specifiedserver': '1.1.1.1'

}

# aa = userradius.test_radius_accounting_server(**test_radius_accounting_server)


#############################Ldap Settings#################################

userldap = modules.CLI.users.UserLdapCli(fw)


ldaptest_dic = {
               'server': Parameter.SERVER,
               'test':'user-authentication',
               'user': Parameter.USER,
               'passwd': Parameter.PASSWORD
        }
    

ldap_setting = {
                      'require-valid-certificate': True,
                      'protocol-version': '3',
                      'allow-referrals': True,
                      'allow-references': 'domain-search',
                      'local-users-only': True,
                      'default-user-group': '"SSLVPN Services"',
                      'mirror-user-groups': 'refresh',
                      'mirrorrefresh': '9',
                      'exclude-tree' :'mydomain.com/groups',
                      'relay': True,
                      'enable': True,  # Enable RADIUS to LDAP Relay
                      'shared-secret': '123pass',
                      'clients-connect': ['wan-zone', 'vpn-zone'],
                      'legacy-user-group': ['vpn', 'aaa']
}

aa = userldap.ldap_settings(**ldap_setting)


add_ldap_server_dict = { 'server' : '192.168.99.88',
                     'timeout operation' : '10',
                     'use-tls' : False,
                     'bind': ['name', 'administrator', 'location', 'builtin'],
                     'bind-password': 'password'
}
add_authen_partition_dict = {'enable': True,
                             'partition': '888',
                             'name': '333',
                             'domain': 'ddd.com',
                             'comment': '"new add"'
}
edit_authen_partition_dict = {'enable': True,
                         'partition': '111',
                         'name': 'newadd',
                         'domain': 'newadddomain.com',
                         'comment': 'editparti'
}
delete_authen_partition_dict = {


}
add_partition_policy_dict = {'enable': True,
                             'policy': True,
                             'interface_init': 'X0',
                             'comment': 'new policy',
                             'zone': 'DMZ',
                             'partition': '222',
                             'interface_init': 'X2'
}
sso_agent_dict = {'agent': '1.2.3.4',
                      'enable': True,
                      'port': '1819',
                      'retries': '15',
                      'max-requests': '20',
                      'timeout': '10',
                      'shared-key': '123abc',
                      'next-agent-on-no-name': True,
                      'no block-traffic': True,
                      'including-for-access-rules': 'all',
                      'windows-service-user-name': 'someservice'
}
config_enforce_dict = {'enforce-on-zone': ['LAN', 'DMZ', 'VPN'],
                    'service_group': 'MSN',
                    'type': 'full-bypass',
                    'dummy-user name': 'test111'
}
sso_user_setting = { 'local-users-only': True,
                     'non-domain-limited-access': True,
                     'user-group-mechanism': 'ldap',
                     'poll rate': '10',
                     'poll same-agent': True,
                     'hold-time after-failure': '10',
                     'hold-time after-no-user': '10'
}
sso_terminalservices = { 'tsa-services-bypass': True,
                         'method terminal-services-agent': True,
                         'terminal-services-agent': '55.6.9.8',
                         'host': '9.8.7.6',
                         'port': '2296',
                         'enable': True,
                         'shared-key': '1234abcd'
}
sso_radiusaccounting = { 'radius-accounting-client': '4.56.6.8',
                         'host': '88.55.6.7',
                         'log-user-out': '5',
                         'user-name-format': 'user-name',
                         'shared-secret': '1234abcd',
                         'proxy-forward timeout': '6',
                         'proxy-forward retries': '5',
                         'server': ['1', '192.168.168.11', '1813', '123abc']
}
sso_test = { 'method': True,
             'agent': ['1.2.3.4', 'user-ip', '192.168.168.99'] # The sso agent must be created first, otherwise you can't test it, error will appear
}
add_local_user = {'user': 'test',
                  'domain': 'example.com',
                  'password': '123password',
                  'expiration': '2020:12:31 23:59',
                  'force-password-change': True,
                  'one-time-password': 'totp',
                  'email-address': 'example@sonicwall.com',
                  'comment': '"Added 7/26/2019"',
                  'member-of' :'"SonicWALL Administrators"',
                  'uuid': 'f40b27d6-b8b9-a4fc-0500-c0eae49ce84c',
                  'prune-on-expiry': True,
                  'session-lifetime': ['48', 'hours'],
                  'unbind-totp-key': True,
                  'quota-cycle': 'month',
                  'receive': '500',
                  'transmit': '300',
                  'vpn-client-access': '"U0 IP"'
}
edit_local_user = {'user': 'test',
                  'name': 'newuser',
                  'domain': 'example.com',
                  'changedomain': 'changedomain.com',
                  'password': '124pass',
                  'expiration': '2019:10:31 23:59',
                  'email-address': 'editexample@sonicwall.com',
                  'comment': '"Added 7/20/2019"',
                  'member-of' :'"SonicWALL Administrators"',
                  'uuid': 'f40b27d6-b8b9-a4fc-0500-c0eae49ce84c',
                  'receive': '200',
                  'transmit': '600',
                  'bookmark': 'testbm',
                  'bmuserhost': '1.3.5.7',          # bmuserhost must be specified
                  'bmusername': 'bkadd',
                  'bmuserservice': 'rdp',
                  'colors': '24bit',
                  'screen-size': '1024x768',
                  'application-path': '"C:\\\\Remote Applications\\\\myapp.exe"',
                  'start-in-folder': '"C:\\Work"',
                  'redirect-clipboard': True,
                  'custom': ['name', '123', 'password', '123abc', 'domain', '111.com']
}
delete_local_user = { 'no user': 'test',
                      'domain': 'example.com',
                      'no users': True
}
add_local_group = {'group': 'aaaa',
                   'comment': '06/27',
                   'domain': 'example.com',
                   'one-time-password': 'totp',
                   'member': 'Limited\ Administrators',
                   'uuid': 'f40b27d6-b8b9-a4fc-0500-c0eae49ce84c',
                   'vpn-client-access': '"U0 IP"'
                   # 'ldap-location': ['domain.com/users', 'at']
}
edit_local_group = { 'group': 'aaaa',
                     'name': 'test',
                     'comment': '06/45',
                     'domain': 'example.com',
                     'changedomain': 'changedomain.com',
                     'bookmark': 'booktest',
                     'bmgrouphost': '1.2.3.4',
                     'bmgroupname': 'newbookmark',
                     'bmgroupservice': 'rdp',
                     'colors': '24bit',
                     'screen-size': '1024x768',
                     'auto-reconnection': True,
                     'custom': ['name', '123', 'password', '123abc', 'domain', '111.com']
}
delete_local_group = { 'no group': 'test',
                       'domain': 'changedomain.com',
                       'no groups': True
}
add_guest_profile = { 'profile': '666',
                      'show-guest-status-window': True,
                      'activate-on-login': True,
                      'comment': '"Today add"',
                      'limit receive': '200',
                      'limit transmit': '300',
                      'enable': True,
                      'generate': 'password',
                      'login-uniqueness': True,
                      'name-prefix': 'guest',
                      'prune-on-expiry': True,
                      'quota-cycle': 'month',
                      'session-lifetime': ['48', 'hours'],
                      'idle-timeout': ['20', 'minutes']
}
edit_guest_profile = { 'profile': '666',
                       'name': '888888',
                      'show-guest-status-window': False,
                      'activate-on-login': False,
                      'comment': '"Today add"',
                      'limit receive': '200',
                      'limit transmit': '300',
                      'enable': False,
                      'generate': 'password',
                      'login-uniqueness': False,
                      'name-prefix': 'guestedit',
                      'prune-on-expiry': True,
                      'quota-cycle': 'month',
                      'session-lifetime': ['24', 'hours'],
                      'idle-timeout': ['10', 'minutes']
}
delete_guest_profile = {'no profile': '111'
}
add_guest_account = { 'user': '777',
                      'hide-password': True,
                      'activate-on-login': True,
                      'comment': '"Today add"',
                      'limit receive': '200',
                      'limit transmit': '300',
                      'enable': True,
                      'generate': 'password',
                      'login-uniqueness': True,
                      'profile': 'Default',
                      'prune-on-expiry': True,
                      'quota-cycle': 'month',
                      'session-lifetime': ['48', 'hours'],
                      'idle-timeout': ['20', 'minutes']
}
edit_guest_account = { 'user': 'guest19532',
                       'name': '888888',
                      'changepassword': '123abc',
                      'activate-on-login': False,
                      'comment': '"Today add"',
                      'limit receive': '200',
                      'limit transmit': '300',
                      'enable': False,
                      'generate': 'password',
                      'login-uniqueness': False,
                      'prune-on-expiry': True,
                      'quota-cycle': 'month',
                      'session-lifetime': ['24', 'hours'],
                      'idle-timeout': ['10', 'minutes']
}
delete_guest_account = {'no user': '888888',
                        'no users': 'temp-guest'    # Delete all guest user accounts with a given name prefix.
}
generate_guest_account = {'number': '2',
                          'profile': 'temp-guest'
}





userpartition = modules.CLI.users.UserPartitioncli(fw)
usersso = modules.CLI.users.UserSSOcli(fw)
userlocal = modules.CLI.users.Userlocalcli(fw)
guestservice = modules.CLI.users.GuestServicecli(fw)
guestaccount = modules.CLI.users.GuestAccountcli(fw)


# aa = userldap.add_ldap_server(**add_ldap_server_dict)
# bb = userpartition.add_authen_partition(**add_authen_partition_dict)
# cc = userpartition.partition_policy(**add_partition_policy_dict)
# dd = usersso.sso_agent(**sso_agent_dict)
# ee = usersso.enforcement(**config_enforce_dict)
# ff = userldap.ldap_setting(**ldap_setting_dict)
# hh = usersso.users(**sso_user_setting)
# ii = usersso.terminalservices(**sso_terminalservices)
# jj = usersso.radiusaccounting(**sso_radiusaccounting)
# kk = usersso.test(**sso_test)
# ll= userlocal.add_local_user(**add_local_user)
# mm = userlocal.edit_local_user(**edit_local_user)
# qq = userlocal.delete_local_user(**delete_local_user)
# nn = userlocal.add_local_group(**add_local_group)
# oo = userlocal.edit_local_group(**edit_local_group)
# pp = userlocal.delete_local_group(**delete_local_group)
# qq = guestservice.add_guest_profile(**add_guest_profile)
# rr = guestservice.edit_guest_profile(**edit_guest_profile)
# ss = guestservice.delete_guest_profile(**delete_guest_profile)
# tt = guestaccount.add_guest_account(**add_guest_account)
# uu = guestaccount.edit_guest_account(**edit_guest_account)
# vv = guestaccount.delete_guest_account(**delete_guest_account)
# wwww = userpartition.edit_authen_partition(**edit_authen_partition_dict)
# yyy = guestaccount.generate_guest_account(**generate_guest_account)
















