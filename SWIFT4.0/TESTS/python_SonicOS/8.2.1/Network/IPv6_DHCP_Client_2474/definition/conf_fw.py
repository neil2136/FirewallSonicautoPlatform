from definition.initial_parameter import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_00_00_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            # 'gateway': Parameter.X1_GW,
            # 'dns1': Parameter.X1_DNS_1,
            # 'dns2': Parameter.X1_DNS_2,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_01_Setup_for_Lanpc(self):
        localhost.send_command('route add -net 11.11.11.0/24 gw 192.168.168.168')
        out = localhost.send_command("route")
        # if re.search(r'11\.11\.11\.0\s+?VTB\d*-UTM', out, re.M):
        #     logger.info('add default route for pc1 successfully')
        Assertion.assert_regular(out, r'11\.11\.11\.0\s+?VTB\d*-UTM', "ERR: setup for lanpc failed")

    def test_00_02_setup_dhcpv6_server(self):
        # restore dhcpv6 server
        cmds = ['configure', 'restore-defaults']
        fw_dhcpv6_server.do_cli_commands(cmds)
        time.sleep(180)
        # config X1 Ipv4 for dhcpv6 server
        cmds = ['configure', 'interface x1', 'ip-assignment WAN static', 'ip 11.11.11.101', 'netmask 255.255.255.0',
                'commit',
                'exit', 'management https', 'management ping', 'commit', 'exit']
        rc = fw_dhcpv6_server.do_cli_commands(cmds)
        cmds = ['configure', 'administration', 'sonicos-api', 'enable', 'basic', 'commit', 'exit']
        rc &= fw_dhcpv6_server.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, "ERR: setup dhcpv6 server failed")

    def test_00_03_config_X1_DHCPV6_Server(self):
        for each in range(0, 5):
            time.sleep(10)
            if not os.system('ping 11.11.11.101 -c 1 -w 1'):
                break        
        X1_IPv6_Interface = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            "ip": dhcpv6_server_v6,
            "prefix_length": 64,
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
            'mgmt_snmp': False,
        }
        rc = interface_v6_server.config_interface_ipv6(**X1_IPv6_Interface)
        Assertion.assert_equal(rc, True, "ERR: config server X1 IPv6 failed")
