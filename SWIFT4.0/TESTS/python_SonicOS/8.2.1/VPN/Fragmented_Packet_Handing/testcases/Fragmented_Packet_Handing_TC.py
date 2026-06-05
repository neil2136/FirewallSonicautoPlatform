from definition.settings import *


class TestAdd_VPN_Policy_00(Test):
    uuid = "NonTC"
    description = "add vpn policy"

    def test_00_01_Add_DUT_AddObj(self):
        logger.info('-' * 10 + 'Add AO for DUT' + '-' * 10)
        rc1 = LAddrOBJ.config_addressobject(**local_r)
        logger.info('-' * 10 + 'Add AO for rm DUT' + '-' * 10)
        rc2 = RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc1 & rc2, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_02_add_vpn_policy(self):
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**Lvpn)
        if not rc1:
            logger.info('Add Local VPN failed')
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**Rvpn)
        if not rc2:
            logger.info('Add Remote VPN failed')
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_00_03_initiate_continuous_pings_from_local_to_remote(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = os.popen("ping {} -c 1".format(RemoteHost_IP)).read()
            if ('100% packet loss' not in str(out)):
                logger.info('Successfully initiated continuous traffic from local to remote.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")


class TestFragmented_Packet_Handling_01(Test):
    uuid = "SOSAIOT-TC-57636"
    description = show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_set_X1_MTU(self):
        x1_opt = {
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
            'mtu': 1500,
        }
        rc = interface.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, "ERR: Config X1 MTU failed")

    def test_01_02_enable_Fragmentation_and_Ignore_DF(self):
        Adv_option = {
            'frag_packets': False,
            'ignore_df_bit': False,
        }
        rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
        Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

    def test_01_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping {} -l 2000 -c 1".format(LocalHost_IP))
            if ('100% packet loss' not in str(out)):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")

    def test_01_04_enable_Fragmentation_and_Ignore_DF(self):
        Adv_option = {
            'frag_packets': True,
            'ignore_df_bit': False,
        }
        rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
        Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

    def test_01_05_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping {} -l 2000 -c 1".format(LocalHost_IP))
            if ('100% packet loss' not in str(out)):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")


class TestFragmented_Packet_Handling_10(Test):
    uuid = "SOSAIOT-TC-57637"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_set_X1_MTU(self):
        x1_opt = {
            'if'     : 'X1',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.WANIP,
            'mask'   : '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1'   : Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
            'fragment_packets': True,
            'mtu': 1200,
        }
        rc = interface.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, "ERR: Config X1 MTU failed")

    def test_10_02_enable_Fragmentation_and_Ignore_DF(self):
        Adv_option = {
            'frag_packets': True,
            'ignore_df_bit': True,
        }
        rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
        Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

    def test_10_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping {} -l 1300 -c 1 -f".format(LocalHost_IP))
            if ('100% packet loss' not in str(out)):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")


class TestFragmented_Packet_Handling_11(Test):
    uuid = "SOSAIOT-TC-57638"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_01_set_X1_MTU(self):
        x1_opt = {
            'if'     : 'X1',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.WANIP,
            'mask'   : '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1'   : Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
            'fragment_packets': True,
            'mtu': 1200,
        }
        rc = interface.config_interface(**x1_opt)
        Assertion.assert_equal(rc, True, "ERR: Config X1 MTU failed")

    def test_11_02_enable_Fragmentation_and_Ignore_DF(self):
        Adv_option = {
            'frag_packets': True,
            'ignore_df_bit': True,
        }
        rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
        Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

    def test_11_03_initiate_continuous_pings_from_remote_to_local(self):
        logger.info(" {} ".center(20, '-').format('Initiate pings'))
        for i in range(10):
            out = PC2_login.send_command("ping {} -l 1400 -c 1".format(LocalHost_IP))
            if ('100% packet loss' not in str(out)):
                logger.info('Successfully initiated continuous traffic from remote to local NAT.')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                logger.info(out)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Ping failed")


# class TestFragmented_Packet_Handling_15(Test):
#     uuid = "1522273"
#     description = show_testcase_info(TESTPLAN, '15', description=True)['title']

#     def test_15_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '15')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_15_01_set_X1_MTU(self):
#         x1_opt = {
#             'if'     : 'X1',
#             'zone'   : 'WAN',
#             'mode'   : 'static',
#             'ip'     : Parameter.WANIP,
#             'mask'   : '255.255.255.0',
#             'gateway': Parameter.WANGW,
#             'dns1'   : Parameter.DNSSERVER,
#             'mgmt_https': True,
#             'mgmt_ssh'  : True,
#             'mgmt_ping' : True,
#             'fragment_packets': True,
#             'mtu': 1200,
#         }
#         rc = interface.config_interface(**x1_opt)
#         Assertion.assert_equal(rc, True, "ERR: Config X1 MTU failed")

#     def test_15_02_enable_Fragmentation_and_Ignore_DF(self):
#         Adv_option = {
#             'frag_packets': True,
#             'ignore_df_bit': False,
#         }
#         rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
#         Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

#     def test_15_03_initiate_continuous_pings_from_remote_to_local(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))
#         for i in range(10):
#             out = PC2_login.send_command("ping {} -l 400 -c 1 -f".format(LocalHost_IP))
#             if ('100% packet loss' not in str(out)):
#                 logger.info('Successfully initiated continuous traffic from remote to local NAT.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 logger.info(out)
#                 rc = False
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")


# class TestFragmented_Packet_Handling_18(Test):
#     uuid = "1522276"
#     description = show_testcase_info(TESTPLAN, '18', description=True)['title']

#     def test_18_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '18')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_18_01_set_X1_MTU(self):
#         x1_opt = {
#             'if'     : 'X1',
#             'zone'   : 'WAN',
#             'mode'   : 'static',
#             'ip'     : Parameter.WANIP,
#             'mask'   : '255.255.255.0',
#             'gateway': Parameter.WANGW,
#             'dns1'   : Parameter.DNSSERVER,
#             'mgmt_https': True,
#             'mgmt_ssh'  : True,
#             'mgmt_ping' : True,
#             'fragment_packets': True,
#             'mtu': 1200,
#         }
#         rc = interface.config_interface(**x1_opt)
#         Assertion.assert_equal(rc, True, "ERR: Config X1 MTU failed")

#     def test_18_02_enable_Fragmentation_and_Ignore_DF(self):
#         Adv_option = {
#             'frag_packets': False,
#             'ignore_df_bit': False,
#         }
#         rc = VPN_Adv_obj.config_vpnadvanced(**Adv_option)
#         Assertion.assert_equal(rc, True, "ERR: enable Fragmentation and Ignore DF failed")

#     def test_18_03_initiate_continuous_pings_from_remote_to_local(self):
#         logger.info(" {} ".center(20, '-').format('Initiate pings'))
#         for i in range(10):
#             out = PC2_login.send_command("ping {} -l 400 -c 1".format(LocalHost_IP))
#             if ('100% packet loss' not in str(out)):
#                 logger.info('Successfully initiated continuous traffic from remote to local NAT.')
#                 rc = True
#                 break
#             elif i == 9:
#                 logger.info('Ping failed')
#                 logger.info(out)
#                 rc = False
#         Assertion.assert_equal(rc, True, "ERR: Ping failed")


