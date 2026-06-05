__author__ = 'CHU'
from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_00_configure_local_interface(self):
        logger.info(" {} ".center(20, '-').format('Configure DUT Interface'))
        rc = interface.config_interface(**Parameter.dut_x0)
        rc &= interface.config_interface(**Parameter.dut_x1)
        rc &= interface.add_interface(**Parameter.dut_x3_sub)
        Assertion.assert_equal(rc, True, "ERR: Config interfaces failed")

    @unittest.skipIf(Params.product!='TZ80-PROTOTYPE','skip register edit if not TZ80-PROTOTYPE')
    @repeat_method(5)
    def test_00_01_register(self):
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register firewall failed")

    def test_00_02_restore_remote(self):
        logger.info(" {} ".center(20, '-').format('Restore Remote'))
        path = Parameter.cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN5 -if=X1 -zone=WAN -ip=12.12.1.201  -restore=1'.format(
            path, Params.testbed)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        logger.info('time sleep 10 sec.')
        time.sleep(10)

    def test_00_03_configure_remote_interface(self):
        logger.info(" {} ".center(20, '-').format('Configure remote Interface'))
        commands1 = [
            'configure',
            'dns server inherit',
            'interface x2',
            'ip-assignment WAN static',
            'ip 172.16.2.101 netmask 255.255.255.0',
            'gateway 172.16.2.1',
            'dns primary {}'.format(G_DNS1),
            'dns secondary {}'.format(G_DNS2),
            'commit', 'end', 'exit'
        ]
        (rc1, output1) = cl2.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Configure X2 Success!')

        commands2 = [
            'configure',
            'interface x3 vlan {}'.format(RT_X3_VLAN_ID),
            'ip-assignment WAN static',
            'ip 12.12.2.201 netmask 255.255.255.0 ',
            'gateway 12.12.2.1',
            'commit', 'end', 'exit'
        ]
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output2:
            logger.info('Configure X3_sub Success!')
        rc = rc1 & rc2
        Assertion.assert_equal(rc, True, "ERR: Configure remote Interface failed")

    def test_00_04_configure_remote_failover(self):
        logger.info(" {} ".center(20, '-').format('Configure remote Failover-LB'))
        time.sleep(5)
        commands = [
            'configure',
            'failover-lb',
            'group \ Default\ LB\ Group',
            'interface X1',
            'rank 2',
            'exit',
            'interface X2',
            'rank 1',
            'exit','commit', 'end', 'exit'
        ]
        (rc, output) = cl2.do_cli_commands(commands, 1)
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: Configure remote Failover-LB failed")

    def test_00_05_configure_dut_failover(self):
        logger.info(" {} ".center(20, '-').format('Enable Load Balancing'))
        rc = failover.config_failover_settings(**Parameter.lb_opt_en)

        logger.info(" {} ".center(20, '-').format('Config probe monitoring for X1'))
        rc &= failover.config_failover_groups(**Parameter.probe_cfg)
        Assertion.assert_equal(rc, True, "ERR: Config DUT failover failed")
        
    # advanced routing needn't register on gen7
    # def test_00_06_register_remote(self):
    #     logger.info(" {} ".center(20, '-').format('Register Remote fw'))
    #     rc = False
    #     for i in range(5):
    #         logger.info('Run for {} time'.format(i+1))
    #         cmd = '/SWIFT4.0/COMMON/bin/fwRegister.pl -d {}'.format(Parameter.RT_IP['X1'])
    #         out = os.popen(cmd).read()
    #         if 'Register successful' in out:
    #             rc = True
    #             logger.info('Register successful!')
    #             break
    #         elif i == 4:
    #             rc = False
    #             logger.info('Register failed!')
    #             logger.info(out)
    #     Assertion.assert_equal(rc, True, "ERR: Register Remote fw failed")

    def test_00_07_set_router_mode_to_advanced_and_enable_bgp(self):
        logger.info(" {} ".center(20, '-').format('Set Router mode to advanced and Enable BGP'))
        opt = {
            'advanced'  : True,
            'BGP'       : True
        }
        rc = dyn_route.set_advanced_routing_mode(**opt)
        rc &= dyn_route.set_BGP(**opt)
        Assertion.assert_equal(rc, True, "ERR: Set router mode and enable BGP failed")

    def test_00_08_disable_load_balancing(self):
        logger.info(" {} ".center(20, '-').format('Disable DUT Load Balancing'))
        opt = copy.deepcopy(Parameter.lb_opt_en)
        opt['enable'] = False
        rc = failover.config_failover_settings(**opt)
        Assertion.assert_equal(rc, True, "ERR: Disable DUT Load Balancing failed")

    def test_00_09_sleep_timeout(self):
        timeout = 120
        logger.info(" {} ".center(20, '-').format('Sleep for {} seconds'.format(timeout)))
        time.sleep(timeout)
