from definition.settings import *


class TestStaticRoutes_1(Test):
    uuid = "SOSAIOT-TC-58749"
    description= show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_01_add_static_route(self):
        add_route = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X1",
                        "metric": 1,
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "any": True
                        },
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "default": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {
                            "auto": True
                        },
                        "name": "test",
                        "type": "standard",
                        "priority": 6,
                        "comment": "",
                        "disable_on_interface_down": False,
                        "vpn_precedence": False,
                        "tcp_acceleration": False,
                        "probe": "",
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": "",
                         }
                    }
                }
            ]
        }
        ret = route_obj.add_route_policy( **add_route )
        Assertion.assert_equal(ret, True, "ERR: add static route failed")
        
    def test_02_delete_static_route(self):
        uuid = ''
        routes = route_obj.show_route_policy( version = 'ipv4')
        logger.info(routes)
        for route in routes['route_policies']:
           if route['ipv4']['name'] == "test":
               uuid = route['ipv4']['uuid']
               logger.info(uuid) 
        ret = route_obj.del_route_policy_by_uuid( uuid = uuid, version = 'v4' )
        Assertion.assert_equal(ret, True, "ERR: del static route failed")


class TestStaticRoutes_4(Test):
    uuid = "SOSAIOT-TC-58750"
    description= show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object(self):
        ao_var1 = {
            'name': '40.1.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '40.1.1.0,255.255.255.0',
        }
        ao_var2 = {
            'name': '2.0.0.100',
            'zone': 'LAN',
            'object_type': 'host',
            'value': '2.0.0.100',
        }
        rc1 = ao_obj.config_addressobject(**ao_var1)
        rc2 = ao_obj.config_addressobject(**ao_var2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR:add ao failed")

    def test_02_add_static_route(self):
        add_route = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": {
                            "name": "X0 Subnet"
                        },
                        "destination": {
                            "name": "40.1.1.0"
                        },
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name":"2.0.0.100"
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {
                            "auto": True
                        },
                        "name": "test",
                        "type": "standard",
                        "priority": 6,
                        "comment": "",
                        "disable_on_interface_down": False,
                        "vpn_precedence": False,
                        "tcp_acceleration": False,
                        "probe": "",
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": "",
                         }
                    }
                }
            ]
        }
        ret = route_obj.add_route_policy( **add_route )
        Assertion.assert_equal(ret, True, "ERR: add static route failed")

    def test_03_verify_traffic(self):
        rc = False
        for i in range(5):
            PC3_login.send_command("ping X2_IP -c 5")
            out = os.popen('ping {} -c 5'.format(PC3_ETH2_IP)).read()
            logger.info(out)
            if '100% packet loss' not in out:
                rc = True
                break
            elif i == 4:
                logger.info('Ping failed')
                rc = False
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Verify traffic failed")

    def test_04_delete_static_route(self):
        uuid = ''
        routes = route_obj.show_route_policy( version = 'ipv4')
        logger.info(routes)
        for route in routes['route_policies']:
           if route['ipv4']['name'] == "test":
               uuid = route['ipv4']['uuid']
               logger.info(uuid) 
        ret = route_obj.del_route_policy_by_uuid( uuid = uuid, version = 'v4' )
        Assertion.assert_equal(ret, True, "ERR: del static route failed")

    def test_05_delete_address_object(self):
        ao_var1 = {
            'ip_type': 'ipv4',
            'name': '40.1.1.0'
        } 
        ao_var2 = {
            'ip_type': 'ipv4',
            'name': '2.0.0.100'
        } 
        rc1 = ao_obj.del_addressobject( **ao_var1 )
        rc2 = ao_obj.del_addressobject( **ao_var2 )
        Assertion.assert_equal(rc1 & rc2, True, "ERR: del address object failed")


