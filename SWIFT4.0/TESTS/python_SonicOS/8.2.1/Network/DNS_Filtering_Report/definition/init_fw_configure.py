from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize Firewall'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed!!")

    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed!!")

    def test_03_disable_dns_proxy_cache(self):
        enCache = {
            'dns_cache': False
        }
        rc = dnsProxy_api.config_dnsproxy(**enCache)
        Assertion.assert_equal(rc, True, "ERR: Enable DNS Proxy Cache failed")
    
    def test_04_add_dns_filtering_policy(self):
        rc = dnsRule_api.add_dns_rule(msg=False, **dns_filter_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filtering_policy failed!!")
