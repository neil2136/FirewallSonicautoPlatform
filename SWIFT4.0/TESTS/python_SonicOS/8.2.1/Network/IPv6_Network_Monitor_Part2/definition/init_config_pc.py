from definition.settings import *


class Test_ConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_v6_addr_for_pc(self):
        pc2_login.send_command('ifconfig eth1 inet6 add 2010::100')
        pc1_login.send_command('ifconfig eth1 inet6 add 2000::100')
        out1 = pc1_login.send_command('ping6 2000::168 -c 3')
        out2 = pc2_login.send_command('ping6 2010::168 -c 3')
        rc = '100% packet loss' not in out1 and '100% packet loss' not in out2
        Assertion.assert_equal(rc, True, 'ERR: config v6 addr for pc failed!!')
