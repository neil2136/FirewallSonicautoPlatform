from definition.settings import *


class Test_IPv6_VPN_TP2334_01(Test):
    uuid = "SOSAIOT-TC-54452"
    description= show_testcase_info(TESTPLAN, '1524531', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524531')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ipv6_vpn_policy(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['sec_gate'] = '2001:db2::193'
        rc = Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, f"ERR: check failover info fail.")

    def test_02_check_vpn_policy(self):
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref = out['vpn']['policy'][0]['ipv6']['site_to_site']
        rc = True if ref['name']=='vpn1' and ref['gateway']['primary'] == '2001:db1:0:0:0:0:0:193' and ref['gateway']['secondary'] == '2001:db2:0:0:0:0:0:193' else False
        Assertion.assert_equal(rc , True, f"ERR: check gateway in policy fail.")


#base_01
class Test_IPv6_VPN_TP2334_02(Test):
    uuid = "SOSAIOT-TC-54451"
    description= show_testcase_info(TESTPLAN, '1524530', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524530')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_and_check_policy_version(self):
        res1 = Lvpn_obj.show_ipv6vpnpolicy()
        res2 = Lvpn_obj.show_all_vpn_policies()
        rc = True if 'WAN GroupVPN' in str(res2) and 'vpn1' in str(res1) else False
        Assertion.assert_equal(rc, True, f"ERR: show and check policy version info fail.")


class Test_IPv6_VPN_TP2334_03(Test):
    uuid = "SOSAIOT-TC-54453"
    description= show_testcase_info(TESTPLAN, '1524532', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524532')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ikev4_not_allowed_null(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        ref['local_ike_type'] = 'ipv4'
        ref['peer_ike_type'] = 'domain_name'
        ref['local_ike_id'] = ''
        ref['peer_ike_id'] = 'domain.cn'
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        logger.info(f'----{res}')
        rc = True if "Local IKE ID not configured" in str(res[1]) and not res[0] else False
        Assertion.assert_equal(rc, True, f"ERR:check IPv4 IKE ID type to NULL is not allowed fail.")


#base_01
class Test_IPv6_VPN_TP2334_04(Test):
    uuid = "SOSAIOT-TC-54454"
    description= show_testcase_info(TESTPLAN, '1524533', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524533')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        rc = True if not res[0] and ("Address object remote_test_ipv6 overlaps in vpn1 policy" in str(res[1]) or "Address object remote_net_ipv6 overlaps in vpn1 policy" in str(res[1])) else False
        Assertion.assert_equal(rc, True, f"ERR: check add vpn policy ipv6 fail.")


#base_01
class Test_IPv6_VPN_TP2334_05(Test):
    uuid = "SOSAIOT-TC-54456"
    description= show_testcase_info(TESTPLAN, '1524535', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524535')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        ref['local_net_name'] = 'X0 IPv6 Primary Static Address'
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        rc = True if not res[0] and ("Address object remote_test_ipv6 overlaps in vpn1 policy" in str(res[1]) or "Address object remote_net_ipv6 overlaps in vpn1 policy" in str(res[1])) else False
        Assertion.assert_equal(rc, True, f"ERR: check add vpn policy ipv6 fail.")


#base_01
class Test_IPv6_VPN_TP2334_06(Test):
    uuid = "SOSAIOT-TC-54455"
    description= show_testcase_info(TESTPLAN, '1524534', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524534')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        ref['remote_net_name'] = local_test_ipv6['name']
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        rc = True if not res[0] and "Address object remote_test_ipv6 overlaps in vpn1 policy" in str(res[1]) else False
        Assertion.assert_equal(rc, True, f"ERR: check add vpn policy ipv6 fail.")


#base_01
class Test_IPv6_VPN_TP2334_07(Test):
    uuid = "SOSAIOT-TC-54457"
    description= show_testcase_info(TESTPLAN, '1524536', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524536')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_restart_and_check_vpn_policy(self):
        rc = LRestartObj.restart_now()
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref = out['vpn']['policy'][0]['ipv6']['site_to_site']
        if ref['name']=='vpn1' and ref['gateway']['primary'] == '2001:db1:0:0:0:0:0:193' and local_r_ipv6['name'] in str(ref['network']):
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: restart and check  vpn policy failed")


#base_01
class Test_IPv6_VPN_TP2334_08(Test):
    uuid = "SOSAIOT-TC-54458"
    description= show_testcase_info(TESTPLAN, '1524537', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524537')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_and_import_setting(self):
        rc = Lsetting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        rc &= Lvpn_obj.del_ipv6_vpn_policy(name='vpn1')
        rc &= Lsetting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: export and  import setting failed")

    def test_02_check_vpn_policy(self):
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref = out['vpn']['policy'][0]['ipv6']['site_to_site']
        if ref['name']=='vpn1' and ref['gateway']['primary'] == '2001:db1:0:0:0:0:0:193' and \
            ref['network']['remote']['destination_network']['name'] == local_r_ipv6['name']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check  vpn policy failed")


class Test_IPv6_VPN_TP2334_09(Test):
    uuid = "SOSAIOT-TC-54470"
    description= show_testcase_info(TESTPLAN, '1524550', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524550')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_Invalid_format(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        ref['local_ike_id'] = '10.10.10.10'
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        rc = True if not res[0] and "property 'ipv6': invalid format" in str(res[1]) else False
        Assertion.assert_equal(rc, True, f"ERR: check Invalid format for IPv6 Address Local IKE ID fail.")


class Test_IPv6_VPN_TP2334_10(Test):
    uuid = "SOSAIOT-TC-54471"
    description= show_testcase_info(TESTPLAN, '1524551', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524551')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_Invalid_format(self):
        ref  = copy.deepcopy(Lvpn_ipv6)
        ref['name'] = 'vpn2'
        ref['peer_ike_type'] = 'ipv4'
        ref['peer_ike_id'] = Remote_X0_IPV6
        res = Lvpn_obj.add_ipv6_vpn_policy(msg=True,**ref)
        rc = True if not res[0] and "property 'ipv4': invalid format" in str(res[1]) else False
        Assertion.assert_equal(rc, True, f"ERR: check Invalid format for IPv4 Address peer IKE ID fail.")


#base_01
class Test_IPv6_VPN_TP2334_11(Test):
    uuid = "SOSAIOT-TC-54474"
    description= show_testcase_info(TESTPLAN, '2357388', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2357388')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        "X0 IPv6 Primary Dynamic Address Subnet"
        ref1  = copy.deepcopy(Lvpn_ipv6)
        ref2  = copy.deepcopy(Lvpn_ipv6)
        ref1['name'] = 'vpn2'
        ref1['pri_gate'] = '2001::1093'
        ref1['local_net_name'] = 'X1 IPv6 Primary Static Address'
        ref2['name'] = 'vpn3'
        ref2['pri_gate'] = '2001:df1::193'
        ref2['sec_gate'] = ''
        ref2['local_net_name'] = 'X2 IPv6 Primary Static Address'
        rc = Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    def test_02_disable_and_check_policy(self):
        rc = Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn1',enable=False)
        rc &= Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn2',enable=False)
        rc &= Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn3',enable=False)
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref1 = out['vpn']['policy'][0]['ipv6']['site_to_site']
        ref2 = out['vpn']['policy'][1]['ipv6']['site_to_site']
        ref3 = out['vpn']['policy'][2]['ipv6']['site_to_site']
        if ref1['enable'] == False and ref2['enable'] == False and ref3['enable'] == False:
            rc &= True
        else:
            rc &=False
        Assertion.assert_equal(rc, True, f"ERR: disable and check policy fail.")

    def test_03_enable_and_check_policy(self):
        rc = Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn1',enable=True)
        rc &= Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn2',enable=True)
        rc &= Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn3',enable=True)
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref1 = out['vpn']['policy'][0]['ipv6']['site_to_site']
        ref2 = out['vpn']['policy'][1]['ipv6']['site_to_site']
        ref3 = out['vpn']['policy'][2]['ipv6']['site_to_site']
        if ref1['enable'] == True and ref2['enable'] == True and ref3['enable'] == True:
            rc &= True
        else:
            rc &=False
        Assertion.assert_equal(rc, True, f"ERR: enable and check policy fail.")


#base_01,base_11 
class Test_IPv6_VPN_TP2334_12(Test):
    uuid = "SOSAIOT-TC-54475"
    description= show_testcase_info(TESTPLAN, '2357391', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2357391')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_modify_vpn_policy(self):
        ref1  = copy.deepcopy(Lvpn_ipv6)
        ref1['name'] = 'vpn2'
        ref1['pri_gate'] = '2001::193'
        ref1['local_net_name'] = 'X1 IPv6 Primary Static Address'
        rc = Lvpn_obj.edit_ipv6_vpn_policy(**ref1)
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref = out['vpn']['policy'][1]['ipv6']['site_to_site']
        if ref['name']=='vpn2' and ref['gateway']['primary'] == '2001:0:0:0:0:0:0:193':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: modify vpn policy fail.")

    def test_02_disable_vpn_policy(self):
        ref1  = copy.deepcopy(Lvpn_ipv6)
        ref1['name'] = 'vpn2'
        ref1['pri_gate'] = '2001::193'
        ref1['local_net_name'] = 'X1 IPv6 Primary Static Address'
        rc = Lvpn_obj.config_ipv6_vpn_policy(name = 'vpn2',enable=False)
        rc &= Lvpn_obj.edit_ipv6_vpn_policy(**ref1)
        out = Lvpn_obj.show_ipv6vpnpolicy()
        ref = out['vpn']['policy'][1]['ipv6']['site_to_site']
        if ref['name']=='vpn2' and ref['gateway']['primary'] == '2001:0:0:0:0:0:0:193' and ref['network']['local']['name'] =='X1 IPv6 Primary Static Address':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: disable and check vpn policy fail.")

    def test_03_restore_env(self):
        rc = Lvpn_obj.del_ipv6_vpn_policy(name='vpn2')
        rc &= Lvpn_obj.del_ipv6_vpn_policy(name='vpn3')
        Assertion.assert_equal(rc, True, f"ERR: restore env fail.")


class Test_IPv6_VPN_TP2334_13_CONFIGENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_vpn_policy_ipv6(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        logger.info(" {} ".center(20, '*').format('clear log'))
        Log_obj.clear_log()
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy IPv6 Failed.') 

    def test_02_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_VPN_TP2334_14(Test):
    uuid = "SOSAIOT-TC-54459"
    description= show_testcase_info(TESTPLAN, '1524538', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524538')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_log_vpn_tunnel(self):
        out = Log_obj.show_log()
        rc = True if "IKEv2 negotiation complete" in str(out) else False
        res = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        if res[0]['policyName'] =='vpn1':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_02_restart_and_check_tunnel(self):
        rc = LRestartObj.restart_now()
        time.sleep(15)
        res = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        if res[0]['policyName'] =='vpn1':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check active  vpn tunnel after restart fail.")


class Test_IPv6_VPN_TP2334_15(Test):
    uuid = "SOSAIOT-TC-54460"
    description= show_testcase_info(TESTPLAN, '1524539', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524539')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1["local_net_name"] = "local_host"
        ref1["remote_net_name"] = "remote_host"
        ref2["local_net_name"] = "local_host"
        ref2["remote_net_name"] = "remote_host"
        Log_obj.clear_log()
        Rlog_obj.clear_log()
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    @repeat_method(3)
    def test_02_check_log_vpn_tunnel(self):
        time.sleep(15)
        out1 = Log_obj.show_log()
        check_str= "Local Net: 2001:db0.*?-2001:db0.*?Remote Net: 2001:db2.*?-2001:db2.*?IKEv2 negotiation complete"
        rc = True if re.search(check_str, str(out1), re.M)  else False
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        res2 = Rvpn_obj.get_active_vpn_tunnels_ipv6()
        logger.info(f'--------{res2}------------')
        if res1[0]['policyName'] =='vpn1' and res2[0]['policyName'] =='vpn2' :
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            out2 = PC1.send_commands([f'ping6 -c 3 {PC3_ETH1_IPV6}'])
            if '100% packet loss' not in out1 and '100% packet loss'  in out2:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")
        

class Test_IPv6_VPN_TP2334_16(Test):
    uuid = "SOSAIOT-TC-54461"
    description= show_testcase_info(TESTPLAN, '1524540', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524540')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1["local_net_name"] = local_l_x0['name']
        ref1["remote_net_type"] = "group"
        ref1["remote_net_group"] = local_r_group['address_groups'][0]['ipv6']['name']
        ref2["local_net_type"] = "group"
        ref2["local_net_group"] = remote_l_group['address_groups'][0]['ipv6']['name']
        Log_obj.clear_log()
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    @repeat_method(3)
    def test_02_check_log_vpn_tunnel(self):
        time.sleep(15)
        out1 = Log_obj.show_log()
        check_str1= "Local Net: 2001:db0.*?2001:db0.*?Remote Net: 2001:db2.*?2001:db2.*?IKEv2 negotiation complete"
        check_str2= "Local Net: 2001:db0.*?2001:db0.*?Remote Net: 2001:db4.*?2001:db4.*?IKEv2 negotiation complete"
        rc = True if re.search(check_str1, str(out1), re.M) and re.search(check_str2, str(out1), re.M)  else False
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        if res1[0]['policyName'] =='vpn1' and ('2001:db4' in res1[0]['inDstNet'] or '2001:db2' in res1[0]['inDstNet']) \
            and  ('2001:db2' in res1[1]['inDstNet'] or '2001:db4' in res1[1]['inDstNet']):
            rc &= True
        else:
            rc &= False
            logger.info('check active vpn tunnel failed')
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            ##config pc3 ipv6 
            out2 = PC1.send_commands([f'ping6 -c 3 {PC3_ETH1_IPV6}'])
            if '100% packet loss' not in out1 and '100% packet loss' not in out2:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_VPN_TP2334_17(Test):
    uuid = "SOSAIOT-TC-54462"
    description= show_testcase_info(TESTPLAN, '1524541', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524541')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1['pri_gate'] = '2001:df1::193'
        ref1['sec_gate'] = '2001:db1::193'
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    def test_02_check_traffic(self):
        rc = False
        LpacketObj.clear_packets()
        LpacketObj.start_capture()
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out1 :
                rc = True
                logger.info("ping traffic is success!!")
                break
        LpacketObj.stop_capture()
        res = LpacketObj.export_captured_packets()
        logger.info(f'-----{res}------')
        # check_str1 = "Forwarded[\s\S.]*?src=[2001:db1::183], Dst=[2001:db1::193]"
        # check_str2 = "Forwarded.*?src=[2001:df1::183], Dst=[2001:df1::193]"
        res= (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if 'Forwarded'  in i and 'Src=[2001:db1::183], Dst=[2001:db1::193]' in i :
                rc2 = True
                logger.info('----check package monitor successful')
            if 'Forwarded'  in i and 'Src=[2001:df1::183], Dst=[2001:df1::193]' in i :
                rc  &= False
                logger.info('----check package monitor failed !!!')
        Assertion.assert_equal(rc&rc2, True, "ERR: check traffic failed")


class Test_IPv6_VPN_TP2334_18(Test):
    uuid = "SOSAIOT-TC-54463"
    description= show_testcase_info(TESTPLAN, '1524542', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524542')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1['local_ike_id'] = DUT_X0_IPV6
        ref1['peer_ike_id'] = Remote_X0_IPV6
        ref2['local_ike_id'] = Remote_X0_IPV6
        ref2['peer_ike_id'] = DUT_X0_IPV6
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    @repeat_method(3)
    def test_02_check_log_vpn_tunnel(self):
        time.sleep(15)
        out1 = Log_obj.show_log()
        check_str= "Local Net: 2001:db0.*?-2001:db0.*?Remote Net: 2001:db2.*?-2001:db2.*?IKEv2 negotiation complete"
        rc = True if re.search(check_str, str(out1), re.M)  else False
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        res2 = Rvpn_obj.get_active_vpn_tunnels_ipv6()
        logger.info(f'--------{res2}------------')
        if res1[0]['policyName'] =='vpn1' and res2[0]['policyName'] =='vpn2' :
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out1 :
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

###skip for now  uuid = '1524543'
class Test_IPv6_VPN_TP2334_19(Test):
    uuid = "SOSAIOT-TC-54465"
    description= show_testcase_info(TESTPLAN, '1524544', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524544')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1['remote_net_name'] = local_r_net['name']
        ref2['local_net_name'] = remote_l_net['name']
        Log_obj.clear_log()
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    @repeat_method(3)
    def test_02_check_log_vpn_tunnel(self):
        time.sleep(15)
        out1 = Log_obj.show_log()
        check_str1= "IKEv2 negotiation complete"
        rc = True if re.search(check_str1, str(out1), re.M)  else False
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        if res1[0]['policyName'] =='vpn1' and '2001:db0:: - 2001:db0::ffff:ffff:ffff:ffff' in str(res1[0]['localNet']) \
            and  ':: - ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff' in str(res1[0]['remoteNet']):
            rc &= True
        else:
            rc &= False
            logger.info('check active vpn tunnel failed')
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out1 :
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


###based tc19
class Test_IPv6_VPN_TP2334_20(Test):
    uuid = "SOSAIOT-TC-54466"
    description= show_testcase_info(TESTPLAN, '1524545', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524545')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ipv6_active_tunnel(self):
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        res2 = Lvpn_obj.get_active_vpn_tunnels()
        if res1[0]['policyName'] =='vpn1' and not res2:
            rc &=True
            logger.info("check IPv6 active tunnels success!!")
        else:
            rc &= False 
        Assertion.assert_equal(rc, True, "ERR: check IPv6 active tunnels  failed")


###based tc19
class Test_IPv6_VPN_TP2334_21(Test):
    uuid = "SOSAIOT-TC-54467"
    description= show_testcase_info(TESTPLAN, '1524546', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524546')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_check_big_packet_fragment(self):
        rc = False
        LpacketObj.clear_packets()
        LpacketObj.start_capture()
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 -s 2800 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out1 :
                rc = True
                logger.info("ping traffic is success!!")
                break
        LpacketObj.stop_capture()
        res = LpacketObj.export_captured_packets()
        logger.info(f'-----{res}------')
        res= (res.split("Packet number:"))[1:]
        rc2 = False
        pkg_num = 0
        for i,pkg in  enumerate(res):
            if "Forwarded" in pkg and "Bytes captured: 1498" in pkg:
                pkg_num = i
                logger.info(f"first fragment pkg is found,num is {pkg_num}, pkg is {pkg},------")
                rc2 = True
                break
        if "Forwarded" in res[pkg_num+1] and "Bytes captured: 1498" in res[pkg_num+1] \
            and "Forwarded" in res[pkg_num+2] and "Bytes captured: 250" in res[pkg_num+2]:
            rc2 &= True
            logger.info(f'second and third fragments pkg is found!!!')
        else:
            rc2 &= False
            logger.info(f'the next pkg id is {pkg_num+1},the pkg info is {res[pkg_num+1]},-----{res[pkg_num+2]} ')
        Assertion.assert_equal(rc&rc2, True, "ERR: check fragment info failed")


###based tc19
class Test_IPv6_VPN_TP2334_22(Test):
    uuid = "SOSAIOT-TC-54468"
    description= show_testcase_info(TESTPLAN, '1524548', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524548')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_ipv4(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc = Rvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.del_all_vpn_policies()
        rc &= Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc &= Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.') 

    @repeat_method(3)
    def test_02_check_active_tunnel(self):
        time.sleep(8)
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        res2 = Lvpn_obj.get_active_vpn_tunnels()
        if res1[0]['policyName'] =='vpn1' and  res2[0]['policyName'] == Lvpn['name']:
            rc =True
            logger.info("check IPv6 active tunnels success!!")
        else:
            rc = False 
        Assertion.assert_equal(rc, True, "ERR: check  active tunnels  failed")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            out2 = PC1.send_commands([f'ping -c 3 {PC2_ETH1_IPV4}'])
            if '100% packet loss' not in out1 and '100% packet loss' not in out2:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    
###skip  uuid = '1524549',need upload firmware that didn't support ipv6
class Test_IPv6_VPN_TP2334_23(Test):
    uuid = "SOSAIOT-TC-54472"
    description= show_testcase_info(TESTPLAN, '1265752', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1265752')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_ipv6)
        ref2 = copy.deepcopy(Rvpn_ipv6)
        ref1["pri_gate"] = Remote_X3_IPV6
        ref1["sec_gate"] = ""
        ref2["pri_gate"] = DUT_X3_IPV6
        Log_obj.clear_log()
        rc = Rvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.del_all_ipv6_vpn_policies()
        rc &= Lvpn_obj.add_ipv6_vpn_policy(**ref1)
        rc &= Rvpn_obj.add_ipv6_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: add vpn policy fail.")

    @repeat_method(3)
    def test_02_check_log_vpn_tunnel(self):
        time.sleep(15)
        out1 = Log_obj.show_log()
        check_str1= "Local Net: 2001:db0.*?2001:db0.*?Remote Net: 2001:db2.*?2001:db2.*?IKEv2 negotiation complete"
        rc = True if re.search(check_str1, str(out1), re.M)  else False
        res1 = Lvpn_obj.get_active_vpn_tunnels_ipv6()
        ##{"localNet":{"range":"2001:db0:: - 2001:db0::ffff:ffff:ffff:ffff"},"remoteNet":{"range":"2001:db2:: - 2001:db2::ffff:ffff:ffff:ffff"}}
        if res1[0]['policyName'] =='vpn1' and  res1[0]['gateway'] == Remote_X3_IPV6  \
            and "2001:db0::" in str(res1[0]['localNet']) and "2001:db2::" in str(res1[0]['remoteNet']):
            rc &= True
        else:
            rc &= False
            logger.info('check active vpn tunnel failed')
        Assertion.assert_equal(rc, True, f"ERR: check log and vpn tunnel fail.")

    def test_03_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out1 = PC1.send_commands([f'ping6 -c 3 {PC2_ETH1_IPV6}'])
            if '100% packet loss' not in out1 :
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

###skip  uuid = '1265753'

    