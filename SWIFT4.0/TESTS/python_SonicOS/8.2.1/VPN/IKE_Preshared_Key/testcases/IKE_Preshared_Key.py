__author__ = 'CHU'
from definition.settings import *


class TestIkePresharedKeySmoke_01(Test):
    uuid = "NonTC"
    description= 'Config Environment 1'

    def test_01_00_config_network(self):
        logger.info(" {} ".center(20, '-').format('Config network'))
        PC3_login = Host(PC3_IP, user='root', password='password')
        if Params.openstack == "1":
            cmd_list = ["cp {}/vpntestbed.com.db /var/named/chroot/var/named/".format(VPN_bin),
                        "cp {}/named.conf /var/named/chroot/etc/".format(VPN_bin),
                        "service named restart"]
            ret = ''
            rc = False
            for cmd in cmd_list:
                logger.info(cmd)
                ret = PC3_login.send_command(cmd)
                logger.info(ret)
                time.sleep(1)
            if 'Starting named: [  OK  ]' in ret:
                logger.info('config DNS PASS')
                rc = True
            else:
                logger.info('config DNS FAIL')

            cmd = " service smb restart;service nmb restart "
            ret  = PC2_login.send_command(cmd)
            logger.info(ret)
            if 'Starting SMB services: [  OK  ]' in ret and 'Starting NMB services: [  OK  ]' in ret:
                logger.info('service smb and service nmb restart successfully.')
            else:
                rc = False
            Assertion.assert_equal(rc, True, 'config Network FAIL')
        else:
            logger.info(Params.openstack)
            logger.info('Maybe something is wrong...')

    def test_01_01_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Prepare Environment 1'))
        rc = 0
        rc1 = LAddrOBJ.config_addressobject(msg=True, **LObj1)
        if rc1[0]:
            rc += 1
            logger.info('Add {} address objects success.'.format(LObj1['name']))
        elif 'Already exists' in rc1[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Local Address Object already exists')
        else:
            logger.info('Add {} Failed'.format(LObj1['name']))

        rc2 = RAddrOBJ.config_addressobject(msg=True, **RObj1)
        if rc2[0]:
            rc += 1
            logger.info('Add {} address objects success.'.format(RObj1['name']))
        elif 'Already exists' in rc2[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Remote Address Object already exists')
        else:
            logger.info('Add {} Failed'.format(RObj1['name']))

        Assertion.assert_equal(rc,2,'Add address objects Failed.')


class TestIkePresharedKeySmoke_02(Test):
    uuid = "SOSAIOT-TC-54316"
    description= show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_02_add_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Add VPN Policy'))
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**Lvpn)
        if rc1:
            logger.info('Add Local VPN pass')
        else:
            logger.info('Add Local VPN failed')

        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**Rvpn)
        if rc2:
            logger.info('Add Remote VPN pass')
        else:
            logger.info('Add Remote VPN failed')
        rc = rc1 and rc2
        Assertion.assert_equal(rc,True,'Add VPN Policy Failed.')

    def test_02_03_initiate_continuous_pings_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        logger.info(PC2)
        rc = False
        for i in range(5):
            out = os.popen('ping {} -c 2'.format(PC2)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from local to remote vpn.')
                rc = True
                break
            elif i == 4:
                logger.info('Ping failed')
                rc = False
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_04_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_02_05_sleep_for_SA_expired(self):
        logger.info(" {} ".center(20, '-').format('Sleep for SA expired'))
        time.sleep(270)
        Assertion.assert_equal(True, True, "ERR: Sleep for SA expired failed")

    def test_02_06_start_pinging_again_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Start pinging again'))
        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(PC2)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from local to remote vpn.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_02_07_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(5)
        log = LogObj.export_log_txt(log_switch=False)

        if 'IKE negotiation complete' in log:
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(" {} ".center(20, '-').format('Log mismatch'))
            logger.info(log)
            logger.info('-' * 34)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_02_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        if rc1:
            logger.info('Delete Local VPN pass')
        else:
            logger.info('Delete Local VPN failed')
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        if rc2:
            logger.info('Delete Remote VPN pass')
        else:
            logger.info('Delete Remote VPN failed')
        rc = rc1 and rc2
        Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')


# duplicate with IKE_Preshared_Keys_TP30
# class TestIkePresharedKeySmoke_03(Test):
#     uuid = "1529909"
#     description = show_testcase_info(TESTPLAN, '25', description=True)['title']

#     def test_03_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '25')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_03_01_clear_log(self):
#         logger.info(" {} ".center(20, '-').format('Clear log'))
#         rc = False
#         ret = LogObj.clear_log()
#         if ret == None:
#             rc = True
#             logger.info('Clear log success!')
#         Assertion.assert_equal(rc, True, "ERR: Clear log failed")

#     def test_03_02_add_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Add VPN Policy'))
#         ref1 = copy.deepcopy(Lvpn)
#         ref2 = copy.deepcopy(Rvpn)
#         ref1['ike_exchange'] = 'aggressive'
#         ref2['ike_exchange'] = 'aggressive'

#         logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
#         rc1 = Lvpn_obj.add_vpn_policy(**ref1)
#         if rc1:
#             logger.info('Add Local VPN pass')
#         else:
#             logger.info('Add Local VPN failed')

#         logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
#         rc2 = Rvpn_obj.add_vpn_policy(**ref2)
#         if rc2:
#             logger.info('Add Remote VPN pass')
#         else:
#             logger.info('Add Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Add VPN Policy Failed.')

#     def test_03_03_initiate_continuous_pings_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))

#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' not in out):
#                 logger.info('Successfully initiated continuous traffic from local to remote vpn.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")

#     def test_03_04_clear_log(self):
#         logger.info(" {} ".center(20, '-').format('Clear log'))
#         rc = False
#         ret = LogObj.clear_log()
#         if ret == None:
#             rc = True
#             logger.info('Clear log success!')
#         Assertion.assert_equal(rc, True, "ERR: Clear log failed")

#     def test_03_05_renegotiate(self):
#         logger.info(" {} ".center(20, '-').format('Renegotiate'))
#         rc = Lvpn_obj.Renegotiate_VPN_Tunnel(**vpn_raw)
#         Assertion.assert_equal(rc, True, "ERR: Renegotiate local DUT failed.")

#     def test_03_06_start_pinging_again_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Start pinging again'))
#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' not in out):
#                 logger.info('Successfully initiated continuous traffic from local to remote vpn.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")

#     def test_03_07_test_log(self):
#         logger.info(" {} ".center(20, '-').format('Test log'))
#         time.sleep(5)
#         log = LogObj.export_log_txt()

#         if 'IKE negotiation complete' in log:
#             rc = True
#             logger.info('Test log passed.')
#         else:
#             logger.info(" {} ".center(20, '-').format('Log mismatch'))
#             logger.info(log)
#             logger.info('-' * 34)
#             rc = False
#         if 'Tunnel Up' in log:
#             logger.info('Tunnel Up')
#         if 'IPsec Tunnel status changed' in log:
#             logger.info('IPsec Tunnel status changed')
#         Assertion.assert_equal(rc, True, "ERR: Test log failed")

#     def test_03_08_remove_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
#         rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
#         if rc1:
#             logger.info('Delete Local VPN pass')
#         else:
#             logger.info('Delete Local VPN failed')
#         rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
#         if rc2:
#             logger.info('Delete Remote VPN pass')
#         else:
#             logger.info('Delete Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')


# duplicate with IKE_Preshared_Keys_TP30
# class TestIkePresharedKeySmoke_04(Test):
#     uuid = "1529922"
#     description = show_testcase_info(TESTPLAN, '48', description=True)['title']

#     def test_04_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '48')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_04_01_clear_log(self):
#         logger.info(" {} ".center(20, '-').format('Clear log'))
#         rc = False
#         ret = LogObj.clear_log()
#         if ret == None:
#             rc = True
#             logger.info('Clear log success!')
#         Assertion.assert_equal(rc, True, "ERR: Clear log failed")

#     def test_04_02_add_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Add VPN Policy'))
#         ref1 = copy.deepcopy(Lvpn)
#         ref2 = copy.deepcopy(Rvpn)

#         logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
#         rc1 = Lvpn_obj.add_vpn_policy(**ref1)
#         if rc1:
#             logger.info('Add Local VPN pass')
#         else:
#             logger.info('Add Local VPN failed')

#         logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
#         rc2 = Rvpn_obj.add_vpn_policy(**ref2)
#         if rc2:
#             logger.info('Add Remote VPN pass')
#         else:
#             logger.info('Add Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Add VPN Policy Failed.')

#     def test_04_03_initiate_continuous_pings_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))

#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' not in out):
#                 logger.info('Successfully initiated continuous traffic from local to remote vpn.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")

#     def test_04_04_disable_vpn_on_local(self):
#         logger.info(" {} ".center(20, '-').format('Disable VPN On Local'))
#         ref = copy.deepcopy(Lvpn)
#         ref['enable'] = False
#         rc = Lvpn_obj.edit_vpn_policy(**ref)
#         if rc:
#             logger.info('Disable Local VPN pass')
#         else:
#             logger.info('Disable Local VPN failed')
#         time.sleep(5)
#         Assertion.assert_equal(rc, True, "ERR: Disable vpn failed")

#     def test_04_05_start_pinging_again_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Start pinging again'))
#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' in out):
#                 logger.info('Ping failed, disable vpn successfully.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping success, disable vpn failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping success, disable vpn failed")

#     def test_04_06_clear_log(self):
#         logger.info(" {} ".center(20, '-').format('Clear log'))
#         rc = False
#         ret = LogObj.clear_log()
#         if ret == None:
#             rc = True
#             logger.info('Clear log success!')
#         Assertion.assert_equal(rc, True, "ERR: Clear log failed")

#     def test_04_07_re_enable_vpn_on_local(self):
#         logger.info(" {} ".center(20, '-').format('Re-enable VPN on local'))
#         ref = copy.deepcopy(Lvpn)
#         ref['enable'] = True
#         rc = Lvpn_obj.edit_vpn_policy(**ref)
#         if rc:
#             logger.info('Re-enable Local VPN pass')
#         else:
#             logger.info('Re-enable Local VPN failed')
#         time.sleep(5)
#         Assertion.assert_equal(rc, True, "ERR: Re-enable vpn failed")

#     def test_04_08_start_pinging_again_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Start pinging again'))
#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' not in out):
#                 logger.info('Successfully initiated continuous traffic from local to remote vpn.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")

#     def test_04_09_test_log(self):
#         logger.info(" {} ".center(20, '-').format('Test log'))
#         time.sleep(5)
#         log = LogObj.export_log_txt(log_switch=False)

#         if 'IKE negotiation complete' in log:
#             rc = True
#             logger.info('Test log passed.')
#         else:
#             logger.info(" {} ".center(20, '-').format('Log mismatch'))
#             logger.info(log)
#             logger.info('-' * 34)
#             rc = False
#         Assertion.assert_equal(rc, True, "ERR: Test log failed")

#     def test_04_10_remove_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
#         rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
#         if rc1:
#             logger.info('Delete Local VPN pass')
#         else:
#             logger.info('Delete Local VPN failed')
#         rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
#         if rc2:
#             logger.info('Delete Remote VPN pass')
#         else:
#             logger.info('Delete Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')


class TestIkePresharedKeySmoke_05(Test):
    uuid = "NonTC"
    description= 'Clear Environment 1'

    def test_05_00_delete_address_object(self):
        logger.info(" {} ".center(20, '-').format('Clear Environment 1'))
        rc = LAddrOBJ.delete_addressobject(object_type="network", object_path="name",
                                           object_name_uuid="remote_net", ip_type="ipv4")
        if rc:
            logger.info('Delete {} address objects success.'.format(LObj1['name']))
        else:
            logger.info('Delete {} Failed'.format(LObj1['name']))

        ret = RAddrOBJ.delete_addressobject(object_type="network", object_path="name",
                                           object_name_uuid="local_net", ip_type="ipv4")
        if ret:
            logger.info('Delete {} address objects success.'.format(RObj1['name']))
        else:
            logger.info('Delete {} Failed'.format(RObj1['name']))
        rc = rc and ret
        Assertion.assert_equal(rc, True, 'Delete address objects Failed.')


class TestIkePresharedKeySmoke_06(Test):
    uuid = "NonTC"
    description= 'Config Environment 3'

    def test_06_00_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Prepare Environment 3'))
        rc = 0
        for item in LaddrList:
            logger.info("rc={}".format(rc))
            logger.info(item)
            rc1 = LAddrOBJ.config_addressobject(msg=True, **item)
            if rc1[0]:
                rc += 1
                logger.info('Add {} address objects success.'.format(item['name']))
            elif 'Already exists' in rc1[1]['status']['info'][0]['message']:
                rc += 1
                logger.info('Address Object already exists')
            else:
                logger.info('Add {} Failed'.format(item['name']))
        if rc==6:
            logger.info('Add address object on local DUT passed.')
        else:
            logger.info('Add address object on local DUT failed.')
        for item in RaddrList:
            logger.info("rc={}".format(rc))
            logger.info(item)
            rc2 = RAddrOBJ.config_addressobject(msg=True, **item)
            if rc2[0]:
                rc += 1
                logger.info('Add {} address objects success.'.format(item['name']))
            elif 'Already exists' in rc2[1]['status']['info'][0]['message']:
                rc += 1
                logger.info('Address Object already exists')
            else:
                logger.info('Add {} Failed'.format(item['name']))
        if rc==12:
            logger.info('Add address object on remote DUT passed.')
        else:
            logger.info('Add address object on local DUT failed.')
        Assertion.assert_equal(rc,12,'Add address objects Failed.')


# duplicate with IKE_Preshared_Keys_TP30
# class TestIkePresharedKeySmoke_07(Test):
#     uuid = "1529920"
#     description = show_testcase_info(TESTPLAN, '45', description=True)['title']

#     def test_07_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '45')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_07_01_clear_log(self):
#         logger.info(" {} ".center(20, '-').format('Clear log'))
#         rc = False
#         ret = LogObj.clear_log()
#         if ret == None:
#             rc = True
#             logger.info('Clear log success!')
#         Assertion.assert_equal(rc, True, "ERR: Clear log failed")

#     def test_07_02_add_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Add VPN Policy'))
#         ref1 = copy.deepcopy(Lvpn)
#         ref2 = copy.deepcopy(Rvpn)

#         ref1['local_net_name']  = 'local_net'
#         ref1['remote_net_name'] = 'remote_net'
#         ref2['local_network']   = 'remote_net'
#         ref2['remote_network']  = 'local_net'

#         logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
#         rc1 = Lvpn_obj.add_vpn_policy(**ref1)
#         if rc1:
#             logger.info('Add Local VPN pass')
#         else:
#             logger.info('Add Local VPN failed')

#         time.sleep(5)
#         logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
#         rc2 = False
#         for i in range(3):
#             rc2 = Rvpn_obj.add_vpn_policy(**ref2)
#             if rc2:
#                 break
#             time.sleep(5)
#             logger.info('Try Try add remote VPN again...')
#         if rc2:
#             logger.info('Add Remote VPN pass')
#         else:
#             logger.info('Add Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Add VPN Policy Failed.')

#     def test_07_03_initiate_continuous_pings_from_local_nonVPN_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))
#         logger.info('Initiate continuous pings from local nonVPN host to remote host.')

#         PC4_login = Host(PC4_IP, user='root', password='password')
#         out = PC4_login.send_command('ping {} -c 10'.format(PC2))
#         logger.info(out)
#         if ('100% packet loss' in str(out)):
#             logger.info('Ping failed.')
#             rc = True
#         else:
#             logger.info('Ping success.')
#             rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping success, nonVPN failed")

#     def test_07_04_initiate_continuous_pings_from_local_to_remote(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))
#         logger.info('Initiate continuous pings from local nonVPN host to remote host.')
#         rc = False
#         for i in range(10):
#             out = os.popen('ping {} -c 2'.format(PC2)).read()
#             logger.info(out)
#             if ('100% packet loss' not in out):
#                 logger.info('Successfully initiated continuous traffic from local to remote vpn.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 rc = False
#         logger.info(rc)
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")

#     def test_07_05_test_log(self):
#         logger.info(" {} ".center(20, '-').format('Test log'))
#         time.sleep(5)
#         log = LogObj.export_log_txt(log_switch=False)

#         if 'IKE negotiation complete' in log:
#             rc = True
#             logger.info('Test log passed.')
#         else:
#             logger.info(" {} ".center(20, '-').format('Log mismatch'))
#             logger.info(log)
#             logger.info('-' * 34)
#             rc = False
#         Assertion.assert_equal(rc, True, "ERR: Test log failed")

#     def test_07_06_remove_vpn_policy(self):
#         logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
#         rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
#         if rc1:
#             logger.info('Delete Local VPN pass')
#         else:
#             logger.info('Delete Local VPN failed')
#         rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
#         if rc2:
#             logger.info('Delete Remote VPN pass')
#         else:
#             logger.info('Delete Remote VPN failed')
#         rc = rc1 and rc2
#         Assertion.assert_equal(rc,True,'Remove VPN Policy Failed.')


class TestIkePresharedKeySmoke_08(Test):
    uuid = "NonTC"
    description= 'Clear Environment 3'

    def test_08_00_delete_address_object(self):
        logger.info(" {} ".center(20, '-').format('Clear Environment 3'))
        rc1 = False
        rc2 = False
        for item in LaddrList:
            rc1 = LAddrOBJ.delete_addressobject(object_type=item['object_type'], object_path="name",
                                               object_name_uuid=item['name'], ip_type="ipv4")
            if rc1:
                logger.info('Delete {} address objects success.'.format(item['name']))
            else:
                logger.info('Delete {} Failed'.format(item['name']))
        for item in RaddrList:
            rc2 = RAddrOBJ.delete_addressobject(object_type=item['object_type'], object_path="name",
                                               object_name_uuid=item['name'], ip_type="ipv4")
            if rc2:
                logger.info('Delete {} address objects success.'.format(item['name']))
            else:
                logger.info('Delete {} Failed'.format(item['name']))
        rc = rc1 and rc2
        Assertion.assert_equal(rc, True, 'Delete address objects Failed.')
