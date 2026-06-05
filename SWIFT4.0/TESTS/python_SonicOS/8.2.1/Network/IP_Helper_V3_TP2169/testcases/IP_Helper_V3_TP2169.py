from definition.init_param import *
from confs.utils import *


class Test_01_IP_Helper_V3_TP2169_tc_1510517(Test):
    uuid = "SOSAIOT-TC-56307"
    description= show_testcase_info(Parameter.TESTPLAN, '1510517', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510517')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_ip_helper_and_reboot_fw(self):
        logger.info('enable ip helper and reboot fw...')
        rc = iphelper.enable_iphelper()
        rc &= settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, 'ERR: enable ip helper and reboot fw failed')

    def test_02_verify_ip_helper(self):
        logger.info('verify ip helper...')
        flag = False
        try:
            output = iphelper.get_iphelper_settings()
            logger.info(output)
            flag = output['ip_helper']['enable']
        except:
            logger.info('can\'t get ip helper setting...')
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper failed')


class Test_02_IP_Helper_V3_TP2169_tc_1510541(Test):
    uuid = "SOSAIOT-TC-56326"
    description= show_testcase_info(Parameter.TESTPLAN, '1510541', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510541')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_disable_ip_helper_and_reboot_fw(self):
        logger.info('disable ip helper and reboot fw...')
        rc = iphelper.disable_iphelper()
        rc &= settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, 'ERR: disable ip helper and reboot fw failed')

    def test_02_verify_ip_helper(self):
        logger.info('verify ip helper...')
        flag = True
        try:
            output = iphelper.get_iphelper_settings()
            logger.info(output)
            flag = output['ip_helper']['enable']
        except:
            logger.info('can\'t get ip helper setting...')
        Assertion.assert_equal(flag, False, 'ERR: verify ip helper failed')


