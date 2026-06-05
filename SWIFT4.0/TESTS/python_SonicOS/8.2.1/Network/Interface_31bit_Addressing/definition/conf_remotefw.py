from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_config_dut1_x2_to_wan(self):
        res = interfacev4api.config_interface(**x2_static_dict)
        logger.info('config X2 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X2 to static wan failed")

    def test_02_init_remote_dut2_conf(self):
        logger.info(" {} ".center(20, '-').format('Restore Remote FW.'))
        command1 = f'python3 {remote_conf_path} ' \
                   f'-os=1 --testbed={Params.testbed} ' \
                   f'-device=RemoteGEN5 -if=X1 -zone=WAN ' \
                   f'-ip={Parameter.X1_REMOTE_IP} -restore=1'
        confres = PC1_login.send_command(command1)
        logger.info(confres)

        logger.info("add a route to interface X2 sub... ")
        command2 = f'route add -net {Parameter.X2_NET}/24 gw {Parameter.FIREWALL}'
        routeres = PC1_login.send_command(command2)
        logger.info('add x2 sub route in PC1 result: {}'.format(routeres))

        pingres = PC1_login.ping_from_eth(
            ip=Parameter.X1_REMOTE_IP, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: config Remote FW failed")

    def test_03_configure_remote_interface(self):
        logger.info(" {} ".center(20, '-').format('Configure remote Interface x2'))
        command = [
            'configure',
            'interface x2',
            'ip-assignment WAN static',
            'ip 172.16.2.101 netmask 255.255.255.0',
            'gateway 172.16.2.1',
            'dns primary {}'.format(Parameter.X1_DNS1),
            'dns secondary {}'.format(Parameter.X1_DNS2),
            'commit', 'end', 'exit'
        ]
        (res, output) = dut2_cli.do_cli_commands(command, 1)
        if 'Error' not in output:
            logger.info('Configure X2 Success!')
        Assertion.assert_equal(res, True, "ERR: Configure remote Interface failed")

    def test_04_configure_remote_failover(self):
        tag = False
        logger.info(" {} ".center(20, '-').format('Configure remote Failover-LB'))
        time.sleep(5)
        command = [
            'configure',
            'failover-lb',
            'group \ Default\ LB\ Group',
            'interface X2',
            'rank 1',
            'exit', 'commit', 'end', 'exit'
        ]
        (res, output) = dut2_cli.do_cli_commands(command, 1)
        if 'Error' not in output:
            logger.info('Configure remote LB Success!')
            tag = True
        Assertion.assert_equal(tag, True, "ERR: Configure remote Failover-LB failed")

    # def test_05_register_remote_dut2(self):
    #     logger.info(" {} ".center(20, '-').format('Register Remote fw'))
    #     tag = False
    #     for i in range(6):
    #         logger.info(f'Run for {i+1} time')
    #         cmd = f'/SWIFT4.0/COMMON/bin/fwRegister.pl -d {Parameter.X1_REMOTE_IP}'
    #         output = PC1_login.send_command(cmd)
    #         if 'Register successful' in output:
    #             tag = True
    #             logger.info('Register successful!')
    #             break
    #         else:
    #             time.sleep(10)
    #     Assertion.assert_equal(tag, True, "ERR: Register Remote fw failed")

    def test_06_set_router_mode_to_advanced_and_enable_bgp(self):
        logger.info(" {} ".center(20, '-').format('Set Router mode to advanced and Enable BGP'))
        opt = {
            'advanced': True,
            'BGP': True
        }
        res = dynroutingapi.set_advanced_routing_mode(**opt)
        res &= dynroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res, True, "ERR: Set router mode and enable BGP failed")