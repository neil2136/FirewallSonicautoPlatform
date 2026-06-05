from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_configure_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': "12.12.1.1",
            'dns1': Parameter.X1_DNS_1,
            'dns2': Parameter.X2_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = iface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_x1_again(self):
        rc = iface_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_04_configure_x2_to_DMZ(self):
        rc = iface_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')

    def test_05_add_aos(self):
        wan_host_dict = {
            'object_type': 'host',
            'name': 'wan ao',
            'zone': 'WAN',
            'value': Parameter.X1_NAT_IP
        }
        lan_pc_dict = {
            'object_type': 'host',
            'name': 'lan pc',
            'zone': 'LAN',
            'value': PC1_ETH1_IP
        }
        dmz_host_dict = {
            'object_type': 'host',
            'name': 'dmz ao',
            'zone': 'DMZ',
            'value': Parameter.X2_NAT_IP
        }
        dmz_pc_dict = {
            'object_type': 'host',
            'name': 'dmz pc',
            'zone': 'DMZ',
            'value': PC3_ETH1_IP
        }
        ao_for_case23 = {
            'object_type': 'network',
            'name': 'ao_test_for_case_23',
            'zone': 'LAN',
            'value': "192.168.168.0" + ',' + '255.255.255.0'
        }

        wan_pool = {
            "object_type": "range",
            "name": "wan_pool",
            "zone": "WAN",
            "value": "12.12.1.166,12.12.1.170"
        }
        lan_unmap = {
            'object_type': 'host',
            'name': 'lan_unmap',
            'zone': 'LAN',
            'value': '192.168.168.200'
        }
        dmz_public = {
            'object_type': 'host',
            'name': 'dmz_pub',
            'zone': 'DMZ',
            'value': Parameter.DMZ_PUB
        }
        for ao in (
        wan_host_dict, lan_pc_dict, dmz_host_dict, dmz_pc_dict, ao_for_case23, wan_pool, lan_unmap, dmz_public):
            rc = ao_api.config_addressobject(**ao)
            if not rc:
                logger.error(f'add addr object <{ao["name"]}> failed!!')
        Assertion.assert_equal(rc, True, 'ERR: add aos failed')

    def test_06_create_service_obj(self):
        service_for_case23 = {
            'object_type': 'tcp',
            'name': 'service_for_case_23',
            'tcp': {
                'begin': 8000,
                'end': 8000
            }
        }
        service_for_case38 = {
            "object_type": "tcp",
            "name": "http_8888",
            "tcp": {
                "begin": 8888,
                "end": 8888
            }
        }
        rc1, _ = srv_api.config_service_object(**service_for_case23)
        rc2, _ = srv_api.config_service_object(**service_for_case38)
        logger.info(f'create service object service_for_case23 result: {rc1}')
        logger.info(f'create service object service_for_case38 result: {rc2}')
        Assertion.assert_equal(rc1 and rc2, True, 'ERR: add service obj for nat policy failed')

    def test_07_add_acls(self):
        acl_1 = copy.deepcopy(acl_base)
        acl_1.update({"name": "wan_to_lan_acl_ping", "service": {"group": "Ping"}})
        acl_2 = copy.deepcopy(acl_base)
        acl_2.update({"name": "wan_to_lan_acl_https", "service": {"name": "http_8888"}})
        acl_3 = copy.deepcopy(acl_base)
        acl_3.update({"name": "wan_to_dmz_acl_ping", "to": "DMZ", "service": {"group": "Ping"}})
        acl_4 = copy.deepcopy(acl_base)
        acl_4.update({"name": "dmz_to_lan_acl_ping", "from": "DMZ", "service": {"group": "Ping"}})
        for acl in (acl_1, acl_2, acl_3, acl_4):
            rc = acl_api.config_accessrule(**acl)
            if not rc:
                logger.error(f'add access rule <{acl["name"]}> failed!!')
        Assertion.assert_equal(rc, True, "ERR: add access rules failed")
