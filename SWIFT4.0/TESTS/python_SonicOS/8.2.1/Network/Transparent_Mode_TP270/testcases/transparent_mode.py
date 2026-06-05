from definition.settings import *


# Expected: set Transparent Mode for X3 defined in LAN, DMZ or custom zone successful.
class TestZones_TC01(Test):
    uuid = "SOSAIOT-TC-57235"
    description = show_testcase_info(
        Parameter.TESTPLAN, '01', description=True)['title']
    tc1aohost = 'tc01aolan1'
    tc1czname = 'tc01customzone1'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ao_and_custom_zone(self):
        ao_dict = {
            "object_type": "host",
            "name": self.tc1aohost,
            "zone": "LAN",
            "value": '172.50.50.100'
        }
        base_dict = {
            'name': self.tc1czname,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg) else False
        (zoneres, zonemsg) = zonesapi.add_zone_object(msg=True, **trusted_dict)
        if zoneres is False:
            zoneres = True if 'Already exists' in str(zonemsg) else False
        Assertion.assert_equal(aores & zoneres,
                               True,
                               f"ERR: add ao {self.tc1aohost} and zone {self.tc1czname} failed")

    def test_02_edit_x3_to_trans_mode_by_zones(self):
        output = False
        x3_dict = {
            'if': 'X3',
            'comment': 'transmodetest',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'name': self.tc1aohost},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        zones = ['LAN', 'DMZ', self.tc1czname]
        for zone in zones:
            x3_dict['zone'] = zone
            interres = interfacev4api.config_interface(**x3_dict)
            if interres:
                getres = interfacev4api.get_interface_status('X3')
                try:
                    reszone = getres['interfaces'][0]['ipv4']['ip_assignment']['zone']
                    output = True if reszone == zone else False
                except Exception as e:
                    logger.error(f'{repr(e)}---edit x3 to {zone} failed')
            else:
                logger.error(f'config x3 to {zone} failed')
        Assertion.assert_equal(output, True, "ERR: edit interface x3 to trans mode failed")

    def test_03_init_ao_zones_x3_config(self):
        del_ao_dict = {
            'ip_type': 'ipv4',
            'name': self.tc1aohost,
        }
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(self.tc1czname)
        aoapi.del_addressobject(**del_ao_dict)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected:check modified tansparent range is only allowed within WAN subnet.
