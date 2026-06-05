from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_Config_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
        }
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_register_fw(self):
        license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_modify_pc1_route(self):
        logger.info('Set route on PC1 via gw {}'.format(Parameter.FIREWALL))
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_1, Parameter.Route_Mask_1, Parameter.PC1_GW))
        rc = os.system('route del default')
        rc = os.system('route add -net {} netmask {} gw {}'.format(Parameter.Route_Host_2, Parameter.Route_Mask_2, Parameter.FIREWALL))
        result = os.popen('ip -4 r')
        output = result.read()
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth0', "ERR: Modify route on PC1 failed")

    def test_04_disable_dns_cache(self):
        disCache = {
            'dns_cache': False
        }
        rc = dnspxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: test_04_disable_dns_cache failed")