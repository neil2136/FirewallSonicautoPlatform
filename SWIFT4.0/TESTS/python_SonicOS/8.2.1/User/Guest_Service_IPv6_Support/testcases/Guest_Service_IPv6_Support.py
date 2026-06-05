from definition.initial_parameter import *
import re


class Test_Guest_Service_IPv6_Support_007(Test):
    uuid = "SOSAIOT-TC-75395"
    description = show_testcase_info(Parameter.TESTPLAN, '007', description=True)['title']
    jira='GEN7-44060'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '007')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x3_interface(self):
        #setup X3 which connect to linux http server
        logger.info("config x3 interface as dmz zone... ")
        x3 = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")
        X2_IPv6_Interface = {
            'name': 'X3',
            'mode': 'static',
            'zone':'DMZ',
            "ip": Parameter.X3_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc &= interface_ipv6.config_interface_ipv6(**X2_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_enable_guest_service_for_dmz(self):
        zonejson = {
            "zones": [
                {
                    "name": "DMZ",
                    "security_type": "Public",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": True
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name = 'DMZ',**zonejson)
        Assertion.assert_equal(rc, True, "ERR: enable guest service for dmz zone failed")

    @repeat_method(3)
    def test_03_login_with_guest_user(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://[2001:db1::1093]"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/lib/ui_guest.py ' + \
              '-url ' + url + ' -user guest -pwd password'
        out = static_client.send_command(cmd)
        logger.info("login with guest user\n" + out)
        # check guest user status
        user_status = guest_obj.get_user_guest_status()
        logger.info('user status:' + str(user_status))
        Assertion.assert_regular(str(user_status), r'2001:1100',"failed to get guest user status")
        
    # logout guest user
    def test_04_logout_guest_user(self):
        # static_client.send_command('pkill firefox')
        rc = guest_obj.logout_all_guest_user()
        Assertion.assert_equal(rc, True, "ERR: logout guest user failed")

    def test_05_disable_guest_service_for_dmz(self):
        zonejson = {
            "zones": [
                {
                    "name": "DMZ",
                    "security_type": "Public",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": False
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='DMZ', **zonejson)
        Assertion.assert_equal(rc, True, "ERR: disable guest service for dmz zone failed")


class Test_Guest_Service_IPv6_Support_010(Test):
    uuid = "SOSAIOT-TC-75397"
    description = show_testcase_info(Parameter.TESTPLAN, '010', description=True)['title']
    jira='GEN7-44060'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '010')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x4_interface(self):
        # setup X3 which connect to linux http server
        logger.info("config x4 interface as dmz zone... ")
        x4 = {
            'if': 'X4',
            'zone': 'customer',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x4)

        X4_IPv6_Interface = {
            'name': 'X4',
            'mode': 'static',
            'zone': 'customer',
            "ip": Parameter.X4_IPv6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc &= interface_ipv6.config_interface_ipv6(**X4_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 failed")

    def test_02_setup_dibbler_client(self):
        filepath = os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/confs';
        logger.info("dibbler path:\r\n{}".format(filepath))
        dibbler.dibblerstart(dibbler_pc, filepath, 'eth1')
        time.sleep(30)
        # show ifconfig
        for i in range(1,5):
            out = dibbler_client.send_command('ifconfig eth1')
            logger.info("out:\r\n{}".format(out))
            time.sleep(20)
            if re.search(r'2003:db93::', out,re.M):
                break
        Assertion.assert_regular(out, r'2003:db93::',"failed to get ipv6 addr by dibbler")

    def test_03_Add_default_Route_for_PC4(self):
        cmds = (
            'ip -6 addr del 2003:db93::205/128 dev eth1',
            'ip -6 addr add 2003:db93::205/64 dev eth1',
            'route -A inet6 add default gw ' + Parameter.X4_IPv6
        )
        for cmd in cmds:
            dibbler_client.send_command(cmd)
        out = dibbler_client.send_command("ip -6 route show")
        Assertion.assert_regular(out,'default via 2003:db93', "ERR: Config X1 IPv4 failed")


    def test_04_enable_guest_service_for_customer_zone(self):
        zonejson = {
            "zones": [
                {
                    "name": "customer",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": True
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='customer', **zonejson)
        time.sleep(6)
        Assertion.assert_equal(rc, True, "ERR: enable guest service for dmz zone failed")

    @repeat_method(3)
    def test_05_login_with_guest_user(self):
        dibbler_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://[2001:db1::1093]"
        cmd = 'python3 '+ os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Service_IPv6_Support/lib/ui_guest.py '+ \
              '-url ' + url + ' -user guest -pwd password'
        out = dibbler_client.send_command(cmd)
        logger.info("login with guest user\n" + out)
        # check guest user status
        user_status = guest_obj.get_user_guest_status()
        logger.info('user status:' + str(user_status))
        Assertion.assert_regular(str(user_status), r'2003:db93', "failed to get guest user status")

    # logout guest user
    def test_06_logout_with_guest_user(self):
        time.sleep(3)
        dibbler_client.send_command('pkill firefox')
        rc = guest_obj.logout_all_guest_user()
        Assertion.assert_equal(rc, True, "ERR: logout guest user failed")

    def test_07_disable_guest_service_for_custom_zone(self):
        zonejson = {
            "zones": [
                {
                    "name": "customer",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": False
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='customer', **zonejson)
        Assertion.assert_equal(rc, True, "ERR: disable guest service for dmz zone failed")



class Test_Guest_Service_IPv6_Support_042(Test):
    uuid = "SOSAIOT-TC-75399"
    description = show_testcase_info(Parameter.TESTPLAN, '042', description=True)['title']
    jira='GEN7-44060'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '042')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ao_for_lhm_server(self):
        win_v4 = {
            "object_type": "host",
            "name": "win_v4",
            "zone": "WAN",
            "value":Parameter.lhm_server_v4
        }
        rc = ao_obj.config_addressobject(**win_v4)
        win_v6 = {
            "object_type": "host",
            "name": "win_v6",
            "zone": "WAN",
            "value":Parameter.lhm_server_v6
        }
        rc &= ao_obj.config_addressobject(**win_v6)
        time.sleep(6)
        Assertion.assert_equal(rc, True, "ERR: add aos for lhm server failed")

    def test_02_enable_external_guest_service_for_lan(self):
        zonejson = {
            "zones": [{
                "name": "LAN",
                "uuid": "8bdcde73-a017-cd2e-0a00-2cb8ed691cac",
                "security_type": "trusted",
                "guest_services": {
                    "enable": True,
                    "inter_guest": False,
                    "external_auth": {
                        "enable": True,
                        "client_redirect": "https",
                        "web_server_1": {
                            "protocol": "https",
                            "name": "win_v4",
                            "port": 443
                        },
                        "web_server_2": {
                            "protocol": "https",
                            "name": "win_v6",
                            "port": 443
                        },
                        "web_server": {
                            "timeout": 15
                        },
                        "auth_pages": {
                            "web_server_1": {
                                "login": "lhm/default.aspx",
                                "expiration": "lhm/default.aspx",
                                "timeout": "lhm/default.aspx",
                                "max_sessions": "lhm/default.aspx",
                                "traffic_exceeded": "lhm/default.aspx"
                            },
                            "web_server_2": {
                                "login": "lhm/default.aspx",
                                "expiration": "lhm/default.aspx",
                                "timeout": "lhm/default.aspx",
                                "max_sessions": "lhm/default.aspx",
                                "traffic_exceeded": "lhm/default.aspx"
                            }
                        }
                    }
                }
            }]
        }
        rc = zone_obj.edit_zone_object(name='LAN', **zonejson)
        time.sleep(6)
        Assertion.assert_equal(rc, True, "ERR: enable guest service for dmz zone failed")

    def test_03_add_nat_policy(self):
        # add ipv6 nat policy X0----X1 for it is default(ipv4 is default nat policy)
        nat_json = {
            "nat_policies": [{
                "ipv6": {
                    "uuid": "00000000-0000-0001-0800-2cb8ed691cac",
                    "name": "lhm_ipv6",
                    "enable": True,
                    "comment": "",
                    "inbound": "X0",
                    "outbound": "X1",
                    "source": {
                        "any": True
                    },
                    "translated_source": {
                        "name": "X1 IPv6 Primary Static Address"
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
                    }
                }
            }]
        }
        rc = natpolicy_obj.add_nat_policy(**nat_json)
        Assertion.assert_equal(rc, True, "ERR: enable guest service for dmz zone failed")

    @repeat_method(3)
    def test_04_login_with_guest_user(self):
        #windows lhm server
        http_server.send_command("service httpd restart")
        logger.info(http_server.send_command("service httpd status"))
        out = localhost.send_command('curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET https://[2001:db1::1093] | grep "Location"')
        time.sleep(15)
        logger.info(out)
        redirect_url = re.search(r'http://(.*?)/', out, re.M|re.I).group()
        logger.info('redirect ipv6 url : {}'.format(redirect_url))
        rc = localhost.send_command('curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET {}'.format(redirect_url))
        time.sleep(15)
        logger.info(rc)
        Assertion.assert_regular(rc, r'Web Server', "failed to redirect url")

    def test_05_disable_guest_service_for_LAN_zone(self):
        zonejson = {
            "zones": [
                {
                    "name": "customer",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "guest_services": {
                        "enable": False
                    }
                }
            ]
        }
        rc = zone_obj.edit_zone_object(name='LAN', **zonejson)
        Assertion.assert_equal(rc, True, "ERR: disable guest service for dmz zone failed")

    def test_06_delte_nat_policy(self):
        rc = natpolicy_obj.del_nat_policy_by_name(name='lhm_ipv6', version='ipv6')
        Assertion.assert_equal(rc, True, "ERR: del nat policy failed")




