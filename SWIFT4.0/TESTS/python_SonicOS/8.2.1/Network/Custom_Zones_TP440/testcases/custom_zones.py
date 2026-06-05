from definition.settings import *
from definition.utils import *
import copy


class TestNagetive_TC57832(Test):
    uuid = 'SOSAIOT-TC-57832'
    description = "add a exist default zone"

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-57832')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_exist_default_zone(self):
        zone_json = copy.deepcopy(custom_zone_dict)
        zone_json['zones'][0]['name'] = 'LAN'
        output, msg = zonesapi.add_zone_object(msg=True, **zone_json)
        res = "already exists" in str(msg).lower()
        Assertion.assert_equal(res, True, "ERR: test add exist default zone failed.")


class TestNagetive_TC57833(Test):
    uuid = 'SOSAIOT-TC-57833'
    description = "add a exist custom zone"
    czname = 'zone_TC57833'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SOSAIOT-TC-57833')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_trusted_custom_zone(self):
        zone_dict = {"zones": [{
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }]}
        output, msg = zonesapi.add_zone_object(msg=True, **zone_dict)
        if not output:
            res = "already exists" in str(msg).lower()
            Assertion.assert_equal(res, True, "ERR: add customer zone failed")

    def test_02_add_exist_custom_zone(self):
        zone_json = copy.deepcopy(custom_zone_dict)
        zone_json['zones'][0]['name'] = self.czname
        output, msg = zonesapi.add_zone_object(msg=True, **zone_json)
        res = "already exists" in str(msg).lower()
        Assertion.assert_equal(res, True, "ERR: test add exist custom zone failed.")

    def test_03_delete_custom_zone(self):
        output = zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: delete custom zone failed")


# Expected: Add a zone with Trusted Security Type successful
class TestCZones_TC01(Test):
    uuid = "SOSAIOT-TC-57800"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']
    czname = 'tc01_addzone_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_trusted_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=base_dict['name'])
            output = check_custom_zones(base_dict, showres)
            zonesapi.delete_zone_object(name=base_dict['name'])
        Assertion.assert_equal(output,
                               True,
                               "ERR: add customer zone with Trusted Security Type failed")


# Expected: Add a zone with Public Security Type successful
class TestCZones_TC02(Test):
    uuid = "SOSAIOT-TC-57802"
    description = show_testcase_info(TESTPLAN, '02', description=True)['title']
    czname = 'tc02_addzone_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_public_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=base_dict['name'])
            output = check_custom_zones(base_dict, showres)
            zonesapi.delete_zone_object(name=base_dict['name'])
        Assertion.assert_equal(output,
                               True,
                               "ERR: add customer zone with Public Security Type failed")