class TestInterfaces_TC04(Test):
    uuid = "SOSAIOT-TC-57252"
    description = show_testcase_info(
        Parameter.TESTPLAN, '04', description=True)['title']
    tc4aohost = 'tc04aohost101'
    tc4aorange = 'tc04aorange102-120'
    tc4aogroup = 'tc04aogroup1'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ao_and_group(self):
        ao_dict1 = {
            "object_type": "host",
            "name": self.tc4aohost,
            "zone": "LAN",
            "value": '172.50.50.101'
        }
        ao_dict2 = {
            "object_type": "range",
            "name": self.tc4aorange,
            "zone": "DMZ",
            "value": '172.50.50.102,172.50.50.110'
        }
        aogroup_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc4aohost},
                                {"name": self.tc4aorange}
                            ]
                        },
                        "name": self.tc4aogroup
                    }
                }
            ]
        }
        (aores1, aomsg1) = aoapi.config_addressobject(msg=True, **ao_dict1)
        if aores1 is False:
            aores1 = True if 'Already exists' in str(aomsg1) else False
        (aores2, aomsg2) = aoapi.config_addressobject(msg=True, **ao_dict2)
        if aores2 is False:
            aores2 = True if 'Already exists' in str(aomsg2) else False
        (aogres, aogmsg) = aogroupapi.add_addressgroup(msg=True, **aogroup_dict)
        if aogres is False:
            aogres = True if 'Already exists' in str(aogmsg) else False
        Assertion.assert_equal(aores1 & aores2 & aogres, True, 'ERR: add ao and group failed')

    def test_02_edit_x3_to_trans_mode_by_group(self):
        output = False
        x3_dict = {
            'if': 'X3',
            'comment': 'trans mode test',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'group': self.tc4aogroup},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        interres = interfacev4api.config_interface(**x3_dict)
        if interres:
            getres = interfacev4api.get_interface_status('X3')
            try:
                reszone = getres['interfaces'][0]['ipv4']['ip_assignment']['zone']
                output = True if reszone == x3_dict['zone'] else False
            except Exception as e:
                logger.error(repr(e))
        else:
            logger.error('config x3 to transparent mode failed')
        Assertion.assert_equal(output, True, "ERR: edit interface x3 to trans mode failed")

    def test_03_invalid_edit_ao_check(self):
        ao_dict = {
            "address_objects": [
                {
                    "ipv4": {
                        "name": "172.50.50.30-60",
                        "range": {
                            "begin": "172.50.50.30",
                            "end": "172.50.50.60"
                        },
                        "zone": "DMZ"
                    }
                }
            ]
        }
        (aores, aomsg) = aoapi.edit_addressobject(
            object_type="range",
            object_path="name",
            obj_name_uuid=self.tc4aorange,
            ip_type="ipv4",
            json_put=ao_dict,
            msg=True)
        if aores is False:
            aores = True if 'Transparent Range includes WAN IP' in str(aomsg) else False
        Assertion.assert_equal(aores, True, 'ERR: add ao and group failed')

    def test_04_valid_edit_ao_check(self):
        ao_dict = {
            "address_objects": [
                {
                    "ipv4": {
                        "name": "172.50.50.51-60",
                        "range": {
                            "begin": "172.50.50.51",
                            "end": "172.50.50.60"
                        },
                        "zone": "LAN"
                    }
                }
            ]
        }
        (aores, aomsg) = aoapi.edit_addressobject(
            object_type="range",
            object_path="name",
            obj_name_uuid=self.tc4aorange,
            ip_type="ipv4",
            json_put=ao_dict,
            msg=True)
        Assertion.assert_equal(aores, True, 'ERR: add ao and group failed')

    def test_05_init_ao_zones_x3_config(self):
        del_ao_dict1 = {
            'ip_type': 'ipv4',
            'name': self.tc4aohost,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': '172.50.50.51-60',
        }
        interfacev4api.unassign_interface(interface='X3')
        aogroupapi.del_addressgroup(name=self.tc4aogroup)
        aoapi.del_addressobject(**del_ao_dict1)
        aoapi.del_addressobject(**del_ao_dict2)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected: set Transparent Mode for X3 defined in trusted and public zone successful.
class TestZones_TC15(Test):
    uuid = "SOSAIOT-TC-57240"
    description = show_testcase_info(
        Parameter.TESTPLAN, '15', description=True)['title']
    tc15aohost = 'tc15aohost'
    tc15cztrusted = 'tc15cztrusted'
    tc15czpublic = 'tc15czpublic'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ao_and_custom_zone(self):
        ao_dict = {
            "object_type": "host",
            "name": self.tc15aohost,
            "zone": "LAN",
            "value": '172.50.50.111'
        }
        base_dict = {
            'name': self.tc15cztrusted,
            'security_type': 'trusted',
            'interface_trust': True,
        }
        trusted_dict = {"zones": [base_dict]}
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg) else False
        (zoneres1, zonemsg1) = zonesapi.add_zone_object(msg=True, **trusted_dict)
        if zoneres1 is False:
            zoneres1 = True if 'Already exists' in str(zonemsg1) else False
        base_dict['security_type'] = 'public'
        base_dict['name'] = self.tc15czpublic
        (zoneres2, zonemsg2) = zonesapi.add_zone_object(msg=True, **trusted_dict)
        if zoneres2 is False:
            zoneres2 = True if 'Already exists' in str(zonemsg2) else False
        Assertion.assert_equal(aores & zoneres1 & zoneres2, True, "ERR: add ao zone failed")

    def test_02_edit_x3_to_trans_mode_by_zones(self):
        output = False
        x3_dict = {
            'if': 'X3',
            'comment': 'transmodetest',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'name': self.tc15aohost},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        zones = ['LAN', 'DMZ', self.tc15cztrusted, self.tc15czpublic]
        for zone in zones:
            x3_dict['zone'] = zone
            interres = interfacev4api.config_interface(**x3_dict)
            if interres:
                getres = interfacev4api.get_interface_status('X3')
                try:
                    reszone = getres['interfaces'][0]['ipv4']['ip_assignment']['zone']
                    output = True if reszone == zone else False
                except Exception as e:
                    logger.error(f'{repr(e)}---edit x3 to {zone} failed')
            else:
                logger.error(f'config x3 to {zone} failed')
        Assertion.assert_equal(output, True, "ERR: edit interface x3 to trans mode failed")

    def test_03_init_ao_zones_x3_config(self):
        del_ao_dict = {
            'ip_type': 'ipv4',
            'name': self.tc15aohost,
        }
        interfacev4api.unassign_interface(interface='X3')
        zonesapi.delete_zone_object(self.tc15cztrusted)
        zonesapi.delete_zone_object(self.tc15czpublic)
        aoapi.del_addressobject(**del_ao_dict)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected: check icmp include/exclude trans range between X3 and X1.
