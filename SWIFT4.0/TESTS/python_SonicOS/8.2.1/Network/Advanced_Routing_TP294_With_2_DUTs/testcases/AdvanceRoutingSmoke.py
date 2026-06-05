from definition.settings import *
from definition.utils import *
 

# Advertise Static Routes
class TestRip_TC61(Test):
    uuid = "SOSAIOT-TC-55714"
    description = show_testcase_info(
        TESTPLAN, '61', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '61')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_rip(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
        }
        resdut = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"enable rip on dut : {resdut}")
        reslbox = lbox_dyrouteapi.set_rip(**rip_dict)
        logger.info(f"enable rip on lbox : {reslbox}")
        Assertion.assert_equal(resdut & reslbox, True,
                               "ERR: Failed To enable rip")

    def test_03_add_AO_and_Route_on_dut(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
            "name": 'test_61',
            "value": "61.1.1.0,255.255.255.0"
        }
        ao_dict.update(ao_update_dict)
        resao = aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_61 on dut: {resao}")
        resgw = aoapi.config_addressobject(**aogw_dict)
        logger.info(f"add ao gw on dut: {resgw}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
            "name": 'test_route_61',
            "interface": "X0",
            'gateway': {'name': 'X0GW'},
            'destination': {"name": 'test_61'},
        }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}
        resrt = routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_78 on dut: {resrt}")
        Assertion.assert_equal(resao & resgw & resrt,
                               True, "ERR:add ao and route fail")

    def test_04_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_05_redistribute_static_from_rip(self):
        rip_setting_dict = {
            'RedistributeStaticRoutes': 'on',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        logger.info(f'Redistribute Static Routes on FW result: {res}')
        Assertion.assert_equal(
            res, True, "ERR: Redistribute Static Routes on FW fail")

    def test_06_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        logger.info(filteredpackets)
        filter_61 = {
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.168",
            "Destination: 224.0.0.9",
            "IP Address: 61.1.1.0",
            "Metric: 1"
        }
        res = check_packet(filteredpackets, filter_61)
        Assertion.assert_equal(res, True, "ERR: search packets failed")

    def test_07_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_61 = {
            "12.1.1.168",
            "61.1.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_61)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_08_disable_redistribute_static_from_rip(self):
        rip_setting_dict = {
            'RedistributeStaticRoutes': 'off',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR: Redistribute static routes failed")

    def test_09_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_61 = {
            "61.1.1.0/24",
        }
        res = check_dynamic_table(dyntb, filter_61)
        flag = False if res else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


# Advertise connected Routes
class TestRip_TC63(Test):
    uuid = "SOSAIOT-TC-55716"
    description = show_testcase_info(
        TESTPLAN, '63', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '63')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_redistribute_connected_from_rip(self):
        rip_setting_dict = {
            'RedistributeConnectedNetworks': 'on',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR: Redistribute Connected Networks failed")

    def test_04_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_route = {
            "Source: 12.1.1.168",
            "Destination: 224.0.0.9",
            "IP Address: 12.12.1.0",
            "IP Address: 192.168.168.0",
        }
        res = check_packet(filteredpackets, filter_route)
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_05_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "192.168.168.0/24",
            "12.12.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_06_disable_redistribute_connected_from_rip(self):
        rip_setting_dict = {
            'RedistributeConnectedNetworks': 'off',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR: Disable Redistribute Connected Networks failed")

    @repeat_method(5)
    def test_07_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "192.168.168.0/24",  
        }
        filter_2 = {
            "12.12.1.0/24",   
        }
        res1 = check_dynamic_table(dyntb, filter_1)
        res2 = check_dynamic_table(dyntb, filter_2)
        flag = False if res1|res2  else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


# Originate Default Route
class TestRip_TC59(Test):
    uuid = "SOSAIOT-TC-55711"
    description = show_testcase_info(
        TESTPLAN, '59', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '59')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_redistribute_connected_from_rip(self):
        rip_setting_dict = {
            'OriginateDefaultRoute': 'on',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR:enable Originate Default Route fail")

    def test_04_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_route = {
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.168",
            "Destination: 224.0.0.9",
            "IP Address: 0.0.0.0",
        }
        res = check_packet(filteredpackets, filter_route)
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_05_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "0.0.0.0/0",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_06_disable_redistribute_connected_from_rip(self):
        rip_setting_dict = {
            'OriginateDefaultRoute': 'off',
        }
        res = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(
            res, True, "ERR:disable Originate Default Route fail")

    def test_07_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "0.0.0.0/0", 
        }        
        res1 = check_dynamic_table(dyntb, filter_1)       
        flag = False if res1 else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


# passive
class TestRip_TC76(Test):
    uuid = "SOSAIOT-TC-55724"
    description = show_testcase_info(
        TESTPLAN, '76', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '76')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_enable_passive_on_X0(self):
        rip_dict = {
            'interface': 'X0',
            'mode': 'passvie',
        }
        res = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"enable_passive_on_X0: {res}")
        Assertion.assert_equal(res, True, "ERR:enable_passive_on_X0 fail")
   
    def test_04_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_x2 = {
            'out:X2',
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.168",
            "Destination: 224.0.0.9",
            "IP Address: 192.168.168.0",
            "Metric: 1"
        }
        res_x2 = check_packet(filteredpackets, filter_x2)
        flag_x2 = True if res_x2 else False
        logger.info(f'check packets of X2 result: {flag_x2}')
        filter_x0 = {
            'out:X0',
            'Source port: router (520)',
            'Destination port: router (520)'
        }
        res_x0 = check_packet(filteredpackets, filter_x0)
        flag_x0 = False if res_x0 else True
        logger.info(f'no any rip packects send from passive interface X0 result: {flag_x0}')
        Assertion.assert_equal(flag_x0, True,
                               "ERR: check packets failed")

    def test_05_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "192.168.168.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_06_disable_passive_on_X0(self):
        rip_dict = {
            'interface': 'X0',
            'mode': 'disable',
        }
        res = dyrouteapi.set_rip(**rip_dict)
        Assertion.assert_equal(res, True, "ERR:disable_passive_on_X0 failed")

    @repeat_method(5)
    def test_07_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "192.168.168.0/24", 
        }        
        res1 = check_dynamic_table(dyntb, filter_1)       
        flag = False if res1 else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


# Verify that SonicWALL updates its routing table after receiving a periodic RTU with new RTEs.
class TestRip_TC81(Test):
    uuid = "SOSAIOT-TC-55730"
    description = show_testcase_info(
        TESTPLAN, '81', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '81')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_redistribute_static_from_rip_on_lbox(self):
        rip_setting_dict = {
            'RedistributeStaticRoutes' : 'on',
        }
        reslbox = lbox_dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(reslbox, True, "ERR:Redistribute Static Routes fail")

    def test_03_add_AO_and_Route_on_lbox(self):
        res03 = []
        for i in range (1,4):
            ao_dict = copy.deepcopy(ao_base_dict)
            ao_update_dict = {
                'name': 'test_81_' + str(i),
                'value': '81.2.'+str(i)+'.0,255.255.255.0'
            }
            ao_dict.update(ao_update_dict)
            resao = lbox_aoapi.config_addressobject(**ao_dict)
            res03.append(resao)
            logger.info(f"add ao test_82 on lbox: {resao}")
        
        aogw_dict['value'] = '192.1.1.200'
        resgw = lbox_aoapi.config_addressobject(**aogw_dict)
        res03.append(resgw)
        logger.info(f"add ao gw on lbox: {resgw}")
        
        for i in range (1,4):
            route_dict = copy.deepcopy(route_base_dict)
            rt_update_dict = {
                "name": 'test_route_81_'+ str(i),
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_81_'+ str(i)},
            }
            route_dict.update(rt_update_dict)
            route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
            resrt = lbox_routeapi.add_route_policy(**route_policy_dict)
            res03.append(resrt)
            logger.info(f"add route test_route_82 on lbox: {resrt}")

        Assertion.assert_equal(all(res03), True, "ERR:add ao and route fail")

    def test_04_check_route_table(self):
        time.sleep(10)
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "12.1.1.100",
            "81.2.1.0/24",
            "81.2.2.0/24",
            "81.2.3.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_dut)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")   
        
    def test_05_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres&clearres, True, "ERR:clear and start packets fail")
    
    def test_06_shutdown_X2(self):
        res = interfaceapi.disable_interface('X2')
        logger.info(f"diable X2 on dut: {res}")
        res1 =statuscli.show_status()
        logger.info(f"show_status on dut: {res1}")
        lres = lbox_interfaceapi.disable_interface('X2')
        logger.info(f"diable X2 on lbox: {lres}")
        lres1 = lbox_statuscli.show_status()
        logger.info(f"show_status  on lbox: {lres1}")
        Assertion.assert_equal(res, True, "ERR:diable X2 on lbox fail")
    
    def test_07_add_AO_and_Route_on_lbox(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
                "name": 'test_81_4',
                "value": "81.2.4.0,255.255.255.0"
            }
        ao_dict.update(ao_update_dict)
        resao = lbox_aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_82 on lbox: {resao}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
                "name": 'test_route_81_4',
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_81_4'},
            }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
        resrt = lbox_routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_82 on lbox: {resrt}")
        Assertion.assert_equal(resao & resrt, True, "ERR:add ao and route fail")
    
    def test_08_noshutdown_X2(self):
        time.sleep(20)
        res = interfaceapi.enable_interface('X2')
        logger.info(f"enable X2 on dut: {res}")
        res1 = statuscli.show_status()
        logger.info(f"show_status on dut: {res1}")
        lres = lbox_interfaceapi.enable_interface('X2')
        logger.info(f"enable X2 on lbox: {lres}")
        lres1 = lbox_statuscli.show_status()
        logger.info(f"show_status on lbox: {lres1}")
        Assertion.assert_equal(res, True, "ERR:enable X2 on lbox fail")

    def test_09_check_packet(self):
        time.sleep(5)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        logger.info(filteredpackets)
        filter_lbox = { 
            "in:X2",
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.100",
            "Destination: 224.0.0.9" ,
            "IP Address: 81.2.1.0" ,
            "IP Address: 81.2.2.0" ,
            "IP Address: 81.2.3.0" ,
            "IP Address: 81.2.4.0" ,
            "Metric: 1"
        }
        res =  check_packet(filteredpackets,filter_lbox) 
        Assertion.assert_equal(res, True, "ERR:check packet fail")

    def test_10_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "12.1.1.100",
            "81.2.1.0/24",
            "81.2.2.0/24",
            "81.2.3.0/24",
            "81.2.4.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_dut)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")


