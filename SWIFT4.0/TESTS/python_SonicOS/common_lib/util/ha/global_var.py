__author__ = 'sgao'
import sys
import os
import copy
import time
import re
import unittest
from multiprocessing import Process,Manager

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/High_Availability')

from runner.unittest.setup import Test, repeat_method
from runner.settings import Params,logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from powercontrol.apc import PDU
from powercontrol.sentry import CDU

from utm import Firewall, is_Firewall_up
from config.swconfig import DeviceConfig
from config.restore_tel import RestoreFwTelnet
from config.upload_firmware import UploadFirmware
from config.get_coredump_tel import GetCoredumpTel

from lib.modules.API import network
from lib.modules.API import highavailability as ha_api
from lib.modules.CLI import highavailability as ha_cli
from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.system import AdminCli
from local_ha_lib import Local_HA_Lib
from lib.modules.API.system import DiagnosticApi

if 'TOPO' not in os.environ:
    os.environ['TOPO'] = 'HA'
topo = f"{Params.product}_{os.environ['TOPO']}"
logger.info(f"This suite use topology: {topo}")

if 'HA_REGISTER' not in os.environ:
    os.environ['HA_REGISTER'] = 'off'

ha_path = os.environ["PYTHON_COMMON_HOME"] + '/util/ha'
sw_cmd = f'python3 {os.environ["PYTHON_COMMON_HOME"]}/config/swconfig.py'
SPECFILE = os.environ["COMMON_HOME"] + '/data/switches/' + Params.testbed + '.yaml'
dc = DeviceConfig(user='admin', password='password', specfile=SPECFILE)
logger.info(Params.product)

# # # Primary and Secondary device
product = Params.product
pri_name = product + '-PRI'.upper()
sec_name = product + '-SEC'.upper()
dut_pri = dc.device(pri_name)
dut_sec = dc.device(sec_name)

# # # Power Controller
yaml = dc.load_yaml()
pri_rpsw_svr = dut_pri[0]['power']['controller']
sec_rpsw_svr = dut_sec[0]['power']['controller']
pri_rpsw_ip = yaml['powercontrol'][pri_rpsw_svr]['ip']
sec_rpsw_ip = yaml['powercontrol'][sec_rpsw_svr]['ip']
pri_rpsw_type = yaml['powercontrol'][pri_rpsw_svr]['type']
sec_rpsw_type = yaml['powercontrol'][sec_rpsw_svr]['type']
pri_rpsw_model = yaml['powercontrol'][pri_rpsw_svr]['model']
sec_rpsw_model = yaml['powercontrol'][sec_rpsw_svr]['model']
pri_rpsw_port = dut_pri[0]['power']['port']
sec_rpsw_port = dut_sec[0]['power']['port']
pri_rpsw_pass = yaml['powercontrol'][pri_rpsw_svr]['password'] \
    if 'password' in yaml['powercontrol'][pri_rpsw_svr].keys() else 'password'
sec_rpsw_pass = yaml['powercontrol'][sec_rpsw_svr]['password'] \
    if 'password' in yaml['powercontrol'][sec_rpsw_svr].keys() else 'password'
tmp_testbed = Params.testbed
logger.info(f"{tmp_testbed} Pri PDU pass: {pri_rpsw_pass}")
logger.info(f"{tmp_testbed} Sec PDU pass: {sec_rpsw_pass}")
pri_power = PDU(ip=pri_rpsw_ip, password=pri_rpsw_pass) if pri_rpsw_type.lower() in ['apc', 'pdu'] else \
            CDU(ip=pri_rpsw_ip, password=pri_rpsw_pass)
sec_power = PDU(ip=sec_rpsw_ip, password=sec_rpsw_pass) if sec_rpsw_type.lower() in ['apc', 'pdu'] else \
            CDU(ip=sec_rpsw_ip, password=sec_rpsw_pass)

# # # Console
pri_con_ip = dut_pri[0]['console']['server']
sec_con_ip = dut_sec[0]['console']['server']
pri_con_port = str(dut_pri[0]['console']['telnetport'])
sec_con_port = str(dut_sec[0]['console']['telnetport'])

# # # FW Parameters
FIREWALL = '192.168.168.168'
pri_x0_ip = '192.168.168.169'
sec_x0_ip = '192.168.168.170'
x0_probe_ip = '192.168.168.161'
x0_mask = '255.255.255.0'

x1_ip = '11.11.11.200'
pri_x1_ip = '11.11.11.204'
sec_x1_ip = '11.11.11.205'
x1_probe_ip = '11.11.11.254'
x1_network = '11.11.0.0'
x1_mask = '255.255.0.0'
local_dns = '10.6.0.249'

x2_ip = '192.1.170.168'
pri_x2_ip = '192.1.170.169'
sec_x2_ip = '192.1.170.170'
x2_probe_ip = '192.1.170.1'
x2_mask = '255.255.255.0'

