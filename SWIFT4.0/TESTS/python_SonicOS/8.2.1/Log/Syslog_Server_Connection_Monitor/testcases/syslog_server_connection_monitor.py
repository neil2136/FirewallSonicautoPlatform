from definition.settings import *
from definition.utils import *


# [GUI]Enable syslog server connection monitor
class Test_Syslog_Monitor_TC01(Test):
    uuid = "SOSAIOT-TC-54849"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_Syslog_Monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": True})
        Assertion.assert_equal(rc, True, 'ERR: Enable syslog connection monitor via GUI failed!!')


# [GUI]Disable syslog server connection monitor
class Test_Syslog_Monitor_TC02(Test):
    uuid = "SOSAIOT-TC-54850"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_disable_Syslog_Monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": False})
        Assertion.assert_equal(rc, True, 'ERR: Disable syslog connection monitor via GUI failed!!')


# [CLI]Enable syslog server connection monitor
class Test_Syslog_Monitor_TC03(Test):
    uuid = "SOSAIOT-TC-54851"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_Syslog_Monitor_CLI(self):
        rc = fw_cli.do_cli_commands(commands=['configure', 'log syslog', "connection-monitor", "commit", "end", "exit"])
        Assertion.assert_equal(rc, True, "ERR: Enable syslog connection monitor via CLI failed!!")


# [CLI]Disable syslog server connection monitor
class Test_Syslog_Monitor_TC04(Test):
    uuid = "SOSAIOT-TC-54852"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_disable_Syslog_Monitor_CLI(self):
        rc = fw_cli.do_cli_commands(
            commands=['configure', 'log syslog', "no connection-monitor", "commit", "end", "exit"])
        Assertion.assert_equal(rc, True, "ERR: Disable syslog connection monitor via CLI failed")


# Enable syslog server connection monitor after syslog server(UDP) is added
class Test_Syslog_Monitor_TC07(Test):
    uuid = "SOSAIOT-TC-54853"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_syslog_server(self):
        res = syslog_api.add_syslog_server(**{'name': 'syslog_server'})
        Assertion.assert_equal(res, True, "ERR: Add UDP syslog server failed")

    def test_02_enable_Syslog_Monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": True})
        Assertion.assert_equal(rc, True, 'ERR: Enable syslog connection monitor via GUI failed!!')

    @repeat_method(3)
    def test_03_check_network_monitor_policy(self):
        rc = False
        logger.info('STEP 1: check network monitor policy is auto added')
        out = net_mon_api.get_network_monitor()
        if out and out.get('network_monitors'):
            for policy in out['network_monitors']:
                if "Auto-added from syslog server connection monitor" in json.dumps(policy):
                    logger.info('auth-added a network monitor policy successfully!!')
                    try:
                        policy_name = policy['policy']["ipv4"]["name"]
                        logger.info("STEP 2: check it can not be deleted")
                        del_res, err_msg = net_mon_api.del_network_monitor(name=policy_name, msg=True)
                        logger.info(f'del auto added network monitor policy result: {del_res}')
                        rc = (not del_res) and bool(re.search(r'ping_Syslog_.*read only', json.dumps(err_msg)))
                    except Exception as e:
                        logger.error(repr(e))
                    break
        else:
            logger.error('no network monitor policy generated!')
        Assertion.assert_equal(rc, True, "ERR: check network monitor policy failed after add syslog server!!")


# Disable syslog server connection monitor after syslog server(UDP) is added
class Test_Syslog_Monitor_TC08(Test):
    uuid = "SOSAIOT-TC-54854"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_disable_Syslog_Monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": False})
        Assertion.assert_equal(rc, True, 'ERR: Disable syslog connection monitor via GUI failed!!')

    def test_02_check_network_monitor_policy(self):
        out = net_mon_api.get_network_monitor()
        Assertion.assert_equal(bool(out), False,
                               'ERR: check auto-added network monitor policy is deleted after disable connection monitor failed!')

    def test_03_del_syslog_server(self):
        rc = syslog_api.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'ERR: delete syslog servers failed!!')