# Expected: edit Security Type successful
class TestCZones_TC03(Test):
    uuid = "SOSAIOT-TC-57822"
    description = show_testcase_info(TESTPLAN, '03', description=True)['title']
    czname1 = 'tc03_edit_zone_test1'
    czname2 = 'tc03_edit_zone_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_test1_zone(self):
        base_dict = {
            'name': self.czname1,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        base_dict['security_type'] = 'public'
        output &= zonesapi.edit_zone_object(self.czname1, **trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(base_dict['name'])
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: edit test1 zone failed")

    def test_02_edit_test2_zone(self):
        base_dict = {
            'name': self.czname2,
            'security_type': 'public',
            'interface_trust': True,
        }
        public_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**public_dict)
        base_dict['security_type'] = 'trusted'
        output &= zonesapi.edit_zone_object(self.czname2, **public_dict)
        if output:
            showres = zonesapi.show_zone_object(base_dict['name'])
            output &= check_custom_zones(base_dict, showres)

        # init custom zones
        zonesapi.delete_zone_object(self.czname1)
        zonesapi.delete_zone_object(self.czname2)
        Assertion.assert_equal(output, True, "ERR: edit test2 zone failed")


# Expected: edit Interface Trust successful
class TestCZones_TC04(Test):
    uuid = "SOSAIOT-TC-57827"
    description = show_testcase_info(TESTPLAN, '04', description=True)['title']
    czname = 'tc04_editzone_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_interface_trust(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=base_dict['name'])
            output &= check_custom_zones(base_dict, showres)
            if output:
                base_dict['interface_trust'] = False
                output &= zonesapi.edit_zone_object(self.czname, **trusted_dict)
                if output:
                    showres = zonesapi.show_zone_object(self.czname)
                    output &= check_custom_zones(base_dict, showres)

            zonesapi.delete_zone_object(self.czname)
        Assertion.assert_equal(output, True, "ERR: edit security type failed")


# Expected: edit Content Filtering successful
# don't support by G7, skip it
class TestCZones_TC05(Test):
    uuid = 'A5708FE4-0464-11DE-860E-445A00F93527'
    description = show_testcase_info(TESTPLAN, '05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")


# Expected: edit Anti-Virus successful
class TestCZones_TC06(Test):
    uuid = "SOSAIOT-TC-57828"
    description = show_testcase_info(TESTPLAN, '06', description=True)['title']
    czname = 'tc06_avzone_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_anti_virus(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
            'gateway_anti_virus': True
        }
        av_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**av_dict)
        if output:
            showres = zonesapi.show_zone_object(self.czname)
            output &= check_custom_zones(base_dict, showres)
            if output:
                base_dict['gateway_anti_virus'] = False
                output &= zonesapi.edit_zone_object(self.czname, **av_dict)
                if output:
                    base_dict['gateway_anti_virus'] = False
                    showres = zonesapi.show_zone_object(self.czname)
                    output &= check_custom_zones(base_dict, showres)

        zonesapi.delete_zone_object(self.czname)
        Assertion.assert_equal(output, True, "ERR: edit gateway_anti_virus failed")


# Expected: add interface to a custom zone successful
class TestCZones_TC07(Test):
    uuid = "SOSAIOT-TC-57829"
    description = show_testcase_info(TESTPLAN, '07', description=True)['title']
    czname = 'tc07_interadd_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_interface_x2(self):
        output2 = False
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = zonesapi.add_zone_object(**zones_dict)
        interfacev4api.config_interface(**x2_dict)
        if output:
            showres = zonesapi.show_zone_object(self.czname)
            output &= check_custom_zones(base_dict, showres)
            if output:
                output &= interfacev4api.config_interface(**x2_dict)
                if output:
                    zonesres = zonesapi.get_reporting_zones_objects()
                    for zone in zonesres:
                        if zone['name'] == self.czname:
                            if zone['member_interfaces'] == x2_dict['if']:
                                output2 = True

        # init x2 configure and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(self.czname)

        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")


# Expected: add X2 X3 interface to a custom zone successful
class TestCZones_TC08(Test):
    uuid = "SOSAIOT-TC-57830"
    description = show_testcase_info(TESTPLAN, '08', description=True)['title']
    czname = 'tc08_multiple_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == x2_dict['if']:
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_edit_interface_x3(self):
        output2 = False
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == 'X2, X3':
                    output2 = True

        # init x2 x3 configure and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)

        Assertion.assert_equal(output & output2, True, "ERR: edit interface x3 failed")


# Expected: Remove X2 interface from custom zone successful
class TestCZones_TC09(Test):
    uuid = "SOSAIOT-TC-57831"
    description = show_testcase_info(TESTPLAN, '09', description=True)['title']
    czname = 'tc09_remove_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '09')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == x2_dict['if']:
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_remove_interface_x2(self):
        output2 = False
        output = interfacev4api.unassign_interface(interface='X2')
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                print(zone)
                if zone['name'] == self.czname:
                    if zone['member_interfaces'] == 'N/A' or zone['member_interfaces'] is None:
                        output2 = True

        # init custom zone
        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output & output2, True, "ERR: remove interface x2 failed")


