from definition.settings import *
from definition.utils import *


@paramunittest.parametrized(
    {'uuid': '1527154',
     'ao_dict': {'name': 'wlan_host', 'zone': 'WLAN', 'object_type': 'host', 'ip': '2004::2'}},
    {'uuid': '1527155',
     'ao_dict': {'name': 'vpn_network', 'zone': 'VPN', 'object_type': 'network', 'subnet': '2009::12',
                 'mask': '/64'}},
    {'uuid': '1527156',
     'ao_dict': {'name': 'multicast_host', 'zone': 'MULTICAST', 'object_type': 'host', 'ip': 'ff08::43'}},
    {'uuid': '1527157',
     'ao_dict': {'name': 'multicast_network', 'zone': 'MULTICAST', 'object_type': 'network',
                 'subnet': 'ff08::43',
                 'mask': '/64'}},
    {'uuid': '1527170',
     'ao_dict': {'name': 'wan_range', 'zone': 'WAN', 'object_type': 'range', 'begin': '2002::2',
                 'end': '2002::5'}},
    {'uuid': '1527172',
     'ao_dict': {'name': 'dmz_host', 'zone': 'DMZ', 'object_type': 'host', 'ip': '2006::2'}},
    {'uuid': '1527173',
     'ao_dict': {'name': 'dmz_network', 'zone': 'DMZ', 'object_type': 'network', 'subnet': '2011::12',
                 'mask': '/64'}},
    {'uuid': '1527160',
     'ao_dict': {'name': 'cus_zone_range', 'zone': 'cus_zone', 'object_type': 'range', 'begin': '2007::3',
                 'end': '2007::5'}},
    {'uuid': '1527158',
     'ao_dict': {'name': 'cus_zone_host', 'zone': 'cus_zone', 'object_type': 'host', 'ip': '2007::2'}},
)
class TestIpv6AddressObject_TC01(Test):

    def setParameters(self, uuid, ao_dict):
        self.uuid = uuid
        self.ao_dict = ao_dict
        self.aoname = self.ao_dict['name']
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ipv6_ao(self):
        rc = addressobj_api.config_ipv6_addressobject(**self.ao_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_02_verify_ipv6_ao_added(self):
        allv6object = addressobj_api.get_all_addressobject_ipv6()
        rc1 = self.aoname in json.dumps(allv6object)
        objectdetails = addressobj_api.get_addressobject_by_name(self.aoname, version="ipv6")
        logger.info(f"object details is {objectdetails}")
        rc2 = compare_ipv6_object_api_return_with_expected(objectdetails, self.ao_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Configure IPv6 Address Obj Failed!")

    def test_03_delete_ipv6addrobj(self):
        rc = addressobj_api.del_ao_by_name(self.aoname, version="ipv6")
        Assertion.assert_equal(rc, True, "ERR: Delete IPv6 Address Object Failed!")
