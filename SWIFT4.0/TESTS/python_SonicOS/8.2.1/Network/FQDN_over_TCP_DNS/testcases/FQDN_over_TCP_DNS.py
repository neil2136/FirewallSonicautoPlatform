from definition.settings import *
from definition.utils import *


class Test_DNS_TCP_Enable_TC01(Test):
    uuid = "SOSAIOT-TC-56051"
    description = show_testcase_info(TESTPLAN, "01", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "01")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_enable_dns_tcp(self):
        logger.info("Enable the DNS over TCP function.")
        upd_value = {"fqdn_over_tcp_dns": True}
        dns_settings = upd_dns_settings_payload(dns_settings_dict, **upd_value)
        res = dnssettingsapi.set_dns(**dns_settings)
        logger.info("Wait 60s for service up.")
        time.sleep(60)
        Assertion.assert_equal(res, True, "ERR: Failed to modify the DNS settings.")

    def test_02_verify_enable_status(self):
        logger.info("Verify the DNS over TCP function is enabled")
        dns_settings = dnssettingsapi.get_dns()
        res = confirm_dns_settings(dns_settings, '"fqdn_over_tcp_dns": true')
        Assertion.assert_equal(
            res, True, "ERR: Verify the DNS over TCP function status failed"
        )


class Test_DNS_TCP_Disable_TC02(Test):
    uuid = "SOSAIOT-TC-56052"
    description = show_testcase_info(TESTPLAN, "02", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "02")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_disable_dns_tcp(self):
        logger.info("Disable the DNS over TCP function.")
        upd_value = {"fqdn_over_tcp_dns": False}
        dns_settings = upd_dns_settings_payload(dns_settings_dict, **upd_value)
        res = dnssettingsapi.set_dns(**dns_settings)
        Assertion.assert_equal(res, True, "ERR: Failed to modify the DNS settings.")

    def test_02_verify_disable_status(self):
        logger.info("Verify the DNS over TCP function is disabled")
        dns_settings = dnssettingsapi.get_dns()
        res = confirm_dns_settings(dns_settings, '"fqdn_over_tcp_dns": false')
        Assertion.assert_equal(
            res, True, "ERR: Verify the DNS over TCP function status failed"
        )


