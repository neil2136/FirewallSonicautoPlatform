from definition.settings import *


class TestVPN_FQDN_based_NAT_01(Test):
    uuid = "SOSAIOT-TC-56032"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_Add_NatRule(self):
        logger.info(" {} ".center(20, '-').format('Add Nat Rule for DUT'))
        rc = natPolicyObj.add_nat_policy(**nat_opts)
        Assertion.assert_equal(rc, True, f"ERR: Add Nat Rule for DUT failed")

    def test_01_02_Check_Delet_AO(self):
        logger.info(" {} ".center(20, '-').format('Check delete AO used Nat policy'))
        _,resp =  LAddrOBJ.delete_addressobject(object_type='fqdn', object_path='name', object_name_uuid=opt2['name'],ip_type='ipv4',msg = True)
        if 'Object is in use by a NAT Policy' in  resp['status']['info'][0]['message']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Check delete AO used Nat policy failed")


class TestVPN_FQDN_based_NAT_02(Test):
    uuid = "SOSAIOT-TC-56034"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_02_01_Check_Edit_AO(self):
        logger.info(" {} ".center(20, '-').format('Check Edit AO used Nat policy'))
        rc = LAddrOBJ.edit_addressobject(object_type='fqdn', object_path='name', obj_name_uuid=opt2['name'],ip_type='ipv4',json_put=edit_opt2)
        Assertion.assert_equal(rc, True, "ERR: Check Edit AO used Nat policy failed")

    def test_02_02_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(edit_opt2)
        ref['address_objects'][0]['fqdn']['domain'] = wanpc_fqdn
        rc = LAddrOBJ.edit_addressobject(object_type='fqdn', object_path='name', obj_name_uuid=opt2['name'],ip_type='ipv4',json_put=ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_03(Test):
    uuid = "SOSAIOT-TC-56033"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_03_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={"group":'nat_group'}
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit Nat policy failed")

    def test_03_02_Edit_AO_Group(self):
        logger.info(" {} ".center(20, '-').format('Edit AO Group'))
        ref = copy.deepcopy(opt8)
        opt = ref['address_groups'][0]
        opt['ipv6']=opt.pop('ipv4')
        opt['ipv6']['address_object']['ipv4'].append({"name":"member1"})
        rc = LAddrGroupOBJ.edit_addressgroup_by_name(version='v6',name = 'nat_group',**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit AO Group failed")
 

class TestVPN_FQDN_based_NAT_04(Test):
    uuid = "SOSAIOT-TC-56039"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_04_01_Add_AO(self):
        logger.info(" {} ".center(20, '-').format('Add AO '))
        rc = LAddrOBJ.config_addressobject(**opt9)
        Assertion.assert_equal(rc, True, "ERR: Add AO  failed")

    def test_04_02_Add_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['name'] = 'nap_policy'
        opt['source']['name']='fqdntest'
        rc = natPolicyObj.add_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    def test_04_03_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        rc = natPolicyObj.del_nat_policy_by_name(name = 'nap_policy')
        rc &= LAddrOBJ.delete_addressobject(object_type='fqdn', object_path='name', object_name_uuid=opt9['name'],ip_type='ipv4')
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_05(Test):
    uuid = "SOSAIOT-TC-56035"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_05_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'name':opt2['name']}
        opt['destination']={'name':'X1 IP'}
        opt['translated_source'] = {'original': True}
        opt['translated_destination'] = {'name': opt1['name']}
        opt['inbound'] = 'X1'
        opt['outbound'] = 'any'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        # print('****'*10,X1_ip)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    def test_05_02_Ping_from_PC2_to_PC1(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc2 to pc1 '))
        cmd = f'ping {X1_ip} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC2.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous icmp traffic.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{PC2_IP}]'  in i and f'Dst=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc2 to pc1 failed")


class TestVPN_FQDN_based_NAT_06(Test):
    uuid = "SOSAIOT-TC-56036"
    description = show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_06_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'X1'
        opt['outbound'] = 'any'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    def test_06_02_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping {wanpc_fqdn} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
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
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 


class TestVPN_FQDN_based_NAT_07(Test):
    uuid = "SOSAIOT-TC-56037"
    description = show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_07_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt3['name']}
        opt['translated_source'] = {'original': True}
        opt['translated_destination'] = {'name': opt1['name']}
        opt['inbound'] = 'X1'
        opt['outbound'] = 'any'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    def test_07_02_Ping_from_PC2_to_PC1(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc2 to pc1 '))
        cmd = f'ping {X1_IP_N} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC2.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Successfully initiated continuous icmp traffic.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if 'Dst=[192.168.168.169]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc2 to pc1 failed")


class TestVPN_FQDN_based_NAT_08(Test):
    uuid = "SOSAIOT-TC-56038"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_08_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":opt3['name']}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    @repeat_method(3)
    def test_08_02_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        time.sleep(10)
        cmd = f'ping {wanpc_fqdn} -c 30'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
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
        LPackageMonitObj.stop_capture()
        time.sleep(10)
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_IP_N}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        if not rc2:
            logger.error('----check package monitor successful')
            logger.info(res)
            nat_policy = natPolicyObj.get_nat_policy(version='ipv4', name='tc_nat_rule')
            logger.info(f'The nat policy detail is:{nat_policy}')
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 


