from definition.settings import *


class TestInitPCConfig(Test):
    uuid = 'NonTC'

    def test_01_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -host {Parameter.R_X1_IP} gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.R_X3_NET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        output = PC1_HOST.send_commands(cmds)
        res['pc1'] = True if (f'{Parameter.R_X3_NET}/24 via {Parameter.FIREWALL}' in output
                              and f'{Parameter.R_X1_IP} via {Parameter.FIREWALL}' in output) else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X3_NET}/24 gw {Parameter.R_X3_IP}',
                f'route add -net {Parameter.R_X2_NET}/24 gw {Parameter.R_X3_IP}',
                'ip -4 r']
        output = PC2_HOST.send_commands(cmds)
        res['pc2'] = True if (f'{Parameter.X3_NET}/24 via {Parameter.R_X3_IP}' in output
                              and f'{Parameter.R_X2_NET}/24 via {Parameter.R_X3_IP}') else False

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [f'route add -net {Parameter.R_X3_NET}/24 gw {Parameter.X3_IP}',
                'ip -4 r']
        output = PC3_HOST.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.R_X3_NET}/24 via {Parameter.X3_IP}' in output else False

        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs Route Failed")