from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True
    
    def test_00_01_Add_ZoneObj(self):
        logger.info('-'*10+'Add  ZoneObj for DUT '+'-'*10)
        rc = Lzone_obj.add_zone_object(**ZONEREF)
        rc &= Rzone_obj.add_zone_object(**ZONEREF)
        Assertion.assert_equal(rc, True, 'Add  ZoneObj for DUT Failed.')
    
    def test_00_02_Config_X3_DMZ_on_Local(self):
        logger.info(" {} ".center(20, '-').format('Config X3 DMZ on Local'))
        rc = Linterface.config_interface(**Lx3)
        rc &= Linterface.config_interface(**Lx4)
        rc &= Rinterface.config_interface(**Rx3)
        rc &= Rinterface.config_interface(**Rx4)
        Assertion.assert_equal(rc, True, "ERR: Config X3 DMZ on Local failed")
    
    def test_00_03_Add_AddObj(self):
        logger.info('-'*10+'Add  AddObj for DUT and Remote DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**Rlocal)
        rc &= LAddrOBJ.config_addressobject(**LDMZ)
        rc &= LAddrOBJ.config_addressobject(**lCustomObj)
        rc &= LAddrOBJ.config_addressobject(**lTransObj)
        logger.info('-'*10+'Add remote AddObj for Remote DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**RDMZ)
        rc &= RAddrOBJ.config_addressobject(**RCustomObj)
        rc &= RAddrOBJ.config_addressobject(**rTransObj)
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    def test_00_04_Add_ACL_for_Zone(self):
        logger.info('-'*10+'Add ACL for Zone in DUT '+'-'*10)
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule1['name'] = 'zone1'
        rule1['from'] = 'VPN'
        rule1['to']   = 'Custom'
        rule2['name'] = 'zone2'
        rule2['from'] = 'Custom'
        rule2['to']   = 'VPN'
        rc = Laccess_rule_obj.config_accessrule(**rule1)
        rc &= Laccess_rule_obj.config_accessrule(**rule2)
        Assertion.assert_equal(rc, True, 'Add  ZoneObj for DUT Failed.')

    def test_00_05_Add_AddGroup(self):
        logger.info('-'*10+'Add  Address Group  for DUT and Remote DUT'+'-'*10)
        rc = LAddrGroupOBJ.add_addressgroup(**local_grp1)#
        rc &= LAddrGroupOBJ.add_addressgroup(**local_grp2)#
        rc &= RAddrGroupOBJ.add_addressgroup(**remote_grp1)#
        rc &= RAddrGroupOBJ.add_addressgroup(**remote_grp2)#
        Assertion.assert_equal(rc, True, 'Add  Address Group  for DUT and Remote DUT Failed.')





   