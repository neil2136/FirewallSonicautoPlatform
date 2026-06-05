from definition.initial_parameter import *


class TestCustomZones_01(Test):
    uuid = '1523158'
    description= show_testcase_info(Parameter.TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_trusted_custom_zone(self):
        customer_zone = {
            "zones": [
                {
                    "name": "Test1",
                    "security_type": "trusted",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        rc = zone_obj.add_zone_object(**customer_zone)
        Assertion.assert_equal(rc, True, "ERR: add customer zone failed")         


class TestCustomZones_02(Test):
    uuid = '1523160'
    description= show_testcase_info(Parameter.TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_public_custom_zone(self):
        customer_zone = {
            "zones": [
                {
                    "name": "Test2",
                    "security_type": "public",
                    "interface_trust": True,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_from_higher": True,
                        "allow_to_lower": True,
                        "deny_from_lower": True
                    },
                    "gateway_anti_virus": True,
                    "intrusion_prevention": False
                }
            ]
        }
        rc = zone_obj.add_zone_object(**customer_zone)
        Assertion.assert_equal(rc, True, "ERR: add customer zone failed")         


class TestCustomZones_03(Test):
    uuid = '1523161'
    description= show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_Config_X2(self):
        x2_custom = {
            'if': 'X2',
            'zone': 'Test1', 
            'mode': 'static',
            'ip': Parameter.X2_IP,
        }
        rc = interface_obj.config_interface(**x2_custom)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed") 

    def test_02_Set_pc2_route(self):
        ret = PC2_login.send_command('route add -host {} gw {}'.format(PC1_ETH0_IP, Parameter.X2_IP))
        if ret == b'':
            logger.info("Add route to PC2 pass")
        else:
            logger.info("Add route to PC2 fail")
        result = PC2_login.send_command('ip -4 r')
        logger.info(result)
        Assertion.assert_regular(result, '192.168.168.169 via 14.1.1.168 dev eth2', "ERR: Set route on PC2 failed")

    def test_03_Verify_traffic(self):
        result = os.popen('ping {} -c 10 -I eth0'.format(PC2_ETH2_IP))
        output = result.read()
        logger.info(output)
        Assertion.assert_not_regular(output, '100% packet loss', "ERR: Verify traffic failed")


class TestCustomZones_04(Test):
    uuid = '1523162'
    description= show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_Config_X2(self):
        x2_custom = {
            'if': 'X2',
            'zone': 'Test2', 
            'mode': 'static',
            'ip': Parameter.X2_IP,
        }
        rc = interface_obj.config_interface(**x2_custom)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed") 

    def test_02_Verify_traffic_from_X0PC_to_X2PC(self):
        result = os.popen('ping {} -c 10 -I eth0'.format(PC2_ETH2_IP))
        output = result.read()
        logger.info(output)
        Assertion.assert_not_regular(output, '100% packet loss', "ERR: Verify traffic failed")

    def test_03_Verify_traffic_from_X2PC_to_X0PC(self):
        flag = False
        result = PC2_login.send_command('ping {} -c 10 -I eth2'.format(PC1_ETH0_IP))
        logger.info(result)
        if "100% packet loss" in result:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify traffic failed")
