# from definition.settings import *
# from definition.utils import *
# import copy
# import os


# # Expected: Should not be able to connect when SSH disabled.
# class Test_SSH_With_ECLI_TC01(Test):
#     uuid = "SOSAIOT-TC-49339"
#     description = show_testcase_info(
#         TESTPLAN, '001', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '001')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Disable_X0_SSH(self):
#         if_x0_dict['mgmt_ssh'] = False
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Disable X0 SSH failed.")

#     def test_02_Try_SSH_Connect_X0(self):
#         rc = fw_cli.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH connect X0 passed, but it should not.")

#     def test_03_Enable_X0_SSH(self):
#         if_x0_dict['mgmt_ssh'] = True
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Enable X0 SSH failed.")


# # Expected: Should be able to connect when SSH enabled.
# class Test_SSH_With_ECLI_TC02(Test):
#     uuid = "SOSAIOT-TC-49349"
#     description = show_testcase_info(
#         TESTPLAN, '002', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '002')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Enable_X0_SSH(self):
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Enable X0 SSH failed.")

#     def test_02_Try_SSH_Connect_X0(self):
#         rc = fw_cli.ssh_connect()
#         Assertion.assert_equal(rc, True, "ERR: SSH connect X0 Failed.")

#     def test_03_Try_SSH_Connect_X1(self):
#          ssh_connect_remote(
#                 openstack_PC='-PC3',
#                 ip=Parameter_SSH.WANIP,
#                 username='admin',
#                 password='password',
#                 action='login')

# # Expected: User entering incorrect credentials is not allowed access.
# class Test_SSH_With_ECLI_TC03(Test):
#     uuid = "SOSAIOT-TC-49357"
#     description = show_testcase_info(
#         TESTPLAN, '003', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '003')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Enable_X0_SSH(self):
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Disable X0 SSH failed.")

#     def test_02_Try_SSH_Connect_X0_Wrong_Credentials(self):
#         tc3_fw_cli = Firewall(
#             ip,
#             user='admin2',
#             password='password2',
#             supported_config_mode='cli-ssh')
#         rc = tc3_fw_cli.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH connect X0 passed, but it should not.")


# # Expected:  Connection on non-standard TCP port 54022
# class Test_SSH_With_ECLI_TC04(Test):
#     uuid = "SOSAIOT-TC-49363"
#     description = show_testcase_info(
#         TESTPLAN, '004', description=True)['title']
#     jira = 'GEN7-34268'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '004')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Set_X0_SSH_Port(self):
#         SSH_default_Port_dict['ssh']['port'] = 54022
#         rc = admin_api.conf_admin(**SSH_default_Port_dict)
#         Assertion.assert_equal(rc, True, "ERR: Set X0 SSH Port failed.")

#     def test_02_Verify_SSH_Port_22(self):
#         rc = fw_cli.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH connect X0 passed, but it should not.")

#     def test_03_Verify_SSH_Port_54022(self):
#         out = fw_cli_p.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'name test', out[1], re.I | re.S | re.M) else False

#         Assertion.assert_equal(rc, True, "ERR: Test SSH Port 54022 failed.")

#     def test_04_Reset_SSH_Port(self):
#         SSH_default_Port_dict['ssh']['port'] = 22
#         rc = admin_api.conf_admin(**SSH_default_Port_dict)
#         Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")

#     def test_05_Delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete address object failed.")


# # Expected:  SSH disconnected after Disable SSH using serial console
# @unittest.skipIf('NSV' in Parameter_SSH.platform,
#                  'This platform have no console port.')
# class Test_SSH_With_ECLI_TC06(Test):
#     uuid = "SOSAIOT-TC-49373"
#     description = show_testcase_info(
#         TESTPLAN, '006', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '006')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_SSH_Connect_X0_1(self):
#         rc = fw_cli.cli_login()
#         Assertion.assert_equal(rc, True, "ERR: SSH Connect to X0 failed")

