from definition.settings import *


class Test_Port_Redundancy_07(Test):
    uuid = "SOSAIOT-TC-57093"

    # description = show_testcase_info(TESTPLAN, '', description=True)['1512775']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_adding_interface_itself_as_redudant_port(self):
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X2'
        }
        rc, statusmsg = Linterface.config_interface(msg=True, **x2)
        error_msg = "'X2' not a reasonable value."
        Assertion.assert_regular(statusmsg['status']['info'][0]['message'], error_msg,
                                 "ERR: Able to add interface itself as redudant port")


class Test_Port_Redundancy_08(Test):
    uuid = "SOSAIOT-TC-57092"

    # description = show_testcase_info(TESTPLAN, '6', description=True)['1512774']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_creating_port_redudancy(self):
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X4'
        }
        rc = Linterface.config_interface(**x2)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")

    def test_03_adding_redudant_port_to_interface_with_subinterface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 143,
            'if': 'x4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '89.5.143.11',
            'netmask': '255.255.255.0'}
        resp, statusmsg = Linterface.add_interface(msg=True, **vlan)
        error_msg = "'x4' not a reasonable value."
        Assertion.assert_regular(statusmsg['status']['info'][0]['message'], error_msg,
                                 "ERR: Able to add interface itself as redudant port")

    def test_04_delete_port_redudancy(self):
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': False
        }
        rc = Linterface.config_interface(**x2)
        Assertion.assert_equal(rc, True, f"ERR: removing port redudancy failed")


class Test_Port_Redundancy_09(Test):
    uuid = "SOSAIOT-TC-57094"

    # description = show_testcase_info(TESTPLAN, '6', description=True)['1512774']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_VLAN_interface_is_not_allowed_to_have_a_redundant_Port(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Port_Redundancy_TP2542_New/definition/ui_user.py -method tc1 ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"


class Test_Port_Redundancy_10(Test):
    uuid = "SOSAIOT-TC-57086"

    # description = show_testcase_info(TESTPLAN, '6', description=True)['1512774']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_editing_interface_with_LAN_and_adding_port_redudancy(self):
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '152.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X5'
        }
        rc = Linterface.config_interface(**x4)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")
        interface_after_config_port = Linterface.get_interface_status('X4')

        # unassigning interface to verify interface should unassign redundant port
        rc2 = Linterface.unassign_interface(interface='X4')
        Assertion.assert_equal(rc2, True, f"ERR: unassigning interface failed")
        interface_after_unassign_int = Linterface.get_interface_status('X4')

        assert interface_after_config_port != interface_after_unassign_int, "interface did not unassign redundant port after unassigning interface"


class Test_Port_Redundancy_11(Test):
    uuid = "SOSAIOT-TC-57085"

    # description = show_testcase_info(TESTPLAN, '6', description=True)['1512774']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_configuring_port_redudancy_for_interface(self):
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '152.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X5'
        }
        rc = Linterface.config_interface(**x4)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")

        x4_before_reboot = Linterface.get_interface_status('X4')

        x6 = {
            'if': 'X6',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '14.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X7'
        }
        rc = Linterface.config_interface(**x6)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")

        x6_before_reboot = Linterface.get_interface_status('X6')

        # reboot the firewall
        res = settingapi.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot fw failed")

        # verify config after reboot
        x4_after_reboot = Linterface.get_interface_status('X4')
        x6_after_reboot = Linterface.get_interface_status('X6')

        assert x4_before_reboot == x4_after_reboot and x6_before_reboot == x6_after_reboot, "Configuration is not same after reboot"

    def test_03_delete_port_redudancy(self):
        rc = Linterface.unassign_interface(interface='X4')
        Assertion.assert_equal(rc, True, f"ERR: unassigning interface failed")
        rc1 = Linterface.unassign_interface(interface='X6')
        Assertion.assert_equal(rc1, True, f"ERR: unassigning interface failed")


class Test_Port_Redundancy_12(Test):
    uuid = "SOSAIOT-TC-57091"

    # description = show_testcase_info(TESTPLAN, '6', description=True)['1512774']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_creating_port_redudancy(self):
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X4'
        }
        rc = Linterface.config_interface(**x2)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")

        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '172.17.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': 'redundancy',
            'redundancy_port': 'X5'
        }
        rc = Linterface.config_interface(**x3)
        Assertion.assert_equal(rc, True, f"ERR: creating port redudancy failed")

    def test_03_save_config_and_remove_redudant_port(self):
        settingapi.export_setting_exp('/tmp/port_redudancy.exp')

        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': False
        }
        rc = Linterface.config_interface(**x2)
        Assertion.assert_equal(rc, True, f"ERR: removing port redudancy failed")

        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '172.17.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': False
        }
        rc = Linterface.config_interface(**x3)
        Assertion.assert_equal(rc, True, f"ERR: removing port redudancy failed")

    def test_04_import_config_and_verify_redudant_port(self):
        settingapi.import_setting_exp('/tmp/port_redudancy.exp')
        rc = Linterface.get_interface_status('X2')
        rc1 = Linterface.get_interface_status('X3')

        assert rc['interfaces'][0]['ipv4']['port']['redundancy']['interface'] == "X4" and \
               rc1['interfaces'][0]['ipv4']['port']['redundancy'][
                   'interface'] == "X5", "Redudant port are not present after importing file"

    def test_05_delete_port_redudancy(self):
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': False
        }
        rc = Linterface.config_interface(**x2)
        Assertion.assert_equal(rc, True, f"ERR: removing port redudancy failed")

        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '172.17.2.168',
            'netmask': '255.255.255.0',
            'redundancy_aggregation_port': False
        }
        rc = Linterface.config_interface(**x3)
        Assertion.assert_equal(rc, True, f"ERR: removing port redudancy failed")
