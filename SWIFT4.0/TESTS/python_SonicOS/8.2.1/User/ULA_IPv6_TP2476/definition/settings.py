import os
import sys
import json
import time
import threading
import re
import argparse
from pexpect import pxssh
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/definition')


from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from utm import Firewall 
from networkdevice import Host
from lib.modules.API import network
from lib.modules.API.sslvpn import SSLVPNServerSettingsAPI
from lib.modules.API import users
from modules.ui.ui_wrapper import Browser
from lib.modules.ui.fw_page import FWPage
from lib.modules.API import log
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.accessrule import Access_Rule
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.firewall import AccessRuleIPv6Api
from ui.ui_ula import UIULA
from ui.ui_fw import FWUI
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

class Parameter():
    FIREWALL = '192.168.168.168'
    X0_SUBNET = '192.168.168.0'
    X0_IPV6_SUBNET = '2001:db0::'
    X0_IPV6 = '2001:db0::193'
  
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3 

    X1_IPV6 = '2001:db1::193'

    PC1_ETH0_IP = '192.168.168.100'
    PC1_ETH0_IPV6 = '2001:db0::1096'
    PC2_ETH0_IPV6 = '2001:db0::1097'

    SSLVPN_Server = '13.0.0.10:4433'

    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/ULA_IPv6_TP2476/testplan/testplan.json'

    X2_IP = '192.168.3.168'
    X2_GW = '192.168.3.1'
    X2_SUBNET = '192.168.3.0'
    X2_IPV6 = '2001:db3::193'
    X2_IPV6_SUBNET = '2001:db3::'

    X3_IP = '12.12.3.168'
    X3_GW = '12.12.3.1'
    X3_SUBNET = '12.12.3.0'
    X3_IPV6 = '2001:db4::193'
    X3_IPV6_SUBNET = '2001:db4::'

    PC1_ETH0_IPV6_EXPANDED = '2001:db0:0:0:0:0:0:1096'
    PC3_ETH0_IPV6 = '2001:db3::1098'
    PC4_ETH0_IPV6 = '2001:db4::1099'


fw_api = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto',  supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password='sonicauto', supported_config_mode='cli-ssh')

license = LicenseCli(fw_cli)
interface_ipv4 = network.InterfaceIPv4Api(fw_api)
interface_ipv6 = network.InterfaceIPv6Api(fw_api)
user_local = users.UserLocalApi(fw_api)
user_status = users.UserStatusApi(fw_api)
user_settings = users.UsersettingApi(fw_api)
logcategory_api = log.LogCategoryApi(fw_api)
sslvpnserver = SSLVPNServerSettingsAPI(fw_api)

log_monitor = log.LogMonitorApi(fw_api)
log_settings = log.LogSettingsApi(fw_api)
log_category = log.LogCategoryApi(fw_api)
admin_api = system.AdminApi(fw_api)
diag_api = system.DiagnosticApi(fw_api)
access_rules = Access_Rule(fw_api)
zone_api = network.ZoneObjectsApi(fw_api)
access_rules_ipv4 = AccessRuleIPv4Api(fw_api)
access_rules_ipv6 = AccessRuleIPv6Api(fw_api)

ui_ula = UIULA()
ui_fw = FWUI()
static_pc1 = Params.testbed + '-PC1'
pc1 = Host(static_pc1)
static_pc2 = Params.testbed + '-PC2'
pc2 = Host(static_pc2)
static_pc3 = Params.testbed + '-PC3'
pc3 = Host(static_pc3)
static_pc4 = Params.testbed + '-PC4'
pc4 = Host(static_pc4)

user_setings =  {
 "user": {
  "auth": {
   "inactivity_timeout": 15,
   "prevent_inactivity_logout": {
    "service": {}
   },
   "log_user_name": {
    "originating_externally": "",
    "other_unidentified": "",
    "sso_fail": "Unknown (SSO failed)",
    "bypass_sso": "Unknown (SSO bypassed)"
   },
   "user_connections_logout": {
    "inactivity": {
     "authentication": {
      "keep_alive": True
     },
     "other": {
      "keep_alive": True
     }
    },
    "reported": {
     "authentication": {
      "terminate": {
       "now": True
      }
     },
     "other": {
      "terminate": {
       "after": 15
      }
     }
    }
   },
   "inactive_user": {
    "login": True,
    "timeout": True
   },
   "age_out": 60,
   "show_user_status_window": True,
   "disconnected_user_detect": True,
   "status_window_heartbeat": {
    "period": 120,
    "timeout": 10
   },
   "open_in_same_window": False,
   "web_login_session_limit": 2
  }
 }
}