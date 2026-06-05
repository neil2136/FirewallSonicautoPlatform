import os
import re
import sys
import copy
import json
import time
import unittest
import urllib3
import requests
from requests.auth import HTTPDigestAuth
from collections import OrderedDict

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_App_Control')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/SSO_App_Control/definition')

from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.users import SSOApi, UsersettingApi, UserStatusApi
from lib.modules.API.system import PacketmonitorApi
from lib.modules.API.accessrule import AccessRuleIPv4Api
from lib.modules.API.system import RestartApi, DiagnosticApi
from lib.modules.CLI.users import UsersSettingsCli, UserAuthCli
from lib.modules.API.users import UserLocalApi, LdapApi
from lib.modules.API.policy import AppRulesApi
from lib.modules.CLI.system import LicenseCli
from lib.modules.API.object import MatchPatternApi,CustomMatchApi
from lib.modules.API.network import InterfaceIPv4Api



class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    sso_server = "192.168.168.65"
    client = "192.168.168.65"
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_App_Control/testplan/testplan.json'

G_PASSWORD_NEW = Params.G_NEW_PASSWORD

ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')


url = "https://192.168.168.168" 
user = "admin" 
pwd = G_PASSWORD_NEW


os_obj = Openstack(Params.testbed)
LAN_HOST = Host(os_obj.get_node_interface_ip("PC1","eth0"))
WAN_HOST = Host(os_obj.get_node_interface_ip("PC2","eth1"))

license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
user_sso = SSOApi(fw_api)
packet = PacketmonitorApi(fw_api)
user_setting = UsersettingApi(fw_api)
user_status = UserStatusApi(fw_api)
accessrule = AccessRuleIPv4Api(fw_api)
usersettingcli = UsersSettingsCli(fw_cli)
userauthcli = UserAuthCli(fw_cli)
tsr = DiagnosticApi(fw_api)
user_ldap = LdapApi(fw_api)
user_local = UserLocalApi(fw_api)
apprule = AppRulesApi(fw_api)
match_obj=CustomMatchApi(fw_api)
match_object = MatchPatternApi(fw_api)
interface = InterfaceIPv4Api(fw_api)
logger.info("The Firewall LAN IP is {}".format(ip))
WAN_IP = Parameter.X1_IP
logger.info("Wan IP is {}".format(WAN_IP))
localhost = Host('localhost')
static_pc = Params.testbed + '-PC2'
static_client = Host(static_pc)

http_object = {
    "match_objects":[{
        "name":"http",
        "type":"http-url",
        "content_entry":[{"content_entry":"url"}],
        "match_type":"partial",
        "input_representation":"alphanumeric"
        }]}

ftp_object = {
            "match_objects":[{
                "name":"ftp",
                "type":"file-name",
                "content_entry":[{"content_entry":"ftp"}],
                "match_type":"partial",
                "input_representation":"alphanumeric",
                "negative_matching":False
       }]}
 

http_rule_policy = {
  "app_rules": {
    "policy": [
      {
        "name": "web_access_policy",
        "enable": True,
        "type": {
          "http": "client"
        },
        "source": {
          "service": {
            "any": True
          },
          "address": {
            "any": True
          }
        },
        "destination": {
          "service": {
            "name": "HTTP"
          },
          "address": {
            "any": True
          }
        },
        "exclusion": {
          "address": {},
          "service": {}
        },
        "match_object": {
          "included": "http",
          "excluded": ""
        },
        "action_object": "Reset/Drop",
        "users": {
          "included": {
            "all": True
          },
          "excluded": {}
        },
        "schedule": {
          "always_on": True
        },
        "flow_reporting": False,
        "logging": True,
        "log": {
          "individual": False,
          "redundancy": {
            "global": True
          }
        },
        "connection_side": "client",
        "direction": {
          "basic": "incoming"
        }
      }
    ]
  }
}

ftp_rule_policy = {
  "app_rules": {
    "policy": [
      {
        "name": "ftp_policy",
        "enable": True,
        "type": {
          "ftp": "client-download"
        },
        "source": {
          "service": {
            "any": True
          },
          "address": {
            "any": True
          }
        },
        "destination": {
          "service": {
            "name": "FTP Control"
          },
          "address": {
            "any": True
          }
        },
        "exclusion": {
          "address": {},
          "service": {}
        },
        "match_object": {
          "object": "ftp"
        },
        "action_object": "Reset/Drop",
        "users": {
          "included": {
            "all": True
          },
          "excluded": {}
        },
        "schedule": {
          "always_on": True
        },
        "flow_reporting": False,
        "logging": True,
        "log": {
          "individual": False,
          "redundancy": {
            "global": True
          }
        },
        "connection_side": "client",
        "direction": {
          "basic": "incoming"
        }
      }
    ]
  }
}

