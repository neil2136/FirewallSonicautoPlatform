from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/bin/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN5 -if=X2 -zone={} -ip={} -restore=1'.\
              format(path, Params.testbed, R_X2_ZONE, R_X2_IP)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(R_X1_IP)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')

        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    def test_03_Enable_Remote_FW_API(self):
        logger.info(" {} ".center(20, '-').format('Enable Remote Api Basic'))
        api_dict = {
            'sonicos-api': True,
            'basic': True,
        }
        rc = r_admin_cli.sonicos_api(**api_dict)
        if rc:
            logger.info('Success enable remote api basic')
        else:
            logger.info('Failed enable remote api basic')
        Assertion.assert_equal(rc, True, "ERR: Enable Remote FW basic API failed")

    @repeat_method(2)
    def test_04_Config_Remote_X2(self):
        logger.info("config remote x2 interface... ")
        time.sleep(5)
        rc = r_interface_cli.config_interface(**r_x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config remote X2 to static failed")

    def test_05_Add_Network_Obj(self):
        rc = r_ao_api.config_addressobject(**remote_vpn_lan)
        Assertion.assert_equal(rc, True, "ERR: Add network AO failed")

    def test_06_Add_VPN_Policy(self):
        rc = vpn_cli.add_vpnpolicy(**local_vpn)
        rc &= r_vpn_cli.add_vpnpolicy(**remote_vpn)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")

    def test_07_Remove_DHCP_Server_on_Remote_GW(self):
        del_dict = { 'type': 'all' }
        rc = r_dhcp_svr_cli.delete_all_scopes(**del_dict)
        dhcp_svr = {}
        rc &= r_dhcp_svr_cli.disable_dhcpserver(**dhcp_svr)
        Assertion.assert_equal(rc, True, "ERR: Remove DHCP on remote GW failed.")

    def test_08_Config_DHCP_Server_on_LAN_PC(self):
        cmd = 'cp -rf {} /etc/dhcp/dhcpd.conf'.format(DHCPCONF)
        os.system(cmd)
        out = os.popen('service dhcpd restart').read()
        logger.info("\n{}".format(out))
        rc = False
        if re.search(r'Starting dhcpd.*OK', out, re.I|re.S):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Config DHCP server failed.")

    def test_09_Config_DHCP_Server_on_Central_GW(self):
        logger.info("Remove all existing DHCP server on central GW.")
        del_dict = { 'type': 'all' }
        rc = dhcp_svr_cli.delete_all_scopes(**del_dict)
        dynamic_scope = {
            'enable': True,
            'type': 'dynamic',
            'start': SCOPE_START,
            'end': SCOPE_END,
            'netmask': MASK,
            'lease-time': '100',
            'dns1': DNS1,
            'dns2': DNS2,
        }
        rc &= dhcp_svr_cli.add_dhcpserver_scope_v4(**dynamic_scope)
        Assertion.assert_equal(rc, True, "ERR: Config DHCP server failed.")
