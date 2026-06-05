__author__ = 'sgao'
'''
This file is to teardown the environment of HA
'''

from global_var import *

class TestTeardownTB(Test):
    uuid = 'NonTC'
    description = "teardown testbed"

    @repeat_method(3)
    def test_00_00_Disable_HA(self):
        logger.info(" Disable HA ".center(30, '-'))
        rc = False
        try:
            out = ha_status_cli.show_high_availability('base')
            if 'Could not start ssh' in out:
                logger.error('Could not start ssh, try to start restore firewalls.')
            if 'no mode' not in out:
                logger.info('--->>> Disable HA to prepare for restore...')
                opt = {'mode': 'None'}
                rc = ha_settings_cli.config_settings(**opt)
                if not rc:
                    raise KeyError
                rc = True
                time.sleep(5)
            else:
                rc = True
                logger.info('Not need disable HA...')
        except Exception as e:
            logger.error(f'Error! Reason: --> {e}')
        Assertion.assert_equal(rc, True, "ERR: Disable failed")

    def test_00_01_Check_firewall_boots_up(self):
        logger.info(" Check firewall up if restart ".center(30, '-'))
        rc = False
        logger.info('---> Waiting for sleeping 200s ...')
        time.sleep(200)
        flag1 = False
        flag2 = False
        for i in range(50):
            if not flag1:
                out1 = is_Firewall_up(
                    ip=FIREWALL, ssh=True, console_ip=sec_con_ip, console_port=sec_con_port,
                    mode='console', pre_sleep=0
                )
                if out1:
                    flag1 = True
            if not flag2:
                out2 = is_Firewall_up(
                    ip=FIREWALL, ssh=True, console_ip=pri_con_ip, console_port=pri_con_port,
                    mode='console', pre_sleep=0
                )
                if out2:
                    flag2 = True
            if flag1 and flag2:
                logger.info(" Firewall boots up ".center(30, '-'))
                rc = True
                break
            logger.info(" Sleep 30s for firewall up ".center(30, '-'))
            time.sleep(30)
        else:
            logger.error("All DUTs are unreachable")
        Assertion.assert_equal(rc, True, "ERR: Firewall up failed")

    def test_00_02_Clear_VLAN(self):
        logger.info(" Clear topo ".center(30, '-'))
#        cmd = f'{sw_cmd} -action rem-trunk-1 -port {product}-PRI:X1,{product}-PRI:X2,{product}-PRI:X3 ' +\
#              f'-spec {SPECFILE}'
#        logger.info(cmd)
#        os.system(cmd)
#        cmd = f'{sw_cmd} -action rem-trunk-2 -port {product}-SEC:X1,{product}-SEC:X2,{product}-SEC:X3 ' +\
#              f'-spec {SPECFILE}'
#        logger.info(cmd)
#        os.system(cmd)

        cmd = f'{sw_cmd} -action clear -spec {SPECFILE}'
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

