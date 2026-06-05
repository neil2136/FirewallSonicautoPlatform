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
        ao1_dict = {
            "object_type": "host",
            "name": CaseParams.wan_host_ip,
            "zone": "LAN",
            "value": CaseParams.wan_host_ip
        }
        ao2_dict = {
            "object_type": "host",
            "name": CaseParams.out_wan_host_ip,
            "zone": "LAN",
            "value": CaseParams.out_wan_host_ip
        }
        ao3_dict = {
            "object_type": "range",
            "name": CaseParams.include_x1_ip_range,
            "zone": "LAN",
            "value": '12.12.1.40,12.12.1.170'
        }
        ao4_dict = {
            "object_type": "range",
            "name": CaseParams.include_x1_gw_range,
            "zone": "LAN",
            "value": '12.12.1.1,12.12.1.20'
        }
        ao5_dict = {
            "object_type": "range",
            "name": CaseParams.in_wan_range1,
            "zone": "LAN",
            "value": '12.12.1.10,12.12.1.100'
        }
        ao6_dict = {
            "object_type": "range",
            "name": CaseParams.in_wan_range2,
            "zone": "LAN",
            "value": '12.12.1.90,12.12.1.120'
        }
        ao7_dict = {
            "object_type": "range",
            "name": CaseParams.in_wan_range3,
            "zone": "LAN",
            "value": '12.12.1.171,12.12.1.200'
        }
        ao8_dict = {
            "object_type": "range",
            "name": CaseParams.out_wan_range,
            "zone": "LAN",
            "value": '22.22.22.171,22.22.22.200'
        }
        ao9_dict = {
            "object_type": "range",
            "name": CaseParams.x3_network_range,
            "zone": "LAN",
            "value": '192.168.3.10,192.168.3.200'
        }
        ao_list = [ao1_dict, ao2_dict, ao3_dict, ao4_dict, ao5_dict, ao6_dict, ao7_dict, ao8_dict, ao9_dict]
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

    def test_04_config_x4(self):
        x4_dmz_dict = {
            'if': 'X4',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '33.33.33.33',
            'mgmt_https': True,
            'mgmt_ssh': True,
        }
        rc = interfaceapi.config_interface(**x4_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
