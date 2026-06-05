from definition.utils import *


# Static IP Address Values
class Test_DHCP_Server_TC1525154(Test):
    uuid = "SOSAIOT-TC-55883"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_ip_for_dhcp_static_scope(self):
        static_opt = copy.deepcopy(static_scope)
        for ip in CaseParams.invalid_ips:
            static_opt["dhcp_server"]["ipv4"]["scope"]["static"][0]["ip"] = ip
            add_res, err_msg = dhcp_api.add_dhcp_server_scope_static(**static_opt, msg=True)
            logger.info(json.dumps(err_msg))
            rc = (not add_res) and "Invalid IP." in json.dumps(err_msg)
            if not rc:
                logger.info(f'check invalid ip <{ip}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: verfify invalid ip for dhcp static scope failed!!")


# Invalid Lease Time Value
class Test_DHCP_Server_TC1525165(Test):
    uuid = "SOSAIOT-TC-55894"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_lease_time_for_dhcp_scope(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        for t in CaseParams.invalid_lease_time:
            scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["lease_time"] = t
            add_res, err_msg = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt, msg=True)
            if t == 10000:
                rc = (
                         not add_res) and 'Value or string length(10000) out of bounds (min = 1, max = 9999)' in json.dumps(
                    err_msg)
            else:
                rc = (not add_res) and "'lease_time': invalid format" in json.dumps(err_msg)
            if not rc:
                logger.info(f'check invalid lease time <{t}> failed!!')
        Assertion.assert_equal(rc, True, 'ERR: verify invalid lease time for dhcp scope failed!!')


# valid Lease Time Value
class Test_DHCP_Server_TC1525166(Test):
    uuid = "SOSAIOT-TC-55895"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_valid_lease_time_for_dhcp_scope(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        for t in CaseParams.valid_lease_time:
            scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["lease_time"] = t
            rc = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt)
            if not rc:
                logger.info(f'check valid lease time <{t}> failed!!')
                break
            else:
                del_res = dhcp_api.delete_dhcp_server_scope_v4(
                    scope='dynamic', p1=dynamic_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["from"],
                    p2=dynamic_scope["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]['to'])
                logger.info(f'delete dynamic scope result: {del_res}')
        Assertion.assert_equal(rc, True, 'ERR: verify valid lease time for dhcp scope failed!!')


# Invalid Client Gateway Value
class Test_DHCP_Server_TC1525168(Test):
    uuid = "SOSAIOT-TC-55897"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_gateway_for_dynamic_entry(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        for ip in CaseParams.invalid_ips:
            scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["default_gateway"] = ip
            add_res, err_msg = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt, msg=True)
            rc = (not add_res) and "Invalid IP." in json.dumps(err_msg)
            if not rc:
                logger.error(f'check invalid ip <{ip}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: verify invalid gateway for dhcp scope failed!!")


# Invalid DNS Server Values
class Test_DHCP_Server_TC1525172(Test):
    uuid = "SOSAIOT-TC-55901"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_dns_for_dhcp_scope(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        for ip in CaseParams.invalid_ips:
            dns_opt = {"dns": {"server": {"static": {"primary": ip, "secondary": "", "tertiary": ""}}}}
            scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(dns_opt)
            add_res, err_msg = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt, msg=True)
            rc = (not add_res) and "Invalid IP." in json.dumps(err_msg)
            if not rc:
                logger.error(f'check invalid ip <{ip}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: verify invalid dns for dhcp scope failed!!")


# Invalid WinServer Values
class Test_DHCP_Server_TC1525174(Test):
    uuid = "SOSAIOT-TC-55903"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_dns_for_dhcp_scope(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        for ip in CaseParams.invalid_ips:
            win_server = {"wins": {"primary": ip, "secondary": ""}}
            scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0].update(win_server)
            add_res, err_msg = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt, msg=True)
            rc = (not add_res) and "Invalid IP." in json.dumps(err_msg)
            if not rc:
                logger.error(f'check invalid ip <{ip}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: verify invalid winserver for dhcp scope failed!!")


# Invalid Domain
class Test_DHCP_Server_TC1525175(Test):
    uuid = "SOSAIOT-TC-55904"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_invalid_domain_for_dhcp_scope(self):
        scope_opt = copy.deepcopy(dynamic_scope)
        scope_opt["dhcp_server"]["ipv4"]["scope"]["dynamic"][0]["domain_name"] = ''.join(
            random.choices(string.ascii_letters, k=256))
        add_res, err_msg = dhcp_api.add_dhcp_server_scope_dynamic(**scope_opt, msg=True)
        rc = (not add_res) and "Value or string length(256) out of bounds (max = 255)" in json.dumps(err_msg)
        Assertion.assert_equal(rc, True, "ERR: verify invalid domain for dhcp entry failed!!")


# [FUNC] Verify the DNS Server in DHCP client is valid when static WAN interface has no DNS Server.
class Test_DHCP_Server_TC1525179(Test):
    uuid = "SOSAIOT-TC-55908"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_dhcp_dynamic_scope_for_x2(self):
        rc = dhcp_api.add_dhcp_server_scope_dynamic(**dynamic_scope)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp dynamic scope for x2 failed!!')

    def test_02_check_client_dns_info(self):
        out1 = pc_renew_dynamic_addr()
        if re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out1):
            out2 = pc3_login.send_command(f'cat {lease_file}')
            rc = bool(re.search(rf'domain-name-servers\s+{Parameter.X1_DNS1},{Parameter.X1_DNS2}', out2))
        else:
            logger.error('client get dynamic address failed!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check client dns info failed!!")

    def test_03_remove_x1_dns(self):
        x1_opt.pop('dns1')
        x1_opt.pop('dns2')
        rc = iface_v4_api.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, 'ERR: update x1 dns failed!')

    def test_04_check_client_dns_after_update_x1_dns(self):
        Test_DHCP_Server_TC1525179().test_02_check_client_dns_info()


# [FUNC] Verify the DNS Server in new DHCP client is valid when DHCP WAN interface has no DNS Server
class Test_DHCP_Server_TC1525180(Test):
    uuid = "SOSAIOT-TC-55909"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_shutdown_x1(self):
        rc = iface_v4_api.disable_interface('x1')
        Assertion.assert_equal(rc, True, 'ERR: shutdown x1 failed!!')

    def test_02_check_new_client_dns_info(self):
        out1 = pc_renew_dynamic_addr(pc4_login)
        if re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out1):
            out2 = pc3_login.send_command(f'cat {lease_file}')
            rc = bool(re.search(rf'domain-name-servers\s+{Parameter.X1_DNS1},{Parameter.X1_DNS2}', out2))
        else:
            logger.error('client get dynamic address failed!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check client dns info failed!!")

    def test_03_up_x1(self):
        rc = iface_v4_api.enable_interface('x1')
        Assertion.assert_equal(rc, True, 'ERR: shutdown x1 failed!!')


# DNS Inherit Settings for Static Entry
class Test_DHCP_Server_TC1525139(Test):
    uuid = "SOSAIOT-TC-55868"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_dhcp_static_scope_for_x2(self):
        scope_opt = copy.deepcopy(static_scope)
        scope_opt["dhcp_server"]["ipv4"]["scope"]["static"][0].update({"mac": get_pc_eth_mac(pc3_login, 'eth1')})
        rc = dhcp_api.add_dhcp_server_scope_static(**scope_opt)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp dynamic scope for x2 failed!!')

    def test_02_check_client_dns_info_for_static_scope(self):
        Test_DHCP_Server_TC1525179().test_02_check_client_dns_info()

    def test_03_del_static_scope(self):
        rc = dhcp_api.delete_dhcp_server_scope_v4('static', CaseParams.static_ip, get_pc_eth_mac(pc3_login, 'eth1'))
        Assertion.assert_equal(rc, True, 'ERR: delete added static scope failed!!')


# DNS Manual Settings for Dynamic Entry
class Test_DHCP_Server_TC1525141(Test):
    uuid = "SOSAIOT-TC-55870"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_client_dns_info_for_dynamic_scope(self):
        Test_DHCP_Server_TC1525179().test_02_check_client_dns_info()

    def test_02_del_dynamic_scope(self):
        rc = dhcp_api.delete_dhcp_server_scope_v4(scope='dynamic', p1=CaseParams.dynamic_from, p2=CaseParams.dynamic_to)
        Assertion.assert_equal(rc, True, 'ERR: delete added dynamic scope failed!!')


# Client gets Domain Name Info with Static lease
class Test_DHCP_Server_TC1525146(Test):
    uuid = "SOSAIOT-TC-55875"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_dhcp_static_scope_with_domain_name(self):
        scope_opt = copy.deepcopy(static_scope)
        scope_opt["dhcp_server"]["ipv4"]["scope"]["static"][0].update(
            {"domain_name": CaseParams.domain_name, "mac": get_pc_eth_mac(pc3_login, 'eth1')})
        rc = dhcp_api.add_dhcp_server_scope_static(**scope_opt)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp static scope with domain name for x2 failed!!')

    def test_02_check_client_domain_name(self):
        out1 = pc_renew_dynamic_addr()
        if re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out1):
            out2 = pc3_login.send_command(f'cat {lease_file}')
            rc = f'domain-name "{CaseParams.domain_name}"' in out2
        else:
            logger.error('client get dynamic address failed!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check client dns info failed!!")

    def test_03_del_static_scope(self):
        Test_DHCP_Server_TC1525139().test_03_del_static_scope()


#  Client gets Network Setting with Dynamic Lease
class Test_DHCP_Server_TC1525147(Test):
    uuid = "SOSAIOT-TC-55876"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_dynamic_scope_with_network_settings(self):
        rc = dhcp_api.add_dhcp_server_scope_dynamic(**dynamic_scope)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp dynamic scope for x2 failed!!')

    def test_02_check_client_network_settings(self):
        out1 = pc_renew_dynamic_addr()
        if re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out1):
            out2 = pc3_login.send_command(f'cat {lease_file}')
            rc = 'subnet-mask 255.255.255.0' in out2 and f'routers {Parameter.X2_IP}' in out2
        else:
            logger.error('client get dynamic address failed!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check client dns info failed!!")

    def test_02_del_dynamic_scope(self):
        Test_DHCP_Server_TC1525141().test_02_del_dynamic_scope()


# Client Gets Network Settings with Static lease
class Test_DHCP_Server_TC1525148(Test):
    uuid = "SOSAIOT-TC-55877"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_dhcp_static_scope_with_network_settings(self):
        scope_opt = copy.deepcopy(static_scope)
        scope_opt["dhcp_server"]["ipv4"]["scope"]["static"][0].update({"mac": get_pc_eth_mac(pc3_login, 'eth1')})
        rc = dhcp_api.add_dhcp_server_scope_static(**scope_opt)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp static scope with domain name for x2 failed!!')

    def test_02_check_client_domain_name(self):
        out1 = pc_renew_dynamic_addr()
        if re.search(r'bound to 13.13.1.\d{2,3}.*renewal', out1):
            out2 = pc3_login.send_command(f'cat {lease_file}')
            rc = 'subnet-mask 255.255.255.0' in out2 and 'routers 0.0.0.0' in out2
        else:
            logger.error('client get dynamic address failed!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check client dns info failed!!")

    def test_03_del_static_scope(self):
        Test_DHCP_Server_TC1525139().test_03_del_static_scope()
        pc3_login.send_command('dhclient -r eth1')
        pc4_login.send_command('dhclient -r eth1')
        Assertion.assert_equal(True, True, 'ERR: init settings on firewall and pc3&pc4 failed!!!')