#     @repeat_method(3)
#     def test_02_Disable_SSH_via_console(self):
#         cmds = [
#             'configure',
#             'interface x0',
#             'no management ssh',
#             'commit',
#             'end',
#             'diag show processes']
#         out = fw_console_login.do_cli_commands(cmds, tag=1)
#         rc = True if out[0] and not re.search(
#             'tSshC', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Using console to disable SSH and SSH Disconnect to X0 failed")

#     def test_03_SSH_Connect_X0_2(self):
#         rc = fw_cli.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH connect X0 passed, but it should not.")

#     def test_04_Enable_SSH_X0(self):
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Enable X0 SSH failed.")


# # Expected:  SSH disconnected after Disable SSH using SSH
# class Test_SSH_With_ECLI_TC07(Test):
#     uuid = "SOSAIOT-TC-49374"
#     description = show_testcase_info(
#         TESTPLAN, '007', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '007')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Disable_X0_SSH_via_SSH(self):
#         cmds = [
#             'configure',
#             'interface x0',
#             'no management ssh',
#             'commit']
#         try:
#             fw_cli.do_cli_commands(cmds)
#         except BaseException:
#             check_SSH_processes(fw_console_login, 0)

#     def test_02_SSH_Connect_X0(self):
#         rc = fw_cli.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH connect X0 passed, but it should not.")

#     def test_03_Enable_SSH_X0(self):
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Enable X0 SSH failed.")


# # Expected:  SSH disconnected after changing ip using SSH
# @unittest.skipIf('NSV' in Parameter_SSH.platform,
#                  'This platform have no console port.')
# class Test_SSH_With_ECLI_TC08(Test):
#     uuid = "SOSAIOT-TC-49375"
#     description = show_testcase_info(
#         TESTPLAN, '008', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '008')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Change_SSH_port_via_SSH(self):
#         cmds = [
#             'configure',
#             'interface x0',
#             'ip-assignment LAN static',
#             'ip 192.168.168.167',
#             'commit']
#         try:
#             fw_cli.do_cli_commands(cmds)
#         except BaseException:
#             check_SSH_processes(fw_console_login, 0)

#     def test_02_Connect_New_IP(self):
#         fw_new_ip = Firewall(
#             '192.168.168.167',
#             user='admin',
#             password='password',
#             supported_config_mode='cli-ssh')
#         rc = fw_new_ip.cli_login()
#         Assertion.assert_equal(rc, True, "ERR: SSH connect to new IP failed.")

#     def test_03_Restore_X0_IP(self):
#         cmds = [
#             'configure',
#             'interface x0',
#             'ip-assignment LAN static',
#             'ip 192.168.168.168',
#             'commit']
#         fw_console_login.cli_login()
#         rc = fw_console_login.do_cli_commands(cmds)
#         Assertion.assert_equal(rc, True, "ERR: Restore X0 IP failed.")


# # Expected:  SSH disconnected after changing port using SSH
# class Test_SSH_With_ECLI_TC09(Test):
#     uuid = "SOSAIOT-TC-49376"
#     description = show_testcase_info(
#         TESTPLAN, '009', description=True)['title']
#     jira = 'GEN7-34268'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '009')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     # def test_01_Change_SSH_port_via_SSH(self):
#     #     cmds = [
#     #         'configure',
#     #         'administration',
#     #         'ssh port 54022',
#     #         'commit']
#     #     try:
#     #         fw_cli.do_cli_commands(cmds)
#     #     except BaseException:
#     #         check_SSH_processes(fw_console_login, 0)

#     # def test_02_Connect_New_port(self):
#     #     rc = fw_cli_p.cli_login()
#     #     Assertion.assert_equal(
#     #         rc, True, "ERR: SSH connect to new port 54022 failed.")

#     # def test_03_Connect_Old_port(self):
#     #     rc = fw_cli.cli_login()
#     #     Assertion.assert_equal(
#     #         rc, False, "ERR: SSH connect to old port 22 passed, but it should not.")

