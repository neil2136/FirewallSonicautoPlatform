import os
import re
import time
import paramunittest
from nose_parameterized import parameterized
from runner.settings import Params, logger
from runner.unittest.setup import Test, repeat_method, skip_if_fail_method
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info
from runner.utils.assertion import Assertion
from utm import Firewall
from networkdevice import Host
from lib.modules.API import network
from lib.modules.API import system
from lib.modules.API import policy
from lib.modules.CLI.system import DiagnosticsCli,StatusCli


class Parameter():
    CONSOLE_METHOD    = 'ssh'    
    DUT_X0_IP         = '192.168.168.168'    
    DUT_X1_IP         = '1.1.1.11'    
    DUT_X1_GATEWAY    = '1.1.1.254'    
    DUT_X2_IP         = '12.12.1.100'    
    DUT_X3_IP         = '2.2.2.12'    
    DUT_X3_GATEWAY    = '2.2.2.254'    
    ROUTER_X1_IP      = '12.12.1.201'    
    ROUTER_X1_GATEWAY = '12.12.1.11'    
    ROUTER_X2_IP      = '3.3.3.13'    
    ROUTER_X2_ZONE    = 'DMZ'    
    PC1_ETH2_IP       = '1.1.1.10'    
    PC1_ETH3_IP       = '12.12.1.11'    
    PC1_ETH4_IP       = '3.3.3.11'    
    TESTPLAN = os.environ["PYTHON_SONICOS_HOME"] + "/Network/OSPF/testplan/ospf.json"
    cfg_path = os.environ["PYTHON_COMMON_HOME"] + '/config/'

fw = Firewall(Parameter.DUT_X0_IP, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(Parameter.DUT_X0_IP, user='admin', password='password', supported_config_mode='cli-ssh')
fw_rt = Firewall(Parameter.ROUTER_X1_IP, user='admin', password='password', supported_config_mode='api')
fw_cli_rt = Firewall(Parameter.ROUTER_X1_IP, user='admin', password='password', supported_config_mode='cli-ssh')
pc1= Host('localhost')

ospf_auth_cmd = {
    'NOAUTH'    : 'no ip ospf authentication',
    'PWDAUTH'   : 'ip ospf authentication-key 1234',
    'MSGAUTH1'  : 'ip ospf message-digest-key 1 md5 1234',
    'MSGAUTH10' : 'ip ospf message-digest-key 10 md5 1234',
}
param_map = {
    'never'     : [ 'never', '10', '2'],
    'wan-up'     : [ 'wan_up', '10', '2'],
    'always'    : [ 'always', '10', '2'],
}
probe_map ={
    'on_good': True,
    'on_bad': True,
    'off':False

}
diag_obj = DiagnosticsCli(fw_cli)
status_obj= StatusCli(fw_cli)
interface_obj = network.InterfaceIPv4Api(fw)
packet_obj=system.PacketmonitorApi(fw)
rem_interface_obj = network.InterfaceIPv4Api(fw_rt)
setting_obj = system.SettingApi(fw)
rem_setting_obj = system.SettingApi(fw_rt)
route_obj =network.DynamicRoutingApi(fw)
r_policy_obj=policy.RoutePolicyApi(fw)
rem_route_obj =network.DynamicRoutingApi(fw_rt)
lb_obj = network.FailoverLbApi(fw)
admin_obj = system.AdminApi(fw)
admin_rt =system.AdminApi(fw_rt)

def check_increasing(L):
    return all(x<y for x, y in zip(L, L[1:]))