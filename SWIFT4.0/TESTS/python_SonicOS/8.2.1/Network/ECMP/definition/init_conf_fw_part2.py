from definition.settings_part2 import *
from definition.utils_part2 import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_config_x0(self):
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
        Assertion.assert_equal(rc1, True, "ERR: Config X2 to static failed")

    def test_02_config_x1(self):
        logger.info("config x2 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.X1_MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
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
        rc1 = interfacev4api.config_interface(**x1_static)
        rc2 = interfacev6api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 to static failed")

    def test_03_config_x2(self):
        logger.info("config x2 interface... ")
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.X2_MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
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
        rc1 = interfacev4api.config_interface(**x2_static)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 to static failed")

    def test_04_add_aos(self):
        tag = []
        X2_GW1_IP_dict = {
            'object_type': 'host',
            'name': 'X2_GW1_IP',
            'zone': 'WAN',
            'value': Parameter.X2_GW1_IP
        }
        X2_GW2_IP_dict = {
            'object_type': 'host',
            'name': 'X2_GW2_IP',
            'zone': 'WAN',
            'value': Parameter.X2_GW2_IP
        }
        X2_GW3_IP_dict = {
            'object_type': 'host',
            'name': 'X2_GW3_IP',
            'zone': 'WAN',
            'value': Parameter.X2_GW3_IP
        }
        X2_GW4_IP_dict = {
            'object_type': 'host',
            'name': 'X2_GW4_IP',
            'zone': 'WAN',
            'value': Parameter.X2_GW4_IP
        }
        X2_GW1_IPV6_dict = {
            'object_type': 'host',
            'name': 'X2_GW1_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X2_GW1_IPV6
        }
        X2_GW2_IPV6_dict = {
            'object_type': 'host',
            'name': 'X2_GW2_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X2_GW2_IPV6
        }
        X2_GW3_IPV6_dict = {
            'object_type': 'host',
            'name': 'X2_GW3_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X2_GW3_IPV6
        }
        X2_GW4_IPV6_dict = {
            'object_type': 'host',
            'name': 'X2_GW4_IPV6',
            'zone': 'WAN',
            'ip': Parameter.X2_GW4_IPV6
        }
        server_pc_ao_dict = {
            "object_type": "host",
            "name": "server_pc",
            "zone": "WAN",
            "value": Parameter.SERVER_PC
        }
        server_pc_v6_dict = {
            "object_type": "host",
            "name": "server_pc_v6",
            "zone": "WAN",
            "ip": Parameter.SERVER_PC_V6
        }

        ipv4_ao_list = [server_pc_ao_dict, X2_GW1_IP_dict, X2_GW2_IP_dict, X2_GW3_IP_dict, X2_GW4_IP_dict]
        ipv6_ao_list = [X2_GW1_IPV6_dict, X2_GW2_IPV6_dict, X2_GW3_IPV6_dict, X2_GW4_IPV6_dict, server_pc_v6_dict]

        for ao_obj in ipv4_ao_list:
            rc = aoapi.config_addressobject(**ao_obj)
            tag.append(rc)

        for ao_obj in ipv6_ao_list:
            rc = aoapi.config_ipv6_addressobject(**ao_obj)
            tag.append(rc)

        Assertion.assert_equal(all(tag), True, "ERR: add ao failed")

