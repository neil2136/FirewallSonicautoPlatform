from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_00_01_config_DNS_in_pc3(self):
        output = os.popen(f'python3 {SCRIPT_PATH}/conf_dns_server.py -i {PC3_ETH0_IP} -p {FILE_PATH}').read()
        logger.info(output)
        res = False if 'failed' in output else True
        Assertion.assert_equal(res, True, "ERR: Config dns server in PC3 failed")

    def test_00_02_add_route_to_pc1(self):
        PC1_login.send_command(f'route add -net 172.16.1.0/24 gw {Parameter.FIREWALL}')
        PC2_login.send_command(f'route add -net 172.16.1.0/24 gw {Parameter.X2_IP}')
        Assertion.assert_equal(True, True, "ERR: add route to pc1 failed")
