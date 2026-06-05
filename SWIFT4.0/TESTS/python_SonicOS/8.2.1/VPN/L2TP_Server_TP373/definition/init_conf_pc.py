from definition.settings import *


class TestSetupForPC(Test):
    uuid = 'NonTC'
    pc_login = PC4_Login
    pc_path = 'pc4'

    def test_01_config_strongswan_and_xl2tpd_in_PC4(self):
        rmcmds = [
            "mv /etc/strongswan/ipsec.conf /tmp/",
            "mv /etc/strongswan/ipsec.secrets /tmp/",
            "mv /etc/xl2tpd/xl2tpd.conf /tmp/"
        ]
        rmres = self.pc_login.send_commands(rmcmds)
        logger.info('Remove old config file: {}'.format( rmres))

        scriptspath = defi_path + f'/conf_files/{self.pc_path}/'
        cpcmds = [
            f"cp -a {scriptspath}ipsec.conf /etc/strongswan/",
            f"cp -a {scriptspath}ipsec.secrets /etc/strongswan/",
            f"cp -a {scriptspath}xl2tpd.conf /etc/xl2tpd/",
            f"cp -a {scriptspath}options.xl2tpd.client /etc/ppp/"
        ]
        cpres = self.pc_login.send_commands(cpcmds )
        logger.info('Copy config file : {}'.format(cpres))

        strongswancmds = [
            "systemctl start strongswan",
            "systemctl status strongswan"
        ]
        strongswanres = self.pc_login.send_commands(strongswancmds)
        logger.info('start srongswan: {}'.format(strongswanres))
        if re.search(r'Active: active \(running\)', str(strongswanres), re.I | re.M | re.DOTALL):
            flag1 = True
        else:
            flag1 = False
        logger.info('check status of srongswan: {}'.format(flag1))

        xl2tpdcmds = [
            'systemctl start xl2tpd',
            'mkdir -p /var/run/xl2tpd',
            'touch /var/run/xl2tpd/l2tp-control',
            "systemctl status xl2tpd",
        ]
        xl2tpdres = self.pc_login.send_commands(xl2tpdcmds)
        logger.info('start xl2tpd: {}'.format(xl2tpdres))
        if re.search(r'Active: active \(running\)', str(xl2tpdres), re.I | re.M | re.DOTALL):
            flag2 = True
        else:
            flag2 = False
        logger.info('check status of xl2tpd: {}'.format(flag2))

        Assertion.assert_equal(flag1 & flag2, True, "ERR: configure and start strongswan and xl2tpd failed")

    def test_02_config_strongswan_and_xl2tpd_in_PC3(self):
        self.pc_login = PC3_Login
        self.pc_path = 'pc3'
        self.test_01_config_strongswan_and_xl2tpd_in_PC4()

    def test_03_add_route_in_PC4(self):
        routecmds = ["route add -host 12.12.1.168 gw 12.12.2.101 dev eth1",
                     "ip -4 r"]
        routeres = PC4_Login.send_commands(routecmds)
        logger.info('add router from interface behind NAT: {}'.format(routeres))
        routecheck1 = f'{Parameter.X1_IP} via {Parameter.GW_X2_IP}'
        logger.info(routecheck1)
        flag = True if routecheck1 in routeres else False
        Assertion.assert_equal(flag, True, "ERR: Add  route on pc4 failed")











