from definition.settings import *
from definition.utils import *


# Expected: Verify duplicate and invalid domain cannot be added
class TestError_1521003(Test):
    uuid = "SOSAIOT-TC-51540"
    description = show_testcase_info(TESTPLAN, '1521003', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521003')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_a_custom_domain(self):
        rc = dnsSec_api.add_dns_custom_domain(**custom_domain_dict)
        Assertion.assert_equal(rc, True, "ERR: add dns filtering custom domain failed!!")

    def test_02_add_the_duplicate_custom_domain(self):
        rc = ''
        res = dnsSec_api.add_dns_custom_domain(msg=True, **custom_domain_dict)
        if not res[0]:
            rc = json.dumps(res[1])
        Assertion.assert_regular(rc, 'Already exists', "ERR: add_the_duplicate_custom_domain should fail!!")

    def test_03_add_the_invalid_custom_domain(self):
        rc = ''
        invalid = copy.deepcopy(custom_domain_dict)
        invalid["dns_security"]["dns_filtering"]["custom_domain"][0]["domain"] = "!@#.222"
        res = dnsSec_api.add_dns_custom_domain(msg=True, **invalid)
        if not res[0]:
            rc = json.dumps(res[1])
        Assertion.assert_regular(rc, 'Invalid domain', "ERR: add_the_invalid_custom_domain should fail!!")


# Expected: Verify the domain with wildcard is supported
class TestFunc_1521018(Test):
    uuid = "SOSAIOT-TC-51554"
    description = show_testcase_info(TESTPLAN, '1521018', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521018')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_dns_is_negative_reply(self):
        res_init = initial_packet_monitor()
        logger.info(f'initial_packet_monitor result... {res_init}')
        rc = False
        out = check_dns_query_no_error(CParam.www_Domain)
        if out:
            cmd = f'dns.qry.name=={CParam.www_Domain} and ip.src=={Parameter.Filtering_server} and ip.dst=={Parameter.X1_IP}'
            target = ('handle DNS dropped the pkt', 'cf02', 'No error')
            rc_server = check_dns_packets_in_tShark(cmd, target)
            logger.info(f'Check Server replied packet result...... {rc_server}')
            cmd = f'dns.qry.name=={CParam.www_Domain} and ip.src=={Parameter.FIREWALL} and ip.dst=={PC1_ETH0_IP}'
            target = ('Server failure', 'Generated')
            rc_client = check_dns_packets_in_tShark(cmd, target)
            logger.info(f'Check packet to client result...... {rc_client}')
            rc = rc_server & rc_client
        Assertion.assert_equal(rc, True, "ERR: failed to check_dns_is_negative_reply!!")


# Expected: Verify edit the category in custom domain list
class TestSettings_1521004(Test):
    uuid = "SOSAIOT-TC-51541"
    description = show_testcase_info(TESTPLAN, '1521004', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521004')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_edit_the_custom_domain_category(self):
        name = custom_domain_dict["dns_security"]["dns_filtering"]["custom_domain"][0]["domain"]
        rc = dnsSec_api.edit_dns_custom_domain(domain=name, **{'category': '8. Social'})
        Assertion.assert_equal(rc, True, "ERR: edit dns filtering custom domain category failed!!")


# Expected: Verify the domain in custom domain list can not be edited
class TestError_1521005(Test):
    uuid = "SOSAIOT-TC-51542"
    description = show_testcase_info(TESTPLAN, '1521005', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521005')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_edit_the_custom_domain_name(self):
        name = custom_domain_dict["dns_security"]["dns_filtering"]["custom_domain"][0]["domain"]
        res = dnsSec_api.edit_dns_custom_domain(domain=name, **{'new-name': 'adult.com'})
        logger.info(f'Edit the custom domain name ...... {res}')
        out = dnsSec_api.show_dns_custom_domain()
        rc = 'adult.com' not in json.dumps(out) if out else False
        Assertion.assert_equal(rc, True, "ERR: The_custom_domain_name is not editable!!")


# Expected: Verify delete a custom domain entry
class TestSettings_1521006(Test):
    uuid = "SOSAIOT-TC-51543"
    description = show_testcase_info(TESTPLAN, '1521006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_delete_one_custom_domain(self):
        name = custom_domain_dict["dns_security"]["dns_filtering"]["custom_domain"][0]["domain"]
        rc = dnsSec_api.del_custom_domain(domainname=name)
        Assertion.assert_equal(rc, True, "ERR: delete one dns filtering custom domain failed!!")


# Expected: Verify custom domains in TSR shows correctly
class TestSettings_1521009(Test):
    uuid = "SOSAIOT-TC-51545"
    description = show_testcase_info(TESTPLAN, '1521009', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521009')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_multiple_custom_domain(self):
        multi = copy.deepcopy(custom_domain_dict)
        multi["dns_security"]["dns_filtering"]["custom_domain"][:] = []
        for domain in domain_name_list:
            multi["dns_security"]["dns_filtering"]["custom_domain"].append({"domain": domain, "category": "1. Adult"})
        rc = dnsSec_api.add_dns_custom_domain(**multi)
        Assertion.assert_equal(rc, True, "ERR: add_multiple_custom_domain failed!!")

    def test_02_check_tsr(self):
        rc = False
        tsr = diag_api.get_tsr_part2(func="Network : DNS Security")
        for domain in domain_name_list:
            rc = f"Domain: {domain}, Category: 1" in tsr if tsr else False
            if not rc:
                logger.error(f"Domain <{domain}> is not in tsr!! or TSR is null!!")
                break
        Assertion.assert_equal(rc, True, "ERR: check_tsr failed!!")


# Expected: Verify delete multiple custom domain entries
class TestSettings_1521007(Test):
    uuid = "SOSAIOT-TC-51544"
    description = show_testcase_info(TESTPLAN, '1521007', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521007')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_delete_multiple_custom_domain(self):
        rc = dnsSec_api.delete_multiple_custom_domain(domain_list=domain_name_list)
        Assertion.assert_equal(rc, True, "ERR: delete_multiple_custom_domain failed!!")


# Expected: Verify the CLI commands to add a custom domain
class TestSettings_1521010(Test):
    uuid = "SOSAIOT-TC-51546"
    description = show_testcase_info(TESTPLAN, '1521010', description=True)['title']
    jira = 'GEN7-46189'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521010')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_add_a_custom_domain(self):
        rc = dns_cli.add_edit_filtering_custom_domain(domain=CParam.test_Domain, category=CParam.Category)
        Assertion.assert_equal(rc, True, "ERR: cli_add_a_custom_domain failed!!")


# Expected: Verify the CLI commands to edit a custom domain
class TestSettings_1521011(Test):
    uuid = "SOSAIOT-TC-51547"
    description = show_testcase_info(TESTPLAN, '1521011', description=True)['title']
    jira = 'GEN7-46189'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521011')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_edit_a_custom_domain(self):
        rc = dns_cli.add_edit_filtering_custom_domain(domain=CParam.test_Domain, category="2. Gaming")
        Assertion.assert_equal(rc, True, "ERR: cli_edit_a_custom_domain failed!!")


# Expected: Verify the CLI commands to delete a custom domain
class TestSettings_1521012(Test):
    uuid = "SOSAIOT-TC-51548"
    description = show_testcase_info(TESTPLAN, '1521012', description=True)['title']
    jira = 'GEN7-46189'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521012')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_delete_a_custom_domain(self):
        rc = dns_cli.del_filtering_custom_domain(domain=CParam.test_Domain)
        Assertion.assert_equal(rc, True, "ERR: cli_delete_a_custom_domain failed!!")


# Expected: Verify the CLI commands to show all custom domains
class TestSettings_1521014(Test):
    uuid = "SOSAIOT-TC-51550"
    description = show_testcase_info(TESTPLAN, '1521014', description=True)['title']
    jira = 'GEN7-46189'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521014')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_add_custom_domains(self):
        rc = False
        for domain in domain_name_list:
            rc = dns_cli.add_edit_filtering_custom_domain(domain=domain, category=CParam.Category)
            if not rc:
                logger.error(f"CLI Add Domain <{domain}> failed!!")
                break
        Assertion.assert_equal(rc, True, "ERR: cli_add_custom_domains failed!!")

    def test_02_cli_show_custom_domain(self):
        out = dns_cli.show_filtering_custom_domain()
        rc = 'adult.com' in str(out) if out else False
        Assertion.assert_equal(rc, True, "ERR: cli_show_one_custom_domain failed!!")

    def test_03_cli_show_custom_domains(self):
        rc = False
        out = dns_cli.show_filtering_custom_domain()
        for domain in domain_name_list:
            rc = domain in str(out) if out else False
            if not rc:
                logger.error(f"Show Domain <{domain}> failed!! or Show null!!")
                break
        Assertion.assert_equal(rc, True, "ERR: cli_show_all_custom_domains failed!!")


# Expected: Verify the CLI commands to delete all custom domains
class TestSettings_1521013(Test):
    uuid = "SOSAIOT-TC-51549"
    description = show_testcase_info(TESTPLAN, '1521013', description=True)['title']
    jira = 'GEN7-46189'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521013')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_delete_all_custom_domain(self):
        rc = dns_cli.del_filtering_custom_domain()
        Assertion.assert_equal(rc, True, "ERR: cli_delete_all_custom_domain failed!!")


# Expected: Verify the Forged IPv4 is configurable
class TestSettings_1521039(Test):
    uuid = "SOSAIOT-TC-51555"
    description = show_testcase_info(TESTPLAN, '1521039', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521039')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_forged_ip_ipv4(self):
        rc = dnsFilter_api.config_forged_ip(ipv4=CParam.Forged_IPv4)
        Assertion.assert_equal(rc, True, "ERR: config_forged_ip_ipv4 failed!!")


# Expected: Verify the Forged IPv6 is configurable
class TestSettings_1521040(Test):
    uuid = "SOSAIOT-TC-51556"
    description = show_testcase_info(TESTPLAN, '1521040', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521040')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_forged_ip_ipv6(self):
        rc = dnsFilter_api.config_forged_ip(ipv6=CParam.Forged_IPv6)
        Assertion.assert_equal(rc, True, "ERR: config_forged_ip_ipv6 failed!!")


# Expected: Verify when a wrong IPv4/IPv6 address is entered, the error message throws
class TestError_1521041(Test):
    uuid = "SOSAIOT-TC-51557"
    description = show_testcase_info(TESTPLAN, '1521041', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521041')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_invalid_forged_ip_ipv4(self):
        rc = False
        for ipv4 in ['10', '10.1', '10.1.1', '10.1.1.256']:
            res, msg = dnsFilter_api.config_forged_ip(msg=True, ipv4=ipv4)
            rc = "property 'ipv4': invalid format" in json.dumps(
                msg) or "Invalid IP" in json.dumps(msg) if not res else False
            if not rc:
                logger.error(f'<{ipv4}> is invalid ipv4 address!!')
                break
        Assertion.assert_equal(rc, True, "ERR: config_invalid_forged_ip_ipv4 should fail!!")

    def test_02_config_invalid_forged_ip_ipv6(self):
        rc = False
        for ipv6 in ['10', '1001:1', '1001::g']:
            res, msg = dnsFilter_api.config_forged_ip(msg=True, ipv6=ipv6)
            rc = "property 'ipv6': invalid format" in json.dumps(msg) if not res else False
            if not rc:
                logger.error(f'<{ipv6}> is invalid ipv6 address!!')
                break
        Assertion.assert_equal(rc, True, "ERR: config_invalid_forged_ip_ipv6 should fail!!")


# Expected: Verify the CLI command to modify valid Forged IPv4 work
class TestSettings_1521044(Test):
    uuid = "SOSAIOT-TC-51559"
    description = show_testcase_info(TESTPLAN, '1521044', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521044')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_config_forged_ip_ipv4(self):
        rc = dnsFilter_cli.config_dns_filtering_base(**{'forged-ip': f'{CParam.Forged_IPv4} ::1'})
        Assertion.assert_equal(rc, True, "ERR: cli_config_forged_ip_ipv4 failed!!")


# Expected: Verify when the wrong IPv4/IPv6 address is entered, the CLI command to modify Forged IP fail
class TestError_1521046(Test):
    uuid = "SOSAIOT-TC-51561"
    description = show_testcase_info(TESTPLAN, '1521046', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_config_invalid_forged_ip_ipv4(self):
        rc = False
        for ipv4 in ['10', '10.1', '10.1.1', '10.1.1.256']:
            out = dnsFilter_cli.config_dns_filtering_base(tag=1, **{'forged-ip': f'{ipv4} ::1'})
            rc = 'Invalid input detected' in out[1] or "Invalid IP" in out[1] if out and not out[0] else False
            if not rc:
                logger.error(f'<{ipv4}> is invalid ipv4 address!!')
                break
        Assertion.assert_equal(rc, True, "ERR: cli_config_invalid_forged_ip_ipv4 should fail!!")

    def test_02_cli_config_invalid_forged_ip_ipv6(self):
        rc = False
        for ipv6 in ['10', '1001:1', '1001::g']:
            out = dnsFilter_cli.config_dns_filtering_base(tag=1, **{'forged-ip': f'127.0.0.1 {ipv6}'})
            rc = 'Invalid input detected' in out[1] if out and not out[0] else False
            if not rc:
                logger.error(f'<{ipv6}> is invalid ipv6 address!!')
                break
        Assertion.assert_equal(rc, True, "ERR: cli_config_invalid_forged_ip_ipv6 should fail!!")


# Expected: Verify the CLI command to show DNS Filtering global configure work
class TestSettings_1521047(Test):
    uuid = "SOSAIOT-TC-51562"
    description = show_testcase_info(TESTPLAN, '1521047', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521047')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_cli_config_forged_ips(self):
        rc = dnsFilter_cli.config_dns_filtering_base(**{'forged-ip': '10.0.0.100 1001::100'})
        Assertion.assert_equal(rc, True, "ERR: cli_config_forged_ips failed!!")

    def test_02_cli_show_forged_ips(self):
        out = dnsFilter_cli.show_filtering_base()
        rc = 'forged-ip 10.0.0.100 1001::100' in str(out) if out else False
        Assertion.assert_equal(rc, True, "ERR: cli_show_forged_ips failed!!")


# Expected: When White List is enabled, the action of the domain in White List will not be enforced and log shows.
class TestFunc_1521179(Test):
    uuid = "SOSAIOT-TC-51571"
    description = show_testcase_info(TESTPLAN, '1521179', description=True)['title']
    actions_str = '{"2":2}'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521179')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_packet_allow_log(self):
        rc = logCate_api.edit_log_category_groups_by_id(id='107', **log_group_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_packet_allow_log failed!!")

    def test_02_add_filtering_profile(self):
        rc = dnsFilter_api.config_dns_filtering_profile(**profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_filtering_profile failed!!")

    def test_03_add_dns_policy(self):
        dns_rule_dict["dns_policies"][0]["name"] = "Gaming_Negative"
        dns_rule_dict["dns_policies"][0]["action"]["filter_profile"] = "Gaming_Negative"
        rc = dnsRule_api.add_dns_rule(**dns_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_04_set_forged_ip(self):
        rc = dnsFilter_api.config_forged_ip(ipv4=CParam.Forged_IPv4, ipv6=CParam.Forged_IPv6)
        Assertion.assert_equal(rc, True, "ERR: set_forged_ip failed!!")

    def test_05_add_white_list_domain(self):
        rc = dnsFilter_api.add_dns_whitelist(name=CParam.www_Domain)
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domain failed!!")

    def test_06_check_the_action_not_enforced(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Change dns filtering profile...... {clear_res}')
        init_res = initial_packet_monitor()
        logger.info(f'initial_packet_monitor result... {init_res}')
        rc_pkt = False
        out = check_dns_query_no_error(CParam.www_Domain)
        if out:
            cmd = f'dns.qry.name=={CParam.www_Domain} and ip.src=={Parameter.FIREWALL} and ip.dst=={PC1_ETH0_IP}'
            target = ('No error', 'Forwarded')
            rc_pkt = check_dns_packets_in_tShark(cmd, target)
            logger.info(f'check_dns_packets_in_tShark... {rc_pkt}')
        rc_log = check_related_logs(target="DNS Packet Bypassed via Whitelist")
        logger.info(f'check_related_logs... {rc_log}')
        Assertion.assert_equal(rc_pkt & rc_log, True, "ERR: check_the_action_not_enforced failed!!")

    def test_07_change_filtering_profile_block_and_check(self):
        profile_dict["dns_security"]["dns_filtering"]["profile"][0]["actions"] = self.actions_str
        change_res = dnsFilter_api.config_dns_filtering_profile(**profile_dict)
        logger.info(f'Change dns filtering profile...... {change_res}')
        self.test_06_check_the_action_not_enforced()

    def test_08_change_filtering_profile_forged_and_check(self):
        self.actions_str = '{"2":3}'
        self.test_07_change_filtering_profile_block_and_check()


# Expected: When White List is enabled, the action of the domain removed from White List will be enforced
class TestFunc_1521180(Test):
    uuid = "SOSAIOT-TC-51572"
    description = show_testcase_info(TESTPLAN, '1521180', description=True)['title']
    actions_str = '{"2":2}'
    pkt_target = ('Server failure', 'Generated')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521180')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_remove_white_list_domain(self):
        rc = dnsFilter_api.del_dns_whitelist(name_list=CParam.www_Domain.split())
        Assertion.assert_equal(rc, True, "ERR: remove_white_list_domain failed!!")

    def test_02_check_the_action_enforced_block(self):
        profile_dict["dns_security"]["dns_filtering"]["profile"][0]["actions"] = '{"2":1}'
        change_res = dnsFilter_api.config_dns_filtering_profile(**profile_dict)
        logger.info(f'Change dns filtering profile...... {change_res}')
        res_init = initial_packet_monitor()
        logger.info(f'initial_packet_monitor result... {res_init}')
        rc = False
        out = check_dns_query_no_error(CParam.www_Domain)
        if not out:
            cmd = f'dns.qry.name=={CParam.www_Domain} and ip.src=={Parameter.Filtering_server} and ip.dst=={Parameter.X1_IP}'
            rc = check_dns_packets_in_tShark(cmd, target='handle DNS dropped the pkt')
        Assertion.assert_equal(rc, True, "ERR: check_the_action_enforced_block failed!!")

    def test_03_check_the_action_enforced_negative_reply(self):
        profile_dict["dns_security"]["dns_filtering"]["profile"][0]["actions"] = self.actions_str
        change_res = dnsFilter_api.config_dns_filtering_profile(**profile_dict)
        logger.info(f'Change dns filtering profile...... {change_res}')
        res_init = initial_packet_monitor()
        logger.info(f'initial_packet_monitor result... {res_init}')
        rc = False
        out = check_dns_query_no_error(CParam.www_Domain)
        if out:
            cmd = f'dns.qry.name=={CParam.www_Domain} and ip.src=={Parameter.FIREWALL} and ip.dst=={PC1_ETH0_IP}'
            rc = check_dns_packets_in_tShark(cmd, self.pkt_target)
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domain failed!!")

    def test_04_check_the_action_enforced_forged(self):
        self.actions_str = '{"2":3}'
        self.pkt_target = ((CParam.Forged_IPv4, 'Generated'))
        self.test_03_check_the_action_enforced_negative_reply()


# Expected: When White List is disabled, the action of the domain in White List will be enforced
class TestFunc_1521181(Test):
    uuid = "SOSAIOT-TC-51573"
    description = show_testcase_info(TESTPLAN, '1521181', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521181')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_white_list(self):
        rc = dnsFilter_api.add_dns_whitelist(name=CParam.www_Domain)
        Assertion.assert_equal(rc, True, "ERR: add_white_list_domain failed!!")

    def test_02_disable_dns_filtering_whitelist(self):
        # disable = {"dns_security":{"dns_filtering":{"use_whitelist":False,"forged_ip":{"ipv4":"192.168.100.100","ipv6":"::1"}}}}
        disable = {"dns_security": {"dns_filtering": {"use_whitelist": False}}}
        rc = dnsFilter_api.config_whitelist(**disable)
        Assertion.assert_equal(rc, True, "ERR: disable_dns_filtering_whitelist failed!!")

    def test_03_check_the_action_enforced_block(self):
        TestFunc_1521180().test_02_check_the_action_enforced_block()

    def test_04_check_the_action_enforced_negative_reply(self):
        TestFunc_1521180().test_03_check_the_action_enforced_negative_reply()

    def test_05_check_the_action_enforced_forged(self):
        TestFunc_1521180().test_04_check_the_action_enforced_forged()