#RIP: Verify that SonicWALL updates its routing table after receiving a triggered update with static RTEs.
class TestRip_TC82(Test):
    uuid = "SOSAIOT-TC-55731"
    description = show_testcase_info(
        TESTPLAN, '82', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '82')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_03_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres&clearres, True, "ERR:clear and start packets fail")
    
    def test_04_add_AO_and_Route_on_lbox(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
                "name": 'test_82',
                "value": "82.2.1.0,255.255.255.0"
            }
        ao_dict.update(ao_update_dict)
        resao = lbox_aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_82 on lbox: {resao}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
                "name": 'test_route_82',
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_82'},
            }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
        resrt = lbox_routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_82 on lbox: {resrt}")
        Assertion.assert_equal(resao & resrt, True, "ERR:add ao and route fail")

    def test_05_check_packet(self):
        time.sleep(20)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        logger.info(filteredpackets)
        filter_lbox = { 
            "in:X2",
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.100",
            "Destination: 224.0.0.9" ,
            "IP Address: 82.2.1.0" ,
            "Metric: 1"
        }
        filter_out = '81.2.1.0'
        res =  check_packet(filteredpackets,filter_lbox,filter_out) 
        Assertion.assert_equal(res, True, "ERR:check packet fail")

    def test_06_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "12.1.1.100",
            "81.2.1.0/24",
            "81.2.2.0/24",
            "81.2.3.0/24",
            "81.2.4.0/24",
            "82.2.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_dut)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")


