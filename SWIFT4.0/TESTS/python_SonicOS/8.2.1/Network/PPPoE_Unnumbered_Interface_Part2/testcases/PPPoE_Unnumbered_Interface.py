from definition.settings import *
from definition.utils import *


# GUI set PPPoE unnumbered successful
class Test_Config_TC06(Test):
    uuid = "SOSAIOT-TC-57151"
    description = show_testcase_info(TESTPLAN, "06", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "06")
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


# Ping the PPPoE unnumbered interface IP successful
class Test_Traffic_TC18(Test):
    uuid = "SOSAIOT-TC-57156"
    description = show_testcase_info(TESTPLAN, "18", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "18")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(5)
    def test_03_can_ping_wan_from_lan_pc(self):
        time.sleep(5)
        output = PC3_login.ping(ip=PC4_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: Ping remote WAN IP failed")

    def test_04_can_ping_x1_from_wan(self):
        output = PC4_login.ping(ip=Parameter.X2_IP)
        Assertion.assert_equal(
            output, True, "ERR: Ping PPPoE unnumbered interface from remote failed"
        )


# Check the PPPoE unnumbered interface MGMT via WAN
class Test_MGMT_TC19(Test):
    uuid = "SOSAIOT-TC-57157"
    description = show_testcase_info(TESTPLAN, "19", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "19")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    def test_03_confirm_mgmt_status_enabled(self):
        port_servs_dict = [
            '"https": true',
            '"ping": true',
            '"ssh": true',
            '"snmp": true',
        ]
        port_info = interfaceapi.get_interface_status("X1")
        res = confirm_port_servs(port_info, port_servs_dict)
        Assertion.assert_equal(res, True, "ERR: Confirm mgmt on X1 failed.")

    def test_04_verify_mgmt_ping_enabled(self):
        output = PC4_login.ping(ip=Parameter.X2_IP)
        Assertion.assert_equal(
            output,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via ping from WAN failed",
        )

    def test_05_verify_mgmt_https_enabled(self):
        curl_cmd = (
            'curl -o /dev/null -skL -w "%{http_code}\n" https://'
            + Parameter.X2_IP
            + " --connect-timeout 3"
        )
        curl_res = "200" in str(PC4_login.send_command(curl_cmd))
        Assertion.assert_equal(
            curl_res,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via https from WAN failed",
        )

    def test_06_verify_mgmt_ssh_enabled(self):
        nc_cmd = f"ncat -i 1 {Parameter.X2_IP} 22"
        nc_res = "SSH" in PC4_login.send_command(nc_cmd)
        Assertion.assert_equal(
            nc_res,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via ssh from WAN failed",
        )

    @repeat_method(5)
    def test_07_verify_mgmt_snmp_enabled(self):
        time.sleep(10)
        user_name = snmp_user_dict["user_name"]
        snmp_cmd = f"snmpwalk -c public -u {user_name} {Parameter.X2_IP} -l noAuthNoPriv .1.3.6.1.2.1.1.1.0"
        snmp_res = PC4_login.send_command(snmp_cmd)
        # Response example >> SNMPv2-MIB::sysDescr.0 = STRING: SonicWALL TZ 370 (SonicOS 7.1.1-7051-P5654)
        Assertion.assert_equal(
            "sonicwall" in snmp_res.lower(),
            True,
            "ERR: Check PPPoE unnumbered interface MGMT via snmp from WAN failed",
        )


# Check the PPPoE unnumbered interface MGMT disabled via X1 and X2
class Test_MGMT_TC23(Test):
    uuid = "SOSAIOT-TC-57160"
    description = show_testcase_info(TESTPLAN, "23", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "23")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip_with_mgmt_disabled(self):
        x2_disable_serv_dict = {
            "if": "x2",
            "zone": "LAN",
            "mode": "unnumbered",
            "ip": Parameter.X2_IP,
            "netmask": "255.255.255.0",
            "mgmt_https": False,
            "mgmt_ssh": False,
            "mgmt_ping": False,
            "user_https": False,
            "mgmt_snmp": False,
        }
        res = interfaceapi.config_interface(**x2_disable_serv_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failed.")

    def test_02_config_pppoe_wan_for_x1_with_unnumber_and_mgmt_disabled(self):
        x1_disable_serv_dict = {
            "if": "x1",
            "zone": "WAN",
            "mode": "pppoe",
            "pppoe_unnumbered": "X2",
            "pppoe_user": "root",
            "pppoe_servicename": "def",
            "pppoe_passwd": "password",
            "mgmt_https": False,
            "mgmt_ssh": False,
            "mgmt_ping": False,
            "user_https": False,
            "mgmt_snmp": False,
        }
        res = interfaceapi.config_interface(**x1_disable_serv_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 failed.")

    def test_03_confirm_mgmt_status_disabled(self):
        port_disable_servs_dict = [
            '"https": false',
            '"ping": false',
            '"ssh": false',
            '"snmp": false',
        ]
        port_info = interfaceapi.get_interface_status("X1")
        res = confirm_port_servs(port_info, port_disable_servs_dict)
        Assertion.assert_equal(res, True, "ERR: Confirm mgmt on X1 failed.")

    def test_04_verify_mgmt_ping_disabled(self):
        output_x1 = PC4_login.ping(ip=Parameter.X2_IP)
        output_x2 = PC2_login.ping(ip=Parameter.X2_IP)
        Assertion.assert_equal(
            output_x1 and output_x2,
            False,
            "ERR: Check PPPoE unnumbered interface MGMT disabled via ping from WAN failed",
        )

    def test_05_verify_mgmt_https_disabled(self):
        curl_cmd = (
            'curl -o /dev/null -skL -w "%{http_code}\n" https://'
            + Parameter.X2_IP
            + " --connect-timeout 3"
        )
        curl_res_x1 = "200" in str(PC4_login.send_command(curl_cmd))
        curl_res_x2 = "200" in str(PC3_login.send_command(curl_cmd))
        Assertion.assert_equal(
            curl_res_x1 and curl_res_x2,
            False,
            "ERR: Check PPPoE unnumbered interface MGMT disabled via https from WAN failed",
        )

    def test_06_verify_mgmt_ssh_disabled(self):
        nc_cmd = f"ncat -i 1 {Parameter.X2_IP} 22"
        chk_kws = ["Connection refused", "Connection timed out"]
        nc_res_x1 = any(kw in PC4_login.send_command(nc_cmd) for kw in chk_kws)
        nc_res_x2 = any(kw in PC3_login.send_command(nc_cmd) for kw in chk_kws)
        Assertion.assert_equal(
            nc_res_x1 and nc_res_x2,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT disabled via ssh from WAN failed",
        )

    def test_07_verify_mgmt_snmp_disabled(self):
        user_name = snmp_user_dict["user_name"]
        snmp_cmd = f"snmpwalk -c public -u {user_name} {Parameter.X2_IP} -l noAuthNoPriv .1.3.6.1.2.1.1.1.0"
        snmp_res_x1 = "Timeout" in PC4_login.send_command(snmp_cmd)
        snmp_res_x2 = "Timeout" in PC3_login.send_command(snmp_cmd)
        Assertion.assert_equal(
            snmp_res_x1 and snmp_res_x2,
            True,
            "ERR: Check PPPoE unnumbered interface MGMT disabled via snmp from WAN failed",
        )


# Disconnect / Connect PPPoE
class Test_Operate_TC25(Test):
    uuid = "SOSAIOT-TC-57162"
    description = show_testcase_info(TESTPLAN, "25", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "25")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    @repeat_method(5)
    def test_04_verify_x1_pppoe_disconnect(self):
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

    @repeat_method(5)
    def test_05_verify_x1_pppoe_connect(self):
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


# Disable / Enable PPPoE Server
class Test_Operate_TC27(Test):
    uuid = "SOSAIOT-TC-57163"
    description = show_testcase_info(TESTPLAN, "27", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "27")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    def test_03_disable_pppoe_server(self):
        kill_cmd = "killall pppoe-server"
        kill_res = PC4_login.send_command(kill_cmd)
        Assertion.assert_equal(kill_res, "", "ERR: Disable PPPoE server failed.")

    def test_04_confirm_server_down(self):
        logger.info("Sleep 20s before step.")
        time.sleep(20)
        ps_cmd = "ps aux | grep pppoe-server"
        ps_res = PC4_login.send_command(ps_cmd)
        Assertion.assert_not_regular(
            ps_res, "pppoe-server -I", "ERR: Confirm PPPoE server down failed."
        )

    @repeat_method(5)
    def test_05_verify_x1_pppoe_down(self):
        logger.info("Sleep 10s before the next step.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        Assertion.assert_regular(
            str(resp),
            PPPoeParams.PPPOE_DOWN_IP,
            "Error: X1 should obtain same IP with 0.0.0.0",
        )

    @repeat_method(10)
    def test_06_enable_pppoe_server(self):
        res = []
        kill_cmd = "killall pppoe-server"
        kill_res = PC4_login.send_command(kill_cmd)
        logger.info("Sleep 30s before step.")
        time.sleep(30)
        pppoe_cmd = f"pppoe-server -I eth1 -L {PC4_ETH1_IP} -R {Parameter.X2_IP} -N 5"
        pppoe_res = PC4_login.send_command(pppoe_cmd)
        res.append(pppoe_res == "")
        logger.info("Sleep 30s before step.")
        time.sleep(30)
        output = PC3_login.ping(ip=PC4_ETH1_IP)
        res.append(output)
        logger.info(f"Enable PPPoE server results = {res}")
        Assertion.assert_equal(all(res), True, "ERR: Enable PPPoE server failed.")

    @repeat_method(20)
    def test_07_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()


# PPPoE > Static
class Test_Modify_Config_TC29(Test):
    uuid = "SOSAIOT-TC-57164"
    description = show_testcase_info(TESTPLAN, "29", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "29")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_04_config_x1_wan_static(self):
        res = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 static failed.")

    @repeat_method(5)
    def test_05_verify_x1_can_get_ip_static(self):
        logger.info("Sleep 10s before checking API response.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X1_IP, "Error: X1 should obtain same IP with X2."
        )

    def test_06_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()


# Static > PPPoE
class Test_Modify_Config_TC30(Test):
    uuid = "SOSAIOT-TC-57165"
    description = show_testcase_info(TESTPLAN, "30", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "30")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_wan_static(self):
        Test_Modify_Config_TC29().test_04_config_x1_wan_static()

    def test_03_verify_x1_can_get_ip_static(self):
        Test_Modify_Config_TC29().test_05_verify_x1_can_get_ip_static()

    def test_04_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_05_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_06_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()


# Change X2 IP
class Test_Modify_Config_TC32(Test):
    uuid = "SOSAIOT-TC-57166"
    description = show_testcase_info(TESTPLAN, "32", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "32")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_04_change_x2_ip(self):
        x2_lan_unnum_new_ip_dict = {
            "if": "x2",
            "zone": "LAN",
            "mode": "unnumbered",
            "ip": Parameter.X2_IP_NEW_1,
            "netmask": "255.255.255.0",
            "mgmt_https": True,
            "mgmt_ssh": True,
            "mgmt_ping": True,
            "user_https": True,
            "mgmt_snmp": True,
        }
        res = interfaceapi.config_interface(**x2_lan_unnum_new_ip_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failed.")

    @repeat_method(5)
    def test_05_verify_x1_can_get_new_ip_pppoe(self):
        logger.info("Sleep 10s before the next step.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X2_IP_NEW_1, "Error: X1 should obtain same IP with X2."
        )

    def test_06_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()


# Change X2 Subnet
class Test_Modify_Config_TC40(Test):
    uuid = "SOSAIOT-TC-57169"
    description = show_testcase_info(TESTPLAN, "40", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "40")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_04_confirm_nat_policies_pppoe_unnumber(self):
        nat_polis = natapi.get_nat_policy()
        res = chk_unnumber_nat_polis(nat_polis)
        Assertion.assert_equal(
            res, True, "ERR: Confirm NAT policies for unnumbered mode failed."
        )

    def test_05_change_x2_subnet(self):
        x2_lan_unnum_new_subnet_dict = {
            "if": "x2",
            "zone": "LAN",
            "mode": "unnumbered",
            "ip": Parameter.X2_IP_NEW_2,
            "netmask": Parameter.X2_NETMASK_NEW,
            "mgmt_https": True,
            "mgmt_ssh": True,
            "mgmt_ping": True,
            "user_https": True,
            "mgmt_snmp": True,
        }
        res = interfaceapi.config_interface(**x2_lan_unnum_new_subnet_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failed.")

    @repeat_method(5)
    def test_06_verify_x1_can_get_new_ip_pppoe(self):
        logger.info("Sleep 10s before the next step.")
        time.sleep(10)
        resp = interfaceapi.get_interface_address(name="X1")
        logger.info(f"Get X1 interface info = {resp}")
        x1_ip = resp.get("ip_address")
        Assertion.assert_equal(
            x1_ip, Parameter.X2_IP_NEW_2, "Error: X1 should obtain same IP with X2."
        )

    def test_07_confirm_nat_policies_updated_pppoe_unnumber(self):
        nat_polis = natapi.get_nat_policy()
        res = chk_unnumber_nat_polis(nat_polis)
        Assertion.assert_equal(
            res, True, "ERR: Confirm NAT policies for unnumbered mode failed."
        )

    def test_08_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()


# Reboot firewall
class Test_Reboot_TC71(Test):
    uuid = "SOSAIOT-TC-57176"
    description = show_testcase_info(TESTPLAN, "71", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "71")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    @repeat_method(20)
    def test_03_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_04_reboot_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Reboot DUT failed.")

    def test_05_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()


# Check TSR
class Test_TSR_TC72(Test):
    uuid = "SOSAIOT-TC-57177"
    description = show_testcase_info(TESTPLAN, "72", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "72")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    def test_03_verify_ports_settings_in_tsr(self):
        x1_info_list = [
            "WAN Mode: NAT with PPPOE Client  Value   : 4",
            "PPPOE configuration for IFace number            : 1",
            "PPPOE client status                             : Enabled",
            "PPPOE Unnumber Iface                            : 2",
            f"Unnumber IP address                             : {Parameter.X2_IP}",
            "User Name                                       : root",
            "Interface https Management                      : Yes",
            "Interface ssh Management                        : Yes",
            "Interface ping Management                       : Yes",
            "Interface snmp Management                       : Yes",
            "Interface https User Login                      : Yes",
        ]
        tsr_x1_info = diagapi.get_tsr_interface_part(lab1="X1", lab2="X2")
        chk_x1_res = chk_tsr_port_info(tsr_x1_info, x1_info_list)

        x2_info_list = [
            Parameter.X2_IP,
            "255.255.255.0",
            "Interface https Management                      : Yes",
            "Interface ssh Management                        : Yes",
            "Interface ping Management                       : Yes",
            "Interface snmp Management                       : Yes",
            "Interface https User Login                      : Yes",
        ]
        tsr_x2_info = diagapi.get_tsr_interface_part(lab1="X2", lab2="X3")
        chk_x2_res = chk_tsr_port_info(tsr_x2_info, x2_info_list)
        Assertion.assert_equal(
            chk_x1_res and chk_x2_res, True, "ERR: Confirm ports settings in TSR."
        )


# Export / Import configuration
class Test_EXP_TC73(Test):
    uuid = "SOSAIOT-TC-57178"
    description = show_testcase_info(TESTPLAN, "73", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "73")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_lan_unnumber_ip(self):
        Test_Config_TC06().test_01_config_x2_lan_unnumber_ip()

    def test_02_config_x1_pppoe_wan_with_unnumber(self):
        Test_Config_TC06().test_02_config_x1_pppoe_wan_with_unnumber()

    def test_03_export_pppoe_unnumber_exp(self):
        res = settingapi.export_setting_exp(CaseParams.exp_file_path)
        Assertion.assert_equal(res, True, "ERR: Export exp file failed.")

    def test_04_config_x1_wan_static(self):
        Test_Modify_Config_TC29().test_04_config_x1_wan_static()

    def test_05_verify_x1_can_get_ip_static(self):
        Test_Modify_Config_TC29().test_05_verify_x1_can_get_ip_static()

    def test_06_import_pppoe_exp(self):
        res = settingapi.import_setting_exp(CaseParams.exp_file_path)
        Assertion.assert_equal(res, True, "ERR: Import exp file failed.")

    @repeat_method(20)
    def test_07_verify_x1_can_get_ip_pppoe(self):
        Test_Config_TC06().test_03_verify_x1_can_get_ip_pppoe()

    def test_08_can_ping_wan_from_lan_pc(self):
        Test_Traffic_TC18().test_03_can_ping_wan_from_lan_pc()
