from definition.settings import *


# Main Mode. using Renegotiate button can re-negotiate vpn tunnel.
class TestMain_TC15(Test):
    uuid = "SOSAIOT-TC-54315"
    description = show_testcase_info(TESTPLAN, 'Main_TC15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Main_TC15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_aos_for_vpn(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "LAN",
            "value": Parameter.REMOTE_X0_NET + ',255.255.255.0'
        }
        res1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        local_ag_dict = {"address_groups": [{
            "ipv4": {"address_object": {
                "ipv4": [{"name": "remote_vpn_net"}]},
                "name": "vpn_ag_name01"
            }}]}
        res2, msg2 = aogroupapi.add_addressgroup(msg=True, **local_ag_dict)
        if 'Already exists' in str(msg2):
            res2 = True
        remote_ao_dict = {
            "object_type": "network",
            "name": "local_vpn_net",
            "zone": "LAN",
            "value": f'{Parameter.X0_SUBNET},{Parameter.MASK}'
        }
        res3, msg3 = r_aoapi.config_addressobject(msg=True, **remote_ao_dict)
        if 'Already exists' in str(msg3):
            res3 = True
        remote_ag_dict = {"address_groups": [{
            "ipv4": {"address_object": {
                "ipv4": [{"name": "local_vpn_net"}]},
                "name": "vpn_ag_name01"
            }}]}
        res4, msg4 = r_aogroupapi.add_addressgroup(msg=True, **remote_ag_dict)
        if 'Already exists' in str(msg4):
            res4 = True
        logger.info(f'add aos result: {res1}, {res3}')
        logger.info(f'add ags result: {res2}, {res4}')
        Assertion.assert_equal(res1 & res2 & res3 & res4, True, "ERR: add aos failed")

    def test_02_s2s_vpn_configure(self):
        res1, msg1 = vpnapi.add_vpn_policy(msg=True, **l_s2s_vpn_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        res2, msg2 = r_vpnapi.add_vpn_policy(msg=True, **r_s2s_vpn_dict)
        if 'Already exists' in str(msg2):
            res2 = True
        logger.info(f'add s2s vpn result: {res1, res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: add vpn failed")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")

    def test_05_renegotiate_tunnel_button_click_on_remote(self):
        res = False
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        # local_cgi = 'cgiaction=ikeNegotiate&ikeSrcAddrType=4&ikeSrcNet=192.168.168.0&ikeSrcMask=255.255.255.0
        # &ikeDstAddrType=4&ikeDstNet=172.16.1.0&ikeDstMask=255.255.255.0&ikeDstGw=12.12.1.201&ikeDstGwPort=500
        # &InitCookie=JZbKrYOXmCk=&ikeIsDhcpClient=0&ikeInSpi='
        remote_cgi = 'cgiaction=ikeNegotiate&ikeSrcAddrType=4&ikeSrcNet=172.16.1.0&ikeSrcMask=255.255.255.0' \
                     '&ikeDstAddrType=4&ikeDstNet=192.168.168.0&ikeDstMask=255.255.255.0&ikeDstGw=12.12.1.168' \
                     '&ikeDstGwPort=500&InitCookie=lJW+nmZhewE=&ikeIsDhcpClient=0&ikeInSpi='
        for count in range(5):
            # res = r_vpnapi.Renegotiate_Tunnel_stats()
            res = r_vpnapi.Re_Negotiate_Entry(stream=remote_cgi)
            if res:
                break
            else:
                logger.info('waiting for 10s to retry...')
                time.sleep(10)
        Assertion.assert_equal(res, True, "ERR: click renegotiate tunnel button failed.")

    @repeat_method(3)
    def test_06_verify_local_vpn_log(self):
        logger.info('waiting for 20s to renegotiated vpn...')
        time.sleep(20)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', CaseParams.local_vpn_name01, 'Lifetime=600']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local IKE negotiation log failed.")

    def test_07_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# Main Mode. disable vpn can show in log.
class TestMain_TC18(Test):
    uuid = "SOSAIOT-TC-54318"
    description = show_testcase_info(TESTPLAN, 'Main_TC18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Main_TC18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_trigger_vpn_negotiation_continue_from_local(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        PC2_login.send_command(f'ping {PC5_ETH1_IP} -c 300  > /tmp/ping.log &')
        output = PC2_login.send_command('ps aux | grep ping')

        logger.info('waiting for 10s to renegotiated vpn...')
        time.sleep(10)
        Assertion.assert_regular(output, f'ping {PC5_ETH1_IP}', "ERR: trigger vpn negotiation continue failed")

    def test_02_disable_vpn_on_remote(self):
        disable_dict = {
            'name': CaseParams.remote_vpn_name01,
            'enable': False
        }
        output = r_vpnapi.dis_s2svpn_policy(**disable_dict)
        Assertion.assert_equal(output, True, "ERR: disable vpn on remote failed")

    def test_03_check_delete_request_and_tunnel_status_in_log(self):
        logger.info('waiting for 10s to renegotiated vpn...')
        time.sleep(10)
        fw_logs = logapi.get_log(413)
        delrequest = True if 'Received IKE SA delete request' in str(fw_logs) else False
        fw_logs = logapi.get_log(427)
        lists = ['IPsec Tunnel status changed', 'Tunnel Down', CaseParams.local_vpn_name01]
        tunneldown = [x in str(fw_logs) for x in lists]
        logger.info(f'check tunnel down: {tunneldown}')
        Assertion.assert_equal(delrequest & all(tunneldown), True, "ERR: check vpn log failed.")

    def test_04_enable_vpn_on_remote(self):
        enable_dict = {
            'name': CaseParams.remote_vpn_name01,
            'enable': True
        }
        output1 = r_vpnapi.en_s2svpn_policy(**enable_dict)
        PC2_login.send_command('killall ping')
        Assertion.assert_equal(output1, True, "ERR: enable vpn on remote failed")


# Main Mode. vpn negotiation successful in enable ipsec_pfs_dhgroup.
class TestMain_TC21(Test):
    uuid = "SOSAIOT-TC-54320"
    description = show_testcase_info(TESTPLAN, 'Main_TC21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Main_TC21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_local_s2s_ipsec_pfs(self):
        output = vpnapi.show_s2svpnpolicy()
        Assertion.assert_regular(str(output), "dh_group': '14", "ERR: check local ipser pfs failed.")

    @repeat_method(5)
    def test_02_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 10)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_03_check_active_s2s_vpn(self):
        logger.info('wait for 20s to make sure vpn negotiation...')
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")


# Main Mode. vpn negotiation successful in domain.
class TestMain_TC23(Test):
    uuid = "SOSAIOT-TC-54322"
    description = show_testcase_info(TESTPLAN, 'Main_TC23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Main_TC23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_to_main(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict.update({
            "ike_exchange": "main",
            "pri_gate": "remote.baidu.com",
        })
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_to_main(self):
        vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        vpn_dict['ike_exchange'] = 'main'
        res = r_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")


# Main Mode. using Renegotiate button can re-negotiate vpn tunnel.
class TestAggressive_TC26(Test):
    uuid = "SOSAIOT-TC-54325"
    description = show_testcase_info(TESTPLAN, 'Aggressive_TC26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Aggressive_TC26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_to_aggressive(self):
        res = vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_to_aggressive(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")

    def test_05_renegotiate_tunnel_button_click_on_remote(self):
        TestMain_TC15().test_05_renegotiate_tunnel_button_click_on_remote()

    @repeat_method(3)
    def test_06_verify_local_vpn_log(self):
        logger.info('waiting for 20s to renegotiated vpn...')
        time.sleep(20)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', CaseParams.local_vpn_name01, 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local IKE negotiation log failed.")

    def test_07_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# Aggressive Mode. The tunnel is re-established after SA life time expired
class TestAggressive_TC27(Test):
    uuid = "SOSAIOT-TC-54326"
    description = show_testcase_info(TESTPLAN, 'Aggressive_TC27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Aggressive_TC27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_02_wait_for_270s_to_renegotiated_vpn(self):
        res = False
        logger.info('wait for 270s to renegotiated vpn...')
        time.sleep(260)
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        time.sleep(10)

        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        if output:
            fw_logs = logapi.get_log(89)
            lists = ['IKE negotiation complete', CaseParams.local_vpn_name01, 'Lifetime=120']
            checkres = [x in str(fw_logs) for x in lists]
            logger.info(f'check log 89: {checkres}')
            res = all(checkres)
        else:
            logger.info('trigger re negotiation vpn via ping failed.')
        Assertion.assert_equal(res, True, "ERR: check re negotiation log failed.")


# Aggressive Mode. Re-enable IKE VPN policy with incoming traffic.
class TestAggressive_TC29(Test):
    uuid = "SOSAIOT-TC-54328"
    description = show_testcase_info(TESTPLAN, 'Aggressive_TC29', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Aggressive_TC29')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_trigger_vpn_negotiation_continue_from_local(self):
        TestMain_TC18().test_01_trigger_vpn_negotiation_continue_from_local()

    def test_02_disable_vpn_on_remote(self):
        disable_dict = {
            'name': CaseParams.remote_vpn_name01,
            'enable': False
        }
        output = r_vpnapi.dis_s2svpn_policy(**disable_dict)
        Assertion.assert_equal(output, True, "ERR: disable vpn on remote failed")

    def test_03_check_delete_request_and_tunnel_status_in_log(self):
        TestMain_TC18().test_03_check_delete_request_and_tunnel_status_in_log()

    def test_04_enable_vpn_on_remote(self):
        enable_dict = {
            'name': CaseParams.remote_vpn_name01,
            'enable': True
        }
        output1 = r_vpnapi.en_s2svpn_policy(**enable_dict)
        Assertion.assert_equal(output1, True, "ERR: enable vpn on remote failed")

    def test_05_check_vpn_re_negotiation_in_log(self):
        logger.info('wait for 20s to re negotiated vpn...')
        time.sleep(20)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', CaseParams.local_vpn_name01, 'Lifetime=120']
        checkres = [x in str(fw_logs) for x in lists]
        logger.info(f'check log 89: {checkres}')

        PC2_login.send_command('killall ping')
        Assertion.assert_equal(all(checkres), True, "ERR: check re negotiation log failed.")


# aggressive Mode. vpn negotiation successful in enable ipsec_pfs_dhgroup.
class TestAggressive_TC32(Test):
    uuid = "SOSAIOT-TC-54330"
    description = show_testcase_info(TESTPLAN, 'Aggressive_TC32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Aggressive_TC32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_local_s2s_ipsec_pfs(self):
        output = vpnapi.show_s2svpnpolicy()
        Assertion.assert_regular(str(output), "dh_group': '14", "ERR: check local ipser pfs failed.")

    def test_02_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_03_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")


# Super net VPN destination network can re-negotiate vpn tunnel.
class TestSuperNet_TC36(Test):
    uuid = "SOSAIOT-TC-54333"
    description = show_testcase_info(TESTPLAN, 'SuperNet_TC36', description=True)['title']
    local_sub_net = 'local_sub_net'
    remote_sub_net = 'remote_sub_net'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SuperNet_TC36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_aos_for_vpn(self):
        local_ao_dict = {
            "object_type": "network",
            "name": self.remote_sub_net,
            "zone": "LAN",
            "value": '172.16.0.0,255.255.0.0'
        }
        res1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        local_ao_dict['name'] = self.local_sub_net
        res2, msg2 = r_aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg2):
            res2 = True
        Assertion.assert_equal(res1 & res2, True, "ERR: add aos failed")

    def test_02_edit_local_and_remote_s2s_to_supnet(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict['remote_net_name'] = self.remote_sub_net
        res1 = vpnapi.edit_vpn_policy(**vpn_dict)

        vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        vpn_dict['local_net_name'] = self.local_sub_net
        res2 = r_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: edit local and remote vpn to supnet failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")


# A tunnel between local network and remote range
class TestNetworkRange_TC44(Test):
    uuid = "SOSAIOT-TC-54334"
    description = show_testcase_info(TESTPLAN, 'NetworkRange_TC44', description=True)['title']
    remote_range_net = 'remote_range_net'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NetworkRange_TC44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_aos_for_vpn(self):
        local_ao_dict = {
            "object_type": "range",
            "name": self.remote_range_net,
            "zone": "LAN",
            "value": '172.16.1.20,172.16.1.60'
        }
        res1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        Assertion.assert_equal(res1, True, "ERR: add aos failed")

    def test_02_edit_local_and_remote_s2s_to_range_net(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict['remote_net_name'] = self.remote_range_net
        res1 = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res1, True, "ERR: edit local and remote vpn to range net failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")


# after Disable VPN, IPsec Tunnel status changed to Tunnel Down
class TestDisable_TC47(Test):
    uuid = "SOSAIOT-TC-54336"
    description = show_testcase_info(TESTPLAN, 'Disable_TC47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Disable_TC47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_to_main(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict['ike_exchange'] = 'main'
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_to_main(self):
        vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        vpn_dict['ike_exchange'] = 'main'
        res = r_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")

    def test_05_disable_vpn_on_local(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        time.sleep(5)

        disable_dict = {"vpn": {"enable": False}}
        output = r_vpnapi.config_vpn_base(**disable_dict)
        Assertion.assert_equal(output, True, "ERR: disable vpn on remote failed")

    def test_06_check_delete_request_and_tunnel_status_in_log(self):
        TestMain_TC18().test_03_check_delete_request_and_tunnel_status_in_log()

    def test_07_verify_ping_to_remote_pc5_blocked(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

    def test_08_enable_vpn_on_local(self):
        enable_dict = {"vpn": {"enable": True}}
        output = r_vpnapi.config_vpn_base(**enable_dict)
        Assertion.assert_equal(output, True, "ERR: enable vpn on remote failed")


# Rules creation is auto added in VPN policy
class TestAutoRule_TC93(Test):
    uuid = "SOSAIOT-TC-54340"
    description = show_testcase_info(TESTPLAN, 'AutoRule_TC93', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'AutoRule_TC93')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_acl_from_lan_to_vpn(self):
        res = False
        lantovpn = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for acl in lantovpn['access_rules']:
                if 'X0 Subnet' in str(acl) and 'remote_vpn_net' in str(acl):
                    res = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res, True, "ERR: check lan to vpn acl failed.")

    def test_02_check_acl_from_vpn_to_lan(self):
        res = False
        vpntolan = accessruleapi.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for acl in vpntolan['access_rules']:
                if 'X0 Subnet' in str(acl) and 'remote_vpn_net' in str(acl):
                    res = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res, True, "ERR: check vpn to lan failed.")


# Re-key event with default SA lifetime
class TestReKey_TC98(Test):
    uuid = "SOSAIOT-TC-54343"
    description = show_testcase_info(TESTPLAN, 'ReKey_TC98', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ReKey_TC98')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_to_main(self):
        res = vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_to_main(self):
        vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        vpn_dict.update({
            'pri_gate': '0.0.0.0',
            'ike_lifetime': 28800,
            'ipsec_lifetime': 28800,
        })
        vpn_dict.pop('keep_alive')
        res = r_vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(5)
    def test_04_check_active_s2s_vpn(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), CaseParams.local_vpn_name01, "ERR: check s2s vpn status failed")

    def test_05_verify_long_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 300)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# Firewall can be managed via https through s2s vpn policy
class TestManagedHttps_TC103(Test):
    uuid = "SOSAIOT-TC-54302"
    description = show_testcase_info(TESTPLAN, 'ManagedHttps_TC103', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ManagedHttps_TC103')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_local_user(self):
        add_user_dict = {
            'action': 'add',
            'username': 'soincauto',
            'userpassword': 'S0nic@uto',
            'member_of': ['SonicWALL Administrators']
        }

        output1, msg1 = userLocalapi.local_user(msg=True, **add_user_dict)
        if 'Already exists' in str(msg1):
            output1 = True
        output2 = userLocalapi.user_member_of(**add_user_dict)
        logger.info(f'add local user: {output1}, add user member: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: Add Local user of SNWL Admin failed!")

    def test_02_edit_local_s2s_managed(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict.update({
            'user_login_https': True,
            'management_https': True,
        })
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_03_edit_remote_s2s_to_main(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_04_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_05_https_login_via_vpn_from_remote(self):
        SCRIPTS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Smoke_Test/Quick_Smoke_For_RTQA/definition/scripts'
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i {Parameter.FIREWALL} -a limit_login -u soincauto -p S0nic@uto'
        logger.info(cmd)
        output = PC5_login.send_command(cmd)
        Assertion.assert_regular(output, 'login fw result is True', "ERR: https login via vpn remote failed")


# Firewall can be managed via ssh through s2s vpn policy
class TestManagedssh_TC104(Test):
    uuid = "SOSAIOT-TC-54303"
    description = show_testcase_info(TESTPLAN, 'ManagedSSH_TC104', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ManagedSSH_TC104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_managed(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict.update({
            'management_ssh': True,
        })
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_ssh_login_via_vpn_from_remote(self):
        SCRIPTS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Smoke_Test/Quick_Smoke_For_RTQA/definition/scripts'
        cmd = f'python3 {SCRIPTS_PATH}/run_ssh_to_fw.py -i {Parameter.FIREWALL} -a showversion'
        logger.info(cmd)
        output = PC5_login.send_command(cmd)
        Assertion.assert_regular(output, 'Firmware Version', "ERR: ssh login via vpn remote failed")


# Firewall can be managed via snmp through s2s vpn policy
class TestSNMP_TC110(Test):
    uuid = "SOSAIOT-TC-54307"
    description = show_testcase_info(TESTPLAN, 'SNMP_TC110', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SNMP_TC110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_snmp(self):
        res = False
        enRes = snmpapi.enable_snmp()
        logger.info(f" Enable result is {enRes} ")
        logger.info(f"{' Check enable flag ':=^50}")
        checkres = snmpapi.show_snmp()
        if 'snmp' in checkres.keys() and 'enable' in checkres['snmp'].keys():
            res = True if checkres["snmp"]["enable"] else False
            
        snmp_dict = {
            "snmp": {
            "enable": True,
            "get_community_name": "public"
        }}
        confres = snmpapi.configure_snmp(**snmp_dict)
        logger.info(f'configure snmp public: {confres}')

        output = snmpapi.snmp_advance_settings(**{'mandatory': False})
        logger.info(f'disable snmp v3: {output}')
        Assertion.assert_equal(res, True, "ERR: Enable snmp failed!")

    def test_02_enable_snmp_on_x0(self):
        x0_dict = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.FIREWALL,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'mgmt_snmp': True
        }
        res = interfaceapi.config_interface(**x0_dict)
        Assertion.assert_equal(res, True, "ERR: Enable X0 SNMP failed!")

    def test_03_edit_local_s2s_managed(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict.update({
            'management_snmp': True,
        })
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_04_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(3)
    def test_05_snmp_get_system_and_check_model(self):
        res = False
        status = statusapi.show_status()
        logger.info(f"{f' snmp monitor -sysDescr- result ':=^60}")
        cmd = f'snmpwalk -v2c -cpublic -OQv {Parameter.FIREWALL} sysDescr'
        output = PC5_login.send_command(cmd)
        if 'model' in status.keys():
            res = True if status['model'] in output else False
        else:
            logger.info('wait for 10s to retry...')
            time.sleep(10)
        Assertion.assert_equal(res, True, f"ERR: Get snmp sysDescr failed!!")


# Disable management on s2s sa, firewall won™t be managed then
class TestDisableManaged_TC106(Test):
    uuid = "SOSAIOT-TC-54304"
    description = show_testcase_info(TESTPLAN, 'DisableManaged_TC106', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DisableManaged_TC106')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_local_s2s_managed(self):
        vpn_dict = copy.deepcopy(edit_localvpn_dict)
        vpn_dict.update({
            'user_login_https': False,
            'management_https': False,
            'management_ssh': False,
            'management_snmp': False,
        })
        res = vpnapi.edit_vpn_policy(**vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_03_verify_ping_to_remote_pc5_passed(self):
        output = PC2_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 5)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_04_https_login_via_vpn_from_remote_must_be_blocked(self):
        SCRIPTS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Smoke_Test/Quick_Smoke_For_RTQA/definition/scripts'
        cmd = f'python3 {SCRIPTS_PATH}/run_user_login_to_fw.py ' \
              f'-i {Parameter.FIREWALL} -a limit_login -u soincauto -p password'
        logger.info(cmd)
        output = PC5_login.send_command(cmd)
        Assertion.assert_not_regular(output, 'login fw result is True', "ERR: https login via vpn remote failed")

    def test_05_ssh_login_via_vpn_from_remote_must_be_blocked(self):
        SCRIPTS_PATH = os.environ["PYTHON_SONICOS_HOME"] + '/Smoke_Test/Quick_Smoke_For_RTQA/definition/scripts'
        cmd = f'python3 {SCRIPTS_PATH}/run_ssh_to_fw.py -i {Parameter.FIREWALL} -a showversion'
        logger.info(cmd)
        output = PC5_login.send_command(cmd)
        Assertion.assert_not_regular(output, 'Firmware Version', "ERR: ssh login via vpn remote failed")

    def test_06_snmp_get_system_and_check_model_must_be_blocked(self):
        res = False
        status = statusapi.show_status()
        logger.info(f"{f' snmp monitor -sysDescr- result ':=^60}")
        cmd = f'snmpwalk -v2c -cpublic -OQv {Parameter.FIREWALL} sysDescr'
        output = PC5_login.send_command(cmd)
        if 'model' in status.keys():
            res = True if status['model'] in output else False
        Assertion.assert_not_equal(res, True, f"ERR: Get snmp sysDescr failed!!")


# A tunnel between VLANs
class TestVLAN_TC96(Test):
    uuid = "SOSAIOT-TC-54342"
    description = show_testcase_info(TESTPLAN, 'VLAN_TC96', description=True)['title']
    remote_x0_range = 'remote_range_50_55'
    local_x3_network = 'local_network_3_0'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'VLAN_TC96')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_aos_for_vpn(self):
        local_ao_dict = {
            "object_type": "range",
            "name": self.remote_x0_range,
            "zone": "LAN",
            "value": '172.16.1.50,172.16.1.55'
        }
        res1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            res1 = True
        remote_ao_dict = {
            "object_type": "network",
            "name": self.local_x3_network,
            "zone": "LAN",
            "value": f'{Parameter.X3_SUBNET},{Parameter.MASK}'
        }
        res2, msg2 = r_aoapi.config_addressobject(msg=True, **remote_ao_dict)
        if 'Already exists' in str(msg2):
            res2 = True
        Assertion.assert_equal(res1 & res2, True, "ERR: add aos failed")

    def test_02_edit_local_s2s_vlan(self):
        local_dict = {
            'edit_auth': True,
            'edit_network': True,
            'edit_proposal': True,
            'edit_advanced': True,
            'type': 'site_to_site',
            'name': CaseParams.local_vpn_name02,
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'pri_gate': Parameter.REMOTE_X2_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '2.2.2.2',
            'local_net_type': 'name',
            'remote_net_type': 'name',
            'local_net_name': 'X3 Subnet',
            'remote_net_name': self.remote_x0_range,

            'ike_exchange': 'main',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 120,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 120,
            'bound_to': ['interface', f'X2:V{L_X2_VLAN}'],
            'keep_alive': False,
        }
        res, msg = vpnapi.add_vpn_policy(msg=True, **local_dict)
        if 'Already exists' in str(msg):
            res = True
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_03_edit_remote_s2s_vlan(self):
        local_dict = {
            'edit_auth': True,
            'edit_network': True,
            'edit_proposal': True,
            'edit_advanced': True,
            'type': 'site_to_site',
            'name': CaseParams.remote_vpn_name02,
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'pri_gate': Parameter.X2_VLAN_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '2.2.2.2',
            'local_net_type': 'name',
            'remote_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_name': self.local_x3_network,

            'ike_exchange': 'main',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 600,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 600,
            'bound_to': ['interface', f'X2:V{L_X2_VLAN}'],
            'keep_alive': False,
        }
        res, msg = r_vpnapi.add_vpn_policy(msg=True, **local_dict)
        if 'Already exists' in str(msg):
            res = True
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_04_verify_ping_to_remote_pc5_passed(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        time.sleep(5)

        output = PC3_login.ping_from_eth(PC5_ETH1_IP, 'eth1', 10)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_05_check_vpn_re_negotiation_in_log(self):
        logger.info('wait for 20s to re negotiated vpn...')
        time.sleep(20)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', CaseParams.local_vpn_name02, 'Lifetime=120']
        checkres = [x in str(fw_logs) for x in lists]
        logger.info(f'check log 89: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check re negotiation log failed.")


# Edit the lifetime for Multiple VPN tunnels, check the rekey for the VPN tunnels
class TestMultipleVPN_TC101(Test):
    uuid = "SOSAIOT-TC-54300"
    description = show_testcase_info(TESTPLAN, 'MultipleVPN_TC101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MultipleVPN_TC101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_trigger_vpn_negotiation_continue_from_local_in_x0(self):
        PC2_login.send_command(f'ping {PC5_ETH1_IP} -c 300  > /tmp/ping.log &')
        output = PC2_login.send_command('ps aux | grep ping')
        Assertion.assert_regular(output, f'ping {PC5_ETH1_IP}', "ERR: trigger vpn negotiation continue failed")

    def test_02_trigger_vpn_negotiation_continue_from_local_in_x3(self):
        PC3_login.send_command(f'ping {PC5_ETH1_IP} -c 300  > /tmp/ping.log &')
        output = PC3_login.send_command('ps aux | grep ping')
        Assertion.assert_regular(output, f'ping {PC5_ETH1_IP}', "ERR: trigger vpn negotiation continue failed")

    def test_03_check_vpn_re_negotiation_in_log(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        logger.info('wait for 300s to re negotiated vpn...')
        time.sleep(300)
        fw_logs = logapi.get_log(89)
        lists1 = ['IKE negotiation complete', CaseParams.local_vpn_name01, 'Lifetime=120']
        checkres1 = [x in str(fw_logs) for x in lists1]
        logger.info(f'check log 89: {checkres1}')

        lists2 = ['IKE negotiation complete', CaseParams.local_vpn_name02, 'Lifetime=120']
        checkres2 = [x in str(fw_logs) for x in lists2]
        logger.info(f'check log 89: {checkres2}')

        PC2_login.send_command('killall ping')
        Assertion.assert_equal(all(checkres1) & all(checkres2), True, "ERR: check re negotiation log failed.")





