from definition.settings import *


class Test_configTB(Test):
    uuid = 'NonTC'
    description = 'Configure TB'
    jira = 'GEN7-31901'

    # on remote PC -- PC2
    # 1. add route
    # 2. Restart dhcp
    def test_00_01_add_route_in_PC2(self):
        pc2_ssh.send_command('route add -net 192.168.168.0/24 gw {}'.format(Parameter.X2_DMZ_IP))  # PC1 Client
        out = pc2_ssh.send_command('route -n')
        pc2_ssh.send_command('exit')
        Assertion.assert_regular(out, r'2.2.2.100', "ERR: Add route for remote pc2 failed!")

    def test_00_02_restart_dhcp_on_pc2(self):
        # config dhcpd.conf
        pc2_ssh.send_command("\cp -f {}/conf/dhcpd.conf  /etc/dhcp/dhcpd.conf".format(testpath))
        out = pc2_ssh.send_command("service dhcpd restart")
        pc2_ssh.send_command('exit')
        Assertion.assert_regular(out, r'OK', "ERR: Restart DHCP service on remote PC2 failed!")

    # on UTM:
    # 1. Disable DHCP server
    # 2. Enable IP Helper
    # 3. Enable DHCP ip helper protocol
    def test_00_03_disable_dhcp_server(self):
        dhcp_server_opt = {
            "dhcp_server": {
                "ipv4": {
                    "enable": False
                    , "conflict_detection": True
                    , "persistence": True
                    , "persistence_monitoring_interval": 5
                    , "trusted_relay_agents": ""
                    , "recycle_expired_lease": 0
                }
            }
        }
        rc = dhcp_obj.config_dhcp_server_settings(**dhcp_server_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp server on fw failed!")

    def test_00_04_enable_iphelper(self):
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper failed!")

    def test_00_05_enable_dhcp_protocol(self):
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp protocol failed!")
