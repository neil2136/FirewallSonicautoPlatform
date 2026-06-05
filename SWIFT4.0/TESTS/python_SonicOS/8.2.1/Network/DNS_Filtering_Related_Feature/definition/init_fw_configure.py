from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_disable_dns_proxy_cache_and_enable_enforce_option(self):
        proxy = {
            'enforce_all_dns_requests': True,
            'dns_cache': False
        }
        rc = dnspxy_api.config_dnsproxy(**proxy)
        Assertion.assert_equal(rc, True, "ERR: disable_dns_proxy_cache_and_enable_enforce_option failed")

    def test_03_enable_split_dns(self):
        out = dnsSett_api.get_dns()
        # {"dns": {"server": {"inherit": false, "static": {"primary": "10.103.202.200", "secondary": "0.0.0.0", "tertiary": "0.0.0.0"}, "ipv6": {"inherit": false, "static": {"primary": "2001:470:80b7:852:219d:af72:ddb4:289e",
        # "secondary": "::", "tertiary": "::"}, "preferred": false}}, "rebinding": {"enable": false, "action": "log-attack-only", "allowed_domains": {}}, "fqdn_binding": false, "split_servers": false, "fqdn_over_tcp_dns": false}}
        out_dns = dict(out).get('dns')
        if out_dns and out_dns.get('split_servers'):
            rc = True
        else:
            out.update({"dns": {"split_servers": True}})
            rc = dnsSett_api.set_dns(**out)
        Assertion.assert_equal(rc, True, "ERR: enable_split_dns failed")

    @repeat_method(10)
    def test_04_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
