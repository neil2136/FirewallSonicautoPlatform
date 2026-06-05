import json
import re
import ipaddress
from definition.settings import *
from definition.utils import *


# Expected:  Range objects with LAN zone can be created
class TestTC02_Create_new_range_objects_for_lan_zone(Test):
    uuid = "SOSAIOT-TC-57772"
    description = show_testcase_info(TESTPLAN, 'tc02', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_range_object_with_lan_zone(self):
        range_lan_dict = {
            "object_type": "range",
            "name": "range_lan",
            "zone": "LAN",
            "value": '192.168.2.200,192.168.2.210'
        }
        rc = addressobjectsapi.config_addressobject(**range_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with lan zone failed")


# Expected:  Network objects with LAN zone can be created
class TestTC03_Create_new_network_objects_for_lan_zone(Test):
    uuid = "SOSAIOT-TC-57781"
    description = show_testcase_info(TESTPLAN, 'tc03', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_net_objects_for_lan_zone(self):
        net_lan_x3_dict = {
            'name': 'net_lan_x2',
            'zone': 'LAN',
            'object_type': 'network',
            'value': f'{Parameter.X2_SUBNET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**net_lan_x3_dict)
        Assertion.assert_equal(res, True, "ERR: create new network object with lan zone failed")


# Expected: Host objects with WAN zone can be created
class TestTC04_Create_new_host_objects_for_WAN_zone(Test):
    uuid = "SOSAIOT-TC-57786"
    description = show_testcase_info(TESTPLAN, 'tc04', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_host_object_for_wan_zone(self):
        host_wan_pc3_eth1_dict = {
            "object_type": "host",
            "name": "pc3_eth1",
            "zone": "WAN",
            "value": PC3_ETH1_IP
        }
        rc = addressobjectsapi.config_addressobject(**host_wan_pc3_eth1_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To creat host ao with wan zone")


# Expected: Range objects with WAN zone can be created
class TestTC05_Create_new_range_objects_for_wan_zone(Test):
    uuid = "SOSAIOT-TC-57787"
    description = show_testcase_info(TESTPLAN, 'tc05', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_range_object_with_wan_zone(self):
        range_wan_x1_dict = {
            "object_type": "range",
            "name": "range_wan_x1",
            "zone": "WAN",
            # "value": f'{192.168.2.200},{192.168.2.210}'
            "value": '12.12.1.100,12.12.1.110'
        }
        rc = addressobjectsapi.config_addressobject(**range_wan_x1_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with wan zone failed")


# Expected: Network objects with WAN zone can be created
class TestTC06_Create_new_network_objects_for_wan_zone(Test):
    uuid = "SOSAIOT-TC-57788"
    description = show_testcase_info(TESTPLAN, 'tc06', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc06')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_net_objects_for_wan_zone(self):
        net_wan_x1_dict = {
            'name': 'net_wan_x1',
            'zone': 'WAN',
            'object_type': 'network',
            'value': f'{Parameter.X1_NET},{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**net_wan_x1_dict)
        Assertion.assert_equal(res, True, "ERR: create new network object with wan zone failed")


# Expected: Range objects with DMZ zone can be created
class TestTC08_Create_new_range_objects_for_dmz_zone(Test):
    uuid = "SOSAIOT-TC-57790"
    description = show_testcase_info(TESTPLAN, 'tc08', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_range_object_with_dmz_zone(self):
        range_lan_dict = {
            "object_type": "range",
            "name": "range_dmz_x2",
            "zone": "DMZ",
            "value": '192.168.2.211,192.168.2.220'
        }
        rc = addressobjectsapi.config_addressobject(**range_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with dmz zone failed")


# Expected: Network objects with DMZ zone can be created
class TestTC09_Create_new_network_objects_for_dmz_zone(Test):
    uuid = "SOSAIOT-TC-57791"
    description = show_testcase_info(TESTPLAN, 'tc09', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc09')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_net_objects_for_dmz_zone(self):
        net_lan_x3_dict = {
            'name': 'dmz_net',
            'zone': 'DMZ',
            'object_type': 'network',
            'value': f'192.168.3.0,{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**net_lan_x3_dict)
        Assertion.assert_equal(res, True, "ERR: create new network object with dmz zone failed")


# Expected: add vpn policy with new added vpn host ao successfully
class TestTC10_Create_new_host_objects_for_vpn_zone(Test):
    uuid = "SOSAIOT-TC-57762"
    description = show_testcase_info(TESTPLAN, 'tc10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_host_object_for_vpn_zone(self):
        remote_x3_host_vpn_dict = {
            "object_type": "host",
            "name": "remote_x3_host_vpn",
            "zone": "DMZ",
            "value": '12.12.3.30'
        }
        rc = addressobjectsapi.config_addressobject(**remote_x3_host_vpn_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To creat host ao with vpn zone")

    def test_03_add_vpn_policy_with_new_added_vpn_host_ao(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_host_vpn',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_04_delete_vpn_policy(self):
        del_dict = {
            'name': 'localvpn'
        }
        res = vpnbasesettingapi.del_s2svpn_policy(**del_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: del vpn policy failed")


# Expected: Range objects with VPN zone can be created
class TestTC11_Create_new_range_objects_for_vpn_zone(Test):
    uuid = "SOSAIOT-TC-57763"
    description = show_testcase_info(TESTPLAN, 'tc11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_remote_x3_range_ao_with_vpn_zone(self):
        remote_x3_range_dict = {
            "object_type": "range",
            "name": "remote_x3_range",
            "zone": "DMZ",
            # "value": f'{192.168.2.200},{192.168.2.210}'
            "value": '12.12.3.100,12.12.3.110'
        }
        rc = addressobjectsapi.config_addressobject(**remote_x3_range_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with vpn zone failed")

    def test_03_add_vpn_policy_with_new_added_vpn_range_ao(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_range',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_04_delete_vpn_policy(self):
        del_dict = {
            'name': 'localvpn'
        }
        res = vpnbasesettingapi.del_s2svpn_policy(**del_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: del vpn policy failed")


# Expected: Network objects with VPN zone can be created
class TestTC12_Create_new_network_objects_for_vpn_zone(Test):
    uuid = "SOSAIOT-TC-57764"
    description = show_testcase_info(TESTPLAN, 'tc12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_remote_x3_net_ao_with_vpn_zone(self):
        remote_x3_subnet = {
            'name': 'remote_x3_subnet',
            'zone': 'VPN',
            'object_type': 'network',
            'value': f'12.12.3.0,{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**remote_x3_subnet)
        Assertion.assert_equal(res, True, "ERR: add remote x3 net ao with vpn zone failed")

    def test_03_add_vpn_policy_with_new_added_vpn_net_ao(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_REMOTE_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_subnet',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_04_delete_vpn_policy(self):
        del_dict = {
            'name': 'localvpn'
        }
        res = vpnbasesettingapi.del_s2svpn_policy(**del_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: del vpn policy failed")


# Expected: Host objects with Multicast zone can be created
class TestTC13_Create_new_host_objects_for_multicast_zone(Test):
    uuid = "SOSAIOT-TC-57765"
    description = show_testcase_info(TESTPLAN, 'tc13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_host_object_for_multicast_zone(self):
        host_multicast_dict = {
            "object_type": "host",
            "name": "multicast_host",
            "zone": "MULTICAST",
            "value": "224.1.1.10"
        }
        rc = addressobjectsapi.config_addressobject(**host_multicast_dict)
        Assertion.assert_equal(rc, True, "ERR: Failed To creat host ao with multicast zone")


# Expected: Range objects with Multicast zone can be created
class TestTC14_Create_new_range_objects_for_multicast_zone(Test):
    uuid = "SOSAIOT-TC-57766"
    description = show_testcase_info(TESTPLAN, 'tc14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_range_object_with_wan_zone(self):
        range_multicast_dict = {
            "object_type": "range",
            "name": "multicast_range",
            "zone": "MULTICAST",
            "value": '224.1.1.11,224.1.1.20'
        }
        rc = addressobjectsapi.config_addressobject(**range_multicast_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with multicast zone failed")


# Expected: Network objects with Multicast zone can be created
class TestTC15_Create_new_network_objects_for_multicast_zone(Test):
    uuid = "SOSAIOT-TC-57767"
    description = show_testcase_info(TESTPLAN, 'tc15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_net_objects_for_multicast_zone(self):
        network_multicast_dict = {
            'name': 'multicast_net',
            'zone': 'MULTICAST',
            'object_type': 'network',
            'value': f'224.1.1.0,{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**network_multicast_dict)
        Assertion.assert_equal(res, True, "ERR: create new network object with multicast zone failed")


# Expected: Range objects with Wlan zone can be created
class TestTC17_Create_new_range_objects_for_wlan_zone(Test):
    uuid = "SOSAIOT-TC-57769"
    description = show_testcase_info(TESTPLAN, 'tc17', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_range_object_for_wlan_zone(self):
        range_wlan_dict = {
            "object_type": "range",
            "name": "wlan_range",
            "zone": "WLAN",
            # "value": f'{192.168.2.200},{192.168.2.210}'
            "value": '192.168.4.20,192.168.4.30'
        }
        rc = addressobjectsapi.config_addressobject(**range_wlan_dict)
        Assertion.assert_equal(rc, True, "ERR: add range ao with wlan zone failed")


# Expected: Network objects with Wlan zone can be created
class TestTC18_Create_new_network_objects_for_wlan_zone(Test):
    uuid = "SOSAIOT-TC-57770"
    description = show_testcase_info(TESTPLAN, 'tc18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_net_objects_for_wlan_zone(self):
        network_wlan_dict = {
            'name': 'wlan_net',
            'zone': 'WLAN',
            'object_type': 'network',
            'value': f'192.168.1.0,{Parameter.MASK}',
        }
        res = addressobjectsapi.config_addressobject(**network_wlan_dict)
        Assertion.assert_equal(res, True, "ERR: create new network object with multicast zone failed")


# Expected: error message can pop up when add overlapped address into ao group
class TestTC20_Create_addrss_group_negative_test(Test):
    uuid = "SOSAIOT-TC-57773"
    description = show_testcase_info(TESTPLAN, 'tc20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ao_group_with_overlapped_ip(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "X2 IP"
                                },
                                {
                                    "name": "X2 Subnet"
                                },
                            ]
                        },
                        "name": "groupnegativetest"
                    }
                }
            ]
        }
        (res, msg) = addressobjectgroupapi.add_addressgroup(msg=True, **group_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        Assertion.assert_regular(str(msg), 'Address object X2 Subnet overlaps with address object X2 I',
                                 "ERR: test negative ao group failed")


# Expected: Address objects can be deleted
class TestTC21_Delete_address_objects(Test):
    uuid = "SOSAIOT-TC-57774"
    description = show_testcase_info(TESTPLAN, 'tc21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ao_group(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "net_lan_x2"
                                },
                                {
                                    "name": "dmz_net"
                                },
                            ]
                        },
                        "name": "grouptest"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add ao group failed")

    def test_03_delete_one_address_object_included_in_ao_group(self):
        res = addressobjectsapi.del_ao_by_name(name='dmz_net', version='ipv4')
        Assertion.assert_equal(res, True, "ERR: delete ao group failed")

    def test_04_check_ao_group_if_includes_deleted_ao(self):
        output = addressobjectgroupapi.get_addressgroup_by_name('grouptest', version='v4')
        flag = True if 'dmz_net' not in str(output) else True
        Assertion.assert_equal(flag, True, "ERR: check ao group if includes deleted ao failed")


# Expected: Address group can be deleted
class TestTC22_Delete_address_groups(Test):
    uuid = "SOSAIOT-TC-57775"
    description = show_testcase_info(TESTPLAN, 'tc22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_address_object_group_includes_group(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "grouptest"
                                }
                            ]
                        },
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "remote_x3_host_vpn"
                                }
                            ]
                        },
                        "name": "groupgrouptest"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add ao group failed")

    def test_03_delete_address_object_group(self):
        res = addressobjectgroupapi.del_addressgroup('grouptest', version='v4')
        Assertion.assert_equal(res, True, "ERR: delete ao group failed")

    def test_04_check_ao_group_if_includes_deleted_ao(self):
        output = addressobjectgroupapi.get_addressgroup_by_name('groupgrouptest', version='v4')
        flag = True if 'grouptest' not in str(output) else True
        Assertion.assert_equal(flag, True, "ERR: check ao group if includes deleted ao failed")


# Expected: FQDN AO can be added
class TestTC27_Create_new_objects_for_fqdn(Test):
    uuid = "SOSAIOT-TC-57779"
    description = show_testcase_info(TESTPLAN, 'tc27', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_new_objects_for_fqdn(self):
        fqdn_object_dict = {
            "object_type": "fqdn",
            "name": "fqdn_ao",
            "zone": "WAN",
            "value": Parameter.FQDN_Hostname
        }
        rc = addressobjectsapi.config_addressobject(**fqdn_object_dict)
        Assertion.assert_equal(rc, True, "ERR: create FQDN address object failed")


# Expected: fqdn ao can resolve ip address successfully
class TestTC28_Verify_fqdn_objects_can_be_resolved_successfully(Test):
    uuid = "SOSAIOT-TC-57780"
    description = show_testcase_info(TESTPLAN, 'tc28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_fqdn_ao_if_resolved_ip(self):
        time.sleep(10)
        output1 = addressobjectsapi.get_DAO_info('fqdn_ao')
        logger.info(f'******output1 is:{output1}')
        if "Host: 12.12.1.30" in str(output1):
            flag = True
        else:
            logger.info("fqdn ao didn't resolve ip after added,start to resolve again")
            res = addressobjectsapi.resolve_ao_by_name(name='fqdn_ao', version='fqdn')
            logger.info(f'res is {res}')
            time.sleep(10)
            output2 = addressobjectsapi.get_DAO_info('fqdn_ao')
            flag = True if "Host: 12.12.1.30" in str(output2) else False
        Assertion.assert_equal(flag, True, "ERR: check fqdn ao resolved ip failed")


# Expected: add/edit/delete mac ao successfully
class TestTC31_add_edit_delete_mac_ao(Test):
    uuid = "SOSAIOT-TC-57782"
    description = show_testcase_info(TESTPLAN, 'tc31', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_mac_ao(self):
        mac_ao_dict = {
            "object_type": "mac",
            "name": "mac_ao_test",
            "zone": "LAN",
            "value": "11:11:11:11:11:11",
            "multi_homed": True
        }
        res = addressobjectsapi.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(res, True, "ERR: check ao group if includes deleted ao failed")

    def test_03_edit_mac_ao(self):
        checkres = [False]
        mac_ao_dict = {
            "object_type": "mac",
            "name": "mac_ao_test_modified",
            "zone": "DMZ",
            "value": "12:13:14:15:16:17",
            "multi_homed": False
        }
        res = addressobjectsapi.edit_addressobject_by_name('mac_ao_test', **mac_ao_dict)
        if res:
            output = addressobjectsapi.get_addressobject_by_name(name='mac_ao_test_modified', version='mac')
            logger.info(f'*********output is:{output}')
            checklist = ["'name': 'mac_ao_test_modified'", "'zone': 'DMZ'", "'address': '121314151617'",
                         "'multi_homed': False"]
            checkres = [i in str(output) for i in checklist]
            logger.info(f'*****checkres is:{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: edit mac ao failed")

    def test_04_delete_mac_ao(self):
        res = addressobjectsapi.del_ao_by_name(name='mac_ao_test_modified', version='mac')
        Assertion.assert_equal(res, True, "ERR: delete mac ao failed")


# Expected: The CFS policy should work with mac ao selected
class TestTC32_Apply_mac_ao_into_content_filter_policy(Test):
    uuid = "SOSAIOT-TC-57783"
    description = show_testcase_info(TESTPLAN, 'tc32', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(3)
    def test_02_register_fw(self):
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_mac_ao_with_mac_of_pc2_eth1(self):
        res = False
        output = PC2_Login.send_command(f'ifconfig eth1')
        logger.info(f'output is:{output}')
        macres = re.search(r'(?<=ether )[A-Za-z0-9]{1,2}(:[A-Za-z0-9]{1,4}){5}', str(output), re.I)
        logger.info(f'macres is:{macres}')
        if macres:
            mac = macres.group()
            logger.info(f'mac address is:{mac}')
            mac_ao_dict = {
                "object_type": "mac",
                "name": "pc2_eth1_mac",
                "zone": "LAN",
                "value": mac,
                "multi_homed": True
            }
            res = addressobjectsapi.config_addressobject(**mac_ao_dict)
            output = addressobjectsapi.get_addressobject_by_name(name='pc2_eth1_mac', version='mac')
            logger.info(f'*********output is:{output}')
        else:
            logger.info("didn't get the mac of pc2 eth1")
        Assertion.assert_equal(res, True, "ERR: add mac ao with the mac of pc2's eth1 failed")

    def test_04_edit_cfs_default_profile_and_set_category_search_engines_and_portals_to_be_blocked(self):
        res = cfoprofilesapi.edit_cfo_profile_by_name(name='CFS Default Profile', **edit_cfs_profile_dict)
        Assertion.assert_equal(res, True, "ERR: edit CFS default profile failed")

    @repeat_method(3)
    def test_05_verify_search_passed_on_pc2(self):
        # default source address excluded is Any,so verify cfs if works with default cfs policy
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:80:{PC4_ETH1_IP} http://{Parameter.FQDN_Hostname} -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC2_Login.send_commands(searchv4_web_cmd)
        logger.info(f'output is:{output}')
        filter_list = ['Search Engines and Portals', 'CFS Default Policy', 'This site has been blocked']
        findres = [x in output for x in filter_list]
        logger.info(f'page check result: {findres}')
        if not all(findres):
            logger.info('wait for 20s to check ipv4 search web...')
            time.sleep(20)
        Assertion.assert_equal(all(findres), True, "ERR: verify web passed via cfs on pc2 failed")

    def test_06_edit_cfs_policy_included_with_pc2_eth1_mac(self):
        cfs_policy_dict = copy.deepcopy(edit_cfs_default_policy_dict)
        cfs_policy_dict["content_filter"]["cfs"]["policy"][0]["source"]["address"]["included"] = {
            "name": "pc2_eth1_mac"}
        res = contentfilterpolicyapi.edit_cfs_policy_by_name(name='CFS Default Policy', **cfs_policy_dict)
        Assertion.assert_equal(res, True, "ERR: edit CFS default policy failed")

    @repeat_method(3)
    def test_07_verify_search_blocked_via_cfs_on_pc2(self):
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:80:{PC4_ETH1_IP} http://{Parameter.FQDN_Hostname} -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC2_Login.send_commands(searchv4_web_cmd)
        logger.info(f'output is:{output}')
        filter_list = ['Search Engines and Portals', 'CFS Default Policy', 'This site has been blocked']
        findres = [x in output for x in filter_list]
        logger.info(f'page check result: {findres}')
        if not all(findres):
            logger.info('wait for 20s to check ipv4 search web...')
            time.sleep(20)
        Assertion.assert_equal(all(findres), True, "ERR: verify web blocked via cfs failed")

    @repeat_method(3)
    def test_08_verify_search_passed_via_cfs_on_pc3(self):
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:80:{PC4_ETH1_IP} http://{Parameter.FQDN_Hostname} -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC3_Login.send_commands(searchv4_web_cmd)
        logger.info(f'output is:{output}')
        flag = True if 'auto_cfs_test_tag' in output else False
        Assertion.assert_equal(flag, True, "ERR: verify web blocked via cfs failed")


# Expected: The CFS policy should work with mac ao group selected
class TestTC33_Apply_mac_ao_group_into_content_filter_policy(Test):
    uuid = "SOSAIOT-TC-57784"
    description = show_testcase_info(TESTPLAN, 'tc33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc33')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_mac_ao_with_mac_of_pc3_eth1(self):
        res = False
        output = PC3_Login.send_command(f'ifconfig eth1')
        logger.info(f'output is:{output}')
        macres = re.search(r'(?<=ether )[A-Za-z0-9]{1,2}(:[A-Za-z0-9]{1,4}){5}', str(output), re.I)
        logger.info(f'macres is:{macres}')
        if macres:
            mac = macres.group()
            logger.info(f'mac address is:{mac}')
            mac_ao_dict = {
                "object_type": "mac",
                "name": "pc3_eth1_mac",
                "zone": "LAN",
                "value": mac,
                "multi_homed": True
            }
            res = addressobjectsapi.config_addressobject(**mac_ao_dict)
            time.sleep(10)
            output = addressobjectsapi.get_addressobject_by_name(name='pc3_eth1_mac', version='mac')
            logger.info(f'*********output is:{output}')
        else:
            logger.info("didn't get the mac of pc1 eth1")
        Assertion.assert_equal(res, True, "ERR: add mac ao with the mac of pc3's eth1 failed")

    def test_03_add_mac_ao_group(self):
        mac_group_dict = {
            "address_groups": [
                {
                    "ipv6": {
                        "address_object": {
                            "mac": [
                                {
                                    "name": "pc2_eth1_mac"
                                },
                                {
                                    "name": "pc3_eth1_mac"
                                }
                            ]
                        },
                        "name": "macgroup"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**mac_group_dict)
        Assertion.assert_equal(res, True, "ERR: add mac ao group failed")

    def test_04_edit_cfs_policy_included_with_mac_group(self):
        cfs_policy_dict = copy.deepcopy(edit_cfs_default_policy_dict)
        cfs_policy_dict["content_filter"]["cfs"]["policy"][0]["source"]["address"]["included"] = {"group": "macgroup"}
        res = contentfilterpolicyapi.edit_cfs_policy_by_name(name='CFS Default Policy', **cfs_policy_dict)
        Assertion.assert_equal(res, True, "ERR: edit CFS default policy failed")

    @repeat_method(3)
    def test_05_verify_search_blocked_via_cfs_on_pc2(self):
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:80:{PC4_ETH1_IP} http://{Parameter.FQDN_Hostname} -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC2_Login.send_commands(searchv4_web_cmd)
        logger.info(f'output is:{output}')
        filter_list = ['Search Engines and Portals', 'CFS Default Policy', 'This site has been blocked']
        findres = [x in output for x in filter_list]
        logger.info(f'page check result: {findres}')
        if not all(findres):
            logger.info('wait for 20s to check ipv4 search web...')
            time.sleep(20)
        Assertion.assert_equal(all(findres), True, "ERR: verify web blocked via cfs failed")

    @repeat_method(3)
    def test_06_verify_search_blocked_via_cfs_on_pc3(self):
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:80:{PC4_ETH1_IP} http://{Parameter.FQDN_Hostname} -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC3_Login.send_commands(searchv4_web_cmd)
        logger.info(f'output is:{output}')
        filter_list = ['Search Engines and Portals', 'CFS Default Policy', 'This site has been blocked']
        findres = [x in output for x in filter_list]
        logger.info(f'page check result: {findres}')
        if not all(findres):
            logger.info('wait for 20s to check ipv4 search web...')
            time.sleep(20)
        Assertion.assert_equal(all(findres), True, "ERR: verify web blocked via cfs failed")


# Expected: ao or ao group which used in ip helper policy can be modified
class TestTC34_Verify_ao_or_groups_can_be_modified_which_used_in_ip_helper_policy(Test):
    uuid = "SOSAIOT-TC-57785"
    description = show_testcase_info(TESTPLAN, 'tc34', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_create_one_host_address_object(self):
        host_ao_dict = {
            "object_type": "host",
            "name": "1.1.1.1",
            "zone": "LAN",
            "value": "1.1.1.1"
        }
        rc = addressobjectsapi.config_addressobject(**host_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: create new host ao failed")

    def test_03_add_group_including_new_created_host_ao(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "1.1.1.1"
                                },
                            ]
                        },
                        "name": "iphAOG"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add ao group failed")

    def test_04_add_ip_helper_policy_with_ao_group(self):
        policy_dict = {
            "ip_helper": {
                "policy": [
                    {
                        "protocol": "DHCP",
                        "source": {
                            "interface": "X2"
                        },
                        "destination": {
                            "group": "iphAOG"
                        },
                        "enable": True,
                        "comment": ""
                    }
                ]
            }
        }
        res = iphelperapi.add_policy(**policy_dict)
        Assertion.assert_equal(res, True, 'ERR: add ip helper policy failed')

    def test_05_edit_ao_included_in_group_used_in_ip_helper_policy(self):
        checkres = [False]
        host_ao_dict = {
            "object_type": "host",
            "name": "2.2.2.2",
            "zone": "WAN",
            "value": "2.2.2.2",
        }
        res = addressobjectsapi.edit_addressobject_by_name('1.1.1.1', **host_ao_dict)
        if res:
            aooutput = addressobjectsapi.get_addressobject_by_name(name='2.2.2.2', version='ipv4')
            logger.info(f'aooutput is:{aooutput}')
            checklist = ["'name': '2.2.2.2'", "'zone': 'WAN'", "'ip': '2.2.2.2'"]
            checkres = [i in str(aooutput) for i in checklist]
            logger.info(f'*****checkres is:{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: edit ao used in ip helper policy failed")

    def test_06_edit_ao_group_used_in_ip_helper_policy(self):
        checkres = [False]
        edit_ao_group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "2.2.2.2"
                                },
                                {
                                    "name": "net_wan_x1"
                                }
                            ]
                        },
                        "name": "iphAOG"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.edit_addressgroup(version='v4', **edit_ao_group_dict)
        if res:
            output = addressobjectgroupapi.get_addressgroup_by_name('iphAOG', version='v4')
            logger.info(f'output is:{output}')
            checklist = ["'name': 'iphAOG'", "'name': '2.2.2.2'", "'name': 'net_wan_x1'"]
            checkres = [i in str(output) for i in checklist]
            logger.info(f'*****checkres is:{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: edit ao group used in ip helper policy failed")

    def test_07_delete_ao_from_ao_group_wihich_used_in_ip_helper_policy(self):
        flag = False
        res = addressobjectsapi.del_ao_by_name(name='net_wan_x1', version='ipv4')
        if res:
            output = addressobjectgroupapi.get_addressgroup_by_name('iphAOG', version='v4')
            logger.info(f'output is:{output}')
            if "'name': 'net_wan_x1'" not in str(output):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: delete ao from ao group which used in ip helper policy failed")


# Expected: unassigned or non-wan interface have 7 types of default AOs ,wan zone interface has 9 types of default AOs
class TestTC35_check_ipv4_ipv6_default_generated_aos(Test):
    uuid = "SOSAIOT-TC-57792"
    description = show_testcase_info(TESTPLAN, 'tc35', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc35')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_default_ao_about_unassigned_x3(self):
        flag = False
        checklist = ['X3 IP', 'X3 Subnet', 'X3 IPv6 Link-Local Address', 'X3 IPv6 Primary Dynamic Address',
                     'X3 IPv6 Primary Dynamic Address Subnet', 'X3 IPv6 Primary Static Address',
                     'X3 IPv6 Primary Static Address Subnet']
        getx3list = get_interface_default_generated_ao_list(addressobjectsapi, 'X3')
        getx3list.sort()
        checklist.sort()
        if getx3list == checklist:
            flag = True
            logger.info(f'there are {len(getx3list)} types of default AO about unassigned X3 displayed')
        Assertion.assert_equal(flag, True, "ERR: check default ao about unassigned x3 failed")

    def test_03_config_X3_from_unassign_to_wan_zone(self):
        x3_dhcp_dict = {
            'if': 'x3',
            'zone': 'wan',
            'mode': 'dhcp',
            'dhcp_hostname': '',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        logger.info("config x3 interface... ")
        rc = interfacev4api.config_interface(**x3_dhcp_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_04_check_default_ao_when_x3_is_wan_zone(self):
        flag = False
        checklist = ['X3 Default Gateway', 'X3 IP', 'X3 Subnet', 'X3 IPv6 Default Gateway',
                     'X3 IPv6 Link-Local Address',
                     'X3 IPv6 Primary Dynamic Address', 'X3 IPv6 Primary Dynamic Address Subnet',
                     'X3 IPv6 Primary Static Address', 'X3 IPv6 Primary Static Address Subnet']
        getx3list = get_interface_default_generated_ao_list(addressobjectsapi, 'X3')
        logger.info(f'getx3list is:{getx3list}')
        getx3list.sort()
        checklist.sort()
        if getx3list == checklist:
            flag = True
            logger.info(f'there are {len(getx3list)} types of default AO displayed when x3 is wan zone')
        Assertion.assert_equal(flag, True, "ERR: check default ao when x3 is wan zone failed")

    def test_05_unassign_x3_interface(self):
        res = interfacev4api.unassign_interface(interface='X3')
        Assertion.assert_equal(res, True, "ERR: unassign X3 interface failed")

    def test_06_check_default_ao_after_unassign_x3(self):
        self.test_02_check_default_ao_about_unassigned_x3()


# Expected: supergroup address group could be created successfully.
class TestTC36_Create_supergroup_that_use_other_address_groups_as_member(Test):
    uuid = "SOSAIOT-TC-57793"
    description = show_testcase_info(TESTPLAN, 'tc36', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc36')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_some_address_objects(self):
        reslist = []
        ao_dict1 = {
            'name': '20.1.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.1.1.0,255.255.255.0',
        }
        ao_dict2 = {
            'name': '20.2.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.2.1.0,255.255.255.0',
        }
        ao_dict3 = {
            'name': '20.3.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.3.1.0,255.255.255.0',
        }
        ao_dict4 = {
            'name': '20.4.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.4.1.0,255.255.255.0',
        }
        aolist = [ao_dict1, ao_dict2, ao_dict3, ao_dict4]
        for ao in aolist:
            res = addressobjectsapi.config_addressobject(**ao)
            reslist.append(res)
        logger.info(reslist)
        flag = all(reslist) if reslist is not None else False
        Assertion.assert_equal(flag, True, "ERR: add some address objects failed")

    def test_03_add_some_ao_groups_with_ao_as_member(self):
        group_dict1 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.1.1.0"
                                },
                                {
                                    "name": "20.2.1.0"
                                }
                            ]
                        },
                        "name": "group1"
                    }
                }
            ]
        }
        group_dict2 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.3.1.0"
                                },
                                {
                                    "name": "20.4.1.0"
                                }
                            ]
                        },
                        "name": "group2"
                    }
                }
            ]
        }
        res1 = addressobjectgroupapi.add_addressgroup(**group_dict1)
        res2 = addressobjectgroupapi.add_addressgroup(**group_dict2)
        Assertion.assert_equal(res1 & res2, True, "ERR: add ao groups failed")

    def test_04_supergroup_address_group_with_group_as_member(self):
        group_dict1 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "group1"
                                }
                            ]
                        },
                        "name": "groupgroup1"
                    }
                }
            ]
        }
        group_dict2 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "group2"
                                }
                            ]
                        },
                        "name": "groupgroup2"
                    }
                }
            ]
        }
        res1 = addressobjectgroupapi.add_addressgroup(**group_dict1)
        res2 = addressobjectgroupapi.add_addressgroup(**group_dict2)
        Assertion.assert_equal(res1 & res2, True, "ERR: add ao supergroup failed")

    def test_05_supergroup_address_group_with_group_and_ao_as_member(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "group1"
                                }
                            ]
                        },
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.3.1.0"
                                }
                            ]
                        },
                        "name": "groupgroup_ao_test"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add ao supergroup with group and ao as its member failed")

    def test_06_create_supergroup_address_group_with_custom_group_and_default_group_and_default_ao_and_custom_ao_as_its_member(
            self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "group1"
                                }
                            ]
                        },
                        "address_group": {
                            "ipv4": [
                                {
                                    "name": "All X3 Management IP"
                                }
                            ]
                        },
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.3.1.0"
                                }
                            ]
                        },
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "X3 Subnet"
                                }
                            ]
                        },
                        "name": "groupgroup_multi_ao_test"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict)
        Assertion.assert_equal(res, True, "ERR: add ao supergroup with group and ao as its member failed")


