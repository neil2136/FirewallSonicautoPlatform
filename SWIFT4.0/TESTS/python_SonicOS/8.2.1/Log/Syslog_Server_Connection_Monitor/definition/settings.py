import sys
import os
import re
from time import sleep
import json
from threading import Thread
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

# import contents from common_lib path
sys.path.append(os.environ['PYTHON_COMMON_HOME'])
from util.openstack import Openstack
from networkdevice import Host
from util.enhancedinfo import show_testcase_info
from utm import Firewall


# import form branch lib contents for test suite
sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
from lib.modules.API.network import InterfaceIPv4Api, AddressobjectsApi, NetworkMonitorApi
from lib.modules.API.log import LogMonitorApi, SyslogSettingsApi, LogSettingsApi
from lib.modules.CLI.log import SyslogSettingsCli
from lib.modules.API.system import DiagnosticApi, SettingApi, PacketmonitorApi, RestartApi
from lib.modules.CLI.system import LicenseCli


sys.path.append(os.environ['PYTHON_COMMON_HOME'])
suite_path = os.environ['PYTHON_SONICOS_HOME'] + '/Log/Syslog_Server_Connection_Monitor/'
sys.path.append(suite_path)
sys.path.append(suite_path + 'testcases')
TESTPLAN = suite_path + 'testplan/syslog_server_connection_monitor.json'

os_obj = Openstack(Params.testbed)
PC1_ETH0_IP = os_obj.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = os_obj.get_node_interface_ip('PC1', 'eth1')
PC1_ETH2_IP = os_obj.get_node_interface_ip('PC1', 'eth2')
PC2_ETH0_IP = os_obj.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = os_obj.get_node_interface_ip('PC2', 'eth1')
PC2_ETH2_IP = os_obj.get_node_interface_ip('PC2', 'eth2')

logger.info(f"""
PC1_ETH0_IP is: {PC1_ETH0_IP}
PC1_ETH1_IP is: {PC1_ETH1_IP}
PC1_ETH2_IP is: {PC1_ETH2_IP}
PC2_ETH0_IP is: {PC2_ETH0_IP}
PC2_ETH1_IP is: {PC2_ETH1_IP}
PC2_ETH2_IP is: {PC2_ETH2_IP}
""")
pc1_login = Host(PC1_ETH2_IP)
pc2_login = Host(PC2_ETH2_IP)


# Params on fw
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.168'
    MAX_NUM = 7
    X1_DNS_1 = Params.G_DNS1
    X2_DNS_2 = Params.G_DNS2


# Instantiate objects including API import
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api'
)
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh'
)

iface_v4_api = InterfaceIPv4Api(fw)
log_mon_api = LogMonitorApi(fw)
syslog_api = SyslogSettingsApi(fw)
syslog_cli = SyslogSettingsCli(fw_cli)
net_mon_api = NetworkMonitorApi(fw)
pkt_api = PacketmonitorApi(fw)
ao_api = AddressobjectsApi(fw)
diag_api = DiagnosticApi(fw)
setting_api = SettingApi(fw)
restart_api = RestartApi(fw)
log_set_api = LogSettingsApi(fw)
licensecli = LicenseCli(fw_cli)
