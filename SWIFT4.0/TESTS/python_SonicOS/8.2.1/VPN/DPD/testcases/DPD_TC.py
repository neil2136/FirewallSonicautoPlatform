from definition.settings import *
from bin import check_traffic
from bin import conf_pri_gw


class TestDPD_10(Test):
    uuid = "SOSAIOT-TC-54234"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_conf_dpd(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['dpd_interval'] = '3'
        ref['dpd_trigger'] = '3'
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_10_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_03_add_first_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_10_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_07_add_secondary_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_2)
        ref2 = copy.deepcopy(Rvpn_2)
        ref2['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_10_08_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_PC4_to_PC5()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_10_09_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_10_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_10_11_disable_remote_x1x2(self):
        logger.info('disable remote x1&x2 port')
        rc = conf_pri_gw.disable_device_port('X1')
        rc &= conf_pri_gw.disable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: disable remote x1x2 failed")

    def test_10_12_ping_from_local_to_remote_blocked(self):
        logger.info('ping traffic')
        rc = check_traffic.ping_traffic_blocked()
        rc &= check_traffic.ping_traffic2_blocked()
        Assertion.assert_equal(rc, True, "ERR: check Ping block failed")

    def test_10_13_test_log_with_enable_dpd(self):
        time.sleep(int(sleep_time))
        rc = check_traffic.check_test_log_with_enable_dpd()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_14_enable_remote_x1x2(self):
        logger.info('enable remote x1 port')
        rc = conf_pri_gw.enable_device_port('X1')
        rc &= conf_pri_gw.enable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: enable remote x1x2 failed")

    def test_10_15_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_10_16_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc1 &= Lvpn_obj.del_s2svpn_policy(**Lvpn_2)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        rc2 &= Rvpn_obj.del_s2svpn_policy(**Rvpn_2)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

    def test_10_17_disable_dpd(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Dis_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**Dis_dpd)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')


class TestDPD_11(Test):
    uuid = "SOSAIOT-TC-54233"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_01_conf_dpd(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['dpd_interval'] = '3'
        ref['dpd_trigger'] = '3'
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_11_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_11_03_config_x1_interface(self):
        logger.info("config x1 interface... ")
        # x1 ip should be in a same network with PC3_eth0
        attr = PC3_eth0.split('.')
        attr[3] = str(int(attr[3]) + 1)
        ip_addr = '.'.join(attr)
        ## gateway
        attr[3] = '1'
        gateway = '.'.join(attr)
        logger.info(gateway)
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': ip_addr,
            'mask': '255.255.255.0',
            'gateway': gateway,
            'dns1': Params.G_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'fragment_packets': True,
        }
        rc = LintfaceObj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(3)
    def test_11_04_register_fw(self):
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_11_05_recover_x1_interface(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.WANIP,
            'mask': '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1': Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'fragment_packets': True,
        }
        rc = LintfaceObj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_11_06_add_first_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_11_07_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_08_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_09_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_11_10_add_secondary_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_2)
        ref2 = copy.deepcopy(Rvpn_2)
        ref2['keep_alive'] = True
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_11_11_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_PC4_to_PC5()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_11_12_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_13_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_11_14_disable_remote_x1x2(self):
        logger.info('disable remote x1&x2 port')
        rc = conf_pri_gw.disable_device_port('X1')
        rc &= conf_pri_gw.disable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: disable remote x1x2 failed")

    def test_11_15_ping_from_local_to_remote_blocked(self):
        logger.info('ping traffic')
        rc = check_traffic.ping_traffic_blocked()
        rc &= check_traffic.ping_traffic2_blocked()
        Assertion.assert_equal(rc, True, "ERR: check Ping block failed")

    def test_11_16_test_log_with_enable_dpd(self):
        time.sleep(int(sleep_time))
        rc = check_traffic.check_test_log_with_enable_dpd()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_17_enable_remote_x1x2(self):
        logger.info('enable remote x1 port')
        rc = conf_pri_gw.enable_device_port('X1')
        rc &= conf_pri_gw.enable_device_port('X2')
        Assertion.assert_equal(rc, True, "ERR: enable remote x1x2 failed")

    def test_11_18_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_11_19_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc1 &= Lvpn_obj.del_s2svpn_policy(**Lvpn_2)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        rc2 &= Rvpn_obj.del_s2svpn_policy(**Rvpn_2)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')

    def test_11_20_disable_dpd(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Dis_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**Dis_dpd)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')


