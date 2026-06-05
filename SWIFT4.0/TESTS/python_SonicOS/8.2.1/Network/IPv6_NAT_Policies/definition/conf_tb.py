from definition.initial_param import *
from lib.utils import *


class Test_ConfigTB(Test):
    uuid = 'NonTC'
    description = 'Configure Test Bed'

    # UTM
    def test_00_01_config_x0_ipv6(self):
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IP,
            'mgmt_ping': True,
            'mgmt_ssh': True
        }
        out = interface_v6.config_interface_ipv6(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 ipv6 failed!")

    def test_00_02_config_pc1_ipv6_route(self):
        # delete default ipv6 route
        delete_default_ipv6_route()
        # config ipv6 route
        cmd = "ip -6 r a default via {} dev {} metric 100".format(Parameter.X0_IP, Parameter.lan_host1_if)
        rc = localhost.send_command(cmd)
        Assertion.assert_equal(rc, '', "ERR: Configure ipv6 address route on PC1 failed!")

    def test_00_03_config_pc2_ipv6_route(self):
        rc = pc2_ssh.send_command("ip -6 r a default via {} dev {} metric 100".format(Parameter.X1_IP, Parameter.wan_host1_if))
        Assertion.assert_equal(rc, '', "ERR: Configure ipv6 address route on PC2 failed!")



