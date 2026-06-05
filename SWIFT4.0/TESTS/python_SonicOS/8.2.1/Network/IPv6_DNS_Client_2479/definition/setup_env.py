from definition.init_param import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1_opt = {
            'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            "dns": {
                "primary": WAN_host,
                "secondary": "::",
                "tertiary": "::"
            },
            'adv_pref': True,
            'router_adv': True,
        }
        rc = interface_ipv6_obj.config_interface_ipv6( **x1_opt )
        Assertion.assert_equal(rc, True, "ERR: Configure X1 ipv6 Failed!")
 
    def test_02_config_IPv6_dns_server(self):
        logger.info('config IPv6 dns server...')
        flag = False
        cmds = (
            'rm -f {}'.format(dnsmasq_conf),
            'cp -f {}/dnsmasq.conf {}'.format(conf_path, dnsmasq_conf)
        )
        for cmd in cmds:
            local_host.send_command(cmd)
            logger.info('run cmd on pc1:{}'.format(cmd))

        local_host.send_command('service dnsmasq start')
        sleep(3)
        output = local_host.send_command('service dnsmasq status')
        logger.info(output)
        if re.search(r"dnsmasq .*running.*", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config IPv6 dns server failed")