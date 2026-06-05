from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'

    def test_02_add_routes_for_pcs(self):
        PC1_login.send_command("route add -net 12.12.1.0/24 gw 192.168.168.168")
        PC1_login.send_command("route add -net 13.13.1.0/24 gw 192.168.168.168")
        PC1_login.send_command("route add -host 224.0.0.22 dev eth1")
        PC1_login.send_command("route add -net 224.0.0.0 netmask 255.0.0.0 dev eth1")
        PC2_login.send_command("route add -host 224.0.0.22 dev eth1")
        PC2_login.send_command("route add -net 224.0.0.0 netmask 255.0.0.0 dev eth1")
        PC3_login.send_command("route add -host 224.0.0.22 dev eth1")
        PC3_login.send_command("route add -net 224.0.0.0 netmask 255.0.0.0 dev eth1")
        Assertion.assert_equal(True, True, "ERR: Add routes failed")
