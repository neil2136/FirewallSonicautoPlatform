from definition.settings import *
from definition.utils import *
import asyncio, time


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_v4(self):
        x1_static = {
            'if': 'X1',
            'zone': Parameter.ZONE_1,
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_x2(self):
        logger.info("config x2 interface... ")
        x2_static = {
            'if': 'X2',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.DNS1,
            # 'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev4api.config_interface(**x2_static)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 to static failed")

    def test_03_config_x3(self):
        logger.info("config x3 interface... ")
        x3_static = {
            'if': 'X3',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.DNS1,
            # 'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev4api.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 to static failed")

    def test_04_config_x4_sub_vlan_if(self):
        logger.info("config x4 interface... ")
        x4_vlan1_static = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': UTM_X4_VLAN1_ID,
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.DNS1,
            # 'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x4_vlan1_v6_dict = {
            'name': 'X4',
            'vlan': UTM_X4_VLAN1_ID,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X4_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = interfacev4api.add_interface(**x4_vlan1_static)
        rc2 = interfacev6api.config_interface_ipv6(**x4_vlan1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X4 sub vlan interface failed")

    def test_05_config_x0_v6(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X0 IPv6 static failed")

    def test_06_add_network_ao_and_host_ao_on_dut(self):
        tag = []
        ao_gateway = {
            "object_type": "host",
            "name": 'gw',
            "zone": 'WAN',
            "ip": 'fe80::1'
        }
        dest_network_ao_1 = {
            'name': 'dest_network_utm',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.UTM_DEST_NETWORK,
            'mask': '/64',
        }
        ao_lists = [ao_gateway, dest_network_ao_1]
        for ao in ao_lists:
            res = addressobjectapi.config_ipv6_addressobject(**ao)
            if res is False:
                logger.error(f'add ao {ao["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: configure AOs on dut failed")

    def test_07_add_ipv6_route_policy_on_dut(self):
        dict_update_1 = {
            "name": "test",
            "destination": {"name": "dest_network_utm"},
            "interface": "X3",
            "gateway": {"name": "gw"}
        }
        ipv6_route_base_dict.update(dict_update_1)
        res = routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy on remote dut failed")


class TestInitRemoteConfig(Test):
    uuid = 'NonTC'

    def test_01_testrestore_remote(Test):
        restore_RemoteGEN7_cmd = f"nohup python3 {defi_path}/script/restoreFW.py -ip {consvr_RemoteGEN7} -p {conport_RemoteGEN7} > /tmp/resotreLbox.log 2>&1 &"
        PC1_Login.send_command(restore_RemoteGEN7_cmd)
        time.sleep(400)
        logger.info('.................Restore RemoteGEN7 .................')
        Assertion.assert_equal(True, True, "ERR: Restore REMOTE failed")

    def test_02_config_interface_x0(self):
        r_x0_static = {
            'if': 'X0',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.R_X0_IP,
            'netmask': Parameter.MASK,
            'management https': True,
            'management ssh': True,
            'management ping': True,
            'user_login_https': True,
            'management snmp': True,
        }
        rc = remotegen7_interfaceconsole.config_interface(**r_x0_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")

    def test_03_config_interface_x2(self):
        r_x2_dict = {
            'if': 'X2',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.R_X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        r_x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.R_X2_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = r_interfacev4api.config_interface(**r_x2_dict)
        rc2 = r_interfacev6api.config_interface_ipv6(**r_x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_04_config_interface_x3(self):
        r_x3_dict = {
            'if': 'X3',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.R_X3_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        r_x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.R_X3_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = r_interfacev4api.config_interface(**r_x3_dict)
        rc2 = r_interfacev6api.config_interface_ipv6(**r_x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 address failed")

    def test_05_config_interface_x4(self):
        logger.info("config x4 interface... ")
        x4_vlan1_static = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': REMOTRGEN7_X4_VLAN1_ID,
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.R_X4_IP,
            'netmask': Parameter.MASK,
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.DNS1,
            # 'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x4_vlan1_v6_dict = {
            'name': 'X4',
            'vlan': REMOTRGEN7_X4_VLAN1_ID,
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.R_X4_IPV6,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = r_interfacev4api.add_interface(**x4_vlan1_static)
        rc2 = r_interfacev6api.config_interface_ipv6(**x4_vlan1_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X4 to static failed")

    def test_06_add_network_ao_and_host_ao_on_remote_dut(self):
        tag = []
        ao_gateway = {
            "object_type": "host",
            "name": 'gw',
            "zone": 'WAN',
            "ip": 'fe80::1'
        }
        dest_network_ao_1 = {
            'name': 'dest_network_remote',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': Parameter.REMOTE_DEST_NETWORK,
            'mask': '/64',
        }

        ao_lists = [ao_gateway, dest_network_ao_1]
        for ao in ao_lists:
            res = r_addressobjectapi.config_ipv6_addressobject(**ao)
            if res is False:
                logger.error(f'add ao {ao["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: configure AOs failed on remote failed")

    def test_07_add_ipv6_route_policy_on_remote_dut(self):
        dict_update_1 = {
            "name": "test",
            "destination": {"name": 'dest_network_remote'},
            "interface": "X3",
            "gateway": {"name": "gw"}
        }
        ipv6_route_base_dict.update(dict_update_1)
        res = r_routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add ipv6 route policy on remote dut failed")