#     # def test_04_Restore_SSH_Port(self):
#     #     rc = admin_api.conf_admin(**SSH_default_Port_dict)
#     #     Assertion.assert_equal(rc, True, "ERR: Reset X0 SSH Port failed.")


# # Expected:  Multiple SSH sessions attempts
# class Test_SSH_With_ECLI_TC10(Test):
#     uuid = "SOSAIOT-TC-49338"
#     description = show_testcase_info(
#         TESTPLAN, '010', description=True)['title']
#     jira = 'GEN7-34268'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '010')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     @repeat_method(3)
#     def test_02_Launch_4_SSH_Connections(self):
#         rc1 = fw_cli_1.cli_login()
#         rc2 = fw_cli_2.cli_login()
#         rc3 = fw_cli_3.cli_login()
#         rc4 = fw_cli_4.cli_login()
#         out = fw_cli_4.do_cli_command('show ssh server sessions')
#         count = out.split('192.168.168')
#         if len(count) != 5:
#             print(out)
#             Assertion.fail("ERR: Get SSH sessions number failed.")
#         Assertion.assert_equal((rc1 and rc2 and rc3 and rc4), True, "ERR: Launch SSH connections failed.")

#     def test_03_Try_SSH_Connection_Again(self):
#         rc = fw_cli.cli_login()
#         Assertion.assert_equal(rc, False, "ERR: SSH to X0 passed, but it should not.")

#     def test_04_Disconnect_All_SSH_Connections(self):
#         fw_cli_1.ssh.sendline('exit')
#         fw_cli_1.close()
#         fw_cli_2.ssh.sendline('exit')
#         fw_cli_2.close()
#         fw_cli_3.ssh.sendline('exit')
#         fw_cli_3.close()
#         fw_cli_4.ssh.sendline('exit')
#         fw_cli_4.close()
#         time.sleep(5)
#         rc = fw_cli.cli_login()
#         Assertion.assert_equal(rc, True, "ERR: SSH to X0 passed.")


# # Expected:  Web session with SSH
# class Test_SSH_With_ECLI_TC11(Test):
#     uuid = "SOSAIOT-TC-49340"
#     description = show_testcase_info(
#         TESTPLAN, '011', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '011')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Web_Login(self):
#         rc = fw.api_login()
#         # Assertion.assert_equal(rc, True, "ERR: Web Login to X0 passed.")

#     def test_02_Enter_Command_Via_SSH(self):
#         out = fw_cli.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'name test', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(rc, True, "ERR: Enter command via SSH failed.")

#     def test_03_Configure_Via_API(self):
#         rc = ao_api.config_addressobject(**ao_dict_tc11)
#         Assertion.assert_equal(
#             rc, True, "ERR: Do some configurations via API failed.")

#     def test_04_Delete_AO(self):
#         rc = ao_api.del_addressobject(**ao_dict_tc11)
#         rc &= ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected:  Only one config level session(two ssh) can be present at the same time.
# class Test_SSH_With_ECLI_TC12(Test):
#     uuid = "SOSAIOT-TC-49341"
#     description = show_testcase_info(
#         TESTPLAN, '012', description=True)['title']
#     tc12_cmd = 'configure'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '012')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_SSH_to_X0(self):
#         rc = fw_cli.cli_login()
#         fw_cli.do_cli_command(self.tc12_cmd)
#         Assertion.assert_equal(rc, True, "ERR: SSH to x0 and go to the configuration level failed.")

#     def test_02_Intiate_another_SSH(self):
#         fw_cli_tc12 = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
#         out = fw_cli_tc12.do_cli_commands([self.tc12_cmd], tag=1)
#         rc = True if out[0] and re.search(
#             r'preempt', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(rc, True, "ERR: Initiate another ssh and go to the configuration level failed.")