class TestInterfaces_TC34(Test):
    uuid = "SOSAIOT-TC-57249"
    description = show_testcase_info(
        Parameter.TESTPLAN, '34', description=True)['title']
    tc34aorange = 'tc34aorange'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_range_ao(self):
        ao_dict = {
            "object_type": "range",
            "name": self.tc34aorange,
            "zone": "LAN",
            "value": '172.50.50.90,172.50.50.100'
        }
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg) else False
        Assertion.assert_equal(aores, True, "ERR: add range ao failed")

    def test_02_edit_x3_to_trans_mode(self):
        x3_dict = {
            'if': 'X3',
            'comment': 'trans mode test',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'name': self.tc34aorange},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 to trans mode failed")

    def test_03_edit_log_settings(self):
        log_dict = {
            "log": {
                "event": [
                    {
                        "alert_email": {},
                        "color": {
                            "hex": "0x00000000"
                        },
                        "email_alert": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "id": 598,
                        "ipfix": {},
                        "log_digest": False,
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "name": "LAN ICMP Allow",
                        "priority_level": "alert",
                        "syslog": {},
                        "trap": {}
                    }
                ]
            }
        }
        output = logsettingsapi.edit_event(event_id='598', **log_dict)
        logmonitorapi.clear_log()
        Assertion.assert_equal(output, True, "ERR: edit log event failed")

    def test_04_check_icmp_include_trans_range(self):
        res = PC3_login.send_command('ifconfig eth1 172.50.50.95')
        logger.info(res)
        output = PC3_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        getlogres = logmonitorapi.get_log(id=598)
        output &= True if 'ICMP packet from LAN allowed' in str(getlogres) else False
        Assertion.assert_equal(output, True, "ERR: check icmp log include range failed")

    def test_05_check_icmp_exclude_trans_range(self):
        res = PC3_login.send_command('ifconfig eth1 172.50.50.89')
        logger.info(res)
        output = PC3_login.ping_from_eth(ip=Parameter.X1_IP, eth='eth1')
        getlogres = logmonitorapi.get_log(id=598)
        output &= True if 'ICMP packet from LAN allowed' not in str(getlogres) else False
        Assertion.assert_equal(output, False, "ERR: check icmp log exclude range failed")

    def test_06_init_ao_zones_x3_config(self):
        del_ao_dict = {
            'ip_type': 'ipv4',
            'name': self.tc34aorange,
        }
        interfacev4api.unassign_interface(interface='X3')
        aoapi.del_addressobject(**del_ao_dict)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected: icmp passed in trans range between X3 and X2.