# TC85 Verify that SonicWALL deletes an entry from its routing table 
# after receiving an infinite route with a metric of 16.
class TestRip_TC85(Test):
    uuid = "SOSAIOT-TC-55732"
    description = show_testcase_info(
        TESTPLAN, '85', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '85')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres&clearres, True, "ERR:clear and start packets fail")

    def test_03_delete_route_in_lbox(self): 
        res = lbox_routecli.del_route_policies(version='ipv4')
        dyntb = routecli.show_route_policies(type='static')
        Assertion.assert_equal(res, True, "ERR:delete route fail")

    def test_04_check_packet(self):
        time.sleep(20)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        logger.info(filteredpackets)
        filter_lbox = { 
            "in:X2",
            'Source port: router (520)',
            'Destination port: router (520)',
            "Source: 12.1.1.100",
            "Destination: 224.0.0.9" ,
            "IP Address: 81.2.1.0" ,
            "IP Address: 81.2.2.0" ,
            "IP Address: 81.2.3.0" ,
            "IP Address: 81.2.4.0" ,
            "IP Address: 82.2.1.0" ,
            "Metric: 16"
            }
        res = check_packet(filteredpackets,filter_lbox)
        logger.info(f'check packets of lbox result: {res}')
        Assertion.assert_equal(res, True, "ERR:check packets fail")

    def test_05_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "12.1.1.100",
            "81.2.1.0/24",
            "81.2.2.0/24",
            "81.2.3.0/24",
            "81.2.4.0/24",
            "82.2.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_dut)
        flag = False if res else True
        Assertion.assert_equal(flag, True, "ERR:can not find rip route in dynamcic route table")

    def test_06_diable_redistribute_static_from_rip(self):
        rip_setting_dict ={
            'RedistributeStaticRoutes' : 'off',
        }
        reslbox = lbox_dyrouteapi.rip_config(**rip_setting_dict)
        logger.info(f'disable Redistribute Static Routes:{reslbox}')
        Assertion.assert_equal(reslbox, True, "ERR:disable Redistribute Static Routes from lbox fail")

    def test_07_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "OSPF, RIP, or BGP Route",  
        }
        filter_2 = {
            "120",   
        }
        res1 = check_dynamic_table(dyntb, filter_1)
        res2 = check_dynamic_table(dyntb, filter_2)
        flag = False if res1|res2  else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")

   
