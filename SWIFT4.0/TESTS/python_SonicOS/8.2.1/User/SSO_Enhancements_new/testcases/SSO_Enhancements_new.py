from asyncio.log import logger
from definition.settings import *
import re


class Test_SSO_Enhancements_new_1(Test):
    uuid = "SOSAIOT-TC-75818"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sso_agent_IP(self):
        add_sso_agent_ip = {
                 'action': 'add',
                 'host': sso_ip,
                 'port': sso_default_port,
                 'timeout': 10,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'123456'
        }

        rc = user_sso_obj.sso_agent(**add_sso_agent_ip)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_sso_agent_IP failed")

    def test_02_add_sso_agent_hostname(self):
        add_sso_agent_hostname = {
                 'action': 'add',
                 'host': sso_hostname,
                 'port': sso_default_port,
                 'timeout': 10,
                 'retries': 6,
                 'max_requests': 32,
                 'enable': True,
                 'shared_key':'123456'
        }
        
        rc = user_sso_obj.sso_agent(**add_sso_agent_hostname)
        Assertion.assert_equal(rc, True, "ERR: test_02_add_sso_agent_hostname failed")


class Test_SSO_Enhancements_new_14(Test):
    uuid = "SOSAIOT-TC-75821"
    description = show_testcase_info(TESTPLAN, '14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_sso_agent(self):
        edit_sso_agent = {
                "user": {
                "sso": {
                    "agent": [
                        {
                            "host": sso_ip,
                            "port": sso_new_port,
                            "timeout": 5,
                            "retries": 3,
                            "max_requests": 32,
                            "enable": True,
                            "shared_key": "123456"
                        }
                    ]
                }
            }    
        }
        rc = user_sso_obj.edit_sso_agent(name=sso_ip, **edit_sso_agent, port=sso_default_port)
        Assertion.assert_equal(rc, True, "ERR: test_02_edit_sso_agent failed")


class Test_SSO_Enhancements_new_15(Test):
    uuid = "SOSAIOT-TC-75822"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_sso_agent(self):
        edit_sso_agent = {
                "user": {
                "sso": {
                    "agent": [
                        {
                            "host": sso_ip,
                            "timeout": 5,
                            "retries": 3,
                            "max_requests": new_max_requests,
                            "enable": True,
                            "shared_key": "123456"
                        }
                    ]
                }
            }    
        }
        rc = user_sso_obj.edit_sso_agent(name=sso_ip, **edit_sso_agent, port=sso_new_port)
        Assertion.assert_equal(rc, True, "ERR: test_02_edit_sso_agent failed")


class Test_SSO_Enhancements_new_13(Test):
    uuid = "SOSAIOT-TC-75820"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_sso_agent(self):
        enable_sso = {
            'sso_agent': True,
        }
        rc = user_settings_obj.user_method_authentication(**enable_sso)
        Assertion.assert_equal(rc, True, "ERR: test_02_enable_sso_agent failed")

    @repeat_method(14)
    def test_03_Verify_SSO_Agent_Address_Object(self):
        rc = ao_obj.get_all_addressobject_ipv4()
        logger.info(rc)
        cmd = 'SSO Agent ' + sso_ip
        Assertion.assert_regular(str(rc), cmd,"test_03_Verify_SSO_Agent_Address_Object failed")

    def test_04_Verify_SSO_Agent_Address_Group(self):
        flag = False
        rc = ag_obj.get_addressgroup(version = 'v4')
        logger.info(rc)
        match = re.search(r'Firewall SSO Agents.*?address_object.*?SSO Agent', str(rc), re.I|re.S) 
        if match:
            flag = True
        Assertion.assert_equal(flag,True, "ERR: test_04_Verify_SSO_Agent_Address_Group failed")

    def test_05_Verify_SSO_Agent_Service_Object(self):
        flag = False
        rc = so_obj.get_serviceobject()
        logger.info(rc)
        match = re.search(r'SSO Agent 1.*?udp.*?2258.*?2258', str(rc), re.I|re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag,True, "test_05_Verify_SSO_Agent_Service_Object failed")

    def test_06_Verify_SSO_Agent_Service_Group(self):
        flag = False
        rc = sg_obj.get_servicegroup()
        logger.info(rc)
        match = re.search(r'SonicWALL SSO Agents.*?service_object.*?SSO Agent 1', str(rc), re.I|re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag,True, "test_06_Verify_SSO_Agent_Service_Group failed")


class Test_SSO_Enhancements_new_12(Test):
    uuid = "SOSAIOT-TC-75819"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']
    

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_sso_agent(self):
        enable_sso = {
            'sso_agent': False,
        }
        rc = user_settings_obj.user_method_authentication(**enable_sso)
        Assertion.assert_equal(rc, True, "ERR: test_02_disable_sso_agent failed")

    def test_03_Verify_SSO_Agent_Address_Object(self):
        rc = ao_obj.get_all_addressobject_ipv4()
        logger.info(rc)
        cmd = 'SSO Agent ' + sso_ip
        Assertion.assert_not_regular(str(rc), cmd,"test_03_Verify_SSO_Agent_Address_Object failed")

    def test_04_Verify_SSO_Agent_Address_Group(self):
        flag = False
        rc = ag_obj.get_addressgroup(version = 'v4')
        logger.info(rc)
        match = re.search(r'Firewall SSO Agents.*?address_object.*?SSO Agent', str(rc), re.I|re.S) 
        if match:
            flag = True
        Assertion.assert_equal(flag,False, "ERR: test_04_Verify_SSO_Agent_Address_Group failed")

    def test_05_Verify_SSO_Agent_Service_Object(self):
        flag = False
        rc = so_obj.get_serviceobject()
        logger.info(rc)
        match = re.search(r'SSO Agent 1.*?udp.*?2258.*?2258', str(rc), re.I|re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag,False, "test_05_Verify_SSO_Agent_Service_Object failed")

    def test_06_Verify_SSO_Agent_Service_Group(self):
        flag = False
        rc = sg_obj.get_servicegroup()
        logger.info(rc)
        match = re.search(r'SonicWALL SSO Agents.*?service_object.*?SSO Agent 1', str(rc), re.I|re.S)
        if match:
            flag = True
        Assertion.assert_equal(flag,False, "test_06_Verify_SSO_Agent_Service_Group failed")


class Test_SSO_Enhancements_new_8(Test):
    uuid = "SOSAIOT-TC-75823"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_delete_sso_agent(self):
        rc = user_sso_obj.del_sso_agent(name=sso_ip,port=sso_new_port)
        Assertion.assert_equal(rc, True, "ERR: test_02_delete_sso_agent failed")


class Test_SSO_Enhancements_new_22(Test):
    uuid = "SOSAIOT-TC-94543"
    description = show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_start_STAF_process_on_PC1(self):
        logger.info('killall STAFProc')
        out = os.system('killall STAFProc')
        for i in range(3):
            cmd = 'nohup sh /usr/local/staf/startSTAFProc.sh > /tmp/staf.log 2>&1 &'
            logger.info(cmd)
            os.system(cmd)
            time.sleep(10)
            out = os.popen('pgrep -lf STAFProc').read()
            if 'STAFProc' in out:
                break
        Assertion.assert_regular(str(out), 'STAFProc', 'ERR: STAFProc failed!')
    
    @repeat_method(4)
    def test_02_test_STAF_connection_to_SSO_Client_PC_and_server(self):
        flag = False
        out1 = os.popen('staf {} ping ping'.format(SSO_CLIENT1_lanip)).read()
        time.sleep(20)
        logger.info(out1)
        out2 = os.popen('staf {} ping ping'.format(SSO_CLIENT1_lanip)).read()
        time.sleep(20)
        logger.info(out2)
        out3 = os.popen('staf {} ping ping'.format(SSO_CLIENT1_wanip)).read()
        time.sleep(20)
        logger.info(out3)
        out4 = os.popen('staf {} ping ping'.format(service_agent1)).read()
        time.sleep(20)
        logger.info(out4)
        out5 = os.popen('staf {} ping ping'.format(service_agent2)).read()
        time.sleep(20)
        logger.info(out5)
        if 'PONG' in out1 and 'PONG' in out2 and 'PONG' in out3 and 'PONG' in out4 and 'PONG' in out5:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_02_test_STAF_connection_to_SSO_Client_PC_and_server failed!")

    @repeat_method(8)
    def test_03_set_route_on_sso_client1(self):
        flag = False
        logger.info('Config interface Local Area Connection 5')
        rc3 =os.popen("staf {} process start shell command 'netsh interface ip set address \"Local Area Connection 5\" static {} {}'".format(SSO_CLIENT1_lanip,SSO_CLIENT1_wanip,Mask)).read()
        logger.info(rc3)
        logger.info('Config interface Local Area Connection 4')
        rc1 = os.popen("staf {} process start shell command 'route delete 0.0.0.0 mask 0.0.0.0'".format(SSO_CLIENT1_wanip)).read()
        logger.info(rc1)
        rc2 =os.popen("staf {} process start shell command 'netsh interface ip set address \"Local Area Connection 4\" static {} {} {}'".format(SSO_CLIENT1_wanip,SSO_CLIENT1_lanip,Mask,FIREWALL)).read()
        logger.info(rc2)
        os.system("staf  process start shell command 'type nul>ip_config.txt'".format(SSO_CLIENT1_lanip))
        os.system("staf {} process start shell command 'ipconfig >C:\\STAF\\ip_config.txt'".format(SSO_CLIENT1_lanip))
        out = os.popen("staf {} fs GET FILE  'C:\\STAF\\ip_config.txt'".format(SSO_CLIENT1_lanip)).read()
        logger.info(out)
        match = re.search(r'IPv4 Address.*? '+ SSO_CLIENT1_lanip +'.*? Default Gateway.*?'+ FIREWALL+ '', out, re.I|re.S) 
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_03_set_route_on_sso_client1 failed!")

    @repeat_method(8)
    def test_04_Config_Windows_Settings(self):
        flag = False
        rc3 =os.popen("staf {} process start shell command \'SLMGR -REARM\'".format(SSO_CLIENT1_lanip)).read()
        logger.info(rc3)
        rc4 =os.popen("staf {} process start shell command \"shutdown /r /t 1\"".format(SSO_CLIENT1_lanip)).read()
        logger.info(rc3)
        if 'Response' in rc4 and 'Response' in rc3:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_04_Config_Windows_Settings failed!")

    def test_05_add_two_agent(self):
        add_sso_agent_servie_1 = {
                 'action': 'add',
                 'host': service_agent1,
                 'port': 2258,
                 'timeout': 5,
                 'retries':2,
                 'enable': True,
                 'shared_key':'225abc'
        }
        add_sso_agent_servie_2 = {
                 'action': 'add',
                 'host': service_agent2,
                 'port': 2258,
                 'timeout': 5,
                 'retries':2,
                 'enable': True,
                 'shared_key':'225abc'
        }

        rc = user_sso_obj.sso_agent(**add_sso_agent_servie_1)
        rc &= user_sso_obj.sso_agent(**add_sso_agent_servie_2)
        Assertion.assert_equal(rc, True, "ERR: test_05_add_two_agent failed")

    def test_06_add_ldap_server(self):
        rc = ldap_obj.add_ldap_server_new(**ldap_server)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: test_06_add_ldap_server failed")

    def test_07_config_ldap(self):
        ldap_setting = {
            'require_valid_certificate': False,
        }
        rc = ldap_obj.ldap_setting_new(**ldap_setting)
        Assertion.assert_equal(rc, True, "ERR: test_07_config_ldap failed")

    def test_08_import_ldap_user(self):
        add = {
            "user": {
                "local": {
                    "user": [{
                        "name": "Administrator",
                        "domain": "os-autosnwl.com"
			        }]
		        }
	        }
        }
        rc = user_local_obj.import_local_usr_from_ldap(**add)
        Assertion.assert_equal(rc, True, "ERR: test_08_import_ldap_user failed")

    def test_09_add_localgroup(self):
        add_local_group = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
        }
        rc = user_local_obj.local_group(**add_local_group)
        add_member_of_group = {
                     'action': 'add',
                     'groupname': 'group1',
                     'member_of': ['OS-AUTOSNWL\Administrator']
        }
        rc = user_local_obj.group_member_of(**add_member_of_group)
        Assertion.assert_equal(rc, True, "ERR: test_09_add_localgroup failed")

    def test_10_Configure_AccessRule(self):
        logger.info('Set the default LAN>WAN access rule "Users Allowed" to "group1".')
        edit = {
            'from': 'LAN',
            'to': 'WAN',
            'action': 'allow',
            'source': {
                'address': {
                    'any': True
                },
                'port': {
                    'any': True
                }
            },
            'service': {
                'any': True
            },
            'destination': {
                'address': {
                    'any': True
                }
            },
            'schedule': {
                'always_on': True
            },
            "geo_ip_filter": {
                    "enable": False,
                    "global": True
                },
            'users': {
                'included': {
                    'group': 'group1'
                },
                'excluded': {
                    'none': True
                }
            }
        }
        rc = access_rules_obj.put_accessrule(**edit)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: test_10_Configure_AccessRule failed")

    def test_11_set_sso_configuration(self):
        ##############Set the mechanism for setting user group memberships to "local configuration"###########
        ##############Set the SSO polling rate and hold time after failure both to 1 minute. #################
        edit = {
            'user': {
                'sso': {
                    'user_group_mechanism': {
                        'local_only': True
                    },
                    'hold_time': {
                        'after_failure': 1,
                        'after_no_user': 1
                    },
                    'poll': {
                        'rate': {
                            'minutes': 1
                        },
                        'same_agent': False
                    }
                }
            }
        }
        rc = user_sso_obj.config_sso_base_settings(**edit)
        Assertion.assert_equal(rc, True, "ERR: test_11_set_sso_configuration failed")

    def test_12_enable_sso_agent(self):
        enable_sso = {
            'sso_agent': True,
        }
        rc = user_settings_obj.user_method_authentication(**enable_sso)
        Assertion.assert_equal(rc, True, "ERR: test_12_enable_sso_agent failed")

    def test_13_clear_logs(self):
        logger.info(" {} ".center(20, '-').format('Clear log'))
        rc = False
        ret = log_obj.clear_log()
        if ret == None:
            rc= True
            logger.info('Clear log success!')
        Assertion.assert_equal(rc, True, "ERR: test_13_clear_logs failed")

    def test_14_config_log_level(self):
        rc = log_config.logging_level(level='debug')
        Assertion.assert_equal(rc, True, "ERR: test_14_config_log_level failed")

    @repeat_method(8)
    def test_15_Issue_Ping_From_LAN(self):
        logger.info('Logout user client1')
        user_status.logout_user_ip(SSO_CLIENT1_lanip)
        flag = False
        for i in range(2):
            os.system("staf  process start shell command 'type nul>ping_result111.txt'".format(SSO_CLIENT1_lanip))
            os.system("staf {} process start shell command 'ping {} >C:\\STAF\\ping_result111.txt'".format(SSO_CLIENT1_lanip,wan_pc_ip))
            rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\ping_result111.txt'".format(SSO_CLIENT1_lanip)).read()
            logger.info(rc)
            cmd = 'Reply from ' + wan_pc_ip
            if cmd in rc:
                break
        flag = True
        Assertion.assert_equal(flag, True, "ERR: test_15_Issue_Ping_From_LAN failed")

    @repeat_method(5)
    def test_16_Change_LAN_IP(self):
        flag = False
        logger.info('Config interface Local Area Connection 4')
        rc2 =os.popen("staf {} process start shell command 'netsh interface ip set address \"Local Area Connection 4\" static {} {} {}'".format(SSO_CLIENT1_wanip,LAN2,Mask,FIREWALL)).read()
        logger.info(rc2)
        os.system("staf  process start shell command 'type nul>ip_config222.txt'".format(SSO_CLIENT1_wanip))
        os.system("staf {} process start shell command 'ipconfig >C:\\STAF\\ip_config222.txt'".format(SSO_CLIENT1_wanip))
        out = os.popen("staf {} fs GET FILE  'C:\\STAF\\ip_config222.txt'".format(SSO_CLIENT1_wanip)).read()
        logger.info(out)
        match = re.search(r'IPv4 Address.*? '+ LAN2 +'', out, re.I|re.S) 
        if match:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: test_16_Change_LAN_IP failed!")

    @repeat_method(5)
    def test_17_Issue_Ping_From_LAN_after_Change_IP(self):
        logger.info('Logout user client1 after changing ip')
        user_status.logout_user_ip(LAN2)
        flag = False
        for i in range(10):
            os.system("staf  process start shell command 'type nul>ping_result222.txt'".format(SSO_CLIENT1_wanip))
            os.system("staf {} process start shell command 'ping {} >C:\\STAF\\ping_result222.txt'".format(SSO_CLIENT1_wanip,wan_pc_ip))
            rc = os.popen("staf {} fs GET FILE  'C:\\STAF\\ping_result222.txt'".format(SSO_CLIENT1_wanip)).read()
            logger.info(rc)
            cmd = 'Reply from ' + wan_pc_ip
            if cmd in rc:
                break
        flag = True
        Assertion.assert_equal(flag, True, "ERR: test_17_Issue_Ping_From_LAN_after_Change_IP failed")

    def test_18_check_logs(self):
        flag = False
        rc = log_obj.show_log()
        logger.info(rc)
        match1 = re.search(r'Users.*?'+ SSO_CLIENT1_lanip + '.*?SSO agent\s'+ service_agent1 +'.*?User login', str(rc), re.I|re.S) 
        match2 = re.search(r'Users.*?'+ LAN2+ '.*?SSO agent\s'+ service_agent2+'.*?User login', str(rc), re.I|re.S)
        match3 = re.search(r'Users.*?'+ LAN2 + '.*?SSO agent\s'+ service_agent1 +'.*?User login', str(rc), re.I|re.S) 
        match4 = re.search(r'Users.*?'+ SSO_CLIENT1_lanip+ '.*?SSO agent\s'+ service_agent2+'.*?User login', str(rc), re.I|re.S)
        if (match1 and match2) or (match3 and match4):
            flag = True        
        Assertion.assert_equal(flag, True, "ERR: test_18_check_logs failed")
