__author__ = 'sgao'
'''
    Init physical testbed
    Config HA and monitoring, is stateful HA, register
'''

from global_var import *


# class TestCheckAndRecoveryCMPort(Test):
#     uuid = 'NonTC'
#     description = "check and recoveyr console port"
#     goto_teardown = True

#     def test_00_00_check_connection_via_console(self):
#         logger.info(" start check pri fw console accessable... ".center(30, '-'))
#         check_pri_console = diagpriconsole.run_recovery_test()
#         logger.info(f"check pri fw console connection: {check_pri_console}.")
#         logger.info(" start check sec fw console accessable... ".center(30, '-'))    
#         check_sec_console = diagsecconsole.run_recovery_test()
#         logger.info(f"check sec fw console connection: {check_sec_console}.")
#         logger.info(f'check_pri_console: {check_pri_console}, check_sec_console: {check_sec_console}')
#         Assertion.assert_equal(check_pri_console & check_sec_console, True, "ERR: check and recovey console port failed")


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_00_Restore_Both_FW_via_console(self):
    # # Send command 'firmware boot current factory' to restore FW can work with HA configured.
    # # To not affect the HA status or cause FW reboot, we will restore via console first.
    # # Then add the topology
        if not pri_console.console_connect() or not sec_console.console_connect():
            logger.info("The devices may be powered off.")
            pri_power.execute('on', pri_rpsw_port)
            sec_power.execute('on', sec_rpsw_port)
            poweron = 0
            time.sleep(300)
            for i in range(0,3):
                if pri_console.console_connect() and sec_console.console_connect():
                    poweron = 1
                    break
                time.sleep(100)
            if poweron == 0:
                Assertion.fail("Please check DUTs console. Restore FW via console failed.")

        ctrl_code = ']'
        pri_console.ssh.sendline('firmware boot current factory')
        time.sleep(2)
        pri_console.ssh.sendline('yes')
        res1 = pri_console.ssh.expect(['Restarting now'], timeout=10)
        pri_console.ssh.sendcontrol(ctrl_code)
        pri_console.close()
        if res1 == 0:
            logger.info("Primary DUT is booting to factory default")

        sec_console.ssh.sendline('firmware boot current factory')
        time.sleep(2)
        sec_console.ssh.sendline('yes')
        res2 = sec_console.ssh.expect(['Restarting now'], timeout=10)
        sec_console.ssh.sendcontrol(ctrl_code)
        sec_console.close()
        if res2 == 0:
            logger.info("Secondary DUT is booting to factory default")

        Assertion.assert_equal(res1+res2, 0, "ERR: Restore DUT failed")

    def test_00_01_Config_Testbed_Switch(self):
        logger.info(" Clear topo ".center(30, '-'))
        cmd = f'{sw_cmd} -action rem-trunk-1 -port {product}-PRI:X1,{product}-PRI:X2,{product}-PRI:X3 ' +\
              f'-spec {SPECFILE}'
        logger.info(cmd)
        os.system(cmd)
        cmd = f'{sw_cmd} -action rem-trunk-2 -port {product}-SEC:X1,{product}-SEC:X2,{product}-SEC:X3 ' +\
              f'-spec {SPECFILE}'
        logger.info(cmd)
        os.system(cmd)
        cmd = f'{sw_cmd} -action clear -spec {SPECFILE}'
        logger.info(cmd)
        rc1 = os.system(cmd)

        logger.info(f"Add topology: {topo}.".center(40, '-'))
        cmd = f'{sw_cmd} -action add -topo {topo} -spec {SPECFILE}'
        logger.info(cmd)
        rc2 = os.system(cmd)

        logger.info(" port down PRI:X0 ".center(40, '-'))
        cmd = f'{sw_cmd} -action portdown -port {pri_name}:X0 -spec {SPECFILE}'
        logger.info(cmd)
        rc3 = os.system(cmd)
        logger.info(f"Switch config results: {rc1}, {rc2}, {rc3}")

        rc = rc1 + rc2 + rc3

        if rc != 0:
            if rc3 != 0:
                logger.info("Need to reboot switch...")
                sw_name = list(yaml['switch'].keys())[0]
                print(sw_name)
                cmd = f'{sw_cmd} -action powercycle -device {sw_name} -spec {SPECFILE}'
                logger.info(cmd)
                os.system(cmd)
                for i in range(10):
                    print(f'Sleep {i} times...')
                    out = os.popen(f'ping {sw_name} -c 1').read()
                    print(out)
                    if ' 0% packet loss' in out:
                        (rc, rc1, rc2, rc3) = (0, 0, 0, 0)
                        print(rc, rc1, rc2, rc3)
                        break
                    time.sleep(10)

            if rc == 0 or rc3 == 0:
                logger.info("Relaunch clear stages...")

                cmd = f'{sw_cmd} -action rem-trunk-1 -port {product}-PRI:X1,{product}-PRI:X2,{product}-PRI:X3 ' +\
                      f'-spec {SPECFILE}'
                logger.info(cmd)
                os.system(cmd)

                cmd = f'{sw_cmd} -action rem-trunk-2 -port {product}-SEC:X1,{product}-SEC:X2,{product}-SEC:X3 ' +\
                      f'-spec {SPECFILE}'
                logger.info(cmd)
                os.system(cmd)

                cmd = f'{sw_cmd} -action clear -spec {SPECFILE}'
                logger.info(cmd)
                rc1 = os.system(cmd)

                logger.info(f"Add topology: {topo}.".center(40, '-'))
                cmd = f'{sw_cmd} -action add -topo {topo} -spec {SPECFILE}'
                logger.info(cmd)
                rc2 = os.system(cmd)

                logger.info(" port down PRI:X0 ".center(40, '-'))
                cmd = f'{sw_cmd} -action portdown -port {pri_name}:X0 -spec {SPECFILE}'
                logger.info(cmd)
                rc3 = os.system(cmd)
                logger.info(f"Switch config results: {rc1}, {rc2}, {rc3}")

                rc = rc1 + rc2 + rc3

        Assertion.assert_equal(rc, 0, "ERR: Config topo failed")

    def test_00_02_Wait_for_Secondary_FW_Boot_up(self):
        logger.info("Wait for secondary FW boot up")
        rc = is_Firewall_up(ip=FIREWALL, ssh=True, console_ip=sec_con_ip, console_port=sec_con_port, mode='ping')

        Assertion.assert_equal(rc, True, "ERR: Restore DUT failed")

    def test_00_03_Upload_SEC_Firmware(self):
        logger.info(" Start upload firmware ".center(40, '-'))
        rc = Local_HA_Lib().upload_firmware_HA(fw_cli, sec_console)
        Assertion.assert_equal(rc, True, "ERR: Upload SEC Firmware failed")

    def test_00_04_Config_SEC_interface_x1(self):
        logger.info(" Config SEC interface x1 ".center(40, '-'))
        x1_dict = copy.deepcopy(sec_x1_static)
        x1_dict['ip'] = '11.11.11.105'
        rc = if_api.config_interface(**x1_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @unittest.skipIf(os.environ['HA_REGISTER'] == 'off',"Just Stateful HA need to register")
    def test_00_05_Register_SEC(self):
        res = False
        for cont in range(5):
            logger.info(f" Verify register server accessable, try {cont+1} times ".center(40, '-'))
            output = diagnostic_api.connect_license_manager()
            logger.info(f'check register server access: {output}')
            if 'HTTPS responded successfully' in str(output):
                for i in range(10):
                    logger.info(f"start Register firewall via cli , try {i+1} times ".center(40, '-'))
                    registercli = license_cli.register("online")
                    logger.info(f"cli register result: {registercli}")  
                    if registercli:
                        logger.info("Register fw via cli successfully!")
                        res = True
                        break
                    else:
                        logger.info("Register fw via cli failed, wait 20s and try again...")
                        time.sleep(20)
                else:
                    logger.info("Register fw via cli failed after 3 tries.")
                    registerperl = os.popen(f'perl /SWIFT4.0/COMMON/bin/fwRegister.pl -p {Params.G_NEW_PASSWORD} ').read()
                    logger.info(f"perl register result: {registerperl}")
                    if 'Registration completed successfully' in registerperl:
                        logger.info("Register fw successfully via perl script!")
                        res = True
                        break
                    else:
                        logger.info("Register fw via perl script failed.")
                        res = False
                if res:
                    logger.info("Register fw successfully!")
                    break
            else:
                logger.info('check register server failed, wait 60s and try again...')
                time.sleep(60)
        else:
            logger.info("Can not access register server lm2.sonicwall.com after 3 tries.")
            res = False
        Assertion.assert_equal(res, True, "ERR: Register SEC fw failed")

    def test_00_06_Cut_Sec_X0_Link_and_Turn_up_Pri_X0(self):
        logger.info(" Switch the firewall from SEC to PRI ".center(40, '-'))
        logger.info(" port down SEC:X0 ".center(40, '-'))
        cmd1 = f'{sw_cmd} -action portdown -port {product}-SEC:X0 -spec {SPECFILE}'
        logger.info(cmd1)
        rc = os.system(cmd1)

        logger.info(" port up PRI:X0 ".center(40, '-'))
        cmd2 = f'{sw_cmd} -action portup -port {product}-PRI:X0 -spec {SPECFILE}'
        logger.info(cmd2)
        rc += os.system(cmd2)
        time.sleep(5)
        logger.info(rc)
        Assertion.assert_equal(rc, 0, "ERR: Config topo failed")

    def test_00_07_Upload_PRI_Firmware(self):
        logger.info("Verify primary FW SSH management ".center(40, '-'))
        if not is_Firewall_up(ip=FIREWALL, ssh=True, console_ip=pri_con_ip,
                              console_port=pri_con_port, mode='ping', pre_sleep=0):
            logger.error("Primary FW maybe died. Please check its status.")
            Assertion.fail("SSH management to primary issue.")
        logger.info(" Start upload firmware ".center(40, '-'))
        rc = Local_HA_Lib().upload_firmware_HA(fw_cli, pri_console)
        Assertion.assert_equal(rc, True, "ERR: Upload PRI Firmware failed")

    def test_00_08_Config_PRI_Interface_X1(self):
        logger.info(" Config PRI Interface X1 ".center(40, '-'))
        rc = if_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(3)
    @unittest.skipIf(os.environ['HA_REGISTER'] == 'off',"Just Stateful HA need to register")
    def test_00_09_Register_PRI(self):
        logger.info(" Register PRI firewall ".center(40, '-'))
        time.sleep(10)
        rc = license_cli.register("online")
        Assertion.assert_equal(rc, True, "ERR: Register PRI fw failed")

    def test_00_10_Enable_HA(self):
        logger.info(" Enable HA ".center(40, '-'))
        rc = ha_settings_api.config_mode_active(**ha_conf)
        Assertion.assert_equal(rc, True, "ERR: Enable HA failed")

    def test_00_11_Waiting_SEC_to_Boot_up(self):
        logger.info(" Waiting SEC firewall up, sleep 240s ".center(40, '-'))
        time.sleep(240)
        logger.info(" Check peer boot status ".center(40, '-'))
        rc = False
        for i in range(30):
            out = ha_status_api.show_ha_status()
            logger.info('*'*30)
            logger.info(out)
            if str(out['primary_state']).lower() == 'active' and \
               str(out['secondary_state']).lower() in ['standby', 'idle']:
                logger.info('--->>> Peer boots up!')
                rc = True
                break
            logger.info(" Sleep 30s for firewall up ".center(40, '-'))
            time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: Peer boots up failed")

    @unittest.skipIf(os.environ['HA_REGISTER'] == 'off', "Just Stateful HA need this step.")
    def test_00_12_Enable_Stateful(self):
        logger.info(" Enable Stateful ".center(30, '-'))
        opt = {
            'stateful_synchronization': True,
            'data_interface': data_if,
        }
        rc = ha_settings_api.config_mode_active(**opt)
        Assertion.assert_equal(rc, True, "ERR: Enable stateful failed")

    def test_00_13_Verify_HA_Status(self):
        logger.info("Wait some time for HA become stable.")
        time.sleep(10)
        logger.info("Verify HA status to make sure Primary active and Secondary standby.")
        out = ha_status_api.show_ha_status()
        logger.info('*'*30)
        logger.info(out)
        rc = False
        tmp_pri_stat = str(out['primary_state']).lower()
        tmp_sec_stat = str(out['secondary_state']).lower()
        logger.info(f"Primary current status: {tmp_pri_stat}")
        logger.info(f"Secondary current status: {tmp_sec_stat}")

        if tmp_pri_stat == 'active' and tmp_sec_stat in ['standby', 'idle']:
            rc = True
        else:
            logger.info(f"Need a force failover to reset HA status.")
            ha_advanced_api.force_failover()
            for i in range(30):
                out = ha_status_api.show_ha_status()
                logger.info('*'*30)
                logger.info(out)
                if str(out['primary_state']).lower() == 'active' and \
                   str(out['secondary_state']).lower() in ['standby', 'idle']:
                    logger.info('--->>> Peer boots up!')
                    rc = True
                    break
                logger.info(" Sleep 30s for firewall up ".center(40, '-'))
                time.sleep(30)
        Assertion.assert_equal(rc, True, "ERR: Reset HA status failed")

    def test_00_14_Enable_SEC_X0(self):
        logger.info(" Enable SEC X0 ".center(40, '-'))
        cmd = f'{sw_cmd} -action portup -port {product}-SEC:X0 -spec {SPECFILE}'
        rc = os.system(cmd)
        Assertion.assert_equal(rc, 0, "ERR: Enable SEC X0 failed")

    def test_00_15_Config_Monitoring(self):
        logger.info(f" Config Monitoring ".center(40, '-'))
        rc = ha_monitor_api.config_ha_monitoring(**x0_monitor)
        rc &= ha_monitor_api.config_ha_monitoring(**x1_monitor)
        Assertion.assert_equal(rc, True, "ERR: Config monitoring")

    def test_00_16_Test_Monitoring(self):
        logger.info(" Test Monitoring IP ".center(40, '-'))
        rc = False
        ti = 5
        for i in range(30):
            out1 = os.popen(f'ping {pri_x0_ip} -c 1 -w 1').read()
            out2 = os.popen(f'ping {sec_x0_ip} -c 1 -w 1').read()
            if '100% packet loss' not in out1 and '100% packet loss' not in out2:
                logger.info(out1)
                logger.info('-'*20)
                logger.info(out2)
                rc = True
                break
            logger.info(f'Need to sleep {ti} secs...')

            if i > 5:
                logger.info('Maybe the firewall is reboot now...')
                ti = 30
            time.sleep(ti)

        Assertion.assert_equal(rc, True, "ERR: Ping Monitoring IP failed")
