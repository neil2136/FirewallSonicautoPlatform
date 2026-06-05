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
from lib.modules.API import network,vpn,firewall,system,log
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.vpn import VpnBaseSettingsCli,VpnAdvancedSettingsCli
from util.dpissl.lib.mail_server import StartMailServer
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_VPN')

OpenS = Openstack(Params.testbed)
MASK = '255.255.255.0'
DUT_X0 = '192.168.168.168'
DUT_X1 = '13.0.0.10'
DUT_X1_GW = '13.0.0.1'
DUT_X2 = '23.0.0.10'
DUT_X3 = '12.12.1.200'
Remote_X0 = '172.16.1.101'
Remote_X1 = '12.12.1.201'
#pc1_ip = "192.168.168.200"
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
LOCALSUBNET = "X0\ Subnet"
REMOTESUBNET = "X0 Subnet"
PC2 = Host('15.0.0.4', user='root', password='password')
PC1 = Host(pc1_ip, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_VPN/testplan/Config_Auditing_CLI_VPN.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_CLI_VPN/confs/'
ca_cert = os.environ["PYTHON_COMMON_HOME"]+'/util/vpn_cert/rootca.pem'
local_cert = os.environ["PYTHON_COMMON_HOME"]+'/util/vpn_cert/my_cert.pfx'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
postfix_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/postfix_1k/'
dovecot_1k_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/config/server_imaps/dovecot_1k/'
mail_server_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/cert/'
start_mail_server = StartMailServer(PC1,postfix_1k_path,dovecot_1k_path,mail_server_path+'vsftpd_1k.key',mail_server_path+'vsftpd_1k.crt')

fw_api = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(DUT_X0, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
Linterface = network.InterfaceIPv4Api(fw_api)
LAddrOBJ = network.AddressobjectsApi(fw_api)
Lvpn_obj = vpn.VpnbasesettingApi(fw_api)
Lvpn_cli = VpnBaseSettingsCli(fw_cli)
vpnadv_cli = VpnAdvancedSettingsCli(fw_cli)

Laccess_rule_obj = firewall.AccessRuleApi(fw_api)
snmp_obj = system.SNMPApi(fw_api)
syslog_api = log.SyslogSettingsApi(fw_api)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw_api)
audit_logobj = log.AuditlogMonitorApi(fw_api)
vpn_setting = vpn.VpnAdvancedsettingApi(fw_api)
admin_obj = system.AdminApi(fw_api)
log_automation = log.LogAutomationApi(fw_api)
logsetting_obj = log.LogSettingsApi(fw_api)
log_category = log.LogCategoryApi(fw_api)
LTimeObj = system.TimeApi(fw_api)
LCACertObj = system.CertificateApi(fw_api)
dhcp_over_vpn = vpn.DhcpOverVpnApi(fw_api)
l2tpserver_obj = vpn.L2tpServerApi(fw_api)
diag_obj = system.DiagnosticApi(fw_api)

pc1_route_cmds = [f'ip r a {PC2_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  "ip route"]
pc2_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X1} dev {PC2_IF}',
                  "ip route"]
vpn_set = {
    'enable': True,
    "firewall_identifier":"AAAAAA"
}
vpn_set_cmds = ['config','vpn','firewall-identifier AAAAAA','commit','exit']
add_pro_client_cmds = ['config','vpn policy provision-client vpn_client','enable','gateway primary 12.12.1.201','user-name user1',
                       'user-password password','auth-method shared-secret',
                      'shared-secret password','ap-client-id vpn_client','commit','exit','end' ]
edit_pro_client_cmds = ['config','vpn policy provision-client vpn_client','user-name user5','commit','exit']
add_pro_server_cmds = ['config','vpn policy provision-server vpn_server','enable','network local allow-unauthenticated name X0\ Subnet ',
                       'network remote destination-network name remote_net ','auth-method shared-secret',
                      'shared-secret password','ap-client-id vpn_server','commit','exit','end' ]
l2tp_cmd = ['config','vpn','l2tp-server','enable','commit','end']
centarl_cmds = ['config','vpn','dhcp-over-vpn','central','send-requests','commit','end']
log_vpn_category = {
    "log":{
        "category":
        [
            {
                "id":7,
                "name":"VPN",
                "priority_level":"alert",
                "log_email":"test.@sonicauto.com",
                "log_monitor":{"type":"mixed"},
                "email_alert":{"type":"mixed"},
                "syslog":{"type":"mixed"},
                "trap":{"type":"mixed"},
                "ipfix":{"type":"mixed"},
                "event_profile":{"syslog_server_profile":0},
                "log_digest":{"mixed":True},
                "color":{"leave_unchanged":True},
                "alert_email":{}
            }
        ]
    }
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
Lx3 = {
        'if': 'X3',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X3,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
    }
local_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(PC3_Network),
}

