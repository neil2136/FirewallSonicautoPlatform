from definition.settings import *


class TestSetup_PCs(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_httpd_server_setup(self):
        virus_server = "10.6.0.69"
        cmd_list = [
            "mkdir /var/www/https/",
            "chmod 777 /var/www/https/",
            "\cp -rf {}/* /var/www/https/".format(HTTPS_SERVER_PATH),
            f"wget http://{virus_server}/virus/password-protected-test.zip -O /var/www/https/password-protected-test.zip",
            f"wget http://{virus_server}/virus/Exploit.VBS.Agent.q.gz -O /var/www/https/Exploit.VBS.Agent.q.gz",
            f"wget http://{virus_server}/virus/upx.exe -O /var/www/https/upx.exe",
            f"wget http://{virus_server}/virus/1.cab.bin -O /var/www/https/1.cab.bin",
            "rm -f /etc/httpd/conf.d/ssl.conf",
            "\cp -fr {}/ssl.conf /etc/httpd/conf.d/".format(configPath + "conf.d"),
            "\cp -fr {}/httpd.conf /etc/httpd/conf/".format(configPath + "conf"),
            "grep /www/https /etc/httpd/conf.d/ssl.conf",
            "install {}/* /etc/pki/tls/certs/".format(certPath),
            "install {}/* /etc/pki/tls/private/".format(certPath),
            "systemctl stop httpd",
            "systemctl start httpd",
            "systemctl status httpd",
        ]
        res = PC5_login.send_commands(cmd_list)
        flag = True if re.search(r"active \(running\)", res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")

    def test_02_pppoe_server_setup(self):
        res = PC5_login.start_PPPoE_server(
            interface=PPPoeParams.PPPOE_IF,
            local_ip=PPPoeParams.LOCAL_IP,
            assign_ip=PPPoeParams.PPPOE_ASSIGN,
            ppp_secrets=PPPoeParams.PPP_SECRETS,
            pppoe_option=PPPoeParams.PPPOE_OPTIONS,
        )
        Assertion.assert_equal(res, True, "ERR: Start PPPoE Server on PC4 failed")

    def test_03_ftp_server_setup(self):
        logger.info("1, configure vsftpd.conf")
        cmd_list = [
            f"\cp -rf {CONF_PATH}/ftpserver/* /etc/vsftpd/",
            "timeout 20 systemctl restart vsftpd",
            "timeout 20 systemctl status vsftpd -l",
        ]
        out = PC5_login.send_commands(cmd_list)
        res = "running" in out
        logger.info("2, mk test file")
        PC5_login.send_command("echo test for pppoe ftp > /var/ftp/test.txt")
        Assertion.assert_equal(res, True, "ERR: start ftp service on PC5 failed!")

    def test_04_config_route_to_pcs(self):
        res = {}
        # PC1
        logger.info(" {} ".center(50, "-").format("PC1 Route Configure"))
        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}",
            "ip -4 r",
        ]
        output = PC1_login.send_commands(cmds)
        res["pc2"] = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X2_IP}" in output
            else False
        )
        # PC2
        logger.info(" {} ".center(50, "-").format("PC2 Route Configure"))
        cmds = [
            "ifconfig eth1 up",
            f"ifconfig eth1 {PC2_ETH1_IP}/24",
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_IP}",
            "ip -4 r",
        ]
        output = PC2_login.send_commands(cmds)
        res["pc2"] = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X2_IP}" in output
            else False
        )
        # PC3
        logger.info(" {} ".center(50, "-").format("PC3 Route Configure"))
        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X3_IP}",
            "ip -4 r",
        ]
        output = PC3_login.send_commands(cmds)
        res["pc3"] = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X3_IP}" in output
            else False
        )
        # PC4
        logger.info(" {} ".center(50, "-").format("PC4 Route Configure"))
        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X4_VLAN_IP}",
            "ip -4 r",
        ]
        output = PC4_login.send_commands(cmds)
        res["pc4"] = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X4_VLAN_IP}" in output
            else False
        )
        Assertion.assert_equal(all(res.values()), True, "ERR: Config PCs route failed")
