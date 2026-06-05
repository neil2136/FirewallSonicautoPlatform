from definition.settings import *
from definition.utils import *

# change X3 routed mode port successful
class Test_Update_TC74(Test):
    uuid = "SOSAIOT-TC-57193"
    description = show_testcase_info(TESTPLAN, '74', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '74')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_wan(self):
        logger.info('config interface x2 WAN...')
        x2_wan_dict = {
            'if': 'X2',
            'zone': 'wan',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 in zone WAN ")

    def test_02_config_x3_DMZ_and_routed_mode_with_x2(self):
        logger.info('config interface x3 DMZ and routed mode with X2...')
        x3_dmz_dict = {
            'if': 'X3',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'routed_mode': {
                "interface": "X2"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x3_dmz_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X3 DMZ and routed mode with X2 failed")

    def test_03_check_x3_DMZ_and_routed_mode_with_x2(self):
        logger.info('check interface x3 DMZ Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X3', 'X2')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x3 DMZ Auto-added No-NAT policy failed")

    def test_04_config_x3_DMZ_and_routed_mode_with_x1(self):
        logger.info('config interface x3 DMZ and routed mode with X1')
        x3_dmz_dict = {
            'if': 'X3',
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'routed_mode': {
                "interface": "X1"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x3_dmz_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X3 DMZ and routed mode with X1 failed")

    def test_05_check_x3_DMZ_and_routed_mode_with_x1(self):
        logger.info('check interface x3 DMZ Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X3', 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x3 DMZ Auto-added No-NAT policy failed")

# check VLAN subinterface routed mode port successful
class Test_VLAN_TC75(Test):
    uuid = "SOSAIOT-TC-57194"
    description = show_testcase_info(
        TESTPLAN, '75', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '75')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_x4_vlan_subinterface_and_routed_mode_with_x1(self):
        logger.info('check x4 vlan subinterface Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X4:V' + str(X4_VLAN1_ID), 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check x4 vlan subinterface and routed mode with X1 failed")

    def test_03_verify_ping_traffic(self):
        logger.info('verify pc3 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc3_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X4:V' + str(X4_VLAN1_ID), 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{PC3_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")

# check Portshield interface routed mode port successful
class Test_Portshield_TC76(Test):
    uuid = "SOSAIOT-TC-57195"
    description = show_testcase_info(
        TESTPLAN, '76', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '76')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_portshield_to_x0(self):
        resp = {}
        # forbid other interface bind to X0
        x2_portshield_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'portshield',
            'portshield_to': 'X0'
        }
        conf_res = interface_obj.config_interface(**x2_portshield_dict)
        if conf_res:
            resp = interface_obj.get_interface_status('x2')
        Assertion.assert_regular(json.dumps(
            resp), '"mode": {"portshield": "X0"}', 'ERR: config x2 failed')

    def test_02_verify_pc1_traffic(self):
        logger.info('verify pc1 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc1_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X0', 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{PC1_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")

    def test_03_verify_pc2_traffic(self):
        logger.info('verify pc2 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc2_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X0', 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{Parameter.PC2_ETH1_portshield}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")

# check X0 IPV4 NO-NAT and IPV6 NAT successful
class Test_Ipv6_TC77(Test):
    uuid = "SOSAIOT-TC-57196"
    description = show_testcase_info(
        TESTPLAN, '77', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '77')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_addrobj_publicIP(self):
        obj = {
            'object_type': 'host',
            'name': 'Public-IP',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
        }
        rc = address_obj.config_ipv6_addressobject(**obj)
        Assertion.assert_equal(
            rc, True, "ERR: Add Public-IP address obj failed!")

    def test_02_add_addrobj_privateIP(self):
        obj = {
            'object_type': 'host',
            'name': 'Private-IP',
            'zone': 'WAN',
            'ip': Parameter.lan_host1,
        }
        rc = address_obj.config_ipv6_addressobject(**obj)
        Assertion.assert_equal(
            rc, True, "ERR: Add Public-IP address obj failed!")

    def test_03_add_ipv6_nat_policy(self):
        # source : trans_src -> Private IP; translated_src -> Public IP
        ipv6_nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "name": "TEST1",
                    "reflexive": False,
                    "source_port_remap": True,
                    "comment": "test",
                    "enable": True,
                    "inbound": "X0",
                    "outbound": "X1",
                    "source": {
                        "name": "Private-IP"
                    },
                    "translated_source": {
                        "name": "Public-IP"
                    },
                    "destination": {
                        "any": True
                    },
                    "translated_destination": {
                        "original": True
                    },
                    "service": {
                        "any": True
                    },
                    "translated_service": {
                        "original": True
                    },
                    "ticket": {
                        "tag1": "",
                        "tag2": "",
                        "tag3": ""
                    }
                }
            }]
        }
        rc = nat_obj.add_nat_policy(**ipv6_nat_json)
        Assertion.assert_equal(rc, True, "ERR: Add ipv6 nat policy failed")

    def test_04_verify_pc1_ipv4_traffic(self):
        logger.info('verify pc1 ipv4 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc1_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X0', 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{PC1_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")

    def test_05_verify_pc1_ipv6_traffic(self):
        logger.info('verify pc1 ipv6 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping6 -c 4 -i 3 -I eth1 {}'.format(Parameter.wan_ip),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc1_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMPV6', 'in:X1', 'out:X0',
                           f'Src=[{Parameter.wan_ip}]', f'Dst=[{Parameter.X1_IPv6}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via NAT mode failed.")

    def test_06_delete_ipv6_nat_policy(self):
        rc = nat_obj.del_nat_policy_by_name(name='TEST1', version='ipv6')
        Assertion.assert_equal(
            rc, True, "ERR: Delete TEST1 nat policy failed!")

    def test_07_delete_ipv6_addrobjs(self):
        rc1 = address_obj.delete_addressobject(
            'host', object_path='name', object_name_uuid='Public-IP', ip_type='ipv6')
        rc2 = address_obj.delete_addressobject(
            'host', object_path='name', object_name_uuid='Private-IP', ip_type='ipv6')
        Assertion.assert_equal(
            rc1 & rc2, True, "ERR: Delete address objects failed!")

    def test_08_unassign_X1_ipv6(self):
        rc = interface_obj_v6.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(rc, True, "ERR: Unassign X1 ipv6 failed!")

# Reboot firewall
class Test_Reboot_TC78(Test):
    uuid = "SOSAIOT-TC-57197"
    description = show_testcase_info(
        TESTPLAN, '78', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '78')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info('config interface x2...')
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                "interface": "X1"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_check_x2_lan_and_routed_mode_with_x1(self):
        logger.info('check interface x2 lan Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X2', 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x2 lan Auto-added No-NAT policy failed")

    def test_03_restart_FW(self):
        logger.info('check restart firmware...')
        rc1 = restart_obj.restart_now()
        Assertion.assert_equal(rc1, True, "ERR: restart FW failed")

    def test_04_check_x2_lan_and_routed_mode_with_x1(self):
        logger.info('check interface x2 lan Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X2', 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x2 lan Auto-added No-NAT policy failed")

    def test_05_config_PC_route(self):
        res = {}
        cmd_pc2 = [
            f"ifconfig eth1 {Parameter.PC2_ETH1}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X2_IP}",
            "ip -4 r",
        ]
        cmd_pc4 = [
            f"route add -net 192.168.2.0/24 gw {Parameter.X1_IP}",
            "ip -4 r",
        ]
        rc1 = pc2_ssh.send_commands(cmd_pc2)
        rc2 = pc4_ssh.send_commands(cmd_pc4)
        logger.info(f'run cmd result in pcs:{rc1}...{rc2}...')
        res["pc2"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.X2_IP}" in rc1
            else False
        )
        res["pc4"] = (
            True
            if f"192.168.2.0/24 via {Parameter.X1_IP}" in rc2
            else False
        )
        Assertion.assert_equal(all(res.values()), True,
                               'ERR: config routers for PC failed')

    def test_06_verify_ipv4_traffic(self):
        logger.info('verify pc2 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc2_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X2', 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{PC2_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")

# Check TSR
class Test_TSR_TC79(Test):
    uuid = "SOSAIOT-TC-57198"
    description = show_testcase_info(
        TESTPLAN, '79', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '79')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_disable_routed_mode(self):
        logger.info('config interface x2...')
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 disable routed mode")

    def test_02_check_TSR_disable_routed_mode(self):
        x2_routed_mode = "Use Routed Mode" + " " * 33 + ": No"
        tsr_x2_info = diag_obj.get_tsr_interface_part(lab1="X2", lab2="X3")
        logger.info(f'show X2 interface config : {tsr_x2_info}..')
        chk_x2_res = True if x2_routed_mode in tsr_x2_info else False
        Assertion.assert_equal(
            chk_x2_res, True, "ERR: Confirm disable ports routed mode in TSR."
        )

    def test_03_config_interface_x2_enable_routed_mode(self):
        logger.info('config interface x2...')
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                "interface": "X1"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 enable routed mode")

    def test_04_check_TSR_enable_routed_mode(self):
        x2_routed_mode = "Use Routed Mode" + " " * 33 + ": Yes"
        tsr_x2_info = diag_obj.get_tsr_interface_part(lab1="X2", lab2="X3")
        logger.info(f'show X2 interface config : {tsr_x2_info}..')
        chk_x2_res = True if x2_routed_mode in tsr_x2_info else False
        Assertion.assert_equal(
            chk_x2_res, True, "ERR: Confirm enable ports routed mode in TSR."
        )

# Export / Import configuration
class Test_EXP_TC80(Test):
    uuid = "SOSAIOT-TC-57199"
    description = show_testcase_info(
        TESTPLAN, '80', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '80')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_enable_routed_mode(self):
        logger.info('config interface x2...')
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'routed_mode': {
                "interface": "X1"
            },
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_02_Export_Perference(self):
        rc = setting_obj.export_setting_exp(
            filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export settings...")

    def test_03_config_interface_x2_disable_routed_mode(self):
        logger.info('config interface x2...')
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_04_check_x2_disable_routed_mode_with_x1(self):
        logger.info('check interface x2 and nat policy...')
        output = nat_obj.get_nat_policy()
        rc = check_no_nat_policy(output, 'X2', 'X1')
        Assertion.assert_equal(
            rc, False, "ERR: Check X2 and routed mode with X1 failed")

    def test_06_Import_Perference(self):
        rc = setting_obj.import_setting_exp(
            filepath='/tmp/preference_test.exp')
        logger.info(rc)
        Assertion.assert_equal(
            rc, True, "Error: Failed to import the settings...")

    def test_07_check_x2_enable_routed_mode_with_x1(self):
        logger.info('check interface x2 lan Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X2', 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x2 lan Auto-added No-NAT policy failed")

# Enable X0 routed mode port successful via CLI
class Test_CLI_TC_81(Test):
    uuid = "SOSAIOT-TC-57200"
    description = show_testcase_info(
        TESTPLAN, '81', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '81')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x0_disable_routed_mode(self):
        logger.info('config interface x0...')
        x0_lan_dict = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X0_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X0_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x0_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv4 failed")

    def test_02_check_x0_disable_routed_mode_with_x1(self):
        logger.info('check interface x0 and check nat policy...')
        output = nat_obj.get_nat_policy()
        rc = check_no_nat_policy(output, 'X0', 'X1')
        Assertion.assert_equal(
            rc, False, "ERR: Check X0 and routed mode with X1 failed")

    def test_04_CLI_config_x0_enable_routed_mode_with_x1(self):
        flag = False
        commands = ['configure', 'interface X0',
                    'routed-mode interface X1', 'commit', 'exit', 'show interface X0']
        rc = fw_cli.do_cli_commands(commands, tag=1)[1]
        logger.info(f"CLI config result is: {rc}")
        if rc:
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR: CLI config X0 routed mode with X1 failed")

    def test_05_check_x0_enable_routed_mode_with_x1(self):
        logger.info('check interface x0 lan Auto-added No-NAT policy')
        output = nat_obj.get_nat_policy()
        logger.info('check...')
        rc = check_no_nat_policy(output, 'X0', 'X1')
        Assertion.assert_equal(
            rc, True, "ERR: check interface x0 lan Auto-added No-NAT policy failed")

    def test_06_verify_ipv4_traffic(self):
        logger.info('verify pc1 ping traffic...')
        flag = False
        run_ping_dict = {
            'cmd': 'ping {} -c 5'.format(PC4_ETH1_IP),
            'packet_obj': packetmonitor_obj,
            'pc_login': pc1_ssh
        }
        (pingres, packets) = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f'...Got ping result is: {pingres}')
        if '0% packet loss' in pingres:
            flag = True
        request_filters = ['ICMP', 'in:X1', 'out:X0', 'IP Type: ICMP',
                           f'Src=[{PC4_ETH1_IP}]', f'Dst=[{PC1_ETH1_IP}]', 'Forwarded']
        (reqres, packet) = check_capture_packets(packets, request_filters)
        logger.info(f'Got the captured packet with request filters: {packet}')
        logger.info(f'Got captured packets result: {reqres}')
        Assertion.assert_equal(reqres & flag, True,
                               "ERR: test traffic via routed mode failed.")
