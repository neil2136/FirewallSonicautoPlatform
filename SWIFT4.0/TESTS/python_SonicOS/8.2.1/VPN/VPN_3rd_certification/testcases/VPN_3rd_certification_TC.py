from definition.settings import *
from bin import packet_monitor


class TestVPN_Cert_07(Test):
    uuid = "SOSAIOT-TC-54196"
    description= show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')
        
    def test_07_02_Delete_CA_Cert(self):
        rc = LCACertObj.delete_ca_cert(ca_hash="nfB5Erd0dz1GD5B6eXXkdQ==")
        Assertion.assert_equal(rc, True, 'Delete CA cert Failed.')


class TestVPN_Cert_10(Test):
    uuid = "SOSAIOT-TC-54164"
    description= show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_set_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2030:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'set DUT time expired Failed.')

    def test_10_02_Add_Exipred_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        resp = LCACertObj.import_ca_cert(file=ca_cert, msg=True)
        if not re.search('\"success\":false.*CA Certificate has expired',resp,re.M|re.I):
            logger.info(resp)
            rc = False
        else:
            rc = True
        Assertion.assert_equal(rc, True, 'test cannot add expired CA cert Failed.')

    def test_10_04_restore_time(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        date_tmp = os.popen('date +%Y:%m:%d').read()
        print(date_tmp)
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": date_tmp,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        logger.info(rc)
        Assertion.assert_equal(rc, True, 'restore DUT time Failed.')


class TestVPN_Cert_1(Test):
    uuid = "SOSAIOT-TC-54163"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_1_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_1_01_Add_Local_Cert(self):
        logger.info('-'*10+'generate signing request'+'-'*10)
        if not os.path.isdir('/tmp/logs/'):
            logger.error("no path /tmp/logs not exists, create it now")
            os.system("mkdir /tmp/logs")
        rc = LCACertObj.generate_req(**signreq)
        rc &= LCACertObj.export_req(filename='my_cert', filepath='/tmp/logs/my_cert.p10')
        rc &= Gen_Local_Cert.gen_local_cert(sign_req='my_cert', sub=False)
        rc &= LCACertObj.import_req_cert(req_cert='my_cert', signed_cert='/tmp/logs/01.pem')
        logger.info('-'*10+'generate signing request rc is {}'.format(rc))
        show_cmds = ['show certificates status imported']
        (rc1, output) = fw_cli.do_cli_commands(show_cmds, 1)
        logger.info(f'show cert: {output}')
        if re.search('my_cert\s+Local certificate', str(output)):
            rc1 &= True
        else:
            rc1 &= False
        Assertion.assert_equal(rc1, True, 'add local cert Failed.')

    def test_1_02_Delete_Local_Cert(self):
        logger.info('-'*10+'delete local cert'+'-'*10)
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'delete local cert Failed.')


