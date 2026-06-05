from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_pc(self):
        cmd_pc1 = ['timedatectl set-ntp on', 'echo 192.168.168.168 shanghaiqa.com >> /etc/hosts', 'curl -k https://shanghaiqa.com']
        cmd_pc2 = ['timedatectl set-ntp on', 'echo 12.12.1.168 shanghaiqa.com >> /etc/hosts', 'curl -k https://shanghaiqa.com']
        cmd_pc3 = ['timedatectl set-ntp on','echo 13.13.1.168 shanghaiqa.com >> /etc/hosts', 'curl -k https://shanghaiqa.com']
        out_pc1 = pc1_login.send_commands(cmd_pc1)
        out_pc2 = pc2_login.send_commands(cmd_pc2)
        out_pc3 = pc3_login.send_commands(cmd_pc3)
        msg = 'This page is redirecting!'
        rc = msg in out_pc1 and msg in out_pc2 and msg in out_pc3
        time.sleep(100)
        Assertion.assert_equal(rc, True, 'ERR: config PC1 failed!!')
