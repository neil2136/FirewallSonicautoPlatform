from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    description = "initial PC"
    goto_teardown = True

    def test_01_config_routes_on_PC(self):
        pc1_login.send_command('route add -net 172.16.1.0/24 gateway 192.168.168.168')
        out = pc1_login.send_command('ip -4 r')
        rc = '172.16.1.0/24 via 192.168.168.168 dev eth1' in out
        Assertion.assert_equal(rc, True, 'ERR: add route on PC1 failed!!')
