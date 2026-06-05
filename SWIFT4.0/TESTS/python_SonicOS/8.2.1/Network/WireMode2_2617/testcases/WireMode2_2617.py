from definition.init_param import *


class Test_01_WireMode2_2617_tc_1(Test):
    uuid = "SOSAIOT-TC-57520"
    description= show_testcase_info(Parameter.TESTPLAN, '1524587', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524587')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_config_interface_x2_bypass(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass failed")

    def test_03_change_interface_x2_zone(self):
        logger.info("change x2 interface zone... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change interface X2 IPv4 failed")

    def test_04_change_interface_x2_bypass_zone(self):
        logger.info('change interface x2 wire-mode bypass zone...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:change interface x2 wire-mode bypass zone failed")
       
    def test_05_change_interface_x2_zone(self):
        logger.info("change x2 interface zone... ")
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change interface X2 IPv4 failed")

    def test_06_change_interface_x2_bypass_zone(self):
        logger.info('change interface x2 wire-mode bypass zone...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:change interface x2 wire-mode bypass zone failed")
       
    def test_07_change_interface_x2_zone(self):
        logger.info("change x2 interface zone... ")
        x2 = {
            'if': 'X2',
            'zone': 'trustZone',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change interface X2 IPv4 failed")

    def test_08_change_interface_x2_bypass_zone(self):
        logger.info('change interface x2 wire-mode bypass zone...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:change interface x2 wire-mode bypass zone failed")
       
    def test_09_change_interface_x2_zone(self):
        logger.info("change x2 interface zone... ")
        x2 = {
            'if': 'X2',
            'zone': 'publicZone',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change interface X2 IPv4 failed")

    def test_10_change_interface_x2_bypass_zone(self):
        logger.info('change interface x2 wire-mode bypass zone...')
        x2 = {
            'if': 'X2',
            'zone': 'publicZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:change interface x2 wire-mode bypass zone failed")
       
    def test_11_change_interface_x2_zone(self):
        logger.info("change x2 interface zone... ")
        x2 = {
            'if': 'X2',
            'zone': 'WLAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_ping': True,

        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: change interface X2 IPv4 failed")
    
    def test_12_change_interface_x2_bypass_zone(self):
        logger.info('change interface x2 wire-mode bypass zone...')
        x2 = {
            'if': 'X2',
            'zone': 'WLAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WLAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, False, "ERR:change interface x2 wire-mode bypass zone failed")
       
    def test_13_unassign_interface(self):  
        logger.info('config interface x2 normal...')
        rc = interface_obj.unassign_interface(interface = 'X2')
        Assertion.assert_equal(rc, True, "ERR: unassign interface x2 failed")


class Test_02_WireMode2_2617_tc_2(Test):
    uuid = "SOSAIOT-TC-57524"
    description= show_testcase_info(Parameter.TESTPLAN, '1524592', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524592')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_wire_mode_x2_bypass_lan2wan(self):
        logger.info('config interface x2 wire-mode bypass lan to wan...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass lan to wan failed")

    def test_02_wire_mode_x2_bypass_lan2dmz(self):
        logger.info('config interface x2 wire-mode bypass lan to dmz...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass lan to dmz failed")

    def test_03_wire_mode_x2_bypass_lan2Truest(self):
        logger.info('config interface x2 wire-mode bypass lan to Truest...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass lan to Truest failed")

    def test_04_wire_mode_x2_bypass_lan2public(self):
        logger.info('config interface x2 wire-mode bypass lan to public...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass lan to public failed")

    def test_05_wire_mode_x2_bypass_wan2dmz(self):
        logger.info('config interface x2 wire-mode bypass wan to dmz...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass wan to dmz failed")

    def test_06_wire_mode_x2_bypass_wan2Truest(self):
        logger.info('config interface x2 wire-mode bypass wan to Truest...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass wan to Truest failed")

    def test_07_wire_mode_x2_bypass_wan2public(self):
        logger.info('config interface x2 wire-mode bypass wan to public...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass wan to public failed")

    def test_08_wire_mode_x2_bypass_dmz2dmz(self):
        logger.info('config interface x2 wire-mode bypass dmz to dmz...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass dmz to dmz failed")

    def test_09_wire_mode_x2_bypass_dmz2Truest(self):
        logger.info('config interface x2 wire-mode bypass dmz to Truest...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass dmz to Truest failed")

    def test_10_wire_mode_x2_bypass_dmz2public(self):
        logger.info('config interface x2 wire-mode bypass dmz to Truest...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass dmz to public failed")
        
    def test_11_wire_mode_x2_bypass_Truest2Truest(self):
        logger.info('config interface x2 wire-mode bypass Truest to Truest...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass Truest to Truest failed")

    def test_12_wire_mode_x2_bypass_Truest2public(self):
        logger.info('config interface x2 wire-mode bypass Truest to public...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass Truest to public failed")

    def test_13_wire_mode_x2_bypass_public2public(self):
        logger.info('config interface x2 wire-mode bypass public to public...')
        x2 = {
            'if': 'X2',
            'zone': 'publicZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR:config interface x2 wire-mode bypass public to public failed")


class Test_03_WireMode2_2617_tc_12(Test):
    uuid = "SOSAIOT-TC-57521"
    description= show_testcase_info(Parameter.TESTPLAN, '1524589', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524589')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_enable_dmz_zone_ips_gav_anti_spy_app_control(self):
        logger.info('enable dmz zone...')
        dmz_dict = {
            "zones": [
                {
                    "name": "DMZ",
                    "security_type": "public",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "anti_spyware": True,
                    "app_control": True,
                    "create_group_vpn": False,
                    "gateway_anti_virus": True,
                    "intrusion_prevention": True,
                    "ssl_control": False,
                    "sslvpn_access": False,
                    "dpi_ssl_server": False,
                    "dpi_ssl_client": False,
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "enable": False,
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            }
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {
                                "value": 15,
                                "unit": "minutes"
                            },
                            "auto_accept": False
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "footer": {},
                            "header": {}
                        }
                    }
                }
            ]
        }
        rc = zoneObj.edit_zone_object(name='DMZ', **dmz_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable dmz zone failed')

    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping traffic between wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(10)
        output1 = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r'100% packet loss', str(output1), re.S|re.I|re.M) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: ping traffic two wiremode interfaces failed')

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc12.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc12.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc12.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc12.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")



class Test_04_WireMode2_2617_tc_16(Test):
    uuid = "SOSAIOT-TC-57522"
    description= show_testcase_info(Parameter.TESTPLAN, '1524590', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524590')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(10)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if re.search(r"100% packet loss", str(output), re.S|re.I) and \
            re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_03_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc16.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc16.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc16.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc16.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_04_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_05_WireMode2_2617_tc_19(Test):
    uuid = "SOSAIOT-TC-57523"
    description= show_testcase_info(Parameter.TESTPLAN, '1524591', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524591')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        sleep(10)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_03_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_04_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc19.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc19.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc19.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc19.txt", str(output), re.S|re.I)  and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_05_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_06_WireMode2_2617_tc_22(Test):
    uuid = "SOSAIOT-TC-57525"
    description= show_testcase_info(Parameter.TESTPLAN, '1524593', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524593')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_disable_icmp_app_rule(self):
        logger.info('disable icmp app rule...')
        app_rule = {
            "app_rules": {
                "policy": [
                    {
                        "name": "icmp_app",
                        "enable": False,
                        "type": {
                            "ips": True
                        },
                        "address": {
                            "any": True
                        },
                        "exclusion": {
                            "address": {},
                            "service": {}
                        },
                        "match_object": {
                            "object": "icmp_match"
                        },
                        "action_object": "Reset/Drop",
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {}
                        },
                        "schedule": {
                            "always_on": True
                        },
                        "flow_reporting": False,
                        "logging": True,
                        "log": {
                            "individual": False,
                            "redundancy": {
                                "global": True
                            }
                        },
                        "ips_message_format": False,
                        "zone": {
                            "any": True
                        }
                    }
                ]
            }
        }
        rc = appObj.edit_app_rule(name='icmp_app', **app_rule)
        Assertion.assert_equal(rc, True, "ERR: disable icmp app rule failed")

    @repeat_method(3)
    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc22.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc22.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc22.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc22.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_07_WireMode2_2617_tc_27(Test):
    uuid = "SOSAIOT-TC-57526"
    description= show_testcase_info(Parameter.TESTPLAN, '1524594', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524594')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_enable_public_zone_ips_gav_anti_spy_app_control(self):
        logger.info('enable public zone...')
        public_dict = {
            "zones": [
                {
                    "name": "publicZone",
                    "security_type": "public",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "anti_spyware": True,
                    "app_control": True,
                    "create_group_vpn": False,
                    "gateway_anti_virus": True,
                    "intrusion_prevention": True,
                    "ssl_control": False,
                    "sslvpn_access": False,
                    "dpi_ssl_server": False,
                    "dpi_ssl_client": False,
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "enable": False,
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            }
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {
                                "value": 15,
                                "unit": "minutes"
                            },
                            "auto_accept": False
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "footer": {},
                            "header": {}
                        }
                    }
                }
            ]
        }
        rc = zoneObj.edit_zone_object(name='publicZone', **public_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable public zone failed')

    @repeat_method(3)
    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and not\
            re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc27.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc27.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc27.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc27.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_08_WireMode2_2617_tc_29(Test):
    uuid = "SOSAIOT-TC-57527"
    description= show_testcase_info(Parameter.TESTPLAN, '1524595', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524595')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode bypass failed")

    def test_02_enable_trust_zone_ips_gav_anti_spy_app_control(self):
        logger.info('enable trust zone...')
        trust_dict = {
            "zones": [
                {
                    "name": "trustZone",
                    "security_type": "trusted",
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "anti_spyware": True,
                    "app_control": True,
                    "create_group_vpn": False,
                    "interface_trust": False,
                    "gateway_anti_virus": True,
                    "intrusion_prevention": True,
                    "ssl_control": False,
                    "sslvpn_access": False,
                    "dpi_ssl_server": False,
                    "dpi_ssl_client": False,
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "login": "",
                                    "expiration": "",
                                    "timeout": "",
                                    "max_sessions": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            },
                            "enable": False
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {
                                "value": 15,
                                "unit": "minutes"
                            },
                            "auto_accept": False
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "footer": {},
                            "header": {}
                        }
                    }
                }
            ]
        }
        rc = zoneObj.edit_zone_object(name='trustZone', **trust_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable public zone failed')

    @repeat_method(3)
    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        sleep(120)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc29.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc29.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc29.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc29.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and not\
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

class Test_09_WireMode2_2617_tc_46(Test):
    uuid = "SOSAIOT-TC-57528"
    description= show_testcase_info(Parameter.TESTPLAN, '1524596', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524596')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode bypass failed")

    def test_02_disable_dmz_lan_default_access_rule(self):
        logger.info('disable dmz to lan default access rule...')
        ar_dict ={
            "access_rules": [
                {
                    "ipv4": {
                        "name": "Default Access Rule",
                        "comment": "",
                        "action": "deny",
                        "priority": {
                            "manual": {
                                "value": 23
                            }
                        },
                        "enable": False,
                        "from": "DMZ",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "to": "LAN",
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "service": {
                            "any": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "tcp": {
                            "urgent": False,
                            "timeout": 15
                        },
                        "udp": {
                            "timeout": 30
                        },
                        "dpi": True,
                        "dpi_ssl": {
                            "client": True,
                            "server": True
                        },
                        "quality_of_service": {
                            "class_of_service": {},
                            "dscp": {
                                "preserve": True
                            }
                        },
                        "botnet_filter": False,
                        "geo_ip_filter": {
                            "enable": False,
                            "global": True
                        },
                        "logging": True,
                        "flow_reporting": False,
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                        },
                        "sip": False,
                        "h323": False,
                        "fragments": True,
                        "management": False,
                        "max_connections": 100,
                        "packet_monitoring": False,
                        "schedule": {
                            "always_on": True
                        }
                    }
                }
            ]
        }
        uuid = accessRulesObj.get_access_rule_uuid('DMZ','LAN','deny')
        logger.info(uuid)
        url = "/access-rules/ipv4/uuid/{}".format(uuid)
        rc = accessRulesObj.disable_accessrule(url = url, **ar_dict)
        Assertion.assert_equal(rc, True, "ERR: disable dmz to lan default access rule failed")

    @repeat_method(3)
    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc46.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc46.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc46.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc46.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_10_WireMode2_2617_tc_47(Test):
    uuid = "SOSAIOT-TC-57529"
    description= show_testcase_info(Parameter.TESTPLAN, '1524597', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524597')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_disable_wan_trust_default_access_rule(self):
        logger.info('disable wan to trust default access rule...')
        ar_dict ={
            "access_rules": [
                {
                    "ipv4": {
                        "name": "Default Access Rule",
                        "comment": "",
                        "action": "deny",
                        "priority": {
                            "manual": {
                                "value": 21
                            }
                        },
                        "enable": False,
                        "from": "WAN",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "to": "trustZone",
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "service": {
                            "any": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "tcp": {
                            "urgent": False,
                            "timeout": 15
                        },
                        "udp": {
                            "timeout": 30
                        },
                        "dpi": True,
                        "dpi_ssl": {
                            "client": True,
                            "server": True
                        },
                        "quality_of_service": {
                            "class_of_service": {},
                            "dscp": {
                                "preserve": True
                            }
                        },
                        "botnet_filter": False,
                        "geo_ip_filter": {
                            "enable": False,
                            "global": True
                        },
                        "logging": True,
                        "flow_reporting": False,
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                        },
                        "sip": False,
                        "h323": False,
                        "fragments": True,
                        "management": False,
                        "max_connections": 100,
                        "packet_monitoring": False,
                        "schedule": {
                            "always_on": True
                        }
                    }
                }
            ]
        }
        uuid = accessRulesObj.get_access_rule_uuid('WAN','trustZone','deny')
        logger.info(uuid)
        url = "/access-rules/ipv4/uuid/{}".format(uuid)
        rc = accessRulesObj.disable_accessrule(url = url, **ar_dict)
        Assertion.assert_equal(rc, True, "ERR: disable wan to trust default access rule failed")

    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc47.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc47.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc47.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc47.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_11_WireMode2_2617_tc_58(Test):
    uuid = "SOSAIOT-TC-57530"
    description= show_testcase_info(Parameter.TESTPLAN, '1524598', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524598')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")
    
    def test_02_add_pc4_pc3_address_object(self):
        logger.info('add pc4 and pc3 address object...')
        ao_param1 ={
            "object_type": "host",
            "name": "PC4",
            "zone": "publicZone",
            "value": Parameter.PC4_ETH0,
        }
        ao_param2 ={
            "object_type": "host",
            "name": "PC3",
            "zone": "LAN",
            "value": Parameter.PC3_ETH0,
        }
        rc = addrObj.config_addressobject(**ao_param1)
        rc &= addrObj.config_addressobject(**ao_param2)
        Assertion.assert_equal(rc, True, 'ERR: Add mail server address object failed')

    def test_03_add_public_lan_default_access_rule(self):
        logger.info('add public to lan default access rule...')
        ar_dict ={
                "name": "My Rule",
                "comment": "",
                "action": "allow",
                "priority": {
                    "auto": True
                },
                "enable": True,
                "from": "publicZone",
                "source": {
                    "address": {
                        "name": "PC4"
                    },
                    "port": {
                        "any": True
                    }
                },
                "to": "LAN",
                "destination": {
                    "address": {
                        "name": "PC3"
                    }
                },
                "service": {
                    "any": True
                },
                "users": {
                    "included": {
                        "all": True
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                },
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False
                },
                "logging": True,
                "flow_reporting": False,
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "sip": False,
                "h323": False,
                "fragments": True,
                "management": False,
                "max_connections": 100,
                "packet_monitoring": False,
                "reflexive": False     
        } 
        rc = accessRulesObj.config_accessrule(**ar_dict)
        Assertion.assert_equal(rc, True, "ERR: add public to lan default access rule failed")

    def test_04_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_05_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_06_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc58.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc58.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc58.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc58.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_07_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_12_WireMode2_2617_tc_63(Test):
    uuid = "SOSAIOT-TC-57531"
    description= show_testcase_info(Parameter.TESTPLAN, '1524599', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524599')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")
    
    def test_02_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' >  /home/ftp_tc63_1.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc63_1.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc63_1.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc63_1.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

    def test_04_change_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'DMZ',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' >  /home/ftp_tc63_2.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc63_2.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc63_2.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc63_2.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_13_WireMode2_2617_tc_65(Test):
    uuid = "SOSAIOT-TC-57532"
    description= show_testcase_info(Parameter.TESTPLAN, '1524600', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524600')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'trustZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc65_1.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc65_1.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc65_1.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc65_1.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

    def test_04_change_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc65_1.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc65_1.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc65_1.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc65_1.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_14_WireMode2_2617_tc_71(Test):
    uuid = "SOSAIOT-TC-57533"
    description= show_testcase_info(Parameter.TESTPLAN, '1524601', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524601')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode bypass...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode bypass failed")

    def test_02_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc71_1.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc71_1.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc71_1.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc71_1.txt", str(output), re.S|re.I) and not \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and not \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

    def test_04_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_05_enable_wan_trust_default_access_rule(self):
        logger.info('enable wan to trust default access rule...')
        ar_dict ={
            "access_rules": [
                {
                    "ipv4": {
                        "name": "Default Access Rule",
                        "comment": "",
                        "action": "deny",
                        "priority": {
                            "manual": {
                                "value": 21
                            }
                        },
                        "enable": True,
                        "from": "WAN",
                        "source": {
                            "address": {
                                "any": True
                            },
                            "port": {
                                "any": True
                            }
                        },
                        "to": "trustZone",
                        "destination": {
                            "address": {
                                "any": True
                            }
                        },
                        "service": {
                            "any": True
                        },
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {
                                "none": True
                            }
                        },
                        "tcp": {
                            "urgent": False,
                            "timeout": 15
                        },
                        "udp": {
                            "timeout": 30
                        },
                        "dpi": True,
                        "dpi_ssl": {
                            "client": True,
                            "server": True
                        },
                        "quality_of_service": {
                            "class_of_service": {},
                            "dscp": {
                                "preserve": True
                            }
                        },
                        "botnet_filter": False,
                        "geo_ip_filter": {
                            "enable": False,
                            "global": True
                        },
                        "logging": True,
                        "flow_reporting": False,
                        "connection_limit": {
                            "source": {},
                            "destination": {}
                        },
                        "sip": False,
                        "h323": False,
                        "fragments": True,
                        "management": False,
                        "max_connections": 100,
                        "packet_monitoring": False,
                        "schedule": {
                            "always_on": True
                        }
                    }
                }
            ]
        }
        uuid = accessRulesObj.get_access_rule_uuid('WAN','trustZone','deny')
        logger.info(uuid)
        url = "/access-rules/ipv4/uuid/{}".format(uuid)
        rc = accessRulesObj.disable_accessrule(url = url, **ar_dict)
        Assertion.assert_equal(rc, True, "ERR: disable wan to trust default access rule failed")

    def test_06_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc71_2.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc71_2.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc71_2.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc71_2.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_07_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")



class Test_15_WireMode2_2617_tc_72(Test):
    uuid = "SOSAIOT-TC-57534"
    description= show_testcase_info(Parameter.TESTPLAN, '1524602', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524602')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode inspect...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'inspect', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'publicZone',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode inspect failed")

    @repeat_method(3)
    def test_02_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(180)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            not re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")
        
    def test_03_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_04_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc72.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc72.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc72.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc72.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_05_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")


class Test_16_WireMode2_2617_tc_75(Test):
    uuid = "SOSAIOT-TC-57535"
    description= show_testcase_info(Parameter.TESTPLAN, '1524603', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524603')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_restart_fw_and_check_wiremode(self):
        logger.info('restart fw and check wiremode...')
        flag = False
        settingObj.boot_fw(mode = 1)
        output = interface_obj.get_interface_status(name = 'X2')
        logger.info(output)
        if output['interfaces'][0]['ipv4']['ip_assignment']['mode']['wire_mode']['type'] == 'secure':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: restart fw and check wiremode failed")

    def test_03_ping_between_two_wiremode_interfaces(self):
        logger.info('ping between two wiremode interfaces...')
        flag = False
        systemlogObj.clear_log()
        sleep(30)
        output = pc3_ssh.send_command('ping -c 5 {}'.format(PC4_ETH0_IP))
        output2 = pc4_ssh.send_command('ping -c 5 {}'.format(PC3_ETH0_IP))
        if not re.search(r"100% packet loss", str(output), re.S|re.I) and \
            re.search(r'100% packet loss', str(output2), re.S|re.I|re.M): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ping between two wiremode interfaces failed")

    def test_04_http_between_two_wiremode_interfaces(self):
        logger.info('start http between wiremode interfaces')
        flag = False
        output = pc3_ssh.send_command('curl http://{}/index.html'.format(PC4_ETH0_IP))
        if re.search(r"this is http server".format(PC4_ETH0_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start http between wiremode interfaces failed")

    def test_05_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc75.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc75.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc75.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc75.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_06_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

class Test_17_WireMode2_2617_tc_76(Test):
    uuid = "SOSAIOT-TC-57536"
    description= show_testcase_info(Parameter.TESTPLAN, '1524604', description=True)['title']
    # jira = 'GEN7-41228'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524604')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2_wiremode(self):
        logger.info('config interface x2 wire-mode secure...')
        x2 = {
            'if': 'X2',
            'zone': 'trustZone', 
            'mode': 'wire-mode',
            'type': 'secure', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'WAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config interface x2 wire-mode secure failed")

    def test_02_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc76_1.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc76_1.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc76_1.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc76_1.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_03_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")

    def test_04_export_setting_and_change_wiremode(self):
        logger.info('export setting and change wiremode...')
        settingObj.export_setting_exp()
        x2 = {
            'if': 'X2',
            'zone': 'LAN', 
            'mode': 'wire-mode',
            'type': 'bypass', 
            'wire_paired_interface': 'X3',
            'wire_paired_zone': 'LAN',
            'wire_link_propagation': False,
            'stateful_inspection': False,
            'restrict_analysis': False,
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: export setting and change wiremode failed")
    
    def test_05_import_setting(self):
        logger.info('import setting...')
        rc = settingObj.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: import setting failed")

    def test_06_ftp_traffic_between_two_wiremode_interfaces(self):
        logger.info('send ftp traffic from interface pc3 to interface pc4....')
        sleep(15)
        cmd = "echo 'aaaaa' > /home/ftp_tc76_2.txt"
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        pc4_ssh.send_command(cmd)
        systemlogObj.clear_log()
        cmd_pc3 = 'python3 {}'.format(toolPath  + '/upload_or_download_file.py download ftp ') + '/home/ftp_tc76_2.txt '+' root ' + Parameter.PC4_ETH0 + \
             ' /home/ftp_tc76_2.txt '  + ' password 22'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /home'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"6\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+ftp_tc76_2.txt", str(output), re.S|re.I) and \
            re.search(r"Application Firewall Alert.*App Rules Alert", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download file from pc4 use ftp failed")

    @repeat_method(3)
    def test_07_download_virus_from_pc4(self):
        logger.info('download virus from pc4...')
        sleep(15)
        cmd_pc3 = 'ls -l /tmp/klez.h.bin'
        pc3_ssh.send_command(cmd_pc3)
        flag = False
        systemlogObj.clear_log()
        cmd_pc3 = 'curl -k --max-time 80 -o /tmp/klez.h.bin http://{}/klez.h.bin'.format(PC4_ETH0_IP)
        pc3_ssh.send_command(cmd_pc3)
        cmd_pc3 = 'ls -l /tmp'
        logger.info('run cmd in pc3:{}'.format(cmd_pc3))
        output = pc3_ssh.send_command(cmd_pc3)
        logger.info(output)
        output2 = systemlogObj.get_log()
        logger.info(output2)
        if not re.search(r"93322\s\w{3}\s+\d{1,2}\s+(\d{4}|\d{2}:\d{2})\s+klez.h.bin", str(output), re.S|re.I) and \
            re.search(r"Gateway Anti-Virus Alert:", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: download virus from pc4 use ftp failed")
