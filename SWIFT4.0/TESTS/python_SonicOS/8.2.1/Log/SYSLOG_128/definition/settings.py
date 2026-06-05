__author__ = 'CHU'

import os
import sys
import copy
import time
import re

from runner.unittest.setup import Test
from runner.settings import Params,logger
from runner.utils.assertion import Assertion

from utm import Firewall
from networkdevice import Host
from util.openstack import Openstack
from util.enhancedinfo import show_testcase_info

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Log/SYSLOG_128')

from lib.modules.API import network
from lib.modules.API import log
from lib.modules.API import system


FIREWALL 		= '192.168.168.168'
# Local DUT
DUT             = "192.168.168.168"
DNS_SERVER      = Params.G_DNS1
WANIP           = '192.168.2.105'
WANIP2          = '192.168.2.100'
GW              = '192.168.2.1'

logserver1 = '192.168.168.167'
logserver2 = '192.168.168.169'
logserver3 = '192.168.168.166'
servers = [logserver1,logserver2,logserver3]

serverport = 514
serverport1 = 513

facility = 'local-use1'
syslog_id = 'SonicBoys'
syslog_format = 'webtrends'

file_path1 = '/etc/sysconfig/rsyslog'
file_path2 = '/etc/rsyslog.conf'

Obj = {
        'name': logserver1,
        'zone': 'LAN',
        'object_type': 'host',
        'value': logserver1,
    }
syslog_opt = {
        'name'      : logserver1,
        'port'      : serverport1,
        'profile'   : 0,
}

TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/Log/SYSLOG_128/testplan/syslog_128_smoke.json'

ip = FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
OpenS  = Openstack(Params.testbed)
LAddr_obj = network.AddressobjectsApi(fw)
Log_obj = log.SyslogSettingsApi(fw)
diag_obj = system.DiagnosticApi(fw)

PC1 = OpenS.get_node_interface_ip('PC1', 'eth0')
PC2 = OpenS.get_node_interface_ip('PC2', 'eth0')

from definition.library import SyslogLib
syslog_lib = SyslogLib(fw)

TestPath = os.environ["PYTHON_SONICOS_HOME"]+'/Log'