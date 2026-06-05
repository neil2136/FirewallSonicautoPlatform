from definition.settings import *


class TestSetup_PCs(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_httpd_server_setup(self):
        cmd_list = [
            "mkdir /var/www/https/",
            "chmod 777 /var/www/https/",
            "\cp -rf {}/* /var/www/https/".format(HTTPS_SERVER_PATH),
            "rm -f /etc/httpd/conf.d/ssl.conf",
            "\cp -fr {}/ssl.conf /etc/httpd/conf.d/".format(HTTP_CFG_PATH + "conf.d"),
            "\cp -fr {}/httpd.conf /etc/httpd/conf/".format(HTTP_CFG_PATH + "conf"),
            "grep /www/https /etc/httpd/conf.d/ssl.conf",
            "install {}/* /etc/pki/tls/certs/".format(HTTP_CERT_PATH),
            "install {}/* /etc/pki/tls/private/".format(HTTP_CERT_PATH),
            "systemctl restart httpd",
            "systemctl status httpd",
        ]
        res = PC4_login.send_commands(cmd_list)
        flag = True if re.search(r"active \(running\)", res, re.S | re.I) else False
        Assertion.assert_equal(flag, True, "ERR: setup for lanpc failed")

    def test_02_dns_server_setup(self):
        cmds = [
            f"\cp {CONF_PATH}/dnsserver/named.conf /etc/named.conf",
            f"\cp {CONF_PATH}/dnsserver/named.rfc1912.zones /etc/named.rfc1912.zones",
            f"\cp {CONF_PATH}/dnsserver/baidu.com.zone /var/named/baidu.com.zone",
            f"\cp {CONF_PATH}/dnsserver/baidu.com.local /var/named/baidu.com.local",
            f"\cp {CONF_PATH}/dnsserver/google.co.jp.zone /var/named/google.co.jp.zone",
            "systemctl restart named",
            "systemctl status named",
        ]
        output = PC4_login.send_commands(cmds)
        Assertion.assert_regular(
            output, "running", "ERR: Config dns server in WAN PC failed"
        )

    def test_03_add_ipv6_lan_pc2(self):
        logger.info(f"Add IPv6 IP = {PC2_ETH2_IP_V6}/64 for PC2 ETH2.")
        cmds = [f"ip -6 addr add {PC2_ETH2_IP_V6}/64 dev eth2", "ifconfig eth2"]
        out = PC2_login.send_commands(cmds)
        res = f"inet6 {PC2_ETH2_IP_V6}  prefixlen 64" in out
        Assertion.assert_equal(res, True, "ERR: setup PC2 ipv6 failed.")

    def test_04_add_ipv6_lan_pc3(self):
        logger.info(f"Add IPv6 IP = {PC3_ETH2_IP_V6}/64 for PC3 ETH2.")
        cmds = [f"ip -6 addr add {PC3_ETH2_IP_V6}/64 dev eth2", "ifconfig eth2"]
        out = PC3_login.send_commands(cmds)
        res = f"inet6 {PC3_ETH2_IP_V6}  prefixlen 64" in out
        Assertion.assert_equal(res, True, "ERR: setup PC3 ipv6 failed.")

    def test_05_add_ipv6_wan_pc4(self):
        logger.info(f"Add IPv6 IP = {PC4_ETH2_IP_V6}/64 for PC4 ETH2.")
        cmds = [f"ip -6 addr add {PC4_ETH2_IP_V6}/64 dev eth2", "ifconfig eth2"]
        out = PC4_login.send_commands(cmds)
        res = f"inet6 {PC4_ETH2_IP_V6}  prefixlen 64" in out
        Assertion.assert_equal(res, True, "ERR: setup PC4 ipv6 failed.")

    def test_06_set_pcs_route_v4(self):
        logger.info(" {} ".center(50, "-").format("PCs V4 Route Configure"))
        results = {}
        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.FIREWALL}",
            "sleep 3",
            "ip -4 r",
        ]
        output = PC1_login.send_commands(cmds)
        res = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.FIREWALL}" in output
            else False
        )
        logger.info(f"Set PC1 route result: {res}")
        results["pc1"] = res

        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X2_GW}",
            "sleep 3",
            "ip -4 r",
        ]
        output = PC2_login.send_commands(cmds)
        res = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X2_GW}" in output
            else False
        )
        logger.info(f"Set PC2 route result: {res}")
        results["pc2"] = res
        cmds = [
            f"route add -net {Parameter.X1_SUBNET}/24 gw {Parameter.X3_GW}",
            "sleep 3",
            "ip -4 r",
        ]
        output = PC3_login.send_commands(cmds)
        res = (
            True
            if f"{Parameter.X1_SUBNET}/24 via {Parameter.X3_GW}" in output
            else False
        )
        logger.info(f"Set PC3 route result: {res}")
        results["pc3"] = res
        logger.info(f"Set PCs route results: {results}")
        Assertion.assert_equal(
            all(results.values()), True, "ERR: Config PCs route settings failed"
        )

    def test_07_set_pcs_route_v6(self):
        logger.info(" {} ".center(50, "-").format("PCs V6 Route Configure"))
        res = {}
        logger.info(" {} ".center(50, "-").format("PC2 ipv6 Route Configure"))
        cmds = [
            'echo "1" >> /proc/sys/net/ipv6/conf/all/forwarding',
            f"ip -6 route add {Parameter.X1_SUBNET_V6}/64 via {Parameter.X2_IP_V6}",
            "sleep 3",
            "ip -6 r",
        ]
        output = PC2_login.send_commands(cmds)
        res["pc2"] = (
            True
            if f"{Parameter.X1_SUBNET_V6}/64 via {Parameter.X2_IP_V6}" in output
            else False
        )

        logger.info(" {} ".center(50, "-").format("PC3 ipv6 Route Configure"))
        cmds = [
            'echo "1" >> /proc/sys/net/ipv6/conf/all/forwarding',
            f"ip -6 route add {Parameter.X1_SUBNET_V6}/64 via {Parameter.X3_IP_V6}",
            "sleep 3",
            "ip -6 r",
        ]
        output = PC3_login.send_commands(cmds)
        res["pc3"] = (
            True
            if f"{Parameter.X1_SUBNET_V6}/64 via {Parameter.X3_IP_V6}" in output
            else False
        )

        logger.info(f"configure pc ipv6 result: {res}")
        Assertion.assert_equal(
            all(res.values()), True, "ERR: Config PCs ipv6 settings failed"
        )
