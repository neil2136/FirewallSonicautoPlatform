from definition.init_param import *


class Test_configTB_0(Test):
    uuid = 'NonTC'
    description = 'Configure FW'

    def test_0_0_config_x0_ipv6(self):
        logger.info("config x0 ipv6 interface... ")
        x0_opt = {
            'name': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.FIREWALL_IPV6,
            'prefix_length': Parameter.IPV6_PREFIXLEN,
            'mgmt_ping': True,
            'router_adv': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(rc, True, 'ERR: Configure X0 ipv6 failed!')

    def test_0_1_config_x1(self):
        x1_v4_opt = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS_1,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        rc1 = interface_v4.config_interface(**x1_v4_opt)
        x1_v6_opt = {
            'name': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IPV6,
            'prefix_length': Parameter.IPV6_PREFIXLEN,
            'mgmt_ping': True,
            'router_adv': True,
        }
        rc2 = interface_v6.config_interface_ipv6(**x1_v6_opt)
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: Configure X1 failed!')

    def test_0_2_config_x2(self):
        x2_v4_opt = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        }
        rc1 = interface_v4.config_interface(**x2_v4_opt)
        x2_v6_opt = {
            'name': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IPV6,
            'prefix_length': Parameter.DMZ_IPV6_PREFIXLEN,
            'mgmt_ping': True,
            'router_adv': True,
        }
        rc2 = interface_v6.config_interface_ipv6(**x2_v6_opt)
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: Configure X2 failed!')



class Test_configTB_1(Test):
    uuid = 'NonTC'
    description = 'Configure PC'

    def test_1_0_setup_PC1(self):
        logger.info(" --------set PC1's IPV6 route information-------------------------------------------")
        cmd = 'ip -6 route add {}/96 via {} dev {}'.format(Parameter.DEST_NETWORK, Parameter.FIREWALL_IPV6, Parameter.PC1_IF)
        localhost.send_command(cmd)
        rc = localhost.send_command('ip -6 route show dev {}'.format(Parameter.PC1_IF))
        Assertion.assert_regular(rc, r'{}'.format(Parameter.DEST_NETWORK), 'ERR: Setup PC1 failed!')

    def test_1_1_setup_PC2(self):
        logger.info(" --------set PC2's IPV6 route information-------------------------------------------")
        cmd = 'ip -6 route add {}/96 via {} dev {}'.format(Parameter.DMZ_PREFIX, Parameter.X1_IPV6, Parameter.PC2_IF)
        pc2_ssh.send_command(cmd)
        rc = pc2_ssh.send_command('ip -6 route show dev {}'.format(Parameter.PC2_IF))
        Assertion.assert_regular(rc, r'{}'.format(Parameter.DMZ_PREFIX), 'ERR: Setup PC2 failed!')

    def test_1_2_setup_PC3(self):
        logger.info(" --------set PC3's IPV6 route information-------------------------------------------")
        cmd = 'ip -6 route add {}/96 via {} dev {}'.format(Parameter.DEST_NETWORK, Parameter.X2_IPV6, Parameter.PC3_IF)
        pc3_ssh.send_command(cmd)
        rc = pc3_ssh.send_command('ip -6 route show dev {}'.format(Parameter.PC3_IF))
        Assertion.assert_regular(rc, r'{}'.format(Parameter.DEST_NETWORK), 'ERR: Setup PC3 failed!')