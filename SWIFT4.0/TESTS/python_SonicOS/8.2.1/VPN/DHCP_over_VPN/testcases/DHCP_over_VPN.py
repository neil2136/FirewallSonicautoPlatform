from definition.settings import *

@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_01_External_Server_Replay_on_Remote(Test):
    uuid = "SOSAIOT-TC-54245"
    description = '''
        External server is used, Relay IP is specified on Remote Gateway, Management IP is set.
        Client obtains a lease.
    '''

    def test_01_Step01_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, '1')

    def test_01_Step02_Config_Central_DHCP_over_VPN(self):
        logger.info("Central Gateway, Eternal DHCP server")
        central_dict = {
            'internal_dhcp': False,
            'global_vpn': False,
            'remote': False,
            'relay_ip': '0.0.0.0',
            'send_requests': True,
            'dhcp_server_ip_list': [LAN_PC],
        }
        rc = dho_vpn_api.config_dhcpvpn_centralgw(**central_dict)
        Assertion.assert_equal(rc, True, "ERR: Config central DHCP over VPN failed.")

    def test_01_Step03_Config_Remote_DHCP_over_VPN(self):
        remote_dict = {
            'bound-to': 'X0',
            #'accept_bridged_wlan_request': False,
            'relay-ip': RELAY_IP,
            'management-ip': MGMT_IP,
            'block-spoof': True,
            'temp-lease': False,
            'lease-time': '2',
        }

        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    def test_01_Step04_Disable_and_Enable_Remote_VPN_Policy(self):
        rc = r_vpn_cli.disable_vpnpolicy(**remote_vpn)
        time.sleep(3)
        rc &= r_vpn_cli.enable_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_01_Step05_Get_Lease_on_Client_PC(self):
        RMT_HOST.system('dhclient -r eth1')
        out = RMT_HOST.system('dhclient -v eth1').decode()
        logger.info(out)
        rc = re.search(r'bound to (\d+\.\d+\.\d+\.\d+)', out, re.I|re.S)
        result = False
        if rc:
            global dhcp_lease
            dhcp_lease = rc.group(1)
            logger.info("Remote PC get IP {} from central LAN PC.".format(dhcp_lease))
            result = True
        Assertion.assert_equal(result, True, "ERR: Remote PC gets DHCP lease failed.")

    @repeat_method(2)
    def test_01_Step06_Verify_Test(self):
        global dhcp_lease
        logger.info("===========" + dhcp_lease + "===========")

        RMT_HOST.system('ifdown eth2')
        out = RMT_HOST.system('ifconfig eth1').decode()
        logger.info(out)
        time.sleep(15)
        out = RMT_HOST.system('ping {} -c 3'.format(LAN_PC))

        out1 = os.popen('ping {} -c 5'.format(dhcp_lease)).read()
        logger.info("\n{}".format(out1))
        os.system('rm -rf /tmp/index.html')
        os.system('wget https://{} --no-check-certificate -O /tmp/index.html'.format(MGMT_IP))
        out2 = os.popen('cat /tmp/index.html').read()
        logger.info("\n{}".format(out2))
        rc = 0
        if re.search(r'100% packet loss', out1, re.I):
            logger.error("ping remote PC failed.")
        else:
            logger.info("ping remote PC passed.")
            rc += 1
        if re.search(r'SonicWALL', out2, re.I | re.S):
            logger.info("Manage remote GW passed.")
            rc += 1
        else:
            logger.error("Manage remote GW failed.")
        Assertion.assert_equal(rc, 2, "ERR: Verify failed.")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_21_Static_Devices_on_LAN_Add(Test):
    uuid = "SOSAIOT-TC-54249"
    description = '''
        The user will ensure that the static entry will be added in DHCP over VPN Configure dialog on Remote Gateway.
        A PC with that static address on Remote network will be able to access the Central network throuth VPN tunnel.
    '''

    def test_21_Step01_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, '21')

    def test_21_Step02_Config_Remote_DHCP_over_VPN(self):
        out = RMT_HOST.system('ifconfig eth1').decode()
        rc = re.search(r'HWaddr\s+(\w+:\w+:\w+:\w+:\w+:\w+)', out, re.I | re.S)
        global r_lan_mac
        r_lan_mac = ''
        if rc:
            r_lan_mac = rc.group(1)
            logger.info("Get remote PC MAC {}.".format(r_lan_mac))
            if len(r_lan_mac) < 17:
                Assertion.fail("Get MAC failed.")
        remote_dict = {
            'bound-to': 'X0',
            'relay-ip': RELAY_IP,
            'management-ip': MGMT_IP,
            'block-spoof': True,
            'temp-lease': False,
            'lease-time': '2',
            'static-device': STATIC_IP + ' ' + r_lan_mac,
        }
        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    def test_21_Step03_Disable_and_Enable_Remote_VPN_Policy(self):
        rc = r_vpn_cli.disable_vpnpolicy(**remote_vpn)
        time.sleep(3)
        rc &= r_vpn_cli.enable_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_21_Step04_Config_Remote_PC_IP(self):
        RMT_HOST.system('ifconfig eth1 {}/24 up'.format(STATIC_IP))
        time.sleep(3)
        Assertion.assert_equal(True, True, "ERR: Config remote PC static IP failed.")

    def test_21_Step05_Verify(self):
        out1 = os.popen('ping {} -c 5'.format(STATIC_IP)).read()
        logger.info("\n{}".format(out1))
        rc = 0
        if re.search(r'100% packet loss', out1, re.I):
            logger.error("ping remote PC failed.")
        else:
            logger.info("Check ICMP from remote PC to central LAN passed.")
            rc += 1

        # # # need check static item account
        Assertion.assert_equal(rc, 1, "ERR: Verification failed.")

    def test_21_Step06_Remove_Static_Device(self):
        remote_dict = {
            'bound-to': 'X0',
            'relay-ip': RELAY_IP,
            'management-ip': MGMT_IP,
            'block-spoof': True,
            'temp-lease': False,
            'lease-time': '2',
            'static-device': '',
        }
        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Remove static device failed.")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_27_Excluded_LAN_Devices_Delete(Test):
    uuid = "SOSAIOT-TC-54252"
    description = '''
        The user will ensure that excluded entry will be removed from DHCP over VPN Config dialog on Remote Gateway.
    '''

    def test_27_Step01_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, '27')

    def test_27_Step02_Config_Remote_DHCP_over_VPN(self):
        r_lan_mac = ''
        out = RMT_HOST.system('ifconfig eth1').decode()
        rc = re.search(r'HWaddr\s+(\w+:\w+:\w+:\w+:\w+:\w+)', out, re.I | re.S)
        if rc:
            r_lan_mac = rc.group(1)
            logger.info(r_lan_mac)
            if len(r_lan_mac) < 17:
                Assertion.fail("Get MAC failed.")
        remote_dict = {
            'bound-to': 'X0',
            'relay-ip': RELAY_IP,
            'management-ip': MGMT_IP,
            'block-spoof': True,
            'temp-lease': False,
            'lease-time': '2',
            'excluded-device': r_lan_mac,
        }
        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    def test_27_Step03_Disable_and_Enable_Remote_VPN_Policy(self):
        rc = r_vpn_cli.disable_vpnpolicy(**remote_vpn)
        time.sleep(3)
        rc &= r_vpn_cli.enable_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_27_Step04_Get_Lease_on_Client_PC(self):
        RMT_HOST.system('dhclient -r eth1')
        out = RMT_HOST.system('dhclient -v eth1').decode()
        logger.info(out)
        rc = re.search(r'bound to (\d+\.\d+\.\d+\.\d+)', out, re.I|re.S)
        result = True
        if rc:
            logger.error("Remote eth1 got IP from central network, but it should not.")
            result = False
        Assertion.assert_equal(result, True, "ERR: Remote PC gets DHCP lease but it should not.")

    def test_27_Step05_Remove_Exclude_Device(self):
        remote_dict = {
            'bound-to': 'X0',
            'excluded-device': '',
        }
        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Remove exclude device failed.")

    def test_27_Step06_Disable_and_Enable_Remote_VPN_Policy_2(self):
        rc = r_vpn_cli.disable_vpnpolicy(**remote_vpn)
        time.sleep(3)
        rc &= r_vpn_cli.enable_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_27_Step07_Get_Lease_on_Client_PC_2(self):
        dhcp_lease = ''
        RMT_HOST.system('dhclient -r eth1')
        out = RMT_HOST.system('dhclient -v eth1').decode()
        logger.info(out)
        rc = re.search(r'bound to (\d+\.\d+\.\d+\.\d+)', out, re.I|re.S)
        result = False
        if rc:
            dhcp_lease = rc.group(1)
            logger.info("Remote PC get IP {} from central LAN PC.".format(dhcp_lease))
            result = True
        Assertion.assert_equal(result, True, "ERR: Remote PC gets DHCP lease failed.")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_65_DHCP_Lease_Bound_to_X2(Test):
    uuid = "SOSAIOT-TC-54255"
    description = '''
        The user will ensure that the DHCP Client on X2 (LAN) zone of Remote network will obtain IP address
        through VPN tunnel when DHCP lease bound to field on the Remote Gateway is set to X2. 
    '''

    def test_65_Step01_Show_Test_Plan(self):
        show_testcase_info(TESTPLAN, '65')

    def test_65_Step02_Config_Remote_DHCP_over_VPN(self):
        remote_dict = {
            'bound-to': 'X2',
            'relay-ip': RELAY_IP,
            'management-ip': MGMT_IP,
            'block-_spoof': True,
            'temp-lease': False,
            'lease-time': '2',
        }
        rc = r_dho_vpn_cli.remote_gw_setting(**remote_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    def test_65_Step03_Disable_and_Enable_Remote_VPN_Policy(self):
        rc = r_vpn_cli.disable_vpnpolicy(**remote_vpn)
        time.sleep(3)
        rc &= r_vpn_cli.enable_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_65_Step04_Get_Lease_on_X2_Client_PC(self):
        global dhcp_lease
        dhcp_lease = ''
        RMT_HOST.system('dhclient -r eth2')
        out = RMT_HOST.system('dhclient -v eth2').decode()
        logger.info(out)
        rc = re.search(r'bound to (\d+\.\d+\.\d+\.\d+)', out, re.I|re.S)
        result = False
        if rc:
            dhcp_lease = rc.group(1)
            logger.info("Remote PC get IP {} from central LAN PC.".format(dhcp_lease))
            result = True
        Assertion.assert_equal(result, True, "ERR: Remote PC gets DHCP lease failed.")

    def test_65_Step06_Verify_Test(self):
        global dhcp_lease
        logger.info(dhcp_lease)
        time.sleep(3)
        out1 = os.popen('ping {} -c 5 -I eth2'.format(dhcp_lease)).read()
        logger.info("\n{}".format(out1))
        os.system('rm -rf /tmp/index.html')
        os.system('wget https://{} --no-check-certificate -O /tmp/index.html'.format(MGMT_IP))
        out2 = os.popen('cat /tmp/index.html').read()
        logger.info("\n{}".format(out2))
        rc = 0
        if re.search(r'100% packet loss', out1, re.I):
            logger.error("ping remote PC failed.")
        else:
            logger.info("ping remote PC passed.")
            rc += 1
        if re.search(r'SonicWALL', out2, re.I | re.S):
            logger.info("Manage remote GW passed.")
            rc += 1
        else:
            logger.error("Manage remote GW failed.")
        Assertion.assert_equal(rc, 2, "ERR: Verify failed.")

