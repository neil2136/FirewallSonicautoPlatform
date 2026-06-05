import os
import sys
import re
import time
import subprocess

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/CLI/SSH_With_ECLI_Additions')

from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from networkdevice import Host
from util.openstack import Openstack

from lib.modules.API.network import InterfaceIPv4Api


class Parameter():
    FIREWALL = '192.168.168.168'
    X2_IP = '12.12.2.168'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/SSH_With_ECLI_Additions/testplan/SSH_With_ECLI_Additions.json'

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli_p = Firewall(ip, user='admin', password='password', cli_port='54022', supported_config_mode='cli-ssh')
fw_cli_x2 = Firewall(Parameter.X2_IP, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli2 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli3 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli4 = Firewall(ip, user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw_cli2_x2 = Firewall(Parameter.X2_IP, user='admin', password='sonicauto', supported_config_mode='cli-ssh')


if_api = InterfaceIPv4Api(fw)


localhost = Host('localhost')
osstack = Openstack(Params.testbed)
        
consvr, conport = osstack.get_console_info(dut='UTM')
fw_console = Firewall(ip, console_ip=consvr, console_port=conport, \
    user='admin', password='sonicauto', supported_config_mode='cli-console')

logger.info(f"console server/port: {consvr} {conport}")

if_x2_dict = {
    'if': 'x2',
    'zone': 'LAN',
    'mode': 'static',
    'ip': Parameter.X2_IP,
    'netmask': '255.255.255.0',
    'mgmt_ssh': True,
    'mgmt_https': True,
    'mgmt_ping': True
}
