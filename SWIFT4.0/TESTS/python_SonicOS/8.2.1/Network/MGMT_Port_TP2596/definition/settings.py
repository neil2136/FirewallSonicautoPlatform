import sys
import os
import time
import copy
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/MGMT_Port_TP2596')
from runner.settings import logger, Params
from runner.unittest.setup import Test, repeat_method
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from modules.API import network
from modules.API.system import RestartApi
from modules.CLI.system import SettingCli

OpenS = Openstack(Params.testbed)
mgmt_cli = Firewall('192.168.1.168', user='admin', password='sonicauto', supported_config_mode='cli-ssh')
fw = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='api')
mgmt_fw = Firewall('192.168.1.168', user='admin', password='sonicauto', supported_config_mode='api')
Linterface = network.InterfaceIPv4Api(fw)
restartobj = RestartApi(fw)
setting_obj = SettingCli(mgmt_cli)
pc1_eth2 = '192.168.1.10'
DUT_X1 = '172.17.1.168'
DUT_MGMT = '192.168.1.168'
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Network/MGMT_Port_TP2596/testplan/MGMT_Port_TP2596.json'
build_file = '/logs/Dont_Delete_Uboot_Upgrade_Release_Build/'
new_build = Params.prebuild
# PC SSH
PC1 = Host(Params.testbed + '-PC1')
# if Params.sonicos_ver == '7.0.1' or Params.sonicos_ver == '7.1.1':
#         res = PC1.send_command(f'ls {build_file}7.0.1/{Params.product}')
#         new_build = build_file + f'7.0.1/{Params.product}/'+ res
# elif Params.sonicos_ver == '7.0.1_x86' or Params.sonicos_ver == '7.1.1_x86':
#         res = PC1.send_command(f'ls {build_file}7.0.1_x86/{Params.product}')
#         new_build = build_file + f'7.0.1_x86/{Params.product}/' + res

MGMT = {
        'if': 'MGMT',
        'zone': 'MGMT',
        'mode': 'static',
        'ip': DUT_MGMT,
        'netmask': '255.255.255.0',
        'mgmt_https': True,
        'mgmt_ssh': True,
        'mgmt_snmp': True,
        'mgmt_ping': True,
        'user_https':True,
}
import_dict = {
            'protocol': 'scp',
            'passwd': 'password',
            'server': pc1_eth2,
            'user': 'root',
            'file': new_build
        }
