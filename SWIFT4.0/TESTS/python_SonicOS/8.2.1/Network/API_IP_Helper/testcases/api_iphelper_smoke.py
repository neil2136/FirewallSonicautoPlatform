from parameter import *


class Test_API_IP_helper_Smoke_01(Test):
    """
    1) get ip helper base info
    """
    uuid = "SOSAIOT-TC-47032"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "01", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_get_iphelper_base(self):
        output = iphelperApi.get_iphelper_settings()
        print(type(output['ip_helper']['enable']))
        Assertion.assert_equal(output['ip_helper']['enable'], False, "ERR: can not get base info")


class Test_API_IP_helper_Smoke_02(Test):
    """
    1) create a new policy with destination network AO
    2) change the policy with destination host AO
    """
    uuid = "SOSAIOT-TC-47034"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "02", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_create_ssdp_policy(self):
        ssdp_opt = {
            'protocol': 'SSDP',
            'src': 'x0',
            'dsn': 'X2 Subnet',
            'enable': False
        }
        output = iphelperApi.add_iphelper_policy(**ssdp_opt)
        Assertion.assert_equal(output, True, "ERR: can not create policy")
    
    def test_02_02_add_dst_host(self):
        address_objects_option = {
            'object_type': 'host',
            'name': 'test_ao',
            'zone': 'LAN',
            'value': '1.1.1.1'
        }
        output = addressObjectsApi.config_addressobject(**address_objects_option)
        Assertion.assert_equal(output, True, "can not add ao")

    def test_02_03_change_dst_ao(self):
        ssdp_opt_dst = {
            'policy': 'SSDP',
            'src': 'x0',
            'dst': 'test_ao',
            'enable': False
        }
        output = iphelperApi.change_iphelper_policy(**ssdp_opt_dst)
        Assertion.assert_equal(output, True, "ERR: can not create policy")

    def test_02_04_get_policy_dst(self):
        policies = iphelperApi.get_policy()
        for policy in policies['ip_helper']['policy']:
            if policy['protocol'] in 'SSDP':
                result = policy['destination']['name']
        Assertion.assert_equal(result, 'test_ao', "ERR: dst ao didn't change")


class Test_API_IP_helper_Smoke_03(Test):
    """
    1) create new dhcpv6 policy
    """
    uuid = "SOSAIOT-TC-47035"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "03", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_create_dhcpv6_policy(self):
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

    def test_03_02_verify_policy(self):
        flag = False
        try:
            policies = iphelperApi.get_policy()
            for policy in policies['ip_helper']['policy']:
                  if policy['protocol'] == "DHCPv6":
                      flag = True
                      break
        except Exception as e:
            logger.error(f'dhcpv6 policy cannot be found')
        Assertion.assert_equal(flag, True, "ERR: policy is not dhcpv6")


class Test_API_IP_helper_Smoke_04(Test):
    """
    1) create one disable policy
    2) change the policy to enable
    """
    uuid = "SOSAIOT-TC-47037"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "04", description=True)['title']

    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_verify_disable_policy(self):
        response = iphelperApi.get_policy()
        for item in response['ip_helper']['policy']:
            if item['protocol'] == "SSDP":
                result = item['enable']
                break
        rc = True if result else False
        Assertion.assert_equal(rc, False, "ERR: policy is enabled")

    def test_04_02_change_to_enable(self):
        ssdp_opt_true = {
            'policy': 'SSDP',
            'enable': True,
        }
        output = iphelperApi.edit_iphelper_policy(**ssdp_opt_true)
        Assertion.assert_equal(output, True, "ERR: cannot policy enabled")

    def test_04_03_verify_policy_enabled(self):
        response = iphelperApi.get_policy()
        for item in response['ip_helper']['policy']:
            if item['protocol'] == "SSDP":
                result = item['enable']
                break
        rc = True if result else False
        Assertion.assert_equal(rc, True, "ERR: policy is disabled")


class Test_API_IP_helper_Smoke_05(Test):
    """
    1) create one customer protocol
    2) delete the protocol
    """
    uuid = "SOSAIOT-TC-47042"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "05", description=True)['title']

    def test_05_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_create_protocol(self):
        test_protocol = {
            'name': 'test',
            'port1': 1000,
            'port2': 1000,
            'timeout': 30,
            'enable': True
        }
        output = iphelperApi.add_protocol(**test_protocol)
        Assertion.assert_equal(output, True, "ERR: can not create protocol")

    def test_05_02_get_protocol(self):
        flag = False
        response = iphelperApi.get_protocol('test')
        for item in response['ip_helper']['protocol']:
              if item['name'] == "test":
                    print('*' * 80)
                    flag = True
                    break
        Assertion.assert_equal(flag, True, "can not find protocol")

    def test_05_03_del_protocol(self):
        output = iphelperApi.del_protocol('test')
        Assertion.assert_equal(output, True, "cannot delete protocol")

    def test_05_04_verify_protocol_exist(self):
        flag = False
        try: 
            iphelperApi.get_protocol('test')
        except:
            flag = True
        Assertion.assert_equal(flag, False, "can find protocol")
        



if __name__ == "__main__":

#    testIPhelper = Test_API_IP_helper_Smoke_01()
#    testIPhelper.test_01_00_show_testplan()
#    testIPhelper.test_01_01_get_iphelper_base()
#    testIPhelper = Test_API_IP_helper_Smoke_02()
#    testIPhelper.test_02_00_show_testplan()
#    testIPhelper.test_02_01_create_ssdp_policy()
#    testIPhelper.test_02_02_add_dst_host()
#    testIPhelper.test_02_03_change_dst_ao()
#    testIPhelper.test_02_04_get_policy_dst()
#    testIPhelper = Test_API_IP_helper_Smoke_03()
#    testIPhelper.test_03_00_show_testplan()
#    testIPhelper.test_03_01_create_dhcpv6_policy()
#    testIPhelper.test_03_02_verify_policy()
    testIPhelper = Test_API_IP_helper_Smoke_04()
    testIPhelper.test_04_00_show_testplan()
    testIPhelper.test_04_01_verify_disable_policy()
    testIPhelper.test_04_02_change_to_enable()
    testIPhelper.test_04_03_verify_policy_enabled()
#    testIPhelper = Test_API_IP_helper_Smoke_05()
#    testIPhelper.test_05_00_show_testplan()
#    testIPhelper.test_05_01_create_protocol()
#    testIPhelper.test_05_02_get_protocol()
#    testIPhelper.test_05_03_del_protocol()
#    testIPhelper.test_05_04_verify_protocol_exist()
    testIPhelper = Test_API_IP_helper_Smoke_06()
    testIPhelper.test_teardown()
    










