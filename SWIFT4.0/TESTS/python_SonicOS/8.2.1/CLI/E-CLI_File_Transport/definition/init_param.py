import os
import sys
import unittest
import re
import time 
from time import sleep
import requests
import threading
import multiprocessing
import pexpect
from pexpect import pxssh
 

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/definition')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["COMMON_HOME"])
print(sys.path)

cert_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/cert/'
cert_1K_path=cert_path+'vsftpd_1k.p12'
cert_2K_path=cert_path+'vsftpd_2k.p12'
cert_4K_path=cert_path+'vsftpd_4k.p12'
cert_self_2K_path=cert_path+'key2048_dell_123456.p12'
common_cert_path = '/util/dpissl/config/server_imaps/'
postfix_1k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'postfix_1k/'
dovecot_1k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'dovecot_1k/'
postfix_2k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'postfix_2k/'
dovecot_2k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'dovecot_2k/'
postfix_4k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'postfix_4k/'
dovecot_4k_path=os.environ["PYTHON_COMMON_HOME"]+common_cert_path+'dovecot_4k/'
mail_server_path=os.environ["PYTHON_COMMON_HOME"]+'/util/dpissl/cert/'

from util.openstack import Openstack
from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test, repeat_method
import paramunittest
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from modules.API import network, firewall, dpissl, system, policy, log, users
from networkdevice import Host
from modules.CLI.system import LicenseCli
from config.cfg_if_tel import ConfigInterfaceTelnet
from lib.modules.CLI.system import PacketmonitorCli, AdminCli
from modules.API import securityservices
from tools.send_fetch_email import Email
from util.dpissl.lib.mail_server import StartMailServer
# from definition.send_recv_email import *
from util.openstack import Openstack
from lib.modules.API import vpn
from lib.modules.ui.fw_page import FWPage
OpenS = Openstack(Params.testbed)
import copy


# get all PC nodes and check GW exists or not from openstack
node_list = OpenS.get_nodes_as_dictionary().keys()
logger.info(node_list)

GW = 0
rm_device = 'RemoteGEN7'

class Parameter():
    FIREWALL='192.168.168.168'
    X1_IP='192.168.10.168'
    X1_GW='192.168.10.1'
    X2_IP='192.168.12.168'
    X3_IP='192.168.13.168'
    X3_GW = '192.168.13.1'

    # Local DUT
    DUT             = "192.168.168.168"
    WANIP           = "12.12.1.200"
    WANNET          = "12.12.1.0"
    LOCALNET        = "192.168.168.0"
    LOCALLANIP      = "X0 IP"
    LOCALSUBNET     = "X0 Subnet"
    DNSSERVER       = "0.0.0.0"
    # Remote DUT
    REMOTEX0        = "172.16.1.101"
    REMOTEX1        = "12.12.1.201"
    REMOTENET       = "172.16.1.0"
    #GW
    WANGW           = "12.12.1.1"

    # pc interface
    PC1_eth0_IP='192.168.168.169'   
    PC1_eth0_NET='192.168.168.0'
    PC1_eth1_IP='192.168.11.100'   #mail client
    PC1_eth1_NET='192.168.11.0'  
    PC1_eth2_IP='172.16.1.10'

    PC2_eth0_IP='172.16.1.20'   
    PC2_eth0_NET='172.16.1.0'
    PC2_eth1_IP='192.168.13.200'   #mail server
    PC2_eth1_NET='192.168.13.0'
    PC2_eth2_IP='192.168.11.200'   #ssh to config mail server
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/E-CLI_File_Transport/testplan/E_cli_filetransport_testplan.json'

VPN_bin = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/bin'
cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'
configPath = os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/cert/httpd/'
local_cert = os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/cert'
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/CLI/E-CLI_File_Transport/'
certPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/cert'
binPath = os.environ["PYTHON_COMMON_HOME"] + '/util/dpissl/bin'
ip=Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
rt = Firewall(Parameter.REMOTEX0, user='admin', password='password', supported_config_mode='api')
rmt = Firewall(Parameter.REMOTEX0, user='admin', password='password', supported_config_mode='cli-ssh')

interface_ipv4 = network.InterfaceIPv4Api(fw)
acrObj = firewall.AccessRuleApi(fw)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw)
appObj = policy.AppRulesApi(fw)
matchObj = firewall.MatchobjectApi(fw)
actionObj = firewall.ActionObjectApi(fw)
restart_api = system.RestartApi(fw)
appcontrol = firewall.AppControlApi(fw)
sonic_api=AdminCli(fw_cli)
user = users.UserLocalApi(fw)
time_api = system.TimeApi(fw)
bwm = firewall.BandwidthObjectApi(fw)
email_obj = firewall.EmailObjectApi(fw)
log_automation = log.LogAutomationApi(fw)
pm_obj = system.PacketmonitorApi(fw)
LAddrOBJ = network.AddressobjectsApi(fw)
system_obj = system.DiagnosticApi(fw)
RAddrOBJ = network.AddressobjectsApi(rt)
Lvpn_obj = vpn.VpnbasesettingApi(fw)
Rvpn_obj = vpn.VpnbasesettingApi(rt)

localhost = Host('localhost')
mail_server = Host(Parameter.PC2_eth2_IP)
mail_server_ip=Parameter.PC2_eth1_IP
start_mail_server = StartMailServer(mail_server,postfix_2k_path,dovecot_2k_path,mail_server_path+'vsftpd_2k.key',mail_server_path+'vsftpd_2k.crt')


# DUT object
remote_l = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
}
#RemoteDUT object
remote_r = {
    'name': 'remote_net',
    'zone': 'VPN',
    'object_type': 'network',
    'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
}

# VPN policy
#########################################
#                Notice!                #
#          Key:"_"      Value:"-"       #
#       site_to_site & site-to-site     #
#         triple_des & triple-des       #
#########################################
Lvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn1',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : "12.12.1.201",
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : "192.168.168.168",
    'peer_ike_id'       : "172.16.1.101",
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : "X0 Subnet",
    'remote_net_name'   : remote_l['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          :['zone', 'WAN'],
}

Rvpn = {
    'type'              : 'site_to_site',
    'name'              : 'vpn2',
    'enable'            : True,
    'auth_mode'         : 'shared_secret',
    'secret'            : '123456',
    'pri_gate'          : '12.12.1.200',
    'local_ike_type'    : 'ipv4',
    'peer_ike_type'     : 'ipv4',
    'local_ike_id'      : "172.16.1.101",
    'peer_ike_id'       : "192.168.168.168",
    'local_net_type'    : 'name',
    'remote_net_type'   : 'name',
    'local_net_name'    : "X0 Subnet",
    'remote_net_name'   : remote_r['name'],
    'ike_exchange'      : 'aggressive',
    'ike_lifetime'      : '120',
    'ipsec_lifetime'    : '120',
    'keep_alive'        : True,
    'bound_to'          : ['zone', 'WAN'],

}
