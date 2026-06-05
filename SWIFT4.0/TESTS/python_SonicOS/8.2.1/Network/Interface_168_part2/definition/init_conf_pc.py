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
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X4_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc4 = [
            f"ifconfig eth1 {Parameter.PC4_ETH1}",
            f"route add -net {PC1_ETH1_NW}/24 gw {Parameter.X1_IP}",
            f"route add -net {PC3_ETH1_NW}/24 gw {Parameter.X1_IP}",
            f"route add -net 12.12.2.0/24 gw {Parameter.X1_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc3 = [
            f"ifconfig eth1 {Parameter.PC3_ETH1}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X4_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        cmd_pc5 = [
            f"ifconfig eth1 {Parameter.PC5_ETH1}",
            f"route add -net {PC4_ETH1_NW}/24 gw {Parameter.X3_IP}",
            "ip -4 r",
            "ifconfig -a",
        ]
        rc1 = pc1_ssh.send_commands(cmd_pc1)
        rc2 = pc2_ssh.send_commands(cmd_pc2)
        rc3 = pc4_ssh.send_commands(cmd_pc4)
        rc4 = pc3_ssh.send_commands(cmd_pc3)
        rc5 = pc5_ssh.send_commands(cmd_pc5)
        logger.info(f'run cmd result in pcs:{rc1}...{rc2}..{rc3}..{rc4}..{rc5}')
        res["pc1"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.FIREWALL}" in rc1
            else False
        )
        res["pc2"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.X4_IP}" in rc2
            else False
        )
        res["pc4"] = (
            True
            if (f"{PC1_ETH1_NW}/24 via {Parameter.X1_IP}" in rc3 and f"{PC3_ETH1_NW}/24 via {Parameter.X1_IP}" in rc3)
            else False
        )
        res["pc3"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.X4_IP}" in rc4
            else False
        )
        res["pc5"] = (
            True
            if f"{PC4_ETH1_NW}/24 via {Parameter.X3_IP}" in rc5
            else False
        )
        logger.info(
            f'check pcs route result : {res["pc1"]}...{res["pc2"]}..{res["pc4"]}..{res["pc3"]}..{res["pc5"]}')
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

    @repeat_method(5)
    def test_03_Setup_dhcp_server_on_pc4(self):
        flag = False
        conf_file = CONF_PATH + '/dhcpd.conf';
        ret = pc4_ssh.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
        ret = ret + pc4_ssh.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
        ret = ret + pc4_ssh.send_command("service dhcpd restart")
        logger.info(ret)
        status = pc4_ssh.send_command("service dhcpd status")
        logger.info(status)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC4 failed")

    def test_04_pppoe_server_setup_on_pc4(self):
        logger.info('start pppoe server...')
        res = pc4_ssh.start_PPPoE_server(
            interface=PPPoeParams.PPPOE_IF,
            local_ip=PPPoeParams.LOCAL_IP,
            assign_ip=PPPoeParams.PPPOE_ASSIGN,
            ppp_secrets=PPPoeParams.PPP_SECRETS,
            pppoe_option=PPPoeParams.PPPOE_OPTIONS,
        )
        Assertion.assert_equal(res, True, "ERR: Start PPPoE Server on PC4 failed")

    def test_05_pptp_server_setup_on_pc4(self):
        logger.info('start pptp server...')
        flag = False
        backup_cmd_pc4 = [
            f"mv /etc/pptpd.conf /etc/pptpd.conf.bak",
            f"mv /etc/ppp/options.pptpd /etc/ppp/options.pptpd.bak",
            f"mv /etc/ppp/pap-secrets /etc/ppp/pap-secrets.bak",
        ]
        pc4_ssh.send_commands(backup_cmd_pc4)
        start_cmd_pc4 = [
            f"cp {suite_path}definition/conf/pptp/options.pptpd  /etc/ppp/options.pptpd",
            f"cp {suite_path}definition/conf/pptp/pptpd.conf  /etc/pptpd.conf",
             f"cp {suite_path}definition/conf/pptp/pap-secrets  /etc/ppp/pap-secrets",
            "service pptpd stop",
            "service pptpd start",
            "service pptpd status",
        ]
        status = pc4_ssh.send_commands(start_cmd_pc4)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start pptp server on PC4 failed")

    def test_06_l2tp_server_setup_on_pc4(self):
        logger.info('start l2tp server...')
        flag = False
        backup_cmd_pc4 = [
            f"mv /etc/xl2tpd/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf.bak",
        ]
        pc4_ssh.send_commands(backup_cmd_pc4)
        start_cmd_pc4 = [
            f"cp {suite_path}definition/conf/l2tp/xl2tpd.conf  /etc/xl2tpd/xl2tpd.conf",
            "service xl2tpd stop",
            "service xl2tpd start",
            "service xl2tpd status",
        ]
        status = pc4_ssh.send_commands(start_cmd_pc4)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start l2tp server on PC4 failed")

    @repeat_method(5)
    def test_07_Setup_dhcp_server_on_pc5(self):
        flag = False
        conf_file = CONF_PATH + '/dhcpd_x3.conf';
        ret = pc5_ssh.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
        ret = ret + pc5_ssh.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
        ret = ret + pc5_ssh.send_command("service dhcpd restart")
        logger.info(ret)
        status = pc5_ssh.send_command("service dhcpd status")
        logger.info(status)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC5 failed")

    def test_08_pppoe_server_setup_on_pc5(self):
        logger.info('start pppoe server...')
        res = pc5_ssh.start_PPPoE_server(
            interface=PPPoeParams_x3.PPPOE_IF,
            local_ip=PPPoeParams_x3.LOCAL_IP,
            assign_ip=PPPoeParams_x3.PPPOE_ASSIGN,
            ppp_secrets=PPPoeParams_x3.PPP_SECRETS,
            pppoe_option=PPPoeParams_x3.PPPOE_OPTIONS,
        )
        Assertion.assert_equal(res, True, "ERR: Start PPPoE Server on PC5 failed")

    def test_09_pptp_server_setup_on_pc5(self):
        logger.info('start pptp server...')
        flag = False
        backup_cmd_pc5 = [
            f"mv /etc/pptpd.conf /etc/pptpd.conf.bak",
            f"mv /etc/ppp/options.pptpd /etc/ppp/options.pptpd.bak",
            f"mv /etc/ppp/pap-secrets /etc/ppp/pap-secrets.bak",
        ]
        pc5_ssh.send_commands(backup_cmd_pc5)
        start_cmd_pc5 = [
            f"cp {suite_path}definition/conf/pptp/options.pptpd  /etc/ppp/options.pptpd",
            f"cp {suite_path}definition/conf/pptp/pptpd.conf  /etc/pptpd_x3.conf",
             f"cp {suite_path}definition/conf/pptp/pap-secrets  /etc/ppp/pap-secrets",
            "service pptpd stop",
            "service pptpd start",
            "service pptpd status",
        ]
        status = pc5_ssh.send_commands(start_cmd_pc5)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start pptp server on PC5 failed")

    def test_10_l2tp_server_setup_on_pc5(self):
        logger.info('start l2tp server...')
        flag = False
        backup_cmd_pc5 = [
            f"mv /etc/xl2tpd/xl2tpd.conf /etc/xl2tpd/xl2tpd.conf.bak",
        ]
        pc5_ssh.send_commands(backup_cmd_pc5)
        start_cmd_pc5 = [
            f"cp {suite_path}definition/conf/l2tp/xl2tpd_x3.conf  /etc/xl2tpd/xl2tpd.conf",
            "service xl2tpd stop",
            "service xl2tpd start",
            "service xl2tpd status",
        ]
        status = pc5_ssh.send_commands(start_cmd_pc5)
        if re.search(r'Active: active \(running\)', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Start l2tp server on PC5 failed")
