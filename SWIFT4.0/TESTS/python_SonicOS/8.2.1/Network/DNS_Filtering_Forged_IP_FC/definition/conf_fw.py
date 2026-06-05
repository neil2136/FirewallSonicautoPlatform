from ast import Param
from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed" 
    goto_teardown = True

    def test_01_Config_X1_to_register_fw(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GW,
            'dns1': Params.G_DNS1,
        }
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_register_fw(self):
        license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X1_IP,
            'gateway': Parameter.DUT_X1_GW,
            'dns1': Parameter.DNS_SERVER,
        }
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_04_modify_pc1_route(self):
        logger.info('Set route on PC1 via gw {}'.format(Parameter.DUT_X0_IP))
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_1, Parameter.Route_Mask_1, Parameter.PC1_GW))
        rc = os.system('route del default')
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_2, Parameter.Route_Mask_2, Parameter.DUT_X0_IP))
        result = os.popen('ip -4 r')
        output = result.read()
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth2', "ERR: Modify route on PC1 failed")

    def test_05_start_dns_server(self):
        pc2_ssh = Host(Params.testbed + '-PC2')
        pc2_ssh.send_command('\cp -f ' + os.environ["PYTHON_SONICOS_HOME"] + '/Network/DNS_Proxy/confs/*' + ' /etc/')
        pc2_ssh.start_service('dnsmasq')
        time.sleep(2)
        rc = pc2_ssh.send_command('service dnsmasq status')
        Assertion.assert_regular(str(rc), 'is running', f"ERR: start dns server failed.")

    def test_06_add_dns_filtering_profile(self):
        add_file = {  
            "dns_security": {
                "dns_filtering": {
                    "profile": [
                        {
                            "name": "test",
                            "actions": "{\"1\":0,\"2\":3,\"3\":0,\"4\":0,\"5\":0,\"6\":0,\"7\":0,\"8\":0,\"9\":0,\"10\":0,\"11\":0,\"12\":0,\"13\":0,\"14\":0,\"15\":0,\"16\":0,\"17\":0,\"18\":0,\"19\":0}"

                        }
                    ]
                }
            }
        }
        rc = config_forged_ip_obj.add_dns_filtering_profile(**add_file)
        Assertion.assert_equal(rc, True, "ERR: Add_dns_filtering_profile failed")

    