# Add maximun numbers of syslog servers(up to 7) when option "Enable syslog server connection monitor" is enabled
class Test_Syslog_Monitor_TC11(Test):
    uuid = "SOSAIOT-TC-54856"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_connection_monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": True})
        Assertion.assert_equal(rc, True, 'ERR: Enable syslog connection monitor via GUI failed!!')

    def test_02_add_maximun_server_addr_objs(self):
        for i in range(Parameter.MAX_NUM):
            ao_opt = {
                "object_type": "host",
                "name": f"syslog_server_{i + 1}",
                "zone": "LAN",
                "value": f"192.168.168.{i + 1}",
            }
            rc = ao_api.config_addressobject(**ao_opt)
            if not rc:
                logger.error(f'add number {i + 1} server addr obj failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: add maximum syslog servers objects failed!")

    def test_03_add_maximum_syslog_servers(self):
        for i in range(Parameter.MAX_NUM):
            syslog_opt = {
                'name': f'syslog_server_{i + 1}',
                'profile': 0
            }
            rc = syslog_api.add_syslog_server(**syslog_opt)
            if not rc:
                logger.error(f'add number {i + 1} syslog server failed!')
                break
        Assertion.assert_equal(rc, True, "ERR: Add maximum UDP syslog servers failed")

    def test_04_check_network_monitor_policy(self):
        rc = False
        out = net_mon_api.get_network_monitor()
        try:
            if len(out["network_monitors"]) < Parameter.MAX_NUM:
                logger.error('get network monitor policies failed！')
            else:
                for policy in out["network_monitors"]:
                    policy_name = policy['policy']["ipv4"]["name"]
                    logger.info(f'check the {policy_name}')
                    logger.info(policy)
                    if "Auto-added from syslog server connection monitor" in json.dumps(policy):
                        del_res, err_msg = net_mon_api.del_network_monitor(name=policy_name, msg=True)
                        logger.info(f'del auto added network monitor policy result: {del_res}')
                        rc = (not del_res) and bool(re.search(r'ping_Syslog_.*read only', json.dumps(err_msg)))
                        if not rc:
                            logger.error(f'check policy <{policy_name}> failed!')
                            break
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(rc, True, "ERR: check the auto-added network monitor failed!")


# Delete all syslog servers when option "Enable syslog server connection monitor" is enabled
class Test_Syslog_Monitor_TC12(Test):
    uuid = "SOSAIOT-TC-54857"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_del_all_syslog_servers(self):
        rc = False
        del_res = syslog_api.delete_all_syslog_servers()
        logger.info(f'delete all syslog servers via API result: {del_res}')
        if del_res:
            out = syslog_api.show_syslog_server()
            rc = not bool(out['log'].get('syslog')) if out and out.get('log') else False
        Assertion.assert_equal(rc, True, 'ERR: delete all syslog servers failed!')

    def test_02_check_network_monitor_policy(self):
        out = net_mon_api.get_network_monitor()
        Assertion.assert_equal(bool(out), False, "ERR: check network monitor policy should be deleted failed!")


# Disable syslog server connection monitor when maximun numbers of syslog servers(up to 7) are added
class Test_Syslog_Monitor_TC13(Test):
    uuid = "SOSAIOT-TC-54858"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_maximun_syslog_servers(self):
        Test_Syslog_Monitor_TC11().test_03_add_maximum_syslog_servers()

    def test_02_disable_connection_monitor(self):
        Test_Syslog_Monitor_TC02().test_01_disable_Syslog_Monitor()

    def test_03_check_network_monitor_policy(self):
        Test_Syslog_Monitor_TC12().test_02_check_network_monitor_policy()


# Enable/Disable syslog server connection monitor repeatedly when maximun numbers of syslog servers(up to 7) are added
class Test_Syslog_Monitor_TC14(Test):
    uuid = "SOSAIOT-TC-54859"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_disable_connection_monitor_repeatly(self):
        for i in range(10):
            sleep(3)
            logger.info(f'enable/disable for the <{i + 1}> time')
            en_rc = syslog_api.edit_syslog_settings(**{"connection_monitor": True})
            logger.info(f'enable result: {en_rc}')
            sleep(3)
            dis_rc = syslog_api.edit_syslog_settings(**{"connection_monitor": False})
            logger.info(f'disable result: {dis_rc}')
            if not en_rc or not dis_rc:
                break
        Assertion.assert_equal(en_rc & dis_rc, True, "ERR: disable/enable connection monitor repeatedly failed!")

    def test_02_del_syslog_server(self):
        rc = syslog_api.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'ERR: delete syslog servers failed')


