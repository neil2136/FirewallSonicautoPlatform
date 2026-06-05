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
from util.dpissl.lib.mail_server import StartMailServer
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_VPN')

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
LOCALSUBNET = "X0 Subnet"
REMOTESUBNET = "X0 Subnet"
PC2 = Host('15.0.0.4', user='root', password='password')
PC1 = Host(pc1_ip, user='root', password='password')

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_VPN/testplan/Config_Auditing_GUI_VPN.json'
CONFS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Log/Config_Auditing_GUI_VPN/confs/'
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
# {"log":{"category":[{"id":7,"name":"VPN","priority_level":"alert","log_email":"test@sonicwall.com","log_monitor":{"type":"mixed"},"email_alert":{"type":"mixed"},"syslog":{"type":"mixed"},"trap":{"type":"mixed"},"ipfix":{"type":"mixed"},"event_profile":{"syslog_server_profile":0},"log_digest":{"mixed":true},"color":{"leave_unchanged":true}}]}}
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
Lx2_ti = {
            'name':'x2_ti',
            "zone": "LAN",
            "type": "manual",
            'ip':'2005::1',
            'bound_to': {"any":True},
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_snmp': True, 
            'prefix_length':64,
            'ipv4_address':{"name":"test_syslog"},
            'ipv6_network':{"name":"X0 IPv6 Link-Local Address"}
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
Lvpn_pro_server = {
    'type'              : 'provision_server',
    'name'              : 'vpn_server',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'ipversion'         : 'ipv4',
    'ap_client_id'      : 'vpn_server',
    'use_default_key'   : False,
    'secret'            :'12345',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : LOCALSUBNET,
    'remote_net_name'   : local_r['name']
}
Lvpn_pro_client = {
    'type'              : 'provision_client',
    'name'              : 'vpn_client',
    'enable'            : True,
    'pri_gate'          : Remote_X1,
    'user_name'         : 'user1',
    'user_password'     : '123456',
    'auth_mode'         : 'shared_secret',
    'ap_client_id'      : 'vpn_server',
    'use_default_key'   : False,
    'secret'            :'12345',
}
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn_s2s',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : DUT_X0,
    'peer_ike_id'       : Remote_X0,
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : LOCALSUBNET,
    'remote_net_name'   : local_r['name'],
    'ike_exchange'      : 'ikev2',
    'ike_encryption'    : 'aes-128',
    'ike_auth'          : 'sha-1',
    'ike_dh_group'      : '2',
    'ike_lifetime'      : '120',
    'ipsec_protocol'    : 'esp',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}
Lvpn_3rd = {
    'type'              : 'site_to_site',  # site-to-site, tunnel_interface
    'name'              : 'vpn_3rd',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Remote_X1,
    'local_net_type'    : 'name',
    'local_net_name'    : 'X0 Subnet',
    'remote_net_type'   : 'name',
    'remote_net_name'   : 'remote_net',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ike_auth'          : 'sha-1',
    'ike_dh_group'      : '26',
    'ipsec_protocol'    : 'esp',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Lvpn_manu = {
    'type'              : 'site_to_site',
    'name'              : 'vpn_s2s',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : LOCALSUBNET,
    'remote_net_name'   : local_r['name'],
    'in_spi': '0xa5ce265b',       ###  3-8 bit Hexa characters
    'out_spi': '0xed2fed7a',      ###  3-8 bit Hexa characters
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'encryption_key'    : '4cd0294851dfd46e8efb271f1641f788',
    'authentication_key'  : '7023a13a19b79295daf059a2ca00f4db3b60114c',
} 
Lvpn_TI_presh = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : 'password',
    'pri_gate'          : Remote_X1,
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'keep_alive'        : True,
}
Lvpn_TI_manual = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'auth_mode'         : 'manual',
    'pri_gate'          : Remote_X1,
    'in_spi'            : '0xa5ce265b',       
    'out_spi'           : '0xed2fed7a', 
    'ipsec_protocol'    : 'esp',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'encryption_key'    : '4cd0294851dfd46e8efb271f1641f788',
    'authentication_key': '7023a13a19b79295daf059a2ca00f4db3b60114c',
    'netbios'    : False,
    'management_https'  : False,
    'management_ssh'  : False,
    'management_snmp'  : False,
    'allow_sonicpointn_layer3'  : False,
    'user_login_http'  : False,
    'user_login_https'  : False,
    'apply_nat'  : False,
}
Lvpn_TI_3rd = {
    'type'              : 'tunnel_interface',
    'name'              : 'vpn_ti_share',
    'enable'            : True,
    'auth_mode'         : 'certificate',  # certificate or shared-secret
    'local_cert'        : 'my_cert',  # add local cert
    'local_ike_type'    : 'distinguished-name',
    'peer_ike_type'     : 'distinguished_name',
    'ipsec_protocol'    : 'esp',
    'ipsec_encryption'  : 'aes_128',
    'ipsec_auth'        : 'sha_1',
    'ike_dh_group'      : '26',
    'peer_ike_id'       : '/CN=AUTO/ST=SH/C=CN/O=SNWL/OU=AUTO/OU=AUTO/OU=AUTO',
    'pri_gate'          : Remote_X1,
    'ike_exchange'      : 'main',
    'ike_encryption'    : 'aes-128',
    'ike_auth'          : 'sha-1',
    'ipsec_pfs'         : True,
    'ipsec_pfs_dhgroup' : 2,
    'ike_lifetime'      : '120',
    'ipsec_lifetime'      : '120',
    'keep_alive'        : True,
}
signreq = {
    "certificates": {
        "generate_signing_request": [{
            "signature_algorithm": "sha-1",
            "key": {
                "type": "rsa",
                "size": "1024"
            },
            "generate": True,
            "alias": "my_cert",
            "distinguished_name": {
                "element1": {
                    "country": "CHINA"
                },
                "element2": {
                    "state": "SH"
                },
                "element3": {
                    "locality": "ShangHai"
                },
                "element4": {
                    "organization": "SNWL"
                },
                "element5": {
                    "department": "AUTO"
                },
                "element6": {
                    "group": "AUTO"
                },
                "element7": {
                    "team": "AUTO"
                },
                "element8": {
                    "common_name": "AUTO"
                }
            }
        }]
    }
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
