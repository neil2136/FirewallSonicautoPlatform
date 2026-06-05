from definition.settings import *


# [GUI][DS-Lite][2.1]it can add a DSLite tunnel interface successful on the GUI
class Test_DSLite_TC2682744(Test):
    uuid = "SOSAIOT-TC-56556"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dslite_tunnel(self):
        opt = {
            "name": "ds-lite_t1",
            "bound_to_if": "X1",
            "local": {"dynamic": True},
            "remote": {"dynamic": True},
            "comment": "ds-lite tunnel interface"
        }
        rc = if_v4_api.add_dslite_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add dslite tunnel failed!!')


# [GUI][DS-Lite][2.2]it can delete a DSLite tunnel after we added a DSLite interface
class Test_DSLite_TC2682745(Test):
    uuid = "SOSAIOT-TC-56557"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_a_dslite_tunnel(self):
        rc = if_v4_api.delete_gre4to6_tunnel_interface_by_name('ds-lite_t1')
        Assertion.assert_equal(rc, True, 'ERR: delete a dslite tunnel interface failed!!')


# [GUI][DS-Lite][3.2]it can add/modify/delete the comment when you add a DS-Lite tunnel interface"
class Test_DSLite_TC1529345(Test):
    uuid = "SOSAIOT-TC-56559"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_dslite_tunnel_interface(self):
        Test_DSLite_TC2682744().test_01_add_dslite_tunnel()

    def test_02_modify_the_comment_of_dslite_tunnel_interface(self):
        opt = {
            "comment": "edit ds-lite tunnel interface"
        }
        rc = if_v4_api.edit_dslite_tunnel_interface_by_name(tunnel_name="ds-lite_t1", **opt)
        Assertion.assert_equal(rc, True, 'ERR: modify comment of dslite tunnel failed!!')

    def test_03_delete_comment_of_dslite_tunnel_interface(self):
        rc = if_v4_api.edit_dslite_tunnel_interface_by_name(tunnel_name="ds-lite_t1", **{"comment": ""})
        Assertion.assert_equal(rc, True, 'ERR: modify comment of dslite tunnel failed!!')


# [CLI][DS-Lite]the command "type" can work normally
class Test_DSLite_TC1529357(Test):
    uuid = "SOSAIOT-TC-56560"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_type_command_cli(self):
        cmds = ['configure', 'tunnel-interface 4to6 ds-lite_t1', 'type dslite', 'commit', 'end', 'exit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: check type command failed!!')


# [CLI][DS-Lite]it can edit the ds-lite interface successful
class Test_DSLite_TC1529358(Test):
    uuid = "SOSAIOT-TC-56554"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_dslite_interface_via_CLI(self):
        cmds = ['configure', 'tunnel-interface 4to6 ds-lite_t1', "comment 'edit ds-lite tunnel interface via CLI'",
                'commit',
                'end', 'exit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: edit Gre interface via CLI failed!!')


# [CLI][DS-Lite]it can correct display the ds-lite information when I show current-config under no-config mode
class Test_DSLite_TC1529359(Test):
    uuid = "SOSAIOT-TC-56561"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_added_dslite_interface_via_CLI(self):
        out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 ds-lite_t1'], tag=1)[1]
        Assertion.assert_regular(out, 'ds-lite_t1', 'ERR: show added dslite tunnel interface via CLI failed!!')


# [CLI][DS-Lite]it can delete the ds-lite interface successful
class Test_DSLite_TC2682743(Test):
    uuid = "SOSAIOT-TC-56555"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_dslite_interface_via_cli(self):
        rc = fw_cli.do_cli_commands(['configure', 'no tunnel-interface 4to6 ds-lite_t1', 'commit', 'end'])
        Assertion.assert_equal(rc, True, 'ERR: delete dslite Tunnel interface via CLI failed!!')


