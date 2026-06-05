__author__ = 'CHU'
from definition.settings import *

class TestBGP_01(Test):
    uuid = "SOSAIOT-TC-55790"
    description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_config_bgp_settings(self):
        logger.info(" {} ".center(20, '-').format('Config local settings for BGP'))
        cmd1 = 'neighbor {} remote-as 2'.format(rt_sub)
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmd1,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc1, output1) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Config remote settings for BGP'))
        cmd2 = 'neighbor {} remote-as 1'.format(lc_sub)
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmd2,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output2:
            logger.info('Remote Success!')
        rc = rc1 & rc2
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_01_02_check_bgp_status(self):
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        time.sleep(stime)
        cmd = 'show ip bgp neighbors {}'.format(rt_sub)
        commands = [
            'configure',
            'routing',
            'bgp',
            cmd,
            'exit', 'end', 'exit']
        rc = False
        for i in range(5):
            (ret, output) = cl1.do_cli_commands(commands, 1)
            if 'BGP state = Established' in output:
                logger.info('Check Established Success!')
                rc = True
                break
            elif i == 2:
                logger.info('Check Established Fail')
            else:
                logger.info('try again ...')
                time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_01_03_clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear settings for BGP'))
        time.sleep(stime)
        rc = clear.clear_BGP_settings()
        Assertion.assert_equal(rc, True, "ERR: Clear settings for BGP failed")

class TestBGP_02(Test):
    uuid = "SOSAIOT-TC-55794"
    description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_config_bgp_settings(self):
        ret = False
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmd1 = 'neighbor {} remote-as 2'.format(rt_ip)
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmd1,
            'end', 'write file ',
            'exit','commit','end','exit']
        (rc1, output1) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Config Remote Settings for BGP'))
        cmd2 = 'neighbor {} remote-as 1'.format(lc_ip)
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmd2,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output2:
            logger.info('Remote Success!')
        else:
            logger.info('Remote fail, do repeat')
            commands3 = ['show status']
            (ret, output3) = cl2.do_cli_commands(commands3, 1)
            logger.info(output3)
            (ret, output) = cl2.do_cli_commands(commands2, 1)
            if 'Error' not in output:
                logger.info('Remote Success!')
        if rc2:
            rc = rc1 & rc2
        else:
            rc = rc1 & ret
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_02_02_check_bgp_status(self):
        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        cmd = 'show ip bgp neighbors {}'.format(rt_ip)
        commands = [
            'configure',
            'routing',
            'bgp',
            cmd,
            'exit', 'commit','end', 'exit']
        rc = False
        for i in range(5):
            (ret, output) = cl1.do_cli_commands(commands, 1)
            if 'BGP state = Established' in output:
                logger.info('Check Established Success!')
                rc = True
                break
            elif i == 2:
                logger.info('Check Established Fail')
            else:
                logger.info('try again ...')
                time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_02_03_clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear Settings for BGP'))
        time.sleep(stime)
        rc = clear.clear_BGP_settings()
        Assertion.assert_equal(rc, True, "ERR: Clear settings for BGP failed")


class TestBGP_03(Test):
    uuid = "SOSAIOT-TC-55801"
    description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_config_bgp_settings(self):
        logger.info(" {} ".center(20, '-').format('Config Local Settings for BGP'))
        cmd1 = 'neighbor {} remote-as 2'.format(rt_ip)
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmd1,
            'network 192.168.168.0/24',
            'end', 'write file ',
            'exit', 'commit','end', 'exit']
        (rc1, output1) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Config Remote Settings for BGP'))
        cmd2 = 'neighbor {} remote-as 1'.format(lc_ip)
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmd2,
            'network 172.16.1.0/24',
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output1:
            logger.info('Remote Success!')
        rc = rc1 & rc2
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_03_02_check_bgp_status(self):
        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        cmd = 'show ip bgp neighbors {}'.format(lc_ip)
        commands = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            cmd,
            'exit',
            'nsm',
            'show ip route',
            'exit', 'commit','end', 'exit']
        (rc, output) = cl2.do_cli_commands(commands, 1)
        if 'BGP state = Established' in output:
            logger.info('Expected: BGP established!')
            rc = True
        else:
            logger.info('BGP not established')
            rc = False
        if '192.168.168.0/24' in output:
            logger.info('Expected: Output contain 192.168.168.0/24 20!')
            logger.info('----- Success -----')
            rc &= True
        else:
            logger.info('-----  Fail   -----')
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_03_03_clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear settings for BGP'))
        time.sleep(stime)
        rc = clear.clear_BGP_settings()
        Assertion.assert_equal(rc, True, "ERR: Clear settings for BGP failed")


