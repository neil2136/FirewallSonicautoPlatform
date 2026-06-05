from definition.settings import *


class TestInit_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_config_x0(self):
        logger.info("config x0 ipv6 interface ... ")
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(rc1, True, "ERR: Config X0 to static failed")

    def test_01_01_config_interface_X1(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x1_static)
        rc2 = interfacev6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    def test_02_config_interface_X2(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'gateway': Parameter.X2_GW,
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X2_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x2_static)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    def test_03_config_interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'gateway': Parameter.X3_GW,
            'dns1': Parameter.DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfaceapi.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X1 to static failed")

    def test_04_add_aos(self):
        tag = []
        X1_GW_IPV6_dict = {
            'object_type': 'host',
            'name': 'X1_GW_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X1_GW_IPV6
        }
        X2_GW_IPV6_dict = {
            'object_type': 'host',
            'name': 'X2_GW_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X2_GW_IPV6
        }
        X3_GW_IPV6_dict = {
            'object_type': 'host',
            'name': 'X3_GW_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X3_GW_IPV6
        }
        ipv6_dst_dict = {
            "object_type": "host",
            "name": "ipv6_host",
            "zone": "WAN",
            "ip": Parameter.IPV6_DST_HOST
        }
        ipv4_dst_dict = {
            "object_type": "host",
            "name": "ipv4_host",
            "zone": "WAN",
            "value": Parameter.DST_HOST
        }

        (aores, msg) = aoapi.config_addressobject(msg=True, **ipv4_dst_dict)
        if aores is False:
            aores = True if 'Already exists' in str(msg) else False
        tag.append(aores)

        ipv6_ao_list = [X1_GW_IPV6_dict, X2_GW_IPV6_dict, X3_GW_IPV6_dict, ipv6_dst_dict]
        for ao_obj in ipv6_ao_list:
            (aores, msg) = aoapi.config_ipv6_addressobject(msg=True, **ao_obj)
            if aores is False:
                aores = True if 'Already exists' in str(msg) else False
            tag.append(aores)

        Assertion.assert_equal(all(tag), True, "ERR: add ao failed")



