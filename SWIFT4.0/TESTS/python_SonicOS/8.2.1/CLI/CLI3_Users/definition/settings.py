import os
import sys
import re
import time
import copy
import requests
import json
from runner.settings import Params, logger
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'CLI/CLI3_Users/testcases')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'CLI/CLI3_Users')
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Users/testplan/users.json'



from lib.modules.CLI.users import UsersSettingsCli, UsersStatusCli, UserLdapCli, Userlocalcli, UserRadiusCli, UserSSOcli, UserAuthCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.system import CertificateApi
from lib.modules.API.users import LdapApi
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '172.16.1.168'
    MASK = '255.255.255.0'
    X1_GW = '172.16.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    PC2_IP = '172.16.1.101'

# settings in TestConfigFW
local_user_dict = {'user': 'autotest', 'password': 'Sonicwall2026@QA'}
confpath = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_Users/definition/cert'
certpath = confpath + '/dovecot_1k.p12'
x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }

# paramenters on the test case
authen_setting_dict = {'auth-method': 'local',
                  # method:ldap | ldap-local | local | radius | radius-local
                  'login-uniqueness': False,
                  'show-user-status-window': True,
                  'initcmds': ['no login-uniqueness','no show-user-status-window','commit']
                  }
add_auth_bypass_dict = {
    'action': 'add',
    'rule-auth-bypass-http-url': '*.windowsupdate.com'
}
del_auth_bypass_dict = {
    'action': 'delete',
    'no rule-auth-bypass-http-url': '*.windowsupdate.com'
}
combined_auth_dict = {
    'acceptable-use-policy': True,
    'window-size': ['480', '350'],
    'scroll-bars': True,
    'content': '22356',
    'aup-on-zones': ['trusted', 'wan', 'vpn'],
    'customize-login-page': ['preempt', 'test'],
    'auth-page-timeout': '10',
    'case-sensitive-names': True,
    'disconnected-user-detect': True,
    'http-redirect-after-login': True,
    'inactivity-timeout': '40',
    'initcmds': ['no case-sensitive-names', 'no disconnected-user-detect', 'no http-redirect-after-login', 'commit']
}
check_auth_dict = {
    'acceptable-use-policy': False,
    'aup-on-zones': False,
    'auth-page-timeout': False,
    'case-sensitive-names': False,
    'disconnected-user-detect': False,
    'http-redirect-after-login': False,
    'inactivity-timeout': False
}

combined_ldap_dict = {
    'default-user-group': 'Trusted Users',
    'server': '12.3.4.5',
    'primary-domain': 'autodirectory.com',
    'local-tls-certificate': 'dovecot_1k',
    'local-users-only': True,
    'operation-timeout': '19',
    'relay': True,
    'schema': 'samba-smb',
    'user': local_user_dict['user'],
    'passwd': local_user_dict['password'],
    'test': {
        'user-authentication'
    },
    'initcmds': ['no servers', 'no local-tls-certificate', 'no local-users-only', 'relay','no enable', 'exit', 'commit']
}
check_ldap_dict = {
    'default-user-group': False,
    'primary-domain': False,
    'local-tls-certificate': False,
    'local-users-only': False,
    'operation-timeout': False,
    'relay': False,
    'schema': False,
    'server-member': False,
    'server-test': False
}

combined_local_dict = {
    'apply-password-constraints': True,
    'groupmember': local_user_dict['user'],
    'prune-on-expiry': True,
    'initcmds': ['no apply-password-constraints', 'no prune-on-expiry', 'commit']
}
check_local_dict = {
    'apply-password-constraints': False,
    'groupmember': False,
    'prune-on-expiry': False,
    'user-added': False
}

combined_radius_dict = {
    'default-user-group': 'Guest Services',
    'local-users-only': True,
    'retries': '4',
    'serverhost': '1.2.3.4',
    'timeout': '10',
    'user-group-mechanism': 'filter-id',
    'initcmds': ['no local-users-only', 'commit']
}
check_radius_dict = {
'default-user-group': False,
'local-users-only': False,
'retries': False,
'server-host': False,
'timeout': False,
'user-group-mechanism': False
}

combined_sso_dict = {
    'agent': '192.168.11.100 2222',
    'enforce-on-zone': 'LAN',
    'hold-time': 'after-failure 10',
    'local-users-only': True,
    'method sso-agent': True,
    'non-domain-limited-access': True,
    'poll rate': '10',
    'security-services-bypass-dns': 'full-bypass',
    'terminal-services-agent': '192.168.168.100 8888',
    'tsa-services-bypass': True,
    'user-group-mechanism': 'ldap',
    'windows-service-user-name': 'someservice',
    'initcmds': ['no agents', 'no enforce-on-zone LAN', 'no local-users-only', 'no non-domain-limited-access', 'no terminal-services-agents',  'no method sso-agent', 'no tsa-services-bypass', 'user-group-mechanism local-only', 'commit']
}
check_sso_dict = {
'agent': False,
'enforce-on-zone': False,
'hold-time': False,
'local-users-only': False,
'method': False,
'non-domain-limited-access': False,
'poll-rate': False,
'security-services-bypass-dns': False,
'terminal-services-agent': False,
'tsa-services-bypass': False,
'user-group-mechanism': False,
'windows-service-user-name': False

}
security_services_dict = {
    'security-services-bypass-ip': 'full-bypass',
    'initcmds': []}
add_user1_dict = {'user': 'user1', 'password': 'Sonicwall2026@QA'}
add_user2_dict = {'user': 'user2', 'password': 'Sonicwall2026@QA'}
add_group1_dict = {'group': 'group1', 'member': 'user1'}
del_user1_dict = {'no user': 'user1'}
del_user2_dict= {'no user': 'user2'}
del_group1_dict = {'no group': 'group1'}

ldap_allow_references_dict = {'allow-references': 'user-authentication',
                             'initcmds': ['no allow-references user-authentication', 'commit']}

ldap_setting_dict = {'allow-referrals': True,
                             'initcmds': ['no allow-referrals', 'commit']
                             }


#Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

lc = LicenseCli(fw_cli)
interface_obj = InterfaceIPv4Api(fw)

userssettingscli = UsersSettingsCli(fw_cli)
usersstatuscli = UsersStatusCli(fw_cli)
userldapcli = UserLdapCli(fw_cli)
userldapapi = LdapApi(fw)
certapi = CertificateApi(fw)
userlocalcli = Userlocalcli(fw_cli)
userradiuscli = UserRadiusCli(fw_cli)
userssocli = UserSSOcli(fw_cli)
userauthcli = UserAuthCli(fw_cli)