# Expected: remove X2 X3 interface to a custom zone successful
class TestCZones_TC10(Test):
    uuid = "SOSAIOT-TC-57806"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']
    czname = 'tc10_multremove_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == x2_dict['if']:
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_edit_interface_x3(self):
        output2 = False
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == 'X2, X3':
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x3 failed")

    def test_04_remove_interface_x2_x3(self):
        output2 = False
        output = interfacev4api.unassign_interface(interface='X2')
        output &= interfacev4api.unassign_interface(interface='X3')
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname:
                    if zone['member_interfaces'] == 'N/A' or zone['member_interfaces'] is None:
                        output2 = True

        # init custom zone
        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output & output2, True, "ERR: remove interface x2 x3 failed")


# Expected: TestObject is shown in the Address Objects table with in a custom zone successful
class TestCZones_TC11(Test):
    uuid = "SOSAIOT-TC-57807"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']
    czname = 'tc11_ao_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_add_ao_with_custom_zone(self):
        output2 = False
        ao_dict = {
            "object_type": "host",
            "name": "custom_host",
            "zone": self.czname,
            "value": '12.13.14.15'
        }
        output = aoapi.config_addressobject(**ao_dict)
        if output:
            showres = aoapi.get_addressobject_by_name(ao_dict['name'], 'ipv4')
            try:
                if showres['address_objects'][0]['ipv4']['zone'] == self.czname:
                    output2 = True
            except Exception as e:
                logger.error(repr(e))

        Assertion.assert_equal(output & output2, True, "ERR: add ao with custom zone failed")


# Expected: remove custom Address Objects successful
class TestCZones_TC12(Test):
    uuid = "SOSAIOT-TC-57808"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']
    czname = 'tc11_ao_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_remove_ao_with_custom_zone(self):
        ao_dict = {
            "ip_type": "ipv4",
            "name": "custom_host",
        }
        output = aoapi.del_addressobject(**ao_dict)

        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: remove ao with custom zone failed")