# # Expected:  Only one config level session (console and ssh)can be present at the same time.
# @unittest.skipIf('NSV' in Parameter_SSH.platform,
#                  'This platform have no console port.')
# class Test_SSH_With_ECLI_TC13(Test):
#     uuid = "SOSAIOT-TC-49342"
#     description = show_testcase_info(
#         TESTPLAN, '013', description=True)['title']
#     tc13_cmd = 'configure'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '013')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     # def test_01_console_connect(self):
#     #     rc = fw_console_login.cli_login()
#     #     fw_console_login.do_cli_command(self.tc13_cmd)
#     #     Assertion.assert_equal(
#     #         Ture, True, "ERR: In Serial Console go to configuration level failed.")

#     def test_02_Intiate_another_SSH(self):
#         rc = fw_cli.cli_login()
#         fw_cli.do_cli_command(self.tc13_cmd)
#         Assertion.assert_equal(
#             rc,
#             True,
#             "ERR: Initiate another ssh and go to the configuration level failed.")

#     # def test_03_configure_first_ssh(self):
#     #     out = fw_console_login.do_cli_commands([self.tc13_cmd], tag=1)
#     #     rc = True if out[0] and re.search(
#     #         r'preempt', out[1], re.I | re.S | re.M) else False
#     #     Assertion.assert_equal(
#     #         rc, True, "ERR: The first ssh connection is not configured fail.")


# # Expected:  SSH1 fail
# class Test_SSH_With_ECLI_TC14(Test):
#     uuid = "SOSAIOT-TC-49343"
#     description = show_testcase_info(
#         TESTPLAN, '014', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '014')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_SSH1_Connect_X0(self):
#         fw_cli_tc14 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             ssh_version=1,
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc14.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH1 to X0 success, but it should fail.")


# # Expected: SSH Connection with Zlib compression successfully
# class Test_SSH_With_ECLI_TC15(Test):
#     uuid = "SOSAIOT-TC-49344"
#     description = show_testcase_info(
#         TESTPLAN, '015', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '015')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_ssh_connect(self):
#         fw_ssh_tc15 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_compr=True,
#             supported_config_mode='cli-ssh')
#         out = fw_ssh_tc15.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'name test', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: SSH Connection with Zlib compression failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with aes128-ctr Encryption successfully
# class Test_SSH_With_ECLI_TC16(Test):
#     uuid = "SOSAIOT-TC-49345"
#     description = show_testcase_info(
#         TESTPLAN, '016', description=True)['title']
#     Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '016')

#     def test_02_Try_Aes128ctr_Encryption_SSH(self):
#         fw_cli_tc16 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='aes128-ctr',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc16.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH aes128-ctr encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with aes192-ctr Encryption successfully
# class Test_SSH_With_ECLI_TC17(Test):
#     uuid = "SOSAIOT-TC-49346"
#     description = show_testcase_info(
#         TESTPLAN, '017', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '017')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Aes172ctr_Encryption_SSH(self):
#         fw_cli_tc17 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='aes192-ctr',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc17.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH aes192-ctr encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with aes256-ctr Encryption successfully
# class Test_SSH_With_ECLI_TC18(Test):
#     uuid = "SOSAIOT-TC-49347"
#     description = show_testcase_info(
#         TESTPLAN, '018', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '018')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Aes256ctr_Encryption_SSH(self):
#         fw_cli_tc18 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='aes256-ctr',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc18.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH aes256-ctr encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with arcfour128 Encryption fail
# class Test_SSH_With_ECLI_TC19(Test):
#     uuid = "SOSAIOT-TC-49348"
#     description = show_testcase_info(
#         TESTPLAN, '019', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '019')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Arcfour128_Encryption_SSH(self):
#         fw_cli_tc19 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='arcfour128',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc19.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: Test SSH arcfour128 encryption success, but it should fail.")


# # Expected: SSH Connection with 3des-cbc Encryption fail
# class Test_SSH_With_ECLI_TC20(Test):
#     uuid = "SOSAIOT-TC-49350"
#     description = show_testcase_info(
#         TESTPLAN, '020', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '020')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_3DESCBC_Encryption_SSH(self):
#         fw_cli_tc20 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='3des-cbc',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc20.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: Test SSH arcfour128 encryption success, but it should fail.")


