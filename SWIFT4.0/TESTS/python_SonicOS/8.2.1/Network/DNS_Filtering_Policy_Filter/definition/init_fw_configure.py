from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_register_fw(self):  
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
    
    def test_03_add_a_custom_zone(self):
        rc = zone_api.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(rc, True, "ERR: Add a custom zone failed!")
    
    def test_04_add_address_object(self):
        rc = addrObj_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add_address_object failed")
    
    def test_05_add_new_address_object(self):
        new_AO = copy.deepcopy(ao_dict)
        test = {
            'name': 'New',
            'value': '192.168.168.250'
        }
        new_AO.update(test)
        rc = addrObj_api.config_addressobject(**new_AO)
        Assertion.assert_equal(rc, True, "ERR: add_address_object failed")
    
    def test_06_disable_dns_proxy_cache(self):
        disCache = {
            'dns_cache': False
        }
        rc = dnspxy_api.config_dnsproxy(**disCache)
        Assertion.assert_equal(rc, True, "ERR: Disable DNS Proxy Cache failed")

