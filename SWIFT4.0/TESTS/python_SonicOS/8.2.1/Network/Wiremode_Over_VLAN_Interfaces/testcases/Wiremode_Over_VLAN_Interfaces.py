from definition.init_param import *


class Test_01_Wiremode_Over_VLAN_Interfaces_tc_022(Test):
    uuid = "SOSAIOT-TC-57559"
    description= show_testcase_info(Parameter.TESTPLAN, '1513132', description=True)['title']
    jira = 'GEN8-7332'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513132')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_X2_vlan_interface(self):
        logger.info('add vlan interface x2 ...')
        x2_vlan = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': vlan_id_X2_1,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_vlan1_IP,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x2_vlan)
        Assertion.assert_equal(rc, True, "ERR:add vlan interface x2 failed")

    def test_02_add_X3_vlan_interface(self):
        logger.info('add vlan interface x3 ...')
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_vlan_IP,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x3_vlan)
        Assertion.assert_equal(rc, True, "ERR:add vlan interface x3 failed")

    def test_03_config_two_vlan_wiremode_interface(self):
        logger.info('config two vlan wiremode interface...')
        interface_obj.unassign_vlan_interface(interface = 'X3', vlan_id = str(vlan_id_X3))
        x2 = {
            'if': "X2:V{}".format(vlan_id_X2_1),
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': "X3:V{}".format(vlan_id_X3),
            'wire_paired_zone': 'LAN',
            'vlan_id':vlan_id_X2_1
        }
        rc = interface_obj.config_vlan_interface_to_wiremode(**x2)
        Assertion.assert_equal(rc, True, "ERR: config two vlan wiremode interface failed")

    def test_04_try_to_delete_vlan_wiremode_interface(self):
        logger.info('try to delete vlan wiremode interface...')
        opt = {
            'if': "X2",
            'vlan_tag':vlan_id_X2_1,
            'type':'vlan'
        }
        rc = interface_obj.del_interface(**opt)    
        Assertion.assert_equal(rc, True, "ERR: config two vlan wiremode interface failed")


class Test_02_Wiremode_Over_VLAN_Interfaces_tc_031(Test):
    uuid = "SOSAIOT-TC-57560"
    description= show_testcase_info(Parameter.TESTPLAN, '1513133', description=True)['title']
    jira = 'GEN8-7332'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_two_vlan_interface_over_same_parent_interface(self):
        logger.info('add two vlan interface over same parent interface...')
        interface_obj.unassign_vlan_interface(interface = 'X3', vlan_id = str(vlan_id_X3))
        interface_obj.unassign_vlan_interface(interface = 'X2', vlan_id = str(vlan_id_X2_1))

        x2_vlan1 = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': vlan_id_X2_1,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_vlan1_IP,
            'mgmt_ping': True,
        }
        x2_vlan2 = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': vlan_id_X2_2,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_vlan2_IP,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x2_vlan1)
        rc &= interface_obj.add_interface(**x2_vlan2)
        Assertion.assert_equal(rc, True, "ERR:add vlan interface x2 failed")


    def test_02_config_two_vlan_wiremode_interface(self):
        logger.info('config two vlan wiremode interface...')
        flag =False
        x2 = {
            'if': "X2:V{}".format(vlan_id_X2_2),
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': "X2:V{}".format(vlan_id_X2_1),
            'wire_paired_zone': 'LAN',
            'vlan_id':vlan_id_X2_2
        }
        output = interface_obj.config_vlan_interface_to_wiremode(msg=True, **x2)
        logger.info(output)
        if re.search(r"not a reasonable value", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config two vlan wiremode interface failed")


class Test_03_Wiremode_Over_VLAN_Interfaces_tc_035(Test):
    uuid = "SOSAIOT-TC-57561"
    description= show_testcase_info(Parameter.TESTPLAN, '1513134', description=True)['title']
    jira = 'GEN8-7332'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513134')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_all_vlan_interfaces(self):
        logger.info('delete all vlan interfaces...')
        opt1 = {
            'if': "X2",
            'vlan_tag':vlan_id_X2_1,
            'type':'vlan'
        }
        opt2 = {
            'if': "X2",
            'vlan_tag':vlan_id_X2_2,
            'type':'vlan'
        }
        opt3 = {
            'if': "X3",
            'vlan_tag':vlan_id_X3,
            'type':'vlan'
        }
        rc = interface_obj.del_interface(**opt1)
        rc &= interface_obj.del_interface(**opt2)
        rc &= interface_obj.del_interface(**opt3)
        Assertion.assert_equal(rc, True, "ERR: delete all vlan interfaces failed")

    def test_02_config_interface_x2_x3_wiremode(self):
        logger.info('config interface x2 x3 to wiremode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,        
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 x3 to wiremode bypass failed")

    def test_03_add_X2_vlan_interface(self):
        logger.info('add vlan interface x2 ...')
        flag = False
        x2_vlan = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': vlan_id_X2_1,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_vlan1_IP,
            'mgmt_ping': True,
        }
        output = interface_obj.add_interface(msg=True, **x2_vlan)
        if re.search(r"not a reasonable value", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:add vlan interface x2 failed")

    def test_04_add_X3_vlan_interface(self):
        logger.info('add vlan interface x3 ...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_vlan_IP,
            'mgmt_ping': True,
        }
        output = interface_obj.add_interface(msg=True, **x3_vlan)
        if re.search(r"not a reasonable value", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:add vlan interface x3 failed")

    def test_05_unassign_x2_and_add_vlan_interface(self):
        logger.info('unassign x2 and add vlan interface...')
        interface_obj.unassign_interface(interface = 'X2')
        x2_vlan = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag': vlan_id_X2_1,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_vlan1_IP,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x2_vlan)
        Assertion.assert_equal(rc, True, "ERR: unassign x2 and add vlan interface failed")

    def test_06_add_X3_vlan_interface(self):
        logger.info('add vlan interface x3 ...')
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_vlan_IP,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x3_vlan)
        Assertion.assert_equal(rc, True, "ERR:add vlan interface x3 failed")

    def test_07_config_two_vlan_wiremode_interface(self):
        logger.info('config two vlan wiremode interface...')
        interface_obj.unassign_vlan_interface(interface = 'X3', vlan_id = str(vlan_id_X3))
        x2 = {
            'if': "X2:V{}".format(vlan_id_X2_1),
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': "X3:V{}".format(vlan_id_X3),
            'wire_paired_zone': 'LAN',
            'vlan_id':vlan_id_X2_1
        }
        rc = interface_obj.config_vlan_interface_to_wiremode(**x2)
        Assertion.assert_equal(rc, True, "ERR: config two vlan wiremode interface failed")
