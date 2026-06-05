from definition.settings import *


class TestSetup_PCs(Test):
    uuid = 'NonTC'

    def test_01_setup_ftp_server_to_pc5(self):
        configfilecmds = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            "echo 1 > /proc/sys/net/ipv4/ip_forward",
            'systemctl restart vsftpd',
            'systemctl status vsftpd',
        ]
        output = PC5_login.send_commands(configfilecmds)
        res = True if 'running' in output and 'failed|Not Found' not in output else False
        Assertion.assert_equal(res, True, "ERR: setup ftp server on pc failed")

    def test_02_pppoe_server_setup(self):
        res = PC5_login.start_PPPoE_server(
            interface=PPPoeParams.PPPOE_IF,
            local_ip=PPPoeParams.LOCAL_IP,
            assign_ip=PPPoeParams.PPPOE_ASSIGN,
            ppp_secrets=PPPoeParams.PPP_SECRETS,
            pppoe_option=PPPoeParams.PPPOE_OPTIONS,
        )
        Assertion.assert_equal(res, True, "ERR: Start PPPoE Server on PC4 failed")

    def test_03_dhcp_server_setup(self):
        cmds = [
            f"\cp -rf {CONF_PATH}/dhcpserver/dhcpd.conf  /etc/dhcp",
            "systemctl restart dhcpd",
            "systemctl status dhcpd",
        ]
        output = PC5_login.send_commands(cmds)
        Assertion.assert_regular(output, 'running', "ERR: Config dhcp server in PC2 failed")

    def test_04_config_route_to_pcs(self):
        res = []
        logger.info(" {} ".center(50, '-').format('PC1 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}',
                f'route add -net {Parameter.REMOTE_X0_NET}/24 gw {Parameter.FIREWALL}',
                'ip -4 r']
        res1 = PC1_login.send_commands(cmds)
        res.append(True if f'{Parameter.REMOTE_X0_NET}/24 via {Parameter.FIREWALL}' in res1 else False)

        logger.info(" {} ".center(50, '-').format('PC3 Route Configure'))
        cmds = [
            f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X3_IP}',
            f'route add -host 10.6.0.69 gw {Parameter.X3_IP}',
            'ip -4 r']
        res3 = PC3_login.send_commands(cmds)
        res.append(True if f'{Parameter.X1_SUBNET}/24 via {Parameter.X3_IP}' in res3 else False)

        logger.info(" {} ".center(50, '-').format('PC4 Route Configure'))
        cmds = [f'route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}',
                f'route add -net {Parameter.X0_SUBNET}/24 gw {Parameter.REMOTE_X0_IP}',
                'ip -4 r']
        res4 = PC4_login.send_commands(cmds)
        res.append(True if f'{Parameter.X0_SUBNET}/24 via {Parameter.REMOTE_X0_IP}' in res4 else False)

        Assertion.assert_equal(all(res), True, "ERR: PCs route settings failed")
