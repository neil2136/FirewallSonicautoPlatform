from settings import *


class TestConfigPPPoEServer(Test):
    uuid = 'NonTC'
    description = 'Initial PPPoE Server testbed'
    goto_teardown = True

    def test_01_backup_pppoe(self):
        ## --------------------------backup PPPoE confs
        ## backup PPPoE -> options
        # PC2_login.send_command('vncserver') #for debug PC2
        PC2_login.send_command('ifconfig')
        PC2_login.send_command(f"\cp -rf /etc/ppp/options  /etc/ppp/options.bak")
        ## backup PPPoE -> pppoe-server-options
        PC2_login.send_command(f"\cp -rf /etc/ppp/pppoe-server-options /etc/ppp/pppoe-server-options.bak")
        ## backup PPPoE -> chap-secrets
        PC2_login.send_command(f"\cp -rf /etc/ppp/chap-secrets /etc/ppp/chap-secrets.bak")
        ## check result
        checkres = PC2_login.send_command("ls /etc/ppp/")
        res = True if 'options.bak' and 'chap-secrets.bak' and 'pppoe-server-options.bak' in checkres else False
        logger.info(f'backup PPPoE server result: {res}')
        Assertion.assert_equal(res, True, "ERR: Backup PPPoE server failed")

    def test_02_setup_pppoe_server_on_pc2(self):
        # options
        logger.info(f"{' Setup options ':=^50}")
        cmd_cp_options = f'\cp -rf {setup_path}/options  /etc/ppp/options'
        PC2_login.send_command(cmd_cp_options)
        logger.info('Execute cmd:' + cmd_cp_options)

        # pppoe-server-options
        logger.info(f"{' Setup pppoe-server-options ':=^50}")
        cmd_cp_pppoe_server = f'\cp -rf {setup_path}/pppoe-server-options  /etc/ppp/pppoe-server-options'
        PC2_login.send_command(cmd_cp_pppoe_server)
        logger.info('Execute cmd:' + cmd_cp_pppoe_server)

        # test "password"  chap-secrets
        logger.info(f"{' Setup chap-secrets ':=^50}")
        cmd_cp_chap = f'\cp -rf {setup_path}/chap-secrets  /etc/ppp/chap-secrets'
        PC2_login.send_command(cmd_cp_chap)
        logger.info('Execute cmd:' + cmd_cp_chap)

        # start PPPoE
        logger.info(f"{' Start PPPoE Server 1 ':=^50}")
        start_pppoe_server1 = '/usr/sbin/pppoe-server -I eth1 -L {} -R {}-{} -N 20'.format(
            Parameter.PC2_SERVER_X2, Parameter.ip_pool_start_X2, Parameter.ip_pool_end_X2)
        PC2_login.send_command(start_pppoe_server1)
        logger.info('Execute cmd:' + start_pppoe_server1)
        logger.info(f"{' Start PPPoE Server 2 ':=^50}")
        start_pppoe_server2 = '/usr/sbin/pppoe-server -I eth2 -L {} -R {}-{} -N 20'.format(
            Parameter.PC2_SERVER_X3, Parameter.ip_pool_start_X3, Parameter.ip_pool_end_X3)
        PC2_login.send_command(start_pppoe_server2)
        logger.info('Execute cmd:' + start_pppoe_server2)

        # check result
        logger.info(f"{' Check Setup Result ':=^50}")
        stat = PC2_login.send_command("ps -aux | grep ppp")
        res = True if '/usr/sbin/pppoe-server' in stat else False
        logger.info('Start PPPoE Server result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: configure PPPoE Server on PC2 eth0 failed!")

    def test_03_client_route_to_pppoe_server(self):
        # --------------------------config client route to ping PPPoE server
        # add route
        localhost.send_command(f'route add -net {Parameter.ADD_PC2_X2_ROUTE}')
        localhost.send_command(f'route add -net {Parameter.ADD_PC2_X3_ROUTE}')
        # test route
        iproute = localhost.send_command('ip route show')
        res = True if Parameter.CHECK_X2_ROUTE and Parameter.CHECK_X3_ROUTE in iproute else False
        Assertion.assert_equal(res, True, "ERR: route to PPPoE Server failed!")
