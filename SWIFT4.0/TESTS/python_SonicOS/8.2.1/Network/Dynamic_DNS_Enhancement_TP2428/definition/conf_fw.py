from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"   
    goto_teardown = True

    def test_00_01_Set_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_Register_fw(self):
        time.sleep(10)
        rc = License_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
    
    