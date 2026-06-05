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
from util.dpissl.lib.mail_server import StartMailServer
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Capture_ATP_And_Log')

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

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Capture_ATP_And_Log/testplan/Config_Audit_CLI_Capture_ATP_And_Log.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Audit_CLI_Capture_ATP_And_Log/confs/'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
postfix_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/postfix_1k/'
dovecot_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/dovecot_1k/'
mail_server_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/cert/'
start_mail_server = StartMailServer(PC1,postfix_1k_path,dovecot_1k_path,mail_server_path+'vsftpd_1k.key',mail_server_path+'vsftpd_1k.crt')

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

GAV_settings = securityservices.GAV(fw_api)
clear_log = ClearlogCli(fw_cli)

pc1_route_cmds = [f'ip r a {PC2_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  "ip route"]
pc2_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X1} dev {PC2_IF}',
                  "ip route"]

edit_alert_cmds1 = ["config","log group id 79","priority-level alert","commit","end"]
edit_alert_cmds2 = ["config","log group id 79","priority-level inform","commit","end"]
edit_attri_cmds1 = ["config","log categories","global-category-attribute ","log-email address 123456@sonicwall.com","commit","end"]
edit_attri_cmds2 = ["config","log categories","global-category-attribute ","log-email address '' ","commit","end"]
reset_count_cmd = ["config","log categories","reset event-count all","commit","end"]
temp_cmds = ['config','log categories','save-template /','import-template custom','end']
edit_category_cmds1=['config',"log category Anti-Spam","log-email 3344_category@sonicwall.com","commit","end"]
edit_category_cmds2=['config',"log category Anti-Spam","log-email '' ","commit","end"]
edit_group_cmds1 = ["config","log group id 79","alert-email address 123_group@sonicwall.com","commit","end"]
edit_group_cmds2 = ["config","log group id 79","alert-email address '' ","commit","end"]
edit_event_cmds1 = ["config","log event id 1750","alert-email address 678_event@sonicwall.com","commit","end"]
edit_event_cmds2 = ["config","log event id 1750","alert-email address '' ","commit","end"]
reset_event_count = ["config","log categories","reset event-count event-id 1146","end"]

edit_syslog_setting1 = ["config","log syslog","display-timestamp-utc","commit","end"]
edit_syslog_setting2 = ["config","log syslog","no display-timestamp-utc","commit","end"]
cap_cmds = ["config","capture-atp","enable","commit","no enable","commit","end"]
add_syslog_cmds = ["config","log syslog","server address name test_syslog port 514 profile 0 ","commit","end"]
dis_syslog_cmds = ["config","log syslog","server address name test_syslog port 514 profile 0 ","no enabled","commit","enabled","commit","end"]
edit_syslog_cmd = ["config","log syslog","server address name test_syslog port 514 profile 0 ","data-rate-limiting","commit","end"]
del_syslog_cmd = ["config","log syslog","no server address name test_syslog port 514 profile 0 ","commit","end"]
edit_name_cmd1 = ["config","log name-resolution","method dns","commit","end"]
edit_name_cmd2 = ["config","log name-resolution","method none","commit","end"]
reset_name_cmds = ["config","log-action reset-name-cache ","end"]
data_collect_cmds = ["config","log-action report-start","log-action report-stop","end"]
# edit_data_cmds = ["config","log reports","report-view bandwidth-usage-by-ip","commit","end"] ##1518500
edit_email_cmds1 = ["config","log automation","email-address log test@sonicauto.com","commit","end"]
edit_email_cmds2 = ["config","log automation","email-address log ''","commit","end"]
edit_file_type= ["config","capture-atp","enable","file-type pdf","commit","no file-type pdf","no enable","commit","end"]
edit_mail_server1 = ["config","log automation","mail-server 192.168.168.200 ","commit","end"]
edit_mail_server2 = ["config","log automation","mail-server '' ","commit","end"]
edit_mail_server_adv1 = ["config","log automation","mail-server-advanced","connection-security-method start-tls","commit","end"]
edit_mail_server_adv2 = ["config","log automation","mail-server-advanced"," no connection-security-method","commit","end"]
test_cmds = ["config","log automation","mail-server 192.168.168.200 ","email-address log test@sonicauto.com","commit",'exit',"log-action test","exit"]
test_clear_cmds = ["config","log automation","email-address log ''","mail-server ''","commit","end"]


edit_ftp_cmds1 = ["config","log automation","ftp-log","send-log-to-ftp","commit","end"]
edit_ftp_cmds2 = ["config","log automation","ftp-log","no send-log-to-ftp","commit","end"]

enable_cap_cmds = ["config","capture-atp","enable","commit","end"]
edit_capture_cmds1 = ["config","capture-atp","enable","exclude address for-capture-atp name test_syslog ","commit","end"]
edit_capture_cmds2 = ["config","capture-atp","no exclude address for-capture-atp","commit","end"]
edit_filesize_cmds1 = ["config","capture-atp","file-size restrict 1234","commit","end"]
edit_filesize_cmds2 = ["config","capture-atp","file-size restrict 10240","file-size default","commit","end"]
md5_cmds1 =  ["config","capture-atp","exclude md5-entry 11223344556677889900aabbccddeeff","commit","end"]
md5_cmds2 =  ["config","capture-atp","no enable","no exclude md5-entry 11223344556677889900aabbccddeeff","commit","end"]
edit_display_cmds1 = ["config","log display max-number 123","commit","exit"]
edit_display_cmds2 = ["config","log display max-number 200","commit","exit"]


gav_put = {
    'enable_GAV': True
}
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
