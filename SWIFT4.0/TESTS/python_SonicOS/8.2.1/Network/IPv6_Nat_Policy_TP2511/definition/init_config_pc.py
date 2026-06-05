from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_v6_route_pc1(self):
        pc1_login.send_command('ip -6 r add 2001::/64 via 2000::168')
        out = pc1_login.send_command('ip -6 r')
        Assertion.assert_regular(out, '2001::/64 via 2000::168 dev eth1', 'ERR: set route for pc1 failed.')

    def test_02_start_httpd_on_pc2(self):
        res = False
        for i in range(3):
            pc2_login.send_command('systemctl restart httpd')
            out = pc2_login.send_command('systemctl status httpd')
            if 'running' in out:
                pc2_login.send_command('echo test for v6 nat > /root/index.html')
                out = pc2_login.send_command('curl http://[::1]')
                res = 'test for v6 nat' in out
                break
        Assertion.assert_equal(res, True, 'ERR: start httpd service on pc2 failed.')
