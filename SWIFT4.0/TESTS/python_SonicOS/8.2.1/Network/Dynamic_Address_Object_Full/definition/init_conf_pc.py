from definition.settings import *
from definition.utils import *


class TestInit_dns_Server(Test):
    uuid = 'NonTC'

    def test_01_setup_ipv4_dns_server(self):
        flag = False
        named_conf = '/etc/named.conf'
        getfilecmds = ['service named stop',
                       f'rm -f {named_conf}.bak',
                       f'mv {named_conf} {named_conf}.bak',
                       f'\\cp -f {confs_path}named.conf /etc/',
                       f'\\cp -f {confs_path}named.ca /var/named/',
                       f'\\cp -f {confs_path}named.local /var/named/',
                       f'\\cp -f {confs_path}127.0.0.zone /var/named/',
                       f'\\cp -f {confs_path}limitFQDN.com.db /var/named/',
                       f'\\cp -f {confs_path}13.0.0.db /var/named/']
        output1 = PC2_login.send_commands(getfilecmds)
        logger.info(output1)

        startservicecmds = ["service named restart -kill",
                            "service named restart -kill",
                            "service named status"]
        output2 = PC2_login.send_commands(startservicecmds)
        logger.info(output2)
        if re.search(r'is running', output2, re.I):
            flag = True
        Assertion.assert_equal(
            flag, True, "ERR:Start dns server on PC2 failed")


class TestInit_get_PC_mac_and_linklocal(Test):
    uuid = 'NonTC'

    def test_01_get_PC1_eth0_mac(self):
        ret = False
        (Parameter.PC1_ETH0_MAC_org, Parameter.PC1_ETH0_MAC) = get_pc_mac(
            PC1_login, 'eth0')
        logger.info(
            f"ETH0 mac is {Parameter.PC1_ETH0_MAC},ETH0 orginal mac is {Parameter.PC1_ETH0_MAC_org}")
        if len(Parameter.PC1_ETH0_MAC) == 12:
            ret = True

        Assertion.assert_equal(ret, True, "ERR: Get PC1 eth0 mac failed")

    def test_02_get_PC1_eth2_mac(self):
        ret = False
        (Parameter.PC1_ETH2_MAC_org, Parameter.PC1_ETH2_MAC) = get_pc_mac(PC1_login, 'eth2')
        logger.info(
            f"ETH2 mac is {Parameter.PC1_ETH2_MAC},ETH2 orginal mac is {Parameter.PC1_ETH2_MAC_org}")
        if len(Parameter.PC1_ETH2_MAC) == 12:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get PC1 eth2 mac failed")

    def test_03_get_PC1_eth0_linklocal(self):
        ret = False
        Parameter.PC1_ETH0_LINKLOCAL = get_pc_linklocal(PC1_login, 'eth0')
        logger.info(f"ETH0 linklocal is {Parameter.PC1_ETH0_LINKLOCAL}")
        if len(Parameter.PC1_ETH0_LINKLOCAL) > 0:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get PC1 eth0 linklocal address failed")

    def test_04_get_PC1_eth2_linklocal(self):
        ret = False
        Parameter.PC1_ETH2_LINKLOCAL = get_pc_linklocal(PC1_login, 'eth2')
        logger.info(f"ETH2 linklocal is {Parameter.PC1_ETH2_LINKLOCAL}")
        if len(Parameter.PC1_ETH2_LINKLOCAL) > 0:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get PC1 eth2 linklocal address failed")

        

