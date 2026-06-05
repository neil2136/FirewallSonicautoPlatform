from definition.settings import *


@paramunittest.parametrized(
    {'ike_exchange': 'main', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': True, 'uuid': '1705082', 'tcid': '10'},
    {'ike_exchange': 'main', 'ike_dh_group': '20', 'ipsec_encryption': 'aes_192', 'ipsec_pfs_dhgroup': 20, \
         'test_log': False, 'uuid': '1705082', 'tcid': '10'},
    {'ike_exchange': 'main', 'ike_dh_group': '21', 'ipsec_encryption': 'aes_256', 'ipsec_pfs_dhgroup': 21, \
         'test_log': False, 'uuid': '1705082', 'tcid': '10'},
    {'ike_exchange': 'main', 'ike_dh_group': '25', 'ipsec_encryption': 'aes_gcm16_128', 'ipsec_pfs_dhgroup': 25, \
         'test_log': False, 'uuid': '1705082', 'tcid': '10'},
    {'ike_exchange': 'main', 'ike_dh_group': '26', 'ipsec_encryption': 'aes_gcm16_192', 'ipsec_pfs_dhgroup': 26, \
         'test_log': False, 'uuid': '1705082', 'tcid': '10'},

    {'ike_exchange': 'aggressive', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': True, 'uuid': '1705084', 'tcid': '12'},
    {'ike_exchange': 'aggressive', 'ike_dh_group': '20', 'ipsec_encryption': 'aes_192', 'ipsec_pfs_dhgroup': 20, \
         'test_log': False, 'uuid': '1705084', 'tcid': '12'},
    {'ike_exchange': 'aggressive', 'ike_dh_group': '21', 'ipsec_encryption': 'aes_256', 'ipsec_pfs_dhgroup': 21, \
         'test_log': False, 'uuid': '1705084', 'tcid': '12'},
    {'ike_exchange': 'aggressive', 'ike_dh_group': '25', 'ipsec_encryption': 'aes_gcm16_128', 'ipsec_pfs_dhgroup': 25, \
         'test_log': False, 'uuid': '1705084', 'tcid': '12'},
    {'ike_exchange': 'aggressive', 'ike_dh_group': '26', 'ipsec_encryption': 'aes_gcm16_192', 'ipsec_pfs_dhgroup': 26, \
         'test_log': False, 'uuid': '1705084', 'tcid': '12'},

    {'ike_exchange': 'ikev2', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': True, 'uuid': '1705086', 'tcid': '14'},
    {'ike_exchange': 'ikev2', 'ike_dh_group': '20', 'ipsec_encryption': 'aes_192', 'ipsec_pfs_dhgroup': 20, \
         'test_log': False, 'uuid': '1705086', 'tcid': '14'},
    {'ike_exchange': 'ikev2', 'ike_dh_group': '21', 'ipsec_encryption': 'aes_256', 'ipsec_pfs_dhgroup': 21, \
         'test_log': False, 'uuid': '1705086', 'tcid': '14'},
    {'ike_exchange': 'ikev2', 'ike_dh_group': '25', 'ipsec_encryption': 'aes_gcm16_128', 'ipsec_pfs_dhgroup': 25, \
         'test_log': False, 'uuid': '1705086', 'tcid': '14'},
    {'ike_exchange': 'ikev2', 'ike_dh_group': '26', 'ipsec_encryption': 'aes_gcm16_192', 'ipsec_pfs_dhgroup': 26, \
         'test_log': False, 'uuid': '1705086', 'tcid': '14'},

    {'ike_exchange': 'main', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': False, 'uuid': '1705087', 'tcid': '16'},
    {'ike_exchange': 'aggressive', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': False, 'uuid': '1705087', 'tcid': '16'},
    {'ike_exchange': 'ikev2', 'ike_dh_group': '19', 'ipsec_encryption': 'aes_128', 'ipsec_pfs_dhgroup': 19,\
         'test_log': False, 'uuid': '1705087', 'tcid': '16'},
 )
class TestSuiteB_VPN_Support_10_12_14_16(Test):
    def setParameters(self, ike_exchange, ike_dh_group, ipsec_encryption, ipsec_pfs_dhgroup, test_log, uuid, tcid):
        self.ike_exchange = ike_exchange
        self.ike_dh_group = ike_dh_group
        self.ipsec_encryption = ipsec_encryption
        self.ipsec_pfs_dhgroup = ipsec_pfs_dhgroup
        self.test_log = test_log
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_clear_log(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = LogObj.clear_log()
        if ret is None:
            rc = True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: Clear log failed")

    def test_01_02_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['ike_exchange'] = self.ike_exchange
        ref1['ike_dh_group'] = self.ike_dh_group
        ref1['ipsec_encryption'] = self.ipsec_encryption
        ref1['ipsec_pfs_dhgroup'] = self.ipsec_pfs_dhgroup
        ref2['ike_exchange'] = self.ike_exchange
        ref2['ike_dh_group'] = self.ike_dh_group
        ref2['ipsec_encryption'] = self.ipsec_encryption
        ref2['ipsec_pfs_dhgroup'] = self.ipsec_pfs_dhgroup
        if self.tcid == '16':
            ref1['ipsec_pfs'] = False
            ref2['ipsec_pfs'] = False
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1&rc2, True, 'Add VPN Policy Failed.')

    def test_01_03_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")

    def test_01_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        rc = False
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
    def test_01_04_test_log(self):
        if not self.test_log:
            pass
        else:
            logger.info(" {} ".center(20, '-').format('Test log'))
            time.sleep(5)
            log = str(LogObj.export_log_txt(log_switch=False))
            reg1 = r'VPN Policy: vpn1.*AES(_CBC)?-128.*256-Bit Random ECP Group'
            reg2 = r'VPN Policy: vpn1.*ESP.*AES(_CBC)?-128.*256-Bit Random ECP Group'
            if self.tcid == '16':
                reg2 = r'VPN Policy: vpn1.*ESP.*AES(_CBC)?-128'
            if re.search(reg1, log, re.I) and re.search(reg2, log, re.I):
                rc = True
                logger.info(reg1)
                logger.info(reg2)
                logger.info('Test log passed.')
            else:
                rc = False
                logger.info(log)
            Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_01_05_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_01_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc1 = Lvpn_obj.del_tunnelvpn_policy(**Lvpn_TI_3rd)
        rc2 = Rvpn_obj.del_tunnelvpn_policy(**Rvpn_TI_3rd)
        Assertion.assert_equal(rc1&rc2, True, 'Remove VPN Policy Failed.')
