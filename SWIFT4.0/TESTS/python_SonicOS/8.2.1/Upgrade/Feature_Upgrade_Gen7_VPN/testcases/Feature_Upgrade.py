from definition.settings import *
from definition.utils import *
from definition.firewall_configure import FWFunctionConfigure

# the fw function configure object
fwconfigure = FWFunctionConfigure()


# path = '/logs/downloads/sw_tz_370_eng.7.1.2-7005-P5844.bin.sig'
class TestUpgradeToPreviousFirmware(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_upgrade_to_previous_firmware(self):
        upgraderes = upgrade_firewall_software(path=Parameter.prebuild, bulidtype='old')
        Assertion.assert_equal(upgraderes, True, "ERR: upgrade the old version failed")


class TestConfigureOldFirmware(Test):
    uuid = 'NonTC'

    def test_01_wlb_configure(self):
        output = fwconfigure.wlb_configure()
        Assertion.assert_equal(output, True, "ERR: wlb configure failed")

    def test_02_numbered_ti_configure(self):
        output = fwconfigure.numbered_ti_configure()
        Assertion.assert_equal(output, True, "ERR: numbered ti configure failed")

    def test_03_s2s_vpn_configure(self):
        output = fwconfigure.s2s_vpn_configure()
        Assertion.assert_equal(output, True, "ERR: s2s vpn configure failed")

    def test_04_wan_groupvpn_configure(self):
        output = fwconfigure.wan_groupvpn_configure()
        Assertion.assert_equal(output, True, "ERR: wan groupvpn configure failed")

    def test_05_ula_configure(self):
        output = fwconfigure.ula_configure()
        Assertion.assert_equal(output, True, "ERR: ula configure failed")


class Test_UpgradeUnderTestFirmwareViaUI(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_upgrade_under_test_firmware(self):
        upgraderes = upgrade_firewall_software(path=Parameter.testbuild, bulidtype='new')
        Assertion.assert_equal(upgraderes, True, "ERR: upgrade the under test firmware failed")


class TestWLB_TC031(Test):
    uuid = "SOSAIOT-TC-74762"
    description = show_testcase_info(TESTPLAN, 'WLB_TC031', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'WLB_TC031')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_WLB_configure(self):
        output = failoverapi.check_failover_members_status()
        lists = ['X1', 'X2']
        res = [x in str(output) for x in lists]
        logger.info(f'check lb member result: {res}')
        Assertion.assert_equal(res.count(True), 2, "ERR: wlb configure check failed")


class TestWLB_TC032(Test):
    uuid = "SOSAIOT-TC-74763"
    description = show_testcase_info(TESTPLAN, 'WLB_TC032', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'WLB_TC032')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ping_from_X0_to_X2_passed(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC2_login.ping(Parameter.R_X2_IP)
        Assertion.assert_equal(output, True, "ERR: check ping from lan to wan failed")


class TestTunnel_TC039(Test):
    uuid = "SOSAIOT-TC-74770"
    description = show_testcase_info(TESTPLAN, 'Tunnel_TC039', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Tunnel_TC039')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ti_configure(self):
        output = interfaceapi.get_tunnel_interface_status(name='Ni', type='vpn')
        Assertion.assert_regular(json.dumps(output),
                                 Parameter.VPN_IF_IP_LOCAL,
                                 "ERR: check tunnel interface configure failed")

    def test_02_check_tunnel_vpn_configure(self):
        output = vpnapi.show_tunnelvpnpolicy()
        filter_list = ['auto_local_tunnel01', Parameter.R_X2_IP, '2.2.2.2']
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check tunnel vpn: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check tunnel vpn configure failed")


class TestTunnel_TC040(Test):
    uuid = "SOSAIOT-TC-74771"
    description = show_testcase_info(TESTPLAN, 'Tunnel_TC040', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Tunnel_TC040')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_check_ping_via_tunnel_passed(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC2_login.ping(PC5_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: check ping via tunnel failed")


class TestS2S_VPN_TC043(Test):
    uuid = "SOSAIOT-TC-74774"
    description = show_testcase_info(TESTPLAN, 'S2S_VPN_TC043', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'S2S_VPN_TC043')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_S2S_VPN_configure(self):
        output = vpnapi.show_s2svpnpolicy()
        filter_list = ['auto_local_s2s_vpn01', '12.12.2.202', '3.3.3.3']
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check tunnel vpn: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check s2s vpn configure failed")

    def test_02_check_group_vpn_configure(self):
        output = vpnapi.show_wangroup_vpn()
        filter_list = ['sha-384', 'sha_384', 'Firewalled Subnets']
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check tunnel vpn: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check group vpn configure failed")


class TestS2S_VPN_TC044(Test):
    uuid = "SOSAIOT-TC-74775"
    description = show_testcase_info(TESTPLAN, 'S2S_VPN_TC044', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'S2S_VPN_TC044')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_tunnel_vpn(self):
        l_tunnel_dict['pri_gate'] = '34.34.34.34'
        output1 = vpnapi.edit_vpn_policy(**l_tunnel_dict)

        r_tunnel_dict['pri_gate'] = '35.35.35.35'
        output2 = r_vpnapi.edit_vpn_policy(**r_tunnel_dict)
        logger.info(f'modify tunnel vpn result: {output1}, {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: modify tunnel vpn failed")

    def test_02_modify_s2s_vpn(self):
        l_s2s_vpn_dict['enable'] = True
        l_s2s_vpn_dict['pri_gate'] = Parameter.R_X2_IP
        output1 = vpnapi.edit_vpn_policy(**l_s2s_vpn_dict)

        r_s2s_vpn_dict['enable'] = True
        r_s2s_vpn_dict['pri_gate'] = Parameter.X2_IP
        output2 = r_vpnapi.edit_vpn_policy(**r_s2s_vpn_dict)
        logger.info(f'modify s2s vpn result: {output1}, {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: modify s2s vpn failed")

    def test_03_add_acl_between_lan_and_vpn(self):
        output1, msg1 = accessruleapi.add_accessrule(msg=True, **lan_vpn_acl_dict)
        if 'Already exists' in str(msg1):
            output1 = True
        lan_vpn_acl_dict['access_rules'][0]['ipv4'].update(
            {
                "name": "vpn_to_lan_name01",
                "from": "VPN",
                "to": "LAN",
            }
        )
        output2, msg2 = r_accessruleapi.add_accessrule(msg=True, **lan_vpn_acl_dict)
        if 'Already exists' in str(msg2):
            output2 = True
        logger.info(f'add acl result: {output1}, {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: add acl between lan and vpn failed")

    @repeat_method(5)
    def test_04_check_ping_via_s2s_vpn_passed(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC2_login.ping(PC5_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: check ping via tunnel failed")


class TestSSLVPN_TC045(Test):
    uuid = "SOSAIOT-TC-74776"
    description = show_testcase_info(TESTPLAN, 'SSLVPN_TC045', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SSLVPN_TC045')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_sslvpn_configure(self):
        output = sslvpnserverapi.get_server_access_setting()
        Assertion.assert_regular(json.dumps(output),
                                 'enable": true, "zone": "LAN',
                                 "ERR: check gav configure failed")


class TestSSLVPN_TC046(Test):
    uuid = "SOSAIOT-TC-74777"
    description = show_testcase_info(TESTPLAN, 'SSLVPN_TC046', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SSLVPN_TC046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_login_from_portal_page_in_wan_host(self):
        cmd = [f'python3 {CONF_PATH}/ui_login_fw.py '
               f'-url https://{Parameter.X1_IP}:4433 '
               f'-user {CaseParams.sslvpn_user_name} -pwd {Params.G_NEW_PASSWORD}']
        # clean firefox process
        PC4_login.send_command('pkill firefox')
        time.sleep(5)
        output = PC4_login.send_commands(cmd)
        logger.info("login with user\n" + output)
        logger.info('wait 20s to check login user status...')
        time.sleep(20)
        # check user status
        showres = userstatusapi.show_user_status()
        res = True if CaseParams.sslvpn_user_name in json.dumps(showres) else False
        Assertion.assert_equal(res, True, "failed to get user status")


class TestULA_TC049(Test):
    uuid = "SOSAIOT-TC-74780"
    description = show_testcase_info(TESTPLAN, 'ULA_TC049', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ULA_TC049')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_local_user_configure(self):
        output = userLocalapi.show_local_user_by_name(name=CaseParams.ula_user_name)
        Assertion.assert_regular(json.dumps(output), 'LAN Subnets', "ERR: check local user configure failed")


class TestULA_TC050(Test):
    uuid = "SOSAIOT-TC-74781"
    description = show_testcase_info(TESTPLAN, 'ULA_TC050', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ULA_TC050')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_acl_configure(self):
        res = False
        getres = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='WAN')
        try:
            for rule in getres['access_rules']:
                if rule['ipv4']['name'] == 'Default Access Rule' and rule['ipv4']['action'] == 'allow':
                    logger.info(f'get target rule successful: {rule}')
                    acl_dict = copy.deepcopy(default_acl_dict)
                    acl_dict.update({"users": {
                        "included": {"group": 'Trusted Users'},
                        "excluded": {"none": True}
                    }})
                    res = accessruleapi.config_accessrule_via_uuid(uuid=rule['ipv4']['uuid'], acl_json=acl_dict)
                    break
        except exception as e:
            logger.info(f'get lan to wan acl failed: {repr(e)}')
        return res

    @repeat_method(5)
    def test_02_check_ula_function(self):
        time.sleep(10)
        cmd = [f'curl https://{PC4_ETH1_IP} -k']
        output = PC2_login.send_commands(cmd)
        Assertion.assert_regular(json.dumps(output), 'Policy Jump', "ERR: check ula function failed")














# class TestCFS_TC016(Test):
#     uuid = '1513999'
#     description = show_testcase_info(TESTPLAN, 'CFS_TC016', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'CFS_TC016')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     @repeat_method(5)
#     def test_01_access_https_site_must_be_blocked(self):
#         logger.info('waiting for 10s to valid cfs configure...')
#         time.sleep(10)
#         searchv4_web_cmd = [
#             'echo '' > /tmp/test.txt',
#             f'curl --resolve *:443:{PC4_ETH1_IP} https://dns.baidu.com -k -o /tmp/test.txt',
#             'cat /tmp/test.txt'
#         ]
#         output = PC2_login.send_commands(searchv4_web_cmd)
#         logger.info(f'send cmds result: {output}')
#         output = logmonitorapi.get_log(id='14')
#         res = True if output else False
#         Assertion.assert_equal(res, True, "ERR: check cfs block log failed")
#
#
# class TestGAVIPSAntiSpyware_TC023(Test):
#     uuid = '1514006'
#     description = show_testcase_info(TESTPLAN, 'TC023', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC023')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_spyware_configure(self):
#         res = False
#         output = spywareapi.get_antispyware()
#         try:
#             if output['anti_spyware']['enable']:
#                 logger.info('check spyware is enabled successful.')
#                 signature_group = json.dumps(output['anti_spyware']['signature_group'])
#                 if signature_group.count('true') == 6:
#                     logger.info('check prevent and detect values all True successful.')
#                     res = True
#                 else:
#                     logger.info('check prevent and detect values all True failed.')
#             else:
#                 logger.info('check spyware enabled failed.')
#         except Exception as e:
#             logger.info(f'check spyware configure abnormal.')
#         Assertion.assert_equal(res, True, "ERR: check spyware configure failed")
#
#     def test_02_check_gav_configure(self):
#         output = gavapi.get_GAV_base()
#         Assertion.assert_regular(json.dumps(output), 'enable": True', "ERR: check gav configure failed")
#
#     def test_03_check_ips_configure(self):
#         output = ipsapi.get_IPS_global()
#         Assertion.assert_regular(json.dumps(output), 'enable": True', "ERR: check ips configure failed")
#
#
# class TestGAVIPSAntiSpyware_TC024(Test):
#     uuid = '1514007'
#     description = show_testcase_info(TESTPLAN, 'TC024', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC024')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     @repeat_method(5)
#     def test_03_spyware_block_from_wan_server(self):
#         logger.info('waiting for 10s to valid spyware configure...')
#         time.sleep(10)
#         searchv4_web_cmd = [
#             'echo '' > /tmp/spyware.txt',
#             f'curl https://{PC4_ETH1_IP}/spy_3_449.bin -k -o /tmp/spyware.txt',
#             'cat /tmp/spyware.txt'
#         ]
#         output = PC2_login.send_commands(searchv4_web_cmd)
#         msg = 'This request is blocked by the Firewall Anti-Spyware Service'
#         Assertion.assert_regular(output, msg, "ERR: spyware block from wan server failed.")
#
#     @repeat_method(5)
#     def test_03_gav_block_from_wan_server(self):
#         logger.info('waiting for 10s to valid gav configure...')
#         time.sleep(10)
#         searchv4_web_cmd = [
#             'echo '' > /tmp/gav.txt',
#             f'curl https://{PC4_ETH1_IP}/Exploit.VBS.Agent.q.gz -k -o /tmp/gav.txt',
#             'cat /tmp/gav.txt'
#         ]
#         output = PC2_login.send_commands(searchv4_web_cmd)
#         msg = 'This request is blocked by the Firewall Gateway Anti-Virus Service'
#         Assertion.assert_regular(output, msg, "ERR: gav block from wan server failed.")
#
#     @repeat_method(5)
#     def test_04_ips_block_from_wan_server(self):
#         logger.info('waiting for 10s to valid ips configure...')
#         time.sleep(10)
#         searchv4_web_cmd = [
#             'echo '' > /tmp/ips.txt',
#             f'curl --connect-timeout 5 https://{PC4_ETH1_IP}/IPS_5342_high_poc.xls -k -o /tmp/ips.txt',
#         ]
#         output = PC2_login.send_commands(searchv4_web_cmd)
#         msg = 'connection reset by peer'
#         Assertion.assert_regular(output, msg, "ERR: ips block from wan server failed.")
#
#
# class TestInterfacesZones_TC027(Test):
#     uuid = '1514010'
#     description = show_testcase_info(TESTPLAN, 'TC027', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC027')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_interface_configure(self):
#         res = False
#         output = interfaceapi.get_interface_status(name='X2')
#         if CaseParams.custom_zone_name in json.dumps(output) and Parameter.X2_IP in json.dumps(output):
#             res = True
#         Assertion.assert_equal(res, True, "ERR: check interface configure failed")
#
#     def test_02_check_zones_configure(self):
#         output = zonesapi.show_zone_object(name=CaseParams.custom_zone_name)
#         Assertion.assert_regular(json.dumps(output), CaseParams.custom_zone_name, "ERR: check zone configure failed")
#
#
# class TestInterfacesZones_TC028(Test):
#     uuid = '1514011'
#     description = show_testcase_info(TESTPLAN, 'TC028', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC028')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_disable_ips(self):
#         enable_ips_dict = {
#             "intrusion_prevention": {
#                 "enable": False,
#                 "signature_group": {
#                     "high_priority": {
#                         "detect_all": True,
#                         "log_redundancy": {},
#                         "prevent_all": True
#                     },
#                     "low_priority": {
#                         "detect_all": True,
#                         "log_redundancy": {
#                             "value": 60
#                         },
#                         "prevent_all": True
#                     },
#                     "medium_priority": {
#                         "detect_all": True,
#                         "log_redundancy": {},
#                         "prevent_all": True
#                     }
#                 }
#             }
#         }
#         output = ipsapi.config_IPS_global(**enable_ips_dict)
#         Assertion.assert_equal(output, True, "ERR: ips configure failed")
#
#     def test_02_config_route_to_pcs(self):
#         res = {}
#         logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
#         cmds = [f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.FIREWALL}',
#                 'ip -4 r']
#         output = PC2_login.send_commands(cmds)
#         res['pc2'] = True if f'{Parameter.X2_SUBNET}/24 via {Parameter.FIREWALL}' in output else False
#
#         logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
#         cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.X2_IP}',
#                 'ip -4 r']
#         output = PC3_login.send_commands(cmds)
#         res['pc3'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.X2_IP}' in output else False
#
#         logger.info(f'config pcs result: {res}')
#         Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
#
#     @repeat_method(5)
#     def test_03_check_ping_from_lan_to_custom_zone(self):
#         output = False
#         pc3ip = get_pc_eth_ip(pc=PC3_login, eth='eth1')
#         if pc3ip:
#             output = PC2_login.ping(pc3ip)
#         else:
#             logger.info('wait 10s to retry...')
#             time.sleep(10)
#         Assertion.assert_equal(output, True, "ERR: check ping failed")
#
#
# class TestNat_TC035(Test):
#     uuid = '1514018'
#     description = show_testcase_info(TESTPLAN, 'TC035', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC035')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_nat_configure(self):
#         output = natpolicyapi.get_nat_policy(name=CaseParams.custom_nat_name)
#         filter_list = [CaseParams.custom_nat_name, 'X1 IP', PC2_ETH1_IP]
#         res = [x in json.dumps(output) for x in filter_list]
#         logger.info(f'check custom nat policy: {res}')
#         Assertion.assert_equal(res.count(True), 3, "ERR: check nat configure failed")
#
#
# class TestNat_TC036(Test):
#     uuid = '1514019'
#     description = show_testcase_info(TESTPLAN, 'TC036', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC036')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_ping_from_wan_to_lan(self):
#         logger.info('waiting for 10s to valid configure...')
#         time.sleep(10)
#         output = PC4_login.ping(PC2_ETH1_IP)
#         Assertion.assert_equal(output, True, "ERR: check ping failed")
#
#
# class TestRoute_TC041(Test):
#     uuid = '1514024'
#     description = show_testcase_info(TESTPLAN, 'TC041', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC041')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_nat_configure(self):
#         output = routepolicyapi.get_route_policy_by_name(name=CaseParams.custom_route_name)
#         filter_list = [CaseParams.custom_route_name, 'X1', 'X1 Default Gateway', 'X2 Subnet', PC4_ETH1_IP]
#         res = [x in json.dumps(output) for x in filter_list]
#         logger.info(f'check custom nat policy: {res}')
#         Assertion.assert_equal(res.count(True), 5, "ERR: check route configure failed")
#
#
# class TestRoute_TC042(Test):
#     uuid = '1514025'
#     description = show_testcase_info(TESTPLAN, 'TC042', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TC042')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_0_check_ping_from_custom_to_wan_zone(self):
#         logger.info('waiting for 10s to valid configure...')
#         time.sleep(10)
#         output = PC3_login.ping(PC4_ETH1_IP)
#         Assertion.assert_equal(output, True, "ERR: check ping failed")
#
#
# class TestAccessrulesApprules_TC01(Test):
#     uuid = '2289266'
#     description = show_testcase_info(TESTPLAN, 'TCACL01', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TCACL01')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_access_rules_configure(self):
#         output = accessruleapi.get_accessrule_via_zones(srczone='WAN', dstzone='LAN')
#         Assertion.assert_regular(
#             json.dumps(output), CaseParams.custom_access_name, "ERR: check access rules configure failed")
#
#     def test_01_check_app_rules_configure(self):
#         output = appruleapi.get_apprule_object(name=CaseParams.custom_apprule_name)
#         Assertion.assert_regular(
#             json.dumps(output), CaseParams.custom_march_name, "ERR: check app rules configure failed")
#
#
# class TestAccessrulesApprules_TC02(Test):
#     uuid = '2289267'
#     description = show_testcase_info(TESTPLAN, 'TCACL02', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'TCACL02')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_ping_passed_from_wan_to_lan(self):
#         logger.info('waiting for 10s to valid configure...')
#         time.sleep(10)
#         output = PC4_login.ping(PC2_ETH1_IP)
#         Assertion.assert_equal(output, True, "ERR: check ping failed")
#
#     def test_02_enable_app_rules(self):
#         apprule_setting_dict = {
#             "enable": True,
#             "log_redundancy": {}
#         }
#         output = appruleapi.config_apprule_setting(**apprule_setting_dict)
#         Assertion.assert_equal(output, True, "ERR: enable app rule failed")
#
#     def test_03_check_app_rules_http_block_function(self):
#         logger.info('waiting for 10s to valid configure...')
#         time.sleep(10)
#         output = PC2_login.send_command(f'curl http://{PC4_ETH1_IP}')
#         msg = 'Connection reset by peer'
#         Assertion.assert_regular(output, msg, "ERR: check app rules http block failed")
#
#     def test_04_disable_app_rules(self):
#         apprule_setting_dict = {
#             "enable": False,
#             "log_redundancy": {}
#         }
#         output = appruleapi.config_apprule_setting(**apprule_setting_dict)
#         Assertion.assert_equal(output, True, "ERR: disable app rule failed")
#
#
# class TestDPISSL01(Test):
#     uuid = '2289268'
#     description = show_testcase_info(TESTPLAN, 'DPISSL01', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DPISSL01')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_dpissl_configure(self):
#         output = clientsslapi.show_dpissl_client()
#         filter_list = ['enable\': True',
#                        'intrusion_prevention\': True',
#                        'anti_virus\': True',
#                        'anti_spyware\': True',
#                        'content_filter\': True']
#         res = [x in str(output) for x in filter_list]
#         logger.info(f'check dpissl configure: {res}')
#         Assertion.assert_equal(res.count(True), 5, "ERR: check dpissl configure failed")
#
#
# class TestDPISSL02(Test):
#     uuid = '2289269'
#     description = show_testcase_info(TESTPLAN, 'DPISSL02', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DPISSL02')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_dpissl_function(self):
#         cmd = f'echo | openssl s_client -connect {PC4_ETH1_IP}:443 2>/dev/null'
#         logger.info(f'send cmd : {cmd}')
#         output = PC2_login.send_command(cmd)
#         Assertion.assert_regular(output, 'SonicWALL Firewall DPI-SSL', "ERR: check certificate failed")
#
#
# class TestDNS_TC021(Test):
#     uuid = '1514004'
#     description = show_testcase_info(TESTPLAN, 'DNS_TC021', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DNS_TC021')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_dns_configure(self):
#         output = dnssettingapi.get_dns()
#         filter_list = [Parameter.VALID_DNS, Parameter.FAKE_DNS1, Parameter.FAKE_DNS2]
#         res = [x in str(output) for x in filter_list]
#         logger.info(f'check dns configure: {res}')
#         Assertion.assert_equal(res.count(True), 3, "ERR: check dns configure failed")
#
#
# class TestDNS_TC022(Test):
#     uuid = '1514005'
#     description = show_testcase_info(TESTPLAN, 'DNS_TC022', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DNS_TC022')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_dns_functions(self):
#         output = diagapi.diag_dns_name_lookup(cmd="nslookup dns.baidu.com")
#         logger.info(f'nslookup dns.baidu.com result: {output}')
#         res = True if Parameter.VALID_DNS in str(output) else False
#         Assertion.assert_equal(res, True, "ERR: check DNS functions failed")
#
#
# class TestSyslog_TC063(Test):
#     uuid = '1514046'
#     description = show_testcase_info(TESTPLAN, 'Syslog_TC063', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Syslog_TC063')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_syslog_configure(self):
#         output = syslogsettingsapi.show_syslog_server()
#         Assertion.assert_regular(str(output), PC4_ETH1_IP, "ERR: check syslog configure failed")
#
#
# class TestSyslog_TC064(Test):
#     uuid = '1514047'
#     description = show_testcase_info(TESTPLAN, 'Syslog_TC066', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Syslog_TC064')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_syslog_function(self):
#         res = False
#         cmds = [
#             "echo '' > /var/log/messages",
#             'systemctl restart rsyslog',
#         ]
#         # clear syslog server msg
#         PC4_login.send_commands(cmds)
#         for count in range(5):
#             logger.info('wait 20s to get syslog msg...')
#             time.sleep(20)
#             output = PC4_login.send_commands(['cat /var/log/messages'])
#             if 'sonicwall.com' in output:
#                 logger.info('fw log upload to syslog server successful.')
#                 res = True
#                 break
#         else:
#             logger.info('can not find fw msg from suslog server.')
#         Assertion.assert_equal(res, True, "ERR: check syslog function failed")
#
#
# class TestTime_TC065(Test):
#     uuid = '1514048'
#     description = show_testcase_info(TESTPLAN, 'Time_TC065', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Time_TC065')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_time_configure(self):
#         res = False
#         output = timeapi.show_time()
#         try:
#             if output['time']['use_ntp'] and output['time']['time_zone'] == 'china,philippines':
#                 res = True
#         except Exception as e:
#             logger.info(f'get time configure fail.\n {e}')
#         Assertion.assert_equal(res, True, "ERR: check time configure failed")
#
#
# class TestTime_TC066(Test):
#     uuid = '1514049'
#     description = show_testcase_info(TESTPLAN, 'Time_TC066', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Time_TC066')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_time_function(self):
#         res = False
#         orgtime = timeapi.show_time()
#         time_dict = {
#             "time": {
#                 "use_ntp": True,
#                 "time_zone": "pacific-time",
#                 "daylight_savings": True,
#                 "only_custom_ntp": False,
#                 "ntp_update_interval": 30
#             }
#         }
#         changezone = timeapi.set_time(**time_dict)
#         logger.info(f'change time zone: {changezone}')
#         newtime = timeapi.show_time()
#         try:
#             new = newtime['time']['time']
#             old = orgtime['time']['time']
#             logger.info(f'new time: {new}, old time: {old}')
#             if new != old:
#                 res = True
#             else:
#                 logger.info(f'new time eq old time.')
#         except Exception as e:
#             logger.info({e})
#         Assertion.assert_equal(res, True, "ERR: check time function failed")
#
#
# class TestLogging_TC033(Test):
#     uuid = '1514016'
#     description = show_testcase_info(TESTPLAN, 'Logging_TC033', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Logging_TC033')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_logging_configure(self):
#         output = logsettingsapi.show_event(event_id='602')
#         Assertion.assert_regular(str(output), 'redundancy_interval\': 123', "ERR: check logging cofnigure failed")
#
#
# class TestLogging_TC034(Test):
#     uuid = '1514017'
#     description = show_testcase_info(TESTPLAN, 'Logging_TC034', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'Logging_TC034')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_logging_function(self):
#         output = logmonitorapi.get_log(id='602')
#         res = True if output else False
#         Assertion.assert_equal(res, True, "ERR: check logging function failed")
#
#
# class TestSNMP_TC067(Test):
#     uuid = '1514050'
#     description = show_testcase_info(TESTPLAN, 'SNMP_TC067', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'SNMP_TC067')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_snmp_configure(self):
#         output = snmpapi.show_snmp()
#         Assertion.assert_regular(str(output), 'enable\': True', "ERR: check snmp configure failed")
#
#
# class TestSNMP_TC068(Test):
#     uuid = '1514051'
#     description = show_testcase_info(TESTPLAN, 'SNMP_TC068', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'SNMP_TC068')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_snmp_function(self):
#         res = False
#         status = statusapi.show_status()
#         logger.info(f"{f' snmp monitor -sysDescr- result ':=^60}")
#         cmd = f'snmpwalk -v2c -cpublic -OQv {Parameter.X2_IP} sysDescr'
#         output = PC3_login.send_command(cmd)
#         if 'model' in status.keys():
#             logger.info(f'status model is {status["model"]}')
#             res = True if status['model'] in output else False
#         Assertion.assert_equal(res, True, f"ERR: Get snmp sysDescr failed!!")
#
#
# class TestDHCPServer_TC019(Test):
#     uuid = '1514002'
#     description = show_testcase_info(TESTPLAN, 'DHCP_TC019', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DHCP_TC019')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_check_dhcp_server_configure(self):
#         output = dhcpserverapi.get_dhcp_server_scope_dynamic()
#         filter_list = ['from": "192.168.2.80', 'to": "192.168.2.85', 'enable": true']
#         res = [x in json.dumps(output) for x in filter_list]
#         logger.info(f'check dhcp server configure: {res}')
#         Assertion.assert_equal(res.count(True), 3, "ERR: check dhcp server configure failed")
#
#
# class TestDHCPServer_TC020(Test):
#     uuid = '1514003'
#     description = show_testcase_info(TESTPLAN, 'DHCP_TC020', description=True)['title']
#
#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, 'DHCP_TC020')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")
#
#     def test_01_enable_dhcp_server(self):
#         dhcp_seting_dict['dhcp_server']['ipv4']['enable'] = True
#         output = dhcpserverapi.config_dhcp_server_settings(**dhcp_seting_dict)
#         Assertion.assert_equal(output, True, "ERR: enable dhcp server failed")
#
#     @repeat_method(5)
#     def test_02_get_dhcp_lease_in_pc2(self):
#         logger.info('waiting for 30s to valid dhcp server configure...')
#         time.sleep(30)
#         cmds = [
#             'cp /dev/null /etc/resolv.conf',
#             'rm -rf /var/lib/dhclient/dhclient.leases',
#         ]
#         PC2_login.send_commands(cmds)
#         res = get_ip_lease_in_pc(PC3_login, 'eth1')
#         Assertion.assert_equal(res, True, 'ERR: PC3 get dhcp lease from DUT failed')
#
#     def test_03_init_pc3_configure(self):
#         dhcp_seting_dict['dhcp_server']['ipv4']['enable'] = False
#         output1 = dhcpserverapi.config_dhcp_server_settings(**dhcp_seting_dict)
#         logger.info(f'disable dhcp server result: {output1}')
#
#         cmds = [
#             f'ifconfig eth1 {PC3_ETH1_IP}',
#             f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}',
#             'ip -4 r']
#         output2 = PC3_login.send_commands(cmds)
#         Assertion.assert_regular(output2, PC3_ETH1_IP, 'ERR: init pc3 configure failed')
#

