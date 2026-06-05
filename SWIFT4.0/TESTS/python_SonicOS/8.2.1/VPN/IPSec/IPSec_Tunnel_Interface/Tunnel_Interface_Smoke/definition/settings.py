import os
import re
import sys
import copy
import time
import unittest

from util.openstack import Openstack
from networkdevice import Host
from utm import Firewall
from utm import FirewallCGI
from runner.utils.assertion import Assertion
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, skip_if_dts
from util.enhancedinfo import show_testcase_info
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke')


from lib.modules.CLI.system import LicenseCli
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.vpn import VpnbasesettingApi
from lib.modules.API.system import CertificateApi

class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_DNS3 = Params.G_DNS3
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke/testplan/testplan.json'    


ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
#fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

tunnelvpn_settings = VpnbasesettingApi(fw_api)
certificate = CertificateApi(fw_api)
license = LicenseCli(fw_cli)
interface = InterfaceIPv4Api(fw_api)
