from definition.settings import *


class Testsetup_network(Test):
    uuid = 'NonTC'
    description = "setup network"
    # goto_teardown = True

    def test_00_00_define_global_net(self):
        global dut_x0, rm_x0, dut_x0_net, rm_x0_net,\
            rm_x1_net, rm_x2_net, route_eth0_path
        dut_x0 = '192.168.168.168'
        rm_x0 = '172.16.1.101'
        dut_x0_net = '192.168.168.0'
        rm_x0_net = '172.16.1.0'
        rm_x1_net = '12.12.1.0'
        rm_x2_net = '12.12.2.0'
        route_eth0_path = '/etc/sysconfig/network-scripts/route-eth0'
        Assertion.assert_equal(True, True, 'Define golobal net params Failed.')

    def test_00_01_add_route_in_pc1(self):
        logger.info('add route in PC1')
        route_list = [
            'route add -net {}/24 gw {}'.format(rm_x0_net, dut_x0),
            'route add -net {}/24 gw {}'.format(rm_x1_net, dut_x0),
            'route add -net {}/24 gw {}'.format(rm_x2_net, dut_x0),
            'echo \"{}/24 via {} dev eth0\" > {}'.format(rm_x0_net, dut_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(rm_x1_net, dut_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(rm_x2_net, dut_x0, route_eth0_path),
        ]
        for route_cmd in route_list:
            os.popen(route_cmd).read()
        resp = os.popen('route -n').read()
        reg1 = re.search('{}\s+{}'.format(rm_x0_net, dut_x0), str(resp), re.I|re.M)
        reg2 = re.search('{}\s+{}'.format(rm_x1_net, dut_x0), str(resp), re.I|re.M)
        reg3 = re.search('{}\s+{}'.format(rm_x2_net, dut_x0), str(resp), re.I|re.M)
        if reg1 and reg2 and reg3:
            rc = True
        else:
            rc = False
            logger.info('route_info:\n{}'.format(resp))
        Assertion.assert_equal(rc, True, 'Add Route in PC1 Failed.')

    def test_00_02_add_route_in_pc2(self):
        logger.info('add route in PC2')
        route_list = [
            'route add -net {}/24 gw {}'.format(dut_x0_net, rm_x0),
            'route add -net {}/24 gw {}'.format(rm_x1_net, rm_x0),
            'route add -net {}/24 gw {}'.format(rm_x2_net, rm_x0),
            'echo \"{}/24 via {} dev eth0\" > {}'.format(dut_x0_net, rm_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(rm_x1_net, rm_x0, route_eth0_path),
            'echo \"{}/24 via {} dev eth0\" >> {}'.format(rm_x2_net, rm_x0, route_eth0_path),
        ]
        for route_cmd in route_list:
            PC2_login.send_command(route_cmd)
        resp = PC2_login.send_command('route -n')
        reg1 = re.search('{}\s+{}'.format(dut_x0_net, rm_x0), str(resp), re.I|re.M)
        reg2 = re.search('{}\s+{}'.format(rm_x1_net, rm_x0), str(resp), re.I|re.M)
        reg3 = re.search('{}\s+{}'.format(rm_x2_net, rm_x0), str(resp), re.I|re.M)
        if reg1 and reg2 and reg3:
            rc = True
        else:
            rc = False
            logger.info('route_info:\n{}'.format(resp))
        Assertion.assert_equal(rc, True, 'Add Route in PC2 Failed.')