# Expected: Move x2 interface from one zone to x3 successful
class TestCZones_TC13(Test):
    uuid = "SOSAIOT-TC-57809"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']
    czname1 = 'tc13_move_test1'
    czname2 = 'tc13_move_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_two_custom_zones(self):
        cz_dict = custom_zone_dict['zones'][0]
        cz_dict['name'] = self.czname1
        output = zonesapi.add_zone_object(**custom_zone_dict)
        cz_dict['name'] = self.czname2
        output &= zonesapi.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zones failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname1,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            interes = interfacev4api.get_interface_status(x2_dict['if'])
            try:
                if interes['interfaces'][0]['ipv4']['ip_assignment']['zone'] == self.czname1:
                    output2 = True
            except Exception as e:
                logger.error(repr(e))
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_move_interface_x2_zone(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname2,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            interes = interfacev4api.get_interface_status(x2_dict['if'])
            try:
                if interes['interfaces'][0]['ipv4']['ip_assignment']['zone'] == self.czname2:
                    output2 = True
            except Exception as e:
                logger.error(repr(e))

        # init x2 configure and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.czname1)
        zonesapi.delete_zone_object(name=self.czname2)
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")


# Expected: Move a ao from one zone to anther successful
class TestCZones_TC14(Test):
    uuid = "SOSAIOT-TC-57810"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']
    czname1 = 'tc14_moveao_test1'
    czname2 = 'tc14_moveao_test2'
    aoname = 'tc14_aoname_host'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_two_custom_zones(self):
        cz_dict = custom_zone_dict['zones'][0]
        cz_dict['name'] = self.czname1
        output = zonesapi.add_zone_object(**custom_zone_dict)
        cz_dict['name'] = self.czname2
        output &= zonesapi.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zones failed")

    def test_02_add_ao_with_custom_zone1(self):
        output2 = False
        ao_dict = {
            "object_type": "host",
            "name": self.aoname,
            "zone": self.czname1,
            "value": '12.13.14.15'
        }
        output = aoapi.config_addressobject(**ao_dict)
        if output:
            showres = aoapi.get_addressobject_by_name(self.aoname, 'ipv4')
            try:
                if showres['address_objects'][0]['ipv4']['zone'] == self.czname1:
                    output2 = True
            except Exception as e:
                logger.error(repr(e))
        Assertion.assert_equal(output & output2, True,
                               "ERR: add ao with custom zone1 failed")

    def test_03_move_zone1_to_zone2_in_ao(self):
        output2 = False
        ao_edit_dict = {
            "address_objects": [{
                "ipv4": {
                    "name": self.aoname,
                    "host": {
                        "ip": "12.13.14.15"
                    },
                    "zone": self.czname2
                }
            }]
        }
        output = aoapi.edit_addressobject(object_type="host",
                                          object_path="name",
                                          obj_name_uuid=self.aoname,
                                          ip_type="ipv4",
                                          json_put=ao_edit_dict)
        if output:
            showres = aoapi.get_addressobject_by_name(self.aoname, 'ipv4')
            try:
                if showres['address_objects'][0]['ipv4']['zone'] == self.czname2:
                    output2 = True
            except Exception as e:
                logger.error(repr(e))

        # init ao configure and custom zone
        ao_dict = {
            "ip_type": "ipv4",
            "name": self.aoname,
        }
        output = aoapi.del_addressobject(**ao_dict)
        zonesapi.delete_zone_object(name=self.czname1)
        zonesapi.delete_zone_object(name=self.czname2)
        Assertion.assert_equal(output & output2, True,
                               "ERR: move custom zone1 to zone2 in ao failed")


# Expected: delete a custom zone use delete zones button successful
class TestCZones_TC15(Test):
    uuid = "SOSAIOT-TC-57801"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']
    czname = 'tc15_del_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_01_delete_custom_zone(self):
        output = zonesapi.delete_zone_object(self.czname)
        Assertion.assert_equal(output, True, "ERR: delete custom zone failed")


# Expected: delete a custom zone use delete button successful
class TestCZones_TC16(Test):
    uuid = "SOSAIOT-TC-57811"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']
    czname = 'tc16_del_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_01_delete_custom_zone(self):
        output = zonesapi.delete_zone_object(self.czname)
        Assertion.assert_equal(output, True, "ERR: delete custom zone failed")


# Expected: delete multiple custom zone use delete button successful
class TestCZones_TC17(Test):
    uuid = "SOSAIOT-TC-57812"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']
    czname1 = 'tc17_del_test1'
    czname2 = 'tc17_del_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        cz_dict = custom_zone_dict['zones'][0]
        cz_dict['name'] = self.czname1
        output = zonesapi.add_zone_object(**custom_zone_dict)
        cz_dict['name'] = self.czname2
        output &= zonesapi.add_zone_object(**custom_zone_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_01_delete_custom_zone(self):
        output = zonesapi.delete_zone_object(self.czname1)
        output &= zonesapi.delete_zone_object(self.czname2)
        Assertion.assert_equal(output, True, "ERR: delete custom zone failed")


# Expected: Remove X2 interface and custom zone successful
class TestCZones_TC18(Test):
    uuid = "SOSAIOT-TC-57813"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']
    czname = 'tc18_rm_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == x2_dict['if']:
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_remove_interface_x2(self):
        output2 = False
        output = interfacev4api.unassign_interface(interface='X2')
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname:
                    if zone['member_interfaces'] == 'N/A' or zone['member_interfaces'] is None:
                        output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: remove interface x2 failed")

    def test_04_remove_custom_zone(self):
        output = zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: remove custom zone failed")


# Expected: Remove ao and custom zone successful
class TestCZones_TC19(Test):
    uuid = "SOSAIOT-TC-57814"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']
    czname = 'tc19_rm_test1'
    aoname = 'tc19_rm_host'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_add_remove_custom_ao(self):
        ao_add_dict = {
            "object_type": "host",
            "name": self.aoname,
            "zone": self.czname,
            "value": '92.19.18.17'
        }
        ao_del_dict = {
            "ip_type": "ipv4",
            "name": self.aoname,
        }
        output = aoapi.config_addressobject(**ao_add_dict)
        output &= aoapi.del_addressobject(**ao_del_dict)
        Assertion.assert_equal(output, True, "ERR: add and delete custom zone failed")

    def test_04_remove_custom_zone(self):
        output = zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: remove custom zone failed")


# Expected: Remove custom zone in x2 get error msg successful
class TestCZones_TC20(Test):
    uuid = "SOSAIOT-TC-57815"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']
    czname = 'tc20_rm_error_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        output2 = False
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        if output:
            zonesres = zonesapi.get_reporting_zones_objects()
            for zone in zonesres:
                if zone['name'] == self.czname and zone['member_interfaces'] == x2_dict['if']:
                    output2 = True
        Assertion.assert_equal(output & output2, True, "ERR: edit interface x2 failed")

    def test_03_remove_custom_zone(self):
        output = False
        (delres, msg) = zonesapi.delete_zone_object(name=self.czname, msg=True)
        logger.info(f'delete custom zone result: {delres}')
        if delres is False:
            output = True if 'Object is in use by an Address Object' in str(msg) else False

        # init interface x2 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: remove custom zone show error massage failed")


# Expected: Remove custom zone in ao get error msg successful
class TestCZones_TC21(Test):
    uuid = "SOSAIOT-TC-57816"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']
    czname = 'tc21_rm_error_test21'
    aoname = 'tc22_rmao_error'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_add_custom_ao(self):
        ao_add_dict = {
            "object_type": "host",
            "name": self.aoname,
            "zone": self.czname,
            "value": '192.59.48.37'
        }
        output = aoapi.config_addressobject(**ao_add_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_03_remove_custom_zone(self):
        output = False
        (delres, msg) = zonesapi.delete_zone_object(name=self.czname, msg=True)
        logger.info(f'delete custom zone result: {delres}')
        if delres is False:
            output = True if 'Object is in use by an Address Object' in str(msg) else False

        # init interface x2 and custom zone
        ao_del_dict = {
            "ip_type": "ipv4",
            "name": self.aoname,
        }
        aoapi.del_addressobject(**ao_del_dict)
        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: remove custom zone show error massage failed")


# Expected: Traffic is sent between interface x2 x3 within a custom zone successful
class TestCZones_TC22(Test):
    uuid = "SOSAIOT-TC-57817"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']
    czname = 'tc22_traffic_x2x3_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_03_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_04_ping_from_x2_to_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            output = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if output:
                break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        Assertion.assert_equal(output, True, "ERR: ping form x2 to x3 failed")


# Expected: Traffic is block between interface x2 x3 within a custom zone successful
class TestCZones_TC23(Test):
    uuid = "SOSAIOT-TC-57818"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']
    czname = 'tc23_traffic_x2x3_test23'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': False,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_from_x2_to_x3(self):
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
        time.sleep(5)
        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()
        output, checkres = icmp_drop_check(resp, PC1_ETH2_IP, PC3_ETH1_IP)
        logger.info(checkres)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 to x3 failed")


# Expected: Traffic is sent between lan to x3 within a custom zone successful
class TestCZones_TC24(Test):
    uuid = "SOSAIOT-TC-57803"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']
    czname = 'tc24_traffic_lanx3_test24'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_from_lan_to_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            output = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth1')
            if output:
                break
            else:
                time.sleep(10)

        # init interface x3 and custom zone
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route del -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form lan to x3 failed")


# Expected: Traffic is sent between wan and x2 within a custom zone successful
class TestCZones_TC25(Test):
    uuid = "SOSAIOT-TC-57819"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']
    czname = 'tc25_traffic_wanx2_test25'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_03_ping_from_lan_to_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X1_NET}/24 gw {Parameter.X2_IP}')
        PC2_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X1_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC2_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres is False:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X1_NET}/24 gw {Parameter.X2_IP}')
        PC2_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X1_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form lan to x3 failed")


# Expected: Traffic is pass between x3 dmz on x2 custom zone successful
class TestCZones_TC26(Test):
    uuid = "SOSAIOT-TC-57820"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']
    czname = 'tc26_traffic_x2dmz_test26'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x2_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres is False:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 custom to x3 dmz failed")


# Expected: Traffic is pass between x0 on x3 custom zone successful
class TestCZones_TC27(Test):
    uuid = "SOSAIOT-TC-57804"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']
    czname = 'tc27_traffic_x0x3_test27'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x0_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth1')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH1_IP, eth='eth1')
                if dropres is False:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x3 and custom zone
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route del -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x0 to x3 custom failed")


# Expected: Traffic is pass between x2 custom on x1 successful
class TestCZones_TC28(Test):
    uuid = "SOSAIOT-TC-57821"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']
    czname = 'tc28_traffic_x3x1_test28'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_03_ping_between_x2_on_x1(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X1_NET}/24 gw {Parameter.X2_IP}')
        PC2_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X1_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC2_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres is False:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X1_NET}/24 gw {Parameter.X2_IP}')
        PC2_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X1_IP}')
        Assertion.assert_equal(output, True, "ERR: ping between x2 and x1 failed")


