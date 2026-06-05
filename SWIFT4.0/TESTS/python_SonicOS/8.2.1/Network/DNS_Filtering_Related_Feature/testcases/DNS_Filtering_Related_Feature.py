from definition.settings import *
from definition.utils import *


class Test_licensed(Test):
    uuid = "SOSAIOT-TC-51422"
    # uuid = '6833B9C8-8641-11EB-826C-45364435BA2B'
    description = show_testcase_info(TESTPLAN, '1521187', description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521187')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(6)
    def test_01_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_02_add_dns_filter_profile(self):
        rc = dnsFil_api.add_dns_filtering_profile(**add_profile_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_filter_rule failed")

    def test_03_add_dns_filter_rule(self):
        rc_api = dnsRule_api.add_dns_rule(**filter_rule_dict)
        logger.info(f"Add dns filter policy by API...... {rc_api}")
        rc_cli = dnsPolicy_cli.add_dns_policy(**filter_policy_cli_dict)
        logger.info(f"Add dns filter policy by CLI...... {rc_cli}")
        Assertion.assert_equal(rc_api & rc_cli, True, "ERR: add_dns_filter_rule failed")


# Expected: Domain in sinkhole custom malicious domain list of DNS query is dropped by sinkhole.
class Test_DNS_Sinkhole_prior(Test):
    uuid = "SOSAIOT-TC-51418"
    # uuid = 'A473C7DE-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521148', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521148')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_dns_sinkhole(self):
        rc = dnsSec_api.enable_dns_sinkhole(**{'action': 'dropping_with_logs'})
        Assertion.assert_equal(rc, True, "ERR: failed to enable dns sinkhole !!")

    def test_02_add_custom_malicious_domain(self):
        rc = dnsSec_api.add_dns_custom_list(domain=CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: failed to add_custom_malicious_domain !!")

    def test_03_check_dns_is_blocked_by_sinkhole(self):
        res_init = initial_packet_monitor()
        logger.info(f'initial_packet_monitor result... {res_init}')
        rc = False
        out = check_dns_query_no_error(CParam.Domain)
        if not out:
            cmd = f'dns.qry.name=={CParam.Domain} and ip.src=={PC1_ETH0_IP} and ip.dst=={Parameter.FIREWALL}'
            rc = check_dns_packets_in_wireshark(cmd, target='DNS sinkhole dropped the pkt')
        Assertion.assert_equal(rc, True, "ERR: failed to check_dns_is_blocked_by_sinkhole !!")

    def test_04_initial_sinkhole(self):
        rc_del = dnsSec_api.delete_dns_custom_list(domains=CParam.Domain.split())
        logger.info(f"Delete sinkhole custom list domain...... {rc_del}")
        rc_disable = dnsSec_api.disable_dns_sinkhole()
        logger.info(f"Disable dns sinkhole...... {rc_disable}")
        Assertion.assert_equal(rc_del & rc_disable, True, "ERR: failed to initial_sinkhole !!")


class Test_DNS_Lookup_bypass(Test):
    uuid = "SOSAIOT-TC-51417"
    # uuid = 'A4721538-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521147', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521147')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_filtering_Gaming_action_to_block(self):
        gaming_block = {"actions": "{\"1\":2,\"2\":2,\"3\":2,\"4\":2,\"5\":2,\"6\":2,\"7\":2,\"8\":0,\"9\":2,\"10\":2,\"11\":0,\"12\":2,\"13\":2,\"14\":2,\"15\":2,\"16\":2,\"17\":2,\"18\":2,\"19\":2}"}
        add_profile_dict["dns_security"]["dns_filtering"]["profile"][0].update(gaming_block)
        rc = dnsFil_api.edit_dns_profile_by_name(msg=False, name=CParam.Profile_Name, **add_profile_dict)
        Assertion.assert_equal(rc, True, "ERR: fail to change Gaming action to block !!")

    def test_02_do_dns_lookup(self):
        rc = diagnostic_api.diag_dns_lookup_name_by_api(msg=False, **{'type': 'system', 'domain_name': CParam.Domain})
        Assertion.assert_equal(rc, True, "ERR: do_dns_lookup failed")

    def test_03_check_dns_lookup_result_success(self):
        out = diagnostic_api.get_name_lookup_Result()
        # example: {"data": {"domainName": "ea.com", "dnsServerUsed": "10.103.202.200", "resolvedAddrs": "23.37.147.2;",
        # "category": "No Category"}, "systime": 1703113099, "loggedin": true}
        data = dict(out).get('data')
        rc = bool(data.get("resolvedAddrs")) if data else False
        Assertion.assert_equal(rc, True, "ERR: fail to check_dns_lookup_result_success")


class Test_FQDN_bypass(Test):
    uuid = "SOSAIOT-TC-51419"
    # uuid = 'A475C9BC-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521149', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521149')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_fqdn(self):
        rc = ao_api.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add_fqdn failed")

    @repeat_method(6)
    def test_02_resolve_fqdn(self):
        res = ao_api.resolve_ao_by_name(name=ao_dict['name'], version='fqdn')
        logger.info(f'Resolve FQDN result...... {res}')
        out = ao_api.get_DAO_info(name=ao_dict['name'])
        # example :{"data":{"daoInfo":"IPv4:^Host: 67.225.146.248; TTL=2730^"},"systime":1703118448,"loggedin":true}
        data = dict(out).get('data')
        rc = 'Host:' in data.get('daoInfo') if data else False
        Assertion.assert_equal(rc, True, "ERR: resolve_fqdn failed")

    def test_03_delete_added_fqdn(self):
        rc = ao_api.del_addressobject(**{'ip_type': 'fqdn', 'name': ao_dict['name']})
        Assertion.assert_equal(rc, True, "ERR: delete added fqdn failed")


class Test_PING_Lookup_bypass(Test):
    uuid = "SOSAIOT-TC-51420"
    # uuid = 'A477A160-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521150', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521150')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_do_ping_lookup(self):
        rc = diagnostic_api.diag_ping(msg=False, dn=CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: do_ping_lookup failed")

    @repeat_method(6)
    def test_02_check_dns_lookup_result_success(self):
        out = diagnostic_api.get_Ping_Result()
        # example : {"data": {"line1": "ea.com [184.84.194.79] is alive", "line2": "Ping Time: 516 ms"}, "systime": 1703116619, "loggedin": true}
        data = dict(out).get('data')
        rc = 'Unable to resolve' not in data.get("line1") if data else False
        Assertion.assert_equal(rc, True, "ERR: fail to check_ping_lookup_result_success")


class Test_Split_DNS_bypass(Test):
    uuid = "SOSAIOT-TC-51421"
    # uuid = 'A479B194-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521151', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521151')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_split_dns(self):
        split_dns = {
            'domain': CParam.Domain,
            'ipv4': {
                'primary': Parameter.X1_DNS2,
                'secondary': Parameter.X1_DNS1,
                'tertiary': ''
            },
            'ipv6': {
                'primary': '',
                'secondary': '',
                'tertiary': ''
            },
            'local_interface': 'X0',
        }
        rc = dnsSett_api.add_split_dns(**split_dns)
        Assertion.assert_equal(rc, True, "ERR: failed to add_split_dns !!")

    @repeat_method(6)
    def test_02_check_resolve_result_success(self):
        rc_init = initial_packet_monitor()
        logger.info(f"initial packet monitor result......{rc_init}")
        rc = check_dns_query_no_error(CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: failed to check_resolve_result_success !!")

    def test_03_initial_split_dns(self):
        rc = dnsSett_api.delete_split_dns(domain=CParam.Domain)
        Assertion.assert_equal(rc, True, "ERR: failed to initial_split_dns !!")


class Test_import_and_export(Test):
    uuid = "SOSAIOT-TC-51415"
    # uuid = 'A4682A82-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521143', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521143')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_filtering(self):
        security_res = dnsFil_api.config_whitelist(**base_config_dict)
        logger.info(f'Config dns filtering base settings...... {security_res}')
        custom_domain_res = dnsSec_api.add_dns_custom_domain(**custom_domain_dict)
        logger.info(f'Config dns filtering custom domain...... {custom_domain_res}')
        rc = security_res & custom_domain_res
        Assertion.assert_equal(rc, True, "ERR: failed to config filtering !!")

    def test_02_export_configs(self):
        rc = sett_api.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: failed to export configs !!")

    def test_03_initialize_all_configs(self):
        default_config = {
            "dns_security": {
                "dns_filtering": {
                    "use_whitelist": True,
                    "forged_ip": {
                        "ipv4": "127.0.0.1",
                        "ipv6": "::1"
                    }
                }
            }
        }
        security_res = dnsFil_api.config_whitelist(**default_config)
        logger.info(f'Initialize dns filtering base settings...... {security_res}')
        custom_domain_res = dnsSec_api.del_custom_domain(domainname=CParam.Domain)
        logger.info(f'Initialize dns filtering custom domain...... {custom_domain_res}')
        policy_res = dnsRule_api.del_dns_rule_by_name(name="Filter")
        logger.info(f'Initialize dns policy...... {policy_res}')
        profile_res = dnsFil_api.del_dns_profile_by_name(name=CParam.Profile_Name)
        logger.info(f'Initialize dns policy...... {profile_res}')
        rc = security_res & custom_domain_res & policy_res & profile_res
        Assertion.assert_equal(rc, True, "ERR: failed to initialize_all_configs !!")

    def test_04_import_configs(self):
        rc = sett_api.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: failed to import_configs !!")

    @repeat_method(5)
    def test_05_check_configs(self):
        time.sleep(10)
        security_out = dnsFil_api.check_dns_filtering_global_settings()
        sec_rc = json.dumps(base_config_dict) in json.dumps(security_out)
        logger.info(f'Check dns filtering base settings...... {sec_rc}')

        custom_domain_out = dnsSec_api.show_dns_custom_domain()
        cus_rc = json.dumps(custom_domain_dict) in json.dumps(custom_domain_out)
        logger.info(f'Check dns filtering custom domain...... {cus_rc}')

        policies = dnsRule_api.get_dns_rule()
        rule = filter_rule_dict["dns_policies"][0]
        plc_rc = False
        if policies and 'dns_policies' in policies.keys():
            for policy in policies['dns_policies']:
                if policy.get('name') == rule['name']:
                    for key in rule.keys():
                        plc_rc = json.dumps(rule[key]) in json.dumps(policy.get(key))
                        if not plc_rc:
                            logger.error(f'The <{key}> are not intact!')
                            break
        logger.info(f'Check dns policy...... {plc_rc}')

        time.sleep(10)
        profiles = dnsFil_api.get_dns_filtering_profile()
        pro = add_profile_dict["dns_security"]["dns_filtering"]["profile"][0]
        pro_rc = False
        try:
            for profile in profiles["dns_security"]["dns_filtering"]["profile"]:
                if profile.get('name') == pro['name']:
                    for key in pro.keys():
                        pro_rc = pro[key] in profile.get(key)
                        if not pro_rc:
                            logger.error(f'The <{key}> are not intact!')
                            break
        except:
            logger.error('Get dns profiles failed!!')
        logger.info(f'Check dns profiles...... {pro_rc}')

        rc = sec_rc & cus_rc & plc_rc & pro_rc
        Assertion.assert_equal(rc, True, "ERR: failed to check_configs !!")


class Test_reboot(Test):
    uuid = "SOSAIOT-TC-51416"
    # uuid = 'A46B4988-4CF7-11EC-85F1-8B61918F55E4'
    description = show_testcase_info(TESTPLAN, '1521144', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521144')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot(self):
        rc = sett_api.boot_fw(mode=1)
        Assertion.assert_equal(rc, True, "ERR: failed to reboot !!")

    @repeat_method(5)
    def test_02_check_configs(self):
        Test_import_and_export().test_05_check_configs()
