from definition.settings import *


class TestSetup_PCs(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_add_ipv6_lan_pc2(self):
        logger.info(f"Add IPv6 IP = {PC2_ETH2_IP_V6}/64 for PC2 ETH2.")
        cmds = [f"ip -6 addr add {PC2_ETH2_IP_V6}/64 dev eth2", "ifconfig eth2"]
        out = PC2_login.send_commands(cmds)
        res = f"inet6 {PC2_ETH2_IP_V6}  prefixlen 64" in out
        Assertion.assert_equal(res, True, "ERR: setup PC2 ipv6 failed.")

    def test_02_add_ipv6_lan_pc3(self):
        logger.info(f"Add IPv6 IP = {PC3_ETH2_IP_V6}/64 for PC3 ETH2.")
        cmds = [f"ip -6 addr add {PC3_ETH2_IP_V6}/64 dev eth2", "ifconfig eth2"]
        out = PC3_login.send_commands(cmds)
        res = f"inet6 {PC3_ETH2_IP_V6}  prefixlen 64" in out
        Assertion.assert_equal(res, True, "ERR: setup PC3 ipv6 failed.")

    def test_03_set_pcs_route_v4(self):
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

        logger.info(f"Set PCs route results: {results}")
        Assertion.assert_equal(
            all(results.values()), True, "ERR: Config PCs route settings failed"
        )

    def test_04_set_pcs_route_v6(self):
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
        logger.info(f"configure pc ipv6 result: {res}")
        Assertion.assert_equal(
            all(res.values()), True, "ERR: Config PCs ipv6 settings failed"
        )

    def test_05_dns_server_setup(self):
        cmds = [
            "cp -f /etc/dnsmasq.conf /etc/dnsmasq.conf.bak",
            f"cp -f {CONF_PATH}/dnsserver/*.* /etc",
            "systemctl restart dnsmasq",
            "systemctl status dnsmasq",
        ]
        output = PC3_login.send_commands(cmds)
        Assertion.assert_regular(
            output, "running", "ERR: Config dns server in WAN PC failed"
        )
