from definition.settings import *
from definition.utils import *
 

#RIP: Verify correct behavior with vlan interfaces
class TestRip_TC78(Test):
    uuid = "SOSAIOT-TC-55726"
    description = show_testcase_info(
        TESTPLAN, '78', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '78')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_rip_on_dut(self):
        rip_dict = {
            'interface': 'X2:V'+ str(X2_VLAN1_ID),
            'mode': 'send_and_receive',
        }      
        resrip = dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on dut: {resrip}")
        Assertion.assert_equal(resrip, True, "ERR: Failed To enable rip on dut")

    def test_02_enable_rip_on_lbox(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
        }
        resrip = lbox_dyrouteapi.set_rip(**rip_dict)
        logger.info(f"config rip on lbox: {resrip}")
        Assertion.assert_equal(resrip, True, "ERR: Failed To enable rip on lbox")

    def test_03_add_AO_and_Route_on_dut(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
                "name": 'test_78',
                "value": "78.1.1.0,255.255.255.0"
            }
        ao_dict.update(ao_update_dict)
        resao = aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_78 on dut: {resao}")
        resgw = aoapi.config_addressobject(**aogw_dict)
        logger.info(f"add ao gw on dut: {resgw}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
                "name": 'test_route_78',
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_78'},
            }
        route_dict.update(rt_update_dict)  
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
        resrt = routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_78 on dut: {resrt}")
        Assertion.assert_equal(resao & resgw & resrt, True, "ERR:add ao and route fail")

    def test_04_add_AO_and_Route_on_lbox(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
                "name": 'test_78',
                "value": "78.2.1.0,255.255.255.0"
            }
        ao_dict.update(ao_update_dict)
        resao = lbox_aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_78 on lbox: {resao}")
        aogw_dict['value'] = '192.1.1.200'
        resgw = lbox_aoapi.config_addressobject(**aogw_dict)
        logger.info(f"add ao gw on lbox: {resgw}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
                "name": 'test_route_78',
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_78'},
            }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
        resrt = lbox_routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_78 on lbox: {resrt}")
        Assertion.assert_equal(resao & resgw & resrt, True, "ERR:add ao and route fail")

    def test_05_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres & clearres, True, "ERR:clear and start packets fail")

    def test_06_redistribute_static_from_rip(self):
        rip_setting_dict = {
            'RedistributeStaticRoutes' : 'on',
        }
        reslbox = lbox_dyrouteapi.rip_config(**rip_setting_dict)
        resdut = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(reslbox&resdut, True, "ERR:Redistribute Static Routes fail")

    def test_07_check_packet(self):
        time.sleep(10)
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')

        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "rip" -r /tmp/packet-c.pcapng -V -T text'
        ripfilteredpackets = PC1_login.send_command(filterripcmd)
        # logger.info(ripfilteredpackets)
        filter_dut = { 
            "out:X2:V" + str(X2_VLAN1_ID),
            "Protocol: UDP (17)",
            'Source port: router (520)',
            'Destination port: router (520)',
            "Version: RIPv2 (2)",
            "Source: 12.1.1.168",
            "Destination: 224.0.0.9",
            "IP Address: 78.1.1.0",
            "Metric: 1"
        }
        filter_lbox = { 
            "in:X2:V" + str(X2_VLAN1_ID),
            "Protocol: UDP (17)",
            'Source port: router (520)',
            'Destination port: router (520)',
            "Version: RIPv2 (2)",
            "Source: 12.1.1.100",
            "Destination: 224.0.0.9",
            "IP Address: 78.2.1.0",
            "Metric: 1"
        }
        res_dut = True if check_packet(ripfilteredpackets,filter_dut) else False
        res_lbox = True if check_packet(ripfilteredpackets,filter_lbox) else False
        CaseParams.res_57 = res_dut & res_lbox
        Assertion.assert_equal(res_dut&res_lbox, True, "ERR:check packets fail")

    def test_09_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "12.1.1.100",
            "78.2.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_dut)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_10_check_route_table(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_lbox = { 
            "12.1.1.168",
            "78.1.1.0/24",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_lbox)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_11_disable_redistribute_static_from_rip(self):
        rip_setting_dict ={
            'RedistributeStaticRoutes' : 'off',
        }
        resdut = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(resdut, True, "ERR:Disable Redistribute Static Routes fail")