# Expected: Traffic is pass between x3 dmz on x2 public zone successful
class TestCZones_TC29(Test):
    uuid = "SOSAIOT-TC-57805"
    description = show_testcase_info(TESTPLAN, '29', description=True)['title']
    czname = 'tc29_traffic_x3x2_test29'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        zones_dict = {"zones": [base_dict]}
        output = zonesapi.add_zone_object(**zones_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x2_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 custom to x3 dmz failed")


# Expected: Traffic is pass between x3 public on x2 Trusted zone successful
class TestCZones_TC30(Test):
    uuid = "SOSAIOT-TC-57823"
    description = show_testcase_info(TESTPLAN, '30', description=True)['title']
    czname1 = 'tc30_traffic_x3x2_test1'
    czname2 = 'tc30_traffic_x3x2_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        trusted_dict = {
            "zones": [
                {
                    "name": self.czname1,
                    "security_type": 'trusted',
                    "interface_trust": True,
                }
            ]
        }
        public_dict = {
            "zones": [
                {
                    "name": self.czname2,
                    "security_type": 'public',
                    "interface_trust": True,
                }
            ]
        }
        output = zonesapi.add_zone_object(**trusted_dict)
        output &= zonesapi.add_zone_object(**public_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname1,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname2,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x2_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres is False:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname1)
        zonesapi.delete_zone_object(name=self.czname2)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 custom to x3 dmz failed")


