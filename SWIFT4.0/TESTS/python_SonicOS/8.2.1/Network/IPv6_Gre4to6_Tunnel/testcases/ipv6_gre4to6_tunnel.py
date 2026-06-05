from definition.utils import *


# [GUI][Gre4to6][2.1]it can add a GRE4to6 tunnel interface successful on the GUI
class Test_GRE4to6_TC02(Test):
    uuid = "SOSAIOT-TC-56589"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_add_4to6_tunnel_iface(self):
        rc = if_v4_api.add_gre4to6_tunnel_interface(**gre_t1_local)
        Assertion.assert_equal(rc, True, 'ERR: add gre4to6 tunnel interface failed!!')


# [GUI][Gre4to6][1]Check for tunnel6 interface, make sure all the items display correctly/ function work
class Test_GRE4to6_TC01(Test):
    uuid = "SOSAIOT-TC-56582"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_added_Gre4to6_iface(self):
        out = if_v4_api.get_tunnel_interface_status(name='gre_t1', type='4to6')
        Assertion.assert_regular(json.dumps(out), 'gre_t1', 'ERR: check added Gre 4to6 tunnel interface failed!!')


# [GUI][Gre4to6][2.2]it can delete a GRE4to6 tunnel after we added a GRE4to6 interface
class Test_GRE4to6_TC03(Test):
    uuid = "SOSAIOT-TC-56590"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_delete_Gre_tunnel_if(self):
        rc = if_v4_api.delete_gre4to6_tunnel_interface_by_name("gre_t1")
        Assertion.assert_equal(rc, True, 'ERR: delete Gre tunnel interface failed!!')


# [GUI][Gre4to6][3.2]it can add/modify/delete the comment when you add a Gre4to6 tunnel interface
class Test_GRE4to6_TC05(Test):
    uuid = "SOSAIOT-TC-56583"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_Gre4to6_tunnle_iface_with_comment(self):
        Test_GRE4to6_TC02().test_01_add_4to6_tunnel_iface()

    @repeat_method(3)
    def test_02_edit_comment_Gre4to6_tunnel(self):
        opt = {
            'comment': "edit gre4to6 tunnel interface"
        }
        rc = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit comment for gre4to6 tunnel interface failed!!')

    @repeat_method(3)
    def test_03_delete_comment_for_Gre4to6_tunnel(self):
        opt = {
            'comment': ""
        }
        rc = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: delete comment for gre4to6 tunnel interface failed!!')


# [GUI][Gre4to6][3.10]when I add the Gre4to6 interface,The bound to interface is editable except for change it to be non-wan zone.
class Test_GRE4to6_TC13(Test):
    uuid = "SOSAIOT-TC-56584"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_edit_bound_to_interface_for_Gre_iface(self):
        opt = {
            'bound_to_if': "X1"
        }
        rc = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit WAN zone Gre tunnel bound to opt failed!!')

    @repeat_method(3)
    def test_02_edit_bound_to_interface_to_Non_WAN(self):
        opt = {
            'bound_to_if': "X0"
        }
        res, err_msg = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt, msg=True)
        rc = (not res) and "'X0' not a reasonable value." in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, 'ERR: edit WAN zone Gre tunnel bound to opt failed!!')


# [CLI][Gre4to6]the command "type" can work normally
class Test_GRE4to6_TC1523876(Test):
    uuid = "SOSAIOT-TC-56585"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_type_command(self):
        cmds = ['configure', 'tunnel-interface 4to6 gre_t1', 'type gre4to6', 'commit', 'end', 'exit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: check type command failed!!')


# [CLI][Gre4to6]it can edit the Gre4to6 interface successful
class Test_GRE4to6_TC1523877(Test):
    uuid = "SOSAIOT-TC-56586"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_Gre_interface_via_CLI(self):
        cmds = ['configure', 'tunnel-interface 4to6 gre_t1', "comment 'edit Gre tunnel interface via CLI'", 'commit',
                'end', 'exit']
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'ERR: edit Gre interface via CLI failed!!')


# [CLI][Gre4to6] it can show correct information after  we add a Gre4to6 interface
class Test_GRE4to6_TC1523878(Test):
    uuid = "SOSAIOT-TC-56587"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_added_Gre_interface_via_CLI(self):
        out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 gre_t1'], tag=1)[1]
        Assertion.assert_regular(out, 'gre_t1', 'ERR: show added Gre tunnel interface via CLI failed!!')


