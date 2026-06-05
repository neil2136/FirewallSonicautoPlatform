from definition.init_param import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_x0(self):
        logger.info("config x0 interface... ")
        x0_opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPv6,
            'managed': True,
            'other_config': True,
            'router_adv': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x0_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X0 ipv6 Failed!")
 
    def test_02_delete_eth1_network_scripts(self):
        logger.info('delete eth1 network scripts...')
        flag = False
        cmds = (
            'rm -rf /etc/sysconfig/network-scripts/ifcfg-eth1',
            'rm -rf /etc/sysconfig/network-scripts/route-eth1',
        )
        for cmd in cmds:
            logger.info('run cmd on pc:{}'.format(cmd))
            local_host.send_command(cmd)

        output = local_host.send_command('ls -l /etc/sysconfig/network-scripts')
        if not re.search(r".*eth1.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: delete eth1 network scripts failed")