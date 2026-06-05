from definition.settings import *


class TestVPN_NAT_01(Test):
    uuid = "SOSAIOT-TC-54702"
    description= show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.config_addressobject(**remote_l)
        rc1 &= LAddrOBJ.config_addressobject(**local_Tran_l)
        rc1 &= LAddrOBJ.config_addressobject(**remote_Tran_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.config_addressobject(**remote_r)
        rc2 &= RAddrOBJ.config_addressobject(**local_Tran_r)
        rc2 &= RAddrOBJ.config_addressobject(**remote_Tran_r)
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')

    def test_01_02_Add_route_from_PC2_to_NAT(self):
        logger.info('-'*10+'Add NAT route'+'-'*10)
        cmd = "route add -net {} netmask {} gw {}".format(Parameter.LOCTRANSNET, Parameter.NETMASK, Parameter.REMOTEX0)
        PC2_login.send_command(cmd)
        rt_info = PC2_login.send_command("route -n")
        if re.search('9\.9\.9\.0.*172\.16\.1\.101', rt_info):
            rc = True
        else:
            rc = False
            logger.info(rt_info)
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')

    def test_01_03_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")
        
    def test_01_04_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**Lvpn)
        if not rc1:
            logger.info('Add Local VPN failed')
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**Rvpn)
        if not rc2:
            logger.info('Add Remote VPN failed')
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_01_05_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping 9.9.9.105 -c 1")
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_06_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(2)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKEv2\s+negotiation\s+completed', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_07_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        if not rc1:
            logger.info('Delete Local VPN failed')
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        if not rc2:
            logger.info('Delete Remote VPN failed')
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')

    def test_01_08_restore_route(self):
        logger.info('-'*10+'Add NAT route'+'-'*10)
        cmd = "service network restart"
        PC2_login.send_command(cmd)
        time.sleep(3)
        rt_info = PC2_login.send_command("route -n")
        if re.search('9\.9\.9\.0.*172\.16\.1\.101', rt_info):
            rc = False
            logger.info(rt_info)
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')

    def test_01_09_delete_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_l['name'],ip_type='ipv4')
        rc1 &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_Tran_l['name'],ip_type='ipv4')
        rc1 &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_Tran_l['name'],ip_type='ipv4')
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_r['name'],ip_type='ipv4')
        rc2 &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_Tran_r['name'],ip_type='ipv4')
        rc2 &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_Tran_r['name'],ip_type='ipv4')
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')

class TestVPN_NAT_04(Test):
    uuid = "SOSAIOT-TC-54703"
    description= show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.config_addressobject(**remote_l)
        rc1 &= LAddrOBJ.config_addressobject(**local_Tran_l)
        rc1 &= LAddrOBJ.config_addressobject(**remote_Tran_l)
        rc1 &= LAddrOBJ.config_addressobject(**new_zone_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.config_addressobject(**remote_r)
        rc2 &= RAddrOBJ.config_addressobject(**local_Tran_r)
        rc2 &= RAddrOBJ.config_addressobject(**remote_Tran_r)
        rc2 &= RAddrOBJ.config_addressobject(**new_zone_r)
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')

    def test_04_02_Add_group(self):
        logger.info('-'*10+'Add group for DUT vpn local network'+'-'*10)
        rc = LAddrGroupOBJ.add_addressgroup(**LocGroup_l)
        logger.info('-'*10+'Add group for DUT vpn NAT local network'+'-'*10)
        rc &= LAddrGroupOBJ.add_addressgroup(**LocTranGroup_l)
        logger.info('-'*10+'Add group for rm DUT vpn NAT remote network'+'-'*10)
        rc &= RAddrGroupOBJ.add_addressgroup(**RemTranGroup_r)
        Assertion.assert_equal(rc, True, 'Add group for DUT and RDUT Failed.')

    def test_04_03_Add_route_from_PC2_to_NAT(self):
        logger.info('-'*10+'Add NAT route'+'-'*10)
        cmd = "route add -net {} netmask {} gw {}".format(Parameter.LOCTRANSNET, Parameter.NETMASK, Parameter.REMOTEX0)
        PC2_login.send_command(cmd)
        rt_info = PC2_login.send_command("route -n")
        if re.search('9\.9\.9\.0.*172\.16\.1\.101', rt_info):
            rc = True
        else:
            rc = False
            logger.info(rt_info)
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')

    def test_04_04_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")
        
    def test_04_05_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**Lvpn_04)
        if not rc1:
            logger.info('Add Local VPN failed')
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**Rvpn_04)
        if not rc2:
            logger.info('Add Remote VPN failed')
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_04_06_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping 9.9.9.105 -c 1")
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_04_07_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(2)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKEv2\s+negotiation\s+completed', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn_04)
        if not rc1:
            logger.info('Delete Local VPN failed')
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn_04)
        if not rc2:
            logger.info('Delete Remote VPN failed')
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')
    
    def test_04_09_restore_route(self):
        logger.info('-'*10+'Add NAT route'+'-'*10)
        cmd = "service network restart"
        PC2_login.send_command(cmd)
        time.sleep(3)
        rt_info = PC2_login.send_command("route -n")
        if re.search('9\.9\.9\.0.*172\.16\.1\.101', rt_info):
            rc = False
            logger.info(rt_info)
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'Add NAT route Failed.')
    
    def test_04_10_delete_group(self):
        logger.info('-'*10+'delete DUT local group'+'-'*10)
        rc = LAddrGroupOBJ.del_addressgroup(LocGroup_l['address_groups'][0]['ipv4']['name'])
        logger.info('-'*10+'delete DUT NAT group'+'-'*10)
        rc &= LAddrGroupOBJ.del_addressgroup(LocTranGroup_l['address_groups'][0]['ipv4']['name'])
        logger.info('-'*10+'delete rm DUT NAT group'+'-'*10)
        rc &= RAddrGroupOBJ.del_addressgroup(RemTranGroup_r['address_groups'][0]['ipv4']['name'])
        Assertion.assert_equal(rc, True, 'delete group for DUT and RDUT Failed.')
    
    def test_04_11_delete_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc1 = LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_l['name'],ip_type='ipv4')
        rc1 &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_Tran_l['name'],ip_type='ipv4')
        rc1 &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_Tran_l['name'],ip_type='ipv4')
        rc1 &= LAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=new_zone_l['name'],ip_type='ipv4')
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc2 = RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_r['name'],ip_type='ipv4')
        rc2 &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=local_Tran_r['name'],ip_type='ipv4')
        rc2 &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=remote_Tran_r['name'],ip_type='ipv4')
        rc2 &= RAddrOBJ.delete_addressobject('network', object_path='name', object_name_uuid=new_zone_r['name'],ip_type='ipv4')
        Assertion.assert_equal(rc1&rc2, True, 'Add AO for DUT and RDUT Failed.')