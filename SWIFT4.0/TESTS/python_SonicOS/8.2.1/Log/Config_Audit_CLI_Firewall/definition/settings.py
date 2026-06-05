import os
import sys
import re
import time
import copy
import unittest
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test,repeat_method
from runner.utils.assertion import Assertion
from runner.unittest.suite import UnittestSuite
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from util.enhancedinfo import show_testcase_info
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API import network,vpn,firewall,system,log,securityservices
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.log import ClearlogCli
# from util.dpissl.lib.mail_server import StartMailServer
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Firewall')

OpenS = Openstack(Params.testbed)
MASK = '255.255.255.0'
DUT_X0 = '192.168.168.168'
DUT_X1 = '13.0.0.10'
DUT_X1_GW = '13.0.0.1'
DUT_X2 = '23.0.0.10'
DUT_X3 = '12.12.1.200'
Remote_X0 = '172.16.1.101'
Remote_X1 = '12.12.1.201'
# pc1_ip = "192.168.168.200"
pc1_ip = OpenS.get_node_interface_ip('PC1','eth0')
logger.info(f'-----pc1 ip----------{pc1_ip}')
pc2_ip = "13.0.0.5"
pc3_ip = "172.16.1.168"
PC2_Network = '13.0.0.0'
PC1_Network = '192.168.168.0'
PC3_Network = '172.16.1.0'
DUT_Network = '12.12.1.0'
PC1_IF = 'eth0'
PC2_IF = 'eth1'
LOCALSUBNET = "X0 Subnet"
REMOTESUBNET = "X0 Subnet"
PC2 = Host('15.0.0.4', user='root', password='password')
PC1 = Host(pc1_ip, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Firewall/testplan/Config_Audit_CLI_Firewall.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Firewall/confs/'

fw_api = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
Linterface = network.InterfaceIPv4Api(fw_api)
LAddrOBJ = network.AddressobjectsApi(fw_api)
snmp_obj = system.SNMPApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw_api)
audit_logobj = log.AuditlogMonitorApi(fw_api)
logsetting_obj = log.LogSettingsApi(fw_api)
log_category = log.LogCategoryApi(fw_api)
diag_obj = system.DiagnosticApi(fw_api)
GAV_settings = securityservices.GAV(fw_api)
# clear_log = ClearlogCli(fw_cli)

pc1_route_cmds = [f'ip r a {PC2_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  "ip route"]
pc2_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X1} dev {PC2_IF}',
                  "ip route"]


modify_email = ["config","email-object test_email","match-type  regex","content-entry test_conten1","commit","match-type exact","commit","exit"]
del_email = ["config","no email-object test_email","commit","exit"]
modify_uri_obj = ["config","content-filter","uri-list-object name test_list_obj","type keyword","keyword www","keyword baidu","commit","type uri","commit","end"]
del_uri_obj = ["config","content-filter","no uri-list-object name test_list_obj","commit","end"]
modify_uri_group = ["config","content-filter","uri-list-object test1","type keyword","keyword www","commit","exit",
                    "uri-list-group test_uri_grp","uri-list-object test1","commit","name test_uri_list","commit","end"]
del_uri_group = ["config","content-filter","no uri-list-group test_uri_list","commit","no uri-list-object name test1","commit","exit"]

modify_cfs_action = ["config","content-filter","action test_action","flow-reporting","commit","no flow-reporting","commit","end"]
del_cfs_action = ["config","content-filter","no actions","commit","end"]
modify_cfs_profile = ["config","content-filter","profile test_profile","uri-list forbidden-operation block","commit","uri-list forbidden-operation passphrase","commit","end"]
del_cfs_profile = ["config","content-filter","no profile test_profile","commit","end"]

modify_cfs_policy = ["config","content-filter","action test_action","flow-reporting","commit","exit","profile test_profile","https-filtering","commit","exit","cfs",
                     "policy test_ploicy","action test_action","profile test_profile","source zone All-ZONES","destination zone All-ZONES","commit","schedule name Work\ Hours","commit","end"]
del_cfs_policy = ["config","content-filter","cfs","no policy test_ploicy","commit","exit","no actions","no profile test_profile","commit","end"]
enable_cfs_plicy = ["config","content-filter","cfs","policy CFS\ Default\ Policy","no enable","commit","enable","commit","end"]

modify_acl_v6 = ["config","access-rule ipv6 from  LAN to any action allow ","service any","commit","name test_acl","commit","end"]
del_acl_v6 = ["config","no access-rule ipv6 from LAN to any action allow","commit","exit"]
modify_acl_v4 = ["config","access-rule ipv4 from  LAN to any action allow ","service any","commit","service name BGP","commit","end"]
enable_acl_v4 = ["config","access-rule ipv4 from  LAN to any action allow service name BGP","no enable","commit","enable","commit","end"]
del_acl_v4 = ["config","no access-rule ipv4 from LAN to any action allow service name BGP","commit","exit"]
modify_match_obj = ["config","match-object test_match","type web-browser","browser netscape","commit","browser firefox","commit","name match_modify","type http-host",
                    "match-type partial","input-representation  alphanumeric","content-entry  modify","commit","exit"]
