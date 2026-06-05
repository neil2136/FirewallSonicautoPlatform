import sys
import os
import time
import copy
import subprocess
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'Network/DNS_Rebinding_Attack_Prevention_2170')
import paramunittest
from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from lib.modules.API import network
from lib.modules.API import object
from lib.modules.API import log
from lib.modules.API import system
from lib.modules.CLI.system import LicenseCli

OpenS = Openstack(Params.testbed)
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='cli-ssh')
license_obj = LicenseCli(fw_cli)

Linterface = network.InterfaceIPv4Api(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
LAddrGroupOBJ = object.AddressObjectGroupApi(fw)
LogObj = log.LogMonitorApi(fw)
dnsObj = network.DnsSettingsApi(fw)
dnsPolicy = network.DnsPolicyApi(fw)
LPackageMonitObj = system.PacketmonitorApi(fw)
setting_obj = system.SettingApi(fw)
faillb_obj = network.FailoverLbApi(fw)
diag_obj = system.DiagnosticApi(fw)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Rebinding_Attack_Prevention_2170/testplan/DNS_Rebinding_Attack_Prevention_2170.json'
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/Network/DNS_Rebinding_Attack_Prevention_2170'
conf_path = os.path.join(suite_path,'conf')
bin_path = os.path.join(suite_path,'bin')
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
PC3 = Host(Params.testbed + '-PC3')
dns_server = Host(Params.testbed + '-PC2')
# define IP
DUT_X0 = '192.168.168.168'
PC1_Network = '192.168.168.0'
PC1_IF = 'eth1'
DUT_X1 = '192.200.200.10'
PC2_WAN = '192.200.200.200'
PC2_IF = 'eth1'
PC2_Network = '192.200.200.0'
DUT_X2 = '192.100.100.10'
PC3_WAN = '192.100.100.200'
PC3_IF = 'eth1'
PC3_Network = '192.100.100.0'
PC3_LAN = PC3_WAN # it'll be used when PC3 worked in LAN Zone;
PC3_DMZ = PC3_WAN # it'll be used when PC3 worked in DMZ Zone.
#cmds
rm_conf = ['rm /etc/named.conf']
install_bind9_cmds = [f"cp {conf_path}/bind-9.10.2.tar.gz ./",
                      "tar -xvzf bind-9.10.2.tar.gz",
                      "cd bind-9.10.2",
                      "./configure sysconfdir=/etc",
                      "make",
                      "make install",
                      "rpm -qa | grep bind"]
config_bind9_cmds = ["rndc-confgen > /etc/rndc.conf",
                     "mkdir -p /var/named",
                     f"cp {conf_path}/named.conf /etc/",
                     f"cp {conf_path}/*.zone /var/named/",
                     f"cp {conf_path}/named.* /var/named/",
                     "tail /etc/rndc.conf|sed '/^# End/ d'|sed 's/^#//g'>>/etc/named.conf",
                     "ls  /var/named/"]
start_bind9_cmds = ['named -c /etc/named.conf &']
dns_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X1} dev {PC2_IF}']
pc3_route_cmds = [f'ip r a {PC1_Network}/24 via {DUT_X2} dev {PC3_IF}',
                  "ip route"]
pc1_route_cmds = [f'ip r a {PC2_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  f'ip r a {PC3_Network}/24 via {DUT_X0} dev {PC1_IF}',
                  "ip route"]
config_pc3_cmds = [f"cp {bin_path}/libnet-1.1.2.1-2.2.el6.rf.i686.rpm /root/",
                    "rpm -ivh /root/libnet-1.1.2.1-2.2.el6.rf.i686.rpm",
                    f"cp {bin_path}/netw-ib-ox-ag-5.39.0.tgz /root/",
                    "tar -xvzf /root/netw-ib-ox-ag-5.39.0.tgz",
                    "cd /root/netw-ib-ox-ag-5.39.0/src/netwib-src/src/",
                    "./genemake",
                    "make",
                    "make",
                    "make install",
                    "cd ../../netwox-src/src/",
                    "./genemake",
                    "make",
                    "make",
                    "make install",
                    "which netwox",
                    ]
#failover disable json
lb_opt = {
    'enable'    : False,
}
#dns setting
dns_set = {"dns":
           {"server":
                {"inherit":True,
                "static":{"primary":"0.0.0.0","secondary":"0.0.0.0","tertiary":"0.0.0.0"},
                "ipv6":{"inherit":True,"static":{"primary":"::","secondary":"::","tertiary":"::"},"preferred":False}
                },
            "rebinding":{"enable":True,"action":"drop-dns-reply","allowed_domains":{"group":"test_group2"}},
            "fqdn_binding":False,
            "split_servers":True,
            "fqdn_over_tcp_dns":False
            }}
# {"dns":{"server":{"inherit":false,"static":{"primary":"192.100.100.200","secondary":"0.0.0.0","tertiary":"0.0.0.0"},
#                   "ipv6":{"inherit":true,"static":{"primary":"::","secondary":"::","tertiary":"::"},"preferred":false}},
#                   "rebinding":{"enable":true,"action":"drop-dns-reply","allowed_domains":{}},
#                   "fqdn_binding":false,"split_servers":true,"fqdn_over_tcp_dns":false}}
#Interface Json
Lx1 = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X1,
        'netmask': '255.255.255.0',
        'gateway': PC2_WAN,
        'dns1': '10.9.1.40',
        'dns2': '10.50.129.148',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }
Lx1_r = {
        'if': 'X1',
        'zone': 'WAN',
        'mode': 'static',
        'ip': DUT_X1,
        'netmask': '255.255.255.0',
        'gateway': '192.200.200.1',
        'dns1': Params.G_DNS1,
        'dns2': Params.G_DNS2,
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
    }

# DUT local Address object and group
fqdn_ao = {
    'name': 'test',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': 'test.com',
    'dns_ttl':0
}
fqdn_ao_com = {
    'name': 'com',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': '*.com',
    'dns_ttl':0
}
fqdn_ao_net = {
    'name': 'net',
    'zone': 'WAN',
    'object_type': 'fqdn',
    'value': '*.net',
    'dns_ttl':0
}
ao_group1 = {
    "address_groups":[{
        "ipv4":{
            "address_object":{
                "fqdn":[]
                },
            "name":"test_group"
            }
        }]
    }
ao_group2 = {
    "address_groups":[{
        "ipv4":{
            "address_object":{
                "fqdn":[]
                },
            "name":"test_group2"
            }
        }]
    }


dns_proxy_4to4 = {"dns_policies":[
    {
        "name":"test",
        "priority":{"manual":1},
        "enable":True,
        "comment":"",
        "source":{"address":{"any":True}},
        "service":{"group":"DNS (Name Service)"},
        "from":"LAN","schedule":{"always_on":True},
        "action":{"proxy":True},
        "ticket":{"tag1":"","tag2":"","tag3":""},
        "max_connections":100,
        "connection_limit":{"source":{"enable":False,"threshold":{"value":128}}},
        "proxy_mode":"ipv4-ipv4"
        }
    ]}

