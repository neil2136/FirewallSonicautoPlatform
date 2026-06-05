from definition.settings import *
from definition.utils import *
import time


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_00_config_x1_v4(self):
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
            'user_https': False,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 ipv4 address failed")

    def test_01_01_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_config_x2(self):
        logger.info("config x2 interface... ")
        rc1 = interfacev4api.config_interface(**x2_static)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_03_config_x3(self):
        logger.info("config x3 interface... ")
        rc1 = interfacev4api.config_interface(**x3_static)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 ipv4 and ipv6 address failed")

    def test_04_config_x4(self):
        logger.info("config x4 interface... ")
        rc1 = interfacev4api.config_interface(**x4_static)
        rc2 = interfacev6api.config_interface_ipv6(**x4_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X4 ipv4 and ipv6 address failed")

    def test_05_config_x0_v6(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH_1,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        logger.info("config x0 interface... ")
        res = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X0 IPv6 address failed")


class TestInitRemoteConfig(Test):
    uuid = 'NonTC'

    def test_01_testrestore_remote(Test):
        restore_RemoteGEN7_cmd = f"python3 {defi_path}/script/restoreFW.py -ip {consvr_RemoteGEN7} -p {conport_RemoteGEN7}"
        PC1_Login.send_command(restore_RemoteGEN7_cmd)
        logger.info('.................Restore RemoteGEN7 .................')
        Assertion.assert_equal(True, True, "ERR: Restore REMOTE failed")

    def test_02_config_interface_X0(self):
        r_x0_static = {
            'if': 'X0',
            'zone': Parameter.ZONE_2,
            'mode': 'static',
            'ip': Parameter.R_X0_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = r_interfaceconsole.config_interface(**r_x0_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")

    def test_03_config_interface_X2(self):
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
            'prefix_length': Parameter.PREFIX_LENGTH_1,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = r_interfacev4api.config_interface(**r_x2_dict)
        rc2 = r_interfacev6api.config_interface_ipv6(**r_x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_04_config_interface_X3(self):
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
            'prefix_length': Parameter.PREFIX_LENGTH_1,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc1 = r_interfacev4api.config_interface(**r_x3_dict)
        rc2 = r_interfacev6api.config_interface_ipv6(**r_x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_05_add_network_ao_and_host_ao_on_remote_dut(self):
        tag = []
        ao_gateway = {
            "object_type": "host",
            "name": 'gw',
            "zone": 'WAN',
            "ip": '2001:1::168'
        }
        dest_network_ao_pc1 = {
            'name': 'dest_network_ao_pc1',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '1001:1::0',
            'mask': '/64',
        }
        dest_network_ao_pc2 = {
            'name': 'dest_network_ao_pc2',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '1001:2::0',
            'mask': '/64',
        }
        ao_lists = [ao_gateway, dest_network_ao_pc1, dest_network_ao_pc2]
        for ao in ao_lists:
            res = r_addressobjectapi.config_ipv6_addressobject(**ao)
            if res is False:
                logger.error(f'add ao {ao["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: configure AOs on remote fw failed")

    def test_06_add_ipv6_route_policy_on_remote_dut(self):
        tag = []
        dict_update_1 = {
            "name": "dest_network_test_pc1",
            "destination": {"name": "dest_network_ao_pc1"},
            "interface": "X2",
            "gateway": {"name": "gw"}
        }

        dict_update_2 = {
            "name": "dest_network_test_pc2",
            "destination": {"name": "dest_network_ao_pc2"},
            "interface": "X2",
            "gateway": {"name": "gw"}
        }
        pbr_lists = [dict_update_1, dict_update_2]
        for pbr_list in pbr_lists:
            ipv6_route_base_dict.update(pbr_list)
            res = r_routepolicyapi.add_route_policy(**ipv6_route_policy_dict)
            if res is False:
                logger.error(f'add ipv6 pbr {pbr_list["name"]} failed')
            tag.append(res)
        Assertion.assert_equal(all(tag), True, "ERR: Add ipv6 route policy on remote fw failed")


