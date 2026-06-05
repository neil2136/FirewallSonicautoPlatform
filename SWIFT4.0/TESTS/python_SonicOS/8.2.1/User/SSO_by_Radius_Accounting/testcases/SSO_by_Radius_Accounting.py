
from asyncio.log import logger
from json import load
from definition.settings import *
import re


class Test_SSO_by_Radius_Accounting_05(Test):
    uuid = "SOSAIOT-TC-75771"
    description = show_testcase_info(TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sso_radius_by_accounting(self):
        add_sso_radius_accounting_client1 = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": account_ip,
                        "shared_secret": "password",
                        "log_user_out_timeout": 0
                    }]
                }
            }
        }
        add_sso_radius_accounting_client2 = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": Hostname,
                        "shared_secret": "password",
                        "log_user_out_timeout": 0
                    }]
                }
            }
        }

        rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client1)
        rc &= user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client2)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_sso_radius_by_accounting failed")

class Test_SSO_by_Radius_Accounting_08(Test):
    uuid = "SOSAIOT-TC-75773"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_sso_radius_by_accounting(self):
        edit = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": new_account_ip,
                        "shared_secret": "password",
                    }]
                }
            }}
        rc = user_sso_obj.edit_sso_radius_accounting_client(name=account_ip, **edit)
        Assertion.assert_equal(rc, True, "ERR: test_02_edit_sso_radius_by_accounting failed")


class Test_SSO_by_Radius_Accounting_09(Test):
    uuid = "SOSAIOT-TC-75774"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_del_sso_radius_by_accounting(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(new_account_ip)
        rc &= user_sso_obj.del_sso_radius_accounting_client(Hostname)
        Assertion.assert_equal(rc, True, "ERR: test_02_del_sso_radius_by_accounting failed")


class Test_SSO_by_Radius_Accounting_06(Test):
    uuid = "SOSAIOT-TC-75772"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Get_The_Max_Client_Number_and_add_them(self):
        logger.info('Get_The_Max_Client_Number from tsr...... ')
        logger.info('Download tsr..... ')
        tsr_obj.download_tsr(filepath = '/tmp/techSupport')
        tsr_content = os.popen('cat /tmp/techSupport').read()
        if 'Max SSO RADIUS Accounting clients' in tsr_content:
            lab1_match = re.search(r'Max SSO RADIUS Accounting clients\W\s+\d+', tsr_content, re.I|re.S|re.M)
            print(lab1_match)
            if lab1_match:
                logger.info(lab1_match.group())
                number = re.findall(r'\d+', lab1_match.group())[0]
                logger.info(number)
                for i in range(int(number)):
                    hostIP = '2.2.2.' + str(i)
                    print(hostIP)
                    add_sso_radius_accounting_client2 = {
                        "user": {
                            "sso": {
                                "radius_accounting_client": [{
                                    "host": hostIP,
                                    "shared_secret": "password",
                                    "log_user_out_timeout": 0
                                }]
                            }
                        }
                    }
                    rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client2)
                    Assertion.assert_equal(rc, True, "ERR: test_02_Get_The_Max_Client_Number_and_add_them failed")

    def test_03_add_one_more_accounting(self):
        add_sso_radius_accounting_client1 = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": account_ip,
                        "shared_secret": "password",
                        "log_user_out_timeout": 0
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client1,msg=True)
        Assertion.assert_regular(str(rc), r'Sorry but the limit of \d+ clients has been reached', "ERR: test_03_add_one_more_accounting failed")
    
    def test_04_del_all_sso_radius_accounting_clients(self):
        rc = user_sso_obj.del_sso_radius_accounting_client('2.2.2.0')
        rc &= user_sso_obj.del_sso_radius_accounting_client('2.2.2.1')
        rc &= user_sso_obj.del_sso_radius_accounting_client('2.2.2.2')
        rc &= user_sso_obj.del_sso_radius_accounting_client('2.2.2.3')
        Assertion.assert_equal(rc, True, "ERR: test_04_del_all_sso_radius_accounting_clients failed")

