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
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from util.enhancedinfo import show_testcase_info
import paramunittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/VPN/AWS_VPN')



from lib.modules.CLI.system import LicenseCli
from lib.modules.CLI.network import InterfaceCli
from lib.modules.API import network,object

from lib.modules.API import aws
from lib.modules.API import firewallsettings
class Parameter():
    FIREWALL = '192.168.168.168'
    X1_DNS1 = Params.G_DNS1
    X1_DNS2 = Params.G_DNS2
    X1_IP = '13.0.0.10'
    X1_GW = '13.0.0.1'
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/AWS_VPN/testplan/aws.json'



ip = Parameter.FIREWALL
fw_api = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cgi = Firewall(ip, user='admin', password='password', supported_config_mode='cgi')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
aws_connection= aws.AwsConnection(fw_api)
aws_objects= aws.AwsObjects(fw_api)
interface = InterfaceCli(fw_cli)
license = LicenseCli(fw_cli)
addressobject=network.AddressobjectsApi(fw_api)
group_mapping=aws.AwsGroupMapping(fw_api)
addressgroup=network.AddressgroupsApi(fw_api)
add_group=object.AddressObjectGroupApi(fw_api)


