from definition.parameter import *

class Test_API_IP_helper_Smoke_01(Test):

    uuid = "SOSAIOT-TC-47033"
    description = show_testcase_info(Parameter.TESTPLAN,"1508716", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508716')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_get_iphelper_base(self):
        output = iphelperApi.get_iphelper_settings()
        print(type(output['ip_helper']['enable']))
        Assertion.assert_equal(output['ip_helper']['enable'], False, "ERR: can not get base info")

    def test_01_02_enable_iphelper(self):
        resp = iphelperApi.enable_iphelper()
        Assertion.assert_equal(resp, True, "ERR:enable IP Helper failed")
        output = iphelperApi.get_iphelper_settings()
        Assertion.assert_equal(output['ip_helper']['enable'], True, "ERR: can not get base info")


class Test_API_IP_helper_Smoke_02(Test):

    uuid = "SOSAIOT-TC-47036"
    description = show_testcase_info(Parameter.TESTPLAN,"1508719", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508719')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_create_dhcpv6_policy(self):
        dhcpv6_policy_json = {
            "ip_helper": {
              "policy": [{
                "egressif": "X2",
                "protocol": "DHCPv6",
                "source": {"interface": "X0"},
                "destination": {"ipv6": "2001:2019::100"},
                "enable": True,
                "comment": "dhcpv6"}
                ]
            }
        }
        output = iphelperApi.add_policy(**dhcpv6_policy_json)
        Assertion.assert_equal(output, True, "ERR: can not create dhcpv6 policy")

    def test_02_02_get_policy(self):
        response = iphelperApi.get_policy()
        Assertion.assert_equal(response["ip_helper"]['policy'][0]['protocol'], 'DHCPv6', "can not find policy")
        Assertion.assert_equal(response["ip_helper"]['policy'][0]['source']['interface'],'X0', "can not find policy")
        Assertion.assert_equal(response["ip_helper"]['policy'][0]['destination']['ipv6'],'2001:2019::100', "can not find policy")
        Assertion.assert_equal(response["ip_helper"]['policy'][0]['egressif'],'X2', "can not find policy")


class Test_API_IP_helper_Smoke_03(Test):

    uuid = "SOSAIOT-TC-47038"
    description = show_testcase_info(Parameter.TESTPLAN,"1508721", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508721')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_get_iphelper_protocols(self):
        response = iphelperApi.get_protocol(protocol='All')
        expected_protocols = [
            {"name": "DHCP", "port1": 67, "port2": 68, "enable": False, "timeout": "30"},
            {"name": "NetBIOS", "port1": 138, "port2": 137, "enable": False, "timeout": "40"},
            {"name": "DNS", "port1": 53, "port2": 0, "enable": False, "timeout": "30"},
            {"name": "TIME", "port1": 37, "port2": 0, "enable": False, "timeout": "30"},
            {"name": "WOL", "port1": 7, "port2": 9, "enable": False, "timeout": "30"},
            {"name": "mDNS", "port1": 5353, "port2": 0, "enable": False, "timeout": "30"},
            {"name": "SSDP", "port1": 1900, "port2": 1901, "enable": False, "timeout": "30"},
            {"name": "DHCPv6", "port1": 547, "port2": 546, "enable": False, "timeout": "30"},
        ]

        for i, protocol in enumerate(expected_protocols):
            Assertion.assert_equal(response["ip_helper"]['protocol'][i]['name'], protocol['name'], "can not find protocol")
            Assertion.assert_equal(response["ip_helper"]['protocol'][i]['port1']['value'], protocol['port1'], "can not find protocol")
            Assertion.assert_equal(response["ip_helper"]['protocol'][i]['enable'], protocol['enable'], "can not find protocol")
            Assertion.assert_equal(response["ip_helper"]['protocol'][i]['timeout'], protocol['timeout'], "can not find protocol")

        Assertion.assert_equal(response["ip_helper"]['protocol'][2]['port2'], {}, "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][3]['port2'], {}, "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][5]['port2'], {}, "can not find protocol")


class Test_API_IP_helper_Smoke_04(Test):
    uuid = "SOSAIOT-TC-47039"
    description = show_testcase_info(Parameter.TESTPLAN,"1508722", description=True)['title']

    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508722')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_get_protocol(self):
        flag = False
        response = iphelperApi.get_protocol('DHCP')
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['enable'] , False, "can not find protocol")

    def test_04_02_edit_protocol(self):
        json = {
            'enable':True
        }
        output = iphelperApi.edit_protocol('DHCP', **json)
        Assertion.assert_equal(output, True, "edit protocol failed")
        response = iphelperApi.get_protocol('DHCP')
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['enable'] , True, "can not find protocol")


class Test_API_IP_helper_Smoke_05(Test):
    uuid = "SOSAIOT-TC-47040"
    description = show_testcase_info(Parameter.TESTPLAN,"1508723", description=True)['title']

    def test_05_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508723')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_get_protocol(self):
        flag = False
        response = iphelperApi.get_protocol('DHCP')
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['timeout'] , '30', "can not find protocol")

    def test_05_02_edit_protocol(self):
        json = {
            'timeout':'50'
        }
        output = iphelperApi.edit_protocol('DHCP', **json)
        Assertion.assert_equal(output, True, "edit protocol failed")
        response = iphelperApi.get_protocol('DHCP')
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['timeout'] , '50', "can not find protocol")


class Test_API_IP_helper_Smoke_06(Test):
    uuid = "SOSAIOT-TC-47041"
    description = show_testcase_info(Parameter.TESTPLAN,"1508724", description=True)['title']

    def test_06_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1508724')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_add_protocol(self):
        usr_protocol = {
            'name': 'TEST',
            'port1': 321,
            'port2': 498,
            'timeout': 40,
            'enable': True
        }
        output = iphelperApi.add_protocol(**usr_protocol)
        Assertion.assert_equal(output, True, "add protocol failed")
        response = iphelperApi.get_protocol(protocol='TEST')
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['name'] , 'TEST', "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['port1'] ['value'], 321, "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['port2'] ['value'], 498, "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['enable'] , True, "can not find protocol")
        Assertion.assert_equal(response["ip_helper"]['protocol'][0]['timeout'] , '40', "can not find protocol")



    










