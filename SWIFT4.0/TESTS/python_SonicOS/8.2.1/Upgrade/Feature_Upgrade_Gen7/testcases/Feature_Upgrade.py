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

    def test_01_cfs_configure(self):
        output = fwconfigure.cfs_configure()
        Assertion.assert_equal(output, True, "ERR: cfs configure failed")

    def test_02_spyware_configure(self):
        output = fwconfigure.spyware_configure()
        Assertion.assert_equal(output, True, "ERR: spyware configure failed")

    def test_03_gav_configure(self):
        output = fwconfigure.gav_configure()
        Assertion.assert_equal(output, True, "ERR: gav configure failed")

    def test_04_ips_configure(self):
        output = fwconfigure.ips_configure()
        Assertion.assert_equal(output, True, "ERR: ips configure failed")

    def test_05_zones_configure(self):
        output = fwconfigure.zones_configure()
        Assertion.assert_equal(output, True, "ERR: zones configure failed")

    def test_07_nat_configure(self):
        output = fwconfigure.nat_configure()
        Assertion.assert_equal(output, True, "ERR: nat configure failed")

    def test_08_route_configure(self):
        output = fwconfigure.route_configure()
        Assertion.assert_equal(output, True, "ERR: route configure failed")

    def test_09_access_rules_configure(self):
        output = fwconfigure.access_rules_configure()
        Assertion.assert_equal(output, True, "ERR: access rules configure failed")

    def test_10_app_rules_configure(self):
        output = fwconfigure.app_rules_configure()
        Assertion.assert_equal(output, True, "ERR: app rules configure failed")

    def test_11_dns_configure(self):
        output = fwconfigure.dns_configure()
        Assertion.assert_equal(output, True, "ERR: dns configure failed")

    def test_12_syslog_configure(self):
        output = fwconfigure.syslog_configure()
        Assertion.assert_equal(output, True, "ERR: syslog configure failed")

    def test_13_time_configure(self):
        output = fwconfigure.time_configure()
        Assertion.assert_equal(output, True, "ERR: time configure failed")

    def test_14_logging_configure(self):
        output = fwconfigure.logging_configure()
        Assertion.assert_equal(output, True, "ERR: logging configure failed")

    def test_15_snmp_configure(self):
        output = fwconfigure.snmp_configure()
        Assertion.assert_equal(output, True, "ERR: snmp configure failed")

    def test_16_dhcp_server_configure(self):
        output = fwconfigure.dhcp_server_configure()
        Assertion.assert_equal(output, True, "ERR: dhcp_server_configure failed")

    def test_17_interface_configure(self):
        output = fwconfigure.interface_configure()
        Assertion.assert_equal(output, True, "ERR: interface configure failed")



