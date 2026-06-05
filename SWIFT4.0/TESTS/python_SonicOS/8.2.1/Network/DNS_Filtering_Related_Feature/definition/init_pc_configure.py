from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    description = 'Initialize PCs routes'
    goto_teardown = True

    @repeat_method(3)
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

    def test_02_check_dns_server(self):
        dns_server = Parameter.Filtering_server
        cmd = f'ping {dns_server} -c 5'
        output = PC1_LOGIN.send_command(cmd)
        logger.info(output)
        Assertion.assert_not_regular(output, '100% packet loss', '==> ERR: Cannot access to dns server')
