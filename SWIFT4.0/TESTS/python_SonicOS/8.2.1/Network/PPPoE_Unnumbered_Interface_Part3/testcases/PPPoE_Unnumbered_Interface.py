from definition.settings import *
from definition.utils import *


# GUI set VLAN port to unnumbered
class Test_Config_TC02(Test):
    uuid = "SOSAIOT-TC-57150"
    description = show_testcase_info(TESTPLAN, "02", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "02")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_config_x4_vlan_unnumber_ip(self):
        res = interfaceapi.edit_vlan_interface(**CaseParams.x4_vlan_unnum_dict)
        Assertion.assert_equal(res, True, "ERR: Config X4:1 failed.")

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        res = interfaceapi.config_interface(**CaseParams.x1_pppoe_unnum_vlan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 failed.")

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X4_VLAN_IP, "Error: X1 should obtain same IP with X4:1."
        )


# Verify MGMT on unnumbered VLAN interface
class Test_MGMT_TC21(Test):
    uuid = "SOSAIOT-TC-57159"
    description = show_testcase_info(TESTPLAN, "21", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "21")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC02().test_03_verify_x1_can_get_ip_pppoe()

    def test_02_confirm_mgmt_status_enabled(self):
        port_servs_dict = [
            '"https": true',
            '"ping": true',
            '"ssh": true',
            '"snmp": true',
        ]
        port_info = interfaceapi.get_interface_status(f"X4:V{X4_VLAN_ID}")
        res = confirm_port_servs(port_info, port_servs_dict)
        Assertion.assert_equal(
            res, True, "ERR: Confirm mgmt on VLAN interface X4:1 failed."
        )

    def test_03_verify_mgmt_ping_enabled(self):
        output = PC4_login.ping(ip=Parameter.X4_VLAN_IP)
        Assertion.assert_equal(
            output,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via ping from WAN failed",
        )

    def test_04_verify_mgmt_https_enabled(self):
        curl_cmd = (
            'curl -o /dev/null -skL -w "%{http_code}\n" https://'
            + Parameter.X4_VLAN_IP
            + " --connect-timeout 3"
        )
        curl_res = "200" in str(PC4_login.send_command(curl_cmd))
        Assertion.assert_equal(
            curl_res,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via https from WAN failed",
        )

    def test_05_verify_mgmt_ssh_enabled(self):
        nc_cmd = f"ncat -i 1 {Parameter.X4_VLAN_IP} 22"
        nc_res = "SSH" in PC4_login.send_command(nc_cmd)
        Assertion.assert_equal(
            nc_res,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via ssh from WAN failed",
        )

    @repeat_method(5)
    def test_06_verify_mgmt_snmp_enabled(self):
        time.sleep(10)
        user_name = snmp_user_dict["user_name"]
        snmp_cmd = f"snmpwalk -c public -u {user_name} {Parameter.X4_VLAN_IP} -l noAuthNoPriv .1.3.6.1.2.1.1.1.0"
        snmp_res = PC4_login.send_command(snmp_cmd)
        # Response example >> SNMPv2-MIB::sysDescr.0 = STRING: SonicWALL TZ 370 (SonicOS 7.1.1-7051-P5654)
        Assertion.assert_equal(
            "sonicwall" in snmp_res.lower(),
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via snmp from WAN failed",
        )


# Unable to delete the bounded VLAN interface
class Test_Config_TC37(Test):
    uuid = "SOSAIOT-TC-57167"
    description = show_testcase_info(TESTPLAN, "37", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "37")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC02().test_03_verify_x1_can_get_ip_pppoe()

    def test_02_del_vlan_iface_x4(self):
        vlan_iface = {
            "type": "vlan",
            "if": "X4",
            "vlan_tag": X4_VLAN_ID,
        }
        res = interfaceapi.del_interface(**vlan_iface)
        Assertion.assert_equal(res, False, "ERR: Delete VLAN interface X4:1 failed")


