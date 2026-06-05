from definition.init_param import *

class Test_01_WAN_Failover_and_Load_Balancing_TP2201_tc_1(Test):
    uuid = "SOSAIOT-TC-57416"
    description= show_testcase_info(Parameter.TESTPLAN, '1506062', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506062')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_config_LB_group_to_add_X2(self):
        logger.info('Edit the default LB group to add X2...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc&flag, True, "ERR:edit the default LB group to add X2 failed")

    def test_03_config_interface_x3(self):
        logger.info("config x3 interface... ")
        interfaceObj.unassign_interface(interface = 'X2')
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_04_config_LB_group_to_add_X3(self):
        logger.info('Edit the default LB group to add X3...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc&flag, True, "ERR:edit the default LB group to add X3 failed")

    def test_05_config_interface_x4(self):
        logger.info("config x4 interface... ")
        interfaceObj.unassign_interface(interface = 'X3')
        x4 = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x4)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 failed")

    def test_06_config_LB_group_to_add_X4(self):
        logger.info('Edit the default LB group to add X4...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc&flag, True, "ERR:edit the default LB group to add X4 failed")

    ###TZ80-PROTOTYPE not X5 interface
    # def test_07_config_interface_x5(self):
    #     logger.info("config x5 interface... ")
    #     interfaceObj.unassign_interface(interface = 'X4')
    #     x5 = {
    #         'if': 'X5',
    #         'zone': 'WAN',
    #         'mode': 'static',
    #         'ip': Parameter.X3_IP,
    #         'netmask': '255.255.255.0',
    #         'gateway': Parameter.X3_GW,
    #         'mgmt_snmp': True,
    #     }
    #     rc = interfaceObj.config_interface(**x5)
    #     Assertion.assert_equal(rc, True, "ERR: Config X5 IPv4 failed")

    # def test_08_config_LB_group_to_add_X5(self):
    #     logger.info('Edit the default LB group to add X5...')
    #     flag = False
    #     lb = {
    #         "failover_lb": {
    #             "group": [
    #                 {
    #                     "name": " Default LB Group",
    #                     "type": "basic",
    #                     "final_backup": "",
    #                     "preempt": False,
    #                     "probing": {
    #                         "health_check": 5,
    #                         "missed_intervals": 3,
    #                         "successful_intervals": 3,
    #                         "global_responder": False
    #                     },
    #                     "interface": [
    #                         {
    #                             "name": "X1",
    #                             "rank": 1,
    #                             "probe_type": "physical",
    #                             "probe_condition": "always"
    #                         },
    #                         {
    #                             "name": "X5",
    #                             "rank": 2
    #                         },
    #                         {}
    #                     ]
    #                 }
    #             ]
    #         }
    #     }
    #     rc = failoverlbObj.config_failover_groups_by_multi(**lb)
    #     output = failoverlbObj.check_failover_members_status()
    #     logger.info(output)
    #     interfaceObj.unassign_interface(interface = 'X5')
    #     if re.search(r"member_name\'\:\s\'X5", str(output), re.S|re.I):
    #         flag = True
    #     Assertion.assert_equal(rc&flag, True, "ERR:edit the default LB group to add X5 failed")

class Test_02_WAN_Failover_and_Load_Balancing_TP2201_tc_4(Test):
    uuid = "SOSAIOT-TC-57373"
    description= show_testcase_info(Parameter.TESTPLAN, '1506106', description=True)['title']
    

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506106')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_02_uncheck_enable_load_balance(self):
        logger.info('uncheck enable load balance...')
        lb = {
            'enable': False
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: uncheck enable load balance failed")

    def test_03_check_enable_load_balance(self):
        logger.info('check enable load balance...')
        lb = {
            'enable': True
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check enable load balance failed")

    def test_04_config_LB_group_to_add_X2(self):
        logger.info('Edit the default LB group to add X2...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc&flag, True, "ERR:edit the default LB group to add X2 failed")


class Test_03_WAN_Failover_and_Load_Balancing_TP2201_tc_5(Test):
    uuid = "SOSAIOT-TC-57377"
    description= show_testcase_info(Parameter.TESTPLAN, '1506110', description=True)['title']
    

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506110')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unplug_x1_interface(self):
        logger.info('unplug x1 interface...')
        systemlogObj.clear_log()
        rc = interfaceObj.disable_interface(name='X1')
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: unplug x1 interface failed")

    @repeat_method(3)
    def test_02_traffic_and_verify_log(self):
        logger.info('traffic and verify log...')
        flag = False
        sleep(30)
        cmd = 'ping -c 10 {}'.format(http_server)
        local_host.send_command(cmd)
        sleep(60)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r"Interface X1 Link Is Down", str(output), re.S|re.I) and \
            re.search(r"WLB Failover in progress", str(output), re.S|re.I) and \
            re.search(r"WLB Resource failed", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:traffic and verify log failed")

    def test_03_verify_routing_info_through_tsr(self):
        logger.info('verify routing info through tsr...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : Routing')
        if re.search(r"Any\s+0.0.0.0\/0\s+Any\s+N\/A\s+Any\s+{}".format(Parameter.PC_GW2_ETH2), str(output), re.S|re.I) :
            flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify routing info through tsr failed")

    def test_04_plug_x1_interface(self):
        logger.info('plug x1 interface...')
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")


class Test_04_WAN_Failover_and_Load_Balancing_TP2201_tc_6(Test):
    uuid = "SOSAIOT-TC-57380"
    description= show_testcase_info(Parameter.TESTPLAN, '1506114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506114')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_unplug_x1_interface(self):
        logger.info('unplug x1 interface...')
        systemlogObj.clear_log()
        sleep(10)
        rc = interfaceObj.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: unplug x1 interface failed")

    @repeat_method(3)
    def test_02_traffic_and_verify_log(self):
        logger.info('traffic and verify log...')
        flag = False
        sleep(15)
        cmd = 'ping -c 10 {}'.format(http_server)
        local_host.send_command(cmd)
        sleep(15)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r"Interface X1 Link Is Down", str(output), re.S|re.I) and \
            re.search(r"WLB Failover in progress", str(output), re.S|re.I) and \
            re.search(r"WLB Resource failed", str(output), re.S|re.I) and \
            re.search(r"The network connection in use is NAT Static IP", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:traffic and verify log failed")

    def test_03_verify_routing_info_through_tsr(self):
        logger.info('verify routing info through tsr...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : Routing')
        if re.search(r"Any\s+0.0.0.0\/0\s+Any\s+N\/A\s+Any\s+{}".format(Parameter.PC_GW2_ETH2), str(output), re.S|re.I) :
            flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify routing info through tsr failed")

    def test_04_plug_x1_interface(self):
        logger.info('plug x1 interface...')
        systemlogObj.clear_log()
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    def test_05_traffic_and_verify_log_after_plug_x1(self):
        logger.info('traffic and verify log after plug x1...')
        flag = False
        cmd = 'ping -c 10 {}'.format(http_server)
        local_host.send_command(cmd)
        sleep(8)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r"Interface X1 Link Is Up", str(output), re.S|re.I) and \
            re.search(r"WLB Resource is now available", str(output), re.S|re.I) and \
            re.search(r"The network connection in use is NAT Static IP", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:traffic and verify log after plug x1 failed")

    def test_06_verify_routing_info_through_tsr(self):
        logger.info('verify routing info through tsr...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : Routing')
        if re.search(r"Any\s+0.0.0.0\/0\s+Any\s+N\/A\s+Any\s+{}".format(Parameter.PC_GW1_ETH2), str(output), re.S|re.I) :
            flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify routing info through tsr failed")


class Test_05_WAN_Failover_and_Load_Balancing_TP2201_tc_7(Test):
    uuid = "SOSAIOT-TC-57381"
    description= show_testcase_info(Parameter.TESTPLAN, '1506120', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506120')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_LB_group_to_uncheck_preempt(self):
        logger.info('Edit the default LB group to uncheck preempt...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": False,
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
        Assertion.assert_equal(rc, True, "ERR:edit the default LB group to uncheck preempt failed")

    def test_02_unplug_x1_interface(self):
        logger.info('unplug x1 interface...')
        systemlogObj.clear_log()
        rc = interfaceObj.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: unplug x1 interface failed")

    def test_03_traffic_and_verify_log(self):
        logger.info('traffic and verify log...')
        flag = False
        cmd = 'ping -c 10 {}'.format(http_server)
        local_host.send_command(cmd)
        sleep(8)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r"Interface X1 Link Is Down", str(output), re.S|re.I) and \
            re.search(r"WLB Failover in progress", str(output), re.S|re.I) and \
            re.search(r"WLB Resource failed", str(output), re.S|re.I) and \
            re.search(r"The network connection in use is NAT Static IP", str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR:traffic and verify log failed")

    def test_04_verify_routing_info_through_tsr(self):
        logger.info('verify routing info through tsr...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : Routing')
        if re.search(r"Any\s+0.0.0.0\/0\s+Any\s+N\/A\s+Any\s+{}".format(Parameter.PC_GW2_ETH2), str(output), re.S|re.I) :
            flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify routing info through tsr failed")

    def test_05_plug_x1_interface(self):
        logger.info('plug x1 interface...')
        systemlogObj.clear_log()
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    def test_06_traffic_and_verify_log_after_plug_x1(self):
        logger.info('traffic and verify log after plug x1...')
        flag = False
        cmd = 'ping -c 10 {}'.format(http_server)
        local_host.send_command(cmd)
        sleep(8)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r"Interface X1 Link Is Up", str(output), re.S|re.I) and \
            re.search(r"WLB Resource is now available", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:traffic and verify log after plug x1 failed")

    def test_07_verify_routing_info_through_tsr(self):
        logger.info('verify routing info through tsr...')
        flag = False
        output = diagObj.get_tsr_part2(func = 'Network : Routing')
        if re.search(r"Any\s+0.0.0.0\/0\s+Any\s+N\/A\s+Any\s+{}".format(Parameter.PC_GW2_ETH2), str(output), re.S|re.I) :
            flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify routing info through tsr failed")


class Test_06_WAN_Failover_and_Load_Balancing_TP2201_tc_8(Test):
    uuid = "SOSAIOT-TC-57383"
    description= show_testcase_info(Parameter.TESTPLAN, '1506122', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506122')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_LB_group(self):
        logger.info('Edit the default LB group...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "round-robin",
                        "final_backup": "",
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
        Assertion.assert_equal(rc, True, "ERR:edit the default LB group failed")

    @repeat_method(3)
    def test_02_verify_http_traffic(self):
        logger.info('verify http traffic...')
        flag = False
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        if re.search(r"Hello Automation", str(output1), re.S|re.I) :
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify http traffic failed")

    @repeat_method(3)
    def test_03_ftp_traffic(self):
        logger.info('send ftp traffic....')
        sleep(15)
        cmd = 'touch /home/ftp_tc8.txt'
        flag = False
        logger.info('create a new file ftp.txt:{}'.format(cmd))
        local_host.send_command(cmd)
        cmd_rcho = ""
        local_host.send_command("echo \"automation\" > \"/home/ftp_tc8.txt\"")
        cmd = 'python3 {}'.format('{}/upload_or_download_file.py upload sftp '.format(toolPath)) + '/home/ftp_tc8.txt '+' root ' + http_server + \
            ' /home/ftp_tc8.txt'  + ' password 22'
        logger.info('run cmd in pc1:{}'.format(cmd))
        local_host.send_command(cmd)
        cmd_server = 'cat /home/ftp_tc8.txt'
        logger.info('run cmd in http server:{}'.format(cmd_server))
        output = pc_server_ssh.send_command(cmd_server)
        if re.search(r"automation", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: send ftp traffic failed")

    @repeat_method(3)
    def test_04_verify_ping_and_packets(self):
        logger.info('verify ping and packet...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(10):
            output2 = local_host.send_command('ping -c 1 {}'.format(http_server))
        logger.info(output2)
        packetObj.stop_capture()
      
        output3 = packetObj.export_captured_packets()
        logger.info(output3)
        if not re.search(r"100% packet loss", str(output2), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, http_server), str(output3), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(http_server, Parameter.X1_IP), str(output3), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X2_IP, http_server), str(output3), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(http_server, Parameter.X2_IP), str(output3), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify ping and traffic failed")


class Test_07_WAN_Failover_and_Load_Balancing_TP2201_tc_10(Test):
    uuid = "SOSAIOT-TC-57333"
    description= show_testcase_info(Parameter.TESTPLAN, '1506063', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506063')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_enable_load_balance(self):
        logger.info('check enable load balance...')
        lb = {
            'enable': True
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check enable load balance failed")

    def test_02_check_boundary_for_ratio(self):
        logger.info('check boundary for ratio...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "ratio",
                        "final_backup": "",
                        "address_binding": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
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
                            {}
                        ],
                        "percent": [
                            {
                                "interface": "X1",
                                "percent": 110
                            },
                            {
                                "interface": "X2",
                                "percent": 50
                            }
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for ratio failed")

    def test_03_check_boundary_for_ratio(self):
        logger.info('check boundary for ratio...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "ratio",
                        "final_backup": "",
                        "address_binding": True,
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
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
                            {}
                        ],
                        "percent": [
                            {
                                "interface": "X1",
                                "percent": '@'
                            },
                            {
                                "interface": "X2",
                                "percent": 50
                            }
                        ]
                    }
                ]
            }
        }
        
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"expected: \\'NUMBER\\', found: \\'\"STRING...", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for ratio failed")


class Test_08_WAN_Failover_and_Load_Balancing_TP2201_tc_12(Test):
    uuid = "SOSAIOT-TC-57343"
    description= show_testcase_info(Parameter.TESTPLAN, '1506074', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506074')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_check_boundary_for_spill_over(self):
        logger.info('check boundary for spill over...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "spillover",
                        "final_backup": "",
                        "address_binding": False,
                        "spillover_bandwidth": {
                            "value": 12000000000
                        },
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for spill over failed")

    def test_02_check_boundary_for_spill_over(self):
        logger.info('check boundary for spill over...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "spillover",
                        "final_backup": "",
                        "address_binding": False,
                        "spillover_bandwidth": {
                            "value": '@'
                        },
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"expected: \\'NUMBER\\', found: \\'\"STRING...", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for spill over failed")


class Test_09_WAN_Failover_and_Load_Balancing_TP2201_tc_13(Test):
    uuid = "SOSAIOT-TC-57346"
    description= show_testcase_info(Parameter.TESTPLAN, '1506077', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506077')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_enable_load_balance(self):
        logger.info('check enable load balance...')
        lb = {
            'enable': True,
            'probes': True,
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check enable load balance failed")

    def test_02_config_LB_group(self):
        logger.info('Edit the default LB group...')
        lb ={
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "13.11.0.120"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "13.11.0.120"
                                },
                                "default_target": {}
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "13.12.0.120"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "13.12.0.120"
                                },
                                "default_target": {}
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(3)
    def test_03_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(60)
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(10)
        packetObj.stop_capture()
        output1 = packetObj.export_captured_packets()
        logger.info(output1)
        match_string="Time:(\d{2}\/\d{2}\/\d{4}\s)" +"(\d{2}:\d{2}:\d{2}).\d{3}"+ \
        ".*(ICMP\(0x1\),\sSrc=\[{}\],\sDst=\[{}\])".format(Parameter.X1_IP, Parameter.X1_GW)
        output2 = re.search(match_string, str(output1), re.S|re.I)
        time1 = output2.group(2)
        
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(10)
        packetObj.stop_capture()
        output3 = packetObj.export_captured_packets()
        logger.info(output3)
        output4 = re.search(match_string, str(output3), re.S|re.I)
        time2 = output4.group(2)
        logger.info(time1)
        logger.info(time2)

        date1 = datetime.datetime.strptime(time1, '%H:%M:%S')
        date2 = datetime.datetime.strptime(time2, '%H:%M:%S')
        reduce_time = date2 - date1
        logger.info(reduce_time.seconds)
        if reduce_time.seconds%5 == 0:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")


class Test_10_WAN_Failover_and_Load_Balancing_TP2201_tc_14(Test):
    uuid = "SOSAIOT-TC-57347"
    description= show_testcase_info(Parameter.TESTPLAN, '1506078', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506078')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_check_boundary_for_interface_every(self):
        logger.info('check boundary for interface every...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 300,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for check interface failed")

    def test_02_check_boundary_for_interface_every(self):
        logger.info('check boundary for interface every...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 310,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for check interface failed")

    def test_03_check_boundary_for_interface_every(self):
        logger.info('check boundary for interface every...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 1,
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for check interface failed")

    def test_04_check_boundary_for_interface_every(self):
        logger.info('check boundary for interface every...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": '%',
                            "missed_intervals": 3,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"expected: \\'NUMBER\\', found: \\'\"STRING...", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for check interface failed")


class Test_11_WAN_Failover_and_Load_Balancing_TP2201_tc_15(Test):
    uuid = "SOSAIOT-TC-57348"
    description= show_testcase_info(Parameter.TESTPLAN, '1506079', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506079')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_wan_failover_group(self):
        logger.info('check boundary for interface every...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for spill over failed")

    @repeat_method(3)
    def test_03_verify_log(self):
        logger.info('verify log...')
        flag = False
        systemlogObj.clear_log()
        sleep(5)
        rc = interfaceObj.enable_interface(name='X1')
        sleep(40)        
        rc = interfaceObj.disable_interface(name='X1')
        sleep(40)        
        output = systemlogObj.get_log()
        logger.info(output)
        match_string1="'time': '\d{2}\/\d{2}\/\d{4}\s(\d{2}:\d{2}:\d{2})',\s'id':\s566.*Interface X1 Link Is Down"
        output1 = re.search(match_string1, str(output), re.S|re.I|re.M)
        time1 = output1.group(1)

        match_string2="'time': '\d{2}\/\d{2}\/\d{4}\s(\d{2}:\d{2}:\d{2})',\s'id':\s584.*WLB Failover in progress"
        output2 = re.search(match_string2, str(output), re.S|re.I|re.M)
        time2 = output2.group(1)
        logger.info(time1)
        logger.info(time2)

        date1 = datetime.datetime.strptime(time1, '%H:%M:%S')
        date2 = datetime.datetime.strptime(time2, '%H:%M:%S')
        reduce_time = date2 - date1
        logger.info(reduce_time.seconds)
        if  5*3<=reduce_time.seconds<=5*4:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify log failed")


class Test_12_WAN_Failover_and_Load_Balancing_TP2201_tc_16(Test):
    uuid = "SOSAIOT-TC-57349"
    description= show_testcase_info(Parameter.TESTPLAN, '1506080', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506080')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_plug_interface_x1(self):
        logger.info('plug interface x1...')
        systemlogObj.clear_log()
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    def test_02_check_boundary_for_deactivate_interface(self):
        logger.info('check boundary for deactivate interface...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 100,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for deactivate interface failed")

    def test_03_check_boundary_for_deactivate_interface(self):
        logger.info('check boundary for deactivate interface...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 101,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for deactivate interface failed")


class Test_13_WAN_Failover_and_Load_Balancing_TP2201_tc_17(Test):
    uuid = "SOSAIOT-TC-57350"
    description= show_testcase_info(Parameter.TESTPLAN, '1506081', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506081')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_wan_load_balance(self):
        logger.info('config wan load balance...')
        sleep(10)
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 2,
                            "successful_intervals": 3,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for spill over failed")
    
    @repeat_method(5)
    def test_03_verify_log(self):
        logger.info('verify log...')
        flag = False
        systemlogObj.clear_log()
        sleep(5)
        rc = interfaceObj.enable_interface(name='X1')
        sleep(30) 
        rc = interfaceObj.disable_interface(name='X1')
        sleep(30) 
        output = systemlogObj.get_log()
        logger.info(output)
        match_string1="'time': '\d{2}\/\d{2}\/\d{4}\s(\d{2}:\d{2}:\d{2})',\s'id':\s566.*Interface X1 Link Is Down"
        output1 = re.search(match_string1, str(output), re.S|re.I|re.M)
        time1 = output1.group(1)

        match_string2="'time': '\d{2}\/\d{2}\/\d{4}\s(\d{2}:\d{2}:\d{2})',\s'id':\s584.*WLB Failover in progress"
        output2 = re.search(match_string2, str(output), re.S|re.I|re.M)
        time2 = output2.group(1)
        logger.info(time1)
        logger.info(time2)

        date1 = datetime.datetime.strptime(time1, '%H:%M:%S')
        date2 = datetime.datetime.strptime(time2, '%H:%M:%S')
        reduce_time = date2 - date1
        logger.info(reduce_time.seconds)
        if  5*2<=reduce_time.seconds<=5*3:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify log failed")


class Test_14_WAN_Failover_and_Load_Balancing_TP2201_tc_18(Test):
    uuid = "SOSAIOT-TC-57351"
    description= show_testcase_info(Parameter.TESTPLAN, '1506082', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506082')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_plug_interface_x1(self):
        logger.info('plug interface x1...')
        systemlogObj.clear_log()
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    def test_02_check_boundary_for_reactivate_interface(self):
        logger.info('check boundary for reactivate interface...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 100,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for reactivate interface failed")

    def test_03_check_boundary_for_reactivate_interface(self):
        logger.info('check boundary for reactivate interface...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 101,
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for reactivate interface failed")

    def test_04_check_boundary_for_reactivate_interface(self):
        logger.info('check boundary for reactivate interface...')
        flag = False
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "probing": {
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": '%',
                            "global_responder": False
                        },
                        "interface": [
                            {
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"expected: \\'NUMBER\\', found: \\'\"STRING...", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for reactivate interface failed")


class Test_15_WAN_Failover_and_Load_Balancing_TP2201_tc_35(Test):
    uuid = "SOSAIOT-TC-57371"
    description= show_testcase_info(Parameter.TESTPLAN, '1506104', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506104')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
   
    def test_01_check_boundary_for_port(self):
        logger.info('check boundary for port...')
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 65535
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 65535
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: check boundary for port failed")


    def test_02_check_boundary_for_port(self):
        logger.info('check boundary for port...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 65536
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 65536
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for port failed")

    def test_03_check_boundary_for_port(self):
        logger.info('check boundary for port...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": -1
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": -1
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"property 'value': invalid format", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for port failed")

    def test_04_check_boundary_for_port(self):
        logger.info('check boundary for port...')
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
                                "name": "X1",
                                "rank": 1,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 'a'
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 'a'
                                        }
                                    },
                                    "host": "responder.global.sonicwall.com"
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        output = failoverlbObj.config_failover_groups_by_multi(msg = True, **lb)
        logger.info(output)
        if re.search(r"expected: \\'NUMBER\\', found: \\'\"STRING...", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for port failed")


class Test_16_WAN_Failover_and_Load_Balancing_TP2201_tc_185(Test):
    uuid = "SOSAIOT-TC-57352"
    description= show_testcase_info(Parameter.TESTPLAN, '1506083', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506083')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_recover_load_balance(self):
        logger.info('recover load balance...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": False,
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
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")
    
    def test_02_config_interface_x2_to_dhcp(self):
        logger.info('config wan interface to dhcp...')
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: config wan interface x2 to dhcp failed")

    def test_03_get_ip_with_dhcp(self):
        logger.info('get ip with dhcp...')
        rc = interfaceObj.click_dhcp_renew(name = 'X2')
        Assertion.assert_equal(rc, True, "ERR: get ip with dhcp failed")

    def test_04_uncheck_preempt_for_groups(self):
        logger.info('uncheck preempt for groups...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
                        "preempt": False,
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")
   
    @repeat_method(3)
    def test_05_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(120)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    def test_06_unplug_interface_x1(self):
        logger.info('unplug interface x1...')
        sleep(10)
        rc = interfaceObj.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: unplug x1 interface failed")

    @repeat_method(3)
    def test_07_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        output = interfaceObj.get_interface_address(name = 'X2')
        output1 = re.search(r"ip_address':\s'(\d+.\d+.\d+.\d+)", str(output), re.S|re.I)
        x2_dhcp = output1.group(1)
        logger.info(x2_dhcp)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(x2_dhcp, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    def test_08_plug_interface_x1(self):
        logger.info('plug interface x1...')
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    @repeat_method(3)
    def test_09_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        output = interfaceObj.get_interface_address(name = 'X2')
        output1 = re.search(r"ip_address':\s'(\d+.\d+.\d+.\d+)", str(output), re.S|re.I)
        x2_dhcp = output1.group(1)
        logger.info(x2_dhcp)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(x2_dhcp, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")


class Test_17_WAN_Failover_and_Load_Balancing_TP2201_tc_186(Test):
    uuid = "SOSAIOT-TC-57353"
    description= show_testcase_info(Parameter.TESTPLAN, '1506084', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506084')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_check_preempt_for_groups(self):
        logger.info('check preempt for groups...')
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X1_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": Parameter.X2_GW
                                },
                                "default_target": {
                                    "value": Parameter.PC_Server_ETH0
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(3)
    def test_02_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    def test_03_unplug_interface_x1(self):
        logger.info('unplug interface x1...')
        rc = interfaceObj.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: unplug x1 interface failed")

    @repeat_method(3)
    def test_04_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        output = interfaceObj.get_interface_address(name = 'X2')
        output1 = re.search(r"ip_address':\s'(\d+.\d+.\d+.\d+)", str(output), re.S|re.I)
        x2_dhcp = output1.group(1)
        logger.info(x2_dhcp)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(x2_dhcp, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")

    def test_05_plug_interface_x1(self):
        logger.info('plug interface x1...')
        rc = interfaceObj.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: plug x1 interface failed")

    @repeat_method(3)
    def test_06_verify_traffic_out_when_connect_to_web_server(self):
        logger.info('verify traffic out when connect to web server...')
        flag = False
        sleep(30)
        output = interfaceObj.get_interface_address(name = 'X2')
        output1 = re.search(r"ip_address':\s'(\d+.\d+.\d+.\d+)", str(output), re.S|re.I)
        x2_dhcp = output1.group(1)
        logger.info(x2_dhcp)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(3):
            output=subprocess.run('curl http://{}'.format(http_server), shell=True, capture_output=True) 
            output1 = output.stdout.decode('utf-8')
            if output1:
                break
        logger.info('output1:{}'.format(output1))
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(output2)
        if re.search(r"Hello Automation", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(Parameter.X1_IP, http_server), str(output2), re.S|re.I):
                 flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic out when connect to web server fail")


class Test_18_WAN_Failover_and_Load_Balancing_TP2201_tc_19(Test):
    uuid = "SOSAIOT-TC-57354"
    description= show_testcase_info(Parameter.TESTPLAN, '1506085', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506085')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")
    
    def test_01_edit_wlb_groups(self):
        logger.info('edit wlb groups...')
        lb ={
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(3)
    def test_03_verify_traffic_ping_probe(self):
        logger.info('verify traffic ping probe ...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r"Src=\[{}\],\sDst=\[{}\]".format(Parameter.X1_IP, Parameter.X1_GW), str(output), re.S|re.I|re.M) and \
            re.search(r"Src=\[{}\],\sDst=\[{}\]".format(Parameter.X2_IP, Parameter.X2_GW), str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic ping probe fail")


class Test_19_WAN_Failover_and_Load_Balancing_TP2201_tc_22(Test):
    uuid = "SOSAIOT-TC-57357"
    description= show_testcase_info(Parameter.TESTPLAN, '1506088', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506088')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_wlb_groups(self):
        logger.info('edit wlb groups...')
        lb ={
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    def test_02_check_syn_load_balance(self):
        logger.info('check syn load balance...')
        lb = {
            'enable': True,
            'probes': True,
            'syn': True,
            'port': 8080

        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check syn load balance failed")

    def test_03_verify_traffic_tcp_probe(self):
        logger.info('verify traffic tcp probe ...')
        flag = False
        cmd = 'nc -v {} 8080'.format(Parameter.X1_IP)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(5):
            pc_gw1_ssh.send_command(cmd)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r"Consumed.*\[SYN,\],\sSrc=\[\d+\],\sDst=\[8080\]", str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_04_uncheck_syn_load_balance(self):
        logger.info('uncheck syn load balance...')
        lb = {   
            'probes': False,
            'syn': True,
            'port':8080

        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check syn load balance failed")

    def test_05_verify_traffic_tcp_probe(self):
        logger.info('verify traffic tcp probe ...')
        flag = False
        cmd = 'nc -v {} 8080'.format(Parameter.X1_IP)
        packetObj.clear_packets()
        packetObj.start_capture()
        for i in range(5):
            pc_gw1_ssh.send_command(cmd)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        if re.search(r"DROPPED.*\[SYN,\],\sSrc=\[\d+\],\sDst=\[8080\]", str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")


class Test_20_WAN_Failover_and_Load_Balancing_TP2201_tc_23(Test):
    uuid = "SOSAIOT-TC-57359"
    description= show_testcase_info(Parameter.TESTPLAN, '1506090', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506090')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_boundary_for_port(self):
        logger.info('check boundary for port...')
        lb = {   
            'probes': True,
            'syn': True,
            'port': 65535

        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: check syn load balance failed")

    def test_02_check_boundary_for_port(self):
        logger.info('check boundary for port...')
        flag = False
        lb = {   
            'probes': True,
            'syn': True,
            'port': 65536

        }
        output = failoverlbObj.config_failover_settings(msg=True, **lb)
        logger.info(output)
        if re.search(r"Value or string length\(\d+\) out of bounds", str(output), re.S|re.I):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: check boundary for port failed")


class Test_21_WAN_Failover_and_Load_Balancing_TP2201_tc_26(Test):
    uuid = "SOSAIOT-TC-57366"
    description= show_testcase_info(Parameter.TESTPLAN, '1506099', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506099')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_probe(self):
        logger.info('enable probe...')
        lb = {   
            'enable': True,
            'probes': True,
            'syn': False
        }
        rc = failoverlbObj.config_failover_settings(**lb)
        Assertion.assert_equal(rc, True, "ERR: enable probe failed")
    
    def test_02_config_wlb_for_groups(self):
        logger.info('config wlb for groups...')
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {}
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": "0.0.0.0"
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(2)
    def test_03_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP,http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP,http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_04_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_22_WAN_Failover_and_Load_Balancing_TP2201_tc_27(Test):
    uuid = "SOSAIOT-TC-57368"
    description= show_testcase_info(Parameter.TESTPLAN, '1506101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_for_groups(self):
        logger.info('config wlb for groups...')
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
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {}
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": "0.0.0.0"
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP,http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP,http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_23_WAN_Failover_and_Load_Balancing_TP2201_tc_29(Test):
    uuid = "SOSAIOT-TC-57369"
    description= show_testcase_info(Parameter.TESTPLAN, '1506102', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506102')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_to_succeed_always(self):
        logger.info('config wlb to succeed always...')
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
                                "probe_type": "logical",
                                "probe_condition": "always"
                            },
                               {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP,http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP,http_server)
        if not re.search(main_x1, str(output), re.S|re.I|re.M) and \
            not re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'No probing", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'No probing", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'No probing", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'No probing", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_24_WAN_Failover_and_Load_Balancing_TP2201_tc_31(Test):
    uuid = "SOSAIOT-TC-57370"
    description= show_testcase_info(Parameter.TESTPLAN, '1506103', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506103')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_for_groups(self):
        logger.info('config wlb for groups...')
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 80
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 80
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {}
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 80
                                        }
                                    },
                                    "host": http_server
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 80
                                        }
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": "0.0.0.0"
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*80".format(Parameter.X1_IP, http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*80".format(Parameter.X2_IP, http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_25_WAN_Failover_and_Load_Balancing_TP2201_tc_37(Test):
    uuid = "SOSAIOT-TC-57372"
    description= show_testcase_info(Parameter.TESTPLAN, '1506105', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506105')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_for_groups(self):
        logger.info('config wlb for groups...')
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
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": http_server
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "either",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                 "default_target": {
                                    "value": http_server
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP,http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP,http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")
  
  
class Test_26_WAN_Failover_and_Load_Balancing_TP2201_tc_45(Test):
    uuid = "SOSAIOT-TC-57375"
    description= show_testcase_info(Parameter.TESTPLAN, '1506108', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506108')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_interface_x3(self):
        logger.info("config x3 interface... ")
        interfaceObj.unassign_interface(interface = 'X4')
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_02_config_interface_x4(self):
        logger.info("config x4 interface... ")
        x4 = {
            'if': 'X4',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X4_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x4)
        Assertion.assert_equal(rc, True, "ERR: Config X4 IPv4 failed")

    def test_03_export_setting(self):
        logger.info('export setting...')
        rc = settingObj.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: export setting failed")


class Test_27_WAN_Failover_and_Load_Balancing_TP2201_tc_46(Test):
    uuid = "SOSAIOT-TC-57376"
    description= show_testcase_info(Parameter.TESTPLAN, '1506109', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506109')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot_fw_factory(self):
        logger.info('reboot fw default factory...')
        rc = settingObj.boot_fw(mode = 2)
        Assertion.assert_equal(rc, True, "ERR: reboot fw default factory failed")

    def test_02_import_setting(self):
        logger.info('export setting...')
        rc = settingObj.import_setting_exp(filepath = '/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: import setting failed")

    @repeat_method(2)
    def test_03_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP,http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP,http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_04_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_28_WAN_Failover_and_Load_Balancing_TP2201_tc_95(Test):
    uuid = "SOSAIOT-TC-57384"
    description= show_testcase_info(Parameter.TESTPLAN, '1506124', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506124')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_primary_wan_interface(self):
        logger.info('change primary wan interface...')
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
                                "name": "X2",
                                "rank": 1
                            },
                            {
                                "name": "X1",
                                "rank": 2
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: change primary wan interface failed")

    def test_02_get_wlb_setting(self):
        logger.info('get wlb setting...')
        flag = False
        output = failoverlbObj.check_failover_groups_status()
        logger.info(output)
        if re.search(r"Default LB Group.*primary_member':\s'X2", str(output[0]), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get wlb setting failed")


class Test_29_WAN_Failover_and_Load_Balancing_TP2201_tc_202(Test):
    uuid = "SOSAIOT-TC-57355"
    description= show_testcase_info(Parameter.TESTPLAN, '1506086', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506086')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_group(self):
        logger.info('config wlb group...')
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
                                "probe_type": "logical",
                                "probe_condition": "main",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "main",
                                "main_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": http_server
                                },
                                "default_target": {
                                    "value": default_target_ip
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: config wlb group failed")
 
    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X1_IP,http_server)
        main_x2 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X2_IP,http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify traffic tcp probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive'", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Not required", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Target Alive'", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Not required", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_30_WAN_Failover_and_Load_Balancing_TP2201_tc_209(Test):
    uuid = "SOSAIOT-TC-57356"
    description= show_testcase_info(Parameter.TESTPLAN, '1506087', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506087')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_wlb_group(self):
        logger.info('config wlb group...')
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
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": '0.0.0.0'
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: config wlb group failed")
 
    @repeat_method(2)
    def test_02_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        sleep(10)
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP, Parameter.X1_GW)
        alter_x1 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X1_IP, Parameter.X1_GW)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP, Parameter.X2_GW)
        alter_x2 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X2_IP, Parameter.X2_GW)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M) and\
            re.search(alter_x1, str(output), re.S|re.I|re.M) and\
            re.search(alter_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify main traffic when enable probe fail")

    def test_03_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


    def test_04_config_wlb_group(self):
        logger.info('config wlb group...')
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
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": http_server
                                }
                            },
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "both",
                                "main_target": {
                                    "protocol": {
                                        "tcp": {
                                            "value": 22
                                        }
                                    },
                                    "host": "0.0.0.0"
                                },
                                "alternate_target": {
                                    "protocol": {
                                        "ping": True
                                    },
                                    "host": "0.0.0.0"
                                },
                                "default_target": {
                                    "value": http_server
                                }
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: config wlb group failed")
 
    @repeat_method(2)
    def test_05_verify_main_traffic_out_when_enable_probe(self):
        logger.info('verify main traffic when enable probe...')
        flag = False
        packetObj.clear_packets()
        packetObj.start_capture()
        sleep(20)
        packetObj.stop_capture()
        output = packetObj.export_captured_packets()
        logger.info(output)
        main_x1 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X1_IP, http_server)
        alter_x1 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X1_IP, http_server)
        main_x2 = "TCP.*Src=\[{}\],\sDst=\[{}\].*22".format(Parameter.X2_IP, http_server)
        alter_x2 = "ICMP.*Src=\[{}\],\sDst=\[{}\]".format(Parameter.X2_IP, http_server)
        if re.search(main_x1, str(output), re.S|re.I|re.M) and \
            re.search(main_x2, str(output), re.S|re.I|re.M) and\
            re.search(alter_x1, str(output), re.S|re.I|re.M) and\
            re.search(alter_x2, str(output), re.S|re.I|re.M):
                flag =  True
        Assertion.assert_equal(flag, True, "ERR: verify main traffic when enable probe fail")

    def test_06_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'Default Target Alive", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_31_WAN_Failover_and_Load_Balancing_TP2201_tc_220(Test):
    uuid = "SOSAIOT-TC-57358"
    description= show_testcase_info(Parameter.TESTPLAN, '1506089', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1506089')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_config_wlb_to_succeed_always(self):
        logger.info('config wlb to succeed always...')
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
                                "probe_type": "logical",
                                "probe_condition": "always"
                            },
                               {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "logical",
                                "probe_condition": "always"
                            },
                            {}
                        ]
                    }
                ]
            }
        }
        rc = failoverlbObj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, "ERR: edit the default LB group failed")

    def test_02_verify_wan_load_balancing_statistics(self):
        logger.info('verify wan load balancing statistics...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"member_name\'\:\s\'X1", str(output[0]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[0]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[0]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'No probing", str(output[0]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'No probing", str(output[0]), re.S|re.I) and \
            re.search(r"member_name\'\:\s\'X2", str(output[1]), re.S|re.I) and \
            re.search(r"link_status\'\:\s\'Link Up", str(output[1]), re.S|re.I) and \
            re.search(r"lb_status\'\:\s\'Available", str(output[1]), re.S|re.I) and \
            re.search(r"main_target_status\'\:\s\'No probing", str(output[1]), re.S|re.I) and \
            re.search(r"alternate_target_status\'\:\s\'No probing", str(output[1]), re.S|re.I)   :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify wan load balancing statistics failed")


class Test_32_WAN_Failover_and_Load_Balancing_TP2201_tc_260(Test):
    uuid = "SOSAIOT-TC-57367"
    description= show_testcase_info(Parameter.TESTPLAN, '1506100', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '260')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
      
    def test_01_config_interface_x1_to_dhcp(self):
        logger.info('config wan interface x1 to dhcp...')
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'dhcp',
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: config wan interface x1 to dhcp failed")

    def test_02_get_ip_with_dhcp(self):
        logger.info('get ip with dhcp...')
        rc = interfaceObj.click_dhcp_renew(name = 'X1')
        Assertion.assert_equal(rc, True, "ERR: get ip with dhcp failed")

    def test_03_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")
    
    def test_04_config_interface_x3(self):
        logger.info('config interface x3...')
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_schedule':'always_on',
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: config wan interface x3 to pppoe failed")

    def test_05_add_x3_to_wlb(self):
        logger.info('add x3 to wlb ...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
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
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc, True, "ERR: add x3 to wlb failed")

    def test_06_get_wlb_setting(self):
        logger.info('get wlb setting...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"group_name':\s'\sDefault LB Group',\s'member_name':\s'X3", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get wlb setting failed")

    def test_07_remove_x3_from_wlb(self):
        logger.info('remove x3 from wlb ...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
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
        Assertion.assert_equal(rc, True, "ERR: remove x3 from wlb failed")

    def test_08_config_interface_x3_pptp(self):
        logger.info('config interface x3...')
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_user': 'test',
            'pptp_passwd': 'test',
            'pptp_server': '10.8.2.254',
            'mgmt_snmp': True,
        }
        rc = interfaceObj.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: config wan interface x3 to pptp failed")

    def test_09_add_x3_to_wlb(self):
        logger.info('add x3 to wlb ...')
        lb = {
            "failover_lb": {
                "group": [
                    {
                        "name": " Default LB Group",
                        "type": "basic",
                        "final_backup": "",
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
                            {
                                "name": "X2",
                                "rank": 2,
                                "probe_type": "physical",
                                "probe_condition": "always"
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
        Assertion.assert_equal(rc, True, "ERR: add x3 to wlb failed")

    def test_10_get_wlb_setting(self):
        logger.info('get wlb setting...')
        flag = False
        output = failoverlbObj.check_failover_members_status()
        logger.info(output)
        if re.search(r"group_name':\s'\sDefault LB Group',\s'member_name':\s'X3", str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: get wlb setting failed")