# Verify that SonicWALL doesn't advertise any RTUs when the RIP feature is disabled.
class TestRip_TC46(Test):
    uuid = "SOSAIOT-TC-55697"
    description = show_testcase_info(
        TESTPLAN, '46', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_disable_rip_on_x2(self):
        rip_dict = {
            'interface': 'X2',
            'mode':  'disable',
        }
        resdut = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"disable rip on dut : {resdut}")
        reslbox = lbox_dyrouteapi.set_rip(**rip_dict)
        logger.info(f"disable rip on lbox : {reslbox}")
        Assertion.assert_equal(resdut & reslbox, True,
                               "ERR: Failed To disable rip")

    def test_04_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_route = {
            "out:X2",
            'Source port: router (520)',
            'Destination port: router (520)'
        }
        res = check_packet(filteredpackets, filter_route)
        flag = False if res else True
        Assertion.assert_equal(flag, True, "ERR: check packets failed")

    def test_05_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "120",  
        }
        filter_2 = {
            "OSPF, RIP, or BGP Route",   
        }
        res1 = check_dynamic_table(dyntb, filter_1)
        res2 = check_dynamic_table(dyntb, filter_2)
        flag = False if res1|res2  else True
        Assertion.assert_equal(
            flag, True, "ERR:can not find rip route in dynamcic route table")


#TC111,103,143,110 are relevent 
#redistribute static
class TestOspf_TC111(Test):
    uuid = "SOSAIOT-TC-55651"
    description = show_testcase_info(
        TESTPLAN, '111', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '111')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'static_route': 'on',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute Static Networks: {res}')
        Assertion.assert_equal(
            res, True, "ERR:enable Redistribute Static Networks fail")

    def test_03_enable_ospf_on_dut(self):
        ospf_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
        }
        resdut = dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf on dut: {resdut}")
        reslbox = lbox_dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf2 on lbox: {reslbox}")
        Assertion.assert_equal(resdut & reslbox, True,
                               "ERR: Failed to enable ospf")

    def test_04_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_05_check_packet(self):        
        for i in range(8):
            time.sleep(10)
            res = lbox_routecli.show_ospf2(mode='neighbor')
            if '12.12.1.168' in res and 'Full' in res:
                logger.info(f'ospf neighbors are established')
                break

        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_route = {
            ' AS-External-LSA (ASBR) (5)',
            'Link State ID: 61.1.1.0'
        }
        res = check_packet(filteredpackets, filter_route)
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_06_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "61.1.1.0/24",
            "12.1.1.168",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find OSPF route in dynamcic route table")


