from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_start_http_server_on_pc2(self):
        cmds = [
            'systemctl start httpd.service',
            'systemctl status httpd.service'
        ]
        res = PC2_Login.send_commands(cmds)
        flag = True if 'Started The Apache HTTP Server' in res else False
        Assertion.assert_equal(flag, True, "ERR: start http server on PC2 failed")