class TestStaticRoutes_6(Test):
    uuid = "SOSAIOT-TC-58752"
    description= show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Config_X2_to_WAN(self):
        logger.info("config x2 interface... ")
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X2_IP,
            'netmask': MASK,
            'gateway': PC3_ETH0_IP,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_02_add_address_object(self):
        ao_var1 = {
            'name': '40.1.1.0',
            'zone': 'WAN',
            'object_type': 'network',
            'value': '40.1.1.0,255.255.255.0',
        }
        ao_var2 = {
            'name': '2.0.0.100',
            'zone': 'WAN',
            'object_type': 'host',
            'value': '2.0.0.100',
        }
        ao_var3 = {
            'name': '80.1.1.0',
            'zone': 'WAN',
            'object_type': 'network',
            'value': '80.1.1.0,255.255.255.0',
        }
        ao_var4 = {
            'name': '13.0.0.100',
            'zone': 'WAN',
            'object_type': 'host',
            'value': '13.0.0.100',
        }
        rc1 = ao_obj.config_addressobject(**ao_var1)
        rc2 = ao_obj.config_addressobject(**ao_var2)
        rc3 = ao_obj.config_addressobject(**ao_var3)
        rc4 = ao_obj.config_addressobject(**ao_var4)
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4, True, "ERR:add ao failed")

    def test_03_add_static_route(self):
        add_route = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": {
                            "name": "X3 Subnet"
                        },
                        "destination": {
                            "name": "40.1.1.0"
                        },
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name":"2.0.0.100"
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": {
                            "auto": True
                        },
                        "name": "test1",
                        "type": "standard",
                        "priority": 6,
                        "comment": "",
                        "disable_on_interface_down": False,
                        "vpn_precedence": False,
                        "tcp_acceleration": False,
                        "probe": "",
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": "",
                         }
                    }
                }
            ]
        }
        ret1 = route_obj.add_route_policy( **add_route )
        add_route["route_policies"][0]['ipv4']["interface"] = 'X1'
        add_route["route_policies"][0]['ipv4']["name"] = 'test2'
        add_route["route_policies"][0]['ipv4']["source"]["name"] = 'X0 Subnet'
        add_route["route_policies"][0]['ipv4']["destination"]["name"] = '80.1.1.0'
        add_route["route_policies"][0]['ipv4']["gateway"]["name"] = '13.0.0.100'
        ret2 = route_obj.add_route_policy( **add_route )
        Assertion.assert_equal(ret1 & ret2, True, "ERR: add static route2 failed")

    def test_04_verify_traffic(self):
        rc = False
        for i in range(5):
            out1 = os.popen('ping {} -c 5'.format(PC2_ETH2_IP)).read()
            logger.info(out1)
            out2 = PC4_login.send_command('ping {} -c 5'.format(PC3_ETH2_IP))
            logger.info(out2)
            if '100% packet loss' not in out1 and '100% packet loss' not in out2:
                rc = True
                break
            elif i == 4:
                logger.info('Ping failed')
        Assertion.assert_equal(rc, True, "ERR: Verify traffic failed")

    def test_05_delete_static_route(self):
        flag = 0
        uuid = ''
        routes = route_obj.show_route_policy( version = 'ipv4')
        logger.info(routes)
        for route in routes['route_policies']:
            if route['ipv4']['name'] == 'test1' or route['ipv4']['name'] == 'test2':
                uuid = route['ipv4']['uuid']
                logger.info(uuid) 
                ret = route_obj.del_route_policy_by_uuid( uuid = uuid, version = 'v4' )
                if ret == True:
                    flag = flag + 1
            else:
               next
        Assertion.assert_equal(flag, 2, "ERR: del static route failed")

    def test_06_delete_address_object(self):
        ao_var1 = {
            'ip_type': 'ipv4',
            'name': '40.1.1.0'
        } 
        ao_var2 = {
            'ip_type': 'ipv4',
            'name': '2.0.0.100'
        } 
        ao_var3 = {
            'ip_type': 'ipv4',
            'name': '13.0.0.100'
        } 
        ao_var4 = {
            'ip_type': 'ipv4',
            'name': '80.1.1.0'
        } 
        rc1 = ao_obj.del_addressobject( **ao_var1 )
        rc2 = ao_obj.del_addressobject( **ao_var2 )
        rc3 = ao_obj.del_addressobject( **ao_var3 )
        rc4 = ao_obj.del_addressobject( **ao_var4 )
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4, True, "ERR: del address object failed")