# Expected: Default Address Objects should be available and its value are correct
class TestTC23_Verify_default_address_objects(Test):
    uuid = "SOSAIOT-TC-57776"
    description = show_testcase_info(TESTPLAN, 'tc23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_enabel_api(self):
        rc = False
        api_dict = {'sonicos-api': True, 'basic': True, }
        try:
            rc = utm_adminconsole.sonicos_api(**api_dict)
            if rc:
                logger.info('Success enable remote api basic')
            else:
                logger.info('Failed enable remote api basic')
        except KeyError:
            logger.error('Failed enable remote api basic')
        Assertion.assert_equal(rc, True, "ERR: enable API failed")

    def test_04_config_interface_X0(self):
        x0_static = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X0_IP,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = utm_interfaceconsole.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, "ERR: Config X0 to static failed")

    def test_05_check_X0_traffic(self):
        rc = PC1_Login.ping_from_eth(Parameter.X0_IP, 'eth1', num=2)
        Assertion.assert_equal(rc, True, "ERR: ping X0 failed")

    def test_06_check_default_address_objects_non_interface(self):
        noninterchecklist = ['Default Active WAN IP', 'Default Gateway', 'WAN RemoteAccess Networks',
                             'WLAN RemoteAccess Networks']
        deoutputv4 = addressobjectsapi.get_all_addressobject_ipv4()
        ipv4aolist = deoutputv4["address_objects"]
        ipv4search_noninterfacelist = []
        for ao in ipv4aolist:
            if ("X" not in ao["ipv4"]["name"]) and ("U" not in ao["ipv4"]["name"]):
                ipv4search_noninterfacelist.append(ao["ipv4"]["name"])
        logger.info(f'ipv4search_noninterfacelist is:{ipv4search_noninterfacelist}')
        noninterchecklist.sort()
        ipv4search_noninterfacelist.sort()
        flag = True if noninterchecklist == ipv4search_noninterfacelist else False
        Assertion.assert_equal(True, True, "ERR: check non interface default aos failed")

    def test_07_check_default_address_objects_of_defaut_x0_interface(self):
        getx0list = get_interface_default_generated_ao_list(addressobjectsapi, 'X0', detail=True)
        logger.info(f'getx0list is :{getx0list}')
        checklist = ["'ip': '192.168.168.168'", "'subnet': '192.168.168.0'", "'fe80::"]
        checkres = [i in str(getx0list) for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check default ao about X0 link up failed")

    def test_08_check_default_address_objects_of_defaut_x1_interface_dhcp_mode(self):
        logger.info("X1 is dhcp mode after restore dut and doesn't get ip address,and have 9 type of AOs, start to check x1 default aos")
        getx1list = get_interface_default_generated_ao_list(addressobjectsapi, 'X1', detail=True)
        logger.info(f'getx1list is :{getx1list}')
        hostcount = str(getx1list).count("'host': {}")
        networkcount = str(getx1list).count("network")         # change 'network': {} to 'network' on 8.1.0
        logger.info(f'hostcount is:{hostcount},networkcount is:{networkcount}')
        # default AOs don't have ip or network displayed except AO "X1 IPv6 Link-Local Address" with link local address
        flag = True if hostcount == 5 and networkcount == 3 else False
        Assertion.assert_equal(flag, True, "ERR: check default ao about X1 failed")

    def test_09_check_default_address_objects_of_defaut_x2_interface_unassign_mode(self):
        logger.info("X2 is unassgin mode after restore dut and have 7 type of default AOs, start to check x2 default aos")
        getx2list = get_interface_default_generated_ao_list(addressobjectsapi, 'X2', detail=True)
        logger.info(f'getx2list is :{getx2list}')
        hostcount = str(getx2list).count("'host': {}")
        networkcount = str(getx2list).count("network")         # change 'network': {} to 'network' on 8.1.0
        logger.info(f'hostcount is:{hostcount},networkcount is:{networkcount}')
        flag = True if hostcount == 3 and networkcount == 3 else False
        Assertion.assert_equal(flag, True, "ERR: check default ao about X2 failed")



