import sys
import os
import json

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/Tacacs_user/Tacacs_API/')
from definition.settings import *


class Test_API_Tacacs_base_01(Test):
    uuid = "SOSAIOT-TC-47847"
    description = show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516309')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_tacacs_base(self):
        add_tacacsuser = {
            'local_users_only': True,
            'default_user_group': "",
            'timeout': 6,
            'retries': 10,
            'user_group_mechanism': {
                'local_only': True
            }
        }
        resp = Tacacs_user.user_tacacs_base_settings(**add_tacacsuser)
        logger.info(resp)
        response_get = Tacacs_user.show_tacacs_base_settings()
        Assertion.assert_regular(json.dumps(response_get), '"local_users_only": false',
                                 'Error: Failed to create Tacacs user')


class Test_API_Tacacs_base_02(Test):
    uuid = "SOSAIOT-TC-47848"
    description = show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516310')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_get_tacacs_base(self):
        response = Tacacs_user.show_tacacs_base_settings()
        logger.info(response)
        expected_output = response['user']['tacacs']['local_users_only']
        Assertion.assert_regular(json.dumps(response), str(expected_output), "ERROR: Failed to get Tacacs base")


class Test_API_Tacacs_base_03(Test):
    uuid = "SOSAIOT-TC-47851"
    description = show_testcase_info(Parameter.TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516313')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_tacacs_base(self):
        add_tacacs_server_dict = {
            'host': '192.168.168.83',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        # Adding the Tacacs_user server
        logger.info("..............Adding the Tacacs_user server...............")
        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs_user user is not created successfully")
        tacacs_user_info = Tacacs_user.show_tacacs_server()
        logger.info(tacacs_user_info)
        Assertion.assert_regular(json.dumps(tacacs_user_info), '"port": 49', 'Error: Failed to create Radius server')


class Test_API_Tacacs_base_04(Test):
    uuid = "SOSAIOT-TC-47852"
    description = show_testcase_info(Parameter.TESTPLAN, '04', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516314')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_tacacs_base(self):
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        edit_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 50,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        # Adding the Tacacs_user server
        logger.info("..............Adding the Tacacs_user server...............")
        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs user is not created successfully")
        tacacs_user_info = Tacacs_user.show_tacacs_server()
        logger.info(tacacs_user_info)
        # Edit the Tacacs_user server
        logger.info("..............Edit the Tacacs_user Server....................")
        tacacs_user_edit = Tacacs_user.edit_tacacs_server(**edit_tacacs_server_dict)
        response_get = Tacacs_user.show_tacacs_server()
        Assertion.assert_regular(json.dumps(response_get), '"port": 50', 'Error: Failed to create Tacacs server')


class Test_API_Tacacs_base_05(Test):
    uuid = "SOSAIOT-TC-47853"

    description = show_testcase_info(Parameter.TESTPLAN, '05', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516315')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_tacacs_base(self):
        tacacs_user = Tacacs_user.show_tacacs_server_name(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_regular(json.dumps(tacacs_user), '"host": "192.168.168.85"', "ERR: tacacs_user is not present")


class Test_API_Tacacs_base_06(Test):
    uuid = "SOSAIOT-TC-47854"
    description = show_testcase_info(Parameter.TESTPLAN, '06', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516316')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_tacacs_base(self):
        edit_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        tacacs_user_edit = Tacacs_user.edit_tacacs_server(**edit_tacacs_server_dict, name="192.168.168.85")
        response_get = Tacacs_user.show_tacacs_server()
        Assertion.assert_regular(json.dumps(response_get), '"port": 49', 'Error : Failed to edit Tacacs server')


class Test_API_Tacacs_base_07(Test):
    uuid = "SOSAIOT-TC-47855"
    description = show_testcase_info(Parameter.TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516317')
        Assertion.assert_equal(True, True, "Error: show testcase info failed")

    def test_07_tacacs_base(self):
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.85")
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "Error : Tacacs server is not deleted successfully")


class Test_API_Tacacs_base_08(Test):
    uuid = "SOSAIOT-TC-47856"
    description = show_testcase_info(Parameter.TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516318')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_08_tacacs_base(self):
        edit_tacacs_server_dict = {
            'host': '192.168.168.86',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 50,
            'secret': 'sonicwall',
            'send_through_vpn_tunnel': False,

        }

        # Adding the Tacacs_user server
        logger.info("..............Adding the Tacacs_user server...............")
        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs Server is not created successfully")
        tacacs_user_info = Tacacs_user.show_tacacs_server()
        logger.info(tacacs_user_info)

        tacacs_user_edit = Tacacs_user.edit_tacacs_server(**edit_tacacs_server_dict)
        response_get = Tacacs_user.show_tacacs_server()
        Assertion.assert_regular(json.dumps(response_get), '"host": "192.168.168.86"',
                                 'ERROR: Failed to edit Tacacs server')


class Test_API_Tacacs_base_09(Test):
    uuid = "SOSAIOT-TC-47857"
    description = show_testcase_info(Parameter.TESTPLAN, '09', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516319')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_09_tacacs_base(self):
        edit_tacacs_server_dict = {
            'host': '192.168.168.86',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        tacacs_user_edit = Tacacs_user.edit_tacacs_server(**edit_tacacs_server_dict, name="192.168.168.89")
        logger.info("The user created is {}".format(tacacs_user_edit))
        Assertion.assert_equal(json.dumps(tacacs_user_edit), "false", "Error : tacacs_user is not present")
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.86")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs Server is not deleted successfully")


class Test_API_Tacacs_base_10(Test):
    uuid = "SOSAIOT-TC-47858"
    description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516320')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_tacacs_base(self):
        tacacs_user = Tacacs_user.show_tacacs_server_name(tacacsserver_name="192.168.168.88")
        logger.info("The user created is {}".format(tacacs_user))
        error_message_value = tacacs_user['status']['info'][0]['message']
        # Assertion.assert_regular(error_message_value, "Command 'show user tacacs server 192.168.168.88' does not match",
        #                          "ERROR: Tacacs is not present")
        Assertion.assert_regular(error_message_value, "'192.168.168.88' not a reasonable value", "ERROR: Tacacs is not present")



class Test_API_Tacacs_base_11(Test):
    uuid = "SOSAIOT-TC-47859"
    description = show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516321')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_tacacs_base(self):
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.88")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, False, "ERROR: Tacacs_user is not deleted successfully")


class Test_API_Tacacs_base_12(Test):
    uuid = "SOSAIOT-TC-47862"
    description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516324')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_12_tacacs_base(self):
        tacacs_acc_base = Tacacs_user.show_tacacs_accounts_base()
        print(tacacs_acc_base)
        logger.info("The Tacacs_user accounting  is {}".format(tacacs_acc_base))
        expected_output = tacacs_acc_base['user']['tacacs']['accounting']
        Assertion.assert_regular(str(tacacs_acc_base), str(expected_output),
                                 "ERROR : Unable to get Tacacs account base details")


# Get accounting server
class Test_API_Tacacs_base_13(Test):
    uuid = "SOSAIOT-TC-47865"

    description = show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516327')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_13_tacacs_base(self):
        tacacs_acc = Tacacs_user.show_tacacs_accounts()
        logger.info("The Tacacs_user accounting  is {}".format(tacacs_acc))
        expected_output = tacacs_acc['user']['tacacs']
        Assertion.assert_regular(str(tacacs_acc), str(expected_output),
                                 "ERROR : Unable to get Tacacs_user account base details")


class Test_API_Tacacs_base_14(Test):
    uuid = "SOSAIOT-TC-47867"
    description = show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516329')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_15_tacacs_base(self):
        tacacs_account = {
            "enable": True,
            "host": "192.168.168.65",
            "port": 1813,
            "shared_secret": "luckyday",
            "user_name_format": {'down_level_logon': True}
        }
        res = Tacacs_user.add_tacacs_account(**tacacs_account)
        Assertion.assert_equal(res, True, "ERROR: Add TACACS+ accounting server failed.")
        tacacs_acc = Tacacs_user.show_tacacs_account_name(tacacsaccount_name="192.168.168.65")
        logger.info("The user created is {}".format(tacacs_acc))
        Assertion.assert_regular(json.dumps(tacacs_acc), '"host": "192.168.168.65"',
                                 "ERROR: Tacacs account is not present")


class Test_API_Tacacs_base_15(Test):
    uuid = "SOSAIOT-TC-47869"
    description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516331')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_15_tacacs_base(self):
        tacacs_user = Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.65")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs account is not deleted successfully")


class Test_API_Tacacs_base_16(Test):
    uuid = "SOSAIOT-TC-47873"
    description = show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516335')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_16_tacacs_base(self):
        tacacs_user = Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.64")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, False, "ERROR : Fake Tacacs account is deleted")


class Test_API_Tacacs_base_17(Test):
    uuid = "SOSAIOT-TC-47872"
    description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516334')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_tacacs_base(self):
        tacacs_user = Tacacs_user.show_tacacs_account_name(tacacsaccount_name="192.168.168.88")
        logger.info("The user created is {}".format(tacacs_user))
        error_message_value = tacacs_user['status']['info'][0]['message']
        # Assertion.assert_regular(error_message_value,
        #                          "Command 'show user tacacs accounting server 192.168.168.88' does not match",
        #                          "ERR: tacacs_user is not present")
        Assertion.assert_regular(error_message_value, "'192.168.168.88' not a reasonable value", "ERROR: Tacacs is not present")



class Test_API_Tacacs_base_18(Test):
    uuid = "SOSAIOT-TC-47866"
    description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516328')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_18_tacacs_base(self):
        for i in range(0, 2):
            add_tacacs_server_dict = {
                'host': f'192.168.168.8{i}',
                'enable': True,
                'port_num': 49 + i,
                'secret': 'password',
                'send_through_vpn_tunnel': False,

            }
            # Adding the Tacacs_user server
            logger.info("..............Adding the Tacacs_user server...............")
            tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
            logger.info("The user created is {}".format(tacacs_user))
            Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs server is not created successfully")

        for i in range(0, 2):
            edit_tacacs_server_dict = {
                'host': f'192.168.168.8{i}',
                'enable': True,
                'port_num': 51 + i,
                'secret': 'password',
                'send_through_vpn_tunnel': False,

            }
            # Edit the Tacacs_user server
            logger.info("..............Edit the Tacacs_user Server....................")
            tacacs_user_edit = Tacacs_user.edit_tacacs_server(**edit_tacacs_server_dict)
            response_get = Tacacs_user.show_tacacs_server()
            Assertion.assert_regular(json.dumps(response_get), f'"port": {51 + i}',
                                     'err: Failed to create Radius server')
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.80")
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.81")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs server is not deleted successfully")


class Test_API_Tacacs_base_19(Test):
    uuid = "SOSAIOT-TC-47849"
    description = show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516311')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_19_tacacs_base(self):
        add_tacacs_server_dict = {
            'host': '192.168.168.89',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }
        # Adding the Tacacs_user server
        logger.info("..............Adding the Tacacs_user server...............")
        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: Tacacs sever is not created successfully")
        tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.89")
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs server is not deleted successfully")


class Test_API_Tacacs_base_20(Test):
    uuid = "SOSAIOT-TC-47850"
    description = show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516312')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_20_tacacs_base(self):
        for i in range(3, 5):
            add_tacacs_server_dict = {
                'host': f'192.168.168.8{i}',
                'enable': True,
                'port_num': 49 + i,
                'secret': 'password',
                'send_through_vpn_tunnel': False,

            }
            # Adding the Tacacs server
            logger.info("..............Adding the Tacacs_user server...............")
            tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
            logger.info("The user created is {}".format(tacacs_user))
            Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs user is not created successfully")
            tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.83")
            tacacs_user = Tacacs_user.del_tacacs_server(tacacsserver_name="192.168.168.84")


class Test_API_Tacacs_base_21(Test):
    uuid = "SOSAIOT-TC-47863"
    description = show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516325')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_21_tacacs_base(self):
        tacacs_account = {
            "enable": True,
            "host": "192.168.168.67",
            "port": 1813,
            "shared_secret": "luckyday",
            "user_name_format": {'down_level_logon': True}
        }
        res = Tacacs_user.add_tacacs_account(**tacacs_account)
        Assertion.assert_equal(res, True, "ERR: Add TACACS+ accounting server failed.")
        tacacs_user = Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.67")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR: Tacacs_user account is not deleted successfully")


# not completed
class Test_API_Tacacs_base_22(Test):
    uuid = "SOSAIOT-TC-47864"
    description = show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516326')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_22_tacacs_base(self):
        for i in range(3, 6):
            tacacs_account = {
                "enable": True,
                "host": f'192.168.168.6{i}',
                "port": 1813,
                "shared_secret": "luckyday",
                "user_name_format": {'down_level_logon': True}
            }
            res = Tacacs_user.add_tacacs_account(**tacacs_account)
            Assertion.assert_equal(res, True, "ERR: Add TACACS+ accounting server failed.")
            Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.63")
            Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.64")
            Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.65")


class Test_API_Tacacs_base_23(Test):
    uuid = "SOSAIOT-TC-47870"
    description = show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516332')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_23_tacacs_base(self):
        tacacs_account = {
            "enable": True,
            "host": "192.168.168.82",
            "port": 1813,
            "shared_secret": "luckyday",
        }
        res = Tacacs_user.add_tacacs_account(**tacacs_account)
        Assertion.assert_equal(res, True, "ERR: Add TACACS+ accounting server failed.")
        response_get = Tacacs_user.show_tacacs_accounts()
        edit_tacacs_server_dict = {
            'host': "192.168.168.85",
            'enable': True,
            'port_num': 49,
            'secret': 'password',
        }
        # Edit the Tacacs_user server
        logger.info("..............Edit the Tacacs_user Server....................")
        tacacs_user_edit = Tacacs_user.edit_tacacs_accounting(**edit_tacacs_server_dict)
        response_get = Tacacs_user.show_tacacs_accounts()
        Assertion.assert_regular(json.dumps(response_get), '"port": 49', 'err: Failed to create Radius server')


class Test_API_Tacacs_base_24(Test):
    uuid = "SOSAIOT-TC-47871"
    description = show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516333')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_24_tacacs_base(self):
        edit_tacacs_account = {
            'host': "192.168.168.85",
            'enable': True,
            'port_num': 49,
            'secret': 'luckyday',
        }
        # Edit the Tacacs_user server
        logger.info("..............Edit the Tacacs_user Server....................")
        tacacs_user_edit = Tacacs_user.edit_tacacs_accounting(**edit_tacacs_account, name="192.168.168.69")
        logger.info("The user created is {}".format(tacacs_user_edit))
        Assertion.assert_equal(json.dumps(tacacs_user_edit), "false", "Error : TACACS Accounting server is not present")


class Test_API_Tacacs_base_25(Test):
    uuid = "SOSAIOT-TC-47868"
    description = show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516330')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_25_tacacs_base(self):
        edit_tacacs_account = {
            'host': "192.168.168.85",
            'enable': True,
            'port_num': 51,
            'secret': 'password',
        }
        # Edit the Tacacs_user server
        logger.info("..............Edit the Tacacs_user Server....................")
        tacacs_user_edit = Tacacs_user.edit_tacacs_accounting(**edit_tacacs_account, name="192.168.168.85")
        response_get = Tacacs_user.show_tacacs_accounts()
        Assertion.assert_regular(json.dumps(response_get), '"port": 51', 'Error : Failed to Edit Tacacs accounting ')
        Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.85")


class Test_API_Tacacs_base_26(Test):
    uuid = "SOSAIOT-TC-47860"
    description = show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516322')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_26_tacacs_base(self):
        # Create tacacs server
        add_tacacs_server_dict = {
            'host': '192.168.168.85',
            'enable': True,
            'port_num': 49,
            'secret': 'password',
            'send_through_vpn_tunnel': False,

        }

        tacacs_user = Tacacs_user.add_tacacs_server(**add_tacacs_server_dict)
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERR: TACACS Server is not created successfully")
        tacacs_user_info = Tacacs_user.show_tacacs_server()
        logger.info(tacacs_user_info)
        time.sleep(10)
        tacacs_user = Tacacs_user.test_tacacs_server()
        Assertion.assert_equal(tacacs_user, True, "ERROR: TACACS Server test got failed")


class Test_API_Tacacs_base_27(Test):
    uuid = "SOSAIOT-TC-47874"
    description = show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516336')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_27_tacacs_base(self):
        tacacs_account = {
            "enable": True,
            "host": "192.168.168.85",
            "port": 49,
            "shared_secret": "password",
            "user_name_format": {'down_level_logon': True}
        }
        res = Tacacs_user.add_tacacs_account(**tacacs_account)
        Assertion.assert_equal(res, True, "ERR: Add TACACS+ accounting server failed.")
        response_get = Tacacs_user.show_tacacs_accounts()
        time.sleep(10)
        tacacs_user = Tacacs_user.test_tacacs_accounting()
        logger.info("The user created is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR : TACACS  accounting test got failed")
        tacacs_user = Tacacs_user.del_tacacs_account(tacacsaccount_name="192.168.168.85")
        logger.info("The user Deleted is {}".format(tacacs_user))
        Assertion.assert_equal(tacacs_user, True, "ERROR:TACACS account is deleted")

class Test_API_Tacacs_base_28(Test):
    uuid = "SOSAIOT-TC-47861"
    description = show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1516323')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_28_tacacs_base(self):
        tacacs_acc_base={
            'timeout': 60,
            'retries': 5,
            'single_connect': False,
            'packet_encrypted': False,
            'watchdog_messages': 10,
            'web_login': True,
            'remote_client': True,
            'guest': False,
            'sso_authenticated': True,
            'sso_users_identified_via_radius_accounting': False,
            'domain_users': True
        }
        res = Tacacs_user.user_tacacs_acc_base(**tacacs_acc_base)
        logger.info(res)
        Assertion.assert_equal(res, True, "ERROR : TACACS+ accounting server base failed.")