class TestVPN_FQDN_based_NAT_09(Test):
    uuid = "SOSAIOT-TC-56040"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_09_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":opt3['name']}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Edit Nat policy failed")

    @repeat_method(3)
    def test_09_02_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        time.sleep(10)
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 30'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        time.sleep(10)
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_IP_N}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        if not rc2:
            logger.error('----check package monitor successful')
            logger.info(res)
            nat_policy = natPolicyObj.get_nat_policy(version='ipv4', name='tc_nat_rule')
            logger.info(f'The nat policy detail is:{nat_policy}')
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_09_03_Del_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        rc = natPolicyObj.del_nat_policy_by_name(name = 'tc_nat_rule')
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")
    
    def test_09_04_Check_Ping_Traffic(self):
        logger.info(" {} ".center(20, '-').format('Check Ping when delete a NAT policy'))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 30'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
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
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Check Ping when delete a NAT policy")

    def test_09_05_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        rc = natPolicyObj.add_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_10(Test):
    uuid = "SOSAIOT-TC-56041"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_10_01_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 15'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_10_02_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":opt3['name']}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    @repeat_method(3)
    def test_10_03_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        time.sleep(10)
        cmd = f'ping -I  {PC1_IP} {wanpc_fqdn} -c 15'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
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
        LPackageMonitObj.stop_capture()
        time.sleep(10)
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_IP_N}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        if not rc2:
            logger.error('----check package monitor successful')
            logger.info(res)
            nat_policy = natPolicyObj.get_nat_policy(version='ipv4', name='tc_nat_rule')
            logger.info(f'The nat policy detail is:{nat_policy}')
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_10_05_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_11(Test):
    uuid = "SOSAIOT-TC-56042"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_11_01_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 15'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_11_02_Disable_and_Add_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Disable and Add Nat Policy '))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['enable'] = False
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        ref2 = copy.deepcopy(nat_opts)
        opts = ref2['nat_policies'][0]['ipv4']
        opts['name']='nap_policy'
        opts['source']={'any':True}
        opts['destination']={'name':opt2['name']}
        opts['translated_source'] = {"name":opt3['name']}
        opts['translated_destination'] = {'original': True}
        opts['inbound'] = 'any'
        opts['outbound'] = 'X1'
        rc = natPolicyObj.edit_nat_policy(**ref)
        rc &= natPolicyObj.add_nat_policy(**ref2)
        time.sleep(60)
        Assertion.assert_equal(rc, True, "ERR: Disable and Add Nat Policy failed") 

    @repeat_method(3)
    def test_11_03_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        time.sleep(10)
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 15'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ,check failed')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed,check Successful')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        time.sleep(10)
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_IP_N}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        if not rc2:
            logger.error('----check package monitor successful')
            logger.info(res)
            nat_policy = natPolicyObj.get_nat_policy(version='ipv4', name='nap_policy')
            logger.info(f'The nat policy detail is:{nat_policy}')
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_11_04_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.del_nat_policy_by_name(name = 'nap_policy')
        rc &= natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_12(Test):
    uuid = "SOSAIOT-TC-56045"
    description = show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_12_01_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_12_02_Export_and_Import_Prefs(self):
        logger.info(" {} ".center(20, '-').format('Export and Import Prefs '))
        rc = setting_obj.export_setting_exp(filepath='/tmp/prefs_module')
        rc &= natPolicyObj.del_nat_policy_by_name(name = 'tc_nat_rule')
        rc &= setting_obj.import_setting_exp(filepath='/tmp/prefs_module')
        Assertion.assert_equal(rc, True, "ERR: Export and Import Prefs failed") 

    def test_12_03_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 


class TestVPN_FQDN_based_NAT_13(Test):
    uuid = "SOSAIOT-TC-56046"
    description = show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_13_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_13_01_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_13_02_Restart_UTM(self):
        logger.info(" {} ".center(20, '-').format('Restart UTM '))
        rc = restart_obj.restart_now()
        Assertion.assert_equal(rc, True, "ERR: Restart UTM failed") 

    def test_13_03_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 5'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 


