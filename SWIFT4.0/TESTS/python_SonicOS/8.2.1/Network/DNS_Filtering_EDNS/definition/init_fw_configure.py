from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_enable_dns_proxy_cache(self):
        enCache = {
            'dns_cache': True
        }
        rc = dnspxy_api.config_dnsproxy(**enCache)
        Assertion.assert_equal(rc, True, "ERR: Enable DNS Proxy Cache failed")

    def test_04_add_dns_filter_rule(self):
        rc = dnsRule_api.add_dns_rule(**filter_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_05_add_dns_proxy_rule(self):
        rc = dnsRule_api.add_dns_rule(**proxy_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_proxy_rule failed")

    def test_06_config_dns_server(self):
        dns_options = {"dns": {"server": {"inherit": False, "static": {
            "primary": Parameter.Neustar_server, "secondary": "0.0.0.0", "tertiary": "0.0.0.0"}, }}}
        rc = dnsSett_api.set_dns(**dns_options)
        Assertion.assert_equal(rc, True, "ERR: config_dns_server failed")