# # Expected: SSH Connection with arcfour128 Encryption successfully
# class Test_SSH_With_ECLI_TC21(Test):
#     uuid = "SOSAIOT-TC-84571"
#     description = show_testcase_info(
#         TESTPLAN, '021', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '021')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Arcfour_Encryption_SSH(self):
#         fw_cli_tc21 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='arcfour',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc21.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH arcfour encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with aes128-gcm@openssh.com Encryption successfully
# class Test_SSH_With_ECLI_TC22(Test):
#     uuid = "SOSAIOT-TC-49351"
#     description = show_testcase_info(
#         TESTPLAN, '022', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '022')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_aes128gcm_Encryption_SSH(self):
#         fw_cli_tc22 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='aes128-gcm@openssh.com',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc22.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH aes128-gcm@openssh.com encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: SSH Connection with aes256-gcm@openssh.com Encryption successfully
# class Test_SSH_With_ECLI_TC23(Test):
#     uuid = "SOSAIOT-TC-49352"
#     description = show_testcase_info(
#         TESTPLAN, '023', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '023')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_aes156gcm_Encryption_SSH(self):
#         fw_cli_tc23 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='aes256-gcm@openssh.com',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc23.ssh_connect()
#         Assertion.assert_equal(
#             rc,
#             False,
#             "ERR: Test SSH aes256-gcm@openssh.com encryption success, but it should fail.")


# # Expected: SSH Connection with blowfish-cbc Encryption rejected
# class Test_SSH_With_ECLI_TC24(Test):
#     uuid = "SOSAIOT-TC-49353"
#     description = show_testcase_info(
#         TESTPLAN, '024', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '024')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_blowfish_cbc_Encryption_SSH(self):
#         fw_cli_tc24 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             cli_encr='blowfish-cbc',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc24.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if not out[0] and not re.search(
#             r'address-object ipv4 test', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc,
#             True,
#             "ERR: Test SSH blowfish-cbc encryption sucessfully, but it should fail.")


# # Expected: SSH Connection with hmac-md5 Encryption successfully
# class Test_SSH_With_ECLI_TC25(Test):
#     uuid = "SOSAIOT-TC-49354"
#     description = show_testcase_info(
#         TESTPLAN, '025', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '025')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Hmac_MD5_Encryption_SSH(self):
#         fw_cli_tc25 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             mac_spec='hmac-md5',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc25.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: Test SSH hmac-md5 encryption success, but it should fail.")


# # Expected: SSH Connection with hmac-sha1 Encryption successfully
# class Test_SSH_With_ECLI_TC26(Test):
#     uuid = "SOSAIOT-TC-49355"
#     description = show_testcase_info(
#         TESTPLAN, '026', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '026')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Try_Hmac_MD5_Encryption_SSH(self):
#         fw_cli_tc26 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             mac_spec='hmac-sha1',
#             supported_config_mode='cli-ssh')
#         out = fw_cli_tc26.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'address-object ipv4 test',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Test SSH hmac-sha1 encryption failed.")

#     def test_03_delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: Telnet to 192.168.168.168:22, SSH version is displayed and nomproblems result.
# class Test_SSH_With_ECLI_TC31(Test):
#     uuid = "SOSAIOT-TC-49358"
#     description = show_testcase_info(
#         TESTPLAN, '031', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '031')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_telnet_with_SSH_Port(self):
#         cmds = ['telnet ' + ip + ' 22', '\n']
#         out = ''
#         for cmd in cmds:
#             logger.info('send command： ' + cmd)
#             out += os.popen(cmd).read()
#         logger.info(out)
#         rc = True if re.search(
#             r'SSH\-2.0.*?Protocol mismatch',
#             out,
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, False, "ERR: Test telnet to ssh port succeed, but it should not")


