from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_01_config_interface(self):
        logger.info('-'*10+'config x1  ip'+'-'*10)
        rc = Linterface.config_interface(**Lx1_ipv4)
        rc &= Linterface.config_interface(**Lx2_ipv4)
        Assertion.assert_equal(rc, True, 'config x1  ip Failed.')

    def test_00_02_restore_remote(self):
        logger.info('Restore Remote FW...')
        path = cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device={} -if=X2 -zone=WAN -ip=12.12.2.201 -restore=1'.format(path, Params.testbed, rm_device)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(DHCPV6_X2)).read()
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

    @repeat_method(3)
    def test_00_03_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_00_04_config_dhcpv6_scope(self):
        rc = Rdhcp_obj.add_dhcp_server_scope_dynamic(**dhcp_scope_dyn_v6)
        Assertion.assert_equal(rc, True, "ERR: add dhcp scope failed")

    def test_00_05_config_dhcpserver_x1_v6(self):
        rc = Rinterface_ipv6.config_interface_ipv6(**Rx1_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 failed")

    def test_00_06_config_dhcpv6_x1(self):
        rc = Linterface_ipv6.config_interface_ipv6(**Lx1_ipv6)
        time.sleep(40)
        Assertion.assert_equal(rc, True, f"ERR: config x1 dhcpv6 failed")
    
    def test_00_07_config_dhcpv6_x1_RA(self):
        ref = copy.deepcopy(Rx1_ipv6)
        ref['router_adv'] = True
        ref['managed'] = False
        ref['other_config'] =True
        rc = Rinterface_ipv6.config_interface_ipv6(**ref)
        rc &= Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        time.sleep(10)
        res = Linterface_ipv6.get_interface_address(name = 'x1')
        logger.info(f'------{res}')
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config  failed")