# passive
class TestOspf_TC103(Test):
    uuid = "SOSAIOT-TC-55646"
    # jira = 'GEN7-38192'
    description = show_testcase_info(
        TESTPLAN, '103', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '103')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_enable_passive_ospf_dut(self):
        ospf_dict = {
            'interface': 'X0',
            'mode': 'passive',
        }
        res = dyrouteapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(
            res, True, "ERR: Failed To enable_passive_ospf on dut")

    def test_04_check_packet_X2(self):
        time.sleep(30)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_X2 = {
            "out:X2",
            "OSPF Version: 2",
            "Protocol: OSPF IGP (89)",
            'Link-State Advertisement Type: Router-LSA (1)',
            'IP network/subnet number: 192.168.168.0'
        }           
        res_x2 = check_packet(filteredpackets, filter_X2)
        flag_x2 = True if res_x2 else False
        logger.info(f'check packets of X2 result: {flag_x2}')            
        Assertion.assert_equal(flag_x2, True, "ERR: search packets failed")
    
    def test_05_check_packet_X0(self):
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_X0 = {
            "out:X0",
            "OSPF Version: 2",
            "Protocol: OSPF IGP (89)",
        }    
        res_x0 = check_packet(filteredpackets, filter_X0)
        flag_x0 = False if res_x0 else True
        logger.info(f'no any ospf packects send from passive interface X0 result: {flag_x0}')
        Assertion.assert_equal( True, True, "ERR: search packets failed")

    def test_06_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "192.168.168.0/24",
            "12.1.1.168",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")


# reboot
class TestOspf_TC143(Test):
    uuid = "SOSAIOT-TC-55665"
    description = show_testcase_info(
        TESTPLAN, '143', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '143')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_show_ospf_before_reboot(self):
        CaseParams.res_143 = routecli.show_ospf2(mode='')        
        Assertion.assert_equal(True, True, f"ERR: show_ospf failed.")

    def test_03_reboot(self):
        rc = settingapi.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    def test_04_show_ospf_after_reboot(self):
        for i in range(3):
            time.sleep(10)
            res = lbox_routecli.show_ospf2(mode='neighbor')
            if '12.12.1.168' and 'Full' in res:
                logger.info(f'ospf neighbors are established')
                break
        res = routecli.show_ospf2(mode='')
        logger.info(f"show ospf configuration before reboot is : \n{CaseParams.res_143}")
        logger.info(f"show ospf configuration after reboot is : \n{res}")
        flag = compare_ospf_info(CaseParams.res_143, res)
        Assertion.assert_equal(flag, True, f"ERR: show_ospf failed.")

    def test_05_disable_passive_ospf_dut(self):
        ospf_dict = {
            'interface': 'X0',
            'mode': 'disable',
        }
        res = dyrouteapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(
            res, True, "ERR: Failed To enable_passive_ospf on dut")

    def test_06_check_route_table(self):
        time.sleep(25)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "192.168.168.0/24",
        }
        res = check_dynamic_table(dyntb, filter_1)
        flag = False if res  else True
        Assertion.assert_equal(
            flag, True, "ERR: find ospf route in dynamcic route table")


#disable redistribute static
class TestOspf_TC110(Test):
    uuid = "SOSAIOT-TC-55650"
    description = show_testcase_info(
        TESTPLAN, '110', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'static_route': 'off',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'disable Redistribute Static Networks: {res}')
        Assertion.assert_equal(
            res, True, "ERR:disable Redistribute Static Networks fail")

    def test_03_check_route_table(self):
        time.sleep(25)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "61.1.1.0/24",  
        }
        res1 = check_dynamic_table(dyntb, filter_1)
        flag = False if res1 else True
        Assertion.assert_equal(
            flag, True, "ERR: find OSPF route in dynamcic route table")

