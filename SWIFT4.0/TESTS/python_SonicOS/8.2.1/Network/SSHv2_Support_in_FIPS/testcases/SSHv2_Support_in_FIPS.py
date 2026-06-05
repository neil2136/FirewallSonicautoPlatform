from definition.settings import *

# ##skip uuid='1524803':sonicos api is disable in  FIPS mode
# ##skip uuid='1524807':[GUI]terminal emulation need to click

class Test_SSHv2_Support_in_FIPS_01(Test):
    uuid = "SOSAIOT-TC-80351"
    description= show_testcase_info(TESTPLAN, '1524802', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524802')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_cipher_ssh(self):
        rc = cipher_ssh.config_cipher_ssh(**cipher_ssh_config1)
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")

    def test_02_config_fips_and_check(self):
        rc = fips_cli.enable_fips(**fips_dict)
        res = fips_obj.get_fips_warning()
        logger.info(res['data'][-1])
        if 'Must disable diffie-hellman-group1-sha1, diffie-hellman-group14-sha1' in res['data'][-1]:
            rc2 =(not rc) & True
        else:
            rc2 =(not rc) & False
        Assertion.assert_equal(rc2, True, f"ERR: config fips mode fail.")
       

class Test_SSHv2_Support_in_FIPS_02(Test):
    uuid = "SOSAIOT-TC-80357"
    description= show_testcase_info(TESTPLAN, '1524808', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524808')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_fips_by_cli(self):
        rc = fips_cli.enable_fips(**fips_dict)
        Assertion.assert_equal(rc, False, f"ERR: config fips mode by cli fail.")


@paramunittest.parametrized(
    {'Content': content_json['1524810'],'cipher_config':cipher_ssh_config2, 'uuid': '1524810'},
    {'Content': content_json['1524811'], 'cipher_config':cipher_ssh_config3,'uuid': '1524811'},
    {'Content': content_json['1524812'], 'cipher_config':cipher_ssh_config4,'uuid': '1524812'},
)
class Test_SSHv2_Support_in_FIPS_03(Test):
    def setParameters(self, Content,cipher_config,uuid):
        self.content = Content
        self.cipher_config = cipher_config
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 

    def test_01_config_cipher(self):
        rc = cipher_ssh.config_cipher_ssh(**self.cipher_config )
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")

    def test_01_modify_ssh_config(self):
        res = PC1.send_commands([f"cp -f {ssh_file}  {ssh_file_back}", f"ls {ssh_file_back}"])
        if 'ssh_config.back' in res:
            rc = True
        else:
            rc = False
        with open(ssh_file,"a+") as f:
            f.write(self.content)
        res2 = PC1.send_command(f"cat {ssh_file}")
        if self.content in res2:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: modify ssh config  failed")

    def test_02_login_fw(self):
        rc = fw_cli.cli_login()
        fw_cli.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: cli login fw  failed")

    def test_03_restore_env(self):
        res = PC1.send_commands([f"cp -f {ssh_file_back}  {ssh_file} ", f"rm -rf {ssh_file_back}",f"ls {ssh_file_back}"])
        if 'No such file'  in res:
            rc = True
        else:
            rc = False
        rc &= cipher_ssh.config_cipher_ssh(**cipher_ssh_config1)
        Assertion.assert_equal(rc, True, "ERR:restore env  failed")


class Test_SSHv2_Support_in_FIPS_04(Test):
    uuid = "SOSAIOT-TC-80365"
    description= show_testcase_info(TESTPLAN, '1524816', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524816')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_download_and_check_tsr(self):
        res = diag_api.get_tsr_part(func='Diagnostic',lab1='Internal Settings',lab2='SSH Cipher Control Settings')
        logger.info(f'-----{res}')
        if '"ecdh-sha2-nistp256": 1' in res and '"ecdh-sha2-nistp384": 1' in res:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR:download and check tsr  failed")


class Test_SSHv2_Support_in_FIPS_05(Test):
    uuid = "SOSAIOT-TC-80366"
    description= show_testcase_info(TESTPLAN, '1524817', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524817')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_reboot_and_check(self):
        rc = restartobj.restart_now()
        res = cipher_ssh.show_ssh_cipher()
        logger.info(f'----{res}')
        ref = res['cipher_control']['ssh']['key_exchange']
        if ref['ecdh_sha2_nistp256'] == True and ref['ecdh_sha2_nistp384'] == True and \
            ref['ecdh_sha2_nistp521'] == True:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: reboot fw  and check  config failed")


class Test_SSHv2_Support_in_FIPS_06(Test):
    uuid = "SOSAIOT-TC-80367"
    description= show_testcase_info(TESTPLAN, '1524818', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524818')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_cipher_ssh(self):
        rc = cipher_ssh.config_cipher_ssh(**disable_nistp384)
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")
    
    def test_02_export_and_import_setting(self):
        rc = setting_obj.export_setting_exp()
        rc &= cipher_ssh.config_cipher_ssh(**disable_nistp256)
        rc &= setting_obj.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, f"ERR: export and import setting fail.")

    def test_03_check_cipher_setting(self):
        res = cipher_ssh.show_ssh_cipher()
        logger.info(f'----{res}')
        ref = res['cipher_control']['ssh']['key_exchange']
        if ref['ecdh_sha2_nistp256'] == True and ref['ecdh_sha2_nistp384'] == False and \
            ref['ecdh_sha2_nistp521'] == True:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check  config failed")

    def test_04_restore_env(self):
        rc = cipher_ssh.config_cipher_ssh(**cipher_ssh_config1)
        Assertion.assert_equal(rc, True, "ERR:restore env  failed")


class Test_SSHv2_Support_in_FIPS_07(Test):
    uuid = "SOSAIOT-TC-80368"
    description= show_testcase_info(TESTPLAN, '1524819', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524819')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_config_cipher_with_cli_and_check(self):
        rc = cipher_cli.config_ssh_control(**cipher_cli_json1)
        res = cipher_ssh.show_ssh_cipher()
        logger.info(f'----{res}')
        ref = res['cipher_control']['ssh']['key_exchange']
        if ref['ecdh_sha2_nistp256'] == False and ref['ecdh_sha2_nistp384'] == False and \
            ref['ecdh_sha2_nistp521'] == False:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR:config cipher by cli and check failed")

    def test_02_config_cipher_with_cli_and_check(self):
        rc = cipher_cli.config_ssh_control(**cipher_cli_json2)
        res = cipher_ssh.show_ssh_cipher()
        logger.info(f'----{res}')
        ref = res['cipher_control']['ssh']['key_exchange']
        if ref['ecdh_sha2_nistp256'] == True and ref['ecdh_sha2_nistp384'] == True and \
            ref['ecdh_sha2_nistp521'] == True:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR:config cipher by cli and check failed")
        

#Set firewall to FIPS mode  
class Test_SSHv2_Support_in_FIPS_08(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_cipher_ssh(self):
        rc = cipher_ssh.config_cipher_ssh(**cipher_ssh_config5)
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")

    def test_02_config_group_vpn(self):
        rc = Lvpn.config_vpn_base(**vpn_base_dict)
        rc &= Lvpn.edit_wangroup_vpn_policy(**wan_groupvpn)
        rc &= Lvpn.edit_wlangroup_vpn_policy(**wlan_groupvpn)
        Assertion.assert_equal(rc, True, f"ERR: config group vpn fail.")

    def test_03_config_advanced_route(self):
        rc = dyn_route.set_advanced_routing_mode(advanced=False)
        Assertion.assert_equal(rc, True, f"ERR: config advanced route fail.")

    def test_04_config_sonicos_api(self):
        rc = admin_cli.sonicos_api(**api_dict)
        Assertion.assert_equal(rc, True, f"ERR: config sonicos api  fail.")

    def test_05_set_fips_mode(self):
        rc = fips_cli.enable_fips(**fips_dict)
        Assertion.assert_equal(rc, True, f"ERR: set fips mode fail.")


class Test_SSHv2_Support_in_FIPS_09(Test):
    uuid = "SOSAIOT-TC-80353"
    description= show_testcase_info(TESTPLAN, '1524804', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524804')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_01_login_via_sshv1(self):
        cmd = 'ssh -1 admin@192.168.168.168'
        out = PC1.send_command(cmd)
        Assertion.assert_regular(out, 'versions differ: 1 vs. 2', "ERR: check sshv1 login ipv6 failed")


class Test_SSHv2_Support_in_FIPS_10(Test):
    uuid = "SOSAIOT-TC-80354"
    description= show_testcase_info(TESTPLAN, '1524805', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524805')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_01_login_via_sshv2(self):
        rc = fw_cli.cli_login()
        fw_cli.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: check sshv2 login  failed")


class Test_SSHv2_Support_in_FIPS_11(Test):
    uuid = "SOSAIOT-TC-80355"
    description= show_testcase_info(TESTPLAN, '1524806', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524806')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_01_login_via_sshv2_ipv6(self):
        rc = fw_ipv6_cli.cli_login()
        fw_ipv6_cli.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: check sshv2 login ipv6  failed")


class Test_SSHv2_Support_in_FIPS_12(Test):
    uuid = "SOSAIOT-TC-80358"
    description= show_testcase_info(TESTPLAN, '1524809', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524809')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_01_config_cipher_with_cli(self):
        rc = cipher_cli.config_ssh_control(**cipher_cli_json3)
        Assertion.assert_equal(rc, False, "ERR: config cipher not allowed  failed")


@paramunittest.parametrized(
    {'Content': content_json['1524813'],'cipher_config':cipher_cli_json4,'login':fw_wan_cli, 'uuid': '1524813'},
    {'Content': content_json['1524814'], 'cipher_config':cipher_cli_json5,'login':fw_cli,'uuid': '1524814'},
    {'Content': content_json['1524815'], 'cipher_config':cipher_cli_json6,'login':mgmt_cli,'uuid': '1524815'},
)
class Test_SSHv2_Support_in_FIPS_13(Test):
    def setParameters(self, Content,cipher_config,login,uuid):
        self.content = Content
        self.cipher_config = cipher_config
        self.login = login
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 

    def test_01_config_cipher(self):
        rc = cipher_cli.config_ssh_control(**self.cipher_config)
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")

    def test_01_modify_ssh_config(self):
        res = PC1.send_commands([f"cp -f {ssh_file}  {ssh_file_back}", f"ls {ssh_file_back}"])
        if 'ssh_config.back' in res:
            rc = True
        else:
            rc = False
        with open(ssh_file,"a+") as f:
            f.write(self.content)
        res2 = PC1.send_command(f"cat {ssh_file}")
        if self.content in res2:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: modify ssh config  failed")

    def test_02_login_fw(self):
        rc = self.login.cli_login()
        self.login.cli_logout()
        Assertion.assert_equal(rc, True, "ERR: cli login fw  failed")

    def test_03_restore_env(self):
        res = PC1.send_commands([f"cp -f {ssh_file_back}  {ssh_file} ", f"rm -rf {ssh_file_back}",f"ls {ssh_file_back}"])
        if 'No such file'  in res:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR:restore env  failed")


class Test_SSHv2_Support_in_FIPS_14(Test):
    uuid = 'NonTC'

    def test_01_set_fips_mode(self):
        rc = fips_cli.enable_fips(**disable_fips)
        Assertion.assert_equal(rc, True, f"ERR: set fips mode fail.")

    def test_02_config_sonicos_api(self):
        rc = admin_cli.sonicos_api(**api_enable_dict)
        Assertion.assert_equal(rc, True, f"ERR: config sonicos api  fail.")

    def test_03_config_cipher_ssh(self):
        rc = cipher_ssh.config_cipher_ssh(**cipher_ssh_config1)
        Assertion.assert_equal(rc, True, f"ERR: config cipher ssh  fail.")






