from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True


    def test_01_change_default_route_for_pc3(self):
        cmd = ['systemctl restart network', 'route add -net 10.0.0.0/8 gateway 192.168.4.1', 'mount -a',
               'route del default', 'route add default gateway 13.13.1.168', 'ip -4 r']
        out = pc3_login.send_commands(cmd)
        Assertion.assert_regular(out, 'default via 13.13.1.168 dev eth1', 'ERR: change_default_route_for_pc3 failed!!')