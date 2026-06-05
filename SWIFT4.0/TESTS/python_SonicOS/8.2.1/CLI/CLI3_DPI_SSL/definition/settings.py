import os
import sys
import re
import time
import copy
import requests
import unittest
from runner.unittest.suite import UnittestSuite
from runner.utils.assertion import Assertion
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.settings import Params, logger
from util.openstack import Openstack

# import contents from common_lib path
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
from util.enhancedinfo import show_testcase_info

# import form test suite root path like definition
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI3_DPI_SSL/'
TESTPLAN = suite_path + 'testplan/cli3_dpi_ssl.json'
cert_path = suite_path + 'definition/certificate'

# import from branch lib contents for test suit
from lib.modules.CLI.dpissl import ClientSslCli, ServerSslCli
from lib.modules.CLI.system import LicenseCli, CertificateCli
from lib.modules.API.network import InterfaceIPv4Api


# parameters on the openstack
class Parameter:
    FIREWALL = '192.168.168.168'
    X1_IP = '12.12.1.200'
    MASK = '255.255.255.0'
    X1_GW = '12.12.1.1'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2


OpenS = Openstack(Params.testbed)
PC1_ETH1_IP = OpenS.get_node_interface_ip('PC1', 'eth1')

# Instantiate objects including API,CLI
fw = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='api')
fw_cli = Firewall(
    Parameter.FIREWALL,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

lc = LicenseCli(fw_cli)
dpisslclientcli = ClientSslCli(fw_cli)
dpisslservercli = ServerSslCli(fw_cli)
certificatecli = CertificateCli(fw_cli)
interfaceapi = InterfaceIPv4Api(fw)

# parameters of dpissl client and server by default
check_dpi_ssl_client_dict = {
    'enable': False,
    'intrusion-prevention': False,
    'gateway anti-virus': False,
    'gateway anti-spyware': False,
    'application-firewall': False,
    'content-filter': False,
    'authenticate-server-for-decrypted-connections': False,
    'expired-ca': False,
    'deployment-server-domains': False,
    'bypass-decryption': False,
    'audit-built-in-exclusion': False,
    'authenticate-server': False,
}

check_dpi_ssl_server_dict = {
    'enable': False,
    'intrusion-prevention': False,
    'gateway anti-virus': False,
    'gateway anti-spyware': False,
    'application-firewall': False,
    'exclude address': None,
    'exclude user': None,
    'include address': 'All',
    'include user': 'All',
}

dpi_ssl_include_exclude_dict = {
    'exclude address': None,
    'exclude service': None,
    'exclude user': None,
    'include address': 'All',
    'include service': 'All',
    'include user': 'All',
}

cfs_category_based_exclusion_inclusion_dict = {
    'exclude cfs-category-unavailable': False,
    'mode': 'exclude',
    'disable category list': ['all'],
}