pri_serial = dut_pri[0]['serial']
sec_serial = dut_sec[0]['serial']

x0_vmac = '1A:C2:41:00:2D:99'
x1_vmac = '1A:C2:41:00:2D:9A'

# # # PC Settings
x0_pc1_eth1 = x0_probe_ip
x1_pc2_eth1 = '11.11.11.13'
x2_pc3_eth1 = x2_probe_ip
vpn_pc4_eth1 = '172.16.1.1'
pc2_name = Params.testbed + '-PC2'
pc2_host = Host(pc2_name)
pc_user = "root"
pc_pass = "password"

data_if = 'X4'
ctrl_if = 'X6'

x1_static = {
    'if'        : 'X1',
    'zone'      : 'WAN',
    'mode'      : 'static',
    'ip'        : x1_ip,
    'netmask'   : x1_mask,
    'gateway'   : x1_probe_ip,
    'dns1'      : Params.G_DNS1,
    'dns2'      : local_dns,
    'mgmt_https': True,
    'mgmt_ssh'  : True,
    'mgmt_ping' : True,
    'fragment_packets': True,
}
sec_x1_static = {
    'if'        : 'X1',
    'zone'      : 'WAN',
    'mode'      : 'static',
    'ip'        : sec_x1_ip,
    'netmask'   : x1_mask,
    'gateway'   : x1_probe_ip,
    'dns1'      : Params.G_DNS1,
    'dns2'      : local_dns,
    'mgmt_https': True,
    'mgmt_ssh'  : True,
    'mgmt_ping' : True,
    'fragment_packets': True,
}
ha_conf = {
    'mode'              : 'active_standby',
    'control_interface' : ctrl_if,
    'secondary_serial'  : sec_serial,
}
x0_monitor = {
    'interface': 'X0',
    'version': 'ipv4',
    'link_monitoring': True,
    'primary': pri_x0_ip,
    'secondary': sec_x0_ip,
    'allow_management': True,
    'logical_probe_enable': True,
    'logical_probe_ip': x0_probe_ip,
}
x1_monitor = {
    'interface': 'X1',
    'version': 'ipv4',
    'link_monitoring': True,
    'primary': pri_x1_ip,
    'secondary': sec_x1_ip,
    'allow_management': True,
    'logical_probe_enable': True,
    'logical_probe_ip': x1_probe_ip,
}

fw = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')
pri_api = Firewall(pri_x0_ip, user='admin', password='password', supported_config_mode='api')
sec_api = Firewall(sec_x0_ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
pri_cli = Firewall(pri_x0_ip, user='admin', password='password', supported_config_mode='cli-ssh')
sec_cli = Firewall(sec_x0_ip, user='admin', password='password', supported_config_mode='cli-ssh')
pri_console = Firewall(
    FIREWALL, user='admin', password='password',
    supported_config_mode='cli-console', console_ip=pri_con_ip, console_port=pri_con_port
)
sec_console = Firewall(
    FIREWALL, user='admin', password='password',
    supported_config_mode='cli-console', console_ip=sec_con_ip, console_port=sec_con_port
)

if_api = network.InterfaceIPv4Api(fw)
ha_status_api = ha_api.StatusApi(fw)
ha_settings_api = ha_api.SettingsApi(fw)
ha_advanced_api = ha_api.AdvancedApi(fw)
ha_monitor_api = ha_api.MonitoringApi(fw)
diagnostic_api = DiagnosticApi(fw)

ha_status_cli = ha_cli.StatusCli(fw_cli)
ha_settings_cli = ha_cli.SettingsCli(fw_cli)
ha_advanced_cli = ha_cli.AdvancedCli(fw_cli)
ha_monitor_cli = ha_cli.MonitoringCli(fw_cli)
license_cli = LicenseCli(fw_cli)

manager = Manager()

from util.ha.diag_fw_console_connection import SLCPortTester
# Configuration pri fw parameters
pri_config = {
    "ip": pri_con_ip,
    "device_port": pri_con_port,     # DUT Console port to test (2022)
    "management_port": 23,   # Console Management port for recovery (23)
    "username": "admin",     # Console Management username
    "password": "password",   # Console Management password
    "timeout": 10,           # Telnet timeout (seconds)
    "wait_time": 300         # Wait time after reboot (seconds)
}
# Create tester instance
diagpriconsole = SLCPortTester(**pri_config)

# Configuration sec fw parameters
sec_config = {
    "ip": sec_con_ip,
    "device_port": sec_con_port,     # DUT Console port to test (2022)
    "management_port": 23,   # Console Management port for recovery (23)
    "username": "admin",     # Console Management username
    "password": "password",   # Console Management password
    "timeout": 10,           # Telnet timeout (seconds)
    "wait_time": 300         # Wait time after reboot (seconds)
}
# Create tester instance
diagsecconsole = SLCPortTester(**sec_config)
