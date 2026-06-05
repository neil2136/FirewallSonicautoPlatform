from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_config_mail_server(self):
        res = False
        # add a route from pc1 to pc3
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC1_login.send_commands(cmds)
        checkres = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.FIREWALL}' in output else False
        if checkres:
            for i in range(5):
                res = setup_mail_server.start_mail_server(mail_server_host=mail_server_ip)
                if res:
                    logger.info('setup maill server to pc3 successful!')
                    break
                else:
                    time.sleep(10)
        Assertion.assert_not_equal(res, True, "ERR: start email server failed")

    def test_02_add_route_to_pc2(self):
        res = []
        PC2_login.send_command(f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}')
        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}',
                'ip -4 r']
        res2 = PC2_login.send_commands(cmds)
        res.append(True if f'{Parameter.X1_SUBNET}/24 via {Parameter.X2_IP}' in res2 else False)

        Assertion.assert_equal(all(res), True, "ERR: add route to pc2 failed")
