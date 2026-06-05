from definition.settings import *

class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    @repeat_method(5, sleep=10)
    def test_01_setup_dhcp_server_on_pc2(self):
        logger.info('conf dhcp server on PC2.....')
        cmd_cp_conf = f'\cp -r {DHCP_SERVER_CONF_FILE} /etc/dhcp/'
        logger.info(f'Execute cmd: {cmd_cp_conf}')
        pc2_login.send_command(cmd_cp_conf)
        res = False
        # start dhcpd service
        for i in range(5):
            pc2_login.send_command('service dhcpd start')
            status = pc2_login.send_command('service dhcpd status')
            logger.info(status)
            if re.search('dhcpd.* is running', status):
                logger.info('dhcpv4 server is running')
                res = True
                break
            else:
                pc2_login.send_command('service dhcpd restart')            
        Assertion.assert_equal(res, True, "ERR: Start dhcp server on PC2 failed")

    @repeat_method(5, sleep=10) 
    def test_02_setup_pppoe_server_on_pc2(self):
        logger.info('conf PPPoE server on pc2......')
        # cp options
        logger.info('setup options.....')
        cmd_options = f'cp -rf {PPPOE_SERVER_CONF_FILE}/options /etc/ppp/options'
        logger.info(f'Execute cmd: {cmd_options}')
        pc2_login.send_command(cmd_options)
        
        # cp pppoe-server-options
        logger.info('setup pppoe server options.....')
        cmd_pppoe_server = f'cp -rf {PPPOE_SERVER_CONF_FILE}/pppoe-server-options /etc/ppp/pppoe-server-options'
        logger.info(f'Execute cmd: {cmd_pppoe_server}')
        pc2_login.send_command(cmd_pppoe_server)
        
        # cp chap-secrets
        logger.info('setup chap-secrets.....')
        cmd_cp_chap = f'cp -rf {PPPOE_SERVER_CONF_FILE}/chap-secrets /etc/ppp/chap-secrets'
        logger.info(f'Execute cmd: {cmd_cp_chap}')
        pc2_login.send_command(cmd_cp_chap)
        
        # start pppoe service
        logger.info('start pppoe service....')
        cmd_start_pppoe_server = f'/usr/sbin/pppoe-server -I eth1 -L \
            {Parameter.PPPOE_SERVER} -R {Parameter.pppoe_pool_start}-{Parameter.pppoe_pool_end}'
        logger.info(f'Execulte cmd {cmd_start_pppoe_server}')
        pc2_login.send_command(cmd_start_pppoe_server)
        
        # test if pppoe server is running
        logger.info('check if pppoe service is running.....')
        status = pc2_login.send_command('ps -aux | grep ppp')
        res = True if 'pppoe-server' in status else False
        logger.info(f'start PPPoE Server result: {res}')
        Assertion.assert_equal(res, True, "ERR: configure PPPoE Server on PC2 failed!")