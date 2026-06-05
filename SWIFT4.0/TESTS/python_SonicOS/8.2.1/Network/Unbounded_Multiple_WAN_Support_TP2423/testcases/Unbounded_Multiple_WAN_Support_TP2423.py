from definition.init_param import *


class Test_01_Unbounded_Multiple_WAN_Support_TP2423_tc_1(Test):
    uuid = "SOSAIOT-TC-57406"
    description= show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_uncheck_enable_load_balance(self):
        logger.info('uncheck enable load balance...')
        lb = {
            'enable': False
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: uncheck enable load balance failed")

    def test_02_check_load_balance(self):
        logger.info('check load balance...')
        flag = False
        output = failoverlbObj.check_failover_setting()
        logger.info(output)
        if output['failover_lb']['enable'] == False:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check load balance failed")


class Test_02_Unbounded_Multiple_WAN_Support_TP2423_tc_5(Test):
    uuid = "SOSAIOT-TC-57413"
    description= show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_enable_load_balance(self):
        logger.info('uncheck enable load balance...')
        lb = {
            'enable': True
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check enable load balance failed")

    def test_02_add_interfaces_to_default_lb_group(self):
        logger.info('add interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "X4",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

    def test_03_check_failover_groups_members_status(self):
        logger.info('check failover group status...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r'.*member_name\'\:\s\'X4', str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check failover group members status failed")


class Test_03_Unbounded_Multiple_WAN_Support_TP2423_tc_6(Test):
    uuid = "SOSAIOT-TC-57414"
    description= show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb groups...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "X4",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

    def test_02_check_failover_groups_members_status(self):
        logger.info('check failover group status...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if not re.search(r'.*member_name.*X3', str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check failover group members status failed")

    def test_03_reset_failover_groups(self):
        logger.info('reset failover groups...')
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
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: reset interfaces to default lb group failed")


class Test_04_Unbounded_Multiple_WAN_Support_TP2423_tc_9(Test):
    uuid = "SOSAIOT-TC-57415"
    description= show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_interfaces_to_default_lb_group(self):
        logger.info('add interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

    def test_02_edit_default_lb_group_member_x1(self):
        logger.info('edit default lb group member x1...')
        lb = {
            'interface': 'X1',
            'rank':1,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x1 failed")

    @repeat_method(2)
    def test_03_edit_default_lb_group_member_x2(self):
        logger.info('edit default lb group member x2...')
        lb = {
            'interface': 'X2',
            'rank':2,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x2 failed")

    def test_04_edit_default_lb_group_member_x3(self):
        logger.info('edit default lb group member x3...')
        lb = {
            'interface': 'X3',
            'rank':3,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x3 failed")

    @repeat_method(2)
    def test_05_edit_default_lb_group_member_x4(self):
        logger.info('edit default lb group member x4...')
        lb = {
            'interface': 'X4',
            'rank':4,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x4 failed")

    @repeat_method(2)
    def test_06_check_packets_ping(self):
        logger.info('check packet x1 ping...')
        flag = False
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('ping {} -c 5'.format(IP_Server))
        sleep(1)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X2_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X3_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X4_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets ping failed")

    def test_07_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


class Test_05_Unbounded_Multiple_WAN_Support_TP2423_tc_12(Test):
    uuid = "SOSAIOT-TC-57407"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_interfaces_to_default_lb_group(self):
        logger.info('add interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "ratio",
                        "final_backup": "X4",
                        "address_binding": False,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1"
                            },
                            {
                                "name": "X2"
                            },
                            {
                                "name": "X3"
                            },
                            {}
                        ],
                        "percent": [
                            {
                                "interface": "X1",
                                "percent": 40
                            },
                            {
                                "interface": "X2",
                                "percent": 30
                            },
                            {
                                "interface": "X3",
                                "percent": 30
                            }
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

    def test_02_edit_default_lb_group_member_x1(self):
        logger.info('edit default lb group member x1...')
        lb = {
            'type': 'ratio',
            'interface': 'X1',
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x1 failed")

    def test_03_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


class Test_06_Unbounded_Multiple_WAN_Support_TP2423_tc_14(Test):
    uuid = "SOSAIOT-TC-57408"
    description= show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_interface_to_default_lb_group(self):
        logger.info('add interface to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "X5",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")

    def test_02_edit_default_lb_group_member_x1(self):
        logger.info('edit default lb group member x1...')
        lb = {
            'type': 'basic',
            'interface': 'X1',
            'rank':1,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x1 failed")

    def test_03_edit_default_lb_group_member_x2(self):
        logger.info('edit default lb group member x2...')
        lb = {
            'type': 'basic',
            'interface': 'X2',
            'rank':2,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x2 failed")

    def test_04_edit_default_lb_group_member_x3(self):
        logger.info('edit default lb group member x3...')
        lb = {
            'type': 'basic',
            'interface': 'X3',
            'rank':3,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x3 failed")

    def test_05_edit_default_lb_group_member_x4(self):
        logger.info('edit default lb group member x4...')
        lb = {
            'type': 'basic',
            'interface': 'X4',
            'rank':4,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x4 failed")

    def test_06_edit_default_lb_group_member_x5(self):
        logger.info('edit default lb group member x5...')
        lb = {
            'type': 'basic',
            'interface': 'X5',
            'rank':5,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x5 failed")

    @repeat_method(2)
    def test_07_check_packets_http(self):
        logger.info('check packet x1 http...')
        flag = False
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(1)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    def test_08_shutdown_interfaces(self):
        logger.info('shutdown interfaces...')
        rc  = interface_obj.disable_interface(name = 'X1')
        rc &= interface_obj.disable_interface(name = 'X2')
        rc &= interface_obj.disable_interface(name = 'X3')
        rc &= interface_obj.disable_interface(name = 'X4')
        Assertion.assert_equal(rc, True, "ERR: shutdown interfaces failed")

    @repeat_method(2)
    def test_09_check_packets_http(self):
        logger.info('check packet x5 http...')
        flag = False
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(1)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X5_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    def test_10_shutdown_interfaces(self):
        logger.info('no shutdown interfaces...')
        rc  = interface_obj.enable_interface(name = 'X1')
        rc &= interface_obj.enable_interface(name = 'X2')
        rc &= interface_obj.enable_interface(name = 'X3')
        rc &= interface_obj.enable_interface(name = 'X4')
        Assertion.assert_equal(rc, True, "ERR: shutdown interfaces failed")

    def test_11_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


class Test_07_Unbounded_Multiple_WAN_Support_TP2423_tc_16(Test):
    uuid = "SOSAIOT-TC-57409"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_interface_to_default_lb_group(self):
        logger.info('add interface to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "X5",
                        "preempt": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")

    def test_02_edit_default_lb_group_member_x1(self):
        logger.info('edit default lb group member x1...')
        lb = {
            'type': 'basic',
            'interface': 'X1',
            'rank':1,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x1 failed")

    def test_03_edit_default_lb_group_member_x2(self):
        logger.info('edit default lb group member x2...')
        lb = {
            'type': 'basic',
            'interface': 'X2',
            'rank':2,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x2 failed")

    def test_04_edit_default_lb_group_member_x3(self):
        logger.info('edit default lb group member x3...')
        lb = {
            'type': 'basic',
            'interface': 'X3',
            'rank':3,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x3 failed")

    def test_05_edit_default_lb_group_member_x4(self):
        logger.info('edit default lb group member x4...')
        lb = {
            'type': 'basic',
            'interface': 'X4',
            'rank':4,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x4 failed")

    def test_06_edit_default_lb_group_member_x5(self):
        logger.info('edit default lb group member x5...')
        lb = {
            'type': 'basic',
            'interface': 'X5',
            'rank':5,
            'probe_type': 'logical',
            "probe_option": "either",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x5 failed")

    @repeat_method(2)
    def test_07_check_packets_http_x1(self):
        logger.info('check packet x1 http...')
        flag = False
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(1)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    def test_08_shutdown_interfaces(self):
        logger.info('shutdown interfaces...')
        rc  = interface_obj.disable_interface(name = 'X1')
        rc &= interface_obj.disable_interface(name = 'X2')
        rc &= interface_obj.disable_interface(name = 'X3')
        rc &= interface_obj.disable_interface(name = 'X4')
        Assertion.assert_equal(rc, True, "ERR: shutdown interfaces failed")

    @repeat_method(2)
    def test_09_check_packets_http_x5(self):
        logger.info('check packet x5 http...')
        flag = False
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(1)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X5_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    @repeat_method(2)
    def test_10_check_packets_http_x4(self):
        logger.info('check packets http x4...')
        interface_obj.enable_interface(name = 'X4')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X4_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    @repeat_method(2)
    def test_11_check_packets_http_x3(self):
        logger.info('check packets http x3...')
        interface_obj.enable_interface(name = 'X3')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X3_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    @repeat_method(2)
    def test_12_check_packets_http_x2(self):
        logger.info('check packets http x2...')
        interface_obj.enable_interface(name = 'X2')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X2_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    @repeat_method(2)
    def test_13_check_packets_http_x1(self):
        logger.info('check packets http x1...')
        interface_obj.enable_interface(name = 'X1')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('curl http://{}'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets http failed")

    def test_14_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


class Test_08_Unbounded_Multiple_WAN_Support_TP2423_tc_30(Test):
    uuid = "SOSAIOT-TC-57410"
    description= show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
     
    def test_01_add_interfaces_to_default_lb_group(self):
        logger.info('add interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

    def test_02_edit_default_lb_group_member_x1(self):
        logger.info('edit default lb group member x1...')
        lb = {
            'interface': 'X1',
            'rank':1,
            'probe_type': 'logical',
            "probe_option": "both",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x1 failed")

    @repeat_method(2)
    def test_03_edit_default_lb_group_member_x2(self):
        logger.info('edit default lb group member x2...')
        lb = {
            'interface': 'X2',
            'rank':2,
            'probe_type': 'logical',
            "probe_option": "both",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x2 failed")

    def test_04_edit_default_lb_group_member_x3(self):
        logger.info('edit default lb group member x3...')
        lb = {
            'interface': 'X3',
            'rank':3,
            'probe_type': 'logical',
            "probe_option": "both",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x3 failed")

    @repeat_method(2)
    def test_05_edit_default_lb_group_member_x4(self):
        logger.info('edit default lb group member x4...')
        lb = {
            'interface': 'X4',
            'rank':4,
            'probe_type': 'logical',
            "probe_option": "both",
            'main_protocol':'tcp',
            'main_value': 80,
            'main_host': Host_Responser_SNWL,
            'alter_protocol':'tcp',
            'alter_value': 80,
            'alter_host': IP_Responser_SNWL,
            'default_value': IP_Server
        }
        rc = failoverlbObj.config_failover_groups(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit default lb group member x4 failed")

    def test_06_shutdown_interfaces(self):
        logger.info('shutdown interfaces...')
        rc  = interface_obj.disable_interface(name = 'X1')
        rc &= interface_obj.disable_interface(name = 'X2')
        rc &= interface_obj.disable_interface(name = 'X3')
        Assertion.assert_equal(rc, True, "ERR: shutdown interfaces failed")

    @repeat_method(2)
    def test_07_check_packets_ping_x4(self):
        logger.info('check packets ping x4...')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('ping {} -c 5'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X4_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets ping failed")

    def test_08_no_shutdown_interfaces(self):
        logger.info('no shutdown interfaces...')
        rc  = interface_obj.enable_interface(name = 'X1')
        rc &= interface_obj.enable_interface(name = 'X2')
        rc &= interface_obj.enable_interface(name = 'X3')
        Assertion.assert_equal(rc, True, "ERR: shutdown interfaces failed")

    @repeat_method(2)
    def test_09_check_packets_ping(self):
        logger.info('check packets ping ...')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        local_host.send_command('ping {} -c 5'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X2_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X3_IP, IP_Server), str(output), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets ping failed")

    def test_10_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


class Test_09_Unbounded_Multiple_WAN_Support_TP2423_tc_34(Test):
    uuid = "SOSAIOT-TC-57411"
    description= show_testcase_info(Parameter.TESTPLAN, '34', description=True)['title']
    jira = 'GEN7-42400'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
     
    def test_01_add_interfaces_to_default_lb_group(self):
        logger.info('add interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
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
                                "name": "X5",
                                "rank": 5
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: add interfaces to default lb group failed")

   
    @repeat_method(2)
    def test_02_check_packets_ping(self):
        logger.info('check packets http  ...')
        flag = False
        sleep(5)
        captureObj.clear_packets()
        captureObj.start_capture()
        for i in range(0,5):
            local_host.send_command('ping {} -c 5'.format(IP_Server))
        sleep(3)
        captureObj.stop_capture()
        output = captureObj.export_captured_packets()
        logger.info(output)
        if re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X1_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X2_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X3_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X4_IP, IP_Server), str(output), re.I|re.DOTALL) and \
            re.search(r'.*Src\W+{}\W+\sDst\W+{}\W'.format(Parameter.X5_IP, IP_Server), str(output), re.I|re.DOTALL) :
            flag =True
        Assertion.assert_equal(flag, True, "ERR: check packets ping failed")

    def test_03_remove_interfaces_to_default_lb_group(self):
        logger.info('remove interfaces to default lb group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 6,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
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
        Assertion.assert_equal(rc, True, "ERR: remove interfaces to default lb group failed")


