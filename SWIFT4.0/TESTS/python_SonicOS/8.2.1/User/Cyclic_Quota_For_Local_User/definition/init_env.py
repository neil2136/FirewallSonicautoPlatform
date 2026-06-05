from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(3)
    def test_03_Register(self):
        time.sleep(10)
        rc = lc_cli.register('online')
        Assertion.assert_equal(rc, True, "ERR: Register failed")

    def test_04_Config_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN5 -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.\
              format(path, Params.testbed)
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

    def test_05_Enable_Remote_FW_API(self):
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

    def test_06_Add_Network_Obj(self):
        rc = ao_api.config_addressobject(**local_vpn_obj)
        rc = ao_cli.add_address_group(**local_group)
        rc &= r_ao_api.config_addressobject(**remote_vpn_lan)
        rc &= r_ao_api.config_addressobject(**remote_vpn_dmz)
        rc &= r_ao_cli.add_address_group(**remote_group)
        Assertion.assert_equal(rc, True, "ERR: Add network AO failed")

    def test_07_Add_VPN_Policy(self):
        rc = r_vpn_cli.fw.do_cli_commands(remote_lan_vpn_cmds)
        rc &= vpn_cli.fw.do_cli_commands(local_lan_vpn_cmds)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policies failed")

    def test_08_Add_Service_Group(self):
        group = {
            'name': 'tc04_group',
            'add-object': ['HTTP', 'FTP'],
            'add-group':['ICMP'],
        }
        rc = service_cli.add_service_group(**group)
        Assertion.assert_equal(rc, True, "ERR: Add service group failed")
