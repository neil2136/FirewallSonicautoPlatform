from definitions.settings import *


class Test_01_L2_Bridge_Mode_1257(Test):
    uuid = "SOSAIOT-TC-56768"
    description = 'Configuring a bridge pair'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_L2_bridge_pair(self):
        logger.info("Disable failover and LB...")
        params = {
            'enable': False,
        }
        rc = lb_obj.config_failover_settings(**params)
        logger.info("config X1 interface...")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc &= interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

        logger.info("config X2 L2 bridge to X1...")
        x2_l2bridge = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to':'X1',
        }
        rc = interface_obj.config_interface(**x2_l2bridge)
        Assertion.assert_equal(rc, True, "ERR: Config X2 L2 Bridge to X1 failed")

    def test_02_check_interface_status(self):
        flag = False
        rc1 = interface_obj.get_interface_status("X1")
        rc2 = interface_obj.get_interface_status("X2")
        try:
            if rc1['interfaces'][0]['ipv4']['comment'] == 'Bridged to X2' and \
            rc2['interfaces'][0]['ipv4']['comment'] == 'Bridged to X1':
                flag = True
            else:
                logger.info(rc1) 
                logger.info(rc2)
        except:
            logger.error("may failed to get interfaces status...") 
        Assertion.assert_equal(flag, True, "ERR: Check interface status failed")


