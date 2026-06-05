from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_config_route_to_pcs(self):
        res = {}
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route -A inet6 add {Parameter.X0_IPV6_SUBNET}/64 gw {Parameter.X0_IPV6}',
                'ip -4 r']
        output = pc1.send_commands(cmds)
        res['pc1'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.FIREWALL}' in output else False
        cmd = [f'ip -6 r']
        output = pc1.send_commands(cmd)
        res['pc1'] &= True if f'{Parameter.X0_IPV6_SUBNET}/64 via {Parameter.X0_IPV6}' in output else False

        logger.info(" {} ".center(50, '-').format('PC2 Route Configure'))
        cmds = [f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route -A inet6 add {Parameter.X0_IPV6_SUBNET}/64 gw {Parameter.X0_IPV6}',
                'ip -4 r']
        output = pc2.send_commands(cmds)
        res['pc2'] = True if f'{Parameter.X0_SUBNET}/24 via {Parameter.FIREWALL}' in output else False
        cmd = [f'ip -6 r']
        output = pc2.send_commands(cmd)
        res['pc2'] &= True if f'{Parameter.X0_IPV6_SUBNET}/64 via {Parameter.X0_IPV6}' in output else False
        
        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        logger.info(pc3)
        cmds = [f'route add -net {Parameter.X2_SUBNET}/24 gw {Parameter.X2_IP}',
                f'route -A inet6 add {Parameter.X2_IPV6_SUBNET}/64 gw {Parameter.X2_IPV6}',
                'ip -4 r']
        output = pc3.send_commands(cmds)
        res['pc3'] = True if f'{Parameter.X2_SUBNET}/24 via {Parameter.X2_IP}' in output else False
        cmd = [f'ip -6 r']
        output = pc3.send_commands(cmd)
        res['pc3'] &= True if f'{Parameter.X2_IPV6_SUBNET}/64 via {Parameter.X2_IPV6}' in output else False

        logger.info(" {} ".center(50, '-').format('PC4 Route Configure'))
        cmds = [f'route add -net {Parameter.X3_SUBNET}/24 gw {Parameter.X3_IP}',
                f'route -A inet6 add {Parameter.X3_IPV6_SUBNET}/64 gw {Parameter.X3_IPV6}',
                'ip -4 r']
        output = pc4.send_commands(cmds)
        res['pc4'] = True if f'{Parameter.X3_SUBNET}/24 via {Parameter.X3_IP}' in output else False
        cmd = [f'ip -6 r']
        output = pc4.send_commands(cmd)
        res['pc4'] &= True if f'{Parameter.X3_IPV6_SUBNET}/64 via {Parameter.X3_IPV6}' in output else False

        logger.info(f'config pcs result: {res}')
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
