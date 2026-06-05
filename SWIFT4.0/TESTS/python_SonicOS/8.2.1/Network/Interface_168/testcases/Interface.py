from testcases.settings import *


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_06(Test):
    uuid = "SOSAIOT-TC-56226"
    description = show_testcase_info(Parameter.TESTPLAN, "6", description=True)['title']

    #show testplan
    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_VerifyInvalidIpAddress(self):
        dns_names = ['dns1', 'dns2', 'dns3']
        invalid_ip_address = ['abc123', '1.1.256.1', '255.1.1.1']
        for address in invalid_ip_address:
            for dns_name in dns_names:
                x1_opt = {
                    'if': 'x1',
                    'zone': 'WAN',
                    'mode': 'static',
                    'ip': Parameter.X1_IP,
                    'mask': Parameter.Mask,
                    dns_name: address
                }
                out = interface.config_interface(msg=True, **x1_opt)
                logger.info(out)
                msg = False
                if 'invalid format' in out[1]['status']['info'][0]['message'] or 'Invalid IP' in out[1]['status']['info'][0]['message']:
                    msg = True
                logger.info(out[1]['status']['info'][0]['message'])
                Assertion.assert_equal(msg, True, "Invalid format or ip can be configured")

    def test_01_02_VerifyValidIpAddress(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'mask': Parameter.Mask,
            'dns1': '7.7.7.7',
            'dns2': '8.8.8.8',
            'dns3': '9.9.9.9',
        }
        out = interface.config_interface(msg=True,**x1_opt)
        logger.info(out[1]['status']['info'][0]['message'])
        Assertion.assert_equal(out[0], True, "Configure X1 with valid ip failed!")