class TestVPN_FQDN_based_NAT_14(Test):
    uuid = "SOSAIOT-TC-56048"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_14_01_Ping_from_PC1_to_PC2(self):
        logger.info(" {} ".center(20, '-').format('Ping traffic from pc1 to pc2 '))
        cmd = f'ping -I {PC1_IP} {wanpc_fqdn} -c 30'
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        LPackageMonitObj.stop_capture()
        res = LPackageMonitObj.export_captured_packets()
        res = (res.split("Packet number:"))[1:]
        rc2 = False
        for i in res:
            if f'Src=[{X1_ip}]'  in i :
                rc2 = True
                logger.info('----check package monitor successful')
                break
        logger.info(res)
        Assertion.assert_equal(rc&rc2, True, "ERR: Ping traffic from pc1 to pc2 failed") 

    def test_14_02_Edit_Nat_Policy_by_CLI(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat Policy by CLI'))
        res = natPolicyObj.get_nat_policy_statistics(version="ipv4", original_destination=opt2['name'])
        uuid = res['uuid']
        nat_cli = ['configure',
            f'nat-policy ipv4 uuid {uuid}',
            'translated-source name x1_addr',
            'commit',
        ]
        logger.info(f'---***----{res}')
        rc = fw_cli.do_cli_commands(nat_cli)
        Assertion.assert_equal(rc, True, "ERR: Edit Nat Policy by CLI failed") 

    @repeat_method(3)
    def test_14_03_verify_nat_policy(self):
        logger.info(" {} ".center(20, '-').format('verify nat policy '))
        time.sleep(10)
        res = natPolicyObj.get_nat_policy(version='ipv4', name='tc_nat_rule')
        if 'x1_addr' == res['nat_policies'][0]['ipv4']['translated_source']['name']:
            rc = True
        else:
            rc = False
            logger.info(f'The nat policy detail is:{res}')
        Assertion.assert_equal(rc, True, "ERR:verify nat policy failed") 

    def test_14_04_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class TestVPN_FQDN_based_NAT_15(Test):
    uuid = "SOSAIOT-TC-56043"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_15_01_Edit_Nat_Policy(self):
        logger.info(" {} ".center(20, '-').format('Edit Nat policy'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt5['name']}
        opt['translated_source'] = {'original':True}
        opt['translated_destination'] = {'group':'lanpc_group'}
        opt['inbound'] = 'X1'
        opt['outbound'] = 'any'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add Nat policy failed")

    @repeat_method(3)
    def test_15_02_Check_Ping_Traffic(self):
        logger.info(" {} ".center(20, '-').format('Check Ping traffic  '))
        cmd = f'ping -I eth1 {x1ao_fqdn} -c 30'
        cmd_get = 'ping -I eth1 x1ao.fqdn.com -c 5|grep "PING x1ao.fqdn.com"|awk -F\( "{print \$2}"| awk -F\) "{print \$1}"'
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            logger.info("send the command {}".format(cmd_get))
            out1 = PC2.send_command(cmd)
            out2 = PC5.send_command(cmd)
            if '100% packet loss' not in str(out1) and '100% packet loss' not in str(out2):
                logger.info('Ping Successful ')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        ip_pc2 = PC2.send_command(cmd_get)
        ip_pc5 = PC5.send_command(cmd_get)
        logger.info(f'-***-----***---,ip_pc2:{ip_pc2},ip_pc5:{ip_pc5}')
        if ip_pc5 != ip_pc2:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: Check Ping traffic  failed") 

    def test_15_03_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']={'any':True}
        opt['destination']={'name':opt2['name']}
        opt['translated_source'] = {"name":"X1 IP"}
        opt['translated_destination'] = {'original': True}
        opt['inbound'] = 'any'
        opt['outbound'] = 'X1'
        del opt['reflexive']
        rc = natPolicyObj.edit_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")


class Test_Tear_down(Test):
    uuid = 'NonTC'
    description = "clear env config settings"

    def test_01_01_restore_dns_server(self):
        logger.info(" {} ".center(20, '-').format('restore dns server'))
        PC1.send_command(f'echo "nameserver 10.190.202.200" > /etc/resolv.conf')
        PC1.send_command(f'echo "nameserver 10.50.56.148" >> /etc/resolv.conf')
        out = PC1.send_command('cat /etc/resolv.conf')
        if '10.50.56.148' in str(out):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Remove Route Policy Failed.')