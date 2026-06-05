from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(10)
    def test_02_register_fw(self):
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class Test_Config_Switch(Test):
    uuid = 'NonTC'

    def test_00_change_untag_to_tag(self):
        osstack = Openstack(Params.testbed)
        rc = osstack.set_node_interface_state('UTM','X2:1', 'tag')
        rc &= osstack.set_node_interface_state('UTM','X2:2', 'tag')
        rc &= osstack.set_node_interface_state('UTM','X3:1', 'tag')
        Assertion.assert_equal(rc, True, "ERR: change X3 to tag.")
