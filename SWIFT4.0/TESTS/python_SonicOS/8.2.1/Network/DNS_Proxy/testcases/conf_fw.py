import sys
import os
import time
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy')
from runner.unittest.setup import Test
from lib.modules.API import network
from utm import Firewall
from testcases.settings import Parameter
from runner.utils.assertion import Assertion
from runner.settings import Params, logger
from networkdevice import Host
from runner.unittest.setup import Test, repeat_method
from lib.modules.CLI.system import LicenseCli


ip = Parameter.X0_IP
fw = Firewall(ip, user='admin', password='password')
interface = network.InterfaceIPv4Api(fw)
zone_api = network.ZoneObjectsApi(fw)
dnsproxy_api = network.DnsProxyApi(fw)
dnspolicy_api = network.DnsPolicyApi(fw)
license_cli= LicenseCli(fw)


class TestConfigENV(Test):
    uuid = 'NonTC'
    description = 'Configure TB'
 
    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.REGISTER_DNS,
            # 'dns_proxy': True,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
            
    def test_00_02_Config_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'static',
            'ip': Parameter.X2_IP,
            # 'gateway': Parameter.X1_GW,
            'dns_proxy': True,
        }
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_00_03_Add_zones(self):
        rc = True
        logger.info(f'Add Trusted zone.') 
        Trusted_zone= {"zones": [{"name": "Trusted", "security_type": "trusted"}]}
        rc &= zone_api.add_zone_object(**Trusted_zone)
        logger.info(f'Add Public zone.') 
        Public_zone= {"zones": [{"name": "Public", "security_type": "public"}]}
        rc &= zone_api.add_zone_object(**Public_zone) 
        Assertion.assert_equal(rc, True, "ERR: Add zone fail.")

    def test_00_04_Add_Route(self):
        logger.info(f'Add route to {Parameter.DESTINATION}')
        rc = os.system(f'route add -host {Parameter.DESTINATION} gw 2.2.2.168')
        Assertion.assert_equal(rc, 0, f"ERR: Config route to {Parameter.DESTINATION}")

    def test_00_05_start_dns_server(self):
        pc2_ssh = Host(Params.testbed + '-PC2')
        pc2_ssh.send_command('\cp -f ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy/confs/*' + ' /etc/')
        pc2_ssh.start_service('dnsmasq')
        time.sleep(2)
        rc = pc2_ssh.send_command('service dnsmasq status')
        Assertion.assert_regular(str(rc), 'is running', f"ERR: Config route to {Parameter.DESTINATION}")
 
    @repeat_method(5)
    def test_00_06_rigister(self):
        self.goto_teardown = True
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, f"ERR:rigister failed.")
       
    def test_00_07_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS_SERVER,
            # 'dns_proxy': True,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
