from definition.settings import *


class TestSetupForPC(Test):
    uuid = 'NonTC'

    def test_01_config_rapid_commit_on_pc5(self):
        cmds = [
            f'cp {config_path} /etc/dhcp/dhclient6.conf',
            'systemctl restart network',

        ]
        PC5_Login.send_commands(cmds)
        checkres = PC5_Login.send_command('cat /etc/dhcp/dhclient6.conf')
        flag = True if 'send dhcp6.rapid-commit' in checkres else False
        Assertion.assert_equal(flag, True, "ERR: Config rapid_commit on pc5 eth1failed")