class TestDPD_12(Test):
    uuid = "SOSAIOT-TC-54236"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_12_01_disable_dpd_idle(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['idle_dpd'] = False
        ref['idle_dpd_interval'] = '100'
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_12_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_12_03_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_12_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_12_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_12_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_12_07_disable_remote_x1_and_ping(self):
        logger.info('disable remote x1 port')
        rc = conf_pri_gw.disable_device_port('X1')
        logger.info('check ping from remote to dut is block')
        rc &= check_traffic.ping_traffic_blocked()
        Assertion.assert_equal(rc, True, "ERR: disable remote x1 failed")

    def test_12_08_test_log_with_disable_idle(self):
        time.sleep(220)
        log = str(LogObj.export_log_txt(log_switch=False))
        reg = re.search('NOTIFY: R_U_THERE', log, re.I|re.M)
        if reg:
            logger.info(reg.group())
            rc = True
        else:
            logger.info('Test log failed.')
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_12_09_recover_remote_x1(self):
        logger.info('enable remote x1 port')
        rc = conf_pri_gw.enable_device_port('X1')
        Assertion.assert_equal(rc, True, "ERR: recover remote x1 failed")

    def test_12_10_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestDPD_13(Test):
    uuid = "SOSAIOT-TC-54237"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_13_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_13_01_disable_dpd_idle(self):
        global sleep_time
        ref = copy.deepcopy(En_dpd)
        ref['idle_dpd'] = True
        ref['idle_dpd_interval'] = '100'
        sleep_time = int(ref['dpd_interval'])*int(ref['dpd_trigger'])+30
        rc = LAdv_obj.config_vpnadvanced(**ref)
        rc &= RAdv_obj.config_vpnadvanced(**ref)
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')

    def test_13_02_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_13_03_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_13_04_ping_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_13_05_test_log(self):
        time.sleep(90)
        rc = check_traffic.check_test_log()
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_13_06_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret == None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_13_07_test_log_to_verify(self):
        time.sleep(220)
        log = str(LogObj.export_log_txt(log_switch=False))
        reg = re.search('NOTIFY: R_U_THERE', log, re.I | re.M)
        if reg:
            logger.info(reg.group())
            rc = True
        else:
            logger.info('Test log failed.')
            logger.info(log)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_13_08_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        rc2 = Rvpn_obj.del_s2svpn_policy(**Rvpn)
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestDPD_07(Test):
    uuid = "SOSAIOT-TC-54240"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_disable_dpd_idle(self):
        rc = True
        ref = copy.deepcopy(En_dpd)
        interval_list = ['2', '121']
        for test_ivl in interval_list:
            ref['dpd_interval'] = test_ivl
            resp = LAdv_obj.config_vpnadvanced(msg=True, **ref)
            logger.info(resp)
            if re.search('Value or string length\({}\) out of bounds \(min = 3, max = 120\)'.format(test_ivl), str(resp)):
                rc = True
            else:
                rc = False
                logger.info(resp)
            rc &= rc
        Assertion.assert_equal(rc, True, 'Config DPD Failed.')


class TestDPD_08(Test):
    uuid = "SOSAIOT-TC-54241"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_08_01_disable_dpd_idle(self):
        rc = True
        ref = copy.deepcopy(En_dpd)
        trigger_list = ['2', '11']
        for test_tri in trigger_list:
            ref['dpd_trigger'] = test_tri
            resp = LAdv_obj.config_vpnadvanced(msg=True, **ref)
            logger.info(resp)
            if re.search('Value or string length\({}\) out of bounds \(min = 3, max = 10\)'.format(test_tri), str(resp)):
                rc = True
            else:
                rc = False
                logger.info(resp)
            rc &= rc
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')


class TestDPD_14(Test):
    uuid = "SOSAIOT-TC-54238"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_14_01_disable_dpd_idle(self):
        rc = True
        ref = copy.deepcopy(En_dpd)
        idle_ivl_list = ['59', '3601', '9999']
        for test_idle_ivl in idle_ivl_list:
            ref['idle_dpd_interval'] = test_idle_ivl
            resp = LAdv_obj.config_vpnadvanced(msg=True, **ref)
            logger.info(resp)
            if re.search('Value or string length\({}\) out of bounds \(min = 60, max = 3600\)'.format(test_idle_ivl), str(resp)):
                rc = True
            else:
                rc = False
                logger.info(resp)
            rc &= rc
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')
