from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC1_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.X2_IP}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X1_SUBNET}/24 via {Parameter.X2_IP}' in output else False
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