class Test_33_L2_Bridge_Mode_1257(Test):
    uuid = "SOSAIOT-TC-56772"
    description = 'Traffic is forwarded through the default gateway configured on the firewall'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_L2_bridge_pair(self):
        logger.info("Disable DHCP Server on X0...")
        params = {
            "dhcp_server": {
                "ipv4": {
                    "enable": False
                }
            }
        }
        rc = dhcp_server_obj.config_dhcp_server_settings(**params)
        logger.info("config X2 L2 bridge to X0...")
        x2_l2bridge = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to':'X0',
            #'bridge_route_on_bridge_pair':False,
            'bridge_block_non_ip': True,
        }
        rc &= interface_obj.config_interface(**x2_l2bridge)
        Assertion.assert_equal(rc, True, "ERR: Config X2 L2 Bridge to X0 failed")

    def test_02_add_route_on_PC2_and_PC3(self):
        rc = False
        PC2_login.send_command("route del default gw 10.6.0.2 dev eth3")
        time.sleep(2)
        PC2_login.send_command("route add default gw {} dev eth0".format(ip))
        time.sleep(2)
        PC2_login.send_command("ifdown eth1")
        output = PC2_login.send_command("route -n")
        logger.info("PC1 route info: {} ".center(20,'-').format(output))
        if (re.search(r'0\.0\.0\.0\s+{}'.format(ip),output)):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: add default route to PC2 failed")

        rc = False
        PC3_login.send_command("route add -net 192.168.168.0 netmask 255.255.255.0 eth0")
        output =PC3_login.send_command("route -n")
        logger.info("PC3 route info: {} ".center(20,'-').format(output))
        if (re.search(r'^192\.168\.168\.0.*eth0$',output,re.M)):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: add route on PC3 failed") 

    def test_03_send_traffic_from_LAN_to_WAN(self):
        rc = False
        out = PC2_login.send_command("ping {} -I eth0 -c 10".format(PC3_ETH0_IP))
        logger.info(" {} ".center(20,'-').format(out))
        if re.search(r' 0% packet loss', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: send traffic from X2 PC2 to X1 PC failed")


class Test_35_L2_Bridge_Mode_1257(Test):
    uuid = "SOSAIOT-TC-56773"
    description = 'Radius'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_L2_bridge_pair(self):
        logger.info("config X2 L2 bridge to X0...")
        x2_l2bridge = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to':'X0',
            #'bridge_route_on_bridge_pair':False,
            'bridge_block_non_ip': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_l2bridge)
        Assertion.assert_equal(rc, True, "ERR: Config X2 L2 Bridge to X0 failed")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc &= interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_LAN_WAN_access_rule_everyone(self):
        ret = access_rules_obj.get_accessrule()
        target_rule_uuid = ""
        rc = False
        for rule in ret['access_rules']:
            if 'ipv4' in rule.keys():
                if rule["ipv4"]["name"] == 'Default Access Rule' and rule["ipv4"]['from'] == 'LAN' \
                    and rule["ipv4"]['to'] == 'WAN':
                    target_rule_uuid = rule["ipv4"]['uuid']
                    logger.info("target rule uuid is:" + target_rule_uuid)
                    break
                else:
                    logger.info("can't find the target rule...")  
            else:
                logger.info("can't find the target ipv4 rule...")
        
        if target_rule_uuid:
            access_rules = {
                "uuid": target_rule_uuid,
                "name": "Default Access Rule",
                "enable": True,
                "from": "LAN",
                "to": "WAN",
                "action": "Allow",
                "source": {
                    "address": {
                        "any": True
                    },
                    "port": {
                        "any": True
                    }
                },
                "service": {
                    "any": True
                },
                "destination": {
                    "address": {
                        "any": True
                    }
                },
                "schedule": {
                    "always_on": True
                },
                "users": {
                    "included": {
                        "group": "Everyone"
                    },
                    "excluded": {
                        "none": True
                    }
                },
                "comment": "",
                "fragments": True,
                "logging": True,
                "sip": False,
                "h323": False,
                "flow_reporting": False,
                "botnet_filter": False,
                "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
                "block": {
                    "countries": {
                        "unknown": False
                    }
                },
                "packet_monitoring": False,
                "management": False,
                "max_connections": 100,
                "priority": {
                    "manual": {
                        "value": 13
                    }
                },
                "tcp": {
                    "timeout": 15,
                    "urgent": False
                },
                "udp": {
                    "timeout": 30
                },
                "connection_limit": {
                    "source": {},
                    "destination": {}
                },
                "dpi": True,
                "dpi_ssl": {
                    "client": True,
                    "server": True
                },
                "redirect_unauthenticated_users_to_log_in": True,
                "quality_of_service": {
                    "class_of_service": {},
                    "dscp": {
                        "preserve": True
                    }
                }       
            }
            rc = access_rules_obj.put_accessrule(url="/access-rules/ipv4/uuid/" + target_rule_uuid, **access_rules)
        else:
            logger.info("can't find the target rule uuid...")
        Assertion.assert_equal(rc, True, "ERR: edit default lan to wan access rule to EVERYONE failed...")             

    def test_03_config_users_settings_radius(self):
        params = {
            'auth_method':'radius'
        }
        rc = user_obj.user_method_authentication( **params)
        Assertion.assert_equal(rc, True, "ERR: config users auto method to radius failed")
        add_radius_server_dict = {
            'host': RADIUS_SERVER_IP,
            'secret': RADIUS_PASS,
        }
        flag = False
        rc = radius_obj.add_radius_server(msg=True, **add_radius_server_dict )
        if rc[0]:
            flag = True
        elif 'Already exists' in rc[1]['status']['info'][0]['message']:
            flag = True
            logger.info('Address Object already exists')
        else:
            logger.info('Add {} Failed'.format(ao['name']))
        Assertion.assert_equal(flag, True, "ERR: config users auto method to radius failed")

    def test_04_start_radius_server_on_PC3(self):
        PC3_login.send_command("pkill radiusd")
        time.sleep(2)
        PC3_login.send_command("/usr/sbin/radiusd")
        time.sleep(2)
        out = PC3_login.send_command("pgrep radiusd")
        logger.info("PC3 pgrep radiusd:  {} ".center(20,'-').format(out))
        Assertion.assert_regular(out, '\d+', "ERR: Start radius on PC3 failed")
           
    def test_05_logout_DUT(self):
        ret = fw_api.api_logout()
        Assertion.assert_equal(ret, True, "ERR: logout DUT failed")

    @repeat_method(3)
    def test_06_send_traffic_from_LAN_to_WAN(self):
        fw_api_radius.api_logout()
        rc = False
        out = PC2_login.send_command("ping {} -I eth0 -c 10".format(PC3_ETH0_IP))
        logger.info(" {} ".center(20,'-').format(out))
        if re.search(r'100% packet loss', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR:LAN can access WAN without radius user login,but Not expected") 

    def test_07_radius_login_DUT_via_PC2(self):
        command = 'curl -k -i -H "Content-Type: application/json" -H "Accept: application/json"' + \
            ' -u {}:{} -X POST'.format(RADIUS_USER, RADIUS_PASSWD) + \
            ' --data \'{\"override\": true}\'' +\
            ' https://192.168.168.168/api/sonicos/auth'
        logger.info(command)
        out = PC2_login.send_command(command)
        logger.info(out)
        Assertion.assert_equal(True, True, "ERR: radius login failed")

    @repeat_method(5)
    def test_08_send_traffic_from_LAN_to_WAN(self):
        rc = False
        out = PC2_login.send_command("ping {} -I eth0 -c 10".format(PC3_ETH0_IP))
        logger.info(" {} ".center(20,'-').format(out))
        if re.search(r' 0% packet loss', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: LAN still can't access WAN with radius user login") 

    def test_09_Restore_environment_on_PC(self):
        PC2_login.send_command("service network restart")
        time.sleep(5)
        output1 = PC2_login.send_command("route -n")
        logger.info(output1)
        PC3_login.send_command("route del -net 192.168.168.0 netmask 255.255.255.0 eth0")
        output2 = PC3_login.send_command("route -n")
        logger.info(output2)
        Assertion.assert_equal(True, True, "ERR: restore environment on PC2 PC3 failed") 


class Test_44_L2_Bridge_Mode_1257(Test):
    uuid = "SOSAIOT-TC-56774"
    description = 'Normal interfaces export prefs, Bridged pair interface, import prefs'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_X2_staic_mode(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': X2_IP,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")
    
    def test_02_Export_Perference(self):
        if os.path.exists('/tmp/preference_test.exp'):
            os.remove('/tmp/preference_test.exp')
        rc = setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export settings...")

    def test_03_config_L2_bridge_pair(self):
        logger.info("config X2 L2 bridge to X1...")
        x2_l2bridge = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to':'X1',
        }
        rc = interface_obj.config_interface(**x2_l2bridge)
        Assertion.assert_equal(rc, True, "ERR: Config X2 L2 Bridge to X1 failed")

    def test_04_Import_Prefs(self):
        file = '/tmp/preference_test.exp'
        rc = setting_obj.import_setting_exp(file)
        Assertion.assert_equal(rc, True, "ERR: Import setting file failed.")
        
    def test_05_check_interface_status(self):
        flag = False
        rc1 = interface_obj.get_interface_status("X1")
        rc2 = interface_obj.get_interface_status("X2")
        try:
            if 'static' in rc1['interfaces'][0]['ipv4']['ip_assignment']['mode'].keys() and \
                 'static' in rc2['interfaces'][0]['ipv4']['ip_assignment']['mode'].keys():
                flag = True
            else:
                logger.info(rc1) 
                logger.info(rc2)
        except:
            logger.error("may failed to get interfaces status...") 
        Assertion.assert_equal(flag, True, "ERR: Check interface status failed")