modify_app_list = ["config","match-object test","type application-list","application category name VPN app name X-VPN","commit","application category name P2P app name  eMule","commit","exit"]
del_match_obj = ["config","no match-objects","commit","exit"]
modify_app_rule1 = ["config","app-rules","policy test_policy","exclusion address name 192.168.168.200","exclusion service name 6over4","match-object included test","match-object excluded test",
                      "users excluded group SSLVPN\ Services","commit","destination address name test_syslog","name test_modify","commit","end"]
modify_app_rule2 = ["config","app-rules","policy test_modify","users excluded group Guest\ Administrators","commit","end"]
del_app_policy = ["config","app-rules","no policy test_modify","commit","end"]

modify_control_settings = ["config","app-control","enable","commit","no enable","commit","end"]
modify_category_settings = ["config","app-control","category name GAMING","log global","commit","no log","commit","end"]
modify_action_obj = ["config","action-object test_action","action http-block-page","content 'www'","color red","commit","color blue","commit","end","exit"]
del_action_obj = ["config","no action-objects","commit","exit"]
modify_addr_v4 = ["config","address-object ipv4 name test_addr_v4 host 1.2.3.4 zone WAN","commit","address-object ipv4 test_addr_v4 zone LAN","commit","end","exit"]
del_addr_v4 = ["config","no address-object ipv4 test_addr_v4","commit","exit"]
modify_addr_v6 = ["config","address-object ipv6 name test_addr_v6 host 2001::193 zone WAN","commit","address-object ipv6 test_addr_v6 zone VPN","commit","end","exit"]
del_addr_v6 = ["config","no address-object ipv6 test_addr_v6","commit","exit"]
modify_addr_group=["config","address-group ipv6 name test_addr_grp","address-group ipv6 LAN\ IPv6\ Subnets","commit","address-object ipv6 IPv6\ Link-Local\ Subnet","commit","end"]
del_addr_group = ["config","no address-group ipv6 test_addr_grp","commit","exit"]
modify_service_grp = ["config","service-group name test_service","service-group VNC","commit","service-object  BGP","commit","end","exit"]
del_service_grp = ["config","no service-group test_service","commit","exit"]
modify_bdw_obj = ["config","bandwidth-object test_bdw","action drop","maximum kbps 1000","commit","maximum kbps 5000","commit","end","exit"]
modify_bdw_obj2 = ["config","bandwidth-object test_bdw2","action drop","maximum kbps 1000","commit","action delay","commit","end","exit"]
del_bdw_obj = ["config","no bandwidth-object test_bdw","commit","exit"]
del_bdw_obj2 = ["config","no bandwidth-object test_bdw2","commit","exit"]

wrong_cmd = ["config","access-rule ipv4 from  LAN to any action allow","commit","priority manual 366","commit","end"]
del_acl = ["config","no access-rule ipv4 from LAN to any action allow ","commit","exit"]
log_group = {
    "log":{
        "group":[
            {
                "id":95,
                "name":"Configuration Auditing",
                "priority_level":"alert",
                "log_monitor":{
                    "type":"enabled",
                    "redundancy_interval":{}
                    },
                "email_alert":{
                    "type":"enabled"
                    },
                "syslog":{
                    "type":"enabled",
                    "redundancy_interval":{}
                    },
                "trap":{
                    "type":"mixed",
                    "redundancy_interval":{}
                    },
                "ipfix":{
                    "type":"enabled"
                    },
                "event_profile":{
                    "syslog_server_profile":0
                    },
                "log_digest":{
                    "mixed":True
                    },
                "color":{
                    "leave_unchanged":True
                    },
                "alert_email":{
                    "address":"test@sonicauto.com"
                    }
                }
            ]
        }
    }
syslog_param = {
            "name":pc1_ip,
        }
local_obj = {
            "object_type": "host",
            "name": pc1_ip,
            "zone": "LAN",
            "value": pc1_ip,
        }
syslog_obj = {
            "object_type": "host",
            "name": 'test_syslog',
            "zone": "LAN",
            "value": '192.168.168.100',
        }
snmp_json = {"snmp":
                         {
                             "enable": True,
                             "system_name": "sonicwall",
                             "get_community_name": "public",
                             "trap_community_name": "public",
                             "host_1": pc2_ip,
                             "host_2": "",
                             "host_3": "",
                             "host_4": ""
                         }
        }
Lx1 = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': DUT_X1,
    'netmask': MASK,
    'gateway': DUT_X1_GW,
    'dns1': Params.G_DNS1,
    'dns2': Params.G_DNS2,
    'mgmt_https': True,
    'mgmt_ssh': True,
    'mgmt_ping': True,
    'mgmt_snmp': True,
    'user_https': True,
}
Lx2 = {
        'if': 'X2',
        'zone': 'LAN',
        'mode': 'static',
        'ip': DUT_X2,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }

log_level_settings = {
            "log": {
                "event": [{
                    "id": 1382,
                    "name": "",
                    "category": "Log",
                    "group": "",
                    "priority_level": "alert",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 600
                    },
                    "syslog": {
                        "redundancy_interval": 0
                    },
                    "event_profile": {
                        "syslog_server_profile": 0
                    },
                    "trap":{
                        "redundancy_interval":0
                    },
                    "ipfix": {
                        "redundancy_interval": 60
                    },
                    "log_digest": True ,
                    "color": {
                        "hex": "0x00FF0000"
                    },
                    "alert_email": {}
                }]
            }
}
