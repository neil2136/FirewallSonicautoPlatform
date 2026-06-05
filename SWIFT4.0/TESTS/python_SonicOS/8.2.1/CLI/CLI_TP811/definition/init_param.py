import os
import sys
import unittest
import re
from time import sleep
import requests
import threading

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/CLI/CLI_TP811')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["COMMON_HOME"])
print(sys.path)


from util.openstack import Openstack
from utm import Firewall,FirewallAPI
from runner.unittest.setup import Test, repeat_method
from runner.settings import Params, logger
from runner.utils.assertion import Assertion
from util.enhancedinfo import show_testcase_info
from runner.unittest.suite import UnittestSuite
from modules.API import network, firewall, dpissl, system, policy, log
from networkdevice import Host
from modules.CLI.system import LicenseCli
from config.cfg_if_tel import ConfigInterfaceTelnet
from modules.API import securityservices


class Parameter():
    FIREWALL='192.168.168.168'
    X1_IP='192.168.4.200'
    X1_GW='192.168.4.1'

    PC1_eth0_IP='192.168.3.100'
    PC1_eth1_IP='192.168.168.200'

    TESTPLAN=os.environ["PYTHON_SONICOS_HOME"] + '/CLI/CLI_TP811/testplan/cli_tp811.json'

ip=Parameter.FIREWALL
fw=Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.FIREWALL, user='admin', password=Params.G_NEW_PASSWORD, supported_config_mode='cli-ssh')

interface_ipv4 = network.InterfaceIPv4Api(fw)
dpissl_server = dpissl.ServerSslApi(fw)
certObj = system.CertificateApi(fw)
appcontrol = firewall.AppControlApi(fw)
natpolicy_obj = network.NatpolicyApi(fw)
zone_obj = network.ZoneObjectsApi(fw)
addrObj = network.AddressobjectsApi(fw)
acrObj = firewall.AccessRuleApi(fw)
GAV_settings = securityservices.GAV(fw)
license_obj = LicenseCli(fw_cli)
log_obj = log.LogMonitorApi(fw)
restart = system.RestartApi(fw)
matchObj = firewall.MatchobjectApi(fw)
actionObj = firewall.ActionObjectApi(fw)
appObj = policy.AppRulesApi(fw)
ips = securityservices.IPSApi(fw)

localhost = Host('localhost')