# Down & Up interface
class Test_Config_TC43(Test):
    uuid = "SOSAIOT-TC-57171"
    description = show_testcase_info(TESTPLAN, "43", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "43")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        res = interfaceapi.config_interface(**CaseParams.x2_lan_unnum_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failed.")

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        res = interfaceapi.config_interface(**CaseParams.x1_pppoe_unnum_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 failed.")

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X2_IP, "Error: X1 should obtain same IP with X2."
        )

    def test_04_config_x1_disable(self):
        res = interfaceapi.disable_interface("X1")
        Assertion.assert_equal(res, True, "ERR: Disable X1 failed.")

    def test_05_confirm_x1_disable_status(self):
        x1_info = interfaceapi.get_interface_status("X1")
        res = is_port_disabled(x1_info)
        Assertion.assert_equal(res, True, "ERR: Confirm X1 disabled status failed.")

    def test_06_config_x1_enable(self):
        res = interfaceapi.enable_interface("X1")
        Assertion.assert_equal(res, True, "ERR: Enable X1 failed.")

    @repeat_method(20)
    def test_07_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()


# Verify traffic LAN > WAN
class Test_Traffic_TC17(Test):
    uuid = "SOSAIOT-TC-57155"
    description = show_testcase_info(TESTPLAN, "17", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "17")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()

    @repeat_method(5)
    def test_02_verify_ping_lan_to_wan(self):
        time.sleep(5)
        output = PC3_login.ping(ip=PC5_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: Ping remote WAN IP failed")

    def test_03_verify_https_lan_to_wan(self):
        curl_cmd = f"curl -kvL https://{PC5_ETH1_IP}"
        curl_res = "auto_cfs_html_tag" in str(PC3_login.send_command(curl_cmd))
        Assertion.assert_equal(curl_res, True, "ERR: LAN to WAN HTTPs failed.")

    def test_04_verify_ftp_lan_to_wan(self):
        ftp_cmd = f"rm -f ./text.txt* && wget ftp://{PC5_ETH1_IP}/test.txt && ls -l && cat ./test.txt"
        ftp_res = "pppoe ftp" in PC3_login.send_command(ftp_cmd)
        Assertion.assert_equal(ftp_res, True, "ERR: LAN to WAN FTP failed.")


# Add DHCP scope on unnumbered interface
class Test_DHCP_TC50(Test):
    uuid = "SOSAIOT-TC-57173"
    description = show_testcase_info(TESTPLAN, "50", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "50")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()

    def test_02_add_dhcp_scope_x2(self):
        dyn_scope = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "192.168.2.101",
                                "to": "192.168.2.109",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "192.168.2.168",
                                "netmask": "255.255.255.0",
                                "comment": "",
                                "allow_bootp": False,
                                "domain_name": "",
                                "dns": {"server": {"inherit": True}},
                                "wins": {"primary": "", "secondary": ""},
                                "call_manager": {
                                    "primary": "",
                                    "secondary": "",
                                    "tertiary": "",
                                },
                                "network_boot": {
                                    "next_server": "",
                                    "boot_file": "",
                                    "server_name": "",
                                },
                                "generic_option": {},
                                "always_send_option": False,
                            }
                        ]
                    }
                }
            }
        }
        res = dhcpserverapi.add_dhcp_server_scope_dynamic(**dyn_scope)
        Assertion.assert_equal(res, True, "ERR: Add DHCP scope for X2 failed.")

    def test_03_verify_get_ip_pc2(self):
        dhcp_cmds = ["ifconfig eth1 0.0.0.0", "dhclient eth1 -r", "dhclient eth1 -v"]
        chk_keys = ["bound to 192.168.2.", "from 192.168.2.168"]
        dhcp_res = (
            len([key for key in chk_keys if key in PC2_login.send_commands(dhcp_cmds)])
            == 2
        )
        Assertion.assert_equal(dhcp_res, True, "ERR: LAN to WAN FTP failed.")

    @repeat_method(5)
    def test_04_verify_ping_pc2_to_x2(self):
        time.sleep(5)
        output = PC2_login.ping(ip=Parameter.X2_IP)
        Assertion.assert_equal(output, True, "ERR: Ping X2 IP from PC2 failed")