# [CLI][Gre4to6]it should use command-- show tunnel-interfaces 4to6 to show all the 4to6 interfaces
class Test_GRE4to6_TC1523879(Test):
    uuid = "SOSAIOT-TC-56588"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_all_tunnel_interfaces_via_CLI(self):
        out = fw_cli.do_cli_commands(['show tunnel-interfaces 4to6'], tag=1)[1]
        Assertion.assert_regular(out, 'gre_t1', 'ERR: show all added Gre tunnel interface via CLI failed!!')


# [CLI][Gre4to6]it can delete the Gre4to6 interface successful
class Test_GRE4to6_TC2682750(Test):
    uuid = "SOSAIOT-TC-56592"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_added_Gre_tunnel_via_CLI(self):
        rc = fw_cli.do_cli_commands(['configure', 'no tunnel-interface 4to6 gre_t1', 'commit', 'end'])
        Assertion.assert_equal(rc, True, 'ERR: delete added Gre Tunnel interface via CLI failed!!')


# Function Part
# [Function][Gre4to6][4.1]When it receives IPv4 traffic, it will put it into GRE4to6 tunnel. The IPv4 traffic will directly encapsulated into tunnel without NATed.
class Test_GRE4to6_TC1523869(Test):
    uuid = "SOSAIOT-TC-56593"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_gre_tunnel_iface_on_local(self):
        rc = if_v4_api.add_gre4to6_tunnel_interface(**gre_t1_local)
        Assertion.assert_equal(rc, True, 'ERR: add gre4to6 tunnel interface failed!!')

    def test_02_add_gre_tunnel_iface_on_remote(self):
        rc = rm_ifacev4_api.add_gre4to6_tunnel_interface(**gre_t1_remote)
        Assertion.assert_equal(rc, True, 'ERR: add gre4to6 tunnel interface failed!!')

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

    def test_05_test_traffic_cross_Gre_tunnel(self):
        rc = False
        init_packet_capture()
        pc1_login.send_command('ping 172.16.1.100 -c 5')
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('Packet comments')
        for pkt in pkt_list:
            check_list = ('Src: 2102::168', ' Dst: 2102::169', "Generic Routing Encapsulation (IP)")
            if all(x in pkt for x in check_list):
                logger.info(f'found the GRE encapsulate packet:\n{pkt}')
                rc = True
                break
        else:
            logger.error('not found the GRE encapsulated packet')
        Assertion.assert_equal(rc, True, 'ERR: function check the Gre4to6 interface failed!!')


#  [Function][Gre4to6][4.8.3] when we add a Gre4to6 interface, export the pref file, then import the pref file ,the configuration can't lost
class Test_GRE4to6_TC1523871(Test):
    uuid = "SOSAIOT-TC-56595"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_exp_file(self):
        res = setting_api.export_setting_exp('/tmp/gre_test.exp')
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
            filepath='/tmp/gre_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_06_settings_check_after_exp_import(self):
        out = if_v4_api.get_tunnel_interface_status(name='gre_t1', type='4to6')
        Assertion.assert_equal(bool(out), True, 'ERR: settings check failed!!')

    def test_07_function_check_after_exp_import(self):
        Test_GRE4to6_TC1523869().test_05_test_traffic_cross_Gre_tunnel()


# [Function][Gre4to6][4.8.11] when we add a Gre4to6 interface, the configuraiton can't lost after we reboot the box
class Test_GRE4to6_TC1523872(Test):
    uuid = "SOSAIOT-TC-56596"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot_fw(self):
        res = setting_api.boot_fw(mode=1)
        Assertion.assert_equal(res, True, "ERR: reboot unit failed")

    def test_02_settings_check_after_reboot(self):
        Test_GRE4to6_TC1523871().test_06_settings_check_after_exp_import()


# [Function][Gre4to6][4.9]  After we add a Gre4to6 interface, if we change some option it can work normally
class Test_GRE4to6_TC2682749(Test):
    uuid = "SOSAIOT-TC-56591"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_gre_tunnel_iface(self):
        opt = {
            'ip_addr': "1.1.1.3"
        }
        rc = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit gre tunnle interface failed!!')

    def test_02_test_traffic_cross_Gre_tunnel(self):
        Test_GRE4to6_TC1523869().test_05_test_traffic_cross_Gre_tunnel()


