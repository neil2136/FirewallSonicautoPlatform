import sys
import os
import json

from definition.settings import *
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SSO_for_Terminal_Services')

resp = status_api.show_status()
model = resp['model']
if model in [ 'TZ 270', 'TZ 270W', 'TZ 80', 'TZ 370','TZ 370W', 'TZ 470', 'TZ 470W', 'TZ 570', 'TZ 570W', 'TZ 570P', 'TZ 670', 'TZ 280', 'TZ 280W', 'TZ 280P', 'TZ 380', 'TZ 380W', 'TZ 480', 'TZ 580', 'TZ 680']:
    max_vlan = 4
elif model in ['NSa 2700', 'NSa 2800']:
    max_vlan = 16
elif model in ['NSa 3700', 'NSa 3800']:
    max_vlan = 64
elif model in ['NSa 4800', 'NSa 4700']:
    max_vlan = 128
elif model in ['NSa 5700', 'NSa 5800', 'NSa 6700', 'NSa 6800','NSSp 10700', 'NSSp 11700', 'NSSp 13700']:
    max_vlan = 256
elif model in ['NSv 270', 'NSv 470']:
    max_vlan = 7
elif model == 'NSv 870':
    max_vlan = 512
else:
    logger.warning(f"Unknown model: {model}.")
    

