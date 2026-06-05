from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_add_ao_and_custom_zone(self):
        aores = []
        fqdn1_dict = {
            'name': 'A.dns.baidu.com',
            'zone': 'WAN',
            'object_type': 'fqdn',
            'value': 'dns.baidu.com',
            'dns_ttl': 0
        }
        fqdn2_dict = {
            'name': 'A.pc2.baidu.com',
            'zone': 'WAN',
            'object_type': 'fqdn',
            'value': 'pc2.baidu.com',
            'dns_ttl': 0
        }
        fqdn3_dict = {
            'name': 'A.pc3.baidu.com',
            'zone': 'WAN',
            'object_type': 'fqdn',
            'value': 'pc3.baidu.com',
            'dns_ttl': 0
        }
        fqdn4_dict = {
            'name': 'A.ipv6.baidu.com',
            'zone': 'WAN',
            'object_type': 'fqdn',
            'value': 'ipv6.baidu.com',
            'dns_ttl': 0
        }
        ao1_dict = {
            "object_type": "host",
            "name": CaseParams.wan_host_ip,
            "zone": "LAN",
            "value": CaseParams.wan_host_ip
        }
        range1_dict = {
            "object_type": "range",
            "name": CaseParams.in_wan_range1,
            "zone": "LAN",
            "value": '12.12.1.30,12.12.1.40'
        }
        ao_list = [fqdn1_dict, fqdn2_dict, fqdn3_dict, fqdn4_dict, ao1_dict, range1_dict]
        for ao in ao_list:
            (res, aomsg) = aoapi.config_addressobject(msg=True, **ao)
            if res is False:
                res = True if 'Already exists' in str(aomsg) else False
            aores.append(res)
        logger.info(f'add aos result: {aores}')

        base_dict = {
            'name': CaseParams.custom_zone,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        (zoneres, zonemsg) = zonesapi.add_zone_object(msg=True, **trusted_dict)
        if zoneres is False:
            zoneres = True if 'Already exists' in str(zonemsg) else False
        Assertion.assert_equal(all(aores) & zoneres, True, "ERR: add ao failed")