class TestInterfaces_TC58(Test):
    uuid = "SOSAIOT-TC-57254"
    description = show_testcase_info(
        Parameter.TESTPLAN, '58', description=True)['title']
    tc58aorange = 'tc58aorange'
    tc58pc3eth1ip = '172.20.20.65'
    aclname = 'tc58acl'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '58')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_range_ao(self):
        ao_dict = {
            "object_type": "range",
            "name": self.tc58aorange,
            "zone": "WAN",
            "value": '172.20.20.60,172.20.20.70'
        }
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg) else False
        Assertion.assert_equal(aores, True, "ERR: add range ao failed")

    def test_02_configure_dut_failover_and_acl(self):
        ao_dict = {
                "object_type": "host",
                "name": self.tc58pc3eth1ip,
                "zone": "WAN",
                "value": self.tc58pc3eth1ip
        }
        access_rule_dict = {
            'name': self.aclname,
            'from': 'WAN',
            'to': 'LAN',
            'source_addr': {'name': 'X2 Subnet'},
            'dst_addr': {'name': self.tc58pc3eth1ip},
            'service': {'group': 'Ping'},
            'action': 'allow',
        }
        lbres = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if aores is False:
            aores = True if 'Already exists' in str(aomsg) else False
        (aclres, aclmsg) = accessruleapi.add_ipv4_access_rule(msg=True, **access_rule_dict)
        if aclres is False:
            aclres = True if 'Already exists' in str(aclmsg) else False
        Assertion.assert_equal(lbres & aores & aclres, True, "ERR: Config DUT failover and acl failed")

    def test_03_edit_x3_to_trans_mode(self):
        x3_dict = {
            'if': 'X3',
            'comment': 'trans mode test',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'name': self.tc58aorange},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        output = interfacev4api.config_interface(**x3_dict)
        Assertion.assert_equal(output, True, "ERR: edit interface x3 to trans mode failed")

    def test_04_check_icmp_from_lan_to_wan(self):
        PC3_login.send_command(f'ifconfig eth1 {self.tc58pc3eth1ip}')
        output = PC3_login.ping_from_eth(ip=PC2_ETH1_IP, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp from x3 to x2 failed")

    def test_05_check_icmp_from_wan_to_lan(self):
        output = PC2_login.ping_from_eth(ip=self.tc58pc3eth1ip, eth='eth1')
        Assertion.assert_equal(output, True, "ERR: check icmp from x2 to x3 failed")

    def test_06_init_ao_zones_x3_config(self):
        del_ao_dict = {
            'ip_type': 'ipv4',
            'name': self.tc58aorange,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': self.tc58pc3eth1ip,
        }
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X1'
        failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        accessruleapi.del_ipv4_access_rule(self.aclname)
        interfacev4api.unassign_interface(interface='X3')
        aoapi.del_addressobject(**del_ao_dict)
        aoapi.del_addressobject(**del_ao_dict2)
        wlb_conf_dict['failover_lb']['group'][0]['interface'][0]['name'] = 'X1'
        failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)

        PC3_login.send_command(f'ifconfig eth1 {PC3_ETH1_IP}')
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected: host/range/group ao can be added to x3 successful.
class TestAOs_TC63(Test):
    uuid = "SOSAIOT-TC-57256"
    description = show_testcase_info(
        Parameter.TESTPLAN, '63', description=True)['title']
    tc63aohost1 = 'tc63aohost1'
    tc63aohost2 = 'tc63aohost2'
    tc63aorange1 = 'tc63aorange1'
    tc63aogphosts = 'tc63aogphosts'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '63')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_ao_and_group(self):
        ao_host1_dict = {
            "object_type": "host",
            "name": self.tc63aohost1,
            "zone": "DMZ",
            "value": '172.50.50.80'
        }
        ao_host2_dict = {
            "object_type": "host",
            "name": self.tc63aohost2,
            "zone": "DMZ",
            "value": '172.50.50.81'
        }
        ao_range1_dict = {
            "object_type": "range",
            "name": self.tc63aorange1,
            "zone": "DMZ",
            "value": '172.50.50.82,172.50.50.85'
        }
        ao_gphosts_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc63aohost1},
                                {"name": self.tc63aohost2}
                            ]
                        },
                        "name": self.tc63aogphosts
                    }
                }
            ]
        }
        tag = []
        aos = [ao_host1_dict, ao_host2_dict, ao_range1_dict]
        for ao in aos:
            (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao)
            if aores is False:
                aores = True if 'Already exists' in str(aomsg) else False
            tag.append(aores)
            logger.info(f'add ao {ao} result: {aores}')

        (aogres, aogmsg) = aogroupapi.add_addressgroup(msg=True, **ao_gphosts_dict)
        if aogres is False:
            aogres = True if 'Already exists' in str(aogmsg) else False
        tag.append(aogres)
        Assertion.assert_equal(all(tag), True, 'ERR: add ao and group failed')

    def test_02_edit_x3_by_aos(self):
        tag = []
        x3_dict = {
            'if': 'X3',
            'comment': 'tc63 trans mode test',
            'zone': 'DMZ',
            'mode': 'transparent',
            'transparent_range': {'group': self.tc63aogphosts},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        trans_range_list = [
            {'name': self.tc63aohost1},
            {'name': self.tc63aohost2},
            {'name': self.tc63aorange1},
            {'group': self.tc63aogphosts}
        ]
        for rangename in trans_range_list:
            x3_dict['transparent_range'] = rangename
            confres = interfacev4api.config_interface(**x3_dict)
            tag.append(confres)
            if confres is False:
                logger.error(f'config X3 to trans ao {rangename} failed')
        Assertion.assert_equal(all(tag), True, "ERR: edit interface x3 to trans mode failed")
    #
    def test_03_init_ao_zones_x3_config(self):
        del_ao_dict1 = {
            'ip_type': 'ipv4',
            'name': self.tc63aohost1,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': self.tc63aohost2,
        }
        del_ao_dict3 = {
            'ip_type': 'ipv4',
            'name': self.tc63aorange1,
        }
        interfacev4api.unassign_interface(interface='X3')
        aogroupapi.del_addressgroup(name=self.tc63aogphosts)
        aoapi.del_addressobject(**del_ao_dict1)
        aoapi.del_addressobject(**del_ao_dict2)
        aoapi.del_addressobject(**del_ao_dict3)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Expected: check valid/invalid ap group in X3 via 27/29 X1 subnet successful.
class TestAOs_TC67(Test):
    uuid = "SOSAIOT-TC-57257"
    description = show_testcase_info(
        Parameter.TESTPLAN, '67', description=True)['title']
    tc67aohost1 = 'tc67aohost1'
    tc67aorange1 = 'tc67aorange1'
    tc67aorange2 = 'tc67aorange2'
    tc67aogpvalid = 'tc67aogpvalid'
    tc67aogppartvalid = 'tc67aogppartvalid'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_Config_X1_and_aos_in_sub29(self):
        ao_host1_dict = {
            "object_type": "host",
            "name": self.tc67aohost1,
            "zone": "LAN",
            "value": '172.50.50.49'
        }
        ao_range1_dict = {
            "object_type": "range",
            "name": self.tc67aorange1,
            "zone": "DMZ",
            "value": '172.50.50.52,172.50.50.54'
        }
        ao_range2_dict = {
            "object_type": "range",
            "name": self.tc67aorange2,
            "zone": "DMZ",
            "value": '172.50.50.56,172.50.50.58'
        }
        ao_gp1_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc67aohost1},
                                {"name": self.tc67aorange1}
                            ]
                        },
                        "name": self.tc67aogpvalid
                    }
                }
            ]
        }
        ao_gp2_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc67aohost1},
                                {"name": self.tc67aorange2}
                            ]
                        },
                        "name": self.tc67aogppartvalid
                    }
                }
            ]
        }
        tag = []
        aos = [ao_host1_dict, ao_range1_dict, ao_range2_dict]
        for ao in aos:
            (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao)
            if aores is False:
                aores = True if 'Already exists' in str(aomsg) else False
            tag.append(aores)
            logger.info(f'add ao {ao} result: {aores}')

        gps = [ao_gp1_dict, ao_gp2_dict]
        for gp in gps:
            (gpres, gpmsg) = aogroupapi.add_addressgroup(msg=True, **gp)
            if gpres is False:
                gpres = True if 'Already exists' in str(gpmsg) else False
            tag.append(gpres)
            logger.info(f'add group {gp} result: {gpres}')

        x1_static_dict['netmask'] = '255.255.255.248'
        confres = interfacev4api.config_interface(**x1_static_dict)
        tag.append(confres)
        Assertion.assert_equal(all(tag), True, 'ERR: add ao and group failed')

    def test_02_check_29sub_in_valid_invalid_gp_on_x3(self):
        x3_base_dict['transparent_range'] = {'group': self.tc67aogpvalid}
        res1 = interfacev4api.config_interface(**x3_base_dict)
        if res1 is False:
            logger.error('config X3 to valid ao group failed')

        x3_base_dict['transparent_range'] = {'group': self.tc67aogppartvalid}
        (res2, msg) = interfacev4api.config_interface(msg=True, **x3_base_dict)
        if res2 is False:
            exceptmsg = 'Transparent Range not in Primary WAN subnet'
            res2 = True if exceptmsg in str(msg) else False
        else:
            logger.error(f'config X3 to invalid ao group feedback error msg: {msg}')
        Assertion.assert_equal(res1 & res2, True, "ERR: check valid/invalid gp in X3 failed")

    def test_04_init_ao_zones_x3_config(self):
        del_ao_dict1 = {
            'ip_type': 'ipv4',
            'name': self.tc67aohost1,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': self.tc67aorange1,
        }
        del_ao_dict3 = {
            'ip_type': 'ipv4',
            'name': self.tc67aorange2,
        }
        interfacev4api.unassign_interface(interface='X3')
        aogroupapi.del_addressgroup(name=self.tc67aogpvalid)
        aogroupapi.del_addressgroup(name=self.tc67aogppartvalid)
        aoapi.del_addressobject(**del_ao_dict1)
        aoapi.del_addressobject(**del_ao_dict2)
        aoapi.del_addressobject(**del_ao_dict3)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")

    def test_05_Config_X1_and_aos_in_sub27(self):
        ao_host1_dict = {
            "object_type": "host",
            "name": self.tc67aohost1,
            "zone": "LAN",
            "value": '172.50.50.33'
        }
        ao_range1_dict = {
            "object_type": "range",
            "name": self.tc67aorange1,
            "zone": "DMZ",
            "value": '172.50.50.35,172.50.50.38'
        }
        ao_range2_dict = {
            "object_type": "range",
            "name": self.tc67aorange2,
            "zone": "DMZ",
            "value": '172.50.50.63,172.50.50.65'
        }
        ao_gp1_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc67aohost1},
                                {"name": self.tc67aorange1}
                            ]
                        },
                        "name": self.tc67aogpvalid
                    }
                }
            ]
        }
        ao_gp2_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {"name": self.tc67aohost1},
                                {"name": self.tc67aorange2}
                            ]
                        },
                        "name": self.tc67aogppartvalid
                    }
                }
            ]
        }
        tag = []
        aos = [ao_host1_dict, ao_range1_dict, ao_range2_dict]
        for ao in aos:
            (aores, aomsg) = aoapi.config_addressobject(msg=True, **ao)
            if aores is False:
                aores = True if 'Already exists' in str(aomsg) else False
            tag.append(aores)
            logger.info(f'add ao {ao} result: {aores}')

        gps = [ao_gp1_dict, ao_gp2_dict]
        for gp in gps:
            (gpres, gpmsg) = aogroupapi.add_addressgroup(msg=True, **gp)
            if gpres is False:
                gpres = True if 'Already exists' in str(gpmsg) else False
            tag.append(gpres)
            logger.info(f'add group {gp} result: {gpres}')

        x1_static_dict['netmask'] = '255.255.255.224'
        confres = interfacev4api.config_interface(**x1_static_dict)
        tag.append(confres)
        Assertion.assert_equal(all(tag), True, 'ERR: add ao and group failed')

    def test_06_check_27sub_in_valid_invalid_gp_on_x3(self):
        x3_base_dict['transparent_range'] = {'group': self.tc67aogpvalid}
        res1 = interfacev4api.config_interface(**x3_base_dict)
        if res1 is False:
            logger.error('config X3 to valid ao group failed')

        x3_base_dict['transparent_range'] = {'group': self.tc67aogppartvalid}
        (res2, msg) = interfacev4api.config_interface(msg=True, **x3_base_dict)
        if res2 is False:
            exceptmsg = 'Transparent Range not in Primary WAN subnet'
            res2 = True if exceptmsg in str(msg) else False
        else:
            logger.error(f'config X3 to invalid ao group feedback error msg: {msg}')
        Assertion.assert_equal(res1 & res2, True, "ERR: check valid/invalid gp in X3 failed")

    def test_07_init_ao_zones_x3_config(self):
        x1_static_dict['netmask'] = '255.255.255.0'
        interfacev4api.config_interface(**x1_static_dict)
        del_ao_dict1 = {
            'ip_type': 'ipv4',
            'name': self.tc67aohost1,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': self.tc67aorange1,
        }
        del_ao_dict3 = {
            'ip_type': 'ipv4',
            'name': self.tc67aorange2,
        }
        interfacev4api.unassign_interface(interface='X3')
        aogroupapi.del_addressgroup(name=self.tc67aogpvalid)
        aogroupapi.del_addressgroup(name=self.tc67aogppartvalid)
        aoapi.del_addressobject(**del_ao_dict1)
        aoapi.del_addressobject(**del_ao_dict2)
        aoapi.del_addressobject(**del_ao_dict3)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")