class Test_03_IP_Helper_V3_TP2169_tc_1510557(Test):
    uuid = "SOSAIOT-TC-56342"
    description= show_testcase_info(Parameter.TESTPLAN, '1510557', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510557')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_ip_protocol(self):
        logger.info('add ip protocol...')
        ip_dict = {
            'name': 'user_defined',
            'port1': 111,
            'port2': 222,
            'timeout': 30,
            'enable': True
        }
        rc = iphelper.add_protocol(**ip_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip protocol failed')

    def test_02_verify_ip_protocol(self):
        logger.info('verify ip protocol...')
        flag = False
        output = iphelper.get_protocol(protocol = 'All')
        logger.info(output)
        if re.search(r'\'name\'\W+\s\'user_defined', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip protocol failed')

    def test_03_add_ip_protocol(self):
        logger.info('add ip protocol...')
        ip_dict = {
            'name': 'user_defined_2',
            'port1': 120,
            'port2': 220,
            'timeout': 30,
            'enable': True
        }
        rc = iphelper.add_protocol(**ip_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip protocol failed')


class Test_04_IP_Helper_V3_TP2169_tc_1510558(Test):
    uuid = "SOSAIOT-TC-56343"
    description= show_testcase_info(Parameter.TESTPLAN, '1510558', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510558')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_delete_ip_prototol(self):
        logger.info('delete ip protocol...')
        rc = iphelper.del_protocol(name = 'user_defined')
        rc &= iphelper.del_protocol(name = 'user_defined_2')
        Assertion.assert_equal(rc, True, 'ERR: add ip protocol failed')

    def test_02_verify_ip_protocol(self):
        logger.info('verify ip protocol...')
        flag = False
        output = iphelper.get_protocol(protocol = 'All')
        logger.info(output)
        if not re.search(r'\'name\'\W+\s\'user_defined', str(output), re.S|re.I) and not \
            re.search(r'\'name\'\W+\s\'user_defined_2', str(output), re.S|re.I) and \
            re.search(r'\'name\'\W+\s\'DHCP', str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip protocol failed')


class Test_05_IP_Helper_V3_TP2169_tc_1510560(Test):
    uuid = "SOSAIOT-TC-56345"
    description= show_testcase_info(Parameter.TESTPLAN, '1510560', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510560')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_ip_protocol(self):
        logger.info('add ip protocol...')
        ip_dict = {
            'name': 'user_defined',
            'port1': 111,
            'port2': 222,
            'timeout': 30,
            'enable': True
        }
        rc = iphelper.add_protocol(**ip_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip protocol failed')

    def test_02_edit_ip_protocol(self):
        logger.info('edit ip protocol...')
        ip_dict = {
            'port1': 333,
            'port2': 444,
            'timeout': 40,
            'enable': False
        }
        rc = iphelper.edit_protocol(name='user_defined', **ip_dict)
        Assertion.assert_equal(rc, True, 'ERR: edit ip protocol failed')

    def test_03_reboot_fw_and_verify_protocol(self):
        logger.info('reboot fw and verify protocol...')
        rc = settingObj.boot_fw(mode = 1)
        output = iphelper.get_protocol(protocol = 'All')
        logger.info(output)
        match_string = "\'name\'\W+\s\'user_defined.*port1\'\:\s\{\'value\'\:\s333},"+\
            "\s\'port2\'\:\s\{\'value\'\:\s444},\s\'timeout\'\:\s\'40"
        if re.search(match_string, str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, 'ERR: verify ip protocol failed')


class Test_06_IP_Helper_V3_TP2169_tc_1510525(Test):
    uuid = "SOSAIOT-TC-56313"
    description= show_testcase_info(Parameter.TESTPLAN, '1510525', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510525')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'X1 IP',
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_02_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'DHCP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')

    def test_03_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_07_IP_Helper_V3_TP2169_tc_1510526(Test):
    uuid = "SOSAIOT-TC-56314"
    description= show_testcase_info(Parameter.TESTPLAN, '1510526', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510526')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao_dict1 = {
            'object_type':'network',
            'name':'tc14_src',
            'zone':'LAN',
            'value': '192.168.168.0,255.255.255.0',
        }
        ao_dict2 = {
            'object_type':'network',
            'name':'tc14_dst',
            'zone':'WAN',
            'value': '13.0.0.0,255.255.255.0',
        }
        rc = addressObj.config_addressobject(**ao_dict1)
        rc &= addressObj.config_addressobject(**ao_dict2)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_add_netBIOS_policy(self):
        logger.info('add netBIOS policy...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'source': {
                'name': 'tc14_src'
            },
            'destination': {
                'name': 'tc14_dst'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_03_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'NetBIOS':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')

    def test_04_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'source': {
                'name': 'tc14_src'
            },
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_08_IP_Helper_V3_TP2169_tc_1510528(Test):
    uuid = "SOSAIOT-TC-56316"
    description= show_testcase_info(Parameter.TESTPLAN, '1510528', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510528')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao_dict = {
            'object_type':'host',
            'name':'tc15_dst',
            'zone':'WAN',
            'value': Parameter.X1_IP,
        }

        rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'tc15_dst',
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_03_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'DHCP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')

    def test_04_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_09_IP_Helper_V3_TP2169_tc_1510530(Test):
    uuid = "SOSAIOT-TC-56318"
    description= show_testcase_info(Parameter.TESTPLAN, '1510530', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510530')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao_dict = {
            'object_type':'host',
            'name':'tc16_dst',
            'zone':'WAN',
            'value': Parameter.X1_IP,
        }
        rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_add_DNS_policy(self):
        logger.info('add DNS policy...')
        policy_dict = {
            'protocol': 'DNS',
            'src': 'X0',
            'destination': {
                'name': 'tc16_dst'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_03_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'DNS':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')


#TC18 can not be automated
class Test_10_IP_Helper_V3_TP2169_tc_1510535(Test):
    uuid = "SOSAIOT-TC-56321"
    description= show_testcase_info(Parameter.TESTPLAN, '1510535', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510535')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DNS',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')

    def test_02_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        logger.info(protocol)
        if protocol == 'ICMP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')


class Test_11_IP_Helper_V3_TP2169_tc_1510533(Test):
    uuid = "SOSAIOT-TC-56319"
    description= show_testcase_info(Parameter.TESTPLAN, '1510533', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510533')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao_dict = {
            'object_type':'host',
            'name':'tc17_dst',
            'zone':'WAN',
            'value': Parameter.X1_IP,
        }
        rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_add_user_defined_policy(self):
        logger.info('add user defined protocol policy...')
        policy_dict = {
            'protocol': 'user_defined',
            'src': 'X0',
            'destination': {
                'name': 'tc17_dst'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add user defined protocol policy failed')

    def test_03_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'user_defined':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')


class Test_12_IP_Helper_V3_TP2169_tc_1510542(Test):
    uuid = "SOSAIOT-TC-56327"
    description= show_testcase_info(Parameter.TESTPLAN, '1510542', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510542')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'user_defined',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')

    def test_02_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        logger.info(protocol)
        if protocol == 'ICMP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')


class Test_13_IP_Helper_V3_TP2169_tc_1510547(Test):
    uuid = "SOSAIOT-TC-56332"
    description= show_testcase_info(Parameter.TESTPLAN, '1510547', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510547')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'tc15_dst',
            'enable': False
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_02_add_user_defined_policy(self):
        logger.info('add user defined protocol policy...')
        policy_dict = {
            'protocol': 'user_defined',
            'src': 'X0',
            'destination': {
                'name': 'tc17_dst'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add user defined protocol policy failed')

    def test_03_enable_dhcp_policy(self):
        logger.info('enable dhcp policy...')
        policy_dict = {
            'policy': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable dhcp policy failed')

    def test_04_disable_user_defined_policy(self):
        logger.info('disable user defined policy...')
        policy_dict = {
            'policy': 'user_defined',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: disable user defined policy failed')

    def test_05_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        output['ip_helper']['policy'][0]['protocol']
        for i in range(len(output['ip_helper']['policy'])):
            if output['ip_helper']['policy'][i]['protocol'] == 'DHCP' and \
                output['ip_helper']['policy'][i]['enable'] == True:
                flag = True
            if output['ip_helper']['policy'][i]['protocol'] == 'user_defined' and \
                output['ip_helper']['policy'][i]['enable'] == False:
                flag &= True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')

    def test_06_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict1 = {
            'protocol': 'user_defined',
            'source': {'interface': 'X0'}
        }
        policy_dict2 = {
            'protocol': 'DHCP',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict1)
        rc &= iphelper.delete_iphelper_policy(**policy_dict2)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_14_IP_Helper_V3_TP2169_tc_1510549(Test):
    uuid = "SOSAIOT-TC-56334"
    description= show_testcase_info(Parameter.TESTPLAN, '1510549', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510549')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_ip_helper(self):
        logger.info('enable ip helper...')
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: enable ip helper  failed')

    def test_02_add_address_object(self):
        logger.info('add address object...')
        ao_dict = {
            'object_type':'host',
            'name':'tc24_dst',
            'zone':'WAN',
            'value': Parameter.X1_IP,
        }
        rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_03_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'tc24_dst',
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_04_export_and_import_fw_setting(fw):
        logger.info('export and import fw setting...')
        rc = settingObj.export_setting_exp()
        rc &= settingObj.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(rc, True, 'ERR: export and import fw setting failed')

    def test_05_verify_ip_helper_policy(self):
        logger.info('verify ip helper policy...')
        flag = False
        output = iphelper.get_policy()
        logger.info(output)
        protocol = 'ICMP'
        try:
            protocol = output['ip_helper']['policy'][0]['protocol']
        except:
            logger.info('can\'t get ip help policy...')
        if protocol == 'DHCP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: verify ip helper policy failed')

    def test_06_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_15_IP_Helper_V3_TP2169_tc_1510550(Test):
    uuid = "SOSAIOT-TC-56335"
    description= show_testcase_info(Parameter.TESTPLAN, '1510550', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510550')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        flag = False
        policy_dict = {
            'protocol': 'DHCP',
            "source": {
                "interface": "X2"
            },
            "destination": {
                "name": "X2 IP"
            },
            'enable': True
        }
        output = iphelper.add_iphelper_policy(msg=True, **policy_dict)
        logger.info(output)
        if re.search(r'Address range overlaps with another range', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: add ip helper policy failed')


class Test_16_IP_Helper_V3_TP2169_tc_1510551(Test):
    uuid = "SOSAIOT-TC-56336"
    description= show_testcase_info(Parameter.TESTPLAN, '1510551', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510551')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_dns_protocol(self):
        logger.info('enable dns protocol...')
        dns ={
            'enable': True
        }
        rc = iphelper.edit_protocol(name='DNS', **dns)
        Assertion.assert_equal(rc, True, 'ERR: enable dns protocol failed')

    def test_02_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DNS',
            'src': 'X0',
            'destination': {
                'name': 'WAN Host'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    @repeat_method(3)
    def test_03_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")


class Test_17_IP_Helper_V3_TP2169_tc_1510552(Test):
    uuid = "SOSAIOT-TC-56337"
    description= show_testcase_info(Parameter.TESTPLAN, '1510552', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510552')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_disable_DNS_policy(self):
        logger.info('disable DNS policy...')
        policy_dict = {
            'policy': 'DNS',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: disable DNS failed')

    @repeat_method(3)
    def test_03_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")


class Test_18_IP_Helper_V3_TP2169_tc_1510553(Test):
    uuid = "SOSAIOT-TC-56338"
    description= show_testcase_info(Parameter.TESTPLAN, '1510553', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510553')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_DNS_policy(self):
        logger.info('enable DNS policy...')
        policy_dict = {
            'policy': 'DNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable DNS failed')

    def test_02_disable_ip_helper(self):
        logger.info('disable ip helper...')
        rc = iphelper.disable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: disable ip helper  failed')
    
    @repeat_method(3)
    def test_03_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")

    def test_04_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DNS',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_19_IP_Helper_V3_TP2169_tc_1510562(Test):
    uuid = "SOSAIOT-TC-56346"
    description= show_testcase_info(Parameter.TESTPLAN, '1510562', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510562')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_ip_helper(self):
        logger.info('enable ip helper...')
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: enable ip helper  failed')

    def test_02_enable_dhcp_protocol(self):
        logger.info('enable dhcp protocol...')
        dhcp ={
            'enable': True
        }
        rc = iphelper.edit_protocol(name='DHCP', **dhcp)
        Assertion.assert_equal(rc, True, 'ERR: enable dhcp protocol failed')

    def test_03_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'destination': {
                'name': 'WAN Host'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    @repeat_method(3)
    def test_04_test_traffic(self):
        logger.info('test traffic...')
        flag = False
        local_host.send_command('ifconfig eth1 down')
        pc2_ssh.send_command('service dhcpd restart')
        local_host.send_command('dhclient eth0 &')
        for i in range(20):
            sleep(30)
            output = local_host.send_command('ifconfig eth0')
            regular = re.search(r'192\.168\.168\.2[0-2]\s+', str(output), re.S|re.I)
            if regular:
                flag = True
                logger.info('dhcp eth0:{}'.format(regular.group()))
                break

        pidof = local_host.send_command('pidof dhclient')
        if pidof:
            local_host.send_command('kill {}'.format(pidof))
        
        sleep(2)
        local_host.send_command('ifconfig eth0 {}'.format(PC1_LAN_IP))
        Assertion.assert_equal(flag, True, 'ERR: test traffic failed')


class Test_20_IP_Helper_V3_TP2169_tc_1510563(Test):
    uuid = "SOSAIOT-TC-56347"
    description= show_testcase_info(Parameter.TESTPLAN, '1510563', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510563')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_disable_DHCP_policy(self):
        logger.info('disable DHCP policy...')
        policy_dict = {
            'policy': 'DHCP',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: disable DHCP failed')

    @repeat_method(3)
    def test_02_test_traffic(self):
        logger.info('test traffic...')
        flag = False
        cmds = (
            'dhclient eth0 &> /tmp/dhcp.txt',
            'ifconfig eth0 >> /tmp/dhcp.txt'
        )
        for cmd in cmds:
            local_host.send_command(cmd)
            sleep(16)

        
        pidof = local_host.send_command('pidof dhclient')
        if pidof:
            local_host.send_command('kill {}'.format(pidof))
        sleep(2)
        local_host.send_command('ifconfig eth0 {}'.format(PC1_LAN_IP))
        with open('/tmp/dhcp.txt', 'r') as f:
            content = f.read()
        logger.info('dhcp.txt content:{}'.format(content))
        local_host.send_command('rm -f /tmp/dhcp.txt')
        if not re.search(r'192\.168\.168\.2[0-2]\s+', str(content), re.S|re.I) and \
            re.search(r'{}'.format(PC1_LAN_IP), str(content), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test traffic failed')


class Test_21_IP_Helper_V3_TP2169_tc_1510564(Test):
    uuid = "SOSAIOT-TC-56348"
    description= show_testcase_info(Parameter.TESTPLAN, '1510564', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510564')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_DHCP_policy(self):
        logger.info('enable DHCP policy...')
        policy_dict = {
            'policy': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable DHCP failed')

    def test_02_disable_ip_helper(self):
        logger.info('enable ip helper...')
        rc = iphelper.disable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: disable ip helper  failed')

    @repeat_method(3)
    def test_03_test_traffic(self):
        logger.info('test traffic...')
        flag = False
        cmds = (
            'dhclient eth0 &> /tmp/dhcp.txt',
            'ifconfig eth0 >> /tmp/dhcp.txt'
        )
        for cmd in cmds:
            local_host.send_command(cmd)
            sleep(16)

        
        pidof = local_host.send_command('pidof dhclient')
        if pidof:
            local_host.send_command('kill {}'.format(pidof))
        sleep(2)
        local_host.send_command('ifconfig eth0 {}'.format(PC1_LAN_IP))
        with open('/tmp/dhcp.txt', 'r') as f:
            content = f.read()
        logger.info('dhcp.txt content:{}'.format(content))
        local_host.send_command('rm -f /tmp/dhcp.txt')
        pc2_ssh.send_command('service dhcpd stop')
        if not re.search(r'192\.168\.168\.2[0-2]\s+', str(content), re.S|re.I) and \
            re.search(r'{}'.format(PC1_LAN_IP), str(content), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test traffic failed')


class Test_22_IP_Helper_V3_TP2169_tc_1510518(Test):
    uuid = "SOSAIOT-TC-56308"
    description= show_testcase_info(Parameter.TESTPLAN, '1510518', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510518')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_download_tsr_and_verify_ip_helper(self):
        logger.info('download tsr and verify ip helper config...')
        flag = False
        output = diagObj.get_tsr_part(func = 'Network', lab1 = 'IP Helper')
        logger.info(output)
        if re.search(r'DHCP.+Interface X0.+Enable', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: download tsr and verify ip helper failed')


class Test_23_IP_Helper_V3_TP2169_tc_1510554(Test):
    uuid = "SOSAIOT-TC-56339"
    description = show_testcase_info(Parameter.TESTPLAN, "1510554", description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510554')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    #already configure X1 as WAN, add dns iphelper policy
    #steps: disable ip helper
    # 1. enable dns protocol, disable dns ip helper policy -> test traffic (failed)
    # 2. enable dns ip helper policy -> test traffic (failed)
    # 3. enable ip helper and dns policy -> test traffic (pass)
    def test_03_01_enable_dns_protocol(self):
        dns_protocol_opt = {
            'protocol': 'DNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**dns_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dns protocol failed!")

    def test_03_02_create_dns_policy(self):
        iphelper_dns_opt = {
            'protocol': 'DNS',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dns ip helper policy failed!")

    def test_03_03_disable_dns_policy(self):
        iphelper_dns_opt = {
            'policy': 'DNS',
            'enable': False
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp ip helper policy failed!")

    def test_03_04_test_traffic_failed(self):
        pc2_ssh.send_command("tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "Test traffic still success while dns policy disabled!")

    def test_03_05_enable_dns_policy(self):
        iphelper_dns_opt = {
            'policy': 'DNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_policy(**iphelper_dns_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp ip helper policy failed!")

    def test_03_06_test_traffic_failed(self):
        pc2_ssh.send_command("tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_not_regular(output, r'shanghai_automation', "Test traffic still success while ip helper disabled!")

    def test_03_07_enable_iphelper(self):
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper failed!")

    @repeat_method(3)
    def test_03_08_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")

    def test_03_09_delete_dns_iphelper_policy(self):
        del_json = {
            'protocol': 'DNS',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete DNS ip helper policy failed!")


class Test_24_IP_Helper_V3_TP2169_tc_1510565(Test):
    uuid = "SOSAIOT-TC-56349"
    description = show_testcase_info(Parameter.TESTPLAN, "1510565", description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510565')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    # 1.disable dhcp server on fw (already done in conf_tb.py)
    # 2.disable dhcp protocol -> test traffic (failed)
    # 3.enable dhcp protocol -> test traffic (pass)
    def test_04_01_disable_dhcp_protocol(self):
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': False
        }
        rc = iphelper.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcp protocol failed!")

    def test_04_02_create_dhcp_iphelper_policy(self):
        iphelper_dhcp_opt = {
            'protocol': 'DHCP',
            'src': 'X0',
            'dsn': 'WAN Host',
        }
        rc = iphelper.add_iphelper_policy(**iphelper_dhcp_opt)
        Assertion.assert_equal(rc, True, "ERR: Add dhcp ip helper policy failed!")

    def test_04_03_restart_dhcp_server_on_PC2(self):
        logger.info("***       Restarting DHCP Server On PC2      ***")
        pc2_ssh.send_command('systemctl restart dhcpd')
        out = pc2_ssh.send_command('systemctl status dhcpd')
        Assertion.assert_regular(out, r'running', "ERR: Restart DHCP on PC2 failed!")

    def test_04_04_test_dhcp_traffic_failed(self):
        rc = test_dhcp_traffic()
        kill_dhclient()
        Assertion.assert_equal(rc, False, "ERR: While dhcp protocol disabled, the dhcp traffic could still pass")

    def test_04_05_enable_dhcp_protocol(self):
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable dhcp protocol failed!")

    def test_04_06_test_dhcp_traffic_pass(self):
        rc = test_dhcp_traffic()
        kill_dhclient()
        Assertion.assert_equal(rc, True, "ERR: Test dhcp traffic failed!")

    def test_04_07_delete_dhcp_iphelper_policy(self):
        del_json = {
            'protocol': 'DHCP',
            'source': 'X0',
        }
        rc = iphelper.delete_iphelper_policy(**del_json)
        Assertion.assert_equal(rc, True, "ERR: Delete dhcp ip helper policy failed!")


class Test_25_IP_Helper_V3_TP2169_tc_1510534(Test):
    uuid = "SOSAIOT-TC-56320"
    description = show_testcase_info(Parameter.TESTPLAN, "1510534", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510534')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao_dict1 = {
            'object_type':'network',
            'name':'1510534',
            'zone':'LAN',
            'value': '3.3.3.0,255.255.255.0',
        }
        rc = addressObj.config_addressobject(**ao_dict1)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'user_defined',
            'src': 'X0',
            'destination': {
                'name': '1510534'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    def test_03_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'user_defined',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_26_IP_Helper_V3_TP2169_tc_1510538(Test):
    uuid = "SOSAIOT-TC-56324"
    description= show_testcase_info(Parameter.TESTPLAN, '1510538', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510538')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_enable_dns_protocol(self):
        logger.info('enable dns protocol...')
        dns ={
            'enable': True
        }
        rc = iphelper.edit_protocol(name='DNS', **dns)
        Assertion.assert_equal(rc, True, 'ERR: enable dns protocol failed')

    def test_02_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DNS',
            'src': 'X0',
            'destination': {
                'name': 'WAN Host'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    @repeat_method(3)
    def test_03_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")

    def test_04_reboot_fw_and_check_ip_helper(self):
        logger.info('reboot fw and check ip helper...')
        flag = False
        settingObj.boot_fw(mode=1)
        output = iphelper.get_policy()
        logger.info(output)
        if output['ip_helper']['policy'][0]['protocol'] == 'DNS':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: reboot fw and check ip helper failed')

    @repeat_method(3)
    def test_05_test_traffic_pass(self):
        sleep(30)
        pc2_ssh.send_command("nohup tcpdump -i eth0 -A -nn -c 10 udp > /tmp/sniff_msg.txt 2>&1 &")
        dns_traffic()
        output = pc2_ssh.send_command('cat /tmp/sniff_msg.txt')
        logger.info(output)
        pc2_ssh.send_command('rm -f /tmp/sniff_msg.txt ')  # delete this file
        Assertion.assert_regular(output, r'shanghai_automation', "ERR: Test dns traffic failed!")
        
    def test_06_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DNS',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_27_IP_Helper_V3_TP2169_tc_1510536(Test):
    uuid = "SOSAIOT-TC-56322"
    description= show_testcase_info(Parameter.TESTPLAN, '1510536', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510536')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
 
    def test_01_add_ip_helper_policy(self):
        logger.info('add ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'src': 'X0',
            'destination': {
                'name': 'WAN Host'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add ip helper policy failed')

    @repeat_method(3)
    def test_02_test_traffic(self):
        logger.info('test traffic...')
        flag = False
        local_host.send_command('ifconfig eth1 down')
        pc2_ssh.send_command('service dhcpd restart')
        local_host.send_command('dhclient eth0 &')
        for i in range(20):
            sleep(30)
            output = local_host.send_command('ifconfig eth0')
            regular = re.search(r'192\.168\.168\.2[0-2]\s+', str(output), re.S|re.I)
            if regular:
                flag = True
                logger.info('dhcp eth0:{}'.format(regular.group()))
                break

        pidof = local_host.send_command('pidof dhclient')
        if pidof:
            local_host.send_command('kill {}'.format(pidof))
        
        sleep(2)
        local_host.send_command('ifconfig eth0 {}'.format(PC1_LAN_IP))
        Assertion.assert_equal(flag, True, 'ERR: test traffic failed')

    def test_03_reboot_fw_and_check_ip_helper(self):
        logger.info('reboot fw and check ip helper...')
        flag = False
        settingObj.boot_fw(mode=1)
        output = iphelper.get_policy()
        logger.info(output)
        if output['ip_helper']['policy'][0]['protocol'] == 'DHCP':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: reboot fw and check ip helper failed')

    @repeat_method(3)
    def test_04_test_traffic(self):
        logger.info('test traffic...')
        flag = False
        local_host.send_command('ifconfig eth1 down')
        pc2_ssh.send_command('service dhcpd restart')
        local_host.send_command('dhclient eth0 &')
        for i in range(20):
            sleep(30)
            output = local_host.send_command('ifconfig eth0')
            regular = re.search(r'192\.168\.168\.2[0-2]\s+', str(output), re.S|re.I)
            if regular:
                flag = True
                logger.info('dhcp eth0:{}'.format(regular.group()))
                break

        pidof = local_host.send_command('pidof dhclient')
        if pidof:
            local_host.send_command('kill {}'.format(pidof))
        
        sleep(2)
        local_host.send_command('ifconfig eth0 {}'.format(PC1_LAN_IP))
        Assertion.assert_equal(flag, True, 'ERR: test traffic failed')

    def test_05_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'DHCP',
            'source': {'interface': 'X0'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_28_IP_Helper_V3_TP2169_tc_1510559(Test):
    uuid = "SOSAIOT-TC-56344"
    description= show_testcase_info(Parameter.TESTPLAN, '1510559', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510559')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_add_time_server_address_object(self):
        logger.info('add time server address object...')
        ao_dict = {
            'object_type':'host',
            'name':'time_server',
            'zone':'LAN',
            'value': '3.3.3.22',
        }
        rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add address object failed')

    def test_02_enable_time_ip_helper(self):
        logger.info('enable time ip helper...')
        policy_dict = {
            'protocol': 'TIME',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable time policy failed')

    def test_03_add_time_iphelper_policy(self):
        logger.info('add time iphelper policy...')
        policy_dict = {
            'protocol': 'TIME',
            'src': 'X2',
            'destination': {
                'name': 'time_server'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add time ip helper policy failed')
    
    def test_04_change_route_on_pc1_and_pc2(self):
        logger.info('change route on pc1 and pc2...')
        flag = False
        local_host.send_command('route add -net 3.3.3.0/24 gw {}'.format(Parameter.X2_IP))
        pc2_ssh.send_command('route add -net 2.2.2.0/24 gw {}'.format(Parameter.X3_IP))

        output1 = local_host.send_command('route -n ')
        output2 = pc2_ssh.send_command('route -n ')
        logger.info(output1)
        logger.info(output2)
        if re.search(r'3.3.3.0\s+{}'.format(Parameter.X2_IP), str(output1), re.S|re.I) and \
           re.search(r'2.2.2.0\s+{}'.format(Parameter.X3_IP), str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: change route on pc1 and pc2 failed')

    def test_05_capture_packets_and_check(self):
        logger.info('capture packets and check...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'python3 {}/time_service.py'.format(confPath)
        local_host.send_command(cmd)
        sleep(5)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Dst=\[{}\]\s+UDP Packet Header\s+Src=\[\d+\], Dst=\[37\]'.format(PC2_ETH2_IP), str(output), re.S|re.I) and \
            re.search(r'Src=\[{}\],\s+Dst=\[{}\]'.format(PC1_ETH2_IP, PC2_ETH2_IP), str(output), re.S|re.I) and \
            re.search(r'Src=\[{}\],\s+Dst=\[{}\]'.format(PC2_ETH2_IP, PC1_ETH2_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: capture packets and check failed')

    
class Test_29_IP_Helper_V3_TP2169_tc_1510539(Test):
    uuid = "SOSAIOT-TC-56325"
    description= show_testcase_info(Parameter.TESTPLAN, '1510539', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510539')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_reboot_fw_and_check_ip_helper(self):
        logger.info('reboot fw and check ip helper...')
        flag = False
        settingObj.boot_fw(mode=1)
        output = iphelper.get_policy()
        logger.info(output)
        if output['ip_helper']['policy'][0]['protocol'] == 'TIME':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: reboot fw and check ip helper failed')
    
    def test_02_capture_packets_and_check(self):
        logger.info('capture packets and check...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'python3 {}/time_service.py'.format(confPath)
        local_host.send_command(cmd)
        sleep(5)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Dst=\[{}\]\s+UDP Packet Header\s+Src=\[\d+\], Dst=\[37\]'.format(PC2_ETH2_IP), str(output), re.S|re.I) and \
            re.search(r'Src=\[{}\],\s+Dst=\[{}\]'.format(PC1_ETH2_IP, PC2_ETH2_IP), str(output), re.S|re.I) and \
            re.search(r'Src=\[{}\],\s+Dst=\[{}\]'.format(PC2_ETH2_IP, PC1_ETH2_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: capture packets and check failed')
        
    def test_03_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'TIME',
            'source': {'interface': 'X2'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')

        
class Test_30_IP_Helper_V3_TP2169_tc_1510527(Test):
    uuid = "SOSAIOT-TC-56315"
    description= show_testcase_info(Parameter.TESTPLAN, '1510527', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510527')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_enable_time_ip_helper(self):
        logger.info('enable time ip helper...')
        policy_dict = {
            'protocol': 'mDNS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable time policy failed')

    def test_02_add_time_iphelper_policy(self):
        logger.info('add time iphelper policy...')
        policy_dict1 = {
            'protocol': 'mDNS',
            'src': 'X2',
            'destination': {
                'name': 'X3 Subnet'
            },
            'enable': True
        }
        policy_dict2 = {
            'protocol': 'mDNS',
            'src': 'X3',
            'destination': {
                'name': 'X2 Subnet'
            },
            'enable': True
        }
        rc = iphelper.add_iphelper_policy(**policy_dict1)
        rc &= iphelper.add_iphelper_policy(**policy_dict2)
        Assertion.assert_equal(rc, True, 'ERR: add time ip helper policy failed')
    
    def test_03_start_mDNS_and_capture_packets(self):
        logger.info('start mDNS and capture packets...')
        cmds = (
                'sudo yum install -y avahi-tools',
                'sudo yum start avahi-tools'
        )
        for cmd in cmds:
            local_host.send_command(cmd)
            pc2_ssh.send_command(cmd)
 
        sleep(10)
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'avahi-resolve-address {}'.format(PC2_ETH2_IP)
        local_host.send_command(cmd)
        sleep(5)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[224.0.0.251\]\s+UDP Packet Header\s+Src=\[5353\], Dst=\[5353\]'.format(PC1_ETH2_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: start mDNS and capture packets failed')

            
class Test_31_IP_Helper_V3_TP2169_tc_1510529(Test):
    uuid = "SOSAIOT-TC-56317"
    description= show_testcase_info(Parameter.TESTPLAN, '1510529', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510529')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    @repeat_method(3)
    def test_01_start_mDNS_and_capture_packets(self):
        logger.info('start mDNS and capture packets...')
        sleep(60)
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'avahi-resolve-address {}'.format(PC2_ETH2_IP)
        local_host.send_command(cmd)
        sleep(10)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[224.0.0.251\]\s+UDP Packet Header\s+Src=\[5353\], Dst=\[5353\]'.format(PC1_ETH2_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: start mDNS and capture packets failed')


class Test_32_IP_Helper_V3_TP2169_tc_1510543(Test):
    uuid = "SOSAIOT-TC-56328"
    description= show_testcase_info(Parameter.TESTPLAN, '1510543', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510543')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_reboot_fw_and_check_ip_helper(self):
        logger.info('reboot fw and check ip helper...')
        flag = False
        settingObj.boot_fw(mode=1)
        output = iphelper.get_policy()
        logger.info(output)
        if output['ip_helper']['policy'][0]['protocol'] == 'mDNS' and \
            output['ip_helper']['policy'][1]['protocol'] == 'mDNS':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: reboot fw and check ip helper failed')

    def test_02_start_mDNS_and_capture_packets(self):
        logger.info('start mDNS and capture packets...')
        sleep(10)
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'avahi-resolve-address {}'.format(PC2_ETH2_IP)
        local_host.send_command(cmd)
        sleep(5)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[224.0.0.251\]\s+UDP Packet Header\s+Src=\[5353\], Dst=\[5353\]'.format(PC1_ETH2_IP), str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: start mDNS and capture packets failed')
   
    def test_03_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict1 = {
            'protocol': 'mDNS',
            'source': {'interface': 'X2'}
        }
        policy_dict2 = {
            'protocol': 'mDNS',
            'source': {'interface': 'X3'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict1)
        rc &= iphelper.delete_iphelper_policy(**policy_dict2)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_33_IP_Helper_V3_TP2169_tc_1510544(Test):
    uuid = "SOSAIOT-TC-56329"
    description= show_testcase_info(Parameter.TESTPLAN, '1510544', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510544')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_get_ip_helper_protocol_and_check_sequence(self):
        logger.info('get ip helper protocols...')
        flag = False
        output = iphelper.get_protocol(protocol='All')
        logger.info(output)
        if output['ip_helper']['protocol'][0]['name'] == 'DHCP' and \
            output['ip_helper']['protocol'][1]['name'] == 'NetBIOS' and \
            output['ip_helper']['protocol'][2]['name'] == 'DNS' and \
            output['ip_helper']['protocol'][3]['name'] == 'TIME' and \
            output['ip_helper']['protocol'][4]['name'] == 'WOL' and \
            output['ip_helper']['protocol'][5]['name'] == 'mDNS' and \
            output['ip_helper']['protocol'][6]['name'] == 'SSDP' and \
            output['ip_helper']['protocol'][7]['name'] == 'DHCPv6':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: get ip helper protocols and check sequence  failed')


class Test_34_IP_Helper_V3_TP2169_tc_1510519(Test):
    uuid = "SOSAIOT-TC-56309"
    description= show_testcase_info(Parameter.TESTPLAN, '1510519', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510519')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_enable_netbios_ip_helper(self):
        logger.info('enable netbios ip helper...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable netbios policy failed')

    def test_02_add_netbios_iphelper_policy(self):
        logger.info('add time iphelper policy...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'source':{
                'name': 'X2 Subnet'
            },
            'destination': {
                'name': 'X3 Subnet'
            },
            'enable': True
        }
      
        rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add netbios ip helper policy failed')
    
    def test_03_edit_hosts_and_test_netbios(self):
        logger.info('edit hosts and test netbios...')
        cmd = 'echo "{} bbb" >> /etc/hosts'.format(PC2_ETH2_IP)
        local_host.send_command(cmd)
        nmb = 'systemctl start nmb'
        local_host.send_command(nmb)
        pc2_ssh.send_command(nmb)
        sleep(5)
        flag =False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'nmblookup -A bbb'
        local_host.send_command(cmd)
        sleep(3)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[{}\]\s+UDP Packet Header\s+Src=\[\d+\], Dst=\[137\]'.format(PC1_ETH2_IP,PC2_ETH2_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: edit hosts and test netbios failed')


class Test_35_IP_Helper_V3_TP2169_tc_1510520(Test):
    uuid = "SOSAIOT-TC-56310"
    description= show_testcase_info(Parameter.TESTPLAN, '1510520', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510520')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_disable_netbios_ip_helper(self):
        logger.info('disable netbios ip helper...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'enable': False
        }
        rc = iphelper.edit_iphelper_protocol(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: disable netbios policy failed')

    @repeat_method(3)
    def test_02_test_netbios_and_capture_packets(self):
        logger.info('test netbios and capture packets...')
        flag =False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'nmblookup -A bbb'
        local_host.send_command(cmd)
        sleep(120)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'DROPPED, Drop Code: \d+\(Broadcast traffic not handled.*Src=\[{}\], Dst=\[2.2.2.255\]'.format(Parameter.PC2_ETH1), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test netbios and capture packets failed')


class Test_36_IP_Helper_V3_TP2169_tc_1510521(Test):
    uuid = "SOSAIOT-TC-56311"
    description= show_testcase_info(Parameter.TESTPLAN, '1510521', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510521')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_enable_netbios_ip_helper(self):
        logger.info('disable netbios ip helper...')
        policy_dict = {
            'protocol': 'NetBIOS',
            'enable': True
        }
        rc = iphelper.edit_iphelper_protocol(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: enable netbios policy failed')

    def test_02_disable_ip_helper(self):
        logger.info('disable ip helper....')
        rc = iphelper.disable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: disable ip helper failed')

    @repeat_method(3)
    def test_03_test_netbios_and_capture_packets(self):
        logger.info('test netbios and capture packets...')
        flag =False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'nmblookup -A bbb'
        local_host.send_command(cmd)
        sleep(120)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'DROPPED, Drop Code: \d+\(Broadcast traffic not handled.*Src=\[{}\], Dst=\[2.2.2.255\]'.format(Parameter.PC2_ETH1), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test netbios and capture packets failed')


class Test_37_IP_Helper_V3_TP2169_tc_1510522(Test):
    uuid = "SOSAIOT-TC-56312"
    description= show_testcase_info(Parameter.TESTPLAN, '1510522', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510522')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_enable_ip_helper(self):
        logger.info('enable ip helper....')
        rc = iphelper.enable_iphelper()
        Assertion.assert_equal(rc, True, 'ERR: enable ip helper failed')

    def test_02_config_interface_x2_dmz(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_03_config_interface_x3_dmz(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_04_test_netbios_and_capture_packets(self):
        logger.info('test netbios and capture packets...')
        flag =False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'nmblookup -A bbb'
        local_host.send_command(cmd)
        sleep(10)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[{}\]\s+UDP Packet Header\s+Src=\[\d+\], Dst=\[137\]'.format(PC1_ETH2_IP,PC2_ETH2_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test netbios and capture packets failed')

    def test_05_config_interface_x2_lan(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_06_config_interface_x3_lan(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")
    
   
class Test_38_IP_Helper_V3_TP2169_tc_1510537(Test):
    uuid = "SOSAIOT-TC-56323"
    description= show_testcase_info(Parameter.TESTPLAN, '1510537', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510537')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_reboot_fw_and_check_ip_helper(self):
        logger.info('reboot fw and check ip helper...')
        flag = False
        settingObj.boot_fw(mode=1)
        output = iphelper.get_policy()
        logger.info(output)
        if output['ip_helper']['policy'][0]['protocol'] == 'NetBIOS':
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: reboot fw and check ip helper failed')

    def test_02_test_netbios_and_capture_packets(self):
        logger.info('test netbios and capture packets...')
        flag =False
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'nmblookup -A bbb'
        local_host.send_command(cmd)
        sleep(10)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r'Src=\[{}\], Dst=\[{}\]\s+UDP Packet Header\s+Src=\[\d+\], Dst=\[137\]'.format(PC1_ETH2_IP,PC2_ETH2_IP), str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test netbios and capture packets failed')


class Test_39_IP_Helper_V3_TP2169_tc_1510548(Test):
    uuid = "SOSAIOT-TC-56333"
    description= show_testcase_info(Parameter.TESTPLAN, '1510548', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1510548')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
     
    def test_01_export_tsr_and_check(self):
        logger.info('export tsr and check...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : IP Helper')
        logger.info(output)
        if re.search(r'NetBIOS\s+138\s+,137', str(output), re.S|re.I) and \
            re.search(r'NetBIOS\s+X2 Subnet\s+X3 Subnet\s+Enabled', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: test netbios and capture packets failed')

    def test_02_delete_ip_helper_policy(self):
        logger.info('delete ip helper policy...')
        policy_dict = {
            'protocol': 'NETBIOS',
            'source': {'name': 'X2 Subnet'}
        }
        rc = iphelper.delete_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: delete ip helper policy failed')


class Test_40_IP_Helper_V3_TP2169_tc_1532480(Test):
    uuid = "SOSAIOT-TC-56350"
    description= show_testcase_info(Parameter.TESTPLAN, '1532480', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1532480')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')
    
    def test_01_add_load_testing_address_object(self):
        logger.info('add load testing address object...')
        for i in range(1000):
            ao_dict = {
                'object_type':'host',
                'name':'Load_Testing_Object{}'.format(i),
                'zone':'LAN',
                'value': '2.2.2.3',
            }
            rc = addressObj.config_addressobject(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add load testing address object failed')
   
    def test_02_add_load_testing_address_group(self):
        logger.info('add load testing address group...')
        for i in range(1000):
            ao_dict = {
                "address_groups": [
                    {
                        "ipv4": {
                            "address_object": {
                                "ipv4": [
                                    {
                                        "name": "time_server"
                                    }
                                ]
                            },
                            "name": "Load_Testing_Group{}".format(i)
                        }
                    }
                ]
            }
            rc = address_groupObj.add_addressgroup(**ao_dict)
        Assertion.assert_equal(rc, True, 'ERR: add load testing address group failed')

    def test_03_add_time_iphelper_policy(self):
        logger.info('add time iphelper policy...')
        # for i in range(2):
        #     policy_dict = {
        #         "ip_helper": {
        #             "policy": [
        #             {
        #                 "protocol": "NetBIOS",
        #                 "source": {
        #                     "name": "Load_Testing_Object{}".format(i)
        #                 },
        #                 "destination": '',
        #                 "enable": True,
        #                 "comment": "test"
        #             }
        #             ]
        #         }
        #     }
        #     for j in range(2):
        #         dest_dict = {'destination': {
        #             'name': 'time_server{}'.format(j)
        #         },
        #         }
        #         policy = copy.deepcopy(policy_dict)
        #         policy['ip_helper']['policy'][0]['destination'] = dest_dict['destination']
        #         rc = iphelper.add_policy(**policy)
        #         logger.info(policy_dict)
        for i in range(4):
            policy_dict = {
                'protocol': 'TIME',
                'src': 'X{}'.format(i),
                'destination': {
                    'name': 'time_server'
                },
                'enable': True
            }
            rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add time ip helper policy failed')

    def test_04_add_dhcp_iphelper_policy(self):
        logger.info('add dhcp iphelper policy...')
        for i in range(4):
            policy_dict = {
                'protocol': 'DHCP',
                'src': 'X{}'.format(i),
                'destination': {
                    'name': 'time_server'
                },
                'enable': True
            }
            rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add dhcp ip helper policy failed')

    def test_05_add_mdns_iphelper_policy(self):
        logger.info('add mdns iphelper policy...')
        for i in range(4):
            policy_dict = {
                'protocol': 'mDNS',
                'src': 'X{}'.format(i),
                'destination': {
                    'name': 'time_server'
                },
                'enable': True
            }
            rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add mdns ip helper policy failed')
    
    def test_06_add_dns_iphelper_policy(self):
        logger.info('add dns iphelper policy...')
        for i in range(4):
            policy_dict = {
                'protocol': 'DNS',
                'src': 'X{}'.format(i),
                'destination': {
                    'name': 'time_server'
                },
                'enable': True
            }
            rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add dns ip helper policy failed')

    def test_07_add_dhcpv6_iphelper_policy(self):
        logger.info('add dhcpv6 iphelper policy...')
        for i in range(4):
            policy_dict = {
                'protocol': 'SSDP',
                'src': 'X{}'.format(i),
                'destination': {
                    'name': 'time_server'
                },
                'enable': True
            }
            rc = iphelper.add_iphelper_policy(**policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: add dhcpv6 ip helper policy failed')