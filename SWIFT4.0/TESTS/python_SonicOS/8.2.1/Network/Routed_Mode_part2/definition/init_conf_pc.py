from definition.settings import *


class TestSetup_PCs(Test):
    uuid = "NonTC"

    def test_01_config_ipv4_route_to_pcs(self):
        res = {}
        cmd_pc1 = [
            f"ifconfig eth1 {Parameter.PC1_ETH1}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.FIREWALL}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc2 = [
            f"ifconfig eth1 {Parameter.PC2_ETH1_portshield}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.FIREWALL}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc4 = [
            f"ifconfig eth1 {Parameter.PC4_ETH1}",
            f"route add -net {PC1_ETH1_NW}/24 gw {Parameter.X1_IP}",
            f"route add -net {PC3_ETH1_NW}/24 gw {Parameter.X1_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc3 = [
            f"ifconfig eth1 {Parameter.PC3_ETH1}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X4_VLAN1_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc1 = pc1_ssh.send_commands(cmd_pc1)
        rc2 = pc2_ssh.send_commands(cmd_pc2)
        rc3 = pc4_ssh.send_commands(cmd_pc4)
        rc4 = pc3_ssh.send_commands(cmd_pc3)
        logger.info(f'run cmd result in pcs:{rc1}...{rc2}..{rc3}..{rc4}')
        res["pc1"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.FIREWALL}" in rc1
            else False
        )
        res["pc2"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.FIREWALL}" in rc2
            else False
        )
        res["pc4"] = (
            True
            if (f"{PC1_ETH1_NW}/24 via {Parameter.X1_IP}" in rc3 and f"{PC3_ETH1_NW}/24 via {Parameter.X1_IP}" in rc3)
            else False
        )
        res["pc3"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.X4_VLAN1_IP}" in rc4
            else False
        )
        logger.info(
            f'check pcs route result : {res["pc1"]}...{res["pc2"]}..{res["pc4"]}..{res["pc3"]}')
        Assertion.assert_equal(all(res.values()), True,
                               "ERR: Config PCs route failed")

    def test_02_config_ipv6_route_to_pcs(self):
        res = {}
        cmd_pc1_ipv6 = [
            f"ip -6 a a {Parameter.lan_host1}/64 dev eth1",
            f"ip -6 r a default via {Parameter.X0_IPv6} dev eth1 metric 100",
            "ip -6 r",
            "ifconfig -a",
        ]
        cmd_pc4_ipv6 = [
            f"ip -6 a a {Parameter.wan_ip}/64 dev eth1",
            f"ip -6 r a default via {Parameter.X1_IPv6} dev eth1 metric 100",
            "ip -6 r",
            "ifconfig -a",
        ]

        rc1 = pc1_ssh.send_commands(cmd_pc1_ipv6)
        rc2 = pc4_ssh.send_commands(cmd_pc4_ipv6)
        logger.info(f'run cmd result in pcs:{rc1}...{rc2}..')

        res["pc1"] = (
            True
            if f"default via {Parameter.X0_IPv6} dev eth1" in rc1
            else False
        )
        res["pc4"] = (
            True
            if f"default via {Parameter.X1_IPv6} dev eth1" in rc2
            else False
        )
        logger.info(f'check pcs route result : {res["pc1"]}..{res["pc4"]}..')
        Assertion.assert_equal(all(res.values()), True,
                               "ERR: Config PCs route failed")