TI_shared = {
    'type'              : 'tunnel-interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'mode'              : 'shared-secret',
    'secret'            : 'password',
    'pri_gate'          : Remote_X1,
    'local_ike_id'      : 'ipv4 192.168.168.200',   
    'peer_ike_id'       : 'ipv4 172.16.1.3',
    'proposal ike exchange': 'main',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,
    'keep-alive':True,
}
TI_manual = {
    'type'              : 'tunnel-interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'edit_authmode'     : True,
    'mode'              : 'manual-key',
    'proposal ike exchange': 'main',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,
}
TI_3rd = {
    'type'              : 'tunnel-interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'edit_authmode'     : True,
    'mode'              : 'certificate',
    'local_cert'        : 'my_cert',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    :'distinguished-name', 
    'peer_ike_type'     :'distinguished-name',
    'peer_ike_id'       :'/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'proposal ike exchange': 'main',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,
}
S2S_shared = {
    'type'              : 'site-to-site',
    'name'              : 'vpn_s2s',
    'enable'            : True,
    'mode'              : 'shared-secret',
    'edit_authmode'     : True,
    'secret'            : 'password',
    'pri_gate'          : Remote_X1,
    'local_ike_id'      : 'ipv4 192.168.168.200',   
    'peer_ike_id'       : 'ipv4 172.16.1.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': LOCALSUBNET,
    'remote_network': local_r['name'],
    'proposal ike exchange': 'main',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,
}
S2S_3rd = {
    'type'              : 'site-to-site',
    'name'              : 'vpn_3rd',
    'enable'            : True,
    'mode'              : 'certificate',
    # 'edit_authmode'     : True,
    'local_cert'        : 'my_cert',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    :'distinguished-name', 
    'peer_ike_type'     :'distinguished-name',
    'peer_ike_id'       :'/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    # 'secret'            : 'password',
    'pri_gate'          : Remote_X1,
    # 'local_ike_id'      : 'ipv4 192.168.168.200',   
    # 'peer_ike_id'       : 'ipv4 172.16.1.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': LOCALSUBNET,
    'remote_network': local_r['name'],
    'proposal ike exchange': 'main',   #main, aggressive, ikev2
    'proposal ike dh-group': '2',
    'proposal ike encryption': 'aes-128',
    'proposal ike authentication': 'sha-1',
    'proposal ike lifetime': '28800',
    'proposal ipsec protocol': 'esp',
    'proposal ipsec encryption': 'aes-128',
    'proposal ipsec authentication': 'sha-1',
    'proposal ipsec lifetime': '28800',
    'proposal ipsec perfect-forward-secrecy': False,
}
S2S_manual = {
    'type'              : 'site-to-site',
    'name'              : 'vpn_s2s',
    'enable'            : True,
    'mode'              : 'manual-key',
    # 'secret'            : 'password',
    'pri_gate'          : Remote_X1,
    # 'local_ike_id'      : 'ipv4 192.168.168.200',   
    # 'peer_ike_id'       : 'ipv4 172.16.1.3',
    'local_net_type': 'name',
    'remote_net_type': 'name',
    'local_network': LOCALSUBNET,
    'remote_network': local_r['name'],
    # 'proposal ipsec authentication': 'aes-xcbc',  #aes-xcbc,md5,sha-1,sha-256,sha-384,sha-512,none
    'proposal ipsec authentication-key': '7023a13a19b79295daf059a2ca00f4db3b60114c',     #String of hexadecimal 32 digits
    'proposal ipsec encryption': 'aes-128',          #aes,des,none
    'proposal ipsec encryption-key': '4cd0294851dfd46e8efb271f1641f788',     #String of hexadecimal 32 digits
    'proposal ipsec in-spi': '0xa5ce265b',   #Hexadecimal integer in the form: 0xHHHHHHHH
    'proposal ipsec out-spi': '0xed2fed7a',  #Hexadecimal integer in the form: 0xHHHHHHHH
    'proposal ipsec protocol': 'esp',         #ah, 
}
adv_set = {
    'traps-on-change' : True
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
