import os
import sys
import re
import copy
import time
import json

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from modules.API import network, firewall, system, users, object, log
from lib.modules.CLI.users import UsersStatusCli
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.system import DiagnosticApi, StatusApi

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2')
from definition.fwpage_ui import FWPage_UI

FIREWALL = '192.168.168.168'
PC2 = '192.168.168.85'
radius_client = '192.168.168.85'
radius_client_fail = '192.168.168.103'
radius_client_user1 = '192.168.100.124'
radius_client_user2 = '192.168.100.125'
radius_client_userip_mior1 = '192.168.100.123'

DUTX1 = '12.12.1.200'
Gateway = '12.12.1.1'
REMOTEX1 = '12.12.1.201'
MASK = '255.255.255.0'

account_ip = '8.8.3.3'
new_account_ip = '11.3.3.3'
Hostname = 'NewRadiusAccount'
forwarding_server_pwd = "password"

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_by_Radius_Accounting_2/testplan/SSO_by_Radius_Accounting.json'

G_NEW_PASSWORD = Params.G_NEW_PASSWORD
fw = Firewall(FIREWALL, user='admin', password=G_NEW_PASSWORD, supported_config_mode='api')
fw_remote = Firewall(REMOTEX1, user='admin', password=G_NEW_PASSWORD, supported_config_mode='api')

fw_cli = Firewall(FIREWALL, user='admin', password=G_NEW_PASSWORD, supported_config_mode='cli-ssh')
fw_cli_remote = Firewall(REMOTEX1, user='admin', password=G_NEW_PASSWORD, supported_config_mode='cli-ssh')

diag_obj = DiagnosticApi(fw)
user_status_cli = UsersStatusCli(fw_cli)
user_status_cli_remote = UsersStatusCli(fw_cli_remote)
user_auth_partition = users.AuthPartitionsApi(fw)
user_status = users.UserStatusApi(fw)
user_sso_obj_remote = users.SSOApi(fw_remote)
tsr_obj = system.DiagnosticApi(fw)
interface_ipv4 = network.InterfaceIPv4Api(fw)
user_settings_obj = users.UsersettingApi(fw)
user_sso_obj = users.SSOApi(fw)
user_local_obj = users.UserLocalApi(fw)
ldap_obj = users.LdapApi(fw)
user_status = users.UserStatusApi(fw)
log_config = log.LogCategoryApi(fw)
zone_obj = network.ZoneObjectsApi(fw)
access_rules_obj = firewall.AccessRuleApi(fw)
ao_obj = network.AddressobjectsApi(fw)
status_api = StatusApi(fw)
ag_obj = object.AddressObjectGroupApi(fw)
so_obj = network.ServiceObjectApi(fw)
sg_obj = network.ServiceGroupApi(fw)
log_obj = log.LogMonitorApi(fw)
ui_obj = FWPage_UI(FIREWALL, "admin", G_NEW_PASSWORD)

logout_user1 = {
    "killusers": [{
        "ip": radius_client_user1,
        "inactive": True
    }]
}

logout_user2 = {
    "killusers": [{
        "ip": radius_client_user2,
        "inactive": True
    }]
}
re_user_name = "[AUDIT].*Index=\"8.8.3.3\".*Description=\" \'User-Name attribute format\' \".*New=\"User-name\""
re_interim = "[AUDIT].*Index=\"8.8.3.3\".*Description=\" \'Interim-Update timeout control\' \".*New=\"2\""
re_shared_secret = "[AUDIT].*Index=\"8.8.3.3\".*Description=\" \'Radius Accounting Client Shared Secret\' \""
re_host = "[AUDIT].*Index=\"8.8.3.3\".*Description=\"Added \'RADIUS Accounting Host name.*IP address\' \".*New=\"8.8.3.3\""
sso_radius_accounting_client_json = {
    "user": {
        "sso": {
            "radius_accounting_client": [
                {
                    "host": "10.10.10.10",
                    "shared_secret": "password",
                    "log_user_out_if_no_interim": {
                        "auto": True
                    },
                    "log_user_out_timeout": 0,
                    "proxy_forward": {
                        "timeout": 10,
                        "retries": 3
                    },
                    "server": [
                        {
                            "serverId": 1,
                            "name": "10.10.10.102",
                            "port": 1812,
                            "shared_secret": forwarding_server_pwd
                        },
                        {
                            "serverId": 2,
                            "name": "10.10.10.12",
                            "port": 1813,
                            "shared_secret": forwarding_server_pwd
                        },
                        {
                            "serverId": 3,
                            "name": "0.0.0.0",
                            "port": 1814,
                            "shared_secret": forwarding_server_pwd
                        },
                        {
                            "serverId": 4,
                            "name": "0.0.0.0",
                            "port": 1815,
                            "shared_secret": forwarding_server_pwd
                        }
                    ]
                }
            ]
        }
    }
}