# Enable syslog server connection monitor when syslog server(using host) is reachable
class Test_Syslog_Monitor_TC15(Test):
    uuid = "SOSAIOT-TC-54860"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_connection_monitor(self):
        rc = syslog_api.edit_syslog_settings(**{"connection_monitor": True})
        Assertion.assert_equal(rc, True, 'ERR: Enable syslog connection monitor via GUI failed!!')

    def test_02_add_reachable_syslog_server(self):
        res = log_mon_api.clear_log()
        logger.info(f'clear log monitor result: {res}')
        Test_Syslog_Monitor_TC07().test_01_add_syslog_server()

    @repeat_method(3)
    def test_03_check_network_monitor_policy_state(self):
        sleep(3)
        out = net_mon_api.get_network_monitor_status()
        rc = '"led": "green"' in json.dumps(out) and '"status": "UP"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check network monitor policy state failed')

    @repeat_method(3)
    def test_04_check_log(self):
        sleep(10)
        log1 = log_mon_api.get_log('707')
        log2 = log_mon_api.get_log('1100')
        Assertion.assert_equal(bool(log1) and bool(log2), True, "ERR: check related logs failed")

    def test_05_del_syslog_server(self):
        rc = syslog_api.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'ERR: delete syslog servers failed!')


# Enable syslog server connection monitor when syslog server(using host) is unreachable
class Test_Syslog_Monitor_TC16(Test):
    uuid = "SOSAIOT-TC-54861"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_00_add_unreachable_syslog_server_addr_object(self):
        ao_opt = {
            "object_type": "host",
            "name": "syslog_server_unreach",
            "zone": "LAN",
            "value": "1.2.3.4",
        }
        rc = ao_api.config_addressobject(**ao_opt)
        Assertion.assert_equal(rc, True, "ERR: add_unreachable_syslog_server_addr_object failed!!")

    def test_01_01_add_unreachable_syslog_server(self):
        log_mon_api.clear_log()
        res = syslog_api.add_syslog_server(**{'name': 'syslog_server_unreach'})
        Assertion.assert_equal(res, True, "ERR: Add a unreachable syslog server failed")

    @repeat_method(3)
    def test_02_check_network_monitor_state(self):
        sleep(3)
        out = net_mon_api.get_network_monitor_status()
        rc = '"led": "red"' in json.dumps(out) and '"status": "DOWN"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check network monitor policy state failed')

    @repeat_method(3)
    def test_03_check_log(self):
        sleep(25)
        log1 = log_mon_api.get_log('706')
        log2 = log_mon_api.get_log('1101')
        Assertion.assert_equal(bool(log1) & bool(log2), True, "ERR: check related logs failed!!")

    def test_04_del_syslog_server(self):
        rc = syslog_api.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, "ERR: delete syslog server failed")