# [Function][Gre4to6][4.8.0] they can work normally if we add multiple softwire who bound to same wan interface.
class Test_GRE4to6_TC1523870(Test):
    uuid = "SOSAIOT-TC-56594"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_second_gre_tunnel_iface_on_local(self):
        gre_t2_local = {
            'name': 'gre_t2',
            'ip_addr': '2.2.2.1',
            'bound_to_if': 'X2',
            'remote_ipv6_addr': '2101::169',
            'local': {"ipv6": "2101::168"}
        }
        rc = if_v4_api.add_gre4to6_tunnel_interface(**gre_t2_local)
        Assertion.assert_equal(rc, True,
                               'ERR: add the second gre4to6 tunnel interface on local firewall failed!!')

    def test_02_add_second_gre_tunnel_iface_on_remote(self):
        gre_t2_remote = {
            'name': 'gre_t2',
            'ip_addr': '2.2.2.2',
            'bound_to_if': 'X2',
            'remote_ipv6_addr': '2101::168',
            'local': {"ipv6": "2101::169"}
        }
        rc = rm_ifacev4_api.add_gre4to6_tunnel_interface(**gre_t2_remote)
        Assertion.assert_equal(rc, True,
                               'ERR: add the second gre4to6 tunnel interface on remote firewall failed!!')

    def test_03_add_routes_on_local_firewall(self):
        route = copy.deepcopy(route_base)
        route.update({"destination": {"name": "172.16.1.0/24"}, "interface": "gre_t2"})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, 'ERR: add routes on remote firewall failed!!')

    def test_04_add_routes_on_remote_firewall(self):
        route = copy.deepcopy(route_base)
        route.update({"destination": {"name": "192.168.168.0/24"}, "interface": "gre_t2"})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = rem_route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, "ERR: add route policy on local firewall failed!!")

    def test_05_traffic_check_cross_gre_tunnel(self):
        Test_GRE4to6_TC1523869().test_05_test_traffic_cross_Gre_tunnel()

    def test_06_delete_second_gre_tunnel_iface(self):
        rc1 = if_v4_api.delete_gre4to6_tunnel_interface_by_name('gre_t2')
        rc2 = rm_ifacev4_api.delete_gre4to6_tunnel_interface_by_name('gre_t2')
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: delete gre tunnel interface failed!!')


# [Function][Gre4to6][4.9.1]  After we add a Gre4to6 interface, if we change the bould interface it can work normally
class Test_GRE4to6_TC1523873(Test):
    uuid = "SOSAIOT-TC-56597"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_the_outbound_interface(self):
        opt = {
            'bound_to_if': "X1"
        }
        rc = if_v4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit gre tunnel interface outbound interface failed!!')

    def test_02_update_remote_gre_tunnel_iface(self):
        opt = {
            'bound_to_if': "X1"
        }
        rc = rm_ifacev4_api.edit_gre4to6_tunnel_interface_by_name(tunnel_name='gre_t1', **opt)
        Assertion.assert_equal(rc, True,
                               'ERR: edit gre tunnel interface outbound interface on remote firewall failed!!')

    def test_03_check_traffic_cross_gre_tunnel(self):
        Test_GRE4to6_TC1523869().test_05_test_traffic_cross_Gre_tunnel()


# [Function][Gre4to6][5.1.4]  After we add a Gre4to6 interface, when I run ipv4 traffic from lan to customer zone, it can work normally
class Test_GRE4to6_TC1523875(Test):
    uuid = "SOSAIOT-TC-56598"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_route_on_remote(self):
        route = copy.deepcopy(route_base)
        route.update(
            {"destination": {"name": "192.168.168.0/24"}, "interface": "gre_t1", "source": {"name": "X3 Subnet"}})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = rem_route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, 'ERR: add route on remote firewall failed!!')

    def test_02_add_route_on_local(self):
        route = copy.deepcopy(route_base)
        route.update({"destination": {"name": "12.12.3.0/24"}, "interface": "gre_t1"})
        route_opt = {"route_policies": [{"ipv4": route}]}
        rc = route_api.add_route_policy(**route_opt)
        Assertion.assert_equal(rc, True, 'ERR: add route on remote firewall failed!!')

    def test_03_check_traffic_to_customer_zone(self):
        pc1_login.send_command('route add -net 12.12.3.0/24 gateway 192.168.168.168')
        rc = False
        init_packet_capture()
        pc1_login.send_command('ping 172.16.1.100 -c 5')
        pkt_api.stop_capture()
        pkt_api.export_captured_packets_pcapng(filepath='/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        pkt_list = pkts.split('Packet comments')
        for pkt in pkt_list:
            check_list = ('Src: 2102::168', ' Dst: 2102::169', "Generic Routing Encapsulation (IP)")
            if all(x in pkt for x in check_list):
                logger.info(f'found the GRE encapsulate packet:\n{pkt}')
                rc = True
                break
        else:
            logger.error('not found the GRE encapsulated packet')
        Assertion.assert_equal(rc, True, 'ERR: function check the Gre4to6 interface failed!!')

    def test_03_init_pc1(self):
        pc1_login.send_command('route del -net 12.12.3.0/24 gateway 192.168.168.168')
        Assertion.assert_equal(True, True, 'ERR: remove route on pc1 failed!!')
