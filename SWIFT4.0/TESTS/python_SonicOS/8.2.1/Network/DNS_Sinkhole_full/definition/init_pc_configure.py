from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    description = 'Initialize PCs routes'
    goto_teardown = True

    def test_01_config_PC1_route(self):
        logger.info(f'Set route on PC1 via gw {Parameter.FIREWALL}')
        cmds = [
            f'route add -net {Parameter.Route_Host_1} netmask {Parameter.Route_Mask_1} gw {Parameter.PC1_GW}',
            'route del default',
            f'route add -net {Parameter.Route_Host_2} netmask {Parameter.Route_Mask_2} gw {Parameter.FIREWALL}',
            'ip -4 r'
        ]
        output = PC1_LOGIN.send_commands(cmds)
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth0', "==> ERR: Config PC1 route failed!!")

    def test_02_copy_script_to_PC2(self):
        cmds = [
            f'cp {script_path}/PC2_query.py /tmp/PC2_query.py',
            f'cp {script_path}/dns_flooding.py /tmp/dns_flooding.py',
            'ls /tmp'
        ]
        out = PC2_LOGIN.send_commands(cmds)
        rc = all(x in out for x in ['PC2_query', 'dns_flooding'])
        Assertion.assert_equal(rc, True, "==> ERR: copy_script_to_PC2 failed!!")

    def test_03_config_PC2_route(self):
        cmds = [
            f'route add -net {Parameter.Route_Host_1} netmask {Parameter.Route_Mask_1} gw {Parameter.FIREWALL}',
            'route del default',
            f'route add default gw {Parameter.FIREWALL}',
            'ip -4 r'
        ]
        output = PC2_LOGIN.send_commands(cmds)
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth0', "==> ERR: Config PC2 route failed!!")
