from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed PCs'
    goto_teardown = True

    def test_01_config_PC1_route(self):
        logger.info(f'Set route on PC1 via gw {Parameter.FIREWALL}')
        cmds = [
            f'route add -net {Parameter.Route_Host_1} netmask {Parameter.Route_Mask_1} gw {Parameter.PC1_GW}',
            'route del default',
            f'route add -net {Parameter.Route_Host_2} netmask {Parameter.Route_Mask_2} gw {Parameter.FIREWALL}',
            'ip -4 r'
        ]
        output = PC1_LOGIN.send_commands(cmds)
        logger.info(output)
        Assertion.assert_regular(output, 'default via 192.168.168.168 dev eth0', "==> ERR: Config PC1 route failed!!")

    def test_02_setup_ftp_server(self):
        path = '/etc/vsftpd'
        logger.info(f"{' Backup ftp user files ':=^50}")
        PC1_LOGIN.send_command(f"cp -rf {path}/ftpusers  {path}/ftpusers.bak")
        PC1_LOGIN.send_command(f"cp -rf {path}/user_list  {path}/user_list.bak")

        logger.info(f"{' Allow user <root> to connect ftp ':=^50}")
        PC1_LOGIN.send_command(f"cp -rf {script_path}/ftpusers  {path}/ftpusers")
        PC1_LOGIN.send_command(f"cp -rf {script_path}/user_list  {path}/user_list")

        logger.info(f"{' Restart FTP service ':=^50}")
        PC1_LOGIN.send_command("systemctl restart vsftpd")

        logger.info(f"{' Check FTP service status':=^50}")
        output = PC1_LOGIN.send_command("netstat -anp | grep vsftpd")
        rc = 'LISTEN' in output
        logger.info(f'Start FTP service status: {rc}')
        Assertion.assert_equal(rc, True, "ERR: Setup FTP server failed")


class TestTraffic(Test):
    uuid = 'NonTC'
    description = 'Check and generate traffic'
    goto_teardown = True

    def test_01_check_dns_filtering_server_connection(self):
        dns_server = Parameter.Filtering_server
        cmd = f'ping {dns_server} -c 5'
        output = PC1_LOGIN.send_command(cmd)
        logger.info(output)
        Assertion.assert_not_regular(output, '100% packet loss', '==> ERR: Cannot access to dns server')

    def test_02_generate_dns_traffic(self):
        try:
            with open(f"{script_path}Categorized_domains", "r", encoding='UTF-8') as f:
                lines = f.readlines()
                for domain in lines:
                    domain = domain.strip()
                    subprocess.Popen(
                        ["dig", "+short", "+retry=0", domain, f"@{Parameter.FIREWALL}"], stdout=subprocess.DEVNULL)
        finally:
            f.close()
        Assertion.assert_equal(True, True, '==> ERR: Generate traffic failed!!')
