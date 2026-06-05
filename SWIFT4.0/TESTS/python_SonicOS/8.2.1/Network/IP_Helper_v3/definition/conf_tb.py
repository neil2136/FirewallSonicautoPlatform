from definition.initial_param import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial TB"

    def test_00_config_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.WAN_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.WAN_GW,
            'dns1': Parameter.WAN_DNS1,
        }
        rc = interface.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_01_add_addrobj(self):
        obj = {
            'object_type': 'host',
            'name': 'WAN Host',
            'zone': 'WAN',
            'value': Parameter.PC2_WAN_IP,
        }
        rc = address_obj.config_addressobject(**obj)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add WAN Host Address Object")

    def test_02_config_dhcp_file_in_pc2(self):
        # config dhcpd.conf
        rc1 = pc2_ssh.send_command("\cp -f {}/confs/dhcp.conf /etc/dhcp/dhcpd.conf".format(TEST_PATH))
        # exit
        rc2 = pc2_ssh.send_command('exit')
        Assertion.assert_equal(rc1+rc2, '', "ERR: Configure DHCP file in PC2 failed!")

    def test_03_add_route_in_pc2(self):
        pc2_ssh.send_command('route add -net 192.168.168.0/24 gw {}'.format(Parameter.WAN_IP))
        out = pc2_ssh.send_command('route -n')
        pc2_ssh.send_command('exit')
        Assertion.assert_regular(out, r'13.0.0.168', "ERR: Add route for remote pc2 failed!")

    def test_04_disable_dhcp_server(self):
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