class Test_UpgradeUnderTestFirmwareViaUI(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_upgrade_under_test_firmware(self):
        upgraderes = upgrade_firewall_software(path=Parameter.testbuild, bulidtype='new')
        Assertion.assert_equal(upgraderes, True, "ERR: upgrade the under test firmware failed")


class TestCFS_TC015(Test):
    uuid = "SOSAIOT-TC-74746"
    description = show_testcase_info(TESTPLAN, 'CFS_TC015', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'CFS_TC015')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_cfs_configure(self):
        output1 = cfoobjectapi.get_cfo_object()
        res1 = True if 'baidu.com' in json.dumps(output1) else False
        output2 = cfoprofileapi.get_cfo_profile()
        res2 = True if 'auto_cfs_object_01' in json.dumps(output2) else False
        logger.info(f'check cfo object result: {res1}, check profile result: {res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: cfs configure check failed")


class TestCFS_TC016(Test):
    uuid = "SOSAIOT-TC-74747"
    description = show_testcase_info(TESTPLAN, 'CFS_TC016', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'CFS_TC016')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_01_access_https_site_must_be_blocked(self):
        logger.info('waiting for 10s to valid cfs configure...')
        time.sleep(10)
        searchv4_web_cmd = [
            'echo '' > /tmp/test.txt',
            f'curl --resolve *:443:{PC4_ETH1_IP} https://dns.baidu.com -k -o /tmp/test.txt',
            'cat /tmp/test.txt'
        ]
        output = PC2_login.send_commands(searchv4_web_cmd)
        logger.info(f'send cmds result: {output}')
        output = logmonitorapi.get_log(id='14')
        res = True if output else False
        Assertion.assert_equal(res, True, "ERR: check cfs block log failed")


class TestGAVIPSAntiSpyware_TC023(Test):
    uuid = "SOSAIOT-TC-74754"
    description = show_testcase_info(TESTPLAN, 'TC023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC023')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_spyware_configure(self):
        res = False
        output = spywareapi.get_antispyware()
        try:
            if output['anti_spyware']['enable']:
                logger.info('check spyware is enabled successful.')
                signature_group = json.dumps(output['anti_spyware']['signature_group'])
                if signature_group.count('true') == 6:
                    logger.info('check prevent and detect values all True successful.')
                    res = True
                else:
                    logger.info('check prevent and detect values all True failed.')
            else:
                logger.info('check spyware enabled failed.')
        except Exception as e:
            logger.info(f'check spyware configure abnormal.')
        Assertion.assert_equal(res, True, "ERR: check spyware configure failed")

    def test_02_check_gav_configure(self):
        output = gavapi.get_GAV_base()
        Assertion.assert_regular(json.dumps(output), 'enable": True', "ERR: check gav configure failed")

    def test_03_check_ips_configure(self):
        output = ipsapi.get_IPS_global()
        Assertion.assert_regular(json.dumps(output), 'enable": True', "ERR: check ips configure failed")


class TestGAVIPSAntiSpyware_TC024(Test):
    uuid = "SOSAIOT-TC-74755"
    description = show_testcase_info(TESTPLAN, 'TC024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_03_spyware_block_from_wan_server(self):
        logger.info('waiting for 10s to valid spyware configure...')
        time.sleep(10)
        searchv4_web_cmd = [
            'echo '' > /tmp/spyware.txt',
            f'curl https://{PC4_ETH1_IP}/spy_3_449.bin -k -o /tmp/spyware.txt',
            'cat /tmp/spyware.txt'
        ]
        output = PC2_login.send_commands(searchv4_web_cmd)
        msg = 'This request is blocked by the Firewall Anti-Spyware Service'
        Assertion.assert_regular(output, msg, "ERR: spyware block from wan server failed.")

    @repeat_method(5)
    def test_03_gav_block_from_wan_server(self):
        logger.info('waiting for 10s to valid gav configure...')
        time.sleep(10)
        searchv4_web_cmd = [
            'echo '' > /tmp/gav.txt',
            f'curl https://{PC4_ETH1_IP}/Exploit.VBS.Agent.q.gz -k -o /tmp/gav.txt',
            'cat /tmp/gav.txt'
        ]
        output = PC2_login.send_commands(searchv4_web_cmd)
        msg = 'This request is blocked by the Firewall Gateway Anti-Virus Service'
        Assertion.assert_regular(output, msg, "ERR: gav block from wan server failed.")

    @repeat_method(5)
    def test_04_ips_block_from_wan_server(self):
        logger.info('waiting for 10s to valid ips configure...')
        time.sleep(10)
        searchv4_web_cmd = [
            'echo '' > /tmp/ips.txt',
            f'curl --connect-timeout 5 https://{PC4_ETH1_IP}/IPS_5342_high_poc.xls -k -o /tmp/ips.txt',
        ]
        output = PC2_login.send_commands(searchv4_web_cmd)
        msg = 'connection reset by peer'
        Assertion.assert_regular(output, msg, "ERR: ips block from wan server failed.")


class TestInterfacesZones_TC027(Test):
    uuid = "SOSAIOT-TC-74758"
    description = show_testcase_info(TESTPLAN, 'TC027', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC027')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_interface_configure(self):
        res = False
        output = interfaceapi.get_interface_status(name='X2')
        if CaseParams.custom_zone_name in json.dumps(output) and Parameter.X2_IP in json.dumps(output):
            res = True
        Assertion.assert_equal(res, True, "ERR: check interface configure failed")

    def test_02_check_zones_configure(self):
        output = zonesapi.show_zone_object(name=CaseParams.custom_zone_name)
        Assertion.assert_regular(json.dumps(output), CaseParams.custom_zone_name, "ERR: check zone configure failed")


class TestInterfacesZones_TC028(Test):
    uuid = "SOSAIOT-TC-74759"
    description = show_testcase_info(TESTPLAN, 'TC028', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC028')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_ips(self):
        enable_ips_dict = {
            "intrusion_prevention": {
                "enable": False,
                "signature_group": {
                    "high_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    },
                    "low_priority": {
                        "detect_all": True,
                        "log_redundancy": {
                            "value": 60
                        },
                        "prevent_all": True
                    },
                    "medium_priority": {
                        "detect_all": True,
                        "log_redundancy": {},
                        "prevent_all": True
                    }
                }
            }
        }
        output = ipsapi.config_IPS_global(**enable_ips_dict)
        Assertion.assert_equal(output, True, "ERR: ips configure failed")

    def test_02_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X2_SUBNET}/24 via {Parameter.FIREWALL}' in output else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC3_login.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.X2_IP}' in output else False

        logger.info(f'config pcs result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")

    @repeat_method(5)
    def test_03_check_ping_from_lan_to_custom_zone(self):
        output = False
        pc3ip = get_pc_eth_ip(pc=PC3_login, eth='eth1')
        if pc3ip:
            output = PC2_login.ping(pc3ip)
        else:
            logger.info('wait 10s to retry...')
            time.sleep(10)
        Assertion.assert_equal(output, True, "ERR: check ping failed")


class TestNat_TC035(Test):
    uuid = "SOSAIOT-TC-74766"
    description = show_testcase_info(TESTPLAN, 'TC035', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC035')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_nat_configure(self):
        output = natpolicyapi.get_nat_policy(name=CaseParams.custom_nat_name)
        filter_list = [CaseParams.custom_nat_name, 'X1 IP', PC2_ETH1_IP]
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check custom nat policy: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check nat configure failed")


class TestNat_TC036(Test):
    uuid = "SOSAIOT-TC-74767"
    description = show_testcase_info(TESTPLAN, 'TC036', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC036')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ping_from_wan_to_lan(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC4_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: check ping failed")


class TestRoute_TC041(Test):
    uuid = "SOSAIOT-TC-74772"
    description = show_testcase_info(TESTPLAN, 'TC041', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC041')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_nat_configure(self):
        output = routepolicyapi.get_route_policy_by_name(name=CaseParams.custom_route_name)
        filter_list = [CaseParams.custom_route_name, 'X1', 'X1 Default Gateway', 'X2 Subnet', PC4_ETH1_IP]
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check custom nat policy: {res}')
        Assertion.assert_equal(res.count(True), 5, "ERR: check route configure failed")


class TestRoute_TC042(Test):
    uuid = "SOSAIOT-TC-74773"
    description = show_testcase_info(TESTPLAN, 'TC042', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC042')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_0_check_ping_from_custom_to_wan_zone(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC3_login.ping(PC4_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: check ping failed")


class TestAccessrulesApprules_TC01(Test):
    uuid = "SOSAIOT-TC-74802"
    description = show_testcase_info(TESTPLAN, 'TCACL01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TCACL01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_access_rules_configure(self):
        output = accessruleapi.get_accessrule_via_zones(srczone='WAN', dstzone='LAN')
        Assertion.assert_regular(
            json.dumps(output), CaseParams.custom_access_name, "ERR: check access rules configure failed")

    def test_01_check_app_rules_configure(self):
        output = appruleapi.get_apprule_object(name=CaseParams.custom_apprule_name)
        Assertion.assert_regular(
            json.dumps(output), CaseParams.custom_march_name, "ERR: check app rules configure failed")


class TestAccessrulesApprules_TC02(Test):
    uuid = "SOSAIOT-TC-74803"
    description = show_testcase_info(TESTPLAN, 'TCACL02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TCACL02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ping_passed_from_wan_to_lan(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC4_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(output, True, "ERR: check ping failed")

    def test_02_enable_app_rules(self):
        apprule_setting_dict = {
            "enable": True,
            "log_redundancy": {}
        }
        output = appruleapi.config_apprule_setting(**apprule_setting_dict)
        Assertion.assert_equal(output, True, "ERR: enable app rule failed")

    def test_03_check_app_rules_http_block_function(self):
        logger.info('waiting for 10s to valid configure...')
        time.sleep(10)
        output = PC2_login.send_command(f'curl http://{PC4_ETH1_IP}')
        msg = 'Connection reset by peer'
        Assertion.assert_regular(output, msg, "ERR: check app rules http block failed")

    def test_04_disable_app_rules(self):
        apprule_setting_dict = {
            "enable": False,
            "log_redundancy": {}
        }
        output = appruleapi.config_apprule_setting(**apprule_setting_dict)
        Assertion.assert_equal(output, True, "ERR: disable app rule failed")


class TestDPISSL01(Test):
    uuid = "SOSAIOT-TC-74804"
    description = show_testcase_info(TESTPLAN, 'DPISSL01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DPISSL01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dpissl_configure(self):
        output = clientsslapi.show_dpissl_client()
        filter_list = ['enable\': True',
                       'intrusion_prevention\': True',
                       'anti_virus\': True',
                       'anti_spyware\': True',
                       'content_filter\': True']
        res = [x in str(output) for x in filter_list]
        logger.info(f'check dpissl configure: {res}')
        Assertion.assert_equal(res.count(True), 5, "ERR: check dpissl configure failed")


class TestDPISSL02(Test):
    uuid = "SOSAIOT-TC-74805"
    description = show_testcase_info(TESTPLAN, 'DPISSL02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DPISSL02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dpissl_function(self):
        cmd = f'echo | openssl s_client -connect {PC4_ETH1_IP}:443 2>/dev/null'
        logger.info(f'send cmd : {cmd}')
        output = PC2_login.send_command(cmd)
        Assertion.assert_regular(output, 'SonicWALL Firewall DPI-SSL', "ERR: check certificate failed")


class TestDNS_TC021(Test):
    uuid = "SOSAIOT-TC-74752"
    description = show_testcase_info(TESTPLAN, 'DNS_TC021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DNS_TC021')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dns_configure(self):
        output = dnssettingapi.get_dns()
        filter_list = [Parameter.VALID_DNS, Parameter.FAKE_DNS1, Parameter.FAKE_DNS2]
        res = [x in str(output) for x in filter_list]
        logger.info(f'check dns configure: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check dns configure failed")


class TestDNS_TC022(Test):
    uuid = "SOSAIOT-TC-74753"
    description = show_testcase_info(TESTPLAN, 'DNS_TC022', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DNS_TC022')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dns_functions(self):
        output = diagapi.diag_dns_name_lookup(cmd="nslookup dns.baidu.com")
        logger.info(f'nslookup dns.baidu.com result: {output}')
        res = True if Parameter.VALID_DNS in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check DNS functions failed")


class TestSyslog_TC063(Test):
    uuid = "SOSAIOT-TC-74793"
    description = show_testcase_info(TESTPLAN, 'Syslog_TC063', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Syslog_TC063')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_syslog_configure(self):
        output = syslogsettingsapi.show_syslog_server()
        Assertion.assert_regular(str(output), PC4_ETH1_IP, "ERR: check syslog configure failed")


class TestSyslog_TC064(Test):
    uuid = "SOSAIOT-TC-74794"
    description = show_testcase_info(TESTPLAN, 'Syslog_TC066', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Syslog_TC064')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_syslog_function(self):
        res = False
        cmds = [
            "echo '' > /var/log/messages",
            'systemctl restart rsyslog',
        ]
        # clear syslog server msg
        PC4_login.send_commands(cmds)
        for count in range(5):
            logger.info('wait 20s to get syslog msg...')
            time.sleep(20)
            output = PC4_login.send_commands(['cat /var/log/messages'])
            if 'id=firewall' in output:
                logger.info('fw log upload to syslog server successful.')
                res = True
                break
        else:
            logger.info('can not find fw msg from suslog server.')
        Assertion.assert_equal(res, True, "ERR: check syslog function failed")


class TestTime_TC065(Test):
    uuid = "SOSAIOT-TC-74795"
    description = show_testcase_info(TESTPLAN, 'Time_TC065', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Time_TC065')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_time_configure(self):
        res = False
        output = timeapi.show_time()
        try:
            if output['time']['use_ntp'] and output['time']['time_zone'] == 'china,philippines':
                res = True
        except Exception as e:
            logger.info(f'get time configure fail.\n {e}')
        Assertion.assert_equal(res, True, "ERR: check time configure failed")


class TestTime_TC066(Test):
    uuid = "SOSAIOT-TC-74796"
    description = show_testcase_info(TESTPLAN, 'Time_TC066', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Time_TC066')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_time_function(self):
        res = False
        orgtime = timeapi.show_time()
        time_dict = {
            "time": {
                "use_ntp": True,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "only_custom_ntp": False,
                "ntp_update_interval": 30
            }
        }
        changezone = timeapi.set_time(**time_dict)
        logger.info(f'change time zone: {changezone}')
        newtime = timeapi.show_time()
        try:
            new = newtime['time']['time']
            old = orgtime['time']['time']
            logger.info(f'new time: {new}, old time: {old}')
            if new != old:
                res = True
            else:
                logger.info(f'new time eq old time.')
        except Exception as e:
            logger.info({e})
        Assertion.assert_equal(res, True, "ERR: check time function failed")


class TestLogging_TC033(Test):
    uuid = "SOSAIOT-TC-74764"
    description = show_testcase_info(TESTPLAN, 'Logging_TC033', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Logging_TC033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_logging_configure(self):
        output = logsettingsapi.show_event(event_id='602')
        Assertion.assert_regular(str(output), 'redundancy_interval\': 123', "ERR: check logging cofnigure failed")


class TestLogging_TC034(Test):
    uuid = "SOSAIOT-TC-74765"
    description = show_testcase_info(TESTPLAN, 'Logging_TC034', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Logging_TC034')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_logging_function(self):
        output = logmonitorapi.get_log(id='602')
        res = True if output else False
        Assertion.assert_equal(res, True, "ERR: check logging function failed")


class TestSNMP_TC067(Test):
    uuid = "SOSAIOT-TC-74797"
    description = show_testcase_info(TESTPLAN, 'SNMP_TC067', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SNMP_TC067')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_snmp_configure(self):
        output = snmpapi.show_snmp()
        Assertion.assert_regular(str(output), 'enable\': True', "ERR: check snmp configure failed")


class TestSNMP_TC068(Test):
    uuid = "SOSAIOT-TC-74798"
    description = show_testcase_info(TESTPLAN, 'SNMP_TC068', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'SNMP_TC068')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_snmp_function(self):
        # res = False
        # status = statusapi.show_status()
        # logger.info(f"{f' snmp monitor -sysDescr- result ':=^60}")
        # cmd = f'snmpwalk -v2c -cpublic -OQv {Parameter.X2_IP} sysDescr'
        # output = PC3_login.send_command(cmd)
        # if 'model' in status.keys():
        #     logger.info(f'status model is {status["model"]}')
        #     res = True if status['model'] in output else False
        # Assertion.assert_equal(res, True, f"ERR: Get snmp sysDescr failed!!")
        snmp_user_group = "snmpgGroup"
        snmp_user_dict = {
            "user_name": "snmpUser",
            "user_security": "",
            "user_group": snmp_user_group,
        }
        user_name = snmp_user_dict["user_name"]
        snmp_cmd = f"snmpwalk -c public -u {user_name} {Parameter.X2_IP} -l noAuthNoPriv .1.3.6.1.2.1.1.1.0"
        snmp_res = PC3_login.send_command(snmp_cmd)
        # Response example >> SNMPv2-MIB::sysDescr.0 = STRING: SonicWALL TZ 370 (SonicOS 7.1.1-7051-P5654)
        Assertion.assert_equal("sonicwall" in snmp_res.lower(), True, "ERR: Check snmp function failed")



class TestDHCPServer_TC019(Test):
    uuid = "SOSAIOT-TC-74750"
    description = show_testcase_info(TESTPLAN, 'DHCP_TC019', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DHCP_TC019')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dhcp_server_configure(self):
        output = dhcpserverapi.get_dhcp_server_scope_dynamic()
        filter_list = ['from": "192.168.2.80', 'to": "192.168.2.85', 'enable": true']
        res = [x in json.dumps(output) for x in filter_list]
        logger.info(f'check dhcp server configure: {res}')
        Assertion.assert_equal(res.count(True), 3, "ERR: check dhcp server configure failed")


class TestDHCPServer_TC020(Test):
    uuid = "SOSAIOT-TC-74751"
    description = show_testcase_info(TESTPLAN, 'DHCP_TC020', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DHCP_TC020')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_dhcp_server(self):
        dhcp_seting_dict['dhcp_server']['ipv4']['enable'] = True
        output = dhcpserverapi.config_dhcp_server_settings(**dhcp_seting_dict)
        Assertion.assert_equal(output, True, "ERR: enable dhcp server failed")

    @repeat_method(5)
    def test_02_get_dhcp_lease_in_pc2(self):
        logger.info('waiting for 30s to valid dhcp server configure...')
        time.sleep(30)
        cmds = [
            'cp /dev/null /etc/resolv.conf',
            'rm -rf /var/lib/dhclient/dhclient.leases',
        ]
        PC2_login.send_commands(cmds)
        res = get_ip_lease_in_pc(PC3_login, 'eth1')
        Assertion.assert_equal(res, True, 'ERR: PC3 get dhcp lease from DUT failed')

    def test_03_init_pc3_configure(self):
        dhcp_seting_dict['dhcp_server']['ipv4']['enable'] = False
        output1 = dhcpserverapi.config_dhcp_server_settings(**dhcp_seting_dict)
        logger.info(f'disable dhcp server result: {output1}')

        cmds = [
            f'ifconfig eth1 {PC3_ETH1_IP}',
            f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}',
            'ip -4 r']
        output2 = PC3_login.send_commands(cmds)
        Assertion.assert_regular(output2, PC3_ETH1_IP, 'ERR: init pc3 configure failed')