class TestVPN_Cert_15(Test):
    uuid = "SOSAIOT-TC-54169"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_15_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_15_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_15_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_15_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_15_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_16(Test):
    uuid = "SOSAIOT-TC-54170"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_16_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_16_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_16_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_16_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_16_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_16_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_17(Test):
    uuid = "SOSAIOT-TC-54171"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_17_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_17_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ipsec_lifetime'] = '18800'
        ref2['ipsec_lifetime'] = '18800'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_17_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_17_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_17_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_18(Test):
    uuid = "SOSAIOT-TC-54172"
    description= show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_18_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_18_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_18_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        ref1['ipsec_lifetime'] = '18800'
        ref2['ipsec_lifetime'] = '18800'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_18_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_18_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_18_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_19(Test):
    uuid = "SOSAIOT-TC-54173"
    description= show_testcase_info(TESTPLAN, '19', description=True)['title']

    def test_19_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_19_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_19_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_lifetime'] = '18800'
        ref2['ike_lifetime'] = '18800'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_19_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_19_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_19_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_20(Test):
    uuid = "SOSAIOT-TC-54175"
    description= show_testcase_info(TESTPLAN, '20', description=True)['title']

    def test_20_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_20_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_20_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        ref1['ike_lifetime'] = '18800'
        ref2['ike_lifetime'] = '18800'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_20_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_20_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_20_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_21(Test):
    uuid = "SOSAIOT-TC-54176"
    description= show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_21_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_21_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_21_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ipsec_pfs'] = True
        ref2['ipsec_pfs'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_21_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_21_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_21_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_22(Test):
    uuid = "SOSAIOT-TC-54177"
    description= show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_22_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_22_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_22_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        ref1['ipsec_pfs'] = True
        ref2['ipsec_pfs'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_22_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    @repeat_method(3)
    def test_22_04_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_22_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_33(Test):
    uuid = "SOSAIOT-TC-54189"
    description= show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_33_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_33_01_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "00:00:00",
                "date": "2019:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        rc &= RTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    @repeat_method(3)
    def test_33_02_import_L2_Cert(self):
        logger.info('-'*10+'Add Level 2 CA cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + l2_cert, name='l2_cert', password='test1234')
        rc &= RCACertObj.import_cert_local(cert_path='@' + l2_cert, name='l2_cert', password='test1234')
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')


class TestVPN_Cert_34(Test):
    uuid = "SOSAIOT-TC-54190"
    description= show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_34_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_34_01_export_L2_Cert(self):
        logger.info('-'*10+'Add Level 2 CA cert'+'-'*10)
        resp = LCACertObj.export_cert_local(name='l2_cert', password='test1234')
        if re.search('HTTP\/1.0 200 OK', str(resp), re.I):
            rc = True
        else:
            rc = False
            logger.info(resp)
        Assertion.assert_equal(rc, True, 'export local cert Failed.')


class TestVPN_Cert_35_01(Test):
    uuid = "SOSAIOT-TC-54191"
    description= show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_35_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35', "ERR: show testcase info failed")

    def test_35_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_35_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_35_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_35_04_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_35_05_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_35_06_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_35_07_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_35_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn_TI_3rd)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn_TI_3rd)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_35_02(Test):
    uuid = "SOSAIOT-TC-54191"
    description= show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_35_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35', "ERR: show testcase info failed")

    def test_35_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_35_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_35_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_35_04_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_35_05_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_35_06_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_35_07_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_35_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn_TI_3rd)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn_TI_3rd)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_35_03(Test):
    uuid = "SOSAIOT-TC-54191"
    description= show_testcase_info(TESTPLAN, '35', description=True)['title']

    def test_35_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35', "ERR: show testcase info failed")

    def test_35_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_35_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['ike_exchange'] = 'aggressive'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_35_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_35_04_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_35_05_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_35_06_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_35_07_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_35_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn_TI_3rd)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn_TI_3rd)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_36_01(Test):
    uuid = "SOSAIOT-TC-54192"
    description= show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_36_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36', "ERR: show testcase info failed")

    def test_36_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_36_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['local_cert'] = 'l2_cert'
        ref1['local_ike_type'] = 'email-id'
        ref1['peer_ike_type'] = 'email_id'
        ref1['peer_ike_id'] = 'allen@allen.com'
        ref1['ike_exchange'] = 'aggressive'
        ref2['local_cert'] = 'l2_cert'
        ref2['local_ike_type'] = 'email-id'
        ref2['peer_ike_type'] = 'email_id'
        ref2['peer_ike_id'] = 'allen@allen.com'
        ref2['ike_exchange'] = 'aggressive'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_36_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_36_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_36_05_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_36_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_36_02(Test):
    uuid = "SOSAIOT-TC-54192"
    description= show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_36_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36', "ERR: show testcase info failed")

    def test_36_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_36_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['local_cert'] = 'l2_cert'
        ref1['local_ike_type'] = 'email-id'
        ref1['peer_ike_type'] = 'email_id'
        ref1['peer_ike_id'] = 'allen@allen.com'
        ref1['ike_exchange'] = 'main'
        ref2['local_cert'] = 'l2_cert'
        ref2['local_ike_type'] = 'email-id'
        ref2['peer_ike_type'] = 'email_id'
        ref2['peer_ike_id'] = 'allen@allen.com'
        ref2['ike_exchange'] = 'main'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_36_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_36_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_36_05_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_36_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')


class TestVPN_Cert_36_03(Test):
    uuid = "SOSAIOT-TC-54192"
    description= show_testcase_info(TESTPLAN, '36', description=True)['title']

    def test_36_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36', "ERR: show testcase info failed")

    def test_36_01_clear_log_and_start_packet_monitor(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        rc &= packet_monitor.start_packet_monitor()
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_36_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['local_cert'] = 'l2_cert'
        ref1['local_ike_type'] = 'email-id'
        ref1['peer_ike_type'] = 'email_id'
        ref1['peer_ike_id'] = 'allen@allen.com'
        ref1['ike_exchange'] = 'ikev2'
        ref2['local_cert'] = 'l2_cert'
        ref2['local_ike_type'] = 'email-id'
        ref2['peer_ike_type'] = 'email_id'
        ref2['peer_ike_id'] = 'allen@allen.com'
        ref2['ike_exchange'] = 'ikev2'
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2,True,'Add VPN Policy Failed.')

    def test_36_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(PC2_eth0)).read()
            if ('100% packet loss' not in out):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_36_04_check_captured_packet(self):
        rc = packet_monitor.check_captured_monitor()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    @repeat_method(3)
    def test_36_05_test_log(self):
        logger.info(" {} ".center(20, '-').format('Test log'))
        time.sleep(3)
        log = LogObj.export_log_txt(log_switch=False)
        if re.search('IKE(v2)?\s+negotiation\s+complete', log, re.I):
            rc = True
            logger.info('Test log passed.')
        else:
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_36_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1&rc2,True,'Remove VPN Policy Failed.')
