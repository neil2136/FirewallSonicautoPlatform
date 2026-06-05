from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'
    PC_login = PC3_login

    def test_01_setup_dhcp_server_in_PC3(self):
        logger.info("Setup for the DHCPv4 server on CentOS7 on PC3... ")
        cmds = [
            "\cp -rf {}/dhcpd.conf /etc/dhcp".format(DHCP_SERVER_PATH),
            "systemctl restart dhcpd",
            "systemctl status dhcpd",
        ]
        output = self.PC_login.send_commands(cmds)
        # As long as there is 'Running' in the response , that means the DHCPv4 server is up
        Assertion.assert_regular(output, 'running', "ERR: Setup for the DHCPv4 server on CentOS7 on PC3 failed")

    def test_02_config_route_to_pc3(self):
        cmds = [
            "ip r a 192.168.2.0/24 via {} dev eth1".format(Parameter.X3_IP),
            "ip -4 r",
        ]
        output = self.PC_login.send_commands(cmds)
        self.PC_login.send_command('exit')
        Assertion.assert_regular(output, r'192.168.2.0', "ERR: Add route for remote X2 network failed!")
