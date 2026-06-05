from definition.settings import *

class Test_01_site_to_site_vpn(Test):
    uuid = "SOSAIOT-TC-48506"
    description = 'add site_to_site vpn via cli'

    def test_01_Step00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '1')

    def test_01_Step01_add_s2s_vpn(self):
        cmds = ['configure',
                'address-object ipv4 rm_net',
                'network 12.12.1.0 255.255.255.0',
                'commit', 
                'exit']
        rc1 = fw_cli.do_cli_commands(cmds)
        cmds = ['configure',
                'vpn policy site-to-site vpn1',
                'auth-method shared-secret',
                'shared-secret 123456',
                'exit',
                'gateway primary 1.1.1.1',
                'network local name "X0 Subnet"',
                'network remote destination-network name rm_net',
                'commit',
                'exit',
            ]
        rc2 = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc1&rc2, True, "ERR: add s2s vpn via cli failed")

    def test_01_Step02_check_s2s_vpn(self):
        cmds = ['show vpn policy ipv4 site-to-site vpn1']
        rc, output = fw_cli.do_cli_commands(cmds, tag=1)
        result = True
        match_strs = ['vpn policy site-to-site vpn1',
                    'auth-method shared-secret',
                    'gateway primary 1.1.1.1',
                    'network local name "X0 Subnet"',
                    'network remote destination-network name rm_net',
                    ]
        for match_str in match_strs:
            if re.search(match_str, output, re.M):
                result = result & True
            else:
                result = result & False
                logger.error("cannot find correct cli config for {}".format(match_str))
        Assertion.assert_equal(result, True, "ERR: check s2s vpn by cli failed")


class Test_02_site_to_group_vpn(Test):
    uuid = "SOSAIOT-TC-48507"
    description = 'add group vpn via cli'

    def test_02_Step00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '2')

    def test_02_Step01_add_group_vpn(self):
        cmds = ['configure',
                'vpn policy group-vpn "WAN GroupVPN"',
                'enable',
                'auth-method shared-secret',
                'shared-secret 123456',
                'exit',
                'client allow-connections-to all-secured-gateways',
                'client cache-xauth always',
                'client virtual-adaptor dhcp-only',
                'client default-route',
                'client access-list',
                'client simple-provisioning',
                'client-authentication allow-unauthenticated name rm_net',
                'commit',
                'exit',
                ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: add group vpn via cli failed")

    def test_02_Step02_check_group_vpn(self):
        cmds = ['show vpn policy ipv4 group-vpn "WAN GroupVPN"']
        rc, output = fw_cli.do_cli_commands(cmds, tag=1)
        result = True
        match_strs = [
                    'vpn policy group-vpn "WAN GroupVPN"',
                    'enable',
                    'auth-method shared-secret',
                    'client allow-connections-to all-secured-gateways',
                    'client cache-xauth always',
                    'client virtual-adaptor dhcp-only',
                    'client default-route',
                    'client access-list',
                    'client simple-provisioning',
                    'client-authentication allow-unauthenticated name rm_net',
                ]
        for match_str in match_strs:
            if re.search(match_str, output, re.M):
                result = result & True
            else:
                result = result & False
                logger.error("cannot find correct config for {}".format(match_str))
        Assertion.assert_equal(result, True, "ERR: check group vpn by cli failed")


class Test_03_tunnel_vpn(Test):
    uuid = "SOSAIOT-TC-48508"
    description = 'add tunnel vpn via cli'

    def test_03_Step00_Show_Test_Plan(self):
        show_testcase_info(Parameter.TESTPLAN, '3')

    def test_03_Step01_add_tunnel_vpn(self):
        cmds = ['configure',
                'vpn policy tunnel-interface vpn2',
                'gateway primary 12.12.2.201',
                'auth-method shared-secret',
                'shared-secret 123456',
                'ike-id local ipv4 1.1.1.1',
                'ike-id peer ipv4 2.2.2.2',
                'exit',
                'no netbios',
                'no anti-replay',
                # 'permit-acceleration',
                # 'multicast',
                'management https',
                'management ssh',
                'management snmp',
                'keep-alive',
                'allow-sonicpointn-layer3',
                'user-login http',
                'user-login https',
                'bound-to interface X1',
                'suppress-trigger-packet',
                'accept-hash',
                'no send-hash',
                'apply-nat',
                'advanced-routing',
                'commit',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: add tunnel vpn via cli failed")

    def test_03_Step02_check_tunnel_vpn(self):
        cmds = ['show vpn policy ipv4 tunnel-interface vpn2']
        rc, output = fw_cli.do_cli_commands(cmds, tag=1)
        result = True
        match_strs = [
                    'vpn policy tunnel-interface vpn2',
                    'gateway primary 12.12.2.201',
                    'auth-method shared-secret',
                    'ike-id local ipv4 1.1.1.1',
                    'ike-id peer ipv4 2.2.2.2',
                    'no netbios',
                    'no anti-replay',
                    # 'permit-acceleration',
                    # 'multicast',
                    'management https',
                    'management ssh',
                    'management snmp',
                    'keep-alive',
                    'allow-sonicpointn-layer3',
                    'user-login http',
                    'user-login https',
                    'bound-to interface X1',
                    'suppress-trigger-packet',
                    'accept-hash',
                    'no send-hash',
                    'apply-nat',
                    'advanced-routing',
                ]
        for match_str in match_strs:
            if re.search(match_str, output, re.M):
                result = result & True
            else:
                result = result & False
                logger.error("cannot find correct cli config for {}".format(match_str))
        Assertion.assert_equal(result, True, "ERR: check tunnel vpn by cli failed")