class Test_SSO_by_Radius_Accounting_23(Test):
    uuid = "SOSAIOT-TC-75770"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']
    

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Radius_Accounting_Client_local(self):
        add_sso_radius_accounting_client1 = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "server": [{
                            "serverId": 1,
                            "name": REMOTEX1,
                            "port": 1813,
                            "shared_secret": "password"
                        }],
                        "host": radius_client,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        }
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add_sso_radius_accounting_client1)
        Assertion.assert_equal(rc, True, "ERR: test_02_Add_Radius_Accounting_Client_local failed")

    def test_03_Add_Radius_Accounting_Client_remote(self):
        add_sso_radius_accounting_client1 = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": DUTX1,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        },
                        "log_user_out_timeout": 0,
                        "proxy_forward": {
                            "timeout": 10,
                            "retries": 3
                        }
                    }]
                }
            }
        }
        rc = user_sso_obj_remote.add_sso_radius_accounting_client(**add_sso_radius_accounting_client1)
        Assertion.assert_equal(rc, True, "ERR: test_03_Add_Radius_Accounting_Client_remote failed")

    def test_04_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        out = os.popen('pgrep -lf STAFProc').read()
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')

    @repeat_method(15)
    def test_05_sending_a_Start_accounting_request(self):
        logger.info('Logout radius_client_user1 and radius_client_user2')
        user_status.logout_user_session(**logout_user1)
        user_status.logout_user_session(**logout_user2)
        logger.info('From the Client, sending a Start accounting request...')
        flag = False
        os.system("staf {} process start shell command 'type nul>result111.txt'".format(PC2))
        for i in range(5):            
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -start >C:\\STAF\\result111.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result111.txt'".format(PC2)).read()
        logger.info(rc)
        cmd1 = 'Sending start record'
        cmd2 = 'Failed to connect to appliance radius service'
        if cmd1 in rc and 'thread' in rc and 'finished' in rc and cmd2 not in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_05_sending_a_Start_accounting_request failed")

    def test_06_verify_user_status_local(self):
        flag = False
        for i in range(2):
            rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if ('RADIUS Accounting' in str(rc) or "SSO" in str(rc)) and radius_client_user1 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_06_verify_user_status_local failed")

    def test_07_verify_user_status_remote(self):
        flag = False
        for i in range(2):
            rc = user_status_cli_remote.show_users_status_inactive()
        logger.info('rc')
        logger.info(rc)
        logger.info('rc')
        if ('RADIUS Accounting' in str(rc) or "SSO" in str(rc)) and radius_client_user1 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_07_verify_user_status_remote failed")

    def test_08_del_accounting_client_local(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(radius_client)
        Assertion.assert_equal(rc,True, "test_08_del_accounting_client_local failed")

    def test_09_del_accounting_client_remote(self):
        rc = user_sso_obj_remote.del_sso_radius_accounting_client(DUTX1)
        Assertion.assert_equal(rc,True, "test_09_del_accounting_client_remote failed")


class Test_SSO_by_Radius_Accounting_10(Test):
    uuid = "SOSAIOT-TC-75766"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Radius_Accounting_Client(self):
        add = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": radius_client,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        }                       
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add)
        Assertion.assert_equal(rc, True, "ERR: test_02_delete_sso_agent failed")
    
    def test_03_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        out = os.popen('pgrep -lf STAFProc').read()
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')

    @repeat_method(15)
    def test_04_sending_a_Start_accounting_request(self):
        logger.info('Logout radius_client_user1 and radius_client_user2')
        user_status.logout_user_session(**logout_user1)
        user_status.logout_user_session(**logout_user2)
        logger.info('From the Client, sending a Start accounting request...')
        flag = False
        os.system("staf {} process start shell command 'type nul>result222.txt'".format(PC2))
        for i in range(5):            
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -start >C:\\STAF\\result222.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result222.txt'".format(PC2)).read()
        logger.info(rc)
        cmd1 = 'Sending start record'
        cmd2 = 'Failed to connect to appliance radius service'
        if cmd1 in rc and 'thread' in rc and 'finished' in rc and cmd2 not in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_03_sending_a_Start_accounting_request failed")

    def test_05_verify_user_status(self):
        flag = False
        rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if ('RADIUS Accounting' in str(rc) or "SSO" in str(rc)) and radius_client_user1 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_04_verify_user_status failed")

    def test_07_del_accounting_client(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(radius_client)
        Assertion.assert_equal(rc,True, "test_07_del_accounting_client failed")


class Test_SSO_by_Radius_Accounting_14(Test):
    uuid = "SOSAIOT-TC-75767"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Radius_Accounting_Client(self):
        add = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": radius_client,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        }
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add)
        Assertion.assert_equal(rc, True, "ERR: test_02_delete_sso_agent failed")

    def test_03_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        out = os.popen('pgrep -lf STAFProc').read()
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')

    @repeat_method(15)
    def test_04_sending_a_Start_accounting_request(self):
        logger.info('Logout radius_client_user1 and radius_client_user2')
        user_status.logout_user_session(**logout_user1)
        user_status.logout_user_session(**logout_user2)
        logger.info('From the Client, sending a Start accounting request...')
        flag = False
        for i in range(5):
            os.system("staf {} process start shell command 'type nul>result333.txt'".format(PC2))
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -start >C:\\STAF\\result333.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result333.txt'".format(PC2)).read()
        logger.info(rc)
        cmd1 = 'Sending start record'
        cmd2 = 'Failed to connect to appliance radius service'
        if cmd1 in rc and 'thread' in rc and 'finished' in rc and cmd2 not in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_03_sending_a_Start_accounting_request failed")

    def test_04_verify_user_status(self):
        flag = False
        rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if ('RADIUS Accounting' in str(rc) or "SSO" in str(rc)) and radius_client_user1 in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_04_verify_user_status failed")

    @repeat_method(20)
    def test_05_sending_a_Stop_accounting_request_and_verify_user_status_after_stop_request(self):
        logger.info('killall STAFProc')
        os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        logger.info('From the Client, sending a stop accounting request...')
        time.sleep(5)
        flag = False
        for i in range(4):
            os.system("staf {} process start shell command 'type nul>result444.txt'".format(PC2))
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -stop >C:\\STAF\\result444.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result444.txt'".format(PC2)).read()
        logger.info(rc)
        rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if 'RADIUS Accounting' not in str(rc) and radius_client_user1 not in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_06_verify_user_status_after_stop_request failed")

    def test_07_del_accounting_client(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(radius_client)
        Assertion.assert_equal(rc,True, "test_06_del_accounting_client failed")


class Test_SSO_by_Radius_Accounting_17(Test):
    uuid = "SOSAIOT-TC-75769"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Radius_Accounting_Client(self):
        add = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": radius_client,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        }
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add)
        Assertion.assert_equal(rc, True, "ERR: test_02_delete_sso_agent failed")

    def test_03_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        out = os.popen('pgrep -lf STAFProc').read()
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')

    @repeat_method(15)
    def test_04_sending_a_Start_accounting_request(self):
        logger.info('Logout radius_client_user1 and radius_client_user2')
        user_status.logout_user_session(**logout_user1)
        user_status.logout_user_session(**logout_user2)
        logger.info('From the Client, sending a Start accounting request...')
        flag = False
        for i in range(4):
            os.system("staf {} process start shell command 'type nul>result555.txt'".format(PC2))
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -start >C:\\STAF\\result555.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result555.txt'".format(PC2)).read()
        logger.info(rc)
        cmd1 = 'Sending start record'
        cmd2 = 'Failed to connect to appliance radius service'
        if cmd1 in rc and 'thread' in rc and 'finished' in rc and cmd2 not in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_03_sending_a_Start_accounting_request failed")

    def test_05_verify_user_status_with_name_Auth(self):
        flag = False
        rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if 'mydomain' in rc and 'SSO' in str(rc) and radius_client_user1 in str(rc):
            flag = True
            Assertion.assert_equal(flag, True, "ERR: test_04_verify_user_status failed")

    def test_06_del_accounting_client(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(radius_client)
        Assertion.assert_equal(rc,True, "test_05_del_accounting_client failed")


class Test_SSO_by_Radius_Accounting_16(Test):
    uuid = "SOSAIOT-TC-75768"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Radius_Accounting_Client(self):
        add = {
            "user": {
                "sso": {
                    "radius_accounting_client": [{
                        "host": radius_client,
                        "shared_secret": "password",
                        "log_user_out_if_no_interim": {
                            "auto": True
                        }
                    }]
                }
            }
        }
        rc = user_sso_obj.add_sso_radius_accounting_client(**add)
        Assertion.assert_equal(rc, True, "ERR: test_02_delete_sso_agent failed")

    def test_03_disable_accounting_client(self):
        logger.info('Disable SSO by RADIUS accounting......')
        edit = {
            "user": {
                "sso": {
                    "method": {
                        "radius_accounting": False,
                    }
                }
            }
        }
        rc =  user_sso_obj.config_sso_base_settings(**edit)
        Assertion.assert_equal(rc, True, "ERR: test_03_disable_accounting_client failed")

    def test_04_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(5)
        out = os.popen('pgrep -lf STAFProc').read()
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')

    def test_05_sending_a_Start_accounting_request(self):
        logger.info('Logout radius_client_user1 and radius_client_user2')
        user_status.logout_user_session(**logout_user1)
        user_status.logout_user_session(**logout_user2)
        logger.info('From the Client, sending a Start accounting request...')
        flag = False
        for i in range(4):
            os.system("staf {} process start shell command 'type nul>result666.txt'".format(PC2))
            os.system("staf {} process start shell command 'c:\\testradius\\testradius.exe -d mydomain -p password -u user -s {} -i 1 -c 1 -t 5 -h {} -start >C:\\STAF\\result666.txt'".format(PC2,radius_client_userip_mior1,FIREWALL))
        rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\result666.txt'".format(PC2)).read()
        logger.info(rc)
        cmd1 = 'Sending start record'
        cmd2 = 'Failed to connect to appliance radius service'
        if cmd1 and cmd2 in rc:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_04_sending_a_Start_accounting_request failed")

    def test_06_verify_user_status(self):
        flag = False
        rc = user_status_cli.show_users_status_inactive()
        logger.info(rc)
        if 'RADIUS Accounting' not in str(rc) and radius_client_user1 not in str(rc):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_05_verify_user_status failed")

    def test_07_del_accounting_client(self):
        rc = user_sso_obj.del_sso_radius_accounting_client(radius_client)
        Assertion.assert_equal(rc,True, "test_06_del_accounting_client failed")