# When it receives IPv4 traffic, it will put it into its IP4-in-IP6 tunnel to AFTR. The IPv4 traffic will directly encapsulated into tunnel without NATed.
class Test_DSLite_TC1529346(Test):
    uuid = "SOSAIOT-TC-56562"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dslite_tunnel_iface_on_local(self):
        opt = {
            "name": "t1",
            "bound_to_if": "X2",
            "local": {"ipv6": "2102::168"},
            "remote": {"ipv6": "2102::169"},
            "comment": "ds-lite tunnel interface"
        }
        rc = if_v4_api.add_dslite_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add dslite tunnel on local failed!!')

    def test_02_add_dis_tunnel_iface_on_remote(self):
        opt = {
            "name": "t1",
            "bound_to_if": "X2",
            "local": {"ipv6": "2102::169"},
            "remote": {"ipv6": "2102::168"},
            "comment": "ds-lite tunnel interface",
            'local_ipv4': "192.0.0.3"
        }
        rc = rm_ifacev4_api.add_dslite_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add dslite tunnel on remote failed!!')

    def test_03_add_route_policy_on_local(self):
        route = copy.deepcopy(route_base)
        route.update({"destination": {"name": "172.16.1.0/24"}})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, "ERR: add route policy on local firewall failed!!")

    def test_04_add_route_policy_on_remote(self):
        route = copy.deepcopy(route_base)
        route.update({"destination": {"name": "192.168.168.0/24"}})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = rem_route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed on remote firewall!!")

    def test_05_test_traffic_tunnel(self):
        rc = False
        pkt_api.clear_packets()
        pkt_api.clear_packets()
        pkt_api.start_capture()
        pc1_login.send_command('ping 172.16.1.100 -c 5')
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('Packet comments')
        for pkt in pkt_list:
            check_list = ('Src: 2102::168', ' Dst: 2102::169')
            if all(x in pkt for x in check_list):
                logger.info(f'found the GRE encapsulate packet:\n{pkt}')
                rc = True
                break
        else:
            logger.error('not found the GRE encapsulated packet')
        Assertion.assert_equal(rc, True, 'ERR: function check the Gre4to6 interface failed!!')


#  [Function][DS-Lite][4.8.3] when we add a DS-Lite interface, export the pref file, then import the pref file ,the configuration can't lost
class Test_DSLite_TC1529348(Test):
    uuid = "SOSAIOT-TC-56563"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_exp_file(self):
        res = setting_api.export_setting_exp('/tmp/dslite_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_02_restore_firewall(self):
        res = setting_api.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_03_config_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '12.12.1.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_04_register_fw(self):
        for i in range(10):
            sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_05_import_exp_file(self):
        res = setting_api.import_setting_exp(
            filepath='/tmp/dslite_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_06_settings_check_after_exp_import(self):
        out = if_v4_api.get_tunnel_interface_status(name='t1', type='4to6')
        Assertion.assert_equal(bool(out), True, 'ERR: settings check failed!!')

    def test_07_function_check_after_exp_import(self):
        Test_DSLite_TC1529346().test_05_test_traffic_tunnel()


# [Function][DS-Lite][4.8.11] when we add a DS-Lite interface, the configuraiton can't lost after we reboot the box
class Test_DSLite_TC1529350(Test):
    uuid = "SOSAIOT-TC-56564"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot_fw(self):
        res = setting_api.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot unit failed")

    def test_02_settings_check_after_reboot(self):
        Test_DSLite_TC1529346().test_05_test_traffic_tunnel()


# [Function][DS-Lite][4.9] After we add a DS-Lite interface, if we change some option it can work normally
class Test_DSLite_TC1529351(Test):
    uuid = "SOSAIOT-TC-86879"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_update_dslite_tunnel_interface(self):
        opt = {
            "comment": "edit ds-lite tunnel interface"
        }
        rc = if_v4_api.edit_dslite_tunnel_interface_by_name(tunnel_name="t1", **opt)
        Assertion.assert_equal(rc, True, 'ERR: modify comment of dslite tunnel failed!!')

    def test_02_traffic_check_for_tunnel(self):
        Test_DSLite_TC1529346().test_05_test_traffic_tunnel()
