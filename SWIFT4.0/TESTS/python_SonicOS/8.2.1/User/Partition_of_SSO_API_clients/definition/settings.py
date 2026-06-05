import os
import sys
import re
import copy
import time
import json
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from util.openstack import Openstack
from runner.settings import Params, logger
from networkdevice import Host
from nose_parameterized import parameterized
import paramunittest
from runner.unittest.setup import Test, skip_if_dts, repeat_method
from runner.utils.assertion import Assertion

from utm import Firewall
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from modules.API import network,firewall,system,users,object,log


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Partition_of_SSO_API_clients')
print(sys.path)

FIREWALL = '192.168.168.168'
X1 = '12.12.1.100'
X1_GW = '12.12.1.1'
Mask = '255.255.255.0'
LAN2 = '192.168.168.223'
sso_ip = '9.9.9.9'
sso_hostname = 'newaddssoagent'
sso_default_port = 2258
sso_new_port = 2220
new_max_requests=16
wan_pc_ip = '12.12.1.3'

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + '/User/Partition_of_SSO_API_clients/testplan/SSO_API_CLIENT_JSON.json'

os_obj = Openstack(Params.testbed)
SSO_CLIENT1_lanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT1','eth0')
SSO_CLIENT1_wanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT1','eth1')
SSO_CLIENT2_lanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT2','eth0')
SSO_CLIENT2_wanip = os_obj.get_node_interface_ip('PC_SSO_CLIENT2','eth1')
ldap_host = os_obj.get_node_interface_ip('PC3','eth0')
service_agent1 = ldap_host
service_agent2 = os_obj.get_node_interface_ip('PC4','eth0')


fw = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='api')

fw_cli = Firewall(FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')

interface_ipv4 = network.InterfaceIPv4Api(fw)
user_settings_obj = users.UsersettingApi(fw)
user_sso_obj = users.SSOApi(fw)
user_local_obj = users.UserLocalApi(fw)
user_status = users.UserStatusApi(fw)
log_config = log.LogCategoryApi(fw)
user_auth_partition = users.AuthPartitionsApi(fw)
sso_client = users.SSOApi(fw)
split_dns_api = network.DnsSettingsApi(fw)