class TC01_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75702"
    description = show_testcase_info(Parameter.TESTPLAN, '1825273', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825273')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        post_tsa_dict = {
            'action': 'add',
            'host': '10.10.10.10',
            'port': 2259,
            'enable': True,
            'shared_key': '12345678'
        }
        response = user_sso.terminal_services_agent(**post_tsa_dict)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 2259, "ERR: get TS agent failed")

    def test_02_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "port": 21
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='2259')
        Assertion.assert_equal(response, True, "ERR: edit TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='21')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 21, "ERR: get TS agent failed")

    def test_03_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "port": 65535
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='21')
        Assertion.assert_equal(response, True, "ERR: edit TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='65535')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 65535, "ERR: get TS agent failed")


    def test_04_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='10.10.10.10',port='65535')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='65535')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC02_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75706"
    description = show_testcase_info(Parameter.TESTPLAN, '1825277', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825277')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'255.255.255.255',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with invalid IP successful")
        Assertion.assert_equal(message, 'Invalid IP address.', "ERR: error message is not displaying")

    def test_02_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'0.0.0.0',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with invalid IP successful")
        Assertion.assert_equal(message, 'SSO Terminal Service Host name / IP address: Host name / IP address', "ERR: error message is not displaying")


class TC03_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75704"
    description = show_testcase_info(Parameter.TESTPLAN, '1825275', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825275')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.10',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 2259, "ERR: get TS agent failed")

    def test_02_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": "7B316"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='2259')
        Assertion.assert_equal(response, True, "ERR: edit TS agent with valid shared Key failed")

    def test_03_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": ""
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='2259')
        Assertion.assert_equal(response, True, "ERR: edit TS agent with valid shared Key failed")

    def test_04_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": "1234567890ABCDEF"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='2259')
        Assertion.assert_equal(response, True, "ERR: edit TS agent with valid shared Key failed")
 
    def test_05_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": "1234567890ABCDE"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,name='10.10.10.10',port='2259')
        Assertion.assert_equal(response, True, "ERR: edit TS agent with valid shared Key failed")

    def test_06_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": "1234567890ABCDEF12"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,msg=True,name='10.10.10.10',port='2259')
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid shared Key successful")
        Assertion.assert_equal(message, 'Value or string length(18) out of bounds (max = 16)', "ERR: error message is not displaying")

    def test_07_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host":'10.10.10.10',
                            "port":2259,
                            "shared_key": "1G2H3I4J5K6L7M8NL"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,msg=True,name='10.10.10.10',port='2259')
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid shared Key successful")
        Assertion.assert_equal(message, 'Value or string length(17) out of bounds (max = 16)', "ERR: error message is not displaying")

    def test_08_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC04_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75705"
    description = show_testcase_info(Parameter.TESTPLAN, '1825276', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825276')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.a.10.',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")


class TC05_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75703"
    description = show_testcase_info(Parameter.TESTPLAN, '1825274', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825274')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.10',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 2259, "ERR: get TS agent failed")

    def test_02_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host": "127.0.0.0/8"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,msg=True,name='10.10.10.10',port='2259')
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")


    def test_03_edit_terminal_services_agent(self):
        ts_agent = {
            "user": {
                "sso": {
                    "terminal_services_agent": [
                        {
                            "host": "224.0.0.0/4"
                        }
                    ]
                }
            }
        }
        response = user_sso.edit_terminal_services_agent_name_port(**ts_agent,msg=True,name='10.10.10.10',port='2259')
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")

    def test_04_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='2259')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC06_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75707"
    description = show_testcase_info(Parameter.TESTPLAN, '1825278', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825278')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'abcdefghijklmnaoow082491701381751767aJBDyuanadvakduao',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduao',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['host'], 'abcdefghijklmnaoow082491701381751767aJBDyuanadvakduao', "ERR: get TS agent failed")

    
    def test_02_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduao',port='2259')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduao',port='2259')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC07_SSO_for_Terminal_Services(Test):

    uuid = "SOSAIOT-TC-75708"
    description = show_testcase_info(Parameter.TESTPLAN, '1825279', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825279')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'abcdefghijklmnaoow082491701381751767aJBDyuanadvakduaodiwhddwdbwiydgwdwedeh278267385762hgvdhfcsadbasdudgquiyuiqw63268425428475vhdsydfaydvadvhadyagdiugdugfdyufdsfd67452472648257654fdytdfhdgfygdqu78254254245ghewdftweyfdytfd2742546245264ghfvghdfsvgehdf275fdeytweqyhwiduwfwfifgft73285462743174312317fyevgsdcvacasy5e62514126471471gvcashgcasgyasgdabsdvyugqugeyq2632784gwyfsdvcuadgaudgahjvdasjaycdaytdcaydvcaydadfafvashwvewqhe3223hvhdgvashdgfa7653fvdshvcsahcvashgdcashdvajdvajydfasjvdajvasjdcashgdsdasdctyq1263141624wdbdgwufygyfvsftdfgyduqdyuvquequhiuqteqrfwvfwfwufwyguwvwufyfwruwrgqwurfqwwuqwyrwiu6478345267rfvdsgdgadghj',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduaodiwhddwdbwiydgwdwedeh278267385762hgvdhfcsadbasdudgquiyuiqw63268425428475vhdsydfaydvadvhadyagdiugdugfdyufdsfd67452472648257654fdytdfhdgfygdqu78254254245ghewdftweyfdytfd2742546245264ghfvghdfsvgehdf275fdeytweqyhwiduwfwfifgft73285462743174312317fyevgsdcvacasy5e62514126471471gvcashgcasgyasgdabsdvyugqugeyq2632784gwyfsdvcuadgaudgahjvdasjaycdaytdcaydvcaydadfafvashwvewqhe3223hvhdgvashdgfa7653fvdshvcsahcvashgdcashdvajdvajydfasjvdajvasjdcashgdsdasdctyq1263141624wdbdgwufygyfvsftdfgyduqdyuvquequhiuqteqrfwvfwfwufwyguwvwufyfwruwrgqwurfqwwuqwyrwiu6478345267rfvdsgdgadghj',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 2259, "ERR: get TS agent failed")

    def test_02_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduaodiwhddwdbwiydgwdwedeh278267385762hgvdhfcsadbasdudgquiyuiqw63268425428475vhdsydfaydvadvhadyagdiugdugfdyufdsfd67452472648257654fdytdfhdgfygdqu78254254245ghewdftweyfdytfd2742546245264ghfvghdfsvgehdf275fdeytweqyhwiduwfwfifgft73285462743174312317fyevgsdcvacasy5e62514126471471gvcashgcasgyasgdabsdvyugqugeyq2632784gwyfsdvcuadgaudgahjvdasjaycdaytdcaydvcaydadfafvashwvewqhe3223hvhdgvashdgfa7653fvdshvcsahcvashgdcashdvajdvajydfasjvdajvasjdcashgdsdasdctyq1263141624wdbdgwufygyfvsftdfgyduqdyuvquequhiuqteqrfwvfwfwufwyguwvwufyfwruwrgqwurfqwwuqwyrwiu6478345267rfvdsgdgadghj',port='2259')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='abcdefghijklmnaoow082491701381751767aJBDyuanadvakduaodiwhddwdbwiydgwdwedeh278267385762hgvdhfcsadbasdudgquiyuiqw63268425428475vhdsydfaydvadvhadyagdiugdugfdyufdsfd67452472648257654fdytdfhdgfygdqu78254254245ghewdftweyfdytfd2742546245264ghfvghdfsvgehdf275fdeytweqyhwiduwfwfifgft73285462743174312317fyevgsdcvacasy5e62514126471471gvcashgcasgyasgdabsdvyugqugeyq2632784gwyfsdvcuadgaudgahjvdasjaycdaytdcaydvcaydadfafvashwvewqhe3223hvhdgvashdgfa7653fvdshvcsahcvashgdcashdvajdvajydfasjvdajvasjdcashgdsdasdctyq1263141624wdbdgwufygyfvsftdfgyduqdyuvquequhiuqteqrfwvfwfwufwyguwvwufyfwruwrgqwurfqwwuqwyrwiu6478345267rfvdsgdgadghj',port='2259')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC08_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75709"
    description = show_testcase_info(Parameter.TESTPLAN, '1825280', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825280')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'00:1A:2B:3C:4D:5E',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")


    def test_02_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'SELECT FROM employees',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")

    def test_03_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'host_name_*com/',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")


class TC09_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75710"
    description = show_testcase_info(Parameter.TESTPLAN, '1825281', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825281')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'host_name_*com/',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'host': invalid format\n", "ERR: error message is not displaying")


class TC10_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75711"
    description = show_testcase_info(Parameter.TESTPLAN, '1825282', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825282')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.10',
            'port':0,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Incomplete command.", "ERR: error message is not displaying")

    def test_02_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.10',
            'port':1,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='1')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 1, "ERR: get TS agent failed")

    def test_03_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.11',
            'port':65536,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with out bound port successful")
        Assertion.assert_equal(message, "Value or string length(65536) out of bounds (min = 1, max = 65535)", "ERR: error message is not displaying")

    def test_04_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.11',
            'port':-1,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: edit TS agent with invalid IP successful")
        Assertion.assert_equal(message, "Schema validation error: property 'port': invalid format\n", "ERR: error message is not displaying")

    def test_05_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='10.10.10.10',port='1')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.10',port='1')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC11_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75712"
    description = show_testcase_info(Parameter.TESTPLAN, '1825283', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825283')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with  without host successful")
        Assertion.assert_equal(message, "Incomplete command.", "ERR: error message is not displaying")


class TC12_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75701"
    description = show_testcase_info(Parameter.TESTPLAN, '1825272', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1825272')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_max_terminal_services_agent(self):

        base_networks = ["10.10.10", "11.11.11", "12.12.12"]
        count = 0
        for net in base_networks:
            for i in range(1, 256): 
                if count >= max_vlan:
                    break  

                addrs = f"{net}.{i}"
                max_sso = {
                    "action": "add",
                    "host": addrs,
                    "port": 2259,
                    "enable": True,
                    "shared_key": "1234"
                }

                sso_create = user_sso.terminal_services_agent(**max_sso)
                logger.info(f"Added TSA Agent {count+1}/{max_vlan} at {addrs}: {sso_create}")

                count += 1

            if count >= max_vlan:
                break


    def test_02_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'12.12.12.100',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent,msg=True)
        success = response[1]['status']['success']
        message = response[1]['status']['info'][0]['message']
        Assertion.assert_equal(success, False, "ERR: add TS agent with invalid IP successful")
        Assertion.assert_equal(message, 'SSO Terminal Service Host name / IP address: Host name / IP address:  Data out of bounds (min = 0, max = 0).', "ERR: error message is not displaying")

    def test_03_delete_terminal_services_agent(self):
        base_networks = ["10.10.10", "11.11.11", "12.12.12"]
        count = 0
        for net in base_networks:
            for i in range(1, 256): 
                if count >= max_vlan:
                    break  

                addrs = f"{net}.{i}"
                res = user_sso.del_terminal_services_agent_by_host(host=addrs, port='2259')
                Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
                count += 1

            if count >= max_vlan:
                break


class TC13_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75718"
    description = show_testcase_info(Parameter.TESTPLAN, '1525686', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525686')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ts_agent(self):
        localhost.send_command('pkill firefox')
        out = uiobj.add_ts_agent('10.10.10.15', '1234')
        Assertion.assert_equal(out, True, "ERR: testcase failed")

    def test_02_delete_ts_agent(self):
        localhost.send_command('pkill firefox')
        out = uiobj.delete_ts_agent()
        Assertion.assert_equal(out, False, "ERR: testcase failed")


class TC14_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75719"
    jira = 'GEN8-9960'
    description = show_testcase_info(Parameter.TESTPLAN, '1525687', description=True)['title']
    
    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525687')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_terminal_services_agent(self):
        ts_agent = {
            'action':'add',
            'host':'10.10.10.16',
            'port':2259,
            'shared_key':'1234',
            'enable': True
        }
        response = user_sso.terminal_services_agent(**ts_agent)
        Assertion.assert_equal(response, True, "ERR: add TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.16',port='2259')
        Assertion.assert_equal(res['user']['sso']['terminal_services_agent'][0]['port'], 2259, "ERR: get TS agent failed")

    def test_02_edit_ts_agent_shared_key(self):
        localhost.send_command('pkill firefox')
        out = uiobj.edit_ts_agent_shared_key_with_different_length()
        Assertion.assert_equal(out, False, "ERR: testcase failed")
    
    def test_03_delete_terminal_services_agent(self):
        res = user_sso.del_terminal_services_agent_by_host(host='10.10.10.16',port='2259')
        Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
        res = user_sso.get_terminal_services_agent_by_host(host='10.10.10.16',port='2259')
        Assertion.assert_regular(json.dumps(res), 'False', "ERR: delete TS agent failed")


class TC15_SSO_for_Terminal_Services(Test):
    uuid = "SOSAIOT-TC-75713"
    description = show_testcase_info(Parameter.TESTPLAN, '1525674', description=True)['title']

    def test_01_add_max_terminal_services_agent(self):
        base_networks = ["10.10.10", "11.11.11", "12.12.12"]
        count = 0
        for net in base_networks:
            for i in range(1, 256): 
                if count >= max_vlan:
                    break  

                addrs = f"{net}.{i}"
                localhost.send_command('pkill firefox')
                out = uiobj.add_ts_agent(addrs, '1234')
                Assertion.assert_equal(out, True, "ERR: testcase failed")

                count += 1

            if count >= max_vlan:
                break

    def test_02_add_ts_agent(self):
        localhost.send_command('pkill firefox')
        out = uiobj.add_ts_agent_max('12.12.12.255', '1234')
        Assertion.assert_equal(out, True, "ERR: testcase failed")

    def test_03_delete_terminal_services_agent(self):
        base_networks = ["10.10.10", "11.11.11", "12.12.12"]
        count = 0
        for net in base_networks:
            for i in range(1, 256): 
                if count >= max_vlan:
                    break  

                addrs = f"{net}.{i}"
                res = user_sso.del_terminal_services_agent_by_host(host=addrs, port='2259')
                Assertion.assert_equal(res, True, "ERR: delete TS agent failed")
                count += 1

            if count >= max_vlan:
                break