# # Expected:  SSH using ssh-dss fail
# class Test_SSH_With_ECLI_TC32(Test):
#     uuid = "SOSAIOT-TC-49359"
#     description = show_testcase_info(
#         TESTPLAN, '032', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '032')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_SSH_SSHDSS(self):
#         fw_cli_tc32 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             option='HostKeyAlgorithms=+ssh-dss',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc32.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: THostKeyAlgorithms=ssh-dss success, but it should not")


# # Expected: SSH to configure mode pass after close console
# @unittest.skipIf('NSV' in Parameter_SSH.platform,
#                  'This platform have no console port.')
# class Test_SSH_With_ECLI_TC42(Test):
#     uuid = "SOSAIOT-TC-49364"
#     description = show_testcase_info(
#         TESTPLAN, '042', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '042')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Console_FW(self):
#         rc = fw_console_login.cli_login()
#         Assertion.assert_equal(
#             rc, True, "ERR: Console connect FW success")

#     def test_03_SSH_X0_Configure(self):
#         rc = fw_cli.ssh_connect()
#         rc &= fw_cli.do_cli_commands(['configure'])
#         Assertion.assert_equal(
#             rc, True, "ERR: SSH to X0 and type configure success")

#     def test_04_Close_Console_Open_SSH(self):
#         fw_console_login.cli_logout()
#         out = fw_cli.do_cli_commands(add_ao_cli, tag=1)
#         rc = True if out[0] and re.search(
#             r'name test', out[1], re.I | re.S | re.M) else False
#         Assertion.assert_equal(rc, True, "ERR: Enter command via SSH failed.")

#     def test_05_Delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete Address Objects failed.")


# # Expected: no issue occurs when type ssh ip_address -l admin show status
# class Test_SSH_With_ECLI_TC43(Test):
#     uuid = "SOSAIOT-TC-49365"
#     description = show_testcase_info(
#         TESTPLAN, '043', description=True)['title']
#     jira = 'GEN7-33618'

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '043')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_SSH_with_Extra_Command(self):
#         fw_cli_tc43 = Firewall(
#             ip,
#             user='admin',
#             password='password',
#             other='show status',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc43.ssh_connect()
#         Assertion.assert_equal(
#             rc, False, "ERR: Enter extra command when SSH connection failed.")


# # Expected: no issues when timeout of CLI session when change of password
# # is required
# @unittest.skipIf('NSV' in Parameter_SSH.platform,
#                  'This platform have no console port.')
# class Test_SSH_With_ECLI_TC44(Test):
#     uuid = "SOSAIOT-TC-49366"
#     description = show_testcase_info(
#         TESTPLAN, '044', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '044')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_Add_Admin_User(self):
#         admin_user_dict = {
#             "action": "add",
#             "username": "test44",
#             "userpassword": "password",
#             "member_of": ["SonicWALL Administrators"],
#             "force_password_change": True
#         }
#         rc = user_api.local_user(**admin_user_dict)
#         Assertion.assert_equal(
#             rc, True, "ERR: Add a local user member of Sonicwall Administrators failed")

#     def test_03_Set_CLI_Timeout(self):
#         cmds = ['configure',
#                 'cli idle-timeout default 1',
#                 'commit',
#                 'show cli idle-timeout ']
#         out = fw_cli.do_cli_commands(cmds, tag=1)
#         rc = True if out[0] and re.search(
#             r'cli idle-timeout default 1',
#             out[1],
#             re.I | re.S | re.M) else False
#         Assertion.assert_equal(
#             rc, True, "ERR: Set CLI idle-timeout default time to 1 failed")

#     def test_04_SSH_With_Admin_User(self):
#         fw_cli_tc44 = Firewall_new(
#             ip,
#             user='test44',
#             password='password',
#             new_password='password2',
#             supported_config_mode='cli-ssh')
#         rc = fw_cli_tc44.ssh_connect_admin_user()
#         Assertion.assert_equal(
#             rc, False, "ERR: SSH with admin user and change password failed")

#     def test_06_delete_user(self):
#         rc = user_api.delete_local_user_no_domain('test44')
#         Assertion.assert_equal(rc, True, "ERR: Delete local user failed")