class TestBGP_04(Test):
    uuid = "SOSAIOT-TC-55791"
    description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_config_bgp_settings(self):
        logger.info(" {} ".center(20, '-').format('Config Local settings for BGP'))
        cmda1 = 'neighbor {} remote-as 2'.format(rt_ip)
        cmda2 = 'neighbor {} password sonicwall'.format(rt_ip)
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmda1,
            cmda2,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc1, output1) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Config Remote Settings for BGP'))
        cmdb1 = 'neighbor {} remote-as 1'.format(lc_ip)
        cmdb2 = 'neighbor {} password sonicwall'.format(lc_ip)
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmdb1,
            cmdb2,
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output1:
            logger.info('Remote Success!')
        rc = rc1 & rc2
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_04_02_check_bgp_status(self):
        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        cmd = 'show ip bgp neighbors {}'.format(rt_ip)
        commands = [
            'configure',
            'routing',
            'bgp',
            cmd,
            'exit', 'commit', 'end', 'exit']
        rc = False
        for i in range(5):
            (ret, output) = cl1.do_cli_commands(commands, 1)
            if 'BGP state = Established' in output:
                logger.info('Check Established Success!')
                rc = True
                break
            elif i == 2:
                logger.info('Check Established Fail')
            else:
                logger.info('try again ...')
                time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Check settings for BGP failed")

    def test_04_03_clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear settings for BGP'))
        time.sleep(stime)
        rc = clear.clear_BGP_settings()
        Assertion.assert_equal(rc, True, "ERR: Clear settings for BGP failed")


class TestBGP_05(Test):
    uuid = "SOSAIOT-TC-55798"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_config_bgp_settings(self):
        logger.info(" {} ".center(20, '-').format('Config local settings for BGP'))
        cmd1 = 'neighbor {} remote-as 2'.format(rt_ip)
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            cmd1,
            'network 192.168.168.0/24',
            'network 192.101.1.0/24',
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc1, output1) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output1:
            logger.info('Local Success!')

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('Config remote settings for BGP'))
        cmd2 = 'neighbor {} remote-as 1'.format(lc_ip)
        commands2 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            'configure terminal',
            'router bgp 2',
            cmd2,
            'network 172.16.1.0/24',
            'network 172.16.2.0/24',
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output2:
            logger.info('Remote Success!')

    def test_05_02_check_bgp_status(self):
        logger.info(" {} ".center(20, '-').format('Specific BGP test case'))
        time.sleep(stime)
        cmd1 = 'show ip bgp neighbors {}'.format(lc_ip)
        commands1 = [
            'configure',
            'routing',
            'mode advanced',
            'bgp',
            cmd1,
            'exit',
            'nsm',
            'show ip route',
            'exit', 'commit', 'end', 'exit']
        (rc1, output1) = cl2.do_cli_commands(commands1, 1)
        if ('192.168.168.168.0/24' and '192.101.1.0/24' and 'Established') in output1:
            logger.info('Check Remote Success!')
            ret1 = True
        else:
            logger.info('Check Remote Fail')
            ret1 = False

        time.sleep(stime)
        logger.info(" {} ".center(20, '-').format('config DUT'))
        cmd2 = 'show ip bgp neighbors {}'.format(rt_ip)
        commands2 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'router bgp 1',
            'no network 192.168.168.0/24',
            'end',
            cmd2,
            'exit', 'commit', 'end', 'exit']
        (rc2, output2) = cl1.do_cli_commands(commands2, 1)
        if 'Established' in output2:
            logger.info('Check Local Success!')
            ret2 = True
        else:
            logger.info('Check Local Fail')
            ret2 = False
        rc = ret1 & ret2
        Assertion.assert_equal(rc, True, "ERR: Config settings for BGP failed")

    def test_05_03_clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear settings for BGP'))
        time.sleep(stime)
        rc = clear.clear_BGP_settings()
        Assertion.assert_equal(rc, True, "ERR: Clear settings for BGP failed")


