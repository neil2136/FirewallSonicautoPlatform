import sys
import os
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Webproxy_813')
from runner.unittest.setup import Test
from lib.modules.CLI import network
from utm import Firewall
from testcases.settings import Parameter
from runner.utils.assertion import Assertion

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceCli(fw)

class TestConfigFW(Test):
    uuid = 'NonTC'
    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
            
    def test_00_02_Config_X2(self):
        x2_dmz = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'static',
            'ip': Parameter.X2_IP,
        }
        rc = interface.config_interface(**x2_dmz)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")   



     
