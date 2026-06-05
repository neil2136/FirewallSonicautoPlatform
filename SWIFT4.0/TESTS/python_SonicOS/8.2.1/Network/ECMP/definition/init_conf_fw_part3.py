from definition.settings_part3 import *
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
        logger.info("config x1 interface... ")
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

    def test_04_config_x3(self):
        logger.info("config x3 interface... ")
        x3_static = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.X3_MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
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
        rc1 = interfacev4api.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 to static failed")

    def test_05_config_x4(self):
        logger.info("config x4 interface... ")
        x4_static = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': Parameter.X4_MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x4_v6_dict = {
            'name': 'X4',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X4_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev4api.config_interface(**x4_static)
        rc2 = interfacev6api.config_interface_ipv6(**x4_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X4 to static failed")

    def test_06_config_x5(self):
        logger.info("config x5 interface... ")
        x5_static = {
            'if': 'X5',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'netmask': Parameter.X5_MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x5_v6_dict = {
            'name': 'X5',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X5_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev4api.config_interface(**x5_static)
        rc2 = interfacev6api.config_interface_ipv6(**x5_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X5 to static failed")

    def test_07_add_aos(self):
        tag = []
        GW1_IP_dict = {
            'object_type': 'host',
            'name': 'GW1_IP',
            'zone': 'WAN',
            'value': Parameter.GW1_IP
        }
        GW2_IP_dict = {
            'object_type': 'host',
            'name': 'GW2_IP',
            'zone': 'WAN',
            'value': Parameter.GW2_IP
        }
        GW3_IP_dict = {
            'object_type': 'host',
            'name': 'GW3_IP',
            'zone': 'WAN',
            'value': Parameter.GW3_IP
        }
        GW4_IP_dict = {
            'object_type': 'host',
            'name': 'GW4_IP',
            'zone': 'WAN',
            'value': Parameter.GW4_IP
        }
        GW5_IP_dict = {
            'object_type': 'host',
            'name': 'GW5_IP',
            'zone': 'WAN',
            'value': Parameter.GW5_IP
        }
        GW1_IPV6_dict= {
            'object_type': 'host',
            'name': 'GW1_IPV6',
            'zone': 'WAN',
            'ip': Parameter.GW1_IPV6
        }
        GW2_IPV6_dict = {
            'object_type': 'host',
            'name': 'GW2_IPV6',
            'zone': 'WAN',
            'ip': Parameter.GW2_IPV6
        }
        GW3_IPV6_dict = {
            'object_type': 'host',
            'name': 'GW3_IPV6',
            'zone': 'WAN',
            'ip': Parameter.GW3_IPV6
        }
        GW4_IPV6_dict = {
            'object_type': 'host',
            'name': 'GW4_IPV6',
            'zone': 'WAN',
            'ip': Parameter.GW4_IPV6
        }
        GW5_IPV6_dict = {
            'object_type': 'host',
            'name': 'GW5_IPV6',
            'zone': 'WAN',
            'ip': Parameter.GW5_IPV6
        }
        server_pc_ao_dict = {
            "object_type": "host",
            "name": "server_pc",
            "zone": "WAN",
            "value": Parameter.SERVER_PC
        }
        server_network_ao_dict = {
            "object_type": "network",
            "name": "server_network",
            "zone": "WAN",
            "value": "100.100.10.192,255.255.255.224"
        }
        server_pc_v6_dict = {
            "object_type": "host",
            "name": "server_pc_v6",
            "zone": "WAN",
            "ip": Parameter.SERVER_PC_V6
        }
        ipv6_range_source_ao_dict = {
            "object_type": "range",
            "name": "ipv6_range_source",
            "zone": "LAN",
            "begin": "2001:2018::1",
            "end": "2001:2018::20"
        }

        ipv6_network_dst_ao_dict = {
            "object_type": "network",
            "name": "ipv6_network_dst",
            "zone": "LAN",
            "subnet": "2001:1000::",
            "mask": "/64"}

        ipv6_network_source_ao_dict = {
            "object_type": "network",
            "name": "ipv6_network_source",
            "zone": "LAN",
            "subnet": "2001:2018::",
            "mask": "/64"}

        ipv4_ao_list = [server_pc_ao_dict,GW1_IP_dict, GW2_IP_dict, GW3_IP_dict, GW4_IP_dict, GW5_IP_dict,server_network_ao_dict]
        ipv6_ao_list = [GW1_IPV6_dict, GW2_IPV6_dict, GW3_IPV6_dict, GW4_IPV6_dict, GW5_IPV6_dict,
                        server_pc_v6_dict, ipv6_range_source_ao_dict, ipv6_network_dst_ao_dict, ipv6_network_source_ao_dict]

        for ao_obj in  ipv4_ao_list:
            rc = aoapi.config_addressobject(**ao_obj)
            tag.append(rc)

        for ao_obj in ipv6_ao_list:
            rc = aoapi.config_ipv6_addressobject(**ao_obj)
            tag.append(rc)

        Assertion.assert_equal(all(tag), True, "ERR: add ao failed")


class TestRestore(Test):
    uuid = 'NonTC'

    def test_01_delete_all_routings(self):
        del4res = routecli.del_route_policies('ipv4')
        logger.info(f"delete ipv4 route : {del4res}\n ")
        del6res = routecli.del_route_policies('ipv6')
        logger.info(f"delete ipv6 route : {del6res}\n ")
        Assertion.assert_equal(del4res & del6res, True, "ERR:  Check Packet fail")

    def test_02_delete_all_aos(self):
        del4res = aocli.del_address_objects('ipv4')
        logger.info(f"delete all ipv4 ao : {del4res}\n ")
        del6res = aocli.del_address_objects('ipv6')
        logger.info(f"delete all ipv6 ao : {del6res}\n ")
        Assertion.assert_equal(del4res & del6res, True, "ERR:  Check Packet fail")