# Redistribute Connected Networks
class TestOspf_TC113(Test):
    uuid = "SOSAIOT-TC-55653"
    description = show_testcase_info(
        TESTPLAN, '113', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '113')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'connect_network': 'on',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute Connected Networks: {res}')
        Assertion.assert_equal(
            res, True, "ERR:enable Redistribute Connected Networks fail")

    def test_04_check_packet(self):
        for i in range(3):
            time.sleep(10)
            res = lbox_routecli.show_ospf2(mode='neighbor')
            if '12.12.1.168' in res and 'Full' in res:
                logger.info(f'ospf neighbors are established')
                break
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        # logger.info(filteredpackets)
        filter_route = {
            'OSPF Version: 2',
            'AS-External-LSA (ASBR) (5)',
            'Link State ID: 12.12.1.0',
            'Link State ID: 192.168.168.0',
        }
        res = check_packet(filteredpackets, filter_route)
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_07_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "192.168.168.0/24",
            "12.12.1.0/24",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")


# disable/enable interface
class TestOspf_TC114(Test):
    uuid = "SOSAIOT-TC-55654"
    description = show_testcase_info(
        TESTPLAN, '114', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '114')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_shutdown_X1(self):
        # rc = interfacecli.shutdown_interface("X1")
        # Assertion.assert_equal(rc, True, "ERR:shutdown X1 failed")
        res = interfaceapi.disable_interface('X1')
        logger.info(f"diable X1 on dut: {res}")
        res1 =statuscli.show_status()
        logger.info(f"show_status on dut: {res1}")
        lres = lbox_interfaceapi.disable_interface('X1')
        logger.info(f"diable X1 on lbox: {lres}")
        lres1 = lbox_statuscli.show_status()
        logger.info(f"show_status  on lbox: {lres1}")
        Assertion.assert_equal(res, True, "ERR:diable X1 on lbox fail")

    
    @repeat_method(20)
    def test_04_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_in = {
            "192.168.168.0/24",
            "110",
            "X2"
        }
        filter_not = "12.12.1.0/24"
        flag = True if filter_not not in dyntb else False
        res = check_dynamic_table(dyntb, filter_in)
        Assertion.assert_equal(
            res & flag, True, "ERR:can not find rip route in dynamcic route table")

    def test_05_no_shutdown_X1(self):
        # noshutdownres = interfacecli.no_shutdown_interface("X1")
        # logger.info('no shutdown X1 :'.format(noshutdownres))
        # Assertion.assert_equal(noshutdownres, True,
        #                        "ERR:no shutdown X1 failed")
        time.sleep(20)
        res = interfaceapi.enable_interface('X1')
        logger.info(f"enable X1 on dut: {res}")
        res1 = statuscli.show_status()
        logger.info(f"show_status on dut: {res1}")
        lres = lbox_interfaceapi.enable_interface('X1')
        logger.info(f"enable X1 on lbox: {lres}")
        lres1 = lbox_statuscli.show_status()
        logger.info(f"show_status on lbox: {lres1}")
        Assertion.assert_equal(res, True, "ERR:enable X1 on lbox fail")

    @repeat_method(20)
    def test_06_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_in = {
            "192.168.168.0/24",
            "12.12.1.0/24",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_in)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_07_change_X1_netmask(self):
        x1_static_114 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask':'255.255.240.0',
            'gateway':Parameter.X1_GW,
            'dns1':  Parameter.X1_DNS1,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static_114)
        logger.info('change X1 netmask :'.format(rc))
        Assertion.assert_equal(rc, True,
                               "ERR:change X1 netmask failed")

    @repeat_method(20)
    def test_08_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_in = {
            "192.168.168.0/24",
            "12.12.0.0/20",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_in)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")

    def test_09_change_X1_ip(self):
        x1_static_114 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '12.12.114.1',
            'netmask':'255.255.255.0',
            'gateway':Parameter.X1_GW,
            'dns1':  Parameter.X1_DNS1,
            'management https': True,
            'management ping': True,
            'management snmp': True,
            'management ssh': True,
            'user_login_https': True,
        }
        rc = interfaceapi.config_interface(**x1_static_114)
        logger.info('change X1 ip :'.format(rc))
        Assertion.assert_equal(rc, True,
                               "ERR:change X1 ip failed")

    @repeat_method(20)
    def test_10_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_in = {
            "192.168.168.0/24",
            "12.12.114.0/24",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_in)
        Assertion.assert_equal(
            res, True, "ERR:can not find rip route in dynamcic route table")


