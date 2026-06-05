from definition.settings import *
from definition.utils import *


# verify every 120s vpn policy will re negotiate in main mode.
class TestBaseFunc_TC13(Test):
    uuid = "SOSAIOT-TC-54313"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_vpn_to_main(self):
        res = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_vpn_to_main(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_renegotiate_via_log(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        logger.info('waiting for 130s to renegotiated vpn...')
        time.sleep(130)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local vpn log failed.")

    def test_04_verify_ping_to_pc4_pass(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 5)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_05_verify_ftp_download_from_pc4(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)
        logger.info(f'check lan to vpn ftp download result: {output}')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# verify vpn policy will negotiate successful via ping in main mode.
class TestBaseFunc_TC14(Test):
    uuid = "SOSAIOT-TC-54314"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_vpn(self):
        res = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_vpn_to_main(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_ping_to_pc4_pass(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        logger.info('waiting for 10s to negotiated vpn...')
        time.sleep(10)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    @repeat_method(3)
    def test_04_renegotiate_tunnel_button_click(self):
        logger.info('waiting for 20s to renegotiated vpn...')
        time.sleep(20)
        res = l_vpnapi.Renegotiate_Tunnel_stats()
        Assertion.assert_equal(res, True, "ERR: click renegotiate tunnel button failed.")

    def test_05_verify_local_vpn_log(self):
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local IKE negotiation log failed.")

    def test_06_verify_ping_to_pc4(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify vpn policy re negotiated successful after disable/enable in main mode.
class TestBaseFunc_TC17(Test):
    uuid = "SOSAIOT-TC-54317"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_local_vpn(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        edit_localvpn_dict['enable'] = False
        res = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_02_verify_vpn_status_is_down(self):
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'down', "ERR: check local vpn status failed.")

    def test_03_verify_local_vpn_log(self):
        fw_logs = logapi.get_log(171)
        lists = ['SENDING', 'HASH', 'DEL']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local vpn log failed.")

    def test_04_verify_nogotiate_vpn_via_ping_must_failed(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

    def test_05_enable_local_vpn_policy(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        edit_localvpn_dict['enable'] = True
        res = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    @repeat_method(3)
    def test_06_start_nogotiate_vpn_via_ping_again(self):
        logger.info('waiting for 10s to negotiated vpn...')
        time.sleep(10)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_07_verify_IKE_negotiation_log_must_exist(self):
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "check local IKE negotiation log failed.")


# verify lan to vpn traffic passed after config pri gate to domain in main mode
class TestDomain_TC22(Test):
    uuid = "SOSAIOT-TC-54321"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']
    jira = 'GEN8-2784'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X1_dns(self):
        edit_dict = {'dns1': PC3_ETH1_IP}
        x1_dict = copy.deepcopy(x1_static_dict)
        x1_dict.update(edit_dict)
        res = interfaceapi.config_interface(**x1_dict)
        Assertion.assert_equal(res, True, "ERR: Config X1 dns failed")

    def test_02_config_local_vpn_domain(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'pri_gate': 'dns.test.com'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'config domain in local vpn policy result: {res}')
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_03_edit_remote_s2s_vpn_to_main(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_04_verify_local_vpn_status(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")

    def test_05_verify_ping_traffic(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify lan to vpn traffic passed after config destination network as a super net 172.16.0.0/16
class TestBaseFunc_TC35(Test):
    uuid = "SOSAIOT-TC-54332"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local_vpn_domain(self):
        ao_dict = {
            "object_type": "network",
            "name": "sub172.16.0.0",
            "zone": "LAN",
            "value": '172.16.0.0,255.255.0.0'
        }
        addaores = l_aoapi.config_addressobject(**ao_dict)
        logger.info(f'add ao result addaores: {addaores}')

        edit_dict = {'remote_net_name': 'sub172.16.0.0'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_02_edit_remote_s2s_vpn(self):
        ao_dict = {
            "object_type": "network",
            "name": "sub172.16.0.0",
            "zone": "LAN",
            "value": '172.16.0.0,255.255.0.0'
        }
        addaores = r_aoapi.config_addressobject(**ao_dict)
        logger.info(f'add ao result addaores: {addaores}')

        edit_dict = {'local_net_name': 'sub172.16.0.0'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_vpn_status(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")

    def test_04_verify_ping_traffic(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify dmz to vpn traffic passed in dmz sub
class TestBaseFunc_TC45(Test):
    uuid = "SOSAIOT-TC-54335"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_to_dmz(self):
        x2_dict = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_ping': True,
        }
        res = interfaceapi.config_interface(**x2_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to dmz failed")

    def test_02_config_local_vpn_domain(self):
        edit_dict = {'edit_network': True, 'local_net_name': 'X2 Subnet'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_03_edit_remote_s2s_vpn(self):
        ao_dict = {
            "object_type": "network",
            "name": "local_dmz_sub",
            "zone": "VPN",
            "value": f'{Parameter.X2_SUBNET},{Parameter.MASK}'
        }
        addaores = r_aoapi.config_addressobject(**ao_dict)
        logger.info(f'add ao result addaores: {addaores}')

        edit_dict = {'edit_network': True, 'remote_net_name': 'local_dmz_sub'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_04_verify_vpn_status(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")

    def test_05_verify_ping_traffic(self):
        output = PC2_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check dmz to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify vpn policy will be auto negotiation if VPN is re-enabled on the firewall
class TestBaseFunc_TC48(Test):
    uuid = "SOSAIOT-TC-54337"
    description = show_testcase_info(TESTPLAN, '48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_vpn(self):
        vpn_setting_dict = {'enable': False}
        editres = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        enableres = vpnsettingapi.config_vpnadvanced(**vpn_setting_dict)
        logger.info(f'disable vpn and edit policy result: enableres: {enableres}, editres: {editres}')
        Assertion.assert_equal(enableres & editres, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_vpn(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_ping_traffic_must_fail(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

    def test_04_enable_local_s2s_vpn_and_check_log(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        vpn_setting_dict = {'enable': True}
        enableres = vpnsettingapi.config_vpnadvanced(**vpn_setting_dict)
        logger.info(f'enable vpn result: {enableres}')

        fw_logs = logapi.get_log(507)
        Assertion.assert_regular(str(fw_logs), 'VPN enabled by administrator', 'ERR: check edit log event failed.')

    @repeat_method(3)
    def test_05_ping_traffic_must_pass(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_06_verify_vpn_status_is_up(self):
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        logger.info(f'check vpn status result: {res, info}')
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")


# verify vpn policy will use small lifetime to re-key while local < remote
class TestBaseFunc_TC49(Test):
    uuid = "SOSAIOT-TC-54338"
    description = show_testcase_info(TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_local_vpn_lifetime(self):
        edit_dict = {'edit_proposal': True, 'keep_alive': False, 'ike_lifetime': 180, 'ipsec_lifetime': 180}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_03_edit_remote_s2s_vpn_lifetime(self):
        edit_dict = {'edit_proposal': True, 'ike_lifetime': 300, 'ipsec_lifetime': 300}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)

        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    @repeat_method(3)
    def test_04_ping_traffic_in_300s(self):
        PC1_login.send_command(f'ping {PC4_ETH1_IP} -c 300 >/opt/ping.log &')
        logger.info('waiting for 5s to check ping...')
        time.sleep(10)
        output = PC1_login.send_command('cat /opt/ping.log')
        logger.info(f'check lan to vpn ping result: {output}')
        res = True if output.count('icmp_seq') > 3 else False
        Assertion.assert_equal(res, True, "ERR: verify ping traffic failed")

    def test_05_verify_vpn_status_and_renegotiation_time(self):
        output = False
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        logger.info(f'check vpn status result: {res, info}')
        if info == 'up':
            output1 = l_vpnapi.get_Tunnel_stats_status()
            basetime = time.strptime(output1['createTm'], '%m/%d/%Y %H:%M:%S')
            logger.info('start wait 180s to get re negotiation time')
            time.sleep(180)
            output2 = l_vpnapi.get_Tunnel_stats_status()
            newtime = time.strptime(output2['createTm'], '%m/%d/%Y %H:%M:%S')
            logger.info(f'old time: {output1["createTm"]}, new time: {output2["createTm"]}')
            output = True if newtime > basetime else False
        Assertion.assert_equal(output, True, "ERR: check local vpn status and log failed.")

    def test_06_check_local_vpn_lifetime_in_log(self):
        fw_logs = logapi.get_log(353)
        Assertion.assert_regular(str(fw_logs), 'lifetime=180 secs', "ERR: check lifetime log event failed.")


# verify vpn policy still use small lifetime to re-key while local > remote
class TestBaseFunc_TC50(Test):
    uuid = "SOSAIOT-TC-54339"
    description = show_testcase_info(TESTPLAN, '50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_local_vpn_lifetime(self):
        edit_dict = {'edit_proposal': True, 'keep_alive': False, 'ike_lifetime': 300, 'ipsec_lifetime': 300}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_03_edit_remote_s2s_vpn_lifetime(self):
        edit_dict = {'edit_proposal': True, 'ike_lifetime': 180, 'ipsec_lifetime': 180}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_04_ping_traffic_for_300s(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        PC1_login.send_command(f'ping {PC4_ETH1_IP} -c 300 >/opt/ping.log &')
        time.sleep(5)
        output = PC1_login.send_command('cat /opt/ping.log')
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_regular(output, 'icmp_seq=5', "ERR: verify ping traffic failed")

    @repeat_method(3)
    def test_05_verify_vpn_status_and_renegotiation_time(self):
        output = False
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        logger.info(f'check vpn status result: {res, info}')
        if info == 'up':
            output1 = l_vpnapi.get_Tunnel_stats_status()
            basetime = time.strptime(output1['createTm'], '%m/%d/%Y %H:%M:%S')
            logger.info('start wait 180s to get re negotiation time')
            time.sleep(180)
            output2 = l_vpnapi.get_Tunnel_stats_status()
            newtime = time.strptime(output2['createTm'], '%m/%d/%Y %H:%M:%S')
            logger.info(f'old time: {output1["createTm"]}, new time: {output2["createTm"]}')
            output = True if newtime > basetime else False
        Assertion.assert_equal(output, True, "ERR: check local vpn status and log failed.")

    def test_06_verify_ping_traffic(self):
        logger.info('waiting for 10s to negotiated vpn...')
        time.sleep(10)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify every 120s vpn policy will re negotiate in aggressive mode.
class TestBaseFunc_TC24(Test):
    uuid = "SOSAIOT-TC-54323"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local_vpn_domain(self):
        edit_dict = {'edit_proposal': True, 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'config domain in local vpn policy result: {res}')
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_02_config_remote_vpn_domain(self):
        edit_dict = {'edit_proposal': True, 'ike_exchange': 'aggressive'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config remote vpn failed.")

    @repeat_method(5)
    def test_03_verify_ping_traffic(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_04_verify_ftp_traffic(self):
        my_ftp.login()
        output = my_ftp.download_file(localfile, remotefile)
        logger.info(f'check lan to vpn ftp download result: {output}')
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')


# verify vpn policy will negotiate successful via ping in aggressive mode.
class TestBaseFunc_TC25(Test):
    uuid = "SOSAIOT-TC-54324"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local_vpn_domain(self):
        edit_dict = {'edit_proposal': True, 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'config domain in local vpn policy result: {res}')
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_02_config_remote_vpn_domain(self):
        edit_dict = {'edit_proposal': True, 'ike_exchange': 'aggressive'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)

        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')
        Assertion.assert_equal(res, True, "ERR: config remote vpn failed.")

    @repeat_method(5)
    def test_03_renegotiate_tunnel_button_click(self):
        vpn_raw = {
            "local_net": Parameter.LOCAL_X0_NET,
            "local_mask": Parameter.MASK,
            "remote_net": Parameter.REMOTE_X0_NET,
            "remote_mask": Parameter.MASK,
            "remote_gw": Parameter.REMOTE_X1_IP,
        }
        logger.info('waiting for 20s to auto negotiated vpn...')
        time.sleep(20)
        output = l_vpnapi.Renegotiate_VPN_Tunnel(**vpn_raw)
        Assertion.assert_equal(output, True, "ERR: renegotiate vpn tunnel failed")

    def test_04_verify_vpn_status(self):
        logger.info('waiting for 20s to auto renegotiated vpn...')
        time.sleep(20)
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")

    def test_05_verify_IKE_negotiation_log(self):
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local IKE negotiation log failed.")

    def test_06_verify_ping_traffic(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


# verify vpn policy re negotiated successful after disable/enable in aggressive mode.
class TestBaseFunc_TC28(Test):
    uuid = "SOSAIOT-TC-54327"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_nogotiate_via_ping(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_02_disable_local_vpn(self):
        edit_dict = {'edit_proposal': True, 'keep_alive': False, 'enable': False, 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_verify_vpn_status_is_down(self):
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'down', "ERR: check local vpn status failed.")

    def test_04_check_IKE_del_log_must_exist(self):
        time.sleep(5)
        fw_logs = logapi.get_log(171)
        lists = ['SENDING', 'HASH', 'DEL']
        output = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(output, True, "ERR: check local IKE del log failed.")

    def test_05_verify_nogotiate_vpn_via_ping_must_failed(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

    def test_06_enable_local_vpn_policy(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        edit_dict = {'edit_proposal': True, 'keep_alive': False, 'enable': True, 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    @repeat_method(5)
    def test_07_start_nogotiate_vpn_via_ping_and_check_log_again(self):
        logger.info('waiting for 10s to renegotiated vpn...')
        time.sleep(10)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        if not output:
            cmds = [f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.FIREWALL}']
            PC1_login.send_commands(cmds)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic and log failed")

    def test_08_check_aggressive_log_again(self):
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        output = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(output, True, "ERR: verify ping traffic and log failed")


# verify lan to vpn traffic passed after config pri gate to domain in aggressive mode
class TestDomain_TC33(Test):
    uuid = "SOSAIOT-TC-54331"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local_vpn_domain(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'pri_gate': 'dns.test.com', 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'config domain in local vpn policy result: {res}')
        Assertion.assert_equal(res, True, "ERR: config domain in local failed.")

    def test_02_config_remote_vpn_domain(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'ike_exchange': 'aggressive'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        Assertion.assert_equal(res, True, "ERR: config remote vpn failed.")

    @repeat_method(5)
    def test_03_verify_vpn_status(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        (res, info) = l_vpnapi.get_vpn_status(edit_localvpn_dict['name'])
        Assertion.assert_equal(info, 'up', "ERR: check local vpn status failed.")

    def test_04_verify_ping_traffic(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")


class TestNETBIOS_TC20(Test):
    uuid = "SOSAIOT-TC-54319"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_route_for_pc5_pc6(self):
        cmds = [f'/usr/local/staf/bin/staf {PC5_ETH0_IP} process start shell command '
                f'route add {Parameter.REMOTE_X0_NET} mask {Parameter.MASK} {Parameter.FIREWALL}',
                ]
        routeres1 = PC1_login.send_commands(cmds)
        cmds = [f'/usr/local/staf/bin/staf {PC6_ETH0_IP} process start shell command '
                f'route add {Parameter.LOCAL_X0_NET} mask {Parameter.MASK} {Parameter.REMOTE_X0_IP}',
                ]
        routeres2 = PC4_login.send_commands(cmds)
        res = True if routeres1 and routeres2 else False
        Assertion.assert_equal(res, True, "ERR: add route for pc5 pc6 failed")

    def test_02_config_local_vpn_netbios(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'netbios': True}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'enable netbios in local vpn policy result: {res}')

        enable_netbios_dict = {'protocol': 'NetBIOS', 'enable': True}
        enableconfig = iphelperapi.enable_iphelper()
        netbiosconfig = iphelperapi.edit_iphelper_protocol(**enable_netbios_dict)
        logger.info(f'enable iphelper and netbios protocol in local result: {enableconfig}, {netbiosconfig}')
        Assertion.assert_equal(res & enableconfig & netbiosconfig, True, "ERR: config netbios in local failed.")

    def test_03_config_remote_vpn_netbios(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'netbios': True}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        logger.info(f'enable netbios in remote vpn policy result: {res}')

        enable_netbios_dict = {'protocol': 'NetBIOS', 'enable': True}
        enableconfig = r_iphelperapi.enable_iphelper()
        netbiosconfig = r_iphelperapi.edit_iphelper_protocol(**enable_netbios_dict)
        logger.info(f'enable iphelper and netbios protocol in remote result: {enableconfig}, {netbiosconfig}')
        Assertion.assert_equal(res & enableconfig & netbiosconfig, True, "ERR: config netbios in remote failed.")

    @repeat_method(3)
    def test_04_check_netbios_traffic_form_local_to_remote(self):
        logger.info('start capture netbios traffic in FW...')
        time.sleep(20)
        cmd = f'/usr/local/staf/bin/staf {PC5_ETH0_IP} process start shell command nbtstat -a {PC6_ETH0_IP}'
        netbios_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmd': cmd,
            'packet': 'pcapng'
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC4_login, netbios_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')

        logger.info('start filter the netbios response packet in pcapng')
        tshark_filter = {'src': PC6_ETH0_IP, 'dst': PC5_ETH0_IP}
        reqres = check_nbstat_query_in_pcapng(PC1_login, tshark_filter)
        Assertion.assert_equal(reqres, True, "ERR: check netbios traffic in FW failed")


# verify netbios traffic passed between local vpn sub on remote vpn sub in aggressive mode.
class TestNETBIOS_TC31(Test):
    uuid = "SOSAIOT-TC-54329"
    description = show_testcase_info(TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_local_vpn_netbios(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'netbios': True, 'ike_exchange': 'aggressive'}
        local_vpn_dict = copy.deepcopy(edit_localvpn_dict)
        local_vpn_dict.update(edit_dict)
        res = l_vpnapi.edit_vpn_policy(**local_vpn_dict)
        logger.info(f'enable netbios in local vpn policy result: {res}')

        enable_netbios_dict = {'protocol': 'NetBIOS', 'enable': True}
        enableconfig = iphelperapi.enable_iphelper()
        netbiosconfig = iphelperapi.edit_iphelper_protocol(**enable_netbios_dict)
        logger.info(f'enable iphelper and netbios protocol in local result: {enableconfig}, {netbiosconfig}')
        Assertion.assert_equal(res & enableconfig & netbiosconfig, True, "ERR: config netbios in local failed.")

    def test_02_config_remote_vpn_netbios(self):
        edit_dict = {'enable': True, 'keep_alive': True, 'netbios': True, 'ike_exchange': 'aggressive'}
        remote_vpn_dict = copy.deepcopy(edit_remotevpn_dict)
        remote_vpn_dict.update(edit_dict)
        res = r_vpnapi.edit_vpn_policy(**remote_vpn_dict)
        logger.info(f'enable netbios in remote vpn policy result: {res}')

        enable_netbios_dict = {'protocol': 'NetBIOS', 'enable': True}
        enableconfig = r_iphelperapi.enable_iphelper()
        netbiosconfig = r_iphelperapi.edit_iphelper_protocol(**enable_netbios_dict)
        logger.info(f'enable iphelper and netbios protocol in remote result: {enableconfig}, {netbiosconfig}')
        Assertion.assert_equal(res & enableconfig & netbiosconfig, True, "ERR: config netbios in remote failed.")

    def test_03_check_netbios_traffic_form_local_to_remote(self):
        logger.info('start capture netbios traffic in FW...')
        cmd = f'/usr/local/staf/bin/staf {PC5_ETH0_IP} process start shell command nbtstat -a {PC6_ETH0_IP}'
        netbios_dict = {
            'type': 'cmd',  # ping, cmd, http,script
            'cmd': cmd,
            'packet': 'pcapng'
        }
        (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC4_login, netbios_dict)
        logger.info(f'http request result: {digres}')
        logger.info(f'packets captured on FW result: {packets}')

        logger.info('start filter the netbios response packet in pcapng')
        tshark_filter = {'src': PC6_ETH0_IP, 'dst': PC5_ETH0_IP}
        reqres = check_nbstat_query_in_pcapng(PC1_login, tshark_filter)
        Assertion.assert_equal(reqres, True, "ERR: check netbios traffic in FW failed")


# verify when enable dpd, vpn policy will down after down local x1.
class Testsettings_TC60(Test):
    uuid = '1529926'
    description = show_testcase_info(TESTPLAN, '60', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '60')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_local_s2s_vpn(self):
        res = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit local vpn policy failed.")

    def test_02_edit_remote_s2s_vpn_to_main(self):
        res = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res, True, "ERR: edit remote vpn policy failed.")

    def test_03_edit_dpd_interval(self):
        dpd_dict = {'dpd_interval': '5'}
        res = vpnsettingapi.config_vpnadvanced(**dpd_dict)
        Assertion.assert_equal(res, True, "ERR: edit dpd interval failed.")

    def test_04_down_x1_and_not_DPD_packet_response_check(self):
        res = False
        downres = interfaceapi.disable_interface('X1')
        if downres:
            sleep_dict = {
                'type': 'sleep',
                'time': 15,
            }
            (digres, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, sleep_dict)
            logger.info(f'http request result: {digres}')
            logger.info(f'packets captured on FW result: {packets}')
            filter_list = ['IP Type: UDP', f'Src=[{Parameter.REMOTE_X1_IP}]', f'Dst=[{Parameter.X1_IP}]',
                           'Src=[500]', 'Dst=[500]']
            (res, packet) = check_capture_packets(packets, filter_list)
            logger.info(f'filter packet: {packet}')
        else:
            logger.info('down local fw x1 in openstack fail.')
        Assertion.assert_equal(res, False, "ERR: disable local x1 and not dpd packet response check failed.")

    def test_05_verify_nogotiate_vpn_via_ping_must_failed(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 10)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, False, "ERR: verify ping traffic failed")

    def test_06_up_local_x1(self):
        output = interfaceapi.enable_interface('X1')
        Assertion.assert_equal(output, True, "ERR: up local x1 failed")


# verify that peer_ike_id will be modified in all per peer gateway VPN policies
class Testsettings_TC72(Test):
    uuid = '1529931'
    description = show_testcase_info(TESTPLAN, '72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_two_local_s2s_vpn(self):
        local_ao_dict1 = {
            "object_type": "network",
            "name": "test_vpn_net1",
            "zone": "VPN",
            "value": '66.66.66.0,255.255.255.0'
        }
        local_ao_dict2 = {
            "object_type": "network",
            "name": "test_vpn_net2",
            "zone": "VPN",
            "value": '77.77.77.0,255.255.255.0'
        }

        addaores1 = l_aoapi.config_addressobject(**local_ao_dict1)
        addaores2 = l_aoapi.config_addressobject(**local_ao_dict2)
        addvpnres1 = l_vpnapi.add_vpn_policy(**tc72_vpn_dict)
        tc72_vpn_dict.update({'name': 'tc72_modify_test2', 'remote_net_name': 'test_vpn_net2'})
        addvpnres2 = l_vpnapi.add_vpn_policy(**tc72_vpn_dict)
        logger.info(f'addaores1: {addaores1}, addaores2: {addaores2}, '
                    f'addvpnres1: {addvpnres1}', f'addvpnres2: {addvpnres2}')
        vpnentry = l_vpnapi.show_s2svpnpolicy()
        namecheck = re.findall('tc72_modify_test\d', str(vpnentry))
        Assertion.assert_equal(len(namecheck), 2, "ERR: Add 2 local vpn policy failed.")

    def test_02_edit_remote_ike_id_and_check_other_policy(self):
        vpn_dict = {
            'name': 'tc72_modify_test2',
            'edit_auth': True,
            'peer_ike_id': '36.36.36.36',
        }
        tc72_vpn_dict.update(vpn_dict)
        editres = l_vpnapi.edit_vpn_policy(**tc72_vpn_dict)
        logger.info(f'edit remote ike id: {editres}')
        vpnentry = l_vpnapi.show_s2svpnpolicy()
        checkres = re.findall(tc72_vpn_dict['peer_ike_id'], str(vpnentry))
        Assertion.assert_equal(len(checkres), 2, "ERR: check shared secret failed.")


# verify that policy bound to will be modified in all per peer gateway VPN policies
class Testsettings_TC88(Test):
    uuid = '1529937'
    description = show_testcase_info(TESTPLAN, '88', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '88')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_bound_to_and_check_other_policy(self):
        vpn_dict = {
            'name': 'tc72_modify_test2',
            'edit_advanced': True,
            'bound_to': ['interface', 'X2'],
        }
        tc72_vpn_dict.update(vpn_dict)
        editres = l_vpnapi.edit_vpn_policy(**tc72_vpn_dict)
        logger.info(f'edit bound to: {editres}')
        vpnentry = l_vpnapi.show_s2svpnpolicy()
        checkres = re.findall('interface\': \'X2', str(vpnentry))
        Assertion.assert_equal(len(checkres), 2, "ERR: check shared secret failed.")


# check Gateway/Destinations/Crypto
class Testsettings_TC116(Test):
    uuid = "SOSAIOT-TC-54311"
    description = show_testcase_info(TESTPLAN, '116', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '116')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_bound_to_and_check_other_policy(self):
        res = []
        check_list = [
            [Parameter.REMOTE_X1_IP, 'remote_vpn_net', 'main', 'aes_256', 'sha-256'],
            [tc72_vpn_dict['pri_gate'], 'test_vpn_net1', 'main', 'aes_256', 'sha-256'],
            [tc72_vpn_dict['pri_gate'], 'test_vpn_net2', 'main', 'aes_256', 'sha-256'],
        ]
        vpnentry = l_vpnapi.show_s2svpnpolicy()
        try:
            for policy in vpnentry['vpn']['policy']:
                for check in check_list:
                    filterres = [x in str(policy) for x in check]
                    logger.info(f'{check}: {filterres}')
                    if all(filterres):
                        res.append(True)
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res.count(True), 3, "ERR: check Gateway/Destinations/Crypto failed.")

    def test_02_del_local_s2s_vpn(self):
        res1 = l_vpnapi.del_s2svpn_policy(**{'name': 'tc72_modify_test1'})
        res2 = l_vpnapi.del_s2svpn_policy(**{'name': 'tc72_modify_test2'})
        Assertion.assert_equal(res1 & res2, True, "ERR: del local vpn policy failed.")


# verify acl between lan with vpn will show.
class Testsettings_TC94(Test):
    uuid = "SOSAIOT-TC-54341"
    description = show_testcase_info(TESTPLAN, '94', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '94')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_s2s_vpn_policy(self):
        vpn_dict = {
            'edit_network': True,
            'local_net_type': 'group',
            'local_net_group': 'LAN Subnets',
        }
        edit_localvpn_dict.update(vpn_dict)
        editres = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(editres, True, "ERR: edit s2s vpn failed.")

    def test_02_check_acl_from_lan_to_vpn(self):
        res = False
        lantovpn = accessruleapi.get_accessrule_via_zones(srczone='LAN', dstzone='VPN')
        try:
            for acl in lantovpn['access_rules']:
                if 'LAN Subnets' in str(acl) and 'remote_vpn_net' in str(acl):
                    res = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res, True, "ERR: check lan to vpn acl failed.")

    def test_03_check_acl_from_vpn_to_lan(self):
        res = False
        vpntolan = accessruleapi.get_accessrule_via_zones(srczone='VPN', dstzone='LAN')
        try:
            for acl in vpntolan['access_rules']:
                if 'LAN Subnets' in str(acl) and 'remote_vpn_net' in str(acl):
                    res = True
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(res, True, "ERR: check vpn to lan failed.")


# verify special characters can be set.
class Testsettings_TC107(Test):
    uuid = "SOSAIOT-TC-54305"
    description = show_testcase_info(TESTPLAN, '107', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '107')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_s2s_vpn_in_special_characters(self):
        vpn_dict = {
            'edit_auth': True,
            'secret': '=><+.!@#$%^&*-_("',
        }
        edit_localvpn_dict.update(vpn_dict)
        editres = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(editres, True, "ERR: edit s2s vpn failed.")

    def test_02_init_s2s_vpn(self):
        vpn_dict = {
            'edit_auth': True,
            'secret': '123456',
        }
        edit_localvpn_dict.update(vpn_dict)
        editres = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        Assertion.assert_equal(editres, True, "ERR: edit s2s vpn failed.")


#  Change the IKE preshared secrets of active VPN tunnel, check VPN tunnel status
class Testsettings_TC102(Test):
    uuid = "SOSAIOT-TC-54301"
    description = show_testcase_info(TESTPLAN, '102', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '102')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_s2s_vpn_not_keep_alive(self):
        vpn_dict = {
            'keep_alive': False,
            'netbios': False,
        }
        edit_localvpn_dict.update(vpn_dict)
        res1 = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        edit_remotevpn_dict.update(vpn_dict)
        res2 = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: edit s2s vpn failed.")

    def test_02_verify_nogotiate_vpn_via_ping(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")

    def test_03_change_s2s_vpn_preshared_secret(self):
        clearlog = logapi.clear_log()
        logger.info(f'clear log result: {clearlog}')

        vpn_dict = {'secret': 'newsecret12345'}
        edit_localvpn_dict.update(vpn_dict)
        res1 = l_vpnapi.edit_vpn_policy(**edit_localvpn_dict)
        edit_remotevpn_dict.update(vpn_dict)
        res2 = r_vpnapi.edit_vpn_policy(**edit_remotevpn_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: edit s2s vpn failed.")

    @repeat_method(3)
    def test_04_verify_renegotiate_via_log(self):
        logger.info('waiting for 20s to negotiated vpn...')
        time.sleep(20)
        fw_logs = logapi.get_log(89)
        lists = ['IKE negotiation complete', 'localvpn', 'Lifetime=120']
        res = all(x in str(fw_logs) for x in lists)
        Assertion.assert_equal(res, True, "ERR: check local vpn log failed.")

    def test_05_verify_nogotiate_vpn_via_ping(self):
        output = PC1_login.ping_from_eth(PC4_ETH1_IP, 'eth1', 20)
        logger.info(f'check lan to vpn ping result: {output}')
        Assertion.assert_equal(output, True, "ERR: verify ping traffic failed")