# Verify the correct RIP packets. Send and Receive. Receive RIPv2, Send RIPv2.
# the packet captured in TestRip_TC78.test_07_check_packet
class TestRip_TC57(Test):
    uuid = "SOSAIOT-TC-55709"
    description = show_testcase_info(
        TESTPLAN, '57', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '57')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_check_result(self):
        logger.info(f'check rip packets:{CaseParams.res_57}')        
        Assertion.assert_equal( CaseParams.res_57, True, "ERR: check rip packets failed")


#OSPF: Verify correct behavior with vlan interfaces    
class TestOspf_TC117(Test):
    uuid = "SOSAIOT-TC-55653"
    description = show_testcase_info(
        TESTPLAN, '117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres&clearres, True, "ERR:clear and start packets fail")

    def test_02_redistribute_static_from_ospf(self):
        ospf_setting_dict_dut ={
            'router_id' : '12.12.1.168',
            'static_route' : 'on',
            }
        ospf_setting_dict_rbox ={
            'router_id' : '12.12.1.101',
            'static_route' : 'on',
            }
        resdut =dyrouteapi.ospf2_config(**ospf_setting_dict_dut)
        resrbox = rbox_dyrouteapi.ospf2_config(**ospf_setting_dict_rbox)
        Assertion.assert_equal(resrbox&resdut, True, "ERR:Redistribute Static Routes fail")

    def test_03_enable_ospf_on_dut(self):
        ospf_dict = {
            'interface': 'X3:V'+ str(X3_VLAN1_ID),
            'mode': 'enable',
            'area':'0'
        }       
        resospf = dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf on dut: {resospf}")
        Assertion.assert_equal(resospf, True, "ERR: Failed To enable osfp on dut")

    def test_04_enable_ospf_on_rbox(self):
        ospf_dict = {
            'interface': 'X3',
            'mode': 'enable', 
            'area':'0'
        }
        resospf = rbox_dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf2 on rbox: {resospf}")
        Assertion.assert_equal(resospf, True, "ERR: Failed To enable ospf on rbox")

    def test_05_add_AO_and_Route_on_rbox(self):
        ao_dict = copy.deepcopy(ao_base_dict)
        ao_update_dict = {
                "name": 'test_113',
                "value": "5.3.1.0,255.255.255.0"
            }
        ao_dict.update(ao_update_dict)
        resao = rbox_aoapi.config_addressobject(**ao_dict)
        logger.info(f"add ao test_113 on rbox: {resao}")
        aogw_dict['value'] = '192.2.1.200'
        resgw = rbox_aoapi.config_addressobject(**aogw_dict)        
        logger.info(f"add ao gw on rbox: {resgw}")
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
                "name": 'test_route_113',
                "interface": "X0",
                'gateway': {'name': 'X0GW'},
                'destination': {"name": 'test_113'},
            }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}  
        resrt = rbox_routeapi.add_route_policy(**route_policy_dict)
        logger.info(f"add route test_route_113 on lbox: {resrt}")
        Assertion.assert_equal(resao & resgw & resrt, True, "ERR:add ao and route fail")
       
    def test_06_check_packet(self):
        for i in range (20):
            time.sleep(10)
            res = routecli.show_ospf2(mode = 'neighbor')
            if '12.12.1.101' in res and 'Full' in res:
                logger.info(f'ospf neighbors are established')
                break
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        ripfilteredpackets = PC1_login.send_command(filterripcmd)
        
        filter_dut = { 
            "out:X3:V" + str(X3_VLAN1_ID),
            'Source: 13.1.1.168 ',
            'OSPF Version: 2',
            'AS-External-LSA (ASBR) (5)',
            'Link State ID: 78.1.1.0' 
        }
        filter_lbox = { 
            "in:X3:V" + str(X3_VLAN1_ID),
            'Source: 13.1.1.101 ',   
            'OSPF Version: 2',    
            'AS-External-LSA (ASBR) (5)',
            'Link State ID: 5.3.1.0'       
        }
        res_dut = True if check_packet(ripfilteredpackets,filter_dut) else False
        logger.info(f'check packets on FW result: {res_dut }')
        res_lbox = True if check_packet(ripfilteredpackets,filter_lbox) else False
        logger.info(f'check packets of lbox result: {res_lbox}')
        Assertion.assert_equal(res_dut&res_lbox, True, "ERR:check packets fail")

    def test_07_check_route_table(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_dut = { 
            "13.1.1.101",
            "5.3.1.0/24",
            "110",
            'X3:V' + str(X3_VLAN1_ID)
        }
        res = check_dynamic_table(dyntb,filter_dut)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_08_check_route_table_on_rbox(self):
        dyntb = rbox_routecli.show_route_policies(type='dynamic')
        filter_rbox = { 
            "13.1.1.168",
            "78.1.1.0/24",
            "110",
            "X3"
        }
        res = check_dynamic_table(dyntb,filter_rbox)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_09_disable_redistribute_static_from_rip(self):
        ospf_setting_dict ={
            'router_id' : '12.12.1.168',
            'static_route' : 'off',
            }
        resdut =dyrouteapi.ospf2_config(**ospf_setting_dict)
        # resrbox = rbox_dyrouteapi.ospf2_config(**ospf_setting_dict)
        Assertion.assert_equal(resdut, True, "ERR:Disable Redistribute Static Routes fail")


#OSPF:Verify that RIP routes are redistributed to OSPF when the Redistribute RIP Routes check box is turned on  
class TestOspf_TC116(Test):
    uuid = "SOSAIOT-TC-55655"
    description = show_testcase_info(
        TESTPLAN, '116', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '116')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_ospf(self):
        ospf_setting_dict ={
            'router_id' : '12.12.1.168',
            'rip_route' :'on',
            }
        res = dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute rip routes: {res}')
        Assertion.assert_equal(res, True, "ERR:enable Redistribute  rip routes fail")   

    def test_02_check_route_table(self):
        time.sleep(10)
        dyntb = rbox_routecli.show_route_policies(type='dynamic')
        filter_116 = { 
            "78.2.1.0/24" ,
            "13.1.1.168",
            "110",
            "X3"
        }
        res = check_dynamic_table(dyntb,filter_116)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_03_set_ospf(self):
        ospf_setting_dict ={
            'router_id' : '12.12.1.168',
            'rip_route' : 'off',
            }
        res=dyrouteapi.ospf2_config(**ospf_setting_dict)
        logger.info(f'Redistribute RIP Networks: {res}')
        Assertion.assert_equal(res, True, "ERR:disable Redistribute RIP fail")   


#Verify that OSPF routes are redistributed to RIP when the Redistribute OSPF Routes check box is turned on.
class TestRip_TC67(Test):
    uuid = "SOSAIOT-TC-55717"
    description = show_testcase_info(
        TESTPLAN, '67', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '67')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_redistribute_static_from_rip(self):
        rip_setting_dict ={
           'RedistributeOSPFRoutes' : 'on',

        }
        resdut = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(resdut, True, "ERR:Redistribute OSPF Routes fail")

    def test_02_check_route_table(self):
        time.sleep(10)
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_67 = { 
            "5.3.1.0/24" ,
            "12.1.1.168",
            "120",
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_67)
        Assertion.assert_equal(res, True, "ERR:can not find rip route in dynamcic route table")

    def test_03_redistribute_static_from_rip(self):
        rip_setting_dict ={
           'RedistributeOSPFRoutes' : 'off',

        }
        resdut = dyrouteapi.rip_config(**rip_setting_dict)
        Assertion.assert_equal(resdut, True, "ERR:disable Redistribute OSPF Routes fail")


#Correct behavior when configured as Stub area: block Type5 LSAs, block external routes from coming in
class TestOspf_TC120(Test):
    uuid = "SOSAIOT-TC-55714"
    description = show_testcase_info(
        TESTPLAN, '120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_packet(self):
        clearres = pkgapi.clear_packets()
        logger.info(f'clear packets on FW result: {clearres}')
        startres = pkgapi.start_capture()
        logger.info(f'start packets on FW result: {startres}')
        Assertion.assert_equal(clearres&clearres, True, "ERR:clear and start packets fail")

    def test_02_enable_ospf_on_dut(self):
        # Parameter.X3_VLAN1_INDEX = interfaceapi.get_vlan_index('X3',X3_VLAN1_ID)
        ospf_dict = {
            'interface': 'X2:V'+ str(X2_VLAN1_ID),
            'mode': 'enable',
            'area': '2',
            'area_type': 'stub area',
        }
       
        resospf = dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf on dut: {resospf}")
        Assertion.assert_equal(resospf, True, "ERR: Failed To enable osfp on dut")

    def test_03_enable_ospf_on_lbox(self):
        ospf_dict = {
            'interface': 'X2',
            'mode': 'enable',
            'area': '2',
            'area_type':'stub area',
        }
        resospf = lbox_dyrouteapi.set_ospf2(**ospf_dict)
        logger.info(f"config ospf2 on lbox: {resospf}")
        Assertion.assert_equal(resospf, True, "ERR: Failed To enable ospf on lbox")

    def test_04_check_packet(self):
        for i in range (8):
            time.sleep(10)
            res = lbox_routecli.show_ospf2(mode = 'neighbor')
            if '12.12.1.168' in res and 'Full' in res:
                logger.info(f'ospf neighbors are established')
                break
        for i in range (8):
            time.sleep(10)
            res = lbox_routecli.show_ospf2(mode = 'routes')

            if 'IA 0.0.0.0/0' and 'X2' in res:
                logger.info(f'default routes are learn from ospf')
                break
        stopres = pkgapi.stop_capture()
        logger.info(f'stop packets on FW result: {stopres}')
        pkgapi.export_captured_packets_pcapng()
        filterripcmd = 'tshark -R "ospf" -r /tmp/packet-c.pcapng -V -T text'
        ripfilteredpackets = PC1_login.send_command(filterripcmd)
        # logger.info(ripfilteredpackets)
        filter_dut = { 
            "out:X2",
            'Source: 12.1.1.168 ',
            'Link-State Advertisement Type: Summary-LSA (IP network) (3)',
            'Link State ID: 0.0.0.0',
 
        }
        res_dut = True if check_packet(ripfilteredpackets,filter_dut) else False
        logger.info(f'check packets of lbox result: {res_dut}')
        Assertion.assert_equal(res_dut, True, "ERR:check packets fail")


    def test_05_check_route_table_on_lbox(self):
        dyntb = lbox_routecli.show_route_policies(type='dynamic')
        filter_120 = { 
            "12.1.1.168",
            "0.0.0.0/0" ,
            "X2"
        }
        res = check_dynamic_table(dyntb,filter_120)
        Assertion.assert_equal(res, True, "ERR:can not find ospf route in dynamcic route table")

    def test_06_check_route_table_on_dut(self):
        dyntb = routecli.show_route_policies(type='dynamic')
        filter_120 = { 
            "5.3.1.0/24",
            "13.1.1.101",
            "110",
        }
        res = check_dynamic_table(dyntb,filter_120)
        Assertion.assert_equal(res, True, "ERR:can not find ospf route in dynamcic route table")




            



    