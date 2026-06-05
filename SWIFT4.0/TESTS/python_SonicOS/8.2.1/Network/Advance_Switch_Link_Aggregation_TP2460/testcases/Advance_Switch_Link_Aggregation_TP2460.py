from definition.settings import *

class Test_1_Verify_manual_key_during_LAG_Port_cnfiguration(Test):
    uuid = "SOSAIOT-TC-61463"
    description= show_testcase_info(TESTPLAN, '1533456', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_vlan_trunk(self):
        logger.info("Add vlan trunk... ")
        rc = VlanPort.add_trunk_ports(**trunkport_X5)
        Assertion.assert_equal(rc, True, "ERR: Add vlan trunk failed")

    def test_03_add_LAG_Port_with_port_256(self):
        flag = True
        logger.info("Add LAG Port with port 256... ")
        add_LAG_ports_X5['switch']['link_aggregation'][0]['key']['id']=LAG_Port_256
        rc = LAG_config.add_LAG_ports(msg=True,**add_LAG_ports_X5)
        command = f'Value or string length({LAG_Port_256}) out of bounds (max = 255)'
        logger.info(command)
        if command in str(rc):
            flag = False
        Assertion.assert_equal(flag, False, "ERR: add_LAG_Port with port 256 succeed.")

    def test_04_add_LAG_Port_with_port_20(self):
        logger.info("Add LAG Port with port 20... ")
        add_LAG_ports_X5['switch']['link_aggregation'][0]['key']['id']=LAG_Port_20
        rc = LAG_config.add_LAG_ports(**add_LAG_ports_X5)
        Assertion.assert_equal(rc, True, "ERR: add_LAG_Port with port 20 failed")

    def test_05_del_LAG(self):
        rc = LAG_config.del_LAG_Port(interface=trunk_X5)
        Assertion.assert_equal(rc, True, "ERR: Del_LAG_Port with port 20 failed")

    def test_06_del_vlan_trunk(self):
        rc = VlanPort.delete_vlan_trunk(**trunkport_X5)
        Assertion.assert_equal(rc, True, "ERR: del_trunk_port failed")


class Test_2_Verify_additional_VLANs_canbe_added_deleted_on_the_LAG(Test):
    uuid = '1509581'
    description= show_testcase_info(TESTPLAN, '1509581', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_trunk_ports(self):
        logger.info("Add trunk ports... ")
        rc = VlanPort.add_trunk_ports(**trunkport_X5)
        rc &= VlanPort.add_trunk_ports(**trunkport_X6)
        Assertion.assert_equal(rc, True, "ERR: Add trunk ports failed")

    def test_03_Enable_vlan_on_trunk_ports(self):
        logger.info("Enable VLAN on two trunk ports... ")
        rc = VlanPort.enable_vlan(interface=trunk_X5,vlan=100)
        rc &= VlanPort.enable_vlan(interface=trunk_X6,vlan=100)
        Assertion.assert_equal(rc, True, "ERR: Config X4 to static failed")

    def test_04_add_a_LAG_with_the_two_trunk_ports(self):
        lag = {
            "switch": {
                "link_aggregation": [{
                    "port": trunk_X5,
                    "key": {
                        "id": 100
                    },
                    "member": [{
                        "name": trunk_X6
                    }],
                    "lacp": False,
                    "load_balance_type": {
                        "source": "mac"
                    }
                }]
            }
        }
        rc = LAG_config.add_LAG_ports(**lag)
        Assertion.assert_equal(rc, True, "ERR: Add a LAG with the two trunk ports failed")

    def test_05_add_another_VLAN_to_the_two_trunk_ports(self):
        logger.info("Add another VLAN to the two trunk ports.....")
        rc = VlanPort.enable_vlan(interface=trunk_X5,vlan=200)
        rc &= VlanPort.enable_vlan(interface=trunk_X6,vlan=200)
        Assertion.assert_equal(rc, True, "ERR: Add another VLAN to the two trunk ports failed")

    def test_06_disable_vlan(self):
        ########## Because X5 and X6 are LAG,We just need to delete one port vlan, when delete one, anthoer is deleted automatically############
        logger.info("Try to delete the VLAN 100......")
        rc = VlanPort.disable_vlan(interface=trunk_X5,vlan=100)
        Assertion.assert_equal(rc, True, "ERR: Disable vlan failed")


class Test_3_Prefs_importandExport_with_two_or_more_LAGs(Test):
    uuid = "SOSAIOT-TC-61418"
    description= show_testcase_info(TESTPLAN, '1509584', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_export_prefs(self):
        rc = setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: Failed to export settings.")

    @repeat_method(8)
    def test_03_do_factory_restore(self):
        rc = setting_obj.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: Factory reboot FW failed.")

    def test_04_import_prefs(self):
        time.sleep(5)
        rc = setting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: Failed to import settings.")
    
    def test_05_get_LAG_after_import_prefs(self):
        flag = False
        rc = LAG_config.show_LAG_Port()
        logger.info(rc)
        if trunk_X5 in str(rc) and trunk_X6 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get_LAG_after_import_prefs.")

    def test_06_add_third_LAG(self):
        logger.info("Add another LAG Port with port 100... ")
        rc = VlanPort.enable_vlan(interface=trunk_X7,vlan=100)
        rc &= LAG_config.add_LAG_ports(**add_LAG_ports_X7)
        Assertion.assert_equal(rc, True, "ERR: Add LAG failed")

    def test_07_import_prefs_after_add_third_LAG(self):
        time.sleep(5)
        rc = setting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: Failed to import settings.")

    def test_08_get_LAG_after_add_third_LAG(self):
        flag = True
        rc = LAG_config.show_LAG_Port()
        logger.info(rc)
        if trunk_X7 in rc:
            flag = False
        Assertion.assert_equal(flag, True, "ERR: get_LAG_after_add_third_LAG.")