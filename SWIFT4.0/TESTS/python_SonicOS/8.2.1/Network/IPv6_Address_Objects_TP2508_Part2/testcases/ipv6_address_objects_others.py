from definition.settings import *
from definition.utils import *


class TestPurgeAll_TC2195470(Test):
    uuid = "SOSAIOT-TC-56392"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    ao_dict = {
        'name': 'purge_lan',
        'zone': 'LAN',
        'object_type': 'host',
        'ip': '2005::9'}
    tcname = ao_dict["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_host_ipv6_ao(self):
        rc = addressobj_api.config_ipv6_addressobject(**self.ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_verify_lan_host_ipv6_ao_added(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        rc1 = self.tcname in json.dumps(allv6aos)
        aodetails = addressobj_api.get_addressobject_by_name(self.tcname, version="ipv6")
        logger.info(f"aodetails is {aodetails}")
        rc2 = compare_ipv6_object_api_return_with_expected(aodetails, self.ao_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_click_purge_all(self):
        rc = addressobj_api.purge_all()
        Assertion.assert_equal(rc, True, "ERR: Purge All Failed!")

    def test_04_verify_lan_host_ipv6_ao_existed(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        rc = self.tcname in json.dumps(allv6aos)
        Assertion.assert_equal(rc, True, "ERR: Purge All IPv6 Address Obj Failed!")

    def test_05_delete_ipv6addrobj(self):
        rc = addressobj_api.del_ao_by_name(self.tcname, version="ipv6")
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")


class TestDefaultGWIpv6AOForWan_TC2195470(Test):
    uuid = "SOSAIOT-TC-56410"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_default_ao_for_unassigned_interface_x2(self):
        rc = verify_ao_list_in_ipv4_ipv6_aos(Default_Interface_Ao_list)
        Assertion.assert_equal(rc, True, "ERR: Check Default Ao For Unassigned Interface X2 Failed")

    def test_02_configure_x2_ipv4_wan(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '3.3.3.3',
            'netmask': '255.255.255.0',
            'gateway': '3.3.3.5'
        }
        rc = interface_api.config_interface(**x2_opt)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 as ipv4 WAN Failed!")

    def test_03_check_ao_for_wan_interface_x2(self):
        rc = verify_ao_list_in_ipv4_ipv6_aos(WAN_Interface_Ao_list)
        Assertion.assert_equal(rc, True, "ERR: Check Ao For WAN Interface X2 Failed")


class TestDefaultGWIpv6AOForUnassignedWan_TC2195471(Test):
    uuid = "SOSAIOT-TC-56411"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unassigned_x2_ipv4(self):
        rc = interface_api.unassign_interface(interface='X2')
        Assertion.assert_equal(rc, True, "ERR: Unassigned X2 Failed!")

    def test_02_check_default_ao_for_unassigned_interface_x2(self):
        rc = verify_ao_list_in_ipv4_ipv6_aos(Default_Interface_Ao_list)
        Assertion.assert_equal(rc, True, "ERR: Check Ao For WAN Interface X2 Failed")


class TestDeleteAoUsedInPB_TC1527168(Test):
    uuid = "SOSAIOT-TC-56405"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    ao_dict = {
        'name': 'pbr_lan',
        'zone': 'WAN',
        'object_type': 'host',
        'ip': '2009::9'}
    tcname = ao_dict["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_host_ipv6_ao(self):
        rc = addressobj_api.config_ipv6_addressobject(**self.ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_verify_lan_host_ipv6_ao_added(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        rc1 = self.tcname in json.dumps(allv6aos)
        aodetails = addressobj_api.get_addressobject_by_name(self.tcname, version="ipv6")
        logger.info(f"aodetails is {aodetails}")
        rc2 = compare_ipv6_object_api_return_with_expected(aodetails, self.ao_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_add_pbr_with_added_ao(self):
        route_policy_dict = {
            "route_policies": [
                {
                    "ipv6": {
                        "interface": "X1",
                        "metric": 20,
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "pbr_lan"
                        },
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X1 IPv6 Default Gateway"
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {
                            "auto": True
                        },
                        "name": "custom_ipv6_host",
                        "type": "standard",
                        "priority": 6,
                        "comment": "",
                        "disable_on_interface_down": False,
                        "vpn_precedence": False,
                        "tcp_acceleration": False,
                        "probe": "",
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": "",
                        }
                    }
                }
            ]
        }
        rc = route_api.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(rc, True, "ERR: Add Static Route Failed")

    def test_04_delete_ipv6addrobj_with_error(self):
        (rc1, msg_api) = addressobj_api.del_ao_by_name(self.tcname, version="ipv6", msg=True)
        logger.info(f"api response when delete a pbr used ao: {msg_api}")
        rc2 = "Object is in use by a Route Policy" in json.dumps(msg_api)
        Assertion.assert_equal(rc2, True, "ERR: Delete IPv6 Address Object Failed!")

    def test_05_delete_static_route(self):
        rc = route_api.del_route_policy_by_name("custom_ipv6_host", version='v6')
        Assertion.assert_equal(rc, True, "ERR: Del Static Route Failed")

    def test_06_delete_ipv6addrobj(self):
        rc = addressobj_api.del_ao_by_name(self.tcname, version="ipv6")
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")


class TestExportImportAo_TC1527171(Test):
    uuid = "SOSAIOT-TC-56407"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    ao_dict1 = {
        'name': 'test1',
        'zone': 'LAN',
        'object_type': 'host',
        'ip': '2005::8'}
    ao_dict2 = {
        'name': 'test2',
        'zone': 'LAN',
        'object_type': 'range',
        'begin': '2007::6',
        'end': '2007::9'
    }
    name1 = ao_dict1["name"]
    name2 = ao_dict2["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_ipv6_ao(self):
        rc1 = addressobj_api.config_ipv6_addressobject(**self.ao_dict1)
        rc2 = addressobj_api.config_ipv6_addressobject(**self.ao_dict2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_verify_lan_ipv6_ao_added(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        allv6aos_str = json.dumps(allv6aos)
        rc1 = self.name1 in allv6aos_str and self.name2 in allv6aos_str
        aodetails_1 = addressobj_api.get_addressobject_by_name(self.name1, version="ipv6")
        logger.info(f"aodetails_1 is {aodetails_1}")
        rc2 = compare_ipv6_object_api_return_with_expected(aodetails_1, self.ao_dict1)
        aodetails_2 = addressobj_api.get_addressobject_by_name(self.name2, version="ipv6")
        logger.info(f"aodetails_2 is {aodetails_2}")
        rc3 = compare_ipv6_object_api_return_with_expected(aodetails_2, self.ao_dict2)
        Assertion.assert_equal(rc1 & rc2 & rc3, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_export_exp(self):
        res = setting_api.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: Export Exp File Failed")

    def test_04_delete_ipv6addrobj(self):
        rc1 = addressobj_api.del_ao_by_name(self.name1, version="ipv6")
        rc2 = addressobj_api.del_ao_by_name(self.name2, version="ipv6")
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Delete IPv6 Address Object Failed!")

    def test_05_verify_delete_ipv6_ao_success(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        allv6aos_str = json.dumps(allv6aos)
        rc = self.name1 not in allv6aos_str and self.name2 not in allv6aos_str
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")

    def test_06_import_exp(self):
        res = setting_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: Import Exp File Failed")

    def test_07_verify_lan_ipv6_ao_added(self):
        self.test_02_verify_lan_ipv6_ao_added()

    def test_08_delete_ipv6addrobj(self):
        self.test_04_delete_ipv6addrobj()


class TestRefreshAo_TC1527162(Test):
    uuid = "SOSAIOT-TC-56401"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    ao_dict = {
        'name': 'refresh_lan',
        'zone': 'LAN',
        'object_type': 'host',
        'ip': '2008::3'}
    tcname = ao_dict["name"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_lan_host_ipv6_ao(self):
        rc = addressobj_api.config_ipv6_addressobject(**self.ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_verify_lan_host_ipv6_ao_added(self):
        allv6aos = addressobj_api.get_all_addressobject_ipv6()
        rc1 = self.tcname in json.dumps(allv6aos)
        aodetails = addressobj_api.get_addressobject_by_name(self.tcname, version="ipv6")
        logger.info(f"aodetails is {aodetails}")
        rc2 = compare_ipv6_object_api_return_with_expected(aodetails, self.ao_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_click_refresh_button(self):
        rc = []
        rc1 = addressobj_api.get_object_timestamps()
        rc.append(True if rc1 else False)
        rc2 = addressobj_api.get_object_list()
        rc.append(True if rc2 else False)
        Assertion.assert_equal(all(rc), True, "ERR: Click Refresh Failed!")

    def test_04_verify_lan_host_ipv6_ao_added(self):
        self.test_02_verify_lan_host_ipv6_ao_added()

    def test_05_delete_ipv6addrobj(self):
        rc = addressobj_api.del_ao_by_name(self.tcname, version="ipv6")
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")
