from definition.settings import *


# [Log Monitor] Verify the NAT mapping log could be generated when having LAN to WAN TCP new connection opened
class Test_Log_Nat_Mapping_TC1529557(Test):
    uuid = "SOSAIOT-TC-54804"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_check_log_LAN_to_WAN(self):
        logmon_api.clear_log()
        PC1.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        Assertion.assert_regular(json.dumps(log), '"message": "NAT Mapping"',
                                 'ERR: check Mapping log from LAN to WAN failed!!')


# [Log Monitor] Verify the NAT mapping log could be generated when having DMZ to WAN TCP new connection opened
class Test_Log_Nat_Mapping_TC1529558(Test):
    uuid = "SOSAIOT-TC-54805"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_check_log_DMZ_to_WAN(self):
        logmon_api.clear_log()
        PC3.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        Assertion.assert_regular(json.dumps(log), '"message": "NAT Mapping"',
                                 'ERR: check Mapping log from LAN to WAN failed!!')


# [Log Monitor] Verify the NAT mapping log could be generated when having WAN to DMZ TCP new connection opened
class Test_Log_Nat_Mapping_TC1529559(Test):
    uuid = "SOSAIOT-TC-54806"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_02_check_log_WAN_to_DMZ(self):
        logmon_api.clear_log()
        PC2.send_command(f'curl -k https://{Parameter.NAT_IP_DMZ}')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        Assertion.assert_regular(json.dumps(log), '"message": "NAT Mapping"',
                                 'ERR: check Mapping log from LAN to WAN failed!!')


# [Syslog]  Verify the NAT mapping log could be generated when having LAN to WAN TCP new connection opened
class Test_Log_Nat_Mapping_TC1529561(Test):
    uuid = "SOSAIOT-TC-54808"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_check_syslog_LAN_to_WAN(self):
        PC1.send_command("echo > /var/log/messages")
        PC1.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        out = PC1.send_command('cat /var/log/messages')
        Assertion.assert_regular(out, 'msg="NAT Mapping"', 'ERR: check syslog from LAN to WAN failed!!')


#  [Syslog] Verify the NAT mapping log could be generated when having DMZ to WAN TCP new connection opened
class Test_Log_Nat_Mapping_TC1529562(Test):
    uuid = "SOSAIOT-TC-54809"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_check_syslog_DMZ_to_WAN(self):
        PC1.send_command("echo > /var/log/messages")
        PC3.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        out = PC1.send_command('cat /var/log/messages')
        Assertion.assert_regular(out, 'msg="NAT Mapping"', 'ERR: check syslog from LAN to WAN failed!!')


# [Syslog] Verify the NAT mapping log could be generated when having WAN to DMZ TCP new connection opened
class Test_Log_Nat_Mapping_TC1529563(Test):
    uuid = "SOSAIOT-TC-54810"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    @repeat_method(3)
    def test_01_check_syslog_WAN_to_DMZ(self):
        PC1.send_command("echo > /var/log/messages")
        PC2.send_command(f'curl -k https://{Parameter.NAT_IP_DMZ}')
        sleep(5)
        out = PC1.send_command('cat /var/log/messages')
        Assertion.assert_regular(out, 'msg="NAT Mapping"', 'ERR: check syslog from LAN to WAN failed!!')


# [Stress] Verify the NAT mapping log still could be generated normally when the TCP new connection rate is high
class Test_Log_Nat_Mapping_TC1529564(Test):
    uuid = "SOSAIOT-TC-54811"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_log_in_stress_test(self):
        logmon_api.clear_log()
        PC3.send_command(f'python3 {script_path} stress')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        Assertion.assert_regular(json.dumps(log), '"message": "NAT Mapping"',
                                 'ERR: check Mapping log from LAN to WAN failed!!')


# [Log Monitor] Verify the "Frequency Filter Interval" timer for TCP NAT mapping log
class Test_Log_Nat_Mapping_TC1529560(Test):
    uuid = "SOSAIOT-TC-54807"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_log_set_for_nat_mapping(self):
        event_1197["log"]["event"][0]["log_monitor"]["redundancy_interval"]=60
        rc = logset_api.edit_event(event_id='1197', **event_1197)
        Assertion.assert_equal(rc, True, 'ERR: edit event for id 1197 failed!!')

    def test_02_check_log_WAN_to_DMZ(self):
        logmon_api.clear_log()
        PC3.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        PC3.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        PC3.send_command(f'curl -k https://{PC2_ETH1_IP}')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        rc = len(re.findall(r'NAT Mapping', json.dumps(log))) == 1 if log else False
        Assertion.assert_equal(rc, True, 'ERR: verify "Frequency Filter Interval" timer for TCP NAT Mapping failed!!')


# Verify the NAT mapping log could be generated when having IPv6 TCP new connection opened
class Test_Log_Nat_Mapping_TC1529566(Test):
    uuid = "SOSAIOT-TC-54812"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_v6_nat_rule(self):
        init_dict = copy.deepcopy(nat_base)
        edit_dict = {
            'name': 'test',
            "translated_source": {"name": "X1 IPv6 Primary Static Address"}
        }
        init_dict.update(edit_dict)
        nat_v6_json = {"nat_policies": [{"ipv6": init_dict}]}
        rc = nat_api.add_nat_policy(**nat_v6_json)
        Assertion.assert_equal(rc, True, 'ERR: add v6 nat rule failed!!')

    @repeat_method(3)
    def test_02_check_ipv6_log_LAN_to_WAN(self):
        logmon_api.clear_log()
        PC1.send_command('curl -k https://[1012::169]')
        sleep(5)
        log = logmon_api.get_log(id='1197')
        logger.info(log)
        Assertion.assert_regular(json.dumps(log), '"message": "NAT Mapping"',
                                 'ERR: check Mapping log from LAN to WAN failed!!')


# Verify the NAT policy counter will be increased when have new LAN to WAN TCP connections opened
class Test_Log_Nat_Mapping_TC1529567(Test):
    uuid = "SOSAIOT-TC-54813"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_range_ao(self):
        range_dict = {
            "object_type": "range",
            "name": "12.12.1.5_35",
            "zone": "WAN",
            "value": "12.12.1.5,12.12.1.35"
        }
        rc = ao_api.config_addressobject(**range_dict)
        Assertion.assert_equal(rc, True, 'ERR: add addr obj for X1 range failed!!')

    def test_02_edit_nat_rule(self):
        init_dict = copy.deepcopy(nat_base)
        edit_dict = {
            'name': 'tc1529560',
            "destination": {"name": '12.12.1.5_35'},
            "translated_destination": {"name": "dmz_host"}
        }
        init_dict.update(edit_dict)
        nat_v4_json = {"nat_policies": [{"ipv4": init_dict}]}
        rc = nat_api.edit_nat_policy_by_name(name='tc1529560', **nat_v4_json)
        Assertion.assert_equal(rc, True, 'ERR: edit nat rule failed!!')

    @repeat_method(3)
    def test_03_check_hit_counters(self):
        out1 = nat_api.get_statistics_by_name(name='tc1529560')
        count1 = out1.get('usage_count') if out1 else -1
        PC3.send_command(f'python3 {script_path} count')
        out2 = nat_api.get_statistics_by_name(name='tc1529560')
        count2 = out2.get('usage_count') if out2 else -2
        Assertion.assert_equal(count2-count1, 20, 'ERR: check the hit counters failed!!')