# Verify DHCP scope can work after PPPoE reconnected
class Test_DHCP_TC51(Test):
    uuid = "SOSAIOT-TC-57174"
    description = show_testcase_info(TESTPLAN, "51", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "51")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()

    def test_02_confirm_dhcp_scope_x2(self):
        chk_dyn_scope = [
            '"from": "192.168.2.101"',
            '"to": "192.168.2.109"',
            '"default_gateway": "192.168.2.168"',
            '"netmask": "255.255.255.0"',
        ]
        dyn_dhcp_info = dhcpserverapi.get_dhcp_server_scope_dynamic()
        res = is_dyn_dhcps_enabled(dyn_dhcp_info, chk_dyn_scope)
        Assertion.assert_equal(res, True, "ERR: Confirm DHCP scope for X2 failed.")

    @repeat_method(5)
    def test_03_verify_x1_pppoe_disconnect(self):
        opt_res = interfaceapi.click_pppoe_disconnect("X1")
        logger.info("Sleep 10s before the next step.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        chk_res = PPPoeParams.PPPOE_DOWN_IP in str(resp)
        Assertion.assert_equal(
            chk_res,
            True,
            "Error: X1 should obtain same IP with 0.0.0.0.",
        )

    def test_04_verify_get_ip_pc2(self):
        Test_DHCP_TC50().test_03_verify_get_ip_pc2()

    def test_05_verify_ping_pc2_to_x2(self):
        Test_DHCP_TC50().test_04_verify_ping_pc2_to_x2()

    @repeat_method(5)
    def test_06_verify_x1_pppoe_connect(self):
        opt_res = interfaceapi.click_pppoe_connect("X1")
        logger.info("Sleep 10s before the next step.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        chk_res = x1_ip == Parameter.X2_IP
        Assertion.assert_equal(
            chk_res, True, "Error: X1 should obtain same IP with X2."
        )

    def test_07_verify_get_ip_pc2(self):
        Test_DHCP_TC50().test_03_verify_get_ip_pc2()

    def test_08_verify_ping_pc2_to_x2(self):
        Test_DHCP_TC50().test_04_verify_ping_pc2_to_x2()


# NAT policy update
class Test_Traffic_TC39(Test):
    uuid = "SOSAIOT-TC-57168"
    description = show_testcase_info(TESTPLAN, "39", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "39")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()

    def test_02_confirm_nat_policies_pppoe_unnumber(self):
        nat_polis = natapi.get_nat_policy()
        res = chk_unnumber_nat_polis(nat_polis)
        Assertion.assert_equal(
            res, True, "ERR: Confirm NAT policies for unnumbered mode failed."
        )

    def test_03_config_x1_wan_static(self):
        res = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 static failed.")

    @repeat_method(5)
    def test_04_verify_x1_can_get_ip_static(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X1_IP, "Error: X1 should obtain same IP with X2."
        )

    def test_05_confirm_nat_policies_pppoe_unnumber(self):
        nat_polis = natapi.get_nat_policy()
        res = chk_unnumber_nat_polis(nat_polis, chk_exist=False)
        Assertion.assert_equal(
            res, True, "ERR: Confirm NAT policies for unnumbered mode failed."
        )

    def test_06_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC17().test_02_verify_ping_lan_to_wan()

    def test_07_verify_nat_lan_to_wan(self):
        logger.info("Verify NAT in the ping traffic from LAN to WAN")
        run_ping_dict = {
            "type": "ping",
            "pc_login": PC3_login,
            "des": PC5_ETH1_IP,
            "packet_obj": packetmonitorapi,
        }
        pingres, packets = fw_packet_monitor_run(**run_ping_dict)
        logger.info(f"Got ping result is: {pingres}")
        req_filters = [
            "ICMP",
            "in:X3",
            "out:X1",
            "IP Type: ICMP",
            "Src=[{PC3_ETH1_IP}]",
            f"Dst=[{PC5_ETH1_IP}]",
            "Forwarded",
        ]
        reqres, pkts_filted = check_capture_packets(packets, req_filters)
        logger.info(f"check http response forwarded result: {pkts_filted}")
        logger.info("check request: {reqres}, check response: {respres}")
        Assertion.assert_equal(
            not reqres, True, "ERR: Verify NAT in ping traffice failed."
        )


# Verify Ping WAN > LAN
class Test_Traffic_TC24(Test):
    uuid = "SOSAIOT-TC-57161"
    description = show_testcase_info(TESTPLAN, "24", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "24")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC43().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC43().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC43().test_03_verify_x1_can_get_ip_pppoe()

    def test_04_edit_default_acl_to_allow(self):
        res = False
        getres = accessruleapi.get_accessrule_via_zones(srczone="WAN", dstzone="LAN")
        try:
            for rule in getres["access_rules"]:
                if rule["ipv4"]["name"] == "Default Access Rule":
                    if rule["ipv4"]["action"] == "deny":
                        logger.info(f"Get target rule successful: {rule}")
                        acl_dict = copy.deepcopy(default_acl_dict)
                        # acl_dict.update({"from": "WAN", "to": "LAN"})
                        res = accessruleapi.config_accessrule_via_uuid(
                            uuid=rule["ipv4"]["uuid"], acl_json=acl_dict
                        )
                    if rule["ipv4"]["action"] == "allow":
                        logger.info("Get the allow action successful")
                        res = True
                    break
        except exception as e:
            logger.error(f"Get wan to lan acl failed: {e}")
        Assertion.assert_equal(
            res, True, "ERR: Edit default wan to lan access rule to Allow failed..."
        )

    @repeat_method(5)
    def test_05_verify_ping_wan_to_lan(self):
        time.sleep(5)
        logger.info("Add route on WAN PC5 for unumbered PC2")
        cmd = "ip r a 192.168.2.0/24 via 192.168.2.168"
        _ = PC5_login.send_command(cmd)
        cmds = [
            "ip r d default via 192.168.2.1 dev eth1",
            "ip r a default via 192.168.2.168 dev eth1",
        ]
        _ = PC2_login.send_commands(cmds)
        pc2_eth1_dhcp_ip = "188.188.188.188"
        cmd = "ip -4 -o a s eth1 | awk '{print $4}'"
        pc2_eth1_info = PC2_login.send_command(cmd)
        if "192.168.2" in pc2_eth1_info:
            pc2_eth1_dhcp_ip = pc2_eth1_info.split("/")[0]
        output = PC5_login.ping(ip=pc2_eth1_dhcp_ip)
        Assertion.assert_equal(output, True, "ERR: Ping LAN IP from WAN failed")


# WAN > LAN NAT
class Test_Traffic_TC41(Test):
    uuid = "SOSAIOT-TC-57170"
    description = show_testcase_info(TESTPLAN, "41", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "41")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_ping_wan_to_lan(self):
        Test_Traffic_TC24().test_05_verify_ping_wan_to_lan()

    def test_03_add_nat_policy(self):
        res = False
        base_dict = {
            "name": "pppoe_unnum_case_41",
            "inbound": "X1",
            "destination": {"name": "X1 IP"},
            "translated_destination": {"name": "lan_pc3"},
            "service": {"name": "ssh_20022"},
            "translated_service": {"name": "SSH"},
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        addres = natapi.add_nat_policy(**nat_dict)
        if addres:
            natgetres = natapi.get_nat_policy(name=base_dict["name"])
            res = True if base_dict["name"] in str(natgetres) else False
        else:
            logger.error("ERR: Add nat policy failed")
        Assertion.assert_equal(res, True, "ERR: Add nat policy failed")

    def test_04_verify_nat_policy(self):
        nc_cmd = f"ncat -i 1 {Parameter.X2_IP} {pc3_ssh_serv_obj_dict['tcp']['begin']}"
        nc_res = "SSH" in PC5_login.send_command(nc_cmd)
        Assertion.assert_equal(
            nc_res,
            True,
            "ERR: Check NAT policy from WAN failed",
        )