# DUT start/stop sending syslog messages whensyslog server(UDP) is reachable/unreachable
class Test_Syslog_Monitor_TC22(Test):
    uuid = "SOSAIOT-TC-54864"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_pkt_mon(self):
        pkt_mon = {
            'monitor_filter': {
                'ip_types': "UDP",
                'destination_ports': "514"
            }
        }
        rc = pkt_api.conf_packmon(**pkt_mon)
        Assertion.assert_equal(rc, True, "ERR: config pkt monitor failed!")

    def test_02_add_syslog_server(self):
        init_packet_capture()
        Test_Syslog_Monitor_TC07().test_01_add_syslog_server()

    @repeat_method(3)
    def test_03_check_syslog_pkt(self):
        rc = False
        sleep(30)
        stop_res = pkt_api.stop_capture()
        logger.info(f'stop pkt capture result: {stop_res}')
        packets = pkt_api.export_captured_packets()
        if packets:
            for pkt in packets.split('\n'):
                if 'Dst=[12.12.1.169]' in pkt:
                    logger.info(f'find the syslog packet:\n{pkt}')
                    rc = True
                    break
        else:
            logger.error('no packet generated!')
        Assertion.assert_equal(rc, True, "ERR: check syslog packet sent failed!!")

    def test_04_disable_x1(self):
        rc = iface_v4_api.disable_interface('x1')
        Assertion.assert_equal(rc, True, 'ERR: shutdown X1 failed!!')

    @repeat_method(3)
    def test_05_check_led_of_network_monitor_red(self):
        sleep(10)
        out = net_mon_api.get_network_monitor_status()
        rc = '"led": "red"' in json.dumps(out) and '"status": "DOWN"' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check network monitor policy state failed!!')

    def test_06_check_no_syslog_pkt(self):
        init_packet_capture()
        for i in range(3):
            logger.info(f'run for the {i + 1} time')
            sleep(30)
            packets = pkt_api.export_captured_packets()
            if packets:
                for pkt in packets.split('\n'):
                    if 'Dst=[12.12.1.169]' in pkt:
                        logger.info(f'find the syslog packet:\n{pkt}')
                        rc = False
                        break
                else:
                    logger.info('no syslog packet generated')
                    rc = True
            else:
                logger.error('no packet generated!')
                rc = True
        Assertion.assert_equal(rc, True, "ERR: should no syslog packet sent out!!")

    def test_07_enable_x1(self):
        rc = iface_v4_api.enable_interface('x1')
        Assertion.assert_equal(rc, True, 'ERR: enable X1 interface failed!')


# Modify syslog server when option "Enable syslog server connection monitor" is enabled
class Test_Syslog_Monitor_TC25(Test):
    uuid = "SOSAIOT-TC-54867"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_modify_syslog_server(self):
        syslog_opt = {
            'original_profile': 0,
            'original_syslog_server_name': "syslog_server",
            'original_port': 514,
            'original_protocol': "udp",
            # 'name': 'syslog_server',
            # 'new_name': "syslog_server_4",
            'address': {'name': "syslog_server_4"},
        }
        rc = syslog_api.edit_syslog_server_new(**syslog_opt)
        Assertion.assert_equal(rc, True, 'ERR: modify syslog server failed!')

    def test_02_check_network_monitor_policy_updated(self):
        out = net_mon_api.get_network_monitor()
        Assertion.assert_regular(json.dumps(out), '192.168.168.4',
                                 "ERR: check the network policy updated failed!")


# Check TSR file after enable syslog server connection monitor
class Test_Syslog_Monitor_TC26(Test):
    uuid = "SOSAIOT-TC-54868"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_tsr_info(self):
        tsr_info = diag_api.get_tsr_part(func='Log', lab1='Log Monitor')
        Assertion.assert_regular(tsr_info, 'Enable UDP Syslog Server Connection Monitor: Enabled',
                                 "ERR: check syslog server connection monitor state in tsr file filed!")


# Reboot DUT after enable syslog server connection monitor
class Test_Syslog_Monitor_TC27(Test):
    uuid = "SOSAIOT-TC-54869"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_reboot_firewall(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: restart firewall failed')

    def test_01_check_connection_monitor_settings(self):
        out = syslog_api.get_syslog_settings()
        Assertion.assert_regular(json.dumps(out), '"connection_monitor": true',
                                 'ERR: check connection monitor settings after reboot failed!')


# Check frequency for syslog event 657 on log settings
class Test_Syslog_Monitor_TC29(Test):
    uuid = "SOSAIOT-TC-54870"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_frequency_of_event657(self):
        out = log_set_api.show_event('657')
        rc = '"email_alert": {"redundancy_interval": 900}' in json.dumps(
            out) and '"syslog": {"redundancy_interval": 60}' in json.dumps(out)
        Assertion.assert_equal(rc, True, 'ERR: check frequency for syslog event 675 on log settings failed!')
