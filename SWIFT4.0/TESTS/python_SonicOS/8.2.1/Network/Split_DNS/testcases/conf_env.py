from settings import *

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
zone_api = network.ZoneObjectsApi(fw)
interface_api = network.InterfaceIPv4Api(fw)
license_cli= LicenseCli(fw)


class TestConfigENV(Test):
    uuid = 'NonTC'

    def test_00_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GW,
            'dns1': Parameter.DNS_SERVER,
            'dns2': Params.G_DNS1,
        }
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_00_02_rigister(self):
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, f"ERR:rigister failed.")

    @parameterized.expand([('public'),('trusted')])
    def test_00_03_Add_zones(self, zone):
        logger.info(f'Add {zone} zone.')
        zone_dict = {
            "zones": [
                {
                    "name": "custom_zone_" + zone,
                    "security_type": zone,
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        rc = zone_api.add_zone_object(**zone_dict)
        Assertion.assert_equal(rc, True, f"ERR: Add zone {zone} fail.")

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
        Assertion.assert_regular(str(rc), 'is running', f"ERR: start dns server failed.")



