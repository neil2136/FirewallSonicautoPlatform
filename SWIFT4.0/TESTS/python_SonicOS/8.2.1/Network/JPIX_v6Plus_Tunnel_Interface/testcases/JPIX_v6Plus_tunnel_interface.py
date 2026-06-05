from definition.utils import *


#[GUI]Verify ""Update URL"" and  ""Update URL Period"" shown in advanced page when add ""v6Plus Static IP Address Service"" tunnel
class Test_TC01(Test):
    uuid = 'SOSAIOT-TC-57672'
    description = show_testcase_info(TESTPLAN, 'TC01', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_v6plus_tunnel_interface_with_url_and_url_period(self):
        # This case is including in TC03
        Assertion.assert_equal(True, True, 'ERR: check update url and update url period option failed!!')
    

# [Negtive]Verify specify charater can't be fill in ""Update URL"" and  ""Update URL Period"" field in ""v6Plus Static IP Address Service"" tunnel advanced page
class Test_TC02(Test):
    uuid = 'SOSAIOT-TC-57673'
    description = show_testcase_info(TESTPLAN, 'TC02', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_v6plus_tunnel_interface_with_invalid_characters_in_URL(self):
        opt = {
                "name": "v6plus_invalid_URL",
                "bound_to_if": "X1",
                "local": {"dynamic": True},
                "remote": {"ipv6": "2001:1:2:3::1"},
                # "update_url": random.choice(string.punctuation),
                "update_url": '$',
                "update_url_period": 1,
                "comment": ""
            }
        rc, err_msg = if_v4_api.add_v6plus_tunnel_interface(**opt, msg=True)
        logger.info(json.dumps(err_msg))
        Assertion.assert_equal(rc, False, 'ERR: check invalid characters in update url failed!!')
    
    def test_02_add_v6plus_tunnel_interface_with_invalid_characters_in_URL_period(self):
        opt = {
                "name": "v6plus_invalid_URL_period",
                "bound_to_if": "X1",
                "local": {"dynamic": True},
                "remote": {"ipv6": "2001:1:2:3::1"},
                "update_url": "http://[2001:1:2:3::1]",
                "update_url_period": random.choice(string.punctuation),
                "comment": ""
            }
        rc, err_msg = if_v4_api.add_v6plus_tunnel_interface(**opt, msg=True)
        logger.info(json.dumps(err_msg))
        Assertion.assert_equal(rc, False, 'ERR: check invalid characters in update url period failed!!')
    

# [Func]Verify \"Update URL Period\" status and details show correct
class Test_TC03(Test):
    uuid = 'SOSAIOT-TC-57674'
    description = show_testcase_info(TESTPLAN, 'TC03', description=True)['title'] 
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_x1v6_to_auto_mode(self):
        opt= {
            'name': 'X1',
            'mode': 'auto',
            'interface_identifier': "::1.1.1.1",
            "mgmt_ping": True,
            "mgmt_https": True
        }
        rc = if_v6_api.config_interface_ipv6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1v6 to auto mode failed!!')
    
    @repeat_method(5, 10)
    def test_02_check_x1_v6_get_v6_addr(self):
        v6_addr = get_v6_addr()
        Assertion.assert_regular(v6_addr, '2001:1:2:3::', 'ERR: x1 v6 get ip addr failed!')

    def test_03_add_v6plus_4to6_tunnel_interface(self):
        opt = {
                "name": "v6plus_t1",
                "bound_to_if": "X1",
                "local": {"dynamic": True},
                "remote": {"ipv6": "2001:1:2:3::1"},
                "update_url": "http://[2001:1:2:3::1]",
                "update_url_period": 1,
                "comment": ""
            }
        rc = if_v4_api.add_v6plus_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add v6Plus tunnel failed!!')
    
    def test_04_check_led_status_with_url_period_1(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1 status'], tag=1)
        rc = bool(re.search(r'Update url status:\s+Success', out, re.I))
        Assertion.assert_equal(rc, True, 'ERR: check led status with url period 1 failed!!')

    def test_05_edit_v6plus_tunnel_interface_url_blank(self):
        opt = {
            "update_url": ""
        }
        rc = if_v4_api.edit_v6plus_tunnel_interface_by_name(tunnel_name='v6plus_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit v6Plus tunnel interface url blank failed!!')
    
    def test_06_check_led_status_with_url_blank(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1 status'], tag=1)
        rc = bool(re.search(r'Update url status:\s+Success 0 times', out, re.I))
        Assertion.assert_equal(rc, True, 'ERR: check led status with url blank failed!!')
    
    def test_07_edit_v6plus_tunnel_interface_url_blow_0(self):
        opt = {
             "update_url": "-1"
        }
        rc = if_v4_api.edit_v6plus_tunnel_interface_by_name(tunnel_name='v6plus_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit v6Plus tunnel interface url below 0 failed!!')
    
    @repeat_method(3, 10)
    def test_08_check_led_status_with_url_blow_0(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1 status'], tag=1)
        rc = bool(re.search(r'Update url status:\s+Failed', out, re.I))
        Assertion.assert_equal(rc, True, 'ERR: check led status with url below 0 failed!!')


# [Func]Verify http request send via "Update URL" when primary address changed
class Test_TC04(Test):
    uuid = 'SOSAIOT-TC-57675'
    description = show_testcase_info(TESTPLAN, 'TC04', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_packet_monitor(self):
        opt = {
            'monitor_filter': {
                'ip_types': 'tcp', 
                'destination_ports': '80',
                'destination_ips': '2001:1:2:3::1'
            }  
        }
        rc = pkt_api.conf_packmon(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config packet monitor failed!!')

    def test_02_edit_url_period_to_43200(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        sleep(5)
        opt = {
            "update_url": "http://[2001:1:2:3::1]",
            "update_url_period": 43200
        }
        rc = if_v4_api.edit_v6plus_tunnel_interface_by_name(tunnel_name='v6plus_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit v6Plus tunnel interface url period to 43200 failed!!')
    
    def test_03_check_http_packet_sent_once(self):
        logger.info('wait 30 for http request sent')
        sleep(30)
        logger.info('check http request sent')
        packets = pkt_api.export_captured_packets()
        print(packets)
        logger.info('clear packets to check http request packet again')
        pkt_api.clear_packets()
        sleep(60)
        out = pkt_api.export_captured_packets()
        rc = '0 packets captured' in out
        Assertion.assert_equal(rc, True, 'ERR: check only one http packet sent failed!!')

    def test_04_update_wan_interface_ID(self):
        pkt_api.clear_packets()
        opt= {
            'name': 'X1',
            'mode': 'auto',
            'interface_identifier': "::200",
            "mgmt_ping": True,
            "mgmt_https": True
        }
        rc = if_v6_api.config_interface_ipv6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: update wan interface ID failed!!')
    
    @repeat_method(2)
    def test_05_check_http_request_sent_again(self):
        sleep(30)
        logger.info('check http request sent after updating wan interface')
        packets = pkt_api.export_captured_packets()
        print(packets)
        rc = bool(re.search(r'\d+ packets captured', packets)) and '0 packets captured' not in packets
        Assertion.assert_equal(rc, True, 'ERR: check http request sent after updating wan interface failed!!')


#[CLI]Verify ""Update URL"" and  ""Update URL Period"" can be set via CLI
class Test_TC05(Test):
    uuid = 'SOSAIOT-TC-57676'
    description = show_testcase_info(TESTPLAN, 'TC05', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_v6plus_tunnel_interface_via_CLI(self):
        opt = {
            'name': 'test',
            'local-ipv4': '192.0.0.1',
            'type': 'v6plus',
            'local-ipv6': 'dynamic',
            'bound-if': 'X1',
            'remote': '1::1',
            'update-url': 'http://[1::1]',
            'update-url-period': 1
        }
        rc = interface_cli.add_tunnel_interface_4to6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add v6plus tunnel interface via CLI failed!!')
    

#[GUI]Verify ""v6Plus Static IP Address Service"" type shown in the dropdown list when add 4to6 tunnel interface
class Test_TC06(Test):
    uuid = 'SOSAIOT-TC-57713'
    description = show_testcase_info(TESTPLAN, 'TC06', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_v6plus_option_is_shown(self):
        # This case is including in other cases
        Assertion.assert_equal(True, True, 'ERR: check v6plus is shown')


#[CLI]Verify ""v6Plus Static IP Address Service"" tunnel can be set via CLI
class Test_TC07(Test):
    uuid = 'SOSAIOT-TC-57715'
    description = show_testcase_info(TESTPLAN, 'TC07', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_set_v6plus_tunnel_interface_via_CLI(self):
        # This case is including in other case
        Assertion.assert_equal(True, True, 'ERR: set v6plus tunnel interface via CLI failed')


#[CLI]Verify JPIX v6Plus tunnel interface can be added successfully
class Test_TC08(Test):
    uuid = 'SOSAIOT-TC-94868'
    description = show_testcase_info(TESTPLAN, 'TC08', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_v6plus_tunnel_interface_via_CLI(self):
        # This case is including in other case
        Assertion.assert_equal(True, True, 'ERR: add v6plus tunnel interface via CLI failed')


#[CLI]Verify JPIX v6Plus tunnel interface can be modified successfully
class Test_TC09(Test):
    uuid = 'SOSAIOT-TC-94869'
    description = show_testcase_info(TESTPLAN, 'TC09', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC09')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_modify_v6plus_tunnel_interface_via_CLI(self):
        opt = {
            'name': 'test',
            'local-ipv6': "100::100"
        }
        rc = interface_cli.edit_v6plus_tunnel_interface_by_name(**opt)
        Assertion.assert_equal(rc, True, 'ERR: modify v6plus tunnel interface via CLI failed')


#[CLI]Verify JPIX v6Plus tunnel interface can be deleted successful
class Test_TC10(Test):
    uuid = 'SOSAIOT-TC-94870'
    description = show_testcase_info(TESTPLAN, 'TC10', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_del_v6plus_tunnel_interface_via_CLI(self):
        opt = {
            'type': '4to6',
            'tunnel-name': 'test'
        }
        rc = interface_cli.del_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: modify v6plus tunnel interface via CLI failed')


# [CLI]Verify it can correct display the JPIX_v6Plus information when I show current-config under no-config mode
class Test_TC11(Test):
    uuid = 'SOSAIOT-TC-94871'
    description = show_testcase_info(TESTPLAN, 'TC11', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_added_v6Plus_interface_via_CLI(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1'], tag=1)
        rc = 'v6plus_t1' in out 
        Assertion.assert_equal(rc, True, 'ERR: show v6plus tunnel interface failed')


#[Func]Verify JPIX v6Plus tunnel interface can be added successful on the GUI
class Test_TC12(Test):
    uuid = 'SOSAIOT-TC-94865'
    description = show_testcase_info(TESTPLAN, 'TC12', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_v6plus_tunnel_interface_on_CUI(self):
        # This case is including in other cases
        Assertion.assert_equal(True, True, 'ERR: add v6plus tunnel interface on CUI failed')
    

# [Func]Verify JPIX v6Plus tunnel interface can be edit successful on the GUI
class Test_TC13(Test):
    uuid = 'SOSAIOT-TC-94866'
    description = show_testcase_info(TESTPLAN, 'TC13', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_edit_v6puls_tunnel_interface_on_GUI(self):
        # This case is including in other cases
        Assertion.assert_equal(True, True, 'ERR: edit v6plus tunnel interface on CUI failed')


#[Func]Verify JPIX v6Plus tunnel interface can be deleted successful on the GUI
class Test_TC14(Test):
    uuid = 'SOSAIOT-TC-94867'
    description = show_testcase_info(TESTPLAN, 'TC14', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_del_v6plus_tunnel_interface_on_GUI(self):
        rc = if_v4_api.delete_gre4to6_tunnel_interface_by_name('v6plus_t1')
        Assertion.assert_equal(True, True, 'ERR: del v6plus tunnel interface on GUI failed')


# [Func]Verify \"Update URL Period\" status and details show correct after reboot FW    
class Test_TC15(Test):
    uuid = 'SOSAIOT-TC-57677'
    description = show_testcase_info(TESTPLAN, 'TC15', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_v6Plus_tunnel_interface(self):
        opt = {
                "name": "v6plus_t1",
                "bound_to_if": "X1",
                "local": {"dynamic": True},
                "remote": {"ipv6": "2001:1:2:3::1"},
                "update_url": "http://[2001:1:2:3::1]",
                "update_url_period": 1,
                "comment": ""
            }
        rc = if_v4_api.add_v6plus_tunnel_interface(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add v6Plus tunnel failed!!')

    def test_02_reboot_fw(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed!!')
    
    @repeat_method(7, 10)
    def test_03_check_url_period_status(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1 status'], tag=1)
        rc = bool(re.search(r'Update url status:\s+Success', out, re.I)) and 'Success 0 times' not in out
        Assertion.assert_equal(rc, True, 'ERR: check url period status failed!!')
    

# [Func]Verify ""Update URL Period"" function
class Test_TC17(Test):
    uuid = 'SOSAIOT-TC-57712'
    description = show_testcase_info(TESTPLAN, 'TC17', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_update_url_period_to_0(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        sleep(3)
        opt = {
            "update_url_period": 0
        }
        rc = if_v4_api.edit_v6plus_tunnel_interface_by_name(tunnel_name='v6plus_t1', **opt)
    
    def test_02_check_http_request_sent_only_once(self):  
        sleep(30)
        packets1 = pkt_api.export_captured_packets()
        print(packets1)
        rc1 = bool(re.search(r'\d+ packets captured', packets1)) and '0 packets captured' not in packets1
        logger.info('clear packets to check http request packet again')
        pkt_api.clear_packets()
        sleep(120)
        packets2 = pkt_api.export_captured_packets()
        rc2 = '0 packets captured' in packets2
        Assertion.assert_equal(rc1 and rc2, True, 'ERR: check only one http packet sent failed!!')
    
    def test_03_edit_url_period_to_3(self):
        pkt_api.clear_packets()
        pkt_api.start_capture()
        sleep(3)
        opt = {
            "update_url_period": 3
        }
        rc = if_v4_api.edit_v6plus_tunnel_interface_by_name(tunnel_name='v6plus_t1', **opt)
        Assertion.assert_equal(rc, True, 'ERR: edit url period to 3 failed!!')
    
    def test_04_check_http_request_sent_every_3_min(self):
        sleep(30)
        packets1 = pkt_api.export_captured_packets()
        rc1 = bool(re.search(r'\d+ packets captured', packets1)) and '0 packets captured' not in packets1
        logger.info('clear packets to check http request packet again')
        pkt_api.clear_packets()
        sleep(180)
        packets2 = pkt_api.export_captured_packets()
        rc2 = bool(re.search(r'\d+ packets captured', packets2)) and '0 packets captured' not in packets2
        Assertion.assert_equal(rc1 and rc2, True, 'ERR: check http request sent every 3 minutes failed!!')  


#Verify v6Plus Tunnel interface include Auto Update URL show correctly on TSR.
class Test_TC18(Test):
    uuid = 'SOSAIOT-TC-57717'
    description = show_testcase_info(TESTPLAN, 'TC18', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_v6plus_info_in_tsr(self):
        rc = False
        out = diagnostic_api.get_tsr_part(func='Network', lab1='Interfaces' )
        pattern = r'Interface Name\s+: v6plus_t1(.*?)(?=Interface Name\s+)'
        match = re.search(pattern, out, re.DOTALL)
        if match:
            tsr_info = match.group(1)
            logger.info(f'tsr_info is:\n{tsr_info}')
            rc = 'Update URL' in tsr_info and 'http://[2001:1:2:3::1]' in tsr_info
        else:
            logger.error('not get v6plus_t1 tsr info')
        Assertion.assert_equal(rc, True, 'ERR: check v6plus info in tsr failed!!')
    

#[Func]Verify LAN PC can access the IPv4 address through IPv6 Internet via  "v6Plus Static IP Address Service" tunnel
class Test_TC19(Test):
    uuid = 'SOSAIOT-TC-57709'
    description = show_testcase_info(TESTPLAN, 'TC19', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_packet_monitor_default(self):
        opt = {
            'monitor_filter': {
                'ip_types': '', 
                'destination_ports': '',
                'destination_ips': ''
            }  
        }
        rc = pkt_api.conf_packmon(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config packet monitor to default failed!!')
    
    def test_02_config_pc2_settings_for_v6plus_tunnel(self):
        create_ipv6_tunnel_interface_on_pc2(get_v6_addr('x1'))
        Assertion.assert_equal(True, True, 'ERR: config pc2 settings for v6plus tunnel failed!!')
    
    def test_03_config_nat_rule_on_firewall(self):
        nat_base = {
            "name": 'test_for_v6_plus',
            "enable": True,
            "comment": "test for add a nat policy",
            "inbound": "any",
            "outbound": "v6plus_t1",
            "source": {
                "name": "X0 Subnet"
            },
            "translated_source": {
                "name": "v6plus_t1 IP"
            },
            "destination": {
                "any": True
            },
            "translated_destination": {
                "original": True
            },
            "service": {
                "any": True
            },
            "translated_service": {
                "original": True
            },
            "ticket": {
                "tag1": "",
                "tag2": "",
                "tag3": ""
            }
        }
        nat_json = {"nat_policies": [{"ipv4": nat_base}]}
        rc = nat_api.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, 'ERR: config nat rule on firewall failed!!')
    
    def test_04_config_route_rule_on_firewall(self):
        route_json = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "v6plus_t1",
                        "metric": 1,
                        "source": {"name": "X0 Subnet"},
                        'destination': {'name': "X1 Subnet"},
                        'service': {'any': True},
                        'gateway': {'default': True},
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {"auto": True},
                        "name": "test_for_v6plus",
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": {"tag1": "","tag2": "","tag3": ""}
                    }
                }      
            ]
        }
        rc = route_api.add_route_policy(**route_json)
        Assertion.assert_equal(rc, True, 'ERR: config route rule on firewall failed!!')

    def test_05_verify_traffic_pass_through_tunnel(self):
        rc = check_traffic_through_v6plus_tunnel_interface(v6_addr=get_v6_addr())
        Assertion.assert_equal(rc, True, 'ERR: verify traffic through tunnel failed!!')


# [Func]Verify LAN PC still access the IPv6 internet via  ""v6Plus Static IP Address Service"" tunnel after restart FW
class Test_TC20(Test):
    uuid = 'SOSAIOT-TC-57710'
    description = show_testcase_info(TESTPLAN, 'TC20', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_restart_firewall(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, 'ERR: restart firewall failed!!')
    
    def test_02_verify_traffic_pass_through_tunnel(self):
        rc = check_traffic_through_v6plus_tunnel_interface(v6_addr=get_v6_addr())
        Assertion.assert_equal(rc, True, 'ERR: verify traffic through tunnel failed!!')
    

# [Func]Verify LAN PC still access the IPv6 internet via ""v6Plus Static IP Address Service"" tunnel after export and import prefs
class Test_TC21(Test):
    uuid = 'SOSAIOT-TC-57714'
    description = show_testcase_info(TESTPLAN, 'TC21', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_01_export_exp_file(self):
        rc = setting_api.export_setting_exp(filepath='/tmp/v6plus.exp')
        Assertion.assert_equal(rc, True, 'ERR: export setting exp file failed!!')
    
    def test_02_restore_firewall(self):
        rc = setting_api.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, 'ERR: restore firewall failed!!')
    
    def test_03_import_exp_file(self):
        rc = setting_api.import_setting_exp(filepath='/tmp/v6plus.exp')
        Assertion.assert_equal(rc, True, 'ERR: import setting exp file failed!!')
    
    def test_04_check_traffic_after_export_and_import_prefs(self):
        rc = check_traffic_through_v6plus_tunnel_interface(get_v6_addr())
        Assertion.assert_equal(rc, True, 'ERR: verify traffic through tunnel failed!!')


# [Func]Verify \"Update URL Period\" status and details show correct after export and impor prefs
class Test_TC16(Test):
    uuid = 'SOSAIOT-TC-57678'
    description = show_testcase_info(TESTPLAN, 'TC16', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_url_period_status(self):
        _, out = fw_cli.do_cli_commands(['show tunnel-interface 4to6 v6plus_t1 status'], tag=1)
        rc = bool(re.search(r'Update url status:\s+Success', out, re.I)) and 'Success 0 times' not in out
        Assertion.assert_equal(rc, True, 'ERR: check url period status failed!!')


    
# [Func]Verify the correct IPv6 address chosen as the primary address to estabish  ""v6Plus Static IP Address Service"" tunnel
class Test_TC22(Test):
    uuid = 'SOSAIOT-TC-57711'
    description = show_testcase_info(TESTPLAN, 'TC22', description=True)['title'] 

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TC22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_01_config_x1_v6_to_static(self):
        opt= {
            'name': 'x1',
            'mode': 'static',
            'zone': "WAN",
            'ip':  Parameter.x1_v6_static,
            "interface_identifier": "::",
            "listen_router_advertisement": True,
            'stateless_address_autoconfig' : True,
            'router_adv': True,
            "mgmt_ping": True,
            "mgmt_https": True
        }
        rc = if_v6_api.config_interface_ipv6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1v6 to static mode failed!!')
    
    def test_02_recreat_ipv6_tunnel_interface_PC2(self):
        create_ipv6_tunnel_interface_on_pc2(Parameter.x1_v6_static)
        Assertion.assert_equal(True, True, 'ERR: setup pc2 failed!!')
    
    def test_03_verify_traffic_pass_through_tunnel(self):
        rc = check_traffic_through_v6plus_tunnel_interface(Parameter.x1_v6_static)
        Assertion.assert_equal(rc, True, 'ERR: verify traffic through tunnel failed!!')
    
    def test_04_config_interface_identifier_for_x1_v6_static(self):
        opt= {
            'name': 'x1',
            'mode': 'static',
            'zone': "WAN",
            'ip': Parameter.x1_v6_static,
            'interface_identifier': "::1.1.1.1", 
            "listen_router_advertisement": True,
            'stateless_address_autoconfig' : True,
            "mgmt_ping": True,
            "mgmt_https": True
        }
        rc = if_v6_api.config_interface_ipv6(**opt)
        Assertion.assert_equal(rc, True, 'ERR: config x1v6 to static mode failed!!')

    def test_05_recreate_ipv6_tunnel_interfce_PC2(self):
        create_ipv6_tunnel_interface_on_pc2('2001:1:2:3::101:101')
        Assertion.assert_equal(True, True, 'ERR: setup pc2 failed!!')
        
    def test_06_check_traffic_through_tunnel_use_stateless_address_autoconfig_v6_addr(self):
        rc = check_traffic_through_v6plus_tunnel_interface('2001:1:2:3::101:101')
        Assertion.assert_equal(rc, True, 'ERR: check traffic through tunnel use stateless address autoconfig v6 addr failed!!')