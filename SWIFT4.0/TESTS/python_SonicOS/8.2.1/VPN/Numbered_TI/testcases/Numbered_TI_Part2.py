from definition.settings import *

##################add new case######################
# add  vpn tunnel policy and add Tunnel interface
class Test_01_SetUpEnv(Test):
    uuid = 'NonTC'
    description = "Set up env"

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        logger.info("Remote VPN Policy {} ".format(ref2))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.') 

    def test_02_add_Tunnel_interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  VPN_IF_IP_LOCAL
        ref2["ip"] =  VPN_IF_IP_REMOTE
        logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
        rc = Linterface.add_interface(**ref1)
        logger.info(" {} ".center(20, '-').format('Add Remote Vpn Tunnel Interface'))
        rc &= Rinterface.add_interface(**ref2)
        Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

    def test_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")


class Test_02_Numbered_TI(Test):
    uuid = "SOSAIOT-TC-54565"
    description = show_testcase_info(TESTPLAN, "1527667", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1527667")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['name'] = 'test2'
        ref1['pri_gate'] ='1.2.3.4'
        ref1['local_ike_id'] = PC1_IP
        ref1['peer_ike_id']= PC2_IP
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        logger.info("Local VPN Policy {} ".format(ref1))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc1 , True, 'Add VPN Policy Failed.') 

    def test_02_add_Tunnel_interface(self):
        ref1 = copy.deepcopy(Tunnel_Interface)
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref1["ip"] =  '2.2.2.3'
        ref1["tunnel_name"] =  'test'
        ref2["ip"] =  '2.2.2.3'
        ref2["tunnel_name"] =  'test'
        ref2["vpn_policy"] =  'test2'
        logger.info(" {} ".center(20, '-').format('Add Local Vpn Tunnel Interface'))
        rc1 = Linterface.add_interface(**ref1,msg=True)
        rc2 = Linterface.add_interface(**ref2)
        rc = True if not rc1[0] and 'The selected VPN policy is already used by another VPN Tunnel Interface' in rc1[1]['status']['info'][0]['message'] and rc2 else False
        Assertion.assert_equal(rc, True, "ERR: Add Vpn Tunnel Interface failed")

###based 2
class Test_03_Numbered_TI(Test):
    uuid = "SOSAIOT-TC-54564"
    description = show_testcase_info(TESTPLAN, "1945878", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1945878")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_vpn_policy(self):
        ref = copy.deepcopy(Lvpn)
        ref["enable"] = False
        ref['name'] = 'test2'
        ref['pri_gate'] ='1.2.3.4'
        ref['local_ike_id'] = PC1_IP
        ref['peer_ike_id']= PC2_IP
        rc = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc, True, 'disable vpn policy Failed.')

    def test_02_restart_and_delete_policy(self):
        rc = LRestartObj.restart_now()
        ref1 = copy.deepcopy(Lvpn)
        ref1['name'] = 'test2'
        ref2 = copy.deepcopy(Tunnel_Interface)
        ref2["tunnel_name"] =  'test'
        rc &= Linterface.del_interface(**ref2)
        rc &= Lvpn_obj.del_tunnelvpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'delete vpn policy Failed.')

    def test_03_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        rc = True
        logger.info(f'--{res}')
        for policy in res['vpn']['policy']:
            if policy['ipv4']['tunnel_interface']['name'] == 'test2':
                rc = False
                logger.info('cannnot find the policy!!')
        Assertion.assert_equal(rc, True, "ERR: check policy failed")

    
class Test_04_Numbered_TI(Test):
    uuid = "SOSAIOT-TC-54560"
    description = show_testcase_info(TESTPLAN, "1513127", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1513127")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_disable_vpn_policy(self):
        res=LRoutePolicyObj.show_route_policy_status(name='ti_route',version='ipv4')
        logger.info(f'----{res}')
        rc1 = True if 'active'==str(res) else False
        ref = copy.deepcopy(Lvpn)
        ref["enable"] = False
        rc2 = Lvpn_obj.edit_vpn_policy(**ref)
        Assertion.assert_equal(rc1 & rc2, True, 'disable vpn policy Failed.')

    @repeat_method(3)
    def test_02_check_route_policy(self):
        res=LRoutePolicyObj.show_route_policy_status(name='ti_route',version='ipv4')
        logger.info(f'----{res}')
        rc1 = True if 'inactive'==str(res) else False
        Assertion.assert_equal(rc1 , True, 'check route policy Failed.')

    def test_03_restore_env(self):
        logger.info(" {} ".center(20, '-').format('Restore ENV'))
        ref1 = copy.deepcopy(Lvpn)
        rc1 = Lvpn_obj.edit_vpn_policy(**ref1)
        Assertion.assert_equal(rc1 , True, 'Restore ENV Failed.')


class Test_05_Numbered_TI(Test):
    uuid = "SOSAIOT-TC-54546"
    description = show_testcase_info(TESTPLAN, "1513113", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1513113")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ipv6_interface(self):
        res=Linterface_v6.show_interface()
        logger.info(f'----{res}')
        rc = True
        for interface in res['interfaces']:
            if interface['ipv6']['name']=='Ni':
                rc = False
        Assertion.assert_equal(rc , True, 'check ipv6 interface Failed.')

    def test_02_try_add_ipv6_route_policy(self):
        res=LRoutePolicyObj.add_route_policy(msg=True,**route_policy3)
        logger.info(f'----{res}')
        if not res[0] and 'Interface value is unreasonable' in res[1]['status']['info'][0]['message']:
            rc =True
        else:
            rc = False
        Assertion.assert_equal(rc , True, 'try add ipv6 route Failed.')


class Test_06_Numbered_TI(Test):
    uuid = "SOSAIOT-TC-54524"
    description = show_testcase_info(TESTPLAN, "1513091", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "1513091")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Export_and_Import_Prefs(self):
        logger.info(" {} ".center(20, '-').format('Export and Import Prefs '))
        ref = copy.deepcopy(Lvpn)
        ref["enable"] = False
        res = Lvpn_obj.show_tunnelvpnpolicy()
        rc = Lsetting.export_setting_exp(filepath='/tmp/prefs_module')
        time.sleep(5)
        rc &= Lvpn_obj.edit_vpn_policy(**ref)
        rc &= Lsetting.import_setting_exp(filepath='/tmp/prefs_module')
        Assertion.assert_equal(rc, True, "ERR: Export and Import Prefs failed") 

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        rc = False
        logger.info(f'--{res}')
        for policy in res['vpn']['policy']:
            if policy['ipv4']['tunnel_interface']['name'] == 'test' and \
                policy['ipv4']['tunnel_interface']['enable'] == True:
                rc = True
                logger.info(' check the vpn policy success!!')
                break
        Assertion.assert_equal(rc, True, "ERR: check policy failed")


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