# # Expected: SSH management via SSLVPN success.
# class Test_SSH_With_ECLI_TC46(Test):
#     uuid = "SOSAIOT-TC-49368"
#     description = show_testcase_info(
#         TESTPLAN, '046', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '046')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_install_nx_for_pc3(self):
#         installnx.buildnx_linux_remote('-PC3')
#         installnx.install_nx_linux_remote('-PC3')

#     # # @repeat_method(3)
#     # def test_02_SSH_connect_over_sslvpn(self):
#     #     run_io_tasks_in_parallel(
#     #         [
#     #             lambda: nx.connect_nxlinux_remote(
#     #                 user='sslvpntest',
#     #                 pswd='password',
#     #                 netexurl=Parameter.WANIP + ':4433',
#     #                 domain='LocalDomain',
#     #                 openstack_PC='-PC3'))
#                 # lambda: ssh_connect_remote(
#                 #     openstack_PC='-PC3',
#                 #     ip=ip,
#                 #     username='admin',
#                 #     password='password',
#                 #     action='login')])


# # Expected: SSH management via VPN success.
# class Test_SSH_With_ECLI_TC47(Test):
#     uuid = "SOSAIOT-TC-49369"
#     description = show_testcase_info(
#         TESTPLAN, '047', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '047')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_02_SSH_connect_over_VPN(self):
#         ssh_connect_remote(
#             openstack_PC='-PC2',
#             ip=ip,
#             username='admin',
#             password='sonicauto',
#             action='addao'),

#     def test_03_Delete_AO(self):
#         rc = ao_api.del_addressobject(**del_ao_dict)
#         Assertion.assert_equal(rc, True, "ERR: Delete address object failed.")


# # Expected: No SSH over SSL-VPN sessions after NetExtender is disconnected.
# class Test_SSH_With_ECLI_TC48(Test):
#     uuid = "SOSAIOT-TC-49370"
#     description = show_testcase_info(
#         TESTPLAN, '048', description=True)['title']

#     def test_01_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '048')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     # @repeat_method(3)
#     # def test_02_SSH_connect_over_sslvpn(self):
#     #     run_io_tasks_in_parallel(
#     #         [
#     #             lambda: nx.connect_nxlinux_remote(
#     #                 user='sslvpntest',
#     #                 pswd='password',
#     #                 netexurl=Parameter.WANIP + ':4433',
#     #                 domain='LocalDomain',
#     #                 openstack_PC='-PC3'),
#     #             lambda: ssh_connect_remote(
#     #                 openstack_PC='-PC3',
#     #                 ip=ip,
#     #                 username='admin',
#     #                 password='sonicauto',
#     #                 action='login'),
#     #             lambda: nx.NX_disconnect_remote('-PC3')
#     #             ])



# # Expected: SSH over SSL-VPN fail after Disable SSH management .
# class Test_SSH_With_ECLI_TC49(Test):
#     uuid = "SOSAIOT-TC-49371"
#     description = show_testcase_info(
#         TESTPLAN, '049', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '049')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_Disable_X0_SSH(self):
#         if_x0_dict['mgmt_ssh'] = False
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Disable X0 SSH failed.")

#     def test_02_SSH_connect_over_sslvpn(self):
#         run_io_tasks_in_parallel(
#             [
#                 lambda: nx.connect_nxlinux_remote(
#                     user='sslvpntest',
#                     pswd='password',
#                     netexurl=Parameter.WANIP +
#                     ':4433',
#                     domain='LocalDomain',
#                     openstack_PC='-PC3'),
#                 lambda: ssh_connect_remote(
#                     openstack_PC='-PC3',
#                     ip=ip,
#                     username='admin',
#                     password='sonicauto',
#                     action='check_login_failed',
#                     enable=1)])

#     def test_03_Enable_X0_SSH(self):
#         if_x0_dict['mgmt_ssh'] = True
#         rc = if_api.config_interface(**if_x0_dict)
#         Assertion.assert_equal(rc, True, "ERR: Enable X0 SSH failed.")
