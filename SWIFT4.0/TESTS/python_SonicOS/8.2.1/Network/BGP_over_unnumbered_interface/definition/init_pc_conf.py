from definition.settings import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_add_route_to_remote_x3_and_x4_subnet_on_pc2(self):
        cmds = [f'route add -net {Parameter.X3_REMOTE_NET} netmask {Parameter.MASK} gw {Parameter.X3_IP}',
                f'route add -net {Parameter.X4_REMOTE_NET} netmask {Parameter.MASK} gw {Parameter.X4_IP}',
                'ip -4 r']
        output = PC2_Login.send_commands(cmds)
        checklist = [f'{Parameter.X3_REMOTE_NET}/24 via {Parameter.X3_IP} dev eth1',
                     f'{Parameter.X4_REMOTE_NET}/24 via {Parameter.X4_IP} dev eth2'
                     ]
        flag = True if all(i in output for i in checklist) else False
        Assertion.assert_equal(flag, True, "ERR: add route to remote x3 and x4 subnet on PC2 failed")

    def test_02_add_route_to_dest_network_on_pc2_eth1(self):
        cmds = [
                f'route add -net 100.1.1.0 netmask {Parameter.MASK} gw {Parameter.X3_IP}',
                f'route add -net 173.1.1.0 netmask {Parameter.MASK} gw {Parameter.X3_IP}',
                'ip -4 r']
        output = PC2_Login.send_commands(cmds)
        checklist = [f'100.1.1.0/24 via {Parameter.X3_IP} dev eth1',
                     f'173.1.1.0/24 via {Parameter.X3_IP} dev eth1'
                     ]
        logger.info("print checklist")
        logger.info(checklist)
        flag = True if all(i in output for i in checklist) else False
        Assertion.assert_equal(flag, True, "ERR: add route to dest network on PC2 failed")

    def test_03_add_route_to_local_x3_and_x4_subnet_on_pc3(self):
        cmds = [f'route add -net {Parameter.X3_SUBNET} netmask {Parameter.MASK} gw {Parameter.X3_REMOTE_IP}',
                f'route add -net {Parameter.X4_SUBNET} netmask {Parameter.MASK} gw {Parameter.X4_REMOTE_IP}',
                'ip -4 r']
        output = PC3_Login.send_commands(cmds)
        checklist = [f'{Parameter.X3_SUBNET}/24 via {Parameter.X3_REMOTE_IP} dev eth1',
                     f'{Parameter.X4_SUBNET}/24 via {Parameter.X4_REMOTE_IP} dev eth2'
                     ]
        logger.info("print checklist")
        logger.info(checklist)
        flag = True if all(i in output for i in checklist) else False
        Assertion.assert_equal(flag, True, "ERR: add route to local x3 and x4 subnet on PC3 failed")

    def test_04_enable_ospfd_on_pc4(self):
        cmds = [
            'yum install -y quagga',
            f'cp {zebra_path} /etc/quagga/zebra.conf',
            f'cp {ospfd_path} /etc/quagga/ospfd.conf',
            'systemctl restart zebra ospfd', # ospf settings in vtysh dosn't work if restarting zebra and ospfd separately
            'systemctl status ospfd',
        ]
        output = PC4_Login.send_commands(cmds)
        flag = True if "Active: active (running)" in output else False
        Assertion.assert_equal(flag, True, "ERR:enable ospfd on pc4 failed")