class Test_Interface_07(Test):
    uuid = "SOSAIOT-TC-56235"
    description = show_testcase_info(Parameter.TESTPLAN, "7", description=True)['title']

    #show testplan
    def test_02_00_show_testplan(self):
        utils.log_testplan('7')

    #enable management
    def test_02_01_EnableManagement(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            # 'mgmt_http': Parameter.MGMT_HTTP,
            'mgmt_https': Parameter.MGMT_HTTPS,
            'mgmt_snmp': Parameter.MGMT_SNMP,
            'mgmt_ping': Parameter.MGMT_Ping,
            'mgmt_ssh': Parameter.MGMT_SSH,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    #verify there is a access-rule
    def test_02_02_VerifyAccessRuleAutoAdded(self):
        result = accessrule.verify_access_rule(access_rule='http', destination='All X2 Management IP')
        Assertion.assert_equal(result, True, "ERR: Verify http access-rules failed!")

    # #delete management on Interface x2
    def test_02_04_DisableManagementOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_http': False,
            'mgmt_https': False,
            'mgmt_snmp': False,
            'mgmt_ping': False,
            'mgmt_ssh': False,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 Management failed!")
        #verify
        result_verify_access_rules = accessrule.verify_access_rule(access_rule='http', destination='All X2 Management IP')
        Assertion.assert_equal(result_verify_access_rules, False, "ERR: The HTTP Management access rule is still here!")
        #test management deleted
        result_test_deleted = utils.test_management_function('http', 'off') # return failed = True
        Assertion.assert_equal(result_test_deleted, True, "ERR: -----------------HTTP Management Function is still working!-------")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_08(Test):
    uuid = "SOSAIOT-TC-56238"
    description = show_testcase_info(Parameter.TESTPLAN, "8", description=True)['title']

    #show testplan
    def test_03_00_show_testplan(self):
        utils.log_testplan('8')

    # enable management
    def test_03_01_EnableManagement(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': Parameter.MGMT_HTTPS,
            'mgmt_snmp': Parameter.MGMT_SNMP,
            'mgmt_ping': Parameter.MGMT_Ping,
            'mgmt_ssh': Parameter.MGMT_SSH,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    #verify there is a access-rule
    def test_03_02_VerifyAccessRuleAutoAdded(self):
        result = accessrule.verify_access_rule(access_rule='https', destination='All X2 Management IP')
        Assertion.assert_equal(result, True, "ERR: Verify https access-rules failed!")

    #test function auto-added
    def test_03_03_TestFunction(self):
        time.sleep(5)
        cmd = 'curl -k -i -H "Content-Type: application/json" -H "Accept: application/json" -X GET https://{}/api/sonicos'.format(Parameter.X2_IP)
        result = localhost.send_command(cmd)    # test http Mangement auto-added, return success = True
        Assertion.assert_regular(result, r'200 OK', "ERR: HTTPS management tests failed!")

    # #delete management on Interface x2
    def test_03_04_DisableManagementOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': False,
            'mgmt_snmp': False,
            'mgmt_ping': False,
            'mgmt_ssh': False,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 Management failed!")
        #verify
        result_verify_access_rules = accessrule.verify_access_rule(access_rule='https', destination='All X2 Management IP')
        Assertion.assert_equal(result_verify_access_rules, False, "ERR: The HTTPS Management access rule is still here!")
        #test management deleted
        result_test_deleted = utils.test_management_function('https', 'off') # return failed = True
        Assertion.assert_equal(result_test_deleted, True, "ERR: -----------------HTTPS Management Function is still working!-------")



@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_09(Test):
    uuid = "SOSAIOT-TC-56239"
    description = show_testcase_info(Parameter.TESTPLAN, "9", description=True)['title']

    #show testplan
    def test_04_00_show_testplan(self):
        utils.log_testplan('9')

    # enable management
    def test_04_01_EnableManagement(self):
        x2_opt = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': Parameter.MGMT_HTTPS,
            'mgmt_snmp': Parameter.MGMT_SNMP,
            'mgmt_ping': Parameter.MGMT_Ping,
            'mgmt_ssh': Parameter.MGMT_SSH,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    #verify there is a access-rule
    def test_04_02_VerifyAccessRuleAutoAdded(self):
        result = accessrule.verify_access_rule(access_rule='ping', destination='All X2 Management IP')
        Assertion.assert_equal(result, True, "ERR: Verify ping access-rules failed!")

    #test function auto-added
    def test_04_03_TestFunction(self):
        time.sleep(5)
        result = utils.test_management_function('ping','on')    # test ping auto-added, return success = True
        Assertion.assert_equal(result, True, "ERR: Ping  tests failed!")

    # #delete management on Interface x2
    def test_04_04_DisableManagementOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            # 'mgmt_http': False,
            'mgmt_https': False,
            'mgmt_snmp': False,
            'mgmt_ping': False,
            'mgmt_ssh': False,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 Management failed!")
        #verify
        result_verify_access_rules = accessrule.verify_access_rule(access_rule='ping', destination='All X2 Management IP')
        Assertion.assert_equal(result_verify_access_rules, False, "ERR: The Ping access rule is still here!")
        #test management deleted
        result_test_deleted = utils.test_management_function('ping', 'off') # return failed = True
        Assertion.assert_equal(result_test_deleted, True, "ERR: -----------------Ping Function is still working!-------")


@repeat_class(3, 20)
@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_10(Test):
    uuid = "SOSAIOT-TC-56177"
    description = show_testcase_info(Parameter.TESTPLAN, "10", description=True)['title']

    #show testplan
    def test_05_00_show_testplan(self):
        utils.log_testplan('10')

    # enable management
    def test_05_01_EnableManagement(self):
        advance = {'mandatory': False}
        res = snmp_obj.snmp_advance_settings(**advance)
        config_snmp_dict = {
            "enable":True,
            "system_name": "SonicwallTest",
            "system_contact": "test@test.com",
            "system_location": "Shanghai",
            "asset_number": "1234567",
            "get_community_name": "public",
            "trap_community_name": "admin",
            "host_1": PC1_ETH1_IP
        }
        res &= snmp_obj.snmp_base_settings(**config_snmp_dict)
        Assertion.assert_equal(res, True, "ERR: config snmp failed.")
        #enable FW snmp :
        fw = Firewall(Parameter.FIREWALL, user='admin', password='password', supported_config_mode='cli-ssh')
        cmds = ['configure','snmp','enable','commit']
        (rc, output) = fw.do_cli_commands(cmds, 1)
        if rc == False:
            logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: Configure FW SNMP failed!")
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': Parameter.MGMT_HTTPS,
            'mgmt_snmp': Parameter.MGMT_SNMP,
            'mgmt_ping': Parameter.MGMT_Ping,
            'mgmt_ssh': Parameter.MGMT_SSH,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    #verify there is a access-rule
    def test_05_02_VerifyAccessRuleAutoAdded(self):
        result = accessrule.verify_access_rule(access_rule='snmp', destination='All X2 Management IP')
        Assertion.assert_equal(result, True, "ERR: Verify SNMP access-rules failed!")

    #test function auto-added
    def test_05_03_TestFunction(self):
        time.sleep(5)
        result = utils.test_management_function('snmp','on')    # test snmp auto-added, return success = True
        Assertion.assert_equal(result, True, "ERR:  SNMP  tests failed!")

    # #delete management on Interface x2
    def test_05_04_DisableManagementOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': False,
            'mgmt_snmp': False,
            'mgmt_ping': False,
            'mgmt_ssh': False,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 Management failed!")
        #verify
        result_verify_access_rules = accessrule.verify_access_rule(access_rule='snmp', destination='All X2 Management IP')
        Assertion.assert_equal(result_verify_access_rules, False, "ERR: The SNMP access rule is still here!")
        #test management deleted
        result_test_deleted = utils.test_management_function('snmp', 'off') # return failed = True
        Assertion.assert_equal(result_test_deleted, True, "ERR: -----------------SNMP Function is still working!-------")


class Test_Interface_11(Test):
    uuid = "SOSAIOT-TC-56178"
    description = show_testcase_info(Parameter.TESTPLAN, "11", description=True)['title']

    #show testplan
    def test_06_00_show_testplan(self):
        utils.log_testplan('11')

    # enable management
    def test_06_01_EnableManagement(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': Parameter.MGMT_HTTPS,
            'mgmt_snmp': Parameter.MGMT_SNMP,
            'mgmt_ping': Parameter.MGMT_Ping,
            'mgmt_ssh': Parameter.MGMT_SSH,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    #verify there is a access-rule
    def test_06_02_VerifyAccessRuleAutoAdded(self):
        result = accessrule.verify_access_rule(access_rule='ssh', destination='All X2 Management IP')
        Assertion.assert_equal(result, True, "ERR: Verify SSH Management access-rules failed!")

    #test function auto-added
    def test_06_03_TestFunction(self):
        #result = utils.test_management_function('ssh','on')    # test ssh auto-added, return success = True
        nc_cmd = f'ncat -i 1 {Parameter.X2_IP} 22'
        result = 'SSH' in localhost.send_command(nc_cmd)
        Assertion.assert_equal(result, True, "ERR:  SSH  tests failed!")

    # #delete management on Interface x2
    def test_06_04_DisableManagementOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': False,
            'mgmt_snmp': False,
            'mgmt_ping': False,
            'mgmt_ssh': False,
        }
        out = interface.config_interface(**x2_opt)
        logger.info(out)
        Assertion.assert_equal(out, True, "ERR: Configure X2 Management failed!")
        #verify
        result_verify_access_rules = accessrule.verify_access_rule(access_rule='ssh', destination='All X2 Management IP')
        Assertion.assert_equal(result_verify_access_rules, False, "ERR: The SSH access rule is still here!")
        #test management deleted
        result_test_deleted = utils.test_management_function('ssh', 'off') # return failed = True
        Assertion.assert_equal(result_test_deleted, True, "ERR: -----------------SSH Management Function is still working!-------")



@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_12(Test):
    uuid = "SOSAIOT-TC-56179"
    description = show_testcase_info(Parameter.TESTPLAN, "12", description=True)['title']

    #show testplan
    def test_07_00_show_testplan(self):
        utils.log_testplan('12')

    def test_07_01_EnableUserLoginOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': True,
            'user_http': True,
            'user_https': False,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure x2 failed!")
        print("------------While API-on Can not open user_http---------------------")


class Test_Interface_13(Test):
    uuid = "SOSAIOT-TC-56180"
    description = show_testcase_info(Parameter.TESTPLAN, "13", description=True)['title']

    # show testplan
    def test_08_00_show_testplan(self):
        utils.log_testplan('13')

    def test_08_01_EnableUserLoginOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': True,
            'user_http': False,
            'user_https': True,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure x2 failed!")

    # add local user member of SNWL Admin
    def test_08_02_AddLocalUser(self):
        add_member_of_user = {
            'action': 'add',
            'username': 'test',
            'userpassword': 'S0nic@uto',
            'member_of': [
                'SonicWALL Administrators',
            ]
        }
        out = userLocal.local_user(**add_member_of_user)
        Assertion.assert_equal(out, True, "ERR: Add local user failed!")
        out_member = userLocal.user_member_of(**add_member_of_user)
        Assertion.assert_equal(out_member, True, "ERR: Add Local user of SNWL Admin failed!")

    @repeat_method(5)
    def test_08_03_UserLoginSuccess(self):
        api_dict = {
        'sonicos-api': True,               ### Bool
        'basic': True,                      ### Bool
        }
        sonic_api.sonicos_api(**api_dict)
        time.sleep(5)
        fw1 = Firewall(Parameter.X2_IP, user='test', password='S0nic@uto',supported_config_mode='api')
        out = fw1.api_login(check_login=False)
        Assertion.assert_equal(out, True, "ERR: Login Failed!")

    # Disable_User_Login_On_Interface
    def test_08_04_DisableUserLoginOnInterface(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_https': True,
            'user_http': False,
            'user_https': False,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure x2 user https failed!")

    # Test user login fail
    @repeat_method(5)
    def test_08_05_UserLoginFail(self):
        time.sleep(5)
        fw1 = Firewall(Parameter.X2_IP, user='test', password='S0nic@uto', supported_config_mode='api')
        out = ''.join(fw1.api_login())
        result = False
        if 'Login error' in out:
            result = True
        Assertion.assert_equal(result, True, "ERR: After shut down user_https User Still Can Login!")

    # Delete Local User
    def test_08_06_DeleteLocalUser(self):
        result = userLocal.delete_local_user_no_domain('test')
        logger.info(result)
        Assertion.assert_equal(result, True, "ERR: Delete local user failed!")



# HTTP now is forbidden
# @unittest.skipIf(Params.smk, 'Skip as this is a smk test')
# class Test_Interface_09(Test):
#     uuid = '1515724'
#     description = show_testcase_info(Parameter.TESTPLAN, "14", description=True)['title']

#     # show testplan
#     def test_09_00_show_testplan(self):
#         utils.log_testplan('14')

#     #              Test those method and login
#     #             'ldap'      ->  'ldap'
#     #             'radius+LocalUsers' -> 'radius-local'
#     #             'ldap+LocalUsers'  -> 'ldap-local'

#     #Set User Authentication -> LDAP
#     def test_09_01_UserAutentication_LDAP(self):
#         method = 'ldap'
#         out = utils.User_authen(method)
#         Assertion.assert_equal(out, True, "ERR: User setting LDAP failed!")

#     #Check user_http can not be checked
#     def test_09_02_CheckUserHttp(self):
#         #configure
#         x2_opt = {
#             'if': 'x2',
#             'zone': 'LAN',
#             'mode': 'static',
#             'ip': Parameter.X2_IP,
#             'mask': Parameter.Mask,
#             'user_http': True,
#             'user_https': True,
#         }
#         out = interface.config_interface(**x2_opt)
#         Assertion.assert_equal(out, True, "ERR: Configure X2 Failed!")
#         result = utils.User_http_Check()
#         Assertion.assert_equal(result, True, "ERR: User HTTP Can still be opened!")

#     #Set User Authentication -> LDAP+LOCAL
#     def test_09_03_UserAutentication_LdapLocal(self):
#         method = 'ldap-local'
#         out = utils.User_authen(method)
#         Assertion.assert_equal(out, True, "ERR: User setting LDAP+LOCAL failed!")
#         result = utils.User_http_Check()
#         Assertion.assert_equal(result, True, "ERR: User HTTP Can still be opened!")

#     #Set User Authentication -> radius+LocalUsers
#     def test_09_04_UserAutentication_RadiusLocal(self):
#         method = 'radius-local'
#         out = utils.User_authen(method)
#         Assertion.assert_equal(out, True, "ERR: User setting RADIUS+LOCAL failed!")
#         result = utils.User_http_Check()
#         Assertion.assert_equal(result, True, "ERR: User HTTP Can still be opened!")

#     #restor
#     def test_09_05_UserAuthentication_Local(self):
#         method = 'local'
#         out = utils.User_authen(method)
#         Assertion.assert_equal(out, True, "ERR: User setting Restore failed!")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_16(Test):
    uuid = "SOSAIOT-TC-56183"
    description = show_testcase_info(Parameter.TESTPLAN, "16", description=True)['title']

    # show testplan
    def test_10_00_show_testplan(self):
        utils.log_testplan('16')

    def test_10_01_ConfigureX1(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'mask': Parameter.Mask,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'user_https': True,
        }
        out = interface.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 failed!")

    #add local user with different privilege
    def test_10_02_AddLocalUserWithDifferentPrivilege(self):
        user_local_obj_a = {
            'action': 'add',
            'username': 'user-a',
            'userpassword': 'S0nic@uto',
        }
        # User - B with limited_administrators
        user_local_obj_b = {
            'action': 'add',
            'username': 'user-b',
            'userpassword': 'S0nic@uto',
            'member_of': [
                'Limited Administrators',
            ]
        }
        #User - C with administrators
        user_local_obj_c = {
            'action': 'add',
            'username': 'user-c',
            'userpassword': 'S0nic@uto',
            'member_of': [
                'SonicWALL Administrators',
            ]
        }
        out1 = userLocal.local_user(**user_local_obj_a)
        Assertion.assert_equal(out1, True, "ERR: Add local user a without any privileges failed!")

        out2 = userLocal.local_user(**user_local_obj_b)
        Assertion.assert_equal(out2, True, "ERR: Add local user b with Limited Administrators failed!")
        out_member_b = userLocal.user_member_of(**user_local_obj_b)
        Assertion.assert_equal(out_member_b, True, "ERR: Add Local user-b of Limited Administrators failed!")

        out3 = userLocal.local_user(**user_local_obj_c)
        Assertion.assert_equal(out3, True, "ERR: Add local user c with SonicWALL Administrators failed!")
        out_member_c = userLocal.user_member_of(**user_local_obj_c)
        Assertion.assert_equal(out_member_c, True, "ERR: Add Local user of SNWL Admin failed!")

    @repeat_method(5)
    def test_10_03_TestUserLogin(self):
        api_dict = {
        'sonicos-api': True,               ### Bool
        'basic': True,                      ### Bool
        }
        sonic_api.sonicos_api(**api_dict)
        time.sleep(5)
        #cant login
        fw1 = Firewall(Parameter.X1_IP, user='user-a', password='S0nic@uto',new_password='S0nic@uto', supported_config_mode='api')
        out = fw1.api_login(check_login=False)
        Assertion.assert_regular(out, r"Login error", 'ERR: User-a Still Can Login!')
        #User-B cant login
        fw2 = Firewall(Parameter.X1_IP, user='user-b', password='S0nic@uto',new_password='S0nic@uto', supported_config_mode='api')
        out = fw2.api_login(check_login=False)
        Assertion.assert_regular(out, r"Login error", 'ERR: User-a Still Can Login!')
        # User-C can login
        fw3 = Firewall(Parameter.X1_IP, user='user-c', password='S0nic@uto',new_password='S0nic@uto', supported_config_mode='api')
        out3 = fw3.api_login(check_login=False)
        Assertion.assert_equal(out3, True, "ERR: User-c Login failed!")

    #Delete local user a,b,c
    def test_10_04_DeleteUser(self):
        #Delete User A
        result1 = userLocal.delete_local_user_no_domain('user-a')
        logger.info(result1)
        Assertion.assert_equal(result1, True, "ERR: Delete user a failed!")
        #Delete User B
        result2 = userLocal.delete_local_user_no_domain('user-b')
        logger.info(result2)
        Assertion.assert_equal(result2, True, "ERR: Delete user b failed!")
        # Delete User C
        result3 = userLocal.delete_local_user_no_domain('user-c')
        logger.info(result3)
        Assertion.assert_equal(result3, True, "ERR: Delete user c failed!")



@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_19(Test):
    uuid = "SOSAIOT-TC-56186"
    description = show_testcase_info(Parameter.TESTPLAN, "19", description=True)['title']
    # show testplan
    def test_11_00_show_testplan(self):
        utils.log_testplan('19')

    def test_11_01_ConfigureWanInterface(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as WAN failed!")

    def test_11_02_AddAddressObj(self):
        #invalid address_obj1
        address_obj1 = {
            'object_type': 'range',
            'name': 'name1',
            'value': '192.168.1.1,192.168.1.100',
            'zone': 'LAN',
        }
        AddressObject.config_addressobject(**address_obj1)
        opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': 'group "WAN Subnets"',
        }
        out1 = interface.config_interface(**opt)
        Assertion.assert_equal(out1, False, "ERR: Invalid address_obj1!")

        #invalid address obj2
        address_obj2 = {
            'object_type': 'range',
            'name': 'name2',
            'value': '172.16.1.199,172.16.1.202',
            'zone': 'LAN',
        }
        AddressObject.config_addressobject(**address_obj2)

        out2 = interface.config_interface(**opt)
        Assertion.assert_equal(out2, False, "ERR: Invalid address_obj2!")

    #delete addrobj
    def test_11_04_DeleteAddressObj(self):
        out1 = AddressObject.delete_addressobject(object_type="range", object_path="name",
                                                object_name_uuid="name1", ip_type="ipv4")
        Assertion.assert_equal(out1, True, "ERR: Delete Address Object Failed!")

        out2 = AddressObject.delete_addressobject(object_type="range", object_path="name",
                                                object_name_uuid="name2", ip_type="ipv4")
        Assertion.assert_equal(out2, True, "ERR: Delete Address Object Failed!")


class Test_Interface_20(Test):
    uuid = "SOSAIOT-TC-56188"
    description = show_testcase_info(Parameter.TESTPLAN, "20", description=True)['title']

    # show testplan
    def test_12_00_show_testplan(self):
        utils.log_testplan('20')

    def test_12_01_ConfigureWanInterface(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as WAN failed!")

    # add addressObj
    def test_12_02_AddAddressObj(self):
        address_obj = {
            'object_type': 'range',
            'name': 'drres_range',
            'value': '172.16.1.2,172.16.1.5',
            'zone': 'LAN',
        }
        out = AddressObject.config_addressobject(**address_obj)
        Assertion.assert_equal(out, True, "ERR: Add Address Object Failed!")


    ##delete addrobj
    def test_12_04_DeleteAddressObj(self):
        out = AddressObject.delete_addressobject(object_type="range", object_path="name",
                                                 object_name_uuid="drres_range", ip_type="ipv4")
        Assertion.assert_equal(out, True, "ERR: Delete Address Object Failed!")


class Test_Interface_40(Test):
    uuid = "SOSAIOT-TC-56205"
    description = show_testcase_info(Parameter.TESTPLAN, "40", description=True)['title']

    #show testplan
    def test_13_00_show_testplan(self):
        utils.log_testplan('40')


    def test_13_01_ConfigurePPPoE(self):
        #backup
        setup.backup_pppoe()
        #configure
        out = setup.setup_pppoe_server_on_PC1()
        Assertion.assert_equal(out, True, "ERR: Can not configure PPPoE Server on PC1 eth2")

    def test_13_02_ConfigureX1_PPPOE(self):
        #In order to get wrong ip , clear logs at first
        Log.clear_log()
        time.sleep(10) #wait for clearing
        x1_pppoe_opt_dynamic = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'test',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': True,
            'pppoe_inactivity': 0,
            'pppoe_lcp_echo_packets': False,
            'pppoe_reconnect': 0,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
        }
        out = interface.config_interface(**x1_pppoe_opt_dynamic)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as pppoe failed!")

    @repeat_method(3)
    def test_13_03_TestPingPPPoEIP(self):
        time.sleep(10)
        ip = utils.GetPPPoEIP()
        result = ping(ip, count=5)
        Assertion.assert_equal(result, True, "ERR: Can not Ping {}".format(ip))


class Test_Interface_47(Test):
    uuid = "SOSAIOT-TC-56212"
    description = show_testcase_info(Parameter.TESTPLAN, "47", description=True)['title']

    # show testplan
    def test_14_00_show_testplan(self):
        utils.log_testplan('47')

    #configure pptp server
    def test_14_01_ConfigurePPTP(self):
        #backup
        setup.backup_pptp()
        #configure
        out = setup.setup_pptp_server_on_PC1()
        Assertion.assert_equal(out, True, "ERR: Configure PPTP Server on PC1 failed!")
        time.sleep(5)   #----wait for pptp server

    #configure
    def test_14_02_ConfigureX1_PPTP(self):
        x1_pptp_opt_dynamic = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'test',
            'pptp_passwd': 'password',
            'pptp_server': '172.16.1.10',
            'pppoe_schedule': 'always_on',
            'pppoe_dynamic': False,
            'pptp_ip': '172.16.1.20',
            'pptp_netmask': Parameter.Mask,
            'pptp_gateway': '172.16.1.10',
            'pppoe_inactivity': 10,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        out = interface.config_interface(**x1_pptp_opt_dynamic)
        Assertion.assert_equal(out,True,"ERR: Configure X1 as PPTP failed!")

    #Ping
    @repeat_method(3)
    def test_14_03_TestPingPPTPIP(self):
        time.sleep(5)
        out = utils.GetPPPIP()
        rc = localhost.send_command('ping {} -c 4'.format(out))
        Assertion.assert_not_regular(rc, r'100% packet loss', "ERR: Can not Ping {}".format(out))


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_15(Test):
    uuid = 'NonTC'

    def test_15_00_RestorePPPoEConfs(self):
        setup.restore_pppoe()

    def test_15_01_RestorePPTPConfs(self):
        setup.restore_pptp()


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_22(Test):
    uuid = "SOSAIOT-TC-56190"
    description = show_testcase_info(Parameter.TESTPLAN, "22", description=True)['title']

    # show testplan
    def test_16_00_show_testplan(self):
        utils.log_testplan('22')
    #Configuring X2
    def test_16_01_ConifgureX2(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'WLAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.Mask,
            'sp_limit': 8,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")


    def test_16_02_ConfigureX0(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to': 'x2',
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, False, "ERR: Default LAN can Bridge to the WLAN interface -> X2")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_29(Test):
    uuid = "SOSAIOT-TC-56196"
    description = show_testcase_info(Parameter.TESTPLAN, "29", description=True)['title']

    # show testplan
    def test_17_00_show_testplan(self):
        utils.log_testplan('29')

    def test_17_01_ConfigureX6(self):
        x6_opt = {
            'if': 'x6',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X6_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x6_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X6 failed!")

    def test_17_02_ConfigureX7(self):
        x7_opt = {
            'if': 'X7',
            'zone': 'LAN',# LAN, DMZ, custom zone name
            'mode': 'l2bridge',
            'bridge_to': 'X6',
            'block_non_ip': False,
            'mgmt_snmp': True,
            'mgmt_http':False,
            'mgmt_https': True,
            "https_redirect": False,
            'bridge_block_non_ip': False,
            'route_on_bridge_pair': True,
            'stateful_inspection':True,#修改了 network 822-824
            'vlan_filtering_mode': 'block',  #allow, block
            'filter_vlans': [ ],
        }
        out = interface.config_interface(**x7_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X7 failed!")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_25(Test):
    uuid = "SOSAIOT-TC-56192"
    description = show_testcase_info(Parameter.TESTPLAN, "25", description=True)['title']

    # show testplan
    def test_18_00_show_testplan(self):
        utils.log_testplan('25')

    def test_18_01_ConfigureX2(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'dhcp',
            'ip': Parameter.X2_IP,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    def test_18_02_L2BridgeX0toX2(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to': 'x2',
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, False, "ERR: Lan interface X0 can l2 to WAN -DHCP interface X2!")


class Test_Interface_26(Test):
    uuid = "SOSAIOT-TC-56193"
    description = show_testcase_info(Parameter.TESTPLAN, "26", description=True)['title']

    # show testplan
    def test_19_00_show_testplan(self):
        utils.log_testplan('26')

    def test_19_01_ConfigureX2(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    def test_19_02_ConfigureX3(self):
        time.sleep(5)
        x3_opt = {
            'if': 'X3',
            'zone': 'LAN',# LAN, DMZ, custom zone name
            'mode': 'l2bridge',
            'bridge_to': 'X2',
            'block_non_ip': False,
            'mgmt_snmp': True,
            'mgmt_http':False,
            'mgmt_https': True,
            "https_redirect": False,
            'bridge_block_non_ip': False,
            'route_on_bridge_pair': True,
            'stateful_inspection':True,#修改了 network 822-824
            'vlan_filtering_mode': 'block',  #allow, block
            'filter_vlans': [ ],
        }
        out = interface.config_interface(**x3_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X3 failed!")

    # Verify l2bridgeMode Success
    def test_19_03_VerifyL2bridgeMode(self):
        result = utils.VerifyL2bridgeMode('X3', 'X2')
        Assertion.assert_equal(result, True, "ERR: Interface x3 is not bridge to x2")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_28(Test):
    uuid = "SOSAIOT-TC-56195"
    description = show_testcase_info(Parameter.TESTPLAN, "28", description=True)['title']

    # show testplan
    def test_20_00_show_testplan(self):
        utils.log_testplan('28')

    def test_20_01_ConfigureX4(self):
        x4_opt = {
            'if': 'x4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x4_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X4 failed!")

    def test_20_02_ConfigureX5(self):
        x5_opt = {
            'if': 'X5',
            'zone': 'LAN',# LAN, DMZ, custom zone name
            'mode': 'l2bridge',
            'bridge_to': 'X4',
            'block_non_ip': False,
            'mgmt_snmp': True,
            'mgmt_http':False,
            'mgmt_https': True,
            "https_redirect": False,
            'bridge_block_non_ip': False,
            'route_on_bridge_pair': True,
            'stateful_inspection':True,#修改了 network 822-824
            'vlan_filtering_mode': 'block',  #allow, block
            'filter_vlans': [ ],
        }
        out = interface.config_interface(**x5_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X5 failed!")


@unittest.skipIf(Params.smk, 'Skip as this is a smk test')
class Test_Interface_23(Test):
    uuid = "SOSAIOT-TC-56191"
    description = show_testcase_info(Parameter.TESTPLAN, "23", description=True)['title']

    # show testplan
    def test_21_00_show_testplan(self):
        utils.log_testplan('23')

    def test_21_01_ConfigureX2(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")


    #Disable x0 lease scope
    def test_21_02_DisableX0LeaseScope(self):
        cmds = ['configure', 'dhcp-server','scope dynamic 192.168.168.1 192.168.168.167','no enable','commit', 'exit', 'exit', 'exit']
        (rc, output) = fw_cli.do_cli_commands(cmds, 1)
        if rc == False:
            logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: Disable X0 DHCP Lease Scope Failed!")

    def test_21_03_L2BridgeX0toX2(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to': 'x2',
        }
        X3_opt = {
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '192.168.11.10',
            'netmask': Parameter.Mask,
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, False, "ERR: DHCP Enable On primary bridge interface can still be l2 to X2!")
        out = interface.config_interface(**X3_opt)
        Assertion.assert_equal(out, True, "ERR: config X3 failed")

    #Disable X2 LeasScope
    def test_21_04_DisableX2LeaseScope(self):
        cmds = ['configure', 'dhcp-server', 'scope dynamic 192.168.10.1 192.168.10.199', 'no enable', 'netmask 255.255.255.0', 'commit', 'exit','exit','exit']
        (rc, output) = fw_cli.do_cli_commands(cmds, 1)
        if rc == False:
            logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: Disable X2 DHCP Lease Scope Failed!")

    def test_21_05_EnableX0LeaseScope(self):
        cmds = ['configure', 'dhcp-server', 'scope dynamic 192.168.10.1 192.168.10.199', 'enable', 'commit', 'exit' ,'exit', 'exit']
        (rc, output) = fw_cli.do_cli_commands(cmds, 1)
        if rc == False:
            logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: Disable X2 DHCP Lease Scope Failed!")

    def test_21_06_L2BridgeX0toX2(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'l2bridge',
            'bridge_to': 'x2',
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, False, "ERR: No enable X2 lease scope still can be l2 to")


class Test_Interface_69(Test):
    uuid = "SOSAIOT-TC-56234"
    description = show_testcase_info(Parameter.TESTPLAN, '69', description=True)['title']

    def test_22_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '69')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_22_01_configX2_static(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_ping': True,
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    def test_22_02_ping(self):
        rc = localhost.send_command('ping {} -c 4'.format(Parameter.X2_IP))
        Assertion.assert_not_regular(rc, r'100% packet loss', "ERR: Can not Ping {}".format(Parameter.X2_IP))

    @repeat_method(5)
    def test_22_03_configX2_DHCP(self):
        x2_dhcp = {
            'if': 'x2',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        output = interface_obj.config_interface(**x2_dhcp)
        Assertion.assert_equal(output, True, "ERR: Configure X2 status to DHCP failed")

    def test_22_04_start_dhcp_server(self):
        flag = False
        for i in range(1,5):
            conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Interface_168/confs/dhcpd.conf';
            ret = localhost.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
            ret = ret + localhost.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
            ret = ret + localhost.send_command("service dhcpd restart")
            logger.info(ret)
            status = localhost.send_command("service dhcpd status")
            logger.info(status)
            if re.search(r'is running', status, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC1 failed")

    def test_22_05_get_X2_address(self):
        x2="0.0.0.0"
        for i in range(0, 5):
            info_x2 = interface_obj.get_interface_address('X2')
            if info_x2['ip_address'] == '0.0.0.0':
                time.sleep(5)
            else:
                x2 = info_x2['ip_address']
                break
        logger.info("X1 DHCP ip is {}".format(x2))
        Assertion.assert_not_regular(x2, '0.0.0.0', "ERR: X2 get dhcp address failed")

    def test_22_06_unassigned_X2(self):
        out = interface.unassign_interface(interface='X2')
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")


class Test_Interface_70(Test):
    uuid = "SOSAIOT-TC-56236"
    description = show_testcase_info(Parameter.TESTPLAN, '70', description=True)['title']

    def test_23_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '70')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_01_config_LAN_ip(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_ping': True
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    def test_23_02_configX1(self):
        x1_opt = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'mask': Parameter.Mask,
            'mgmt_ping': True
        }
        out = interface.config_interface(**x1_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 as WAN failed!")

    def test_23_03_ping_LAN_to_LAN(self):
        rc = localhost.send_command('ping {} -c 10'.format(Parameter.X2_IP))
        Assertion.assert_regular(rc, r'time=[0,1,2,3,4,5,6,7]\.', "ERR: Can not Ping {}".format(Parameter.X2_IP))

    def test_23_04_ping_LAN_to_WAN(self):
        rc = localhost.send_command('ping {} -c 10'.format(PC2_ETH1_IP))
        Assertion.assert_regular(rc, r'time=[0,1]\.', "ERR: Can not Ping {}".format(PC2_ETH1_IP))

    
class Test_Interface_71(Test):
    uuid = "SOSAIOT-TC-56237"
    description = show_testcase_info(Parameter.TESTPLAN, '71', description=True)['title']

    def test_24_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_24_01_unassign_interface_x3_and_x4(self):
        out = interface.unassign_interface(interface='X7')
        out &= interface.unassign_interface(interface='X6')
        out &= interface.unassign_interface(interface='X5')
        out &= interface.unassign_interface(interface='X3')
        out &= interface.unassign_interface(interface='X4')
        Assertion.assert_equal(out, True, "ERR: unassign X3 and X4 failed!")

    def test_24_02_config_x3(self):
        x3_opt = {
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'unnumbered',
        }
        out = interface.config_interface(**x3_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X3 failed!")

    def test_24_03_config_x4(self):
        x4_opt = {
            'if': 'x4',
            'zone': 'DMZ',
            'mode': 'unnumbered',
        }
        out = interface.config_interface(**x4_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X4 failed!")

    def test_24_04_check_config(self):
        flage=False
        x3 = interface.get_interface_status("X3")
        x4 = interface.get_interface_status("X4")
        if re.findall("'zone': 'LAN', 'mode': {'unnumbered'",str(x3)) and re.findall("{'zone': 'DMZ', 'mode': {'unnumbered'",str(x4)):
            flage=True
        Assertion.assert_equal(flage, True, "ERR: check x3 and x4 failed")

    def test_24_05_unassign_x3_x4(self):
        out = interface.unassign_interface(interface='X3')
        out &= interface.unassign_interface(interface='X4')
        Assertion.assert_equal(out, True, "ERR: unassign X3 and X4 failed!")


class Test_Interface_30(Test):
    uuid = "SOSAIOT-TC-56198"
    description = show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']

    def test_25_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_25_01_config_x2(self):
        x2_opt = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mask': Parameter.Mask,
            'mgmt_ping': True
        }
        out = interface.config_interface(**x2_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X2 failed!")

    def test_25_02_change_route_for_pc2(self):
        pc2.send_command('route add -net 192.168.10.0 netmask 255.255.255.0 gw 172.16.1.200')
        out =pc2.send_command('route -n')
        Assertion.assert_regular(out, r'192.168.10.0\s+?172.16.1.200', "ERR: change route on mail server failed")
    
    def test_25_03_change_route_for_pc1(self):
        localhost.send_command('route add -net 172.16.1.0 netmask 255.255.255.0 gw 192.168.10.200')
        out =localhost.send_command('route -n')
        Assertion.assert_regular(out, r'172.16.1.0\s+?192.168.10.200', "ERR: change route on mail server failed")

    def test_25_04_config_acl(self):
        rule_opt = {
            'name': 'LAN_TO_WAN',
            'enable': True,
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'source': {
                "address":{
                    'any': True},
                "port":{"any":True}
            },
            'destination': {
                "address":{
                    "name":"X1 Subnet"},
            },
            'service': { 'any': True },
            'schedule': {"always_on": True},
            'users': {'included': {'group': 'Limited Administrators'}, 'excluded': {'none': True}},
            'geo_ip_filter': {'enable': False, 'global': True},
            'priority': { 'auto': True }
        }
        rc = acrObj.config_accessrule(**rule_opt)
        Assertion.assert_equal(rc, True, "ERR: Add accessrule LAN to WAN failed")
    
    def test_25_05_check_ping(self):
        rc = localhost.send_command('ping {} -c 5'.format(PC2_ETH1_IP))
        Assertion.assert_regular(rc, r'100% packet loss', "ERR: Ping {} is still allowed".format(Parameter.X2_IP))

    def test_25_06_get_icmp_from_pc2(self):
        package_cap.clear_packets()
        sleep(1)
        package_cap.start_capture()
        sleep(1)
        rc = localhost.send_command('ping {} -c 5'.format(PC2_ETH1_IP))
        package_cap.stop_capture()
        Assertion.assert_regular(rc, r'100% packet loss', "ERR: icmp packet not lost")
        
    @repeat_method(5)
    def test_25_07_export_packet(self): 
        pack = package_cap.export_captured_packets()
        rc = re.findall(r"X2.*interface.*DROPPED, Drop",pack)
        logger.info(rc)
        if rc:
            flage=True
        Assertion.assert_equal(flage, True, "ERR: check packege fialed")

    def test_25_08_del_acl(self):
        rc = acrObj.delete_accessrule_by_name("LAN_TO_WAN")
        Assertion.assert_equal(rc, True, "ERR: del accessrule LAN to WAN failed")

    def test_25_09_del_route_on_pc2(self):
        pc2 = Host(PC2_ETH1_IP)
        pc2.send_command('route del -net 192.168.10.0 netmask 255.255.255.0 gw 172.16.1.200')
        out =pc2.send_command('route -n')
        Assertion.assert_not_regular(out, r'192.168.10.0\s+?172.16.1.200', "ERR: change route on mail server failed")

    def test_25_10_del_route_on_pc1(self):
        localhost.send_command('route del -net 172.16.1.0 netmask 255.255.255.0 gw 192.168.10.200')
        out =localhost.send_command('route -n')
        Assertion.assert_not_regular(out, r'172.16.1.0\s+?192.168.10.200', "ERR: change route on mail server failed")


class Test_Interface_15(Test):
    uuid = "SOSAIOT-TC-56182"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_26_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_26_01_config_x0(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': "192.168.168.168",
            'mask': "255.255.255.0",
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
            'https_redirect': True,
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 with redirect failed!")

    def test_26_02_check_with_x0(self):
        out =localhost.send_command('curl http://192.168.168.168')
        Assertion.assert_regular(out, r'This page is redirecting! Click <A HREF="https://192.168.168.168/sonicui/7/login/', "ERR: check x0 with redirect failed")

    def test_26_03_config_x0_without_redirect(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': "192.168.168.168",
            'mask': "255.255.255.0",
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
            'https_redirect': False,
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X1 without redirect failed!")

    def test_26_04_check_with_x0(self):
        out =localhost.send_command('curl http://192.168.168.168')
        Assertion.assert_regular(str(out), '', "ERR: check x0 without redirect failed")

    def test_26_05_recover_X0(self):
        x0_opt = {
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': "192.168.168.168",
            'mask': "255.255.255.0",
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
            'https_redirect': True,
        }
        out = interface.config_interface(**x0_opt)
        Assertion.assert_equal(out, True, "ERR: Configure X0 with redirect failed!")


class Test_Interface_36(Test):
    uuid = "SOSAIOT-TC-56201"
    description = show_testcase_info(Parameter.TESTPLAN, '36', description=True)['title']

    def test_27_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_27_01_config_x2_to_DHCP(self):
        x1_dhcp = {
            'if': 'x1',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        output = interface_obj.config_interface(**x1_dhcp)
        Assertion.assert_equal(output, True, "ERR: Configure X1 status to DHCP failed")

    def test_27_02_start_dhcp_server(self):
        flag = False
        for i in range(1,5):
            conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/Network/Interface_168/confs/dhcpd.conf_X1';
            ret = localhost.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
            ret = ret + localhost.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
            ret = ret + localhost.send_command("service dhcpd restart")
            logger.info(ret)
            status = localhost.send_command("service dhcpd status")
            logger.info(status)
            if re.search(r'is running', status, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC1 failed")

    def test_27_03_get_X2_address(self):
        log_obj.clear_log()
        x1="0.0.0.0"
        for i in range(0, 5):
            interface_obj.click_dhcp_release(name='X1')
            interface_obj.click_dhcp_renew(name='X1')
            info_x1 = interface_obj.get_interface_address('X1')
            if info_x1['ip_address'] == '0.0.0.0':
                time.sleep(5)
            else:
                x1 = info_x1['ip_address']
                break
        logger.info("X1 DHCP ip is {}".format(x1))
        Assertion.assert_not_regular(x1, '0.0.0.0', "ERR: X1 get dhcp address failed")

    def test_27_04_ping_WAN_ip(self):
        info_x1 = interface_obj.get_interface_address('X1')
        x1 = info_x1['ip_address']
        rc = localhost.send_command('ping {} -c 4'.format(x1))
        Assertion.assert_not_regular(rc, r'100% packet loss', "ERR: Can not Ping {}".format(x1))

    def test_27_05_check_log(self):
        log = log_obj.show_log()
        Assertion.assert_regular(str(log),r'X1.*Wan IP Changed', 'ERR: Check log failed')


class Test_Interface_53(Test):
    uuid = "SOSAIOT-TC-56219"
    description = show_testcase_info(Parameter.TESTPLAN, '53', description=True)['title']

    def test_28_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '53')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_28_01_install_Xl2tpd(self):
        conf_path=os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/'
        localhost.send_command('yum install -y libreswan')
        localhost.send_command('yum install -y epel-release')
        localhost.send_command('yum install -y xl2tpd')
        localhost.send_command('cp {} /etc/xl2tpd/xl2tpd.conf'.format(conf_path +'confs/xl2tpd.conf'))
        localhost.send_command('service xl2tpd start')
        rc = localhost.send_command('service xl2tpd status')
        logger.info(rc)
        Assertion.assert_regular(rc,r'xl2tpd.*is running', 'ERR: Check xl2tpd server failed')

    def test_28_02_config_x1_dhcp(self):
        x1_l2tp_static_dict = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'l2tp',
            'l2tp_server': '172.16.1.10',
            'l2tp_ip': 'dynamic',
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'l2tp_user': 'test',
            'l2tp_passwd':'password'
            }
        output = interface_obj.config_interface(**x1_l2tp_static_dict)
        Assertion.assert_equal(output, True, "ERR: Configure X1 status to DHCP failed")

    def test_28_03_check_ip(self):
        x1="0.0.0.0"
        interface_obj.get_interface_address('X1')
        for i in range(0, 5):
            info_x1 = interface_obj.get_interface_address('X1')
            if info_x1['ip_address'] == '0.0.0.0':
                time.sleep(5)
            else:
                x1 = info_x1['ip_address']
                break
        logger.info("X1 DHCP ip is {}".format(x1))
        Assertion.assert_not_regular(x1, '0.0.0.0', "ERR: X1 get dhcp address failed")

    def test_28_04_check_ping(self):
        info_x1 = interface_obj.get_interface_address('X1')
        x1 = info_x1['ip_address']
        rc = localhost.send_command('ping {} -c 4'.format(x1))
        Assertion.assert_not_regular(rc, r'100% packet loss', "ERR: Can not Ping {}".format(x1))

    def test_28_05_config_x1_static(self):
        x1_l2tp_static_dict = {
                'if': 'x1',
                'zone': 'WAN',
                'mode': 'l2tp',
                'l2tp_server': '172.16.1.10',
                'l2tp_ip': '172.16.1.100',
                'l2tp_gateway': '172.16.1.1',
                'mgmt_https': True,
                'mgmt_snmp': True,
                'mgmt_ping': True,
                'l2tp_user': 'test',
                'l2tp_passwd':'password'
                }
        output = interface_obj.config_interface(**x1_l2tp_static_dict)
        Assertion.assert_equal(output, True, "ERR: Configure X1 status to DHCP failed")

    @repeat_method(5)
    def test_28_06_check_ping(self):
        sleep(2)
        rc = localhost.send_command('ping 172.16.1.100 -c 4')
        Assertion.assert_not_regular(rc, r'100% packet loss', "ERR: Can not Ping 172.16.1.100")

        