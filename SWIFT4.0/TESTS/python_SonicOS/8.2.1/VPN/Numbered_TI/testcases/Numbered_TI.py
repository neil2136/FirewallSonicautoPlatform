from unicodedata import name
from definition.settings import *


# add  vpn tunnel policy and add Tunnel interface
class TestNumbered_TI_01(Test):
    uuid = "SOSAIOT-TC-54511"
    description = show_testcase_info(TESTPLAN, "01", description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_01_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.') 

    def test_01_02_add_Tunnel_interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_IF_IP_LOCAL
        ref2["ip"] =  VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
        rc = Linterface.add_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Add Remote Vpn Tunnel Interface'))
        rc &= Rinterface.add_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

    def test_01_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")


class TestNumbered_TI_02(Test):
    uuid = "SOSAIOT-TC-54518"
    description = show_testcase_info(TESTPLAN, "17", description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "17")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_Traffic_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Send ping from pc1 to pc2'))
        cmd = "ping {}  -w 3".format(PC2_IP)
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to pc2 success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to pc2 failed")

    def test_02_02_Check_Connetion_Filter(self):
        logger.info(" {} ".center(20, '-').format('Check Connetion Filter'))
        res = LPackageMonitObj.get_connections_filter(**Connetion_Filter)
        rc = True
        for data in res['cacheFlowArray']:
            if data['dstIf'] == 'X0':
                rc &= True
            else:
                rc &= False
        Assertion.assert_equal(rc, True, "ERR: Check  Connection Monitor Filter failed")

    @repeat_method(3)
    def test_02_03_Restore_Setting(self):
        time.sleep(5)
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        res = LPackageMonitObj.get_connections_filter(n='null') 
        logger.info(f'----res data is {res}')
        rc = False
        for data in res['cacheFlowArray']:
            if data['dstIf'] :
                rc = True
                break
        Assertion.assert_equal(rc,True, "ERR: Restore Setting failed")


class TestNumbered_TI_03(Test):
    uuid = "SOSAIOT-TC-54521"
    description = show_testcase_info(TESTPLAN, "02", description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "02")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_03_01_del_route_policy_and_add_acl(self):
        logger.info(" {} ".center(20, '-').format('del route policy and add remote acl'))
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= RRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= Raccess_rule_obj.config_accessrule(**rule1)
        rc &= Raccess_rule_obj.config_accessrule(**rule2)
        Assertion.assert_equal(rc, True, "ERR: del route policy and add remote acl failed")

    def test_03_02_Set_Rip(self):
        rip["send"] = '2'
        rip["receive"] = '2'
        ref1 = copy.deepcopy(rip)
        ref2 = copy.deepcopy(rip)
        ref1 ["DUT"] = 'local'
        ref1['num_id'] = '0'
        ref2 ["DUT"] = 'remote'
        ref2['num_id'] = '0'
        logger.info(" {} ".center(20, '-').format('Set Local Dynamic Routing Rip'))
        rc = LDynRouteObj.set_advanced_routing_mode(advanced = "on")
        rc &= RDynRouteObj.set_advanced_routing_mode(advanced = "on")
        rc &= LDynRouteObj.set_rip(**ref1)
        rc &= RDynRouteObj.set_rip(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Set Rip failed")

    def test_03_03_Config_Global_Rip(self):
        logger.info(" {} ".center(20, '-').format('enable all the checkboxes of global Rip configuration'))
        rc = LDynRouteObj.rip_config(**rip_setting_dict)
        rc = RDynRouteObj.rip_config(**rip_setting_dict)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: enable all the checkboxes of global Rip configuration failed")

    def test_03_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(PC2_IP)
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_05_Set_Rip(self):
        rip["send"] = '0'
        rip["receive"] = '0'
        ref1 = copy.deepcopy(rip)
        ref2 = copy.deepcopy(rip)
        ref1 ["DUT"] = 'local'
        ref1['num_id'] = '0'
        ref2 ["DUT"] = 'remote'
        ref2['num_id'] = '0'
        logger.info(" {} ".center(20, '-').format('Set Local Dynamic Routing Rip'))
        rc = LDynRouteObj.set_advanced_routing_mode(advanced = "on")
        rc &= RDynRouteObj.set_advanced_routing_mode(advanced = "on")
        rc &= LDynRouteObj.set_rip(**ref1)
        rc &= RDynRouteObj.set_rip(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Set Rip failed")

    def test_03_06_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(PC2_IP)
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_03_07_Restor_Rip(self):
        ref1 = copy.deepcopy(rip)
        ref2 = copy.deepcopy(rip)
        ref1 ["DUT"] = 'local'
        ref1['num_id'] = '0'
        ref1 ["mode"] = 'disable'
        ref2 ["DUT"] = 'remote'
        ref2 ["mode"] = 'disable'
        ref2['num_id'] = '0'
        logger.info(" {} ".center(20, '-').format('Restore Rip Disable'))
        rc = LDynRouteObj.set_rip(**ref1)
        rc &= RDynRouteObj.set_rip(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Restore Rip Disable failed")


class TestNumbered_TI_04(Test):
    uuid = "SOSAIOT-TC-54525"
    jira = 'GEN8-5340'
    description = show_testcase_info(TESTPLAN, "03", description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "03")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_Set_OSPFv2(self):
        ref1 = copy.deepcopy(ospf2)
        ref2 = copy.deepcopy(ospf2)
        ref1 ["DUT"] = 'local'
        ref1 ["num_id"] = 0
        ref2 ["DUT"] = 'remote'
        ref2 ["num_id"] = 0
        logger.info(" {} ".center(20, '-').format('Set Local Dynamic Routing OSPFv2'))
        rc = LDynRouteObj.set_ospf2(**ref1)
        rc &= RDynRouteObj.set_ospf2(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Set ospf2 failed")

    def test_04_02_Config_Global_OSPF(self):
        logger.info(" {} ".center(20, '-').format('enable all the checkboxes of global OSPF configuration'))
        ref = copy.deepcopy(ospf_setting_dict)
        ref['router_id'] = '10.0.0.2'
        rc = LDynRouteObj.ospf2_config(**ospf_setting_dict)
        rc &= RDynRouteObj.ospf2_config(**ref)
        time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: enable all the checkboxes of global OSPF configuration failed")

    def test_04_03_Check_neighbor_Status(self):
        logger.info(" {} ".center(20, '-').format('Check neighbor Status'))
        res1 = LDynRouteObj.get_route_advanced_data()
        res2 = RDynRouteObj.get_route_advanced_data()
        rc1,rc2 = False,False
        for i in  res1['data']['ipv4']['interfaces']:
            logger.info(i)
            #neighborStatus is 0 or 1,1 build up,-1 down 
            if i["name"]=='Ni' and i['OSPFv2']['neighborStatus']!=-1:
                rc1 = True
                logger.info("local dut neighborStatus is build up success!!")
        for i in  res2['data']['ipv4']['interfaces']:
            logger.info(i)
            if i["name"]=='Ni' and i['OSPFv2']['neighborStatus']!=-1:
                rc2 = True
                logger.info("Remote dut neighborStatus is build up success!!")
        Assertion.assert_equal(rc1&rc2, True, "ERR: Check neighbor Status failed")
        
    def test_04_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(PC2_IP)
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_05_Restor_Rip(self):
        ref1 = copy.deepcopy(ospf2)
        ref2 = copy.deepcopy(ospf2)
        ref1 ["DUT"] = 'local'
        ref1 ["mode"] = "disable"
        ref1 ["num_id"] = 0
        ref2 ["DUT"] = 'remote'
        ref2 ["mode"] = "disable"
        ref2 ["num_id"] = 0
        logger.info(" {} ".center(20, '-').format('Restore Rip Disable'))
        rc = LDynRouteObj.set_ospf2(**ref1)
        rc &= RDynRouteObj.set_ospf2(**ref2)
        logger.info("add route policy")
        rc &= fw_cli.do_cli_commands(route_policy)
        rc &= rm_cli.do_cli_commands(route_policy)
        logger.info('del acl')
        rc &= Laccess_rule_obj.delete_accessrule_by_name('VPN_to_LAN')
        rc &= Raccess_rule_obj.delete_accessrule_by_name('VPN_to_LAN')
        rc &= Laccess_rule_obj.delete_accessrule_by_name('LAN_to_VPN')
        rc &= Raccess_rule_obj.delete_accessrule_by_name('LAN_to_VPN')
        Assertion.assert_equal(rc, True, "ERR: Restore Rip Disable failed")  

    def test_04_06_Restore_Global_OSPF(self):
        logger.info(" {} ".center(20, '-').format('disable all the checkboxes of global OSPF configuration'))
        ref = copy.deepcopy(ospf_setting_dict)
        ref['router_id'] = '0.0.0.1'
        ref['static_route'] = 'off'
        ref['connect_network'] = 'off'
        ref['rip_route'] = 'off'
        ref['vpn_network'] = 'off'
        rc = LDynRouteObj.ospf2_config(**ospf_setting_dict)
        rc &= RDynRouteObj.ospf2_config(**ref)
        time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: disable all the checkboxes of global OSPF configuration failed")


class TestNumbered_TI_05(Test):
    uuid = "SOSAIOT-TC-54548"
    description = show_testcase_info(TESTPLAN, "07", description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "07")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_05_02_Edit_TI(self):
        ref = copy.deepcopy(Tunnel_Interface)
        ref["ip"] = "3.3.3.3"
        logger.info(" {} ".center(20, '-').format('Edit Local Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref)
        Assertion.assert_equal(rc,True, "ERR: Edit Vpn Tunnel Interface failed")

    def test_05_03_Check_Edit_Log(self):
        logger.info(" {} ".center(20, '-').format('Check Edit Local Vpn Tunnel Interface'))
        res = AuditlogObj.export_audit_log_txt(log_switch=False)  
        if re.search('Ni[\S\s]+1\S1\S1\S2[\S\s]+3\S3\S3\S3', res):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(res)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")
        
    def test_05_04_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_IF_IP_LOCAL
        logger.info(" {} ".center(20, '-').format('Edit Local Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1) 
        Assertion.assert_equal(rc,True, "ERR: Restore Setting failed")


class TestNumbered_TI_06(Test):
    uuid = "SOSAIOT-TC-54541"
    description = show_testcase_info(TESTPLAN, "63", description=True)['title']
    
    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "63")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_06_01_clearup_route_and_acl(self):
        logger.info(" {} ".center(20, '-').format('Clear up  Route Policy')) 
        ref1 = copy.deepcopy(Tunnel_Interface)
        modify = {
            'mgmt_https'    : False,
            'mgmt_ssh'      : False,
            'mgmt_ping'     : False,
            'mgmt_snmp'     : False,
        }
        ref1.update(modify)
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= RRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= Linterface.config_interface(**ref1)
        rc &= LDynRouteObj.set_BGP(BGP = "off")
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: clearup route and acl failed")

    def test_06_02_add_route_policy_with_noacl(self):
        logger.info(" {} ".center(20, '-').format('Add Route Policy without ACL')) 
        ref = copy.deepcopy(route_policy)
        ref.remove('auto-add-access-rules')
        rc = fw_cli.do_cli_commands(ref)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(ref)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy without ACL failed")
        
    def test_06_03_check_no_acl(self):
        time.sleep(15)
        logger.info(" {} ".center(20, '-').format('Check Route Policy without ACL'))
        cmd = "ping {}  -w 3".format(PC2_IP)
        logger.info("send the command {}".format(cmd))
        out = PC1.send_command(cmd)
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from remote to local NAT.')
            rc = False
            res = Laccess_rule_obj.get_accessrule()
            logger.info("------"*20)
            logger.info(res)
        else:
            logger.info('Ping failed')
            logger.info(out)
            rc = True
        Assertion.assert_equal(rc, True, "ERR: check no acl failed")

    def test_06_04_add_route_policy_with_acl(self):
        logger.info(" {} ".center(20, '-').format('Add Route Policy with ACL'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= RRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy with ACL failed")

    def test_06_05_check_policy_with_acl(self):
        logger.info(" {} ".center(20, '-').format('Check Route Policy with ACL'))
        cmd = "ping {} -c 10 -w 1".format(PC2_IP)
        logger.info("send the command {}".format(cmd))
        out = PC1.send_command(cmd)
        if '100% packet loss' not in str(out):
            logger.info('Successfully initiated continuous traffic from local to remote.')
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check policy with acl failed")

    def test_06_06_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(Tunnel_Interface)
        rc = Linterface.config_interface(**ref)
        rc &= LDynRouteObj.set_BGP(BGP = "on")
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_06_env(Test):
    uuid = 'NonTC'
    description = " env config settings"
    
    def test_01_Add_Static_Route(self):
        logger.info(" {} ".center(20, '-').format('Add Static Route for DUT1'))
        PC1.send_command("route add -net {} gw {}".format(VPN_IF_NET, Parameter.DUT))
        out1 = PC1.send_command("route")
        if "1.1.1.0" in str(out1):
            rc1 = True
        else:
            rc1 = False
            logger.info(rc1,out1)
        logger.info(" {} ".center(20, '-').format('Add Static Route for DUT2'))
        PC2.send_command("route add -net {} gw {}".format(VPN_IF_NET, Parameter.REMOTEX0))
        out2 = PC2.send_command("route")
        if "1.1.1.0" in str(out2):
            rc2 = True
        else:
            rc2 = False
            logger.info(rc2,out2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Add Static Route failed")
    
    def test_02_add_acl(self):
        logger.info(" {} ".center(20, '-').format('Add Access Rule'))
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
        rc = Laccess_rule_obj.config_accessrule(**rule1)
        rc &= Laccess_rule_obj.config_accessrule(**rule2)
        rc &= Raccess_rule_obj.config_accessrule(**rule1)
        rc &= Raccess_rule_obj.config_accessrule(**rule2)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")


class TestNumbered_TI_07(Test):
    uuid = "SOSAIOT-TC-54555"
    description = show_testcase_info(TESTPLAN, "08", description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "08")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_Set_Remote_Access_Rule(self):
        logger.info(" {} ".center(20, '-').format('Set Access Rule for DUT2'))
        rule = copy.deepcopy(rule_opt)
        logger.info(rule)
        rule['name'] = 'LAN_to_VPN'
        rule['from'] = 'LAN'
        rule['to']   = 'VPN'
        rule['source']['address'] = {}
        rule['source']['address']['name'] = 'X0 Subnet'
        rule['destination']['address'] = {}
        rule['destination']['address']['name']   = "Ni Subnet"
        rc = Raccess_rule_obj.put_accessrule(**rule)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: config access rule LAN to VPN  in DUT2 failed")
    
    def test_07_02_Ping_from_Remote_to_Local(self):
        logger.info(" {} ".center(20, '-').format('Ping from Remote to Local'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(VPN_IF_IP_LOCAL)
            logger.info("send the command {}".format(cmd))
            out =  PC2.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_07_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        rule = copy.deepcopy(rule_opt)
        rule['name'] = 'LAN_to_VPN'
        rule['from'] = 'LAN'
        rule['to']   = 'VPN'
        rc = Raccess_rule_obj.put_accessrule(**rule)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: config access rule LAN to VPN  in DUT2 failed")


class TestNumbered_TI_09(Test):
    uuid = "SOSAIOT-TC-54513"
    description = show_testcase_info(TESTPLAN, "11", description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "11")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_01_Enable_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Enable SNMP'))
        rc = LSNMPObj.enable_snmp()
        rc &= RSNMPObj.enable_snmp()
        Assertion.assert_equal(rc, True, "ERR: show testcase info failed")

    def test_09_02_Set_Local_Access_Rule(self):
        logger.info(" {} ".center(20, '-').format('Set Access Rule for DUT'))
        rule = copy.deepcopy(rule_opt)
        logger.info(rule)
        rule['name'] = 'LAN_to_VPN'
        rule['from'] = 'LAN'
        rule['to']   = 'VPN'
        rule['source']['address'] = {}
        rule['source']['port'] = {}
        rule['source']['address']['name'] = 'X0 Subnet'
        rule['source']['port']['name'] = 'SNMP'
        rule['destination']['address'] = {}
        rule['destination']['service'] = {}
        rule['destination']['address']['name']   = "Ni Subnet"
        rule['destination']['service']['name']   = "SNMP"
        rc = Laccess_rule_obj.put_accessrule(**rule)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: config access rule LAN to VPN  in DUT2 failed")

    @repeat_method(4)
    def test_09_03_Check_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Check SNMP '))
        cmd = "snmpwalk -v 2c -c public {} .1.3.6.1.2.1.31 | grep {}".format(VPN_IF_IP_REMOTE,Tunnel_Interface["tunnel_name"])
        out = PC1.send_command(cmd)
        if str(out):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check SNMP failed")

    def test_09_04_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        rule = copy.deepcopy(rule_opt)
        rule['name'] = 'LAN_to_VPN'
        rule['from'] = 'LAN'
        rule['to']   = 'VPN'
        rc = Laccess_rule_obj.put_accessrule(**rule)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: config access rule LAN to VPN  in DUT failed")


class TestNumbered_TI_10(Test):
    uuid = "SOSAIOT-TC-54517"
    description = show_testcase_info(TESTPLAN, "16", description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "16")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_Traffic_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Send ping from pc1 to pc2'))
        cmd = "ping {}  -w 3".format(PC2_IP)
        logger.info("send the command {}".format(cmd))
        out = PC1.send_command(cmd)
        if '100% packet loss' not in str(out):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to pc2 failed")

    def test_10_02_Check_Connection_Monitor(self):
        logger.info(" {} ".center(20, '-').format('Check  Connection Monitor'))
        res = LPackageMonitObj.get_connections_list()
        logger.info(res)
        rc = False
        for data in res['cacheFlowArray']:
            if data['dstIf'] == 'Ni':
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: Check  Connection Monitor failed")


class TestNumbered_TI_11(Test):
    uuid = "SOSAIOT-TC-54519"
    description = show_testcase_info(TESTPLAN, "18", description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "18")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(4)
    def test_11_01_Packet_Capture_and_Check_filter(self):
        logger.info(" {} ".center(20, '-').format('Packet Capture'))
        logger.info(" {} ".center(20, '-').format('Clear Packet '))
        LPackageMonitObj.clear_packets()
        logger.info(" {} ".center(20, '-').format('Start Capture '))
        LPackageMonitObj.start_capture()
        out1 = PC1.send_command("ping {}  -w 2".format(PC2_IP))
        out2 = PC1.send_command("ping {}  -w 1".format(Parameter.DUT))
        logger.info(" {} ".center(20, '-').format('Stop Capture '))
        LPackageMonitObj.stop_capture()
        if '100% packet loss' not in str(out1) and '100% packet loss' not in str(out2):
            rc = True
        else:
            rc = False
        rc = LPackageMonitObj.conf_packmon(**packet_filter)
        res = LPackageMonitObj.export_captured_packets()
        logger.info(" {} ".center(20, '!').format(res))
        res = (res.split("Packet number:"))[1:]
        for i in res:
            if 'in:Ni'  in i or 'out:Ni' in i :
                rc &= True
            else:
                rc &= False
        Assertion.assert_equal(rc, True, "ERR: Packet Capture filter  failed")


class TestNumbered_TI_12(Test):
    uuid = "SOSAIOT-TC-54520"
    description = show_testcase_info(TESTPLAN, "19", description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "19")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_12_01_Packet_Capture(self):
        logger.info(" {} ".center(20, '-').format('Packet Capture'))
        logger.info(" {} ".center(20, '-').format('Start Capture '))
        LPackageMonitObj.start_capture()
        logger.info(" {} ".center(20, '-').format('Clear Packet '))
        LPackageMonitObj.clear_packets()
        PC1.send_command("ping {}  -w 3".format(PC2_IP))
        PC1.send_command("ping {}  -w 1".format(Parameter.DUT))
        logger.info(" {} ".center(20, '-').format('Stop Capture '))
        LPackageMonitObj.stop_capture()
        rc = LPackageMonitObj.conf_packmon(**packet_filter)
        Assertion.assert_equal(rc, True, "ERR: Packet Capture filter  failed")

    def test_12_02_check_Packet_Filter(self):
        res = LPackageMonitObj.export_captured_packets()
        logger.info(" {} ".center(20, '!').format(res))
        res = (res.split("Packet number:"))[1:]
        rc = True
        for i in res:
            if 'in:Ni'  in i or 'out:Ni' in i :
                rc &= True
            else:
                rc &= False
        Assertion.assert_equal(rc, True, "ERR: chec _Packet Filter  failed")


#TC14 relies on TC13
class TestNumbered_TI_13(Test):
    uuid = "SOSAIOT-TC-54522"
    description = show_testcase_info(TESTPLAN, "23", description=True)['title']

    def test_13_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "23")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_13_01_Enable_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Enable SNMP'))
        rc = LSNMPObj.enable_snmp()
        rc &= RSNMPObj.enable_snmp()
        Assertion.assert_equal(rc, True, "ERR: Enable SNMP failed")

    def test_13_02_Config_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Config SNMP Group'))
        rc = LSNMPObj.add_snmp_group(name = "g1")
        rc &= RSNMPObj.add_snmp_group(name = "g1")
        logger.info(" {} ".center(20, '-').format('Config SNMP User'))
        rc &= LSNMPObj.add_snmp_user(**snmp_user)
        rc &= RSNMPObj.add_snmp_user(**snmp_user)
        logger.info(" {} ".center(20, '-').format('Config SNMP Access'))
        rc &= LSNMPObj.add_access(**snmp_access)
        rc &= RSNMPObj.add_access(**snmp_access)
        Assertion.assert_equal(rc, True, "ERR: Config SNMP failed")
    
    def test_13_03_Check_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Check SNMP '))
        cmd = "snmpwalk -v 3 -u vpntc23user {} 1.3.6.1.2.1.2 | grep -E 'ifDescr|ifType'".format(Parameter.DUT)
        res = PC1.send_command(cmd)
        if Tunnel_Interface["tunnel_name"] in res:
            rc = True
        else:
            rc = False
            logger.info(" {} {} ".center(20, '*').format(type(res),res))
        Assertion.assert_equal(rc, True, "ERR: check SNMP failed")

    def test_13_04_Restore_SNMP(self):
        logger.info(" {} ".center(20, '-').format('Delet SNMP Access'))
        rc = LSNMPObj.delete_snmp_access(name =snmp_access['snmp']['access'][0]['name'] )
        rc &= RSNMPObj.delete_snmp_access(name =snmp_access['snmp']['access'][0]['name'])
        logger.info(" {} ".center(20, '-').format('Delet SNMP User'))
        rc &= LSNMPObj.delete_snmp_user(**snmp_user)
        rc &= RSNMPObj.delete_snmp_user(**snmp_user)
        logger.info(" {} ".center(20, '-').format('Delet SNMP Group'))
        rc &= LSNMPObj.delete_snmp_group(name = "g1")
        rc &= RSNMPObj.delete_snmp_group(name = "g1")
        Assertion.assert_equal(rc, True, "ERR: Rsetore SNMP failed")
    

class TestNumbered_TI_14(Test):
    uuid = "SOSAIOT-TC-54523"
    description = show_testcase_info(TESTPLAN, "24", description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "24")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_14_01_Check_SNMP(self):
        logger.info(" {} ".center(20, '-').format('check SNMP'))
        cmd1 = "snmpwalk -v 2c -c public {} .1.3.6.1.2.1.31 | grep 'ifName'".format(Parameter.DUT)
        cmd2 = "snmpwalk -v 2c -c public {} .1.3.6.1.2.1.31 | grep 'ifName'".format(Parameter.REMOTEX1)
        res1  = PC1.send_command(cmd1)
        res2  = PC1.send_command(cmd2)
        if  Tunnel_Interface["tunnel_name"] in res2:
            rc = True
        else:
            rc = False
            logger.info(" {} {} ".center(20, '*').format(res1,res2))
        Assertion.assert_equal(rc, True, "ERR: check SNMP failed")


class TestNumbered_TI_15(Test):
    uuid = "SOSAIOT-TC-54527"
    description = show_testcase_info(TESTPLAN, "38", description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "38")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_15_01_Enable_Multicast(self):
        logger.info(" {} ".center(20, '-').format('Enable Multicast'))
        rc = LMulticast.config_multicast(**Multicast_json)
        rc &= RMulticast.config_multicast(**Multicast_json)
        Assertion.assert_equal(rc, True, "ERR: Enable Multicast failed")

    def test_15_02_Check_Multicast(self):
        logger.info(" {} ".center(20, '-').format('Check Multicast'))
        cmd = "nohup python3 {}/definition/server.py &".format(TESTPATH)
        os.system("python3 {}/definition/run_server.py -ip {} -c \"{}\"".format(TESTPATH, PC2_IP, cmd))
        logger.info("Server is running")
        out1 = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        if 'TEST PASS' in out1:
            logger.info("Check Multicast passed.")
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Multicast failed")

    def test_15_03_Disable_Interface_Multicast(self):
        logger.info(" {} ".center(20, '-').format('Disable Interface Multicast'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref1['multicast'] = False
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2['ip'] = VPN_IF_IP_REMOTE
        ref2['multicast'] = False
        logger.info(" {} ".center(20, '-').format('Edit Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: config NI disabled multicast failed")

    def test_15_04_Check_Disable_Multicast(self):
        logger.info(" {} ".center(20, '-').format('Check Disable Multicast'))
        out1 = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        if 'TEST PASS' in out1:
            rc = False
        else:
            logger.info("Check Disabled Multicast passed.")
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Check Disabled Multicast failed")


class TestNumbered_TI_16(Test):
    uuid = "SOSAIOT-TC-54530"
    description = show_testcase_info(TESTPLAN, "40", description=True)['title']
    
    def test_16_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "40")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_16_01_Check_Fragment_Packet(self):
        logger.info(" {} ".center(20, '-').format('Check Enable Fragment Packet'))
        rc = icmp_packet_check(LPackageMonitObj, scapyPacketObj, filter_frag)
        Assertion.assert_equal(rc, True, "ERR: Check Enable Fragment Packet failed")

    def test_16_02_Disable_Fragment_Packet(self):
        logger.info(" {} ".center(20, '-').format('Disable Fragment Packet'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref1['fragment_packets'] = False
        ref1.pop("ignore_df_bit")
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2['ip'] = VPN_IF_IP_REMOTE
        ref2['fragment_packets'] = False
        ref2.pop("ignore_df_bit")
        logger.info(" {} ".center(20, '-').format('Edit Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: config NI disabled Fragment Packet failed")

    def test_16_03_Check_Disable_Fragment_Packet(self):
        logger.info(" {} ".center(20, '-').format('Check Disable Fragment Packet'))
        rc = icmp_packet_check(LPackageMonitObj, scapyPacketObj, filter_frag)
        Assertion.assert_equal(rc, True, "ERR: Check Disable Fragment Packet failed")
        
    def test_16_04_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2['ip'] = VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Edit Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: config NI enabled Fragment Packet failed")


class TestNumbered_TI_17(Test):
    uuid = "SOSAIOT-TC-54531"
    description = show_testcase_info(TESTPLAN, "41", description=True)['title']
    
    def test_17_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "41")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_01_Check_DF_bits(self):
        logger.info(" {} ".center(20, '-').format('Check enable ignore do not Fragment bit'))
        cmd = "ping {}  -s 1460 -c 1 -W 1".format(PC2_IP)
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous icmp traffic.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Check enable ignore do not Fragment bit failed")
        
    def test_17_02_Disable_Fragment_Packet(self):
        logger.info(" {} ".center(20, '-').format('Disable ignore do not Fragment Packet'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref1['ignore_df_bit'] = False
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2['ip'] = VPN_IF_IP_REMOTE
        ref2['ignore_df_bit'] = False
        logger.info(" {} ".center(20, '-').format('Edit Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: config NI disabled DF failed")

    def test_17_03_Check_Disable_DF(self):
        logger.info(" {} ".center(20, '-').format('Check disable ignore do not Fragment bit'))
        cmd = "ping {}  -s 1460 -c 1 -W 1".format(PC2_IP)
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' in str(out):
                logger.info('continuous icmp traffic failed, disable df bit is successful')
                rc = True
                break
            elif i == 9:
                logger.info('Unexpected ping pass on large packets when ignore df not enabled')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Check disable ignore do not Fragment bit failed")
        
    def test_17_04_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2['ip'] = VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Edit Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: config NI enabled ignore df bit failed")


class TestNumbered_TI_18(Test):
    uuid = "SOSAIOT-TC-54532"
    description = show_testcase_info(TESTPLAN, "42", description=True)['title']
    
    def test_18_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "42")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_18_01_Check_TI_Not_Included(self):
        logger.info(" {} ".center(20, '-').format('Check  TI Not Included Interface Traffic Statistics'))
        res = Linterface.get_interface_statistics()
        if res:
            for i in res:
                if i['interface_name'] == Tunnel_Interface['tunnel_name']:
                    rc = False
                else:
                    rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check  TI Not Included Interface Traffic Statistics failed")


class TestNumbered_TI_19(Test):
    uuid = "SOSAIOT-TC-54533"
    description = show_testcase_info(TESTPLAN, "49", description=True)['title']
    
    def test_19_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "49")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_19_01_Check_Static_Route(self):
        logger.info(" {} ".center(20, '-').format('Check Static  Route'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(PC2_IP)
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")


class TestNumbered_TI_20(Test):
    uuid = "SOSAIOT-TC-54534"
    description = show_testcase_info(TESTPLAN, "50", description=True)['title']
    
    def test_20_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "50")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_20_01_Clear_Route_Policy_and_AccessRule(self):
        logger.info(" {} ".center(20, '-').format('clear static route policy and access rule'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        Assertion.assert_equal(rc, True, "ERR: delete route policy and access rule failed")
    
    def test_20_02_Add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")
    
    def test_20_03_Check_Access_Rule(self):
        logger.info(" {} ".center(20, '-').format('Check Auto add access rule is exist'))
        rc = Laccess_rule_obj.is_accessrule_exists(**del_rule1)
        rc &= Laccess_rule_obj.is_accessrule_exists(**del_rule2)
        Assertion.assert_equal(rc, True, "ERR: Check access rule is exist failed")


class TestNumbered_TI_21(Test):
    uuid = "SOSAIOT-TC-54535"
    description = show_testcase_info(TESTPLAN, "52", description=True)['title']
    
    def test_22_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "52")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_21_01_Add_Nat_and_Rule(self):
        logger.info(" {} ".center(20, '-').format('Add Adress ,NAT Policy,Access rule and Route'))
        rc = LAddrOBJ.config_addressobject(**trans_net)
        rc &= Laccess_rule_obj.config_accessrule(**nat_lan2vpn)
        rc &= Laccess_rule_obj.config_accessrule(**nat_vpn2lan)
        rc &= natPolicyObj.add_nat_policy(**nat_policy)
        PC1.send_command("route add -net 192.168.101.0/24 gw 192.168.168.168")
        out = PC1.send_command("route")
        if "192.168.101.0" in str(out):
            rc &= True
        else:
            rc &= False
            logger.error("Add Route Failed")
        Assertion.assert_equal(rc, True, "ERR: Add Nat and Rule failed")

    def test_21_02_Check_Nat_on_VPN(self):
        logger.info(" {} ".center(20, '-').format('Check Nat on VPN'))
        cmd = "ping {} -c 10 -W 2".format(new_pc_ip)
        logger.info("send command {}".format(cmd))
        out1 = PC1.send_command(cmd)
        if '100% packet loss' not in str(out1):
            rc = True
        else:
            rc = False
            logger.error("Ping {} is failed".format(new_pc_ip))
        new_pc = Host(ip = new_pc_ip)
        out2 = new_pc.send_command("hostname")
        if "PC2" in str(out2):
            rc &= True
        else:
            rc &= False
            logger.error("Not reaching PC2 on {}".format(new_pc_ip))
        Assertion.assert_equal(rc, True, "ERR: Check Nat on VPN failed")

    def test_21_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting'))
        PC1.send_command("route delete -net 192.168.101.0/24 gw 192.168.168.168")
        rc = Laccess_rule_obj.delete_accessrule_by_name(nat_lan2vpn["name"])
        rc &= Laccess_rule_obj.delete_accessrule_by_name(nat_vpn2lan["name"])
        rc &= natPolicyObj.del_nat_policy_by_name(Nat_reflexive_name)
        rc &= natPolicyObj.del_nat_policy_by_name(Nat_name)
        rc &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=trans_net['name'],ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_22(Test):
    uuid = "SOSAIOT-TC-54537"
    description = show_testcase_info(TESTPLAN, "54", description=True)['title']
    
    def test_22_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "54")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_22_01_Check_TI_not_in_Arp_list(self):
        logger.info(" {} ".center(20, '-').format('Check TI not in included in add arp entry interface list'))     
        res = arpObj.show_arp_caches()
        rc = True
        for i in res:
            if Tunnel_Interface['tunnel_name'] == i["interface"]:
                rc &= False
                logger.error("TI included in arp caches report list")
            else:
                rc &= True
        Assertion.assert_equal(rc, True, "ERR: check TI not in included in add arp entry interface list failed")


class TestNumbered_TI_23(Test):
    uuid = "SOSAIOT-TC-54538"
    description = show_testcase_info(TESTPLAN, "59", description=True)['title']
    
    def test_23_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "59")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_01_Enable_NetBios(self):
        logger.info(" {} ".center(20, '-').format('Enable VPN policy NetBios'))     
        ref = copy.deepcopy(Lvpn)
        ref["netbios"] = True
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Enable VPN policy NetBios failed")

    def test_23_02_Add_IPhelper_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add  IPhelper  Policy')) 
        rc = LiphelperObj.enable_iphelper()
        rc &= LiphelperObj.add_iphelper_policy(**iphelper_policy1)
        rc &= LiphelperObj.add_iphelper_policy(**iphelper_policy2)
        Assertion.assert_equal(rc, True, "ERR: Enable IPhelper and add iphelper policy failed")

    def test_23_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(Lvpn)
        ref["netbios"] = False
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        rc &= LiphelperObj.delete_iphelper_policy(**iphelper_policy1)
        rc &= LiphelperObj.delete_iphelper_policy(**iphelper_policy2)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_24(Test):
    uuid = "SOSAIOT-TC-54539"
    description = show_testcase_info(TESTPLAN, "60", description=True)['title']
    
    def test_24_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "60")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_24_01_Enable_NetBios(self):
        logger.info(" {} ".center(20, '-').format('Enable VPN policy NetBios'))
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1["netbios"] = True
        ref2["netbios"] = True
        rc = Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Enable VPN policy NetBios failed")   

    def test_24_02_Enable_IPhelper(self):
        logger.info(" {} ".center(20, '-').format('Add  IPhelper  Policy')) 
        rc = LiphelperObj.enable_iphelper()
        rc &= RiphelperObj.enable_iphelper()
        rc &= LiphelperObj.add_iphelper_policy(**iphelper_policy1)
        rc &= RiphelperObj.add_iphelper_policy(**iphelper_policy1)
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Enable IPhelper  failed")

    def test_24_03_Check_IPhelper(self):
        logger.info(" {} ".center(20, '-').format('Check  IPhelper  Policy')) 
        LPackageMonitObj.start_capture()
        LPackageMonitObj.clear_packets()
        RPackageMonitObj.start_capture()
        RPackageMonitObj.clear_packets()
        scapyPacketObj.send_udp_packet(**udp_packet)
        logger.info(" {} ".center(20, '-').format('Stop Capture '))
        LPackageMonitObj.stop_capture()
        RPackageMonitObj.stop_capture()
        Lpacket = LPackageMonitObj.export_captured_packets()
        Rpacket = RPackageMonitObj.export_captured_packets()
        Lpacket = (Lpacket.split("Packet number:"))[1:]
        Rpacket = (Rpacket.split("Packet number:"))[1:]
        logger.info('---*****----'*20)
        rc1,rc2 = True, False
        for p in Lpacket:
            if 'Src=[137], Dst=[137]' in p and 'Forwarded' in p:
                rc1 &= False
                logger.info(p)
                break
            else:
                rc1 &= True
        for p in Rpacket:
            if 'Src=[137], Dst=[137]' in p and 'Forwarded' in p:
                rc2 = True
                logger.info(p)
        Assertion.assert_equal(rc1&rc2 , True, "ERR: Check NetBios failed")

    def test_24_04_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1["netbios"] = False
        ref2["netbios"] = False
        rc = RRoutePolicyObj.del_route_policy_by_name(name = 'ti_route2')
        rc &= LiphelperObj.delete_iphelper_policy(**iphelper_policy1)
        rc &= RiphelperObj.delete_iphelper_policy(**iphelper_policy1)
        rc &= Lvpn_obj.edit_vpn_policy(**ref1)
        rc &= Rvpn_obj.edit_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting  failed")


class TestNumbered_TI_25(Test):
    uuid = "SOSAIOT-TC-54552"
    description = show_testcase_info(TESTPLAN, "75", description=True)['title']
    
    def test_25_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "75")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_25_01_Set_Route_Mode(self):
        logger.info(" {} ".center(20, '-').format('Set Route Mode is advanced ')) 
        rc = LDynRouteObj.set_advanced_routing_mode(advanced = "on")
        Assertion.assert_equal(rc, True, "ERR: Set Route Mode  failed")

    def test_25_02_Check_Route_Page(self):
        logger.info(" {} ".center(20, '-').format('Check Route page included TI interface')) 
        res= LDynRouteObj.get_route_advanced_data()
        res = res['data']['ipv4']['interfaces']
        rc = ''
        for i in res:
            if i['name'] == Tunnel_Interface["tunnel_name"]:
                rc = True
        if isinstance(rc,bool):
            rc1 = True
        else:
            rc1 = False
            logger.info(res)
        Assertion.assert_equal(rc1, True, "ERR: Check Route page included TI interfacefailed")


class TestNumbered_TI_27(Test):
    uuid = "SOSAIOT-TC-54553"
    description = show_testcase_info(TESTPLAN, "76", description=True)['title']
    
    def test_27_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "76")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_27_01_Set_Route_Mode(self):
        logger.info(" {} ".center(20, '-').format('Check route policy ')) 
        res = LRoutePolicyObj.show_route_policy(version = 'ipv4')
        res = res["route_policies"]
        rc = False
        for i in res:
            if i['ipv4']['interface'] == 'Ni' and i['ipv4']['name'] == 'ti_route':
                rc = True
        Assertion.assert_equal(rc, True, "ERR: Check route policy  failed")


class TestNumbered_TI_28(Test):
    uuid = "SOSAIOT-TC-54559"
    description = show_testcase_info(TESTPLAN, "86", description=True)['title']
    
    def test_28_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "86")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_28_01_Disable_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Disable VPN Policy ')) 
        ref = copy.deepcopy(Lvpn)
        ref["enable"] = False
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Disable Local VPN Policy  failed")
       
    def test_28_02_Check_TI_Status(self):
        logger.info(" {} ".center(20, '-').format('Check TI Status')) 
        res = Linterface.get_interface_report()
        rc = False
        for i in res:
            if i['name'] == Tunnel_Interface['tunnel_name'] and i['status'] == 'Interface Down':
                rc = True
        Assertion.assert_equal(rc, True, "ERR: Check TI Status failed")

    def test_28_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(Lvpn)
        ref["enable"] = True
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Enable Local VPN Policy  failed")


class TestNumbered_TI_29(Test):
    uuid = "SOSAIOT-TC-54562"
    description = show_testcase_info(TESTPLAN, "77", description=True)['title']
    
    def test_29_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "77")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_29_01_Check_ACL(self):
        logger.info(" {} ".center(20, '-').format('Check ACL for vpn->vpn with enabled HTTPS/PING/SSH/SNMP of management ')) 
        mngt_list = ['https','snmp','ssh','ping']
        rc = True
        for mngt in mngt_list:
            rc &= Laccess_rule_obj.verify_access_rule(mngt,"Ni IP")
        Assertion.assert_equal(rc, True, "ERR: Check ACL  failed")
    

class TestNumbered_TI_30(Test):
    uuid = "SOSAIOT-TC-54556"
    description = show_testcase_info(TESTPLAN, "80", description=True)['title']
    
    def test_30_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "80")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_30_01_Delete_TI(self):
        logger.info(" {} ".center(20, '-').format('Delete TI')) 
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= Linterface.del_interface(**Tunnel_Interface)
        Assertion.assert_equal(rc, True, "ERR: Delete TI failed")

    def test_30_02_Check_Route_Page(self):
        logger.info(" {} ".center(20, '-').format('Check Route page is not included TI interface')) 
        res= LDynRouteObj.get_route_advanced_data()
        res = res['data']['ipv4']['interfaces']
        rc = True
        for i in res:
            if i['name'] == Tunnel_Interface["tunnel_name"]:
                rc = False
                logger.info(res)
                break
        Assertion.assert_equal(rc, True, "ERR: Check Route page failed")

    def test_30_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        rc = Linterface.add_interface(**Tunnel_Interface)
        rc &= fw_cli.do_cli_commands(route_policy)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


#DynamicRoutingApi.set_ospf2，tableIndex index
class TestNumbered_TI_31(Test):
    uuid = "SOSAIOT-TC-54557"
    jira = 'GEN8-5340'
    description = show_testcase_info(TESTPLAN, "82", description=True)['title']
    
    def test_31_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "82")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_31_01_Config_OSPF(self):
        logger.info(" {} ".center(20, '-').format('Config TI OSPF in Dynamic Routing')) 
        ref = copy.deepcopy(ospf2)
        ref ["num_id"] = 1
        ref ["router_priority"] = 2
        rc = LDynRouteObj.set_ospf2(**ref)
        Assertion.assert_equal(rc, True, "ERR: Config TI OSPF failed")

    def test_31_02_Check_Delete_TI(self):
        logger.info(" {} ".center(20, '-').format('Check Delete TI Message')) 
        _, msg = Linterface.del_interface(True,**Tunnel_Interface)
        if 'Interface is in use by OSPF' in msg['status']['info'][0]['message']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Delete TI Message failed")

    def test_31_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(ospf2)
        ref["mode"] = "disable"
        ref ["num_id"] = 1
        rc = LDynRouteObj.set_ospf2(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_32(Test):
    uuid = "SOSAIOT-TC-54558"
    description = show_testcase_info(TESTPLAN, "83", description=True)['title']
    
    def test_32_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "83")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_32_01_Config_RIP(self):
        logger.info(" {} ".center(20, '-').format('Config TI RIP in Dynamic Routing')) 
        ref = copy.deepcopy(rip)
        rc = LDynRouteObj.set_rip(**ref)
        Assertion.assert_equal(rc, True, "ERR: Config TI RIP failed")

    def test_32_02_Check_Delete_TI(self):
        logger.info(" {} ".center(20, '-').format('Check Delete TI Message')) 
        _, msg = Linterface.del_interface(True,**Tunnel_Interface)
        if 'Interface is in use by RIP' in msg['status']['info'][0]['message']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Delete TI Message failed")

    def test_32_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(rip)
        ref["mode"] = "disable"
        rc = LDynRouteObj.set_rip(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_33(Test):
    uuid = "SOSAIOT-TC-54563"
    description = show_testcase_info(TESTPLAN, "84", description=True)['title']
    
    def test_33_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "84")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_33_01_Config_BGP(self):
        logger.info(" {} ".center(20, '-').format('Config TI BGP in Dynamic Routing')) 
        rc = LDynRouteObj.set_BGP(BGP = "on")
        rc &= fw_cli.do_cli_commands(local_bgp_cmds2)
        Assertion.assert_equal(rc, True, "ERR: Config TI BGP failed")
    
    def test_33_02_Check_Delete_TI(self):
        logger.info(" {} ".center(20, '-').format('Check Delete TI Message')) 
        _, msg = Linterface.del_interface(True,**Tunnel_Interface)
        if 'Tunnel Interface is in use by Route Policy' in msg['status']['info'][0]['message']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Delete TI Message failed")

    
class TestNumbered_TI_34(Test):
    uuid = "SOSAIOT-TC-54540"
    description = show_testcase_info(TESTPLAN, "62", description=True)['title']
    
    def test_34_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "62")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_34_01_Add_Adress_and_Monitor_policy(self):
        logger.info(" {} ".center(20, '-').format('Add Adress and Network Monitor policy')) 
        rc = LAddrOBJ.config_addressobject(**remote_pc)
        rc &= LNetMonitObj.add_network_monitor(**netmonit_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Adress and Network Monitor policy failed")

    def test_34_02_Check_Monitor_policy_Status(self):
        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('Check Monitor policy Status')) 
        res = LNetMonitObj.get_network_monitor_status()
        res_data = res['data']['netMonArray']
        for data in res_data:
            if data['policy_name'] == 'monitor_policy' and '100% Successful' in data['netMonProbeStatus']['probeStatus']:
                rc = True
            else:
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Monitor policy Status failed")  

    def test_34_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        rc = LNetMonitObj.del_network_monitor(netmonit_policy['network_monitors'][0]['policy']['ipv4']['name'])
        rc &= LAddrOBJ.delete_addressobject(object_type='host', object_path='name', object_name_uuid=remote_pc['name'],ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")   


class TestNumbered_TI_35(Test):
    uuid = "SOSAIOT-TC-54543"
    description = show_testcase_info(TESTPLAN, "65", description=True)['title']
    
    def test_35_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "65")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_35_01_Check_Delete_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Check Unable Delete VPN Policy when it used by TI')) 
        _, msg = Lvpn_obj.del_tunnelvpn_policy(True,**Lvpn)
        if 'VPN Policy used by VPN tunnel interface' in  msg['status']['info'][0]['message']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Unable Delete VPN Policy when it used by TI failed")


class TestNumbered_TI_36(Test):
    uuid = "SOSAIOT-TC-54544"
    description = show_testcase_info(TESTPLAN, "66", description=True)['title']
    
    def test_36_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "66")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_36_01_Edit_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit VPN Policy ')) 
        ref = copy.deepcopy(Lvpn)
        ref["netbios"] = True
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit VPN Policy")

    def test_36_02_Check_Host_Traffic(self):
        logger.info(" {} ".center(20, '-').format('Ping from PC1 to PC2 ')) 
        cmd = "ping {} -c 10 -w 1".format(PC2_IP)
        logger.info("send the command {}".format(cmd))
        for i in range(10):
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from local to remote.')
                rc = True
                break
            elif i == 9:
                rc = False
            logger.info(out)
        Assertion.assert_equal(rc, True, "ERR: Ping from PC1 to PC2 failed")

    def test_36_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(Lvpn)
        ref["netbios"] = False
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_37(Test):
    uuid = "SOSAIOT-TC-54536"
    description = show_testcase_info(TESTPLAN, "53", description=True)['title']
    
    def test_37_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "53")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_37_01_Check_TI_Not_in_ARP_list(self):
        logger.info(" {} ".center(20, '-').format('Check TI should not included in add arp entry interface list')) 
        _, msg = LArpObj.add_arp_entry(True,**arp_json)
        pattern = r'["\']?Ni["\']?\s+(is\s+)?not\s+a\s+reasonable\s+value\.?'
        match = re.search(pattern, msg['status']['info'][0]['message'])
        # if 'Ni" is not a reasonable value' in  msg['status']['info'][0]['message']:
        if match:
            rc = True
        else:
            rc = False
            logger.info(f'Not serach the keywords:  {pattern}')
        Assertion.assert_equal(rc, True, "ERR: Check TI should not included in add arp entry interface list Failed")


class TestNumbered_TI_38(Test):
    uuid = "SOSAIOT-TC-54542"
    description = show_testcase_info(TESTPLAN, "64", description=True)['title']
    
    def test_38_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "64")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_38_01_Set_BWM(self):
        logger.info(" {} ".center(20, '-').format('enable Global BWM'))
        rule1 = copy.deepcopy(rule_opt)
        rule1['bandwidth_management'] = {
            "egress": {
                    "bandwidth_object": bwm_obj1['name']
                },
                "ingress": {
                    "bandwidth_object": bwm_obj1['name']
                },
        }
        rc = LBWMObj.add_bandwidth_object(**bwm_obj1)
        rc &= Laccess_rule_obj.config_accessrule(**rule1)
        Assertion.assert_equal(rc, True, "ERR: enable Global BWM Failed")

    def test_38_02_Check_TI_Not_Display_BWM(self):
        logger.info(" {} ".center(20, '-').format(' check BWM option is not displayed in TI')) 
        res = Linterface.get_tunnel_interface_status(name = 'Ni', type = 'vpn')
        data = res['tunnel_interfaces'][0]['vpn']
        rc = True
        for k in data.keys():
            if "BWM" in k:
                rc &= False
                logger.info(k)
                break
            else:
                rc &= True
        Assertion.assert_equal(rc, True, "ERR: check BWM option is not displayed in TI Failed")

    def test_38_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        rc = Laccess_rule_obj.delete_accessrule_by_name('any_to_any')
        rc &= LBWMObj.delete_bandwidth_object(**bwm_obj1)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_39(Test):
    uuid = "SOSAIOT-TC-54547"
    description = show_testcase_info(TESTPLAN, "69", description=True)['title']
    
    def test_39_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "69")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_39_01_Check_TI_Not_Display_HA_List(self):
        logger.info(" {} ".center(20, '-').format('Check TI Not Display HA Interface Listbox'))
        res = LHASet.config_mode_active(True,**HA_set)
        res = res[1]['status']['info'][0]['message']
        
        pattern = r'["\']?Ni["\']?\s+(is\s+)?not\s+a\s+reasonable\s+value\.?'
        match = re.search(pattern, res)
        if match:
            rc = True
        else:
            rc = False
            logger.info(f'Not serach the keywords:  {pattern}')
        Assertion.assert_equal(rc, True, "ERR: Check TI Not Display HA Interface Listbox Failed")


class TestNumbered_TI_40(Test):
    uuid = "SOSAIOT-TC-54550"
    description = show_testcase_info(TESTPLAN, "72", description=True)['title']
    
    def test_41_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "72")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_40_01_Add_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add VPN policy and config TI'))
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Rvpn)
        ref1['vpn_policy'] = 'test1'
        ref2['name'] = 'test1'
        rc = Lvpn_obj.add_vpn_policy(**ref2)
        rc &= Linterface.config_interface(**ref1)
        Assertion.assert_equal(rc, True, "ERR: Add VPN policy and config TI Failed")

    def test_40_02_Check_TI_Policy(self):
        logger.info(" {} ".center(20, '-').format('VPN policy selection in TI cannot be changed'))
        res = Linterface.get_tunnel_interface_status(name='Ni',type="vpn")
        policy_name = res['tunnel_interfaces'][0]['vpn']['policy']
        if policy_name == Tunnel_Interface['vpn_policy']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: VPN policy selection in TI cannot be changed Failed")

    def test_40_03_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        ref = copy.deepcopy(Rvpn)
        ref['name'] = 'test1'
        rc = Lvpn_obj.del_tunnelvpn_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_41(Test):
    uuid = "SOSAIOT-TC-54551"
    description = show_testcase_info(TESTPLAN, "73", description=True)['title']
    
    def test_41_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "73")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_41_01_Check_TI_for_Same_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Check TI for Same VPN Policy'))
        ref = copy.deepcopy(Tunnel_Interface)
        ref['ip'] = VPN_BGP_IP_LOCAL
        ref['tunnel_name'] = 'Ni2'
        _,res = Linterface.config_interface(True,**ref)
        res = res['status']['info'][0]['message']
        
        pattern = r'["\']?tunnel-interface vpn Ni2["\']?\s+(is\s+)?not\s+found\.?'
        # if "tunnel-interface vpn Ni2' is not found" in res:
        if re.search(pattern,res):
            rc = True
        else:
            rc = False
            logger.info(f'Not serach the keywords:  {pattern}')
        Assertion.assert_equal(rc, True, "ERR: Check TI for Same VPN Policy failed")


class TestNumbered_TI_42(Test):
    uuid = "SOSAIOT-TC-54554"
    description = show_testcase_info(TESTPLAN, "79", description=True)['title']
    
    def test_42_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "79")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_42_01_Check_Modify_TI(self):
        logger.info(" {} ".center(20, '-').format('Check Modify TI'))
        rc = Linterface.config_interface(**TI_modify)
        res = Linterface.get_tunnel_interface_status(name = 'Ni',type = "vpn")
        mngm = res['tunnel_interfaces'][0]['vpn']['management']
        user = res['tunnel_interfaces'][0]['vpn']['user_login']
        mode = res['tunnel_interfaces'][0]['vpn']['ip_assignment']['mode']['static']
        if mngm['https']==True and mngm['ping']==False and mngm['snmp']==False and mngm['ssh']==True:
            if user['http']==True and user['https']==True:
                if mode['ip']==VPN_BGP_IP_LOCAL and mode['netmask']=='255.255.0.0':
                    rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check Modify TI failed")

    def test_42_02_Restore_Setting(self):
        logger.info(" {} ".center(20, '-').format('Restore Setting')) 
        rc = Linterface.config_interface(**Tunnel_Interface)
        Assertion.assert_equal(rc, True, "ERR: Restore Setting failed")


class TestNumbered_TI_43(Test):
    uuid = "SOSAIOT-TC-54529"
    description = show_testcase_info(TESTPLAN, "04", description=True)['title']

    def test_43_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "04")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_43_01_Edit_TI(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_BGP_IP_LOCAL
        ref2["ip"] =  VPN_BGP_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Edit Local Vpn Tunnel Interface'))
        rc = Linterface.config_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Edit Remote Vpn Tunnel Interface'))
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc,True, "ERR: Edit Vpn Tunnel Interface failed")

    def test_43_02_Turn_BGP_On(self):
        logger.info(" {} ".center(20, '-').format('Turn BGP On'))
        rc = LDynRouteObj.set_BGP(BGP = "on")
        rc &= RDynRouteObj.set_BGP(BGP = "on")
        Assertion.assert_equal(rc,True, "ERR: Turn BGP On failed")

    def test_43_03_Set_BGP(self):
        logger.info(" {} ".center(20, '-').format('Set BGP in CLI'))
        rc = fw_cli.do_cli_commands(local_bgp_cmds)
        rc &= rm_cli.do_cli_commands(remote_bgp_cmds)
        Assertion.assert_equal(rc, True, "ERR: Set BGP in CLI failed")

    def test_43_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
        for i in range(10):
            cmd = "ping {} -c 10 -w 1".format(PC2_IP)
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_43_05_Restore_Setting(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_IF_IP_LOCAL
        ref2["ip"] =  VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Turn BGP Off'))
        rc = LDynRouteObj.set_BGP(BGP='off')
        rc &= RDynRouteObj.set_BGP(BGP='off')
        logger.info(" {} ".center(20, '-').format('Edit Local Vpn Tunnel Interface'))
        rc &= Linterface.config_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Edit Remote Vpn Tunnel Interface'))
        rc &= Rinterface.config_interface(**ref2)
        Assertion.assert_equal(rc,True, "ERR: Restore Setting failed")


class TestNumbered_TI_44(Test):
    uuid = "SOSAIOT-TC-54561"
    description = show_testcase_info(TESTPLAN, "09", description=True)['title']

    def test_44_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "09")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_44_01_Set_Local_Access_Rule(self):
        logger.info(" {} ".center(20, '-').format('Set Access Rule for DUT'))
        rule = copy.deepcopy(rule_opt)
        rule['name'] = 'LAN_to_VPN'
        rule['from'] = 'LAN'
        rule['to']   = 'VPN'
        rc = Laccess_rule_obj.put_accessrule(**rule)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: config access rule LAN to VPN  in DUT2 failed")

    @repeat_method(4)
    def test_44_02_Check_HTTPS(self):
        logger.info(" {} ".center(20, '-').format('Check HTTPS,visit InterFace {}'.format(VPN_IF_IP_REMOTE)))
        FW_API = FirewallAPI(VPN_IF_IP_REMOTE)
        rc = FW_API.api_login()
        Assertion.assert_equal(rc, True, "ERR: check HTTPs failed")
    
class TestNumbered_TI_45(Test):
    uuid = "SOSAIOT-TC-54512"
    description = show_testcase_info(TESTPLAN, "10", description=True)['title']

    def test_45_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "10")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(10)
    def test_45_01_Check_SSH(self):
        logger.info(" {} ".center(20, '-').format('Check SSH,visit InterFace {}'.format(VPN_IF_IP_REMOTE)))
        FW_CLI = Firewall(VPN_IF_IP_REMOTE, user='admin', password='password', supported_config_mode='cli-ssh')
        rc = FW_CLI.cli_login()
        Assertion.assert_equal(rc, True, "ERR: check SSH failed")


class Test_Tear_down(Test):
    uuid = 'NonTC'
    description = "clear env config settings"

    def test_01_01_remove_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Delete Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        rc &= RRoutePolicyObj.del_route_policy_by_name(name = 'ti_route')
        Assertion.assert_equal(rc, True, 'Remove Route Policy Failed.')
    
    def test_01_02_remove_Tunnel_Interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_IF_IP_LOCAL
        ref2["ip"] =  VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Delete Vpn Tunnel Interface'))
        rc = Linterface.del_interface(**ref1)
        rc &= Rinterface.del_interface(**ref2)
        Assertion.assert_equal(rc, True, 'Remove Vpn Tunnel Interface Failed.')

    def test_01_03_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

  