import os
import sys
import re
import time
import copy

from runner.unittest.suite import UnittestSuite
from runner.unittest.setup import Test, skip_if_fail_method, repeat_method
from runner.utils.assertion import Assertion
from runner.settings import Params, logger

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.enhancedinfo import show_testcase_info
from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall, G_PASSWORD_NEW
import paramunittest

# import form branch lib contents for test suite
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from modules.ui.fw_page import FWPage
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.system import AdminApi, SettingApi
from lib.modules.CLI.system import LicenseCli


# import from test suite root path like bin
suite_path = os.environ["PYTHON_SONICOS_HOME"] + 'UI8'

# PC addresses
OpenS = Openstack(Params.testbed)
PC1_ETH0_IP = OpenS.get_node_interface_ip('PC1', 'eth0')
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')
PC2_ETH0_IP = OpenS.get_node_interface_ip('PC2', 'eth0')
PC2_ETH1_IP = OpenS.get_node_interface_ip('PC2', 'eth1')
logger.info(f'\n PC1_ETH0_IP: {PC1_ETH0_IP}'
            f'\n PC1_ETH1_IP: {PC1_ETH1_IP}'
            f'\n PC2_ETH0_IP: {PC2_ETH0_IP}'
            f'\n PC2_ETH1_IP: {PC2_ETH1_IP}'
            )
PC1_LOGIN = Host(PC1_ETH0_IP)
PC2_LOGIN = Host(PC2_ETH0_IP)


# parameters on the firewall
class Parameter:
    FIREWALL = '192.168.168.168'
    Mask = '255.255.255.0'
    X1_IP = '12.12.1.168'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


# fw object
ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
fw_page_ui = FWPage(password=G_PASSWORD_NEW)

admin_api = AdminApi(fw)
interface_api = InterfaceIPv4Api(fw)
setting_api = SettingApi(fw)
license_cli = LicenseCli(fw_cli)


# parameters on the init_resource
X1_static_dict = {
    'if': 'X1',
    'zone': 'WAN',
    'mode': 'static',
    'ip': Parameter.X1_IP,
    'gateway': Parameter.X1_GW,
    'dns1': Parameter.X1_DNS1,
    'dns2': Parameter.X1_DNS2,
    'comment': 'Default WAN',
    'mgmt_https': True
}
