from definition.init_param import *


class Test_01_Multiple_WAN_Phase_1_Smoke_tc_01(Test):
    uuid = "SOSAIOT-TC-57389"
    description= show_testcase_info(Parameter.TESTPLAN, '1524041', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524041')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_check_all_unassigned_interface(self):
        logger.info('check all unassigned interface...')
        flag = False
        output1 = interfaceObj.get_interface_status(name = 'X1')
        logger.info(output1)
        output2 = interfaceObj.get_interface_status(name = 'X2')
        logger.info(output2)
        output3 = interfaceObj.get_interface_status(name = 'X3')
        logger.info(output3)
        output4 = interfaceObj.get_interface_status(name = 'X4')
        logger.info(output4)
        output5 = interfaceObj.get_interface_status(name = 'X5')
        logger.info(output5)
        if output1['interfaces'][0]['ipv4']['ip_assignment']['zone'] == 'WAN' and \
            output2['interfaces'][0]['ipv4']['ip_assignment']['zone'] == 'WAN' and \
            output3['interfaces'][0]['ipv4']['ip_assignment']['zone'] == 'WAN' and \
            output4['interfaces'][0]['ipv4']['ip_assignment']['zone'] == 'WAN' and \
            output5['interfaces'][0]['ipv4']['ip_assignment']['zone'] == 'WAN':
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check all unassigned interface failed")


class Test_02_Multiple_WAN_Phase_1_Smoke_tc_24(Test):
    uuid = "SOSAIOT-TC-57393"
    description= show_testcase_info(Parameter.TESTPLAN, '1524049', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524049')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_default_route_be_added(self):
        logger.info('check multiple wan interfaces default route be added...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name'] == 'X5 IP' :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X5 Default Gateway':
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name'] == 'X4 IP' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X4 Default Gateway':
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name'] == 'X3 IP' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3 Default Gateway':
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name'] == 'X2 IP' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Default Gateway':
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name'] == 'X1 IP' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X1 Default Gateway':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check multiple wan interfaces default route be added failed")

    def test_02_add_vlan_interface(self):
        logger.info('add vlan interface ...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.add_interface(**x3_vlan)
        output = interfaceObj.get_vlan_interface_status(name = 'X3', vlan_id = '66')
        logger.info(output)
        if output['interfaces'][0]['ipv4']['vlan'] == 66:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add vlan interface X3 failed")

    def test_03_check_vlan_interface_route_policy(self):
        logger.info('check vlan interface route policy...')
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if output['route_policies'][i]['ipv4']['interface'] == 'X3:V66' :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3:V66 Default Gateway':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check vlan interface route policy failed")


class Test_03_Multiple_WAN_Phase_1_Smoke_tc_25(Test):
    uuid = "SOSAIOT-TC-57394"
    description= show_testcase_info(Parameter.TESTPLAN, '1524050', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524050')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_default_route_subnet_be_added(self):
        logger.info('check multiple wan interfaces default route subnet be added...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if output['route_policies'][i]['ipv4']['interface']== 'X5' :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X5 Subnet':
                flag &= True
            if output['route_policies'][i]['ipv4']['interface']== 'X4' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X4 Subnet':
                flag &= True
            if output['route_policies'][i]['ipv4']['interface']== 'X3' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3 Subnet':
                flag &= True
            if output['route_policies'][i]['ipv4']['interface']== 'X2':
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Subnet':
                flag &= True
            if output['route_policies'][i]['ipv4']['interface']== 'X1' :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X1 Subnet':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check multiple wan interfaces default route subnet be added failed")

    def test_02_check_vlan_interface_route_policy_subnet(self):
        logger.info('check vlan interface route policy subnet...')
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if output['route_policies'][i]['ipv4']['interface'] == 'X3:V66' :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3:V66 Subnet':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check vlan interface route policy subnet failed")


class Test_04_Multiple_WAN_Phase_1_Smoke_tc_26(Test):
    uuid = "SOSAIOT-TC-57395"
    description= show_testcase_info(Parameter.TESTPLAN, '1524051', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524051')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_default_route_any_be_added(self):
        logger.info('check multiple wan interfaces default route any be added...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X5 IP' :
                flag = True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X4 IP' :
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X3 IP' :
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X2 IP' :
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X1 IP' :
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check multiple wan interfaces default route any be added failed")


class Test_05_Multiple_WAN_Phase_1_Smoke_tc_27(Test):
    uuid = "SOSAIOT-TC-57396"
    description= show_testcase_info(Parameter.TESTPLAN, '1524052', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_primary_wan_default_route_X1(self):
        logger.info('check primary wan default route X1....')
        flag = False
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X1', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X1 failed")

    def test_02_change_primary_wan_to_X2(self):
        logger.info('change primary wan to X2...')
        flag = False
        lb = tc27_json
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X2", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: change primary wan to X2 failed")

    @repeat_method(3)
    def test_03_check_primary_wan_default_route_X2(self):
        logger.info('check primary wan default route X2....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X2', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X2 failed")

    def test_04_change_primary_wan_to_X3(self):
        logger.info('change primary wan to X3...')
        flag = False
        tc27_json['failover_lb']['group'][0]['interface'][0]['name'] = 'X3'
        lb = tc27_json
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X3", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: change primary wan to X3 failed")

    @repeat_method(3)
    def test_05_check_primary_wan_default_route_X3(self):
        logger.info('check primary wan default route X3....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X3', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X3 failed")

    def test_06_change_primary_wan_to_X4(self):
        logger.info('change primary wan to X4...')
        flag = False
        lb = tc27_json['failover_lb']['group'][0]['interface'][0]['name'] = 'X4'
        lb = tc27_json
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X4", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: change primary wan to X4 failed")

    @repeat_method(3)
    def test_07_check_primary_wan_default_route_X4(self):
        logger.info('check primary wan default route X4....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X4', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X4 failed")

    def test_08_change_primary_wan_to_X5(self):
        logger.info('change primary wan to X5...')
        flag = False
        lb = lb = tc27_json['failover_lb']['group'][0]['interface'][0]['name'] = 'X5'
        lb = tc27_json
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X5", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: change primary wan to X5 failed")

    @repeat_method(3)
    def test_09_check_primary_wan_default_route_X5(self):
        logger.info('check primary wan default route X5....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X5', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X5 failed")

    def test_10_change_primary_wan_to_vlan_interface(self):
        logger.info('change primary wan to vlan interface...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X3:V66",
                                "rank": 1
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X3:V66", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: change primary wan to vlan interface failed")

    @repeat_method(3)
    def test_11_check_primary_wan_default_route_vlan_interface(self):
        logger.info('check primary wan default route vlan interface ....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X3:V66', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route vlan interface failed")


class Test_06_Multiple_WAN_Phase_1_Smoke_tc_28(Test):
    uuid = "SOSAIOT-TC-57397"
    description= show_testcase_info(Parameter.TESTPLAN, '1524053', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524053')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_X1_X2_to_load_balance_group(self):
        logger.info('add X1 X2 to load balance group...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X2", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: add X1 X2 to load balance group failed")

    @repeat_method(3)
    def test_02_check_primary_wan_default_route_X1(self):
        logger.info('check primary wan default route X1 ....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X1', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X1 failed")

    @repeat_method(3)
    def test_03_disable_X1_and_check_route_policy(self):
        logger.info('disable X1 and check route policy...')
        flag = False
        interfaceObj.disable_interface(name='X1')
        sleep(30)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X2', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: disable X1 and check route policy failed")
        
    def test_04_enable_X1_and_add_X2_X3_to_load_balance_group(self):
        logger.info('enable X1 and add X2 X3 to load balance group...')
        flag = False
        interfaceObj.enable_interface(name='X1')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X2",
                                "rank": 1
                            },
                            {
                                "name": "X3",
                                "rank": 2
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X3", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable X1 and add X2 X3 to load balance group failed")

    @repeat_method(3)
    def test_05_check_primary_wan_default_route_X2(self):
        logger.info('check primary wan default route X2 ....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X2', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route X2 failed")

    @repeat_method(3)
    def test_06_disable_X2_and_check_route_policy(self):
        logger.info('disable X2 and check route policy...')
        flag = False
        interfaceObj.disable_interface(name='X2')
        sleep(30)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X3', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: disable X2 and check route policy failed")

    def test_07_enable_X2_and_add_vlan_X4_to_load_balance_group(self):
        logger.info('enable X2 and add vlan X4 to load balance group...')
        flag = False
        interfaceObj.enable_interface(name='X2')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X3:V66",
                                "rank": 1
                            },
                            {
                                "name": "X4",
                                "rank": 2
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X4", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable X2 and add vlan X4 to load balance group failed")

    @repeat_method(3)
    def test_08_check_primary_wan_default_route_vlan(self):
        logger.info('check primary wan default route vlan ....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X3:V66', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route vlan failed")

    @repeat_method(3)
    def test_09_disable_vlan_and_check_route_policy(self):
        logger.info('disable vlan and check route policy...')
        flag = False
        interfaceObj.disable_interface(name='X3')
        sleep(30)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X4', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: disable X2 and check route policy failed")

    def test_10_enable_X3_and_add_X5_vlan_to_load_balance_group(self):
        logger.info('enable X3 and add X5 vlan to load balance group...')
        flag = False
        interfaceObj.enable_interface(name='X3')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X5",
                                "rank": 1
                            },
                            {
                                "name": "X3:V66",
                                "rank": 2
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X3:V66", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable X2 and add vlan X4 to load balance group failed")
        
    @repeat_method(3)
    def test_11_check_primary_wan_default_route_X5(self):
        logger.info('check primary wan default route X5....')
        flag = False
        sleep(10)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X5', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check primary wan default route vlan failed")

    @repeat_method(3)
    def test_12_disable_X5_and_check_route_policy(self):
        logger.info('disable X5 and check route policy...')
        flag = False
        interfaceObj.disable_interface(name='X5')
        sleep(30)
        output = routeObj.show_route_policy_system(version = 'ipv4')
        logger.info(output)
  
        if re.search(r'destination\':\s\'0.0.0.0/0\'.*\'interface\':\s\'X3:V66', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: disable X2 and check route policy failed")


class Test_07_Multiple_WAN_Phase_1_Smoke_tc_29(Test):
    uuid = "SOSAIOT-TC-57398"
    description= show_testcase_info(Parameter.TESTPLAN, '1524054', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524054')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_X5_and_restore_load_balance_group(self):
        logger.info('enable X5 and restore load balance group...')
        flag = False
        interfaceObj.enable_interface(name='X5')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable X5 and restore load balance group failed")

    def test_02_check_X2_default_route_policy(self):
        logger.info('check X2 default route policy...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X2 IP' :
                flag = True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Default Gateway':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check X2 default route policy failed")

    def test_03_unassign_X2_interface_and_check_route_policy(self):
        logger.info('unassign X2 interface and check route policy...')
        interfaceObj.unassign_interface(interface = 'X2')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))

        if not re.search(r"X2 IP", str(output), re.S|re.I) and not \
            re.search(r"X2 Default Gateway", str(output), re.S|re.I):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: unassign X2 interface and check route policy failed")

    def test_04_reassign_X2_interface_and_check_route_policy(self):
        logger.info('reassign X2 interface and check route policy...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        interfaceObj.config_interface(**x2)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X2 IP' :
                flag = True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Default Gateway':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check X2 default route policy failed")

    def test_05_check_vlan_route_policy(self):
        logger.info('check vlan interface route policy...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3:V66 Default Gateway':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check vlan interface route policy failed")

    def test_06_remove_vlan_interface_and_check_route_policy(self):
        logger.info('remove vlan interface and check route policy...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.del_interface(**x3_vlan)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
        if not re.search(r"X3:V66 Default Gateway", str(output), re.S|re.I):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: remove vlan interface and check route policy failed")

    def test_07_change_X4_interface_zone_and_check_route_policy(self):
        logger.info('change X4 interface zone and check route policy...')
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X4_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        interfaceObj.config_interface(**x4)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
 
        for i in range(len(output['route_policies'])):
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X4 Subnet':
                flag &= True
        if not re.search(r"X4 Default Gateway", str(output), re.S|re.I) and not \
            re.search(r"X4 IP", str(output), re.S|re.I):
            flag &= True
        Assertion.assert_equal(flag, True, "ERR: change X4 interface zone and check route policy failed")


class Test_08_Multiple_WAN_Phase_1_Smoke_tc_30(Test):
    uuid = "SOSAIOT-TC-57399"
    description= show_testcase_info(Parameter.TESTPLAN, '1524055', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524055')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_X2_default_route_policy(self):
        logger.info('check X2 default route policy...')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X2 IP' :
                flag = True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Subnet':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check X2 default route policy failed")

    def test_02_unassign_X2_interface_and_check_route_policy(self):
        logger.info('unassign X2 interface and check route policy...')
        interfaceObj.unassign_interface(interface = 'X2')
        flag = False
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))

        if not re.search(r"X2 IP", str(output), re.S|re.I) and not \
            re.search(r"X2 Subnet", str(output), re.S|re.I):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: unassign X2 interface and check route policy failed")

    def test_03_reassign_X2_interface_and_check_route_policy(self):
        logger.info('reassign X2 interface and check route policy...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        interfaceObj.config_interface(**x2)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'name' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['name']== 'X2 IP' :
                flag = True
            if 'any' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['any'] == True:
                flag &= True
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag &= True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X2 Subnet':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: check X2 default route policy failed")

    def test_04_add_vlan_interface_and_check_route_policy(self):
        logger.info('add vlan interface and check interface route policy...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.add_interface(**x3_vlan)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
  
        for i in range(len(output['route_policies'])):
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X3:V66 Subnet':
                flag &= True
        Assertion.assert_equal(flag, True, "ERR: add vlan interface and check interface route policyfailed")

    def test_05_remove_vlan_interface_and_check_route_policy(self):
        logger.info('remove vlan interface and check route policy...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.del_interface(**x3_vlan)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
        if not re.search(r"X3:V66 Subnet", str(output), re.S|re.I):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: remove vlan interface and check route policy failed")

    def test_06_change_X5_interface_zone_and_check_route_policy(self):
        logger.info('change X5 interface zone and check route policy...')
        x5 = {
            'if': 'X5',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X5_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        interfaceObj.config_interface(**x5)
        sleep(30)
        output = routeObj.show_route_policy(version = 'ipv4')
        logger.info(output)
        logger.info('route policy length : {}'.format(len(output['route_policies'])))
 
        for i in range(len(output['route_policies'])):
            if 'any' in output['route_policies'][i]['ipv4']['source'] and \
                output['route_policies'][i]['ipv4']['source']['any']== True :
                flag = True
            if 'name' in output['route_policies'][i]['ipv4']['destination'] and \
                output['route_policies'][i]['ipv4']['destination']['name'] == 'X5 Subnet':
                flag &= True
        if not re.search(r"X5 IP", str(output), re.S|re.I):
            flag &= True
        Assertion.assert_equal(flag, True, "ERR: change X5 interface zone and check route policy failed")


class Test_09_Multiple_WAN_Phase_1_Smoke_tc_34(Test):
    uuid = "SOSAIOT-TC-57400"
    description= show_testcase_info(Parameter.TESTPLAN, '1524056', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524056')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_lan_to_wan_auto_nat_policy(self):
        logger.info('check lan to wan auto nat policy...')
        flag = False
        output = natObj.get_nat_policy()
        logger.info(output)
        logger.info('nat policy length:{}'.format(len(output['nat_policies'])))

        if re.search(r"Auto-added X0 outbound NAT Policy for X1 WAN", str(output), re.S|re.I) and \
            re.search(r"Auto-added X0 outbound NAT Policy for X2 WAN", str(output), re.S|re.I) and \
            re.search(r"Auto-added X0 outbound NAT Policy for X3 WAN", str(output), re.S|re.I) and \
            re.search(r"Auto-added X4 outbound NAT Policy for X3 WAN", str(output), re.S|re.I) and \
            re.search(r"Auto-added X5 outbound NAT Policy for X3 WAN", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:check lan to wan auto nat policy failed")

    def test_02_change_X4_to_WAN_and_check_nat_policy(self):
        logger.info('change X4 from LAN to WAN and check nat policy...')
        flag =False
        x4 = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X4_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        interfaceObj.config_interface(**x4)
        sleep(30)
        output = natObj.get_nat_policy()
        logger.info(output)
        logger.info('nat policy length:{}'.format(len(output['nat_policies'])))

        if re.search(r"Auto-added X0 outbound NAT Policy for X4 WAN", str(output), re.S|re.I) and not \
            re.search(r"Auto-added X4 outbound NAT Policy for X3 WAN", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: change X4 from LAN to WAN and check nat policy failed")

    def test_03_add_vlan_interface_and_check_nat_policy(self):
        logger.info('add vlan interface and check nat policy...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.add_interface(**x3_vlan)
        sleep(30)
        output = natObj.get_nat_policy()
        logger.info(output)
        logger.info('nat policy length:{}'.format(len(output['nat_policies'])))

        if re.search(r"Auto-added X0 outbound NAT Policy for X3:V66 WAN", str(output), re.S|re.I) and \
            re.search(r"Auto-added X5 outbound NAT Policy for X3:V66 WAN", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: add vlan interface and check nat policy failed")


class Test_10_Multiple_WAN_Phase_1_Smoke_tc_54(Test):
    uuid = "SOSAIOT-TC-57401"
    description= show_testcase_info(Parameter.TESTPLAN, '1524057', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524057')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_wan_and_vlan_wan_to_load_balance_group(self):
        logger.info('add wan and vlan wan to load balance group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {
                                "name": "X3",
                                "rank": 3
                            },
                            {
                                "name": "X4",
                                "rank": 4
                            },
                            {
                                "name": "X3:V66",
                                "rank": 5
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X2", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X4", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3:V66", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable X5 and restore load balance group failed")

    @repeat_method(3)
    def test_02_check_load_balance_group_statistics(self):
        logger.info('check load balance group statistics...')
        flag = False
        sleep(30)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3", str(output[2]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[2]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[2]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X4", str(output[3]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[3]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[3]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3:V66", str(output[4]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[4]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[4]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check load balance group statistics failed")


class Test_11_Multiple_WAN_Phase_1_Smoke_tc_8(Test):
    uuid = "SOSAIOT-TC-57402"
    description= show_testcase_info(Parameter.TESTPLAN, '1524058', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524058')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_wan_and_vlan_wan_to_ipv6_load_balance_group(self):
        logger.info('add wan and vlan wan to ipv6 load balance group...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group IPv6",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {
                                "name": "X3",
                                "rank": 3
                            },
                            {
                                "name": "X4",
                                "rank": 4
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X2", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X4", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3:V66", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable X5 and restore load balance group failed")

    def test_02_unassign_all_WAN_interfaces_except_X4(self):
        logger.info('unassign all WAN interfaces except X4')
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': 66,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        rc = interfaceObj.del_interface(**x3_vlan)
        sleep(5)
        rc &= interfaceObj.enforce_unassign_interface(interface = 'X1')
        sleep(5)
        rc &= interfaceObj.enforce_unassign_interface(interface = 'X2')
        sleep(5)
        rc &=interfaceObj.enforce_unassign_interface(interface = 'X3')
        Assertion.assert_equal(rc, True, "ERR: unassign all WAN interfaces except X4 failed")

    def test_03_check_unassign_last_WAN_interface(self):
        logger.info('check unassign last WAN interface...')
        flag = False
        output = interfaceObj.enforce_unassign_interface(msg = True, interface = 'X4')
        logger.info(output)
        if re.search(r"One WAN interface must be selected for Failover & LB Group", str(output), re.S|re.I): 
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check unassign last WAN interface failed")


class Test_12_Multiple_WAN_Phase_1_Smoke_tc_80(Test):
    uuid = "SOSAIOT-TC-57403"
    description= show_testcase_info(Parameter.TESTPLAN, '1524059', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524059')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x1_dhcp(self):
        logger.info("config x1 interface dhcp ... ")
        sleep(60)
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ping': True
        }
        rc = interfaceObj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 dhcp failed")

    def test_02_config_interface_x2_dhcp(self):
        logger.info("config x2 interface dhcp ... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ping': True
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 dhcp failed")
    
    def test_03_config_interface_x3_dhcp(self):
        logger.info("config x3 interface dhcp ... ")
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ping': True
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 dhcp failed")

    def test_04_config_interface_x4_dhcp(self):
        logger.info("config x4 interface dhcp ... ")
        x4 = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
            'mgmt_ping': True
        }
        rc = interfaceObj.config_interface(**x4)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 dhcp failed")

    def test_05_add_http_address_object(self):
        logger.info('add http address object...')
        ao_param ={
            "object_type": "host",
            "name": "http_server",
            "zone": "LAN",
            "value": HTTP_Server,
        }
        rc = addrObj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: add http address object failed")

    def test_06_add_wan_to_ipv6_load_balance_group(self):
        logger.info('add wan and vlan wan to ipv6 load balance group...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {
                                "name": "X3",
                                "rank": 3
                            },
                            {
                                "name": "X4",
                                "rank": 4
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X2", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3", str(output), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X4", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable X5 and restore load balance group failed")

    def test_07_add_static_route_for_X2(self):
        logger.info('add static route for X2...')
        route ={
            "route_policies": [
                {
                    "ipv4": {
                        "name": "tc80",
                        "comment": "",
                        "interface": "X2",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X2 Default Gateway"
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "http_server"
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route)
        Assertion.assert_equal(rc, True, "ERR: add static route for X2 failed")

    @repeat_method(3)
    def test_08_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(X2_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    def test_09_delete_static_route(self):
        logger.info('delete static route...')
        rc = routeObj.del_route_policy_by_name(name = 'tc80')
        Assertion.assert_equal(rc, True, "ERR: delete static route fail")

    @repeat_method(3)
    def test_10_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(X1_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    @repeat_method(3)
    def test_11_disable_X1_and_verify_traffic(self):
        logger.info('disable X1 and verify traffic...')
        flag = False
        interfaceObj.disable_interface(name='X1')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(X2_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X1 and verify traffic fail")

    @repeat_method(3)
    def test_12_disable_X2_and_verify_traffic(self):
        logger.info('disable X2 and verify traffic...')
        flag = False
        interfaceObj.disable_interface(name='X2')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(X3_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X2 and verify traffic fail")

    @repeat_method(3)
    def test_13_disable_X3_and_verify_traffic(self):
        logger.info('disable X3 and verify traffic...')
        flag = False
        interfaceObj.disable_interface(name='X3')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(X4_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X3 and verify traffic fail")

    def test_14_enable_X2_X3_interfaces(self):
        logger.info('enable X2 X3 interfaces...')
        rc = interfaceObj.enable_interface(name='X2')
        sleep(5)
        rc &= interfaceObj.enable_interface(name='X3')
        Assertion.assert_equal(rc, True, "ERR: enable X2 X3 interfaces fail")


class Test_13_Multiple_WAN_Phase_1_Smoke_tc_84(Test):
    uuid = "SOSAIOT-TC-57404"
    description= show_testcase_info(Parameter.TESTPLAN, '1524060', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524060')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X2_X3_to_pppoe(self):
        logger.info('change X2 X3 to pppoe...')
        sleep(60)
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'automation',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_dynamic':True,
            'pppoe_inactivity':0,
            'pppoe_lcp_echo_packets':False,
            'pppoe_reconnect':5,
            'pppoe_schedule':'always_on',
            'mgmt_ping': True,
            'mgmt_snmp': True,

        }
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_user': 'automation',
            'pppoe_servicename': '',
            'pppoe_passwd': 'password',
            'pppoe_dynamic':True,
            'pppoe_inactivity':0,
            'pppoe_lcp_echo_packets':False,
            'pppoe_reconnect':5,
            'pppoe_schedule':'always_on',
            'mgmt_ping': True,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        rc &= interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR:change x2 x3 to pppoe failed")

    @repeat_method(3)
    def test_02_verify_traffic_pppoe(self):
        logger.info('verify traffic pppoe...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"X2\*, Generated.*VPN policy: WAN GroupVPN.*Ether Type: PPPOE-SES", str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic pppoe fail")

    @repeat_method(3)
    def test_03_disable_X2_and_verify_traffic_pppoe(self):
        logger.info('disable X2 and verify traffic pppoe...')
        flag = False
        interfaceObj.disable_interface(name='X2')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"X3\*, Generated.*VPN policy: WAN GroupVPN.*Ether Type: PPPOE-SES", str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X2 and verify traffic pppoe fail")

    @repeat_method(3)
    def test_04_disable_X3_and_verify_traffic_pppoe(self):
        logger.info('disable X3 and verify traffic pppoe...')
        flag = False
        interfaceObj.disable_interface(name='X3')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
              re.search(r"Src=\[{}\], Dst=\[{}\]".format(X4_IP_DHCP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X3 and verify traffic pppoe fail")

    @repeat_method(3)
    def test_05_enable_X3_and_verify_traffic_pppoe(self):
        logger.info('enable X3 and verify traffic pppoe...')
        flag = False
        interfaceObj.enable_interface(name='X3')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"X3\*, Generated.*VPN policy: WAN GroupVPN.*Ether Type: PPPOE-SES", str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: enable X3 and verify traffic pppoe fail")
   
    @repeat_method(3)
    def test_06_enable_X2_and_verify_traffic_pppoe(self):
        logger.info('enable X2 and verify traffic pppoe...')
        flag = False
        interfaceObj.enable_interface(name='X2')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"X2\*, Generated.*VPN policy: WAN GroupVPN.*Ether Type: PPPOE-SES", str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: enable X2 and verify traffic pppoe fail")


class Test_14_Multiple_WAN_Phase_1_Smoke_tc_88(Test):
    uuid = "SOSAIOT-TC-57405"
    description= show_testcase_info(Parameter.TESTPLAN, '1524061', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524061')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        sleep(60)
        interfaceObj.enable_interface(name='X1')
        sleep(10)
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")
    
    def test_03_config_interface_x3(self):
        logger.info("config x3 interface... ")
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_04_config_interface_x4(self):
        logger.info("config x4 interface... ")
        x4 = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X4_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x4)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 failed")

    def test_05_config_LB_group_to_round_robin(self):
        logger.info('config LB group to round robin...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X3",
                                "rank": 3,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X4",
                                "rank": 4,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: config LB group to round robin failed")

    def test_06_verify_traffic_round_robin_X1(self):
        logger.info('verify traffic round robin...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin fail")

    def test_07_verify_traffic_round_robin_X2(self):
        logger.info('verify traffic round robin...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X2_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin fail")

    def test_08_verify_traffic_round_robin_X3(self):
        logger.info('verify traffic round robin...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X3_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin fail")

    def test_09_verify_traffic_round_robin_X4(self):
        logger.info('verify traffic round robin...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X4_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin fail")

    @repeat_method(3)
    def test_10_disable_X1_and_verify_traffic_round_robin(self):
        logger.info('disable X1 and verify traffic round robin...')
        flag = False
        interfaceObj.disable_interface(name='X1')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X2_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X1 and verify traffic round robin fail")

    def test_11_add_static_route_for_X4(self):
        logger.info('add static route for X4...')
        route ={
            "route_policies": [
                {
                    "ipv4": {
                        "name": "tc88",
                        "comment": "",
                        "interface": "X4",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X4 Default Gateway"
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "http_server"
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route)
        Assertion.assert_equal(rc, True, "ERR: add static route for X4 failed")

    def test_12_verify_traffic_round_robin(self):
        logger.info('verify traffic round robin trough static route...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X4_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin trough static route fail")

    def test_13_delete_static_route(self):
        logger.info('delete static route...')
        rc = routeObj.del_route_policy_by_name(name = 'tc88')
        Assertion.assert_equal(rc, True, "ERR: delete static route fail")

    def test_14_verify_traffic_round_robin(self):
        logger.info('verify traffic round robin trough static route...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X3_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic round robin trough static route fail")


class Test_15_Multiple_WAN_Phase_1_Smoke_tc_125(Test):
    uuid = "SOSAIOT-TC-57390"
    description= show_testcase_info(Parameter.TESTPLAN, '1524046', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
 
    def test_01_enable_X1_and_config_X5(self):
        logger.info('enable X1 and config X5...')
        interfaceObj.enable_interface(name='X1')
        sleep(10)
        x5 = {
            'if': 'X5',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X5_GW,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interfaceObj.config_interface(**x5)
        Assertion.assert_equal(rc, True, "ERR: enable X1 and config X5 failed")

    def test_02_change_wlb_to_basic(self):
        logger.info('change wlb to basic...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {
                                "name": "X3",
                                "rank": 3
                            },
                            {
                                "name": "X4",
                                "rank": 4
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: change wlb to basic failed")

    def test_03_config_vlan_wan_to_X2(self):
        logger.info('config vlan wan to X2...')
        x2_vlan = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag':22,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.13.13.13',
            'mgmt_ping': True,
        }
        interfaceObj.add_interface(**x2_vlan)
        output = interfaceObj.get_vlan_interface_status(name = 'X2', vlan_id = '22')
        logger.info(output)
        if output['interfaces'][0]['ipv4']['vlan'] == 22:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config vlan wan to X2 failed")

    @repeat_method(3)
    def test_04_verify_traffic_basic(self):
        logger.info('verify traffic basic...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic basic fail")

    def test_05_disable_all_wlb_interfaces(self):
        logger.info('disable all wlb interfaces...')
        rc = interfaceObj.disable_interface(name='X1')
        sleep(10)
        rc &= interfaceObj.disable_interface(name='X2')
        sleep(10)
        rc &= interfaceObj.disable_interface(name='X3') 
        sleep(10)
        rc &= interfaceObj.disable_interface(name='X4')
        Assertion.assert_equal(rc, True, "ERR: disable all wlb interfaces fail")

    @repeat_method(3)
    def test_06_verify_server_can_not_be_connected(self):
        logger.info('verify server can not be connected...')
        flag = False
        output = local_host.send_command('ping -c 5 {}'.format(HTTP_Server))
        if re.search(r"100% packet loss", str(output), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify server can not be connected fail")
    
    def test_07_enable_all_wlb_interfaces(self):
        logger.info('enable all wlb interfaces...')
        rc = interfaceObj.enable_interface(name='X1')
        sleep(10)
        rc &= interfaceObj.enable_interface(name='X2')
        sleep(10)
        rc &= interfaceObj.enable_interface(name='X3') 
        sleep(10)
        rc &= interfaceObj.enable_interface(name='X4')
        Assertion.assert_equal(rc, True, "ERR:enable all wlb interfaces fail")

    @repeat_method(3)
    def test_08_verify_traffic_basic(self):
        logger.info('verify traffic basic...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic basic fail")


class Test_16_Multiple_WAN_Phase_1_Smoke_tc_126(Test):
    uuid = "SOSAIOT-TC-57391"
    description= show_testcase_info(Parameter.TESTPLAN, '1524047', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524047')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_static_route_for_X5(self):
        logger.info('add static route for X5...')
        route ={
            "route_policies": [
                {
                    "ipv4": {
                        "name": "tc126",
                        "comment": "",
                        "interface": "X5",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": "X5 Default Gateway"
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": "http_server"
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route)
        Assertion.assert_equal(rc, True, "ERR: add static route for X5 failed")

    @repeat_method(3)
    def test_02_verify_traffic_through_x5(self):
        logger.info('verify traffic through x5...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X5_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic through x5 fail")

    @repeat_method(3)
    def test_03_disable_X5_and_verify_traffic_through_x1(self):
        logger.info('disable X5 and verify traffic through x1...')
        flag = False
        interfaceObj.disable_interface(name='X5')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X5 and verify traffic through x1 fail")

    @repeat_method(3)
    def test_04_disable_X1_and_verify_traffic_through_x2(self):
        logger.info('disable X1 and verify traffic through x2...')
        flag = False
        interfaceObj.disable_interface(name='X1')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X2_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X5 and verify traffic through x1 fail")

    @repeat_method(3)
    def test_05_enable_X5_and_verify_traffic_through_x5(self):
        logger.info('disable X5 and verify traffic through x5...')
        flag = False
        interfaceObj.enable_interface(name='X5')
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(HTTP_Server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation, this is http server", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X5_IP, HTTP_Server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: disable X5 and verify traffic through x1 fail")


class Test_17_Multiple_WAN_Phase_1_Smoke_tc_131(Test):
    uuid = "SOSAIOT-TC-57392"
    description= show_testcase_info(Parameter.TESTPLAN, '1524048', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1524048')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_static_route(self):
        logger.info('delete static route...')
        sleep(60)
        rc = routeObj.del_route_policy_by_name(name='tc126')
        Assertion.assert_equal(rc, True, "ERR: delete static route failed")

    def test_02_config_vlan_wan_to_X2(self):
        logger.info('config vlan wan to X2...')
        x2_vlan = {
            'if': 'X2',
            'type': 'vlan',
            'vlan_tag':33,
            'zone': 'WAN',
            'mode': 'static',
            'ip': '14.14.14.14',
            'mgmt_ping': True,
        }
        interfaceObj.add_interface(**x2_vlan)
        output = interfaceObj.get_vlan_interface_status(name = 'X2', vlan_id = '33')
        logger.info(output)
        if output['interfaces'][0]['ipv4']['vlan'] == 33:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config vlan wan to X2 failed")

    def test_03_enable_interface_X1_back(self):
        logger.info('enable interface X1 back')
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: enable interface X1 failed")

    def test_04_config_wlb_probes(self):
        logger.info('config wlb probes...')
        lb = {
            'enable': True,
            'probes': True,
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": True,
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
                            },
                            {
                                "name": "X2",
                                "rank": 2
                            },
                            {
                                "name": "X3",
                                "rank": 3
                            },
                            {
                                "name": "X4",
                                "rank": 4
                            },
                            {
                                "name": "X2:V22",
                                "rank": 5
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc &= failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: config wlb probes failed")
    
    def test_05_check_wlb_probes(self):
        logger.info('check wlb probes...')
        sleep(30)
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X3", str(output[2]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[2]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[2]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X4", str(output[3]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[3]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[3]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2:V22", str(output[4]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[4]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[4]), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")
