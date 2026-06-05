from definition.settings import *

class TestSetup_On_PC1(Test):
    uuid = 'NonTC'
    logger.info(os.environ["PYTHON_SONICOS_HOME"] + '/Network/WireGuard_VPN/definition/')

    def test_02_add_route_to_PC1(self):
        command1 = 'route add -net {} gw {}'.format(wg0_Network, FIREWALL)
        ret1 = os.system(command1)
        logger.info(ret1)
        Assertion.assert_equal(True, True, "ERR: Add routes to PC1 failed")


# class TestSetup_http_server_on_PC2(Test):
#     uuid = 'NonTC'
#     logger.info(os.environ["PYTHON_SONICOS_HOME"] + '/Security_Services/GAV_Settings/config/')
#     def test_01_setup_http_serverr(self):
#
#         ### get virus to /var/www/html/ from virus server
#         virus_name = ('password-protected-test.zip', 'Exploit.VBS.Agent.q.gz', 'upx.exe')
#         for name in virus_name:
#             ret = PC2_login.send_command('wget http://10.6.0.69/virus/' + name + ' -O /var/www/html/' + name)
#             ret = str(ret)
#             if re.search('failed|Not Found', ret, re.I|re.S):
#                 logger.info("Copy virus and anti-spyware file fail")
#                 Assertion.assert_regular(False, True,"ERR: Copy virus and anti-spyware file failed")
#             else:
#                 if re.search('100%', ret, re.I|re.S):
#                     logger.info("Copy virus and anti-spyware file pass")
#                 else:
#                     time.sleep(5)
#
#         ### change http config file
#         ret = PC2_login.send_command('cp -f {} /etc/httpd/conf/'.format(conf_path))
#         logger.info('8' * 60)
#         logger.info(ret)
#         logger.info('8' * 60)
#         if ret == '':
#             logger.info("config httpd.conf file pass")
#         else:
#             logger.info("config httpd.conf file fail")
#
#         PC2_login.send_command('service httpd start')
#         ret = PC2_login.send_command('service httpd status')
#         ret = str(ret)
#         Assertion.assert_regular(ret, 'running',"ERR: start httpd service failed")
#
#     def test_02_add_route_to_PC(self):
#         command1 = 'route add -host {} gw {}'.format(PC2_ETH2_IP, FIREWALL)
#         ret1 = os.system( command1 )
#         logger.info(ret1)
#         command2 = 'route add -host {} gw {}'.format(PC1_ETH0_IP, X2_IP)
#         ret2 = PC2_login.send_command( command2 )
#         logger.info(ret2)
#         Assertion.assert_equal(True, True, "ERR: Add routes to PC failed")



