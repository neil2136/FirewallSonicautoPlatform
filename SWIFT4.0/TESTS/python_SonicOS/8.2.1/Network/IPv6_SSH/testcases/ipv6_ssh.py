from definition.settings import *


class Test_IPV6_SSH_01(Test):
    uuid = "SOSAIOT-TC-56676"
    description= show_testcase_info(TESTPLAN, '1530588', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530588')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_check_ipv6_info(self):
        res1 = interfacev6api.show_interface(name = 'X0')
        res2 = interfacev6api.show_interface(name = 'X1')
        if DUT_X0_IPV6 in str(res1) and "'ssh': True" in str(res1) and "'ssh': True" in str(res2) and DUT_X1_IPV6 in str(res2):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: check interface ipv6 info fail.")


class Test_IPV6_SSH_02(Test):
    uuid = "SOSAIOT-TC-56677"
    description= show_testcase_info(TESTPLAN, '1530589', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530589')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_check_ipv6_info_by_cli(self):
        res1 = interface_cli.show_interface_status(interface = 'X0',version='ipv6')
        res2 = interface_cli.show_interface_status(interface = 'X1',version='ipv6')
        if DUT_X0_IPV6 in str(res1) and 'no management ssh' not in str(res1) and DUT_X1_IPV6 in str(res2) and 'no management ssh' not in str(res2):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: check interface ipv6 info by cli fail.")


class Test_IPV6_SSH_03(Test):
    uuid = "SOSAIOT-TC-56678"
    description= show_testcase_info(TESTPLAN, '1530590', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530590')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_export_tsr_by_scp(self):
        cmds = ['export tech-support-report scp root@[2001:db0::1096]:/root/tsr.wri','password']
        fw_ipv6_cli.cli_login()
        fw_ipv6_cli.do_cli_commands(cmds)
        out = PC1.send_command('ls /root/tsr.wri ')
        Assertion.assert_regular(out, '/root/tsr.wri', f"ERR: export tsr by scp fail.")

    def test_02_restore_env(self):
        PC1.send_command('rm -rf /root/tsr.wri ')
        out = PC1.send_command('ls /root/tsr.wri ')
        Assertion.assert_regular(out, 'No such file or directory', f"ERR: export tsr by scp fail.")


class Test_IPV6_SSH_04(Test):
    uuid = "SOSAIOT-TC-56679"
    description= show_testcase_info(TESTPLAN, '1530591', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530591')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_login_with_KexAlgorithms(self):
        rc = fw_cli_option.cli_login()
        fw_cli_option.cli_logout()
        Assertion.assert_equal(rc, True, f"ERR: login_with_KexAlgorithms fail.")


class Test_IPV6_SSH_05(Test):
    uuid = "SOSAIOT-TC-56680"
    description= show_testcase_info(TESTPLAN, '1530592', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530592')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_login_with_EncryptAlgo(self):
        rc = fw_cli_encr.cli_login()
        fw_cli_encr.cli_logout()
        Assertion.assert_equal(rc, True, f"ERR: login_with_EncryptAlgo fail.")


class Test_IPV6_SSH_06(Test):
    uuid = "SOSAIOT-TC-56681"
    description= show_testcase_info(TESTPLAN, '1530593', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530593')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_login_with_MACAlgo(self):
        rc = fw_cli_mac.cli_login()
        res=fw_cli_mac.cli_logout()
        logger.info(f'-----{res}')
        Assertion.assert_equal(rc, True, f"ERR: login_with_MACAlgo fail.")


class Test_IPV6_SSH_07(Test):
    uuid = "SOSAIOT-TC-56683"
    description= show_testcase_info(TESTPLAN, '1530595', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530595')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_check_ipv6_ssh_status_in_tsr(self):
        rc = False
        res=diag_api.get_tsr_part(func='Network', lab1='Interfaces',lab2='')
        pattern1='IPv6 Settings]'+'\n(.*)\n' +'Interface Name                                  : X1'
        lab_match = re.search(r''+ pattern1 +'', res, re.I|re.S|re.M)
        if lab_match:
            out = lab_match.group(1)
            logger.info('+++++++++')
            logger.info(f'--++===={out}====++--')
            if 'Interface SSH Management' in out:
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check ipv6 ssh management status in tsr failed")


class Test_IPV6_SSH_08(Test):
    uuid = "SOSAIOT-TC-56684"
    description= show_testcase_info(TESTPLAN, '1530596', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530596')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_sshv1_login_ipv6(self):
        cmd = 'ssh -1 admin@2001:db0::193'
        out = PC1.send_command(cmd)
        Assertion.assert_regular(out, 'versions differ: 1 vs. 2', "ERR: check sshv1 login ipv6 failed")

    def test_01_sshv2_login_ipv6(self):
        rc = fw_cli.cli_login()
        fw_cli.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: check sshv2 login ipv6 failed")


class Test_IPV6_SSH_09(Test):
    uuid = "SOSAIOT-TC-56685"
    description= show_testcase_info(TESTPLAN, '1530597', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530597')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_add_bookmark(self):
        rc = sslvpnvirtual.configure_bookmark(**sshv2_bookmark)
        Assertion.assert_equal(rc, True, "ERR: add bookmark failed")

    @repeat_method(5)
    def test_02_login_portal_page_ipv6(self):
        try:
            cmd= [f'python3  {ui_file} -type connect_ssh_bookmark']
            out = PC2.send_commands(cmd)
            logger.info(f'-------{out}')
            if '---True---' in str(out):
                rc = True
            else:
                rc = False
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            rc= False
        Assertion.assert_equal(rc, True, "ERR: config  failed")
        

    def test_03_Del_bookmark(self):
        rc = sslvpnvirtual.delete_bookmark_by_name(name=sshv2_bookmark['name'])
        Assertion.assert_equal(rc, True, "ERR: delete bookmark failed")


class Test_IPV6_SSH_10(Test):
    uuid = "SOSAIOT-TC-56686"
    description= show_testcase_info(TESTPLAN, '1530598', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530598')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_vpn_ssh_ipv6(self):
        rc = Lvpn.add_ipv6_vpn_policy(**vpn_dict)
        Assertion.assert_equal(rc, True, "ERR: config vpn ssh ipv6 failed")

    def test_02_restore_env(self):
        rc = Lvpn.del_ipv6_vpn_policy(name=vpn_dict['name'])
        Assertion.assert_equal(rc, True, "ERR: restore env failed")


class Test_IPV6_SSH_11(Test):
    uuid = "SOSAIOT-TC-56688"
    description= show_testcase_info(TESTPLAN, '1530600', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530600')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_check_ssh_port(self):
        res = admin_api.show_admin_setting()
        logger.info(res)
        if res["administration"]['ssh']['port'] == 22:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check ssh port failed")


class Test_IPV6_SSH_12(Test):
    uuid = "SOSAIOT-TC-56682"
    description= show_testcase_info(TESTPLAN, '1530594', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1530594')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_change_ssh_port(self):
        rc = admin_api.conf_admin(**option_dict)
        Assertion.assert_equal(rc, True, "ERR: config ssh port failed")

    def test_02_login_ipv6_ssh(self):
        rc = fw_ipv6_cli.cli_login()
        Assertion.assert_equal(rc, False, "ERR: ssh ipv6 login should False failed")

    @repeat_method(4)
    def test_03_restore_ssh_and_login(self):
        ref = copy.deepcopy(option_dict)
        ref['ssh']['port'] = 22
        rc = admin_api.conf_admin(**ref)
        time.sleep(5)
        rc &= fw_ipv6_cli.cli_login()
        fw_ipv6_cli.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: restore default ssh port 22 and login success failed")


        