# Expected: Traffic is pass between x3 Trusted on x2 Trusted zone successful
class TestCZones_TC31(Test):
    uuid = '1704862'
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']
    czname1 = 'tc31_traffic_x3x2_test1'
    czname2 = 'tc31_traffic_x3x2_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        trusted1_dict = {
            "zones": [
                {
                    "name": self.czname1,
                    "security_type": 'trusted',
                    "interface_trust": True,
                }
            ]
        }
        trusted2_dict = {
            "zones": [
                {
                    "name": self.czname2,
                    "security_type": 'trusted',
                    "interface_trust": True,
                }
            ]
        }
        output = zonesapi.add_zone_object(**trusted1_dict)
        output &= zonesapi.add_zone_object(**trusted2_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname1,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname2,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x2_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname1)
        zonesapi.delete_zone_object(name=self.czname2)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 custom to x3 dmz failed")


# Expected: Traffic is pass between x3 public on x2 public zone successful
class TestCZones_TC32(Test):
    uuid = "SOSAIOT-TC-57824"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']
    czname1 = 'tc32_traffic_x3x2_test1'
    czname2 = 'tc32_traffic_x3x2_test2'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        public1_dict = {
            "zones": [
                {
                    "name": self.czname1,
                    "security_type": 'public',
                    "interface_trust": True,
                }
            ]
        }
        public2_dict = {
            "zones": [
                {
                    "name": self.czname2,
                    "security_type": 'public',
                    "interface_trust": True,
                }
            ]
        }
        output = zonesapi.add_zone_object(**public1_dict)
        output &= zonesapi.add_zone_object(**public2_dict)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x2(self):
        x2_dict = {
            'if': 'X2',
            'zone': self.czname1,
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x2_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x2 failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname2,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x2_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route add -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC1_login.ping_from_eth(ip=PC3_ETH1_IP, eth='eth2')
            if passres:
                dropres = PC3_login.ping_from_eth(ip=PC1_ETH2_IP, eth='eth1')
                if dropres:
                    output = True
                    break
            else:
                time.sleep(10)

        # init interface x2, x3 and custom zone
        interfacev4api.unassign_interface(interface='X2')
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname1)
        zonesapi.delete_zone_object(name=self.czname2)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.X2_IP}')
        PC3_login.send_command(
            f'route del -net {Parameter.X2_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x2 custom to x3 dmz failed")


# Expected: Traffic is drop while x3 custom modified to public
class TestCZones_TC33(Test):
    uuid = "SOSAIOT-TC-57825"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']
    czname = 'tc33_traffic_x0x3_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {
            "zones": [
                {
                    "name": self.czname,
                    "security_type": 'trusted',
                    "interface_trust": True,
                }
            ]
        }
        output = zonesapi.add_zone_object(**trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x0_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC3_login.ping_from_eth(ip=PC1_ETH1_IP, eth='eth1')
            if passres:
                output = True
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(output, True, "ERR: ping form x0 to x3 custom failed")

    def test_04_modify_custom_zone_to_public(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        trusted_dict = {
            "zones": [
                {
                    "name": self.czname,
                    "security_type": 'public',
                    "interface_trust": True,
                }
            ]
        }
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        interfacev4api.unassign_interface(interface='X3')
        output = zonesapi.edit_zone_object(self.czname, **trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
            if output:
                interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: modify custom zone failed")

    def test_05_ping_between_x0_on_x3(self):
        output = False
        for i in range(3):
            passres = PC3_login.ping_from_eth(ip=PC1_ETH1_IP, eth='eth1')
            if passres is False:
                output = True
                break
            else:
                time.sleep(10)

        # init interface x3 and custom zone
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route del -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x0 to x3 failed")


# Expected: Traffic is pass while x3 custom modified to Trusted
class TestCZones_TC34(Test):
    uuid = "SOSAIOT-TC-57826"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']
    czname = 'tc34_traffic_x0x3_test1'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_custom_zone(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'public',
            'interface_trust': True,
        }
        public_dict = {
            "zones": [
                {
                    "name": self.czname,
                    "security_type": 'public',
                    "interface_trust": True,
                }
            ]
        }
        output = zonesapi.add_zone_object(**public_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
        Assertion.assert_equal(output, True, "ERR: add custom zone failed")

    def test_02_edit_interface_x3(self):
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 failed")

    def test_03_ping_between_x0_on_x3(self):
        output = False
        PC1_login.send_command(
            f'route add -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route add -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')

        for i in range(3):
            passres = PC3_login.ping_from_eth(ip=PC1_ETH1_IP, eth='eth1')
            if passres is False:
                output = True
                break
            else:
                time.sleep(10)
        Assertion.assert_equal(output, True, "ERR: ping form x0 to x3 custom failed")

    def test_04_modify_custom_zone_to_public(self):
        base_dict = {
            'name': self.czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {
            "zones": [
                {
                    "name": self.czname,
                    "security_type": 'trusted',
                    "interface_trust": True,
                }
            ]
        }
        x3_dict = {
            'if': 'X3',
            'zone': self.czname,
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X3_GW,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        interfacev4api.unassign_interface(interface='X3')
        output = zonesapi.edit_zone_object(self.czname, **trusted_dict)
        if output:
            showres = zonesapi.show_zone_object(name=self.czname)
            output &= check_custom_zones(base_dict, showres)
            if output:
                interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: modify custom zone failed")

    def test_05_ping_between_x0_on_x3(self):
        output = False
        for i in range(3):
            passres = PC3_login.ping_from_eth(ip=PC1_ETH1_IP, eth='eth1')
            if passres:
                output = True
                break
            else:
                time.sleep(10)

        # init interface x3 and custom zone
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(name=self.czname)
        PC1_login.send_command(
            f'route del -net {Parameter.X3_NET}/24 gw {Parameter.FIREWALL}')
        PC3_login.send_command(
            f'route del -net {Parameter.X0_NET}/24 gw {Parameter.X3_IP}')
        Assertion.assert_equal(output, True, "ERR: ping form x0 to x3 failed")