class Test_DNS_TCP_Func_V4_TC03(Test):
    uuid = "SOSAIOT-TC-56053"
    description = show_testcase_info(TESTPLAN, "03", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "03")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_enable_dns_tcp(self):
        Test_DNS_TCP_Enable_TC01().test_01_enable_dns_tcp()

    def test_02_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()

    @repeat_method(7)
    def test_03_verify_dns_tcp_v4(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        resolve_ao_res = aoapi.resolve_ao_by_name(
            name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
        )
        logger.info(f"Resolve AO result: {resolve_ao_res}")
        req_filters = {
            "filter": [
                "DNS",
                "out:X1",
                "IP Type: TCP",
                f"Src=[{Parameter.X1_IP_V4}]",
                f"Dst=[{PC3_ETH2_IP}]",
                "Dst=[53]",
                "dnstcp",
            ],
        }
        res, _ = chk_cap_results(**req_filters)
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_Func_V4_TC05(Test):
    uuid = "SOSAIOT-TC-56055"
    description = show_testcase_info(TESTPLAN, "05", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "05")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()

    def test_02_verify_dns_tcp_v4(self):
        logger.info("Verify DNS over TCP")
        res, res_filters = False, {"filter_1": False, "filter_2": False}
        for i in range(7):
            logger.info(f"Check loop = {i+1}")
            _ = start_cap_pkts()
            resolve_ao_res_1 = aoapi.resolve_ao_by_name(
                name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
            )
            time.sleep(1)
            resolve_ao_res_2 = aoapi.resolve_ao_by_name(
                name=CaseParms.TEST_DNS_AO_NAME_2, version="fqdn"
            )
            logger.info(f"Resolve AO result: {[resolve_ao_res_1, resolve_ao_res_2]}")
            req_filters = {
                "filter_1": [
                    "DNS",
                    "out:X1",
                    "IP Type: TCP",
                    f"Src=[{Parameter.X1_IP_V4}]",
                    f"Dst=[{PC3_ETH2_IP}]",
                    "Dst=[53]",
                    "dnstcp",
                ],
                "filter_2": [
                    "DNS",
                    "out:X1",
                    "IP Type: TCP",
                    f"Src=[{Parameter.X1_IP_V4}]",
                    f"Dst=[{PC3_ETH2_IP}]",
                    "Dst=[53]",
                    "tcpdns",
                ],
            }
            _, details = chk_cap_results(wait_time=60, **req_filters)
            upd_res = {filter: result for filter, result in details.items() if result}
            if upd_res:
                res_filters.update(upd_res)
            res = all(res_filters.values())
            logger.info(f"Check DNS packets result = {res}")
            if res:
                break
            if i < 6:
                logger.info("Sleep 15s before the next retry")
                time.sleep(15)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_Verify_Logs_TC09(Test):
    uuid = "SOSAIOT-TC-56059"
    description = show_testcase_info(TESTPLAN, "09", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "09")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    @repeat_method(7)
    def test_01_verify_dns_logs(self):
        logger.info("Verify DNS over TCP logs")
        cls_res = logapi.clear_log()
        logger.info(f"Clear log result: {cls_res}")
        time.sleep(10)
        resolve_ao_res = aoapi.resolve_ao_by_name(
            name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
        )
        logger.info(f"Resolve AO result: {resolve_ao_res}")
        logger.info("Sleep 30s before checking logs.")
        time.sleep(30)
        logs = logapi.get_log(id=1535)
        logger.info(f"Get target logs = {logs}")
        log_res = f"Truncated flag is set:domain {CaseParms.TEST_DOMAIN_1}" in str(logs)
        logger.info(f"Check DNS over TCP logs result: {log_res}")
        check_case_result(log_res)
        Assertion.assert_equal(log_res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_Verify_TSR_TC11(Test):
    uuid = "SOSAIOT-TC-56060"
    description = show_testcase_info(TESTPLAN, "11", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "11")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_02_verify_dns_settings_tsr(self):
        logger.info("Verify DNS over TCP settings in TSR")
        tsr_dns_info = diagapi.get_tsr_part("Network", lab1="DNS")
        logger.info(f"Get DNS info in TSR = {tsr_dns_info}")
        chk_dns_res = re.search(r"Enable FQDN over TCP DNS:\s*1", tsr_dns_info)
        Assertion.assert_equal(
            bool(chk_dns_res), True, "ERR: Verify DNS settings in TSR."
        )


class Test_DNS_TCP_ACL_TC20(Test):
    uuid = "SOSAIOT-TC-56066"
    description = show_testcase_info(TESTPLAN, "20", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "20")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_add_acl_lan_wan_deny(self):
        res = accessruleapi.add_ipv4_access_rule(**deny_lan_to_wan_dict)
        Assertion.assert_equal(
            res, True, "ERR: Add deny access rule from LAN to WAN failed"
        )

    @repeat_method(7)
    def test_02_ping_from_lan(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        cmd = f"ping -c 5 {CaseParms.TEST_DOMAIN_1}"
        out = PC2_login.send_command(cmd)
        pingres = True if "ttl=" in out else False
        logger.info(f"Ping result: {pingres}")
        req_filters = {
            "filter": [
                "DNS",
                "out:X1",
                "IP Type: TCP",
                f"Src=[{Parameter.X1_IP_V4}]",
                f"Dst=[{PC3_ETH2_IP}]",
                "Dst=[53]",
                "dnstcp",
            ],
        }
        reqres, _ = chk_cap_results(**req_filters)
        res = not pingres and not reqres
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")

    def test_03_clean_acl(self):
        res = accessruleapi.del_ipv4_access_rule(deny_lan_to_wan_dict["name"])
        Assertion.assert_equal(
            res, True, "ERR: Delete access rule from LAN to WAN failed"
        )


class Test_DNS_TCP_Proxy_TC17(Test):
    uuid = "SOSAIOT-TC-56065"
    description = show_testcase_info(TESTPLAN, "17", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "17")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_set_dns_proxy(self):
        logger.info("Enable the DNS proxy settings")
        res = dnsproxyapi.config_dnsproxy(**dns_proxy_settings_dict)
        Assertion.assert_equal(
            res, True, "ERR: Failed to modify the DNS proxy settings."
        )

    def test_02_confirm_dns_proxy(self):
        logger.info("Confirm the DNS proxy settings")
        resp = dnsproxyapi.get_dnsproxy()
        res = {"enable": True, **resp["dns_proxy"]} == dns_proxy_settings_dict
        Assertion.assert_equal(
            res, True, "ERR: Failed to modify the DNS proxy settings."
        )

    @repeat_method(7)
    def test_03_verify_dns_tcp_v4(self):
        Test_DNS_TCP_Func_V4_TC03().test_03_verify_dns_tcp_v4()


class Test_DNS_TCP_Multi_TC07(Test):
    uuid = "SOSAIOT-TC-56057"
    description = show_testcase_info(TESTPLAN, "07", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "07")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    @repeat_method(7)
    def test_01_verify_dns_tcp(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        res_query = send_dns_query_via_lan(
            PC2_login,
            PC3_ETH2_IP,
            CaseParms.TEST_DOMAIN_1,
            opt="query",
        )
        logger.info(f"Send DNS query result: {res_query}")
        req_filters = {
            "filter": [
                "DNS",
                "out:X1",
                "IP Type: TCP",
                f"Src=[{Parameter.X1_IP_V4}]",
                f"Dst=[{PC3_ETH2_IP}]",
                "Dst=[53]",
                "dnstcp",
            ],
        }
        res, _ = chk_cap_results(**req_filters)
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_Multi_TC08(Test):
    uuid = "SOSAIOT-TC-56058"
    description = show_testcase_info(TESTPLAN, "08", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "08")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_stop_dns_service(self):
        cmds = [
            "systemctl stop dnsmasq",
            "systemctl status dnsmasq",
        ]
        output = PC3_login.send_commands(cmds)
        Assertion.assert_regular(
            output, "dead", "ERR: Config dns server in WAN PC failed"
        )

    @repeat_method(7)
    def test_02_verify_dns_tcp(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        res_query = send_dns_query_via_lan(
            PC3_login,
            Parameter.X1_IP_V4,
            CaseParms.TEST_DOMAIN_1,
            port=11066,
            opt="answer",
        )
        logger.info(f"Send DNS query result: {res_query}")
        req_filters = {
            "filter": [
                "DNS",
                "in:X1",
                "IP Type: UDP",
                f"Src=[{PC3_ETH2_IP}]",
                f"Dst=[{Parameter.X1_IP_V4}]",
                "Src=[53]",
                "DROPPED",
            ],
        }
        res, _ = chk_cap_results(**req_filters)
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")

    def test_03_restart_dns_service(self):
        cmds = [
            "systemctl restart dnsmasq",
            "systemctl status dnsmasq",
        ]
        output = PC3_login.send_commands(cmds)
        Assertion.assert_regular(
            output, "running", "ERR: Config dns server in WAN PC failed"
        )


class Test_DNS_TCP_Split_TC15(Test):
    uuid = "SOSAIOT-TC-56064"
    description = show_testcase_info(TESTPLAN, "15", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "15")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_set_split_dns(self):
        res = dnssettingsapi.add_split_dns(**dns_split_settings_dict)
        Assertion.assert_equal(res, True, "ERR: Failed to add the split DNS entry.")

    def test_02_modify_dns_settings(self):
        logger.info("Modify the DNS settings")
        dns_settings = copy.deepcopy(dns_settings_dict)
        dns_settings["dns"]["server"]["static"]["primary"] = Parameter.X1_DNS2
        res = dnssettingsapi.set_dns(**dns_settings)
        Assertion.assert_equal(res, True, "ERR: Failed to modify the DNS settings.")

    @repeat_method(7)
    def test_03_verify_dns_tcp_split(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        resolve_ao_res = aoapi.resolve_ao_by_name(
            name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
        )
        logger.info(f"Resolve AO result: {resolve_ao_res}")
        req_filters = {
            "filter": [
                "DNS",
                "out:X1",
                "IP Type: TCP",
                f"Src=[{Parameter.X1_IP_V4}]",
                f"Dst=[{Parameter.X1_DNS2}]",
                "Dst=[53]",
                "dnstcp",
            ],
        }
        res, _ = chk_cap_results(**req_filters)
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")

    def test_04_clean_split_dns_settings(self):
        res_split = dnssettingsapi.delete_split_dns(
            domain=dns_split_settings_dict["domain"]
        )
        Assertion.assert_equal(res_split, True, "ERR: Delete split DNS entry failed.")

    def test_05_clean_dns_proxy_settings(self):
        logger.info("Disable the DNS proxy settings")
        upd_value = {"enable": False, "enforce_all_dns_requests": False}
        dns_settings = upd_dns_settings_payload(dns_proxy_settings_dict, **upd_value)
        res = dnsproxyapi.config_dnsproxy(**dns_settings)
        Assertion.assert_equal(
            res, True, "ERR: Failed to modify the DNS proxy settings."
        )


class Test_DNS_TCP_Func_V6_TC04(Test):
    uuid = "SOSAIOT-TC-56054"
    description = show_testcase_info(TESTPLAN, "04", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "04")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_set_dns_prefer_v6(self):
        logger.info("Set to prefer the IPv6 DNS.")
        upd_value = {"preferred": True}
        dns_settings = upd_dns_settings_payload(dns_settings_dict, **upd_value)
        res = dnssettingsapi.set_dns(**dns_settings)
        Assertion.assert_equal(res, True, "ERR: Failed to modify the DNS settings.")

    @repeat_method(7)
    def test_02_verify_dns_tcp_v6(self):
        logger.info("Verify DNS over TCP")
        _ = start_cap_pkts()
        resolve_ao_res = aoapi.resolve_ao_by_name(
            name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
        )
        logger.info(f"Resolve AO result: {resolve_ao_res}")
        req_filters = {
            "filter": [
                "DNS",
                "out:X1",
                "Ether Type: IPV6",
                "Next header: TCP",
                f"Src=[{Parameter.X1_IP_V6}]",
                f"Dst=[{PC3_ETH2_IP_V6}]",
                "Dst=[53]",
                "dnstcp",
            ],
        }
        res, _ = chk_cap_results(**req_filters)
        check_case_result(res)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_Func_V6_TC06(Test):
    uuid = "SOSAIOT-TC-56056"
    description = show_testcase_info(TESTPLAN, "06", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "06")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_verify_dns_tcp_v6(self):
        logger.info("Verify DNS over TCP")
        res, res_filters = False, {"filter_1": False, "filter_2": False}
        for i in range(7):
            logger.info(f"Check loop = {i+1}")
            _ = start_cap_pkts()
            resolve_ao_res_1 = aoapi.resolve_ao_by_name(
                name=CaseParms.TEST_DNS_AO_NAME_1, version="fqdn"
            )
            time.sleep(1)
            resolve_ao_res_2 = aoapi.resolve_ao_by_name(
                name=CaseParms.TEST_DNS_AO_NAME_2, version="fqdn"
            )
            logger.info(f"Resolve AO result: {[resolve_ao_res_1, resolve_ao_res_2]}")
            req_filters = {
                "filter_1": [
                    "DNS",
                    "out:X1",
                    "Ether Type: IPV6",
                    "Next header: TCP",
                    f"Src=[{Parameter.X1_IP_V6}]",
                    f"Dst=[{PC3_ETH2_IP_V6}]",
                    "Dst=[53]",
                    "dnstcp",
                ],
                "filter_2": [
                    "DNS",
                    "out:X1",
                    "Ether Type: IPV6",
                    "Next header: TCP",
                    f"Src=[{Parameter.X1_IP_V6}]",
                    f"Dst=[{PC3_ETH2_IP_V6}]",
                    "Dst=[53]",
                    "tcpdns",
                ],
            }
            _, details = chk_cap_results(wait_time=60, **req_filters)
            upd_res = {filter: result for filter, result in details.items() if result}
            if upd_res:
                res_filters.update(upd_res)
            res = all(res_filters.values())
            logger.info(f"Check DNS packets result = {res}")
            if res:
                break
            if i < 6:
                logger.info("Sleep 15s before the next retry")
                time.sleep(15)
        Assertion.assert_equal(res, True, "ERR: Verify DNS over TCP failed.")


class Test_DNS_TCP_CLI_Set_TC12(Test):
    uuid = "SOSAIOT-TC-56061"
    description = show_testcase_info(TESTPLAN, "12", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "12")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_disable_dns_tcp(self):
        Test_DNS_TCP_Disable_TC02().test_01_disable_dns_tcp()

    def test_02_verify_disable_status(self):
        Test_DNS_TCP_Disable_TC02().test_02_verify_disable_status()

    def test_03_cli_set_dns(self):
        logger.info("Enable DNS over TCP via CLI")
        dns_settings = {"dns fqdn-over-tcp-dns": True}
        res = dnscli.dns_setting(**dns_settings)
        Assertion.assert_equal(
            res, True, "ERR: Failed to modify the DNS settings via CLI."
        )

    def test_04_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()


class Test_DNS_TCP_Reboot_TC13(Test):
    uuid = "SOSAIOT-TC-56062"
    description = show_testcase_info(TESTPLAN, "13", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "13")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_enable_dns_tcp(self):
        Test_DNS_TCP_Enable_TC01().test_01_enable_dns_tcp()

    def test_02_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()

    def test_03_reboot_dut(self):
        logger.info("Will reboot the DUT")
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Reboot DUT failed.")

    @repeat_method(6)
    def test_04_verify_dns_tcp_v4(self):
        Test_DNS_TCP_Func_V4_TC03().test_03_verify_dns_tcp_v4()


class Test_DNS_TCP_Import_EXP_TC14(Test):
    uuid = "SOSAIOT-TC-56063"
    description = show_testcase_info(TESTPLAN, "14", description=True)["title"]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "14")
        Assertion.assert_equal(True, True, "ERR: Show testcase info failed")

    def test_01_enable_dns_tcp(self):
        Test_DNS_TCP_Enable_TC01().test_01_enable_dns_tcp()

    def test_02_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()

    def test_03_export_dns_settings(self):
        res = settingapi.export_setting_exp(CaseParms.EXP_FILE_PATH)
        Assertion.assert_equal(res, True, "ERR: Export exp file failed.")

    def test_04_disable_dns_tcp(self):
        Test_DNS_TCP_Disable_TC02().test_01_disable_dns_tcp()

    def test_05_verify_disable_status(self):
        Test_DNS_TCP_Disable_TC02().test_02_verify_disable_status()

    def test_06_import_exp(self):
        res = settingapi.import_setting_exp(CaseParms.EXP_FILE_PATH)
        Assertion.assert_equal(res, True, "ERR: Import exp file failed.")

    def test_07_verify_enable_status(self):
        Test_DNS_TCP_Enable_TC01().test_02_verify_enable_status()