# disable connected
#RedistributeConnectedNetworks turn on in TestOspf_TC113
class TestOspf_TC112(Test):
    uuid = "SOSAIOT-TC-55652"
    description = show_testcase_info(
        TESTPLAN, '112', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '112')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'connect_network': 'off',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'disable Redistribute Connected Networks: {res}')
        Assertion.assert_equal(
            res, True, "ERR:disable Redistribute Connected Networks fail")

    def test_03_check_route_table(self):
        time.sleep(25)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_1 = {
            "192.168.168.0/24",
        }
        res = check_dynamic_table(dyntb, filter_1)
        flag = False if res  else True
        Assertion.assert_equal(
            flag, True, "ERR: find ospf route in dynamcic route table")

# redistribute default
class TestOspf_TC105(Test):
    uuid = "SOSAIOT-TC-55648"
    description = show_testcase_info(
        TESTPLAN, '105', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '105')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True,
                               "ERR:clear and start packets fail")

    def test_03_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'default_route': 'always',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute Default Route: {res}')
        Assertion.assert_equal(
            res, True, "ERR:enable Redistribute Default Routefail")

    def test_04_check_packet(self):
        time.sleep(30)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        filteredpackets = PC1_login.send_command(filterripcmd)
        filter_route = {
            "OSPF Version: 2",
            'AS-External-LSA (ASBR) (5)',
            'Link State ID: 0.0.0.0'
        }
        res = check_packet(filteredpackets, filter_route)
        flag = True if res else False
        Assertion.assert_equal(flag, True, "ERR: search packets failed")

    def test_05_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_63 = {
            "0.0.0.0/0",
            "12.1.1.168",
            "110",
            "X2"
        }
        res = check_dynamic_table(dyntb, filter_63)
        Assertion.assert_equal(
            res, True, "ERR:can not find ospf route in dynamcic route table")


class TestOspf_TC104(Test):
    uuid = "SOSAIOT-TC-55647"
    description = show_testcase_info(
        TESTPLAN, '104', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_ospf(self):
        ospf_setting_dict = {
            'router_id': '12.12.1.168',
            'default_route': 'never',
        }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'disable Originate Default Route: {res}')
        Assertion.assert_equal(
            res, True, "ERR:disable Originate Default Route fail")

    def test_03_check_route_table(self):
        time.sleep(25)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        res = re.search("No entries(.*) No entries.", dyntb, re.S)
        flag = True if res else False
        Assertion.assert_equal(
            flag, True, "ERR:can not find ospf route in dynamcic route table")


# clear ip ospf process
class TestOspf_TC142(Test):
    uuid = "SOSAIOT-TC-55664"
    description = show_testcase_info(
        TESTPLAN, '142', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '142')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_ospf_neighbors(self):
        resnb = routecli.show_ospf2(mode='neighbor')
        res = True if '192.1.1.100' in resnb and 'Full' in resnb else False
        logger.info(f'ospf neighbors are established: {res}')
        Assertion.assert_equal(
            res, True, "ERR:ospf neighbors established fail")

    def test_03_clear_ip_ospf_process(self):
        resnb = routecli.clear_ospf()
        logger.info(f'ospf process is cleared: {resnb}')
        Assertion.assert_equal(
            resnb, True, "ERR:ospf process cleared fail")

    def test_04_check_ospf_neighbors(self):
        time.sleep(15)
        resnb = routecli.show_ospf2(mode='neighbor')
        res = True if '192.1.1.100' in resnb and 'Full' in resnb else False           
        logger.info(f'ospf neighbors are established: {res}')
        Assertion.assert_equal(
            res, True, "ERR:ospf neighbors established fail")
