from definition.settings import *


class Test_Config_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_00_config_x1(self):
        rc = iface_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed!')

    def test_01_01_register_fw(self):
        for i in range(10):
            sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_config_x2(self):
        rc = iface_v4_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed!')

    def test_03_config_log_setting_for_nat_mapping(self):
        rc = logset_api.edit_event(event_id='1197', **event_1197)
        Assertion.assert_equal(rc, True, "ERR: config log settings for ntp failed.")

    def test_04_add_acl_wan_to_dmz(self):
        acl_dict = copy.deepcopy(acl_base)
        acl_dict.update({"name": "wan_to_dmz", "to": "DMZ", "service": {"name": "HTTPS"}})
        acl_json = {"access_rules": [{"ipv4": acl_dict}]}
        rc = acl_api.add_accessrule(**acl_json)
        Assertion.assert_equal(rc, True, 'ERR: add acl from WAN to DMZ failed!')

    def test_05_add_NAT_addr_obj(self):
        dmz_nat = {
            "object_type": 'host',
            'name': 'NAT_DMZ',
            'zone': 'WAN',
            'value': Parameter.NAT_IP_DMZ
        }
        lan_nat = {
            "object_type": 'host',
            'name': 'NAT_LAN',
            'zone': 'WAN',
            'value': Parameter.NAT_IP_LAN
        }
        lan_host = {
            "object_type": 'host',
            'name': 'lan_host',
            'zone': 'LAN',
            'value': PC1_ETH1_IP
        }
        dmz_host = {
            "object_type": 'host',
            'name': 'dmz_host',
            'zone': 'DMZ',
            'value': PC3_ETH1_IP
        }
        for ao in (lan_host, dmz_host, lan_nat, dmz_nat):
            rc = ao_api.config_addressobject(**ao)
            if not rc:
                logger.info(f'add addr object for <{ao["name"]}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: add addr obj for nat rule failed!!')

    def test_06_add_nat_rule_wan_to_dmz(self):
        init_dict = copy.deepcopy(nat_base)
        edit_dict = {
            'name': 'tc1529560',
            "destination": {"name": 'NAT_DMZ'},
            "translated_destination": {"name": "dmz_host"}
        }
        init_dict.update(edit_dict)
        nat_v4_json = {"nat_policies": [{"ipv4": init_dict}]}
        rc = nat_api.add_nat_policy(**nat_v4_json)
        Assertion.assert_equal(rc, True, 'ERR: add nat rule for WAN to DMZ failed!!')

    def test_07_add_syslog_server(self):
        ao_param = {
            "object_type": "host",
            "name": "syslog_server",
            "zone": "LAN",
            "value": PC1_ETH1_IP,
        }
        rc1 = ao_api.config_addressobject(**ao_param)
        logger.info(f'config addr object for syslog server result: {rc1}')
        syslog_para = {
            'name': 'syslog_server',
            'profile': 0
        }
        res = syslog_api.add_syslog_server(**syslog_para)
        Assertion.assert_equal(res, True, "ERR: Add syslog server failed")

    def test_08_config_x0_ipv6(self):
        rc = iface_v6_api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(rc, True, 'ERR: config ipv6 add for X0 failed!!')

    def test_09_config_x1_ipv6(self):
        rc = iface_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc, True, 'ERR: config ipv6 add for X0 failed!!')
