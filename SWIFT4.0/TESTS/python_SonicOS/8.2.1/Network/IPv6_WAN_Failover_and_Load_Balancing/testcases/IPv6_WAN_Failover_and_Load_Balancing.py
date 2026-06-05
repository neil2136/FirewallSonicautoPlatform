from definition.settings import *


class Test_IPv6_WAN_Failover_and_LB_01(Test):
    uuid = "SOSAIOT-TC-56704"
    description= show_testcase_info(TESTPLAN, '1523957', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523957')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_failover(self):
        rc = failover_obj.config_failover_settings(**failover_json)
        Assertion.assert_equal(rc, True, f"ERR: check failover info fail.")

    def test_02_check_failover(self):
        res1 = failover_obj.check_failover_setting()
        rc1 = True if res1['failover_lb']['enable'] == False else False
        rc1 &= failover_obj.reset_statistics(version = 'ipv6')
        time.sleep(5)
        res2 = failover_obj.get_statistics_report()
        if res2[1]['total_connection'] == 0 and res2[1]['rx_unicast'] == 0 and res2[1]['total_unicast_bytes'] == 0:
            rc1 &= True 
        else:
            rc1 &= False
        Assertion.assert_equal(rc1 , True, f"ERR: check failover info fail.")

    def test_03_config_and_check_failover(self):
        ref = copy.deepcopy(failover_json)
        ref['enable'] = True
        rc = failover_obj.config_failover_settings(**ref)
        res1 = failover_obj.check_failover_setting()
        if res1['failover_lb']['enable'] == True:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check failover info fail.")


class Test_IPv6_WAN_Failover_and_LB_02(Test):
    uuid = "SOSAIOT-TC-56705"
    description= show_testcase_info(TESTPLAN, '1523958', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523958')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_probes_disable(self):
        ref = copy.deepcopy(failover_json)
        ref['enable'] = True
        rc = failover_obj.config_failover_settings(**ref)
        res1 = failover_obj.check_failover_setting()
        if res1['failover_lb']['respond_to_probes'] == False:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check failover info fail.")

    def test_02_config_and_check_probes_enable(self):
        ref = copy.deepcopy(failover_json)
        ref['enable'] = True
        ref['probes'] = True
        rc = failover_obj.config_failover_settings(**ref)
        res1 = failover_obj.check_failover_setting()
        if res1['failover_lb']['respond_to_probes'] == True:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check failover info fail.")


class Test_IPv6_WAN_Failover_and_LB_03(Test):
    uuid = "SOSAIOT-TC-56706"
    description= show_testcase_info(TESTPLAN, '1523959', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523959')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_tcp_syn_disable(self):
        ref = copy.deepcopy(failover_json)
        ref['enable'] = True
        ref['probes'] = True
        rc = failover_obj.config_failover_settings(**ref)
        res1 = failover_obj.check_failover_setting()
        if res1['failover_lb']['any_tcp_syn'] == False:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check failover info fail.")

    def test_02_config_and_check_tcp_syn_enable(self):
        ref = copy.deepcopy(failover_json)
        ref2 = copy.deepcopy(failover_port)
        ref['enable'] = True
        ref['probes'] = True
        ref['syn'] = True
        ref2['port'] = 65535
        rc = failover_obj.config_failover_settings(**ref)
        res1 = failover_obj.check_failover_setting()
        if res1['failover_lb']['any_tcp_syn'] == True:
            rc &= True
        else:
            rc &= False
        rc &= failover_obj.config_failover_settings(**ref2)
        Assertion.assert_equal(rc, True, f"ERR:config and check failover info fail.")

    def test_03_config_and_check_port_out_boundary(self):
        ref1 = copy.deepcopy(failover_port)
        ref2 = copy.deepcopy(failover_port)
        ref1['port'] = 0
        ref2['port'] = 65536
        rc = failover_obj.config_failover_settings(**ref1)
        rc &= failover_obj.config_failover_settings(**ref2)
        Assertion.assert_equal(rc, False, f"ERR:config and check port out boundarys fail.")

    def test_04_restore_env(self):
        rc = failover_obj.config_failover_settings(**failover_port)
        Assertion.assert_equal(rc, True, f"ERR:config failover info fail.")


class Test_IPv6_WAN_Failover_and_LB_04(Test):
    uuid = "SOSAIOT-TC-56707"
    description= show_testcase_info(TESTPLAN, '1523960', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523960')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Basic Failover' in res1[1]['type'] and 'Active' in  res1[1]['status'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_05(Test):
    uuid = "SOSAIOT-TC-56708"
    description= show_testcase_info(TESTPLAN, '1523961', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523961')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_round_robin)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Round Robin' in res1[1]['type'] and 'Active' in  res1[1]['status'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_06(Test):
    uuid = "SOSAIOT-TC-56709"
    description= show_testcase_info(TESTPLAN, '1523962', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523962')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_spill)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Spill-over' in res1[1]['type'] and 'Active' in  res1[1]['status'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")
        

class Test_IPv6_WAN_Failover_and_LB_07(Test):
    uuid = "SOSAIOT-TC-56710"
    description= show_testcase_info(TESTPLAN, '1523963', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523963')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_radio)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Ratio' in res1[1]['type'] and 'Active' in  res1[1]['status'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")
        

##round robin group status no keyword about IP address binding
class Test_IPv6_WAN_Failover_and_LB_08(Test):
    uuid = "SOSAIOT-TC-56712"
    description= show_testcase_info(TESTPLAN, '1523965', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523965')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_round_robin)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.get_failover_groups_info()
        res2 = failover_obj.get_statistics_report()
        if res1['failover_lb']['group'][1]['address_binding'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


## spill over group status no keywords about IP address binding and bandwidth
class Test_IPv6_WAN_Failover_and_LB_09(Test):
    uuid = "SOSAIOT-TC-56713"
    description= show_testcase_info(TESTPLAN, '1523966', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523966')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_spill)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.get_failover_groups_info()
        res2 = failover_obj.get_statistics_report()
        if res1['failover_lb']['group'][1]['address_binding'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_10(Test):
    uuid = "SOSAIOT-TC-56714"
    description= show_testcase_info(TESTPLAN, '1523967', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523967')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Spill-over' in res1[1]['type'] and 'Active' in  res1[1]['status'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_11(Test):
    uuid = "SOSAIOT-TC-56711"
    description= show_testcase_info(TESTPLAN, '1523964', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523964')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        ref['failover_lb']['group'][0]['final_backup']='X2'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_statistics_report()
        if 'Basic Failover' in res1[1]['type'] and 'X2' in  res1[1]['final_back_up'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")

    def test_03_restore_env(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")


##ratio group status no keyword about IP address binding
class Test_IPv6_WAN_Failover_and_LB_12(Test):
    uuid = "SOSAIOT-TC-56715"
    description= show_testcase_info(TESTPLAN, '1523968', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523968')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_radio)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_show_group_and_statistics(self):
        time.sleep(5)
        res1 = failover_obj.get_failover_groups_info()
        res2 = failover_obj.get_statistics_report()
        if res1['failover_lb']['group'][1]['address_binding'] \
            and 'total_connection' in res2[1].keys() and 'rx_unicast' in res2[1].keys():
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show group and statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_13(Test):
    uuid = "SOSAIOT-TC-56716"
    description= show_testcase_info(TESTPLAN, '1523969', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523969')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_check_group_member(self):
        res1 = failover_obj.check_failover_groups_status()
        rc = True if  res1[1]['total_members'] == 1 else False
        Assertion.assert_equal(rc, True, f"ERR:check group member fail.")

    def test_03_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_04_check_group_member(self):
        res1 = failover_obj.check_failover_groups_status()
        rc = True if  res1[1]['total_members'] == 2 else False
        Assertion.assert_equal(rc, True, f"ERR:check group member  fail.")


class Test_IPv6_WAN_Failover_and_LB_14(Test):
    uuid = "SOSAIOT-TC-56717"
    description= show_testcase_info(TESTPLAN, '1523970', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523970')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        ref['failover_lb']['group'][0]['final_backup']='X2'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_check_group_final_back(self):
        res1 = failover_obj.check_failover_groups_status()
        if 'X2' in  res1[1]['final_back_up']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:check group final back  fail.")

    def test_03_config_lb_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_04_check_group_final_back(self):
        res1 = failover_obj.check_failover_groups_status()
        rc = True if  res1[1]['final_back_up'] == 'Unknown' else False
        Assertion.assert_equal(rc, True, f"ERR:check group final back  fail.")

###skip repeat uuid 1523977
class Test_IPv6_WAN_Failover_and_LB_15(Test):
    uuid = "SOSAIOT-TC-56718"
    description= show_testcase_info(TESTPLAN, '1523971', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523971')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'physical'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_member_probing(self):
        res = failover_obj.check_failover_members_status()
        rc = True if res[2]['member_name'] == 'X2' and 'Physical' in  res[2]['probe_status']  else False
        Assertion.assert_equal(rc, True, f"ERR:check member probing  fail.")


class Test_IPv6_WAN_Failover_and_LB_16(Test):
    uuid = "SOSAIOT-TC-56719"
    description= show_testcase_info(TESTPLAN, '1523972', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523972')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'logical'
        ref['failover_lb']['group'][0]['interface'][1]['probe_condition'] = 'always'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_member_probing(self):
        res = failover_obj.check_failover_members_status()
        rc = True if res[2]['member_name'] == 'X2' and "Logical   - Succeeds always" in res[2]['probe_status'] else False
        Assertion.assert_equal(rc, True, f"ERR:check member probing  fail.")

#### skip 1523973,check Succeeds always all target gray


class Test_IPv6_WAN_Failover_and_LB_17(Test):
    uuid = "SOSAIOT-TC-56720"
    description= show_testcase_info(TESTPLAN, '1523974', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523974')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        ref['failover_lb']['group'][0]['interface'].append(x2_main)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        result['main_config'] = rc 
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_member_probing(self):
        res = failover_obj.check_failover_members_status()
        rc = True if res[2]['member_name'] == 'X2' and "Logical   - Only main target is required" in res[2]['probe_status'] else False
        Assertion.assert_equal(rc, True, f"ERR:check member probing  fail.")


class Test_IPv6_WAN_Failover_and_LB_18(Test):
    uuid = "SOSAIOT-TC-56721"
    description= show_testcase_info(TESTPLAN, '1523975', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523975')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        ref['failover_lb']['group'][0]['interface'].append(x2_both)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        result['both_config'] = rc 
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_member_probing(self):
        res = failover_obj.check_failover_members_status()
        rc = True if res[2]['member_name'] == 'X2' and "Logical   - All targets must reply" in res[2]['probe_status'] else False
        Assertion.assert_equal(rc, True, f"ERR:check member probing  fail.")


class Test_IPv6_WAN_Failover_and_LB_19(Test):
    uuid = "SOSAIOT-TC-56722"
    description= show_testcase_info(TESTPLAN, '1523976', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523976')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        ref['failover_lb']['group'][0]['interface'].append(x2_either)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_member_probing(self):
        res = failover_obj.check_failover_members_status()
        rc = True if res[2]['member_name'] == 'X2' and "Logical   - At least one target should reply" in res[2]['probe_status'] else False
        Assertion.assert_equal(rc, True, f"ERR:check member probing  fail.")


class Test_IPv6_WAN_Failover_and_LB_20(Test):
    uuid = "SOSAIOT-TC-56723"
    description= show_testcase_info(TESTPLAN, '1523978', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523978')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_main_target_input(self):
        rc = result['main_config']
        Assertion.assert_equal(rc, True, "ERR: check main target input failed")


class Test_IPv6_WAN_Failover_and_LB_21(Test):
    uuid = "SOSAIOT-TC-56724"
    description= show_testcase_info(TESTPLAN, '1523979', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523979')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_alternate_target_input(self):
        rc = result['both_config']
        Assertion.assert_equal(rc, True, "ERR: check alternate target input failed")


class Test_IPv6_WAN_Failover_and_LB_22(Test):
    uuid = "SOSAIOT-TC-56725"
    description= show_testcase_info(TESTPLAN, '1523980', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523980')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_target_ip_input(self):
        rc = result['both_config']
        Assertion.assert_equal(rc, True, "ERR: check target ip input failed")


class Test_IPv6_WAN_Failover_and_LB_23(Test):
    uuid = "SOSAIOT-TC-56726"
    description= show_testcase_info(TESTPLAN, '1523981', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523981')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_display_and_check_statistics_report(self):
        res = failover_obj.get_statistics_report()
        rc = True if res[1]['group_name'] == ' Default LB Group IPv6' and res[1]['member_name'] == 'X1' and res[2]['member_name'] == 'X2' else False
        Assertion.assert_equal(rc, True, f"ERR:display and check statistics fail.")


###skip 1523982,api can not check clear ipv6 statistics for multi interfaces
class Test_IPv6_WAN_Failover_and_LB_24(Test):
    uuid = "SOSAIOT-TC-56727"
    description= show_testcase_info(TESTPLAN, '1523983', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523983')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sattic_interface_for_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        res = failover_obj.check_failover_members_status()
        if res[1]['member_name'] == 'X1' and res[2]['member_name'] == 'X2':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:add sattic interface for group fail.")


class Test_IPv6_WAN_Failover_and_LB_25(Test):
    uuid = "SOSAIOT-TC-56728"
    description= show_testcase_info(TESTPLAN, '1523984', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523984')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][1]['name'] = f'X3:V{vlan_tag}'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")
    
    def test_02_check_group_vlan_member(self):
        res = failover_obj.check_failover_members_status()
        if res[1]['member_name'] == 'X1' and res[2]['member_name'] == f'X3:V{vlan_tag}':
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:check group vlan member fail.")


class Test_IPv6_WAN_Failover_and_LB_26(Test):
    uuid = "SOSAIOT-TC-56729"
    description= show_testcase_info(TESTPLAN, '1523985', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523985')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_display_and_check_statistics_report(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6)
        res = failover_obj.check_failover_members_status()
        if 'Default LB Group' in res[0]['group_name'] and res[0]['member_name'] == 'X1' and \
             res[1]['group_name'] == ' Default LB Group IPv6' and res[1]['member_name'] == 'X1' \
                 and res[2]['member_name'] == 'X2':
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:display and check v4 v6 interface fail.")


class Test_IPv6_WAN_Failover_and_LB_27(Test):
    uuid = "SOSAIOT-TC-56730"
    description= show_testcase_info(TESTPLAN, '1523986', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523986')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_and_chack_lb_group_by_cli(self):
        cmds = ["show failover-lb  group \ Default\ LB\ Group\ IPv6"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'type basic' in res1 and 'interface X1' in res1 and 'interface X2' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check lb group info fail.")


class Test_IPv6_WAN_Failover_and_LB_28(Test):
    uuid = "SOSAIOT-TC-56731"
    description= show_testcase_info(TESTPLAN, '1523987', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523987')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_and_chack_responder_by_cli(self):
        cmds = ["show failover-lb  responder"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'Responder Status:         Enabled' in res1 and 'Probe Requests Received' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check  failover-lb responder fail.")


class Test_IPv6_WAN_Failover_and_LB_29(Test):
    uuid = "SOSAIOT-TC-56732"
    description= show_testcase_info(TESTPLAN, '1523988', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523988')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_and_chack_lb_statistics_by_cli(self):
        cmds = ["show failover-lb statistics group \ Default\ LB\ Group\ IPv6"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'New Connection' in res1 and 'Average Ratio' in res1 and 'X1' in res1 and 'X2' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check failover-lb statistics fail.")


class Test_IPv6_WAN_Failover_and_LB_30(Test):
    uuid = "SOSAIOT-TC-56733"
    description= show_testcase_info(TESTPLAN, '1523989', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523989')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_chack_lb_status_by_cli(self):
        cmds = ["show failover-lb status"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'Default LB Group IPv6  Basic Failover  Active' in res1 and 'Default LB Group       Basic Failover  Active' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check failover-lb status fail.")


class Test_IPv6_WAN_Failover_and_LB_31(Test):
    uuid = "SOSAIOT-TC-56734"
    description= show_testcase_info(TESTPLAN, '1523990', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523990')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_chack_lb_status_group_by_cli(self):
        cmds = ["show failover-lb status group \ Default\ LB\ Group\ IPv6"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'Active' in res1 and 'Basic Failover' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check failover-lb status group fail.")


class Test_IPv6_WAN_Failover_and_LB_32(Test):
    uuid = "SOSAIOT-TC-56735"
    description= show_testcase_info(TESTPLAN, '1523991', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523991')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_chack_lb_member_status_by_cli(self):
        cmds = ["show failover-lb  status members"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        check_str1 = "Default LB Group IPv6  X2\s*Link Up\s*Available\s*Physical"
        check_str2 = "Default LB Group IPv6  X1\s*Link Up\s*Available\s*Physical"
        if re.search(check_str1, res1, re.M) and re.search(check_str2, res1, re.M):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check failover-lb member status fail.")


class Test_IPv6_WAN_Failover_and_LB_33(Test):
    uuid = "SOSAIOT-TC-56736"
    description= show_testcase_info(TESTPLAN, '1523992', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523992')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_chack_lb_by_cli(self):
        cmds = ["show failover-lb"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        check_str1 = "Default LB Group.|\s*?interface X1.|\s*?Default LB Group IPv6.*?interface X1.|\s*?interface X2"
        # check_str1 = "Default LB Group.|\s*?interface X1"
        if re.search(check_str1, res1, re.M):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check failover-lb  fail.")


class Test_IPv6_WAN_Failover_and_LB_34(Test):
    uuid = "SOSAIOT-TC-56737"
    description= show_testcase_info(TESTPLAN, '1523993', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523993')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_lb(self):
        rc = failover_cli.enable_Load_Balancing(**lb_cli)
        Assertion.assert_equal(rc, True, f"ERR:enable lb  fail.")
    
    def test_02_check_lb(self):
        res = failover_obj.check_failover_setting()
        if res['failover_lb']['enable'] == True:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: check failover info fail.")

#### show lb
class Test_IPv6_WAN_Failover_and_LB_35(Test):
    uuid = "SOSAIOT-TC-56738"
    description= show_testcase_info(TESTPLAN, '1523994', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523994')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_show_and_chack_lb_group_by_cli(self):
        cmds = ["show failover-lb  group \ Default\ LB\ Group\ IPv6"]
        res1 = fw_cli.do_cli_commands(cmds,tag=1)[1]
        if 'type basic' in res1 and 'interface X1' in res1 and 'interface X2' in res1:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR:show and check lb group info fail.")


class Test_IPv6_WAN_Failover_and_LB_36(Test):
    uuid = "SOSAIOT-TC-56739"
    description= show_testcase_info(TESTPLAN, '1523995', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523995')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_group_basic(self):
        rc = failover_cli.edit_default_LB(**basic_cli)
        res1 = failover_obj.check_failover_groups_status()
        rc2 = True if f'X3:V{vlan_tag}' in res1[1]['final_back_up'] else False
        result['check_backup'] = rc&rc2
        if 'Basic Failover' in res1[1]['type'] :
            rc &= True
        else:
            rc &= False
        
        Assertion.assert_equal(rc, True, f"ERR:config and check group type basic fail.")


class Test_IPv6_WAN_Failover_and_LB_37(Test):
    uuid = "SOSAIOT-TC-56740"
    description= show_testcase_info(TESTPLAN, '1523996', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523996')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_backup(self):
        rc = result['check_backup']
        Assertion.assert_equal(rc, True, f"ERR: check group backup fail.")


class Test_IPv6_WAN_Failover_and_LB_38(Test):
    uuid = "SOSAIOT-TC-56741"
    description= show_testcase_info(TESTPLAN, '1523997', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523997')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_group_ratio(self):
        rc = failover_cli.edit_default_LB(**ratio_cli)
        res1 = failover_obj.check_failover_groups_status()

        res2 = failover_obj.get_failover_groups_info()
        logger.info(f'-----{res2}')
        rc2 = True if res2['failover_lb']['group'][1]['address_binding'] else False
        result['check_ratio_bind'] = rc & rc2
        rc3 = True if res2['failover_lb']['group'][1]['percent'][0]['percent'] == 60 else False
        result['check_ratio_percent'] = rc & rc3
        if 'Ratio' in res1[1]['type'] :
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check group type ratio fail.")


class Test_IPv6_WAN_Failover_and_LB_39(Test):
    uuid = "SOSAIOT-TC-56742"
    description= show_testcase_info(TESTPLAN, '1523998', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523998')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ratio_binding(self):
        rc = result['check_ratio_bind']
        Assertion.assert_equal(rc, True, f"ERR: check group ratio Address binding fail.")


class Test_IPv6_WAN_Failover_and_LB_40(Test):
    uuid = "SOSAIOT-TC-56743"
    description= show_testcase_info(TESTPLAN, '1523999', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1523999')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ratio_percent(self):
        rc = result['check_ratio_percent']
        Assertion.assert_equal(rc, True, f"ERR: check group ratio -Manual Percent can be set fail.")


## auto-adjust-ratio can not get info from api
class Test_IPv6_WAN_Failover_and_LB_41(Test):
    uuid = "SOSAIOT-TC-56744"
    description= show_testcase_info(TESTPLAN, '1524000', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524000')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_auto_adjust_ratio(self):
        ref = copy.deepcopy(ratio_cli)
        del ref['percentages']
        ref['auto-adjust-ratio'] = True
        rc = failover_cli.edit_default_LB(**ref)
        res = failover_obj.get_failover_groups_info()
        res = failover_obj.check_failover_members_status()
        res1 = failover_obj.check_failover_groups_status()
        Assertion.assert_equal(rc, True, f"ERR: config auto adjust ratio fail.")
    

class Test_IPv6_WAN_Failover_and_LB_42(Test):
    uuid = "SOSAIOT-TC-56745"
    description= show_testcase_info(TESTPLAN, '1524001', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524001')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_group_rundrobin(self):
        rc = failover_cli.edit_default_LB(**round_robin_cli)
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_failover_groups_info()
        logger.info(f'-----{res2}')
        rc2 = True if res2['failover_lb']['group'][1]['address_binding'] else False
        result['check_rundrobin_bind'] = rc & rc2
        if 'Round Robin' in res1[1]['type'] :
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check group type round robin fail.")


class Test_IPv6_WAN_Failover_and_LB_43(Test):
    uuid = "SOSAIOT-TC-56746"
    description= show_testcase_info(TESTPLAN, '1524002', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524002')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_round_robin_binding(self):
        rc = result['check_rundrobin_bind']
        Assertion.assert_equal(rc, True, f"ERR: check group round robin Address binding fail.")


class Test_IPv6_WAN_Failover_and_LB_44(Test):
    uuid = "SOSAIOT-TC-56747"
    description= show_testcase_info(TESTPLAN, '1524003', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524003')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_and_check_group_spillover(self):
        rc = failover_cli.edit_default_LB(**spill_cli)
        res1 = failover_obj.check_failover_groups_status()
        res2 = failover_obj.get_failover_groups_info()

        logger.info(f'-----{res2}')
        rc2 = True if res2['failover_lb']['group'][1]['address_binding'] else False
        result['check_spill_bind'] = rc & rc2
        rc3 = True if res2['failover_lb']['group'][1]['probing']['global_responder'] == False else False
        result['check_global_responder'] = rc & rc3
        rc4 = True if res2['failover_lb']['group'][1]['probing']['health_check'] == 5 else False
        result['check_health_check'] = rc & rc4
        rc5 = True if res2['failover_lb']['group'][1]['probing']['missed_intervals'] == 6 else False
        result['check_missed_intervals'] = rc & rc5
        rc6 = True if res2['failover_lb']['group'][1]['probing']['successful_intervals'] == 7 else False
        result['check_successful_intervals'] = rc & rc6

        if 'Spill-over' in res1[1]['type'] and res2['failover_lb']['group'][1]['spillover_bandwidth']['value'] == 1000:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR:config and check group type spill over fail.")


class Test_IPv6_WAN_Failover_and_LB_45(Test):
    uuid = "SOSAIOT-TC-56748"
    description= show_testcase_info(TESTPLAN, '1524004', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524004')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_spill_over_binding(self):
        rc = result['check_spill_bind']
        Assertion.assert_equal(rc, True, f"ERR: check group spill over Address binding fail.")


class Test_IPv6_WAN_Failover_and_LB_46(Test):
    uuid = "SOSAIOT-TC-56749"
    description= show_testcase_info(TESTPLAN, '1524005', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524005')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_global_responder(self):
        rc = result['check_global_responder']
        Assertion.assert_equal(rc, True, f"ERR: check group global responder fail.")


class Test_IPv6_WAN_Failover_and_LB_47(Test):
    uuid = "SOSAIOT-TC-56750"
    description= show_testcase_info(TESTPLAN, '1524006', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524006')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_health(self):
        rc = result['check_health_check']
        Assertion.assert_equal(rc, True, f"ERR: check group health check fail.")


class Test_IPv6_WAN_Failover_and_LB_48(Test):
    uuid = "SOSAIOT-TC-56751"
    description= show_testcase_info(TESTPLAN, '1524007', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524007')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_Deactivate_Interface_missed_intervals(self):
        rc = result['check_missed_intervals']
        Assertion.assert_equal(rc, True, f"ERR: check group Deactivate Interface missed intervals fail.")

class Test_IPv6_WAN_Failover_and_LB_49(Test):
    uuid = "SOSAIOT-TC-56752"
    description= show_testcase_info(TESTPLAN, '1524008', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524008')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_reactivate_Interfacesuccessful_intervals(self):
        rc = result['check_successful_intervals']
        Assertion.assert_equal(rc, True, f"ERR: check group Reactivate Interface successful intervals fail.")

##skip 1524009,1524010,1524011
###start function test
@unittest.skipIf('8.2' in Params.sonicos_ver, 'Skip as issue wont fixed')
class Test_IPv6_WAN_Failover_and_LB_50(Test):
    uuid = "SOSAIOT-TC-56753"
    goto_teardown = True
    description= show_testcase_info(TESTPLAN, '1524012', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524012')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'physical'
        ref['failover_lb']['group'][0]['interface'][1]['probe_condition'] = 'always'
        ref['failover_lb']['group'][0]['preempt']=False
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        result['1524017'] = [rc]
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_disable_x1(self):
        rc = interfacev4api.disable_interface(name='X1')
        result['1524017'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: disable x1 interface failed")

    @repeat_method(3)
    def test_03_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) \
            and re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X2_IPV6), str(output2), re.S|re.I) \
            and not re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        result['1524017'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    def test_04_enable_x1(self):
        rc = interfacev4api.enable_interface(name='X1')
        result['1524017'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: enable x1 interface failed")

    @repeat_method(3)
    def test_05_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) \
            and re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X2_IPV6), str(output2), re.S|re.I) \
            and not re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_WAN_Failover_and_LB_51(Test):
    uuid = "SOSAIOT-TC-56754"
    description= show_testcase_info(TESTPLAN, '1524013', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524013')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        #del ref['failover_lb']['group'][0]['interface'][1]
        #ref['failover_lb']['group'][0]['final_backup']='X2'
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'physical'
        ref['failover_lb']['group'][0]['interface'][1]['probe_condition'] = 'always'
        ref['failover_lb']['group'][0]['preempt']=True
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_disable_x1(self):
        rc = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: disable x1 interface failed")

    @repeat_method(3)
    def test_03_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
             re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) and \
             re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X2_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    def test_04_enable_x1(self):
        rc = interfacev4api.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: enable x1 interface failed")

    @repeat_method(3)
    def test_05_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
             re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) and \
             re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

# @unittest.skipIf('TZ80' in PLATFORM_NAME, 'skip')
# class Test_IPv6_WAN_Failover_and_LB_52(Test):
#     uuid = '1524014'
#     description= show_testcase_info(TESTPLAN, '1524014', description=True)['title']

#     def test_00_show_testcase_info(self):
#         show_testcase_info(TESTPLAN, '1524014')
#         Assertion.assert_equal(True, True, "ERR: show testcase info failed")

#     def test_01_config_lb_group(self):
    #     rc = failover_obj.config_failover_groups_by_multi(**lb_ipv6_round_robin)
    #     Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    # @repeat_method(3)
    # def test_02_check_traffic(self):
        # time.sleep(15)
        # packetObj.clear_packets()
        # packetObj.start_capture()
        # output1 = PC1.send_commands(traffic_cmd)
        # packetObj.stop_capture()
        # output2 = packetObj.export_captured_packets()
        # logger.info(f'----{output2}')
        # if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
        #      re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
        #     rc = True
        # else:
        #     rc = False
        # Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    # @repeat_method(3)
    # def test_03_modify_src_ip(self):
    #     cmds = ['sudo ip addr flush dev eth0','ifconfig eth0 inet6 add 2001:db0::112/64','ifconfig eth0 192.168.168.200/24','ip addr']
    #     output = PC1.send_commands(cmds)
    #     if '2001:db0::112/64' in str(output) and '192.168.168.200/24' in str(output) and '2001:db0::1093/64' not in str(output):
    #         rc = True
        # else:
        #     rc = False
        # Assertion.assert_equal(rc, True, "ERR: modify src addr  failed")
    
    # @repeat_method(3)
    # def test_04_check_traffic(self):
    #     time.sleep(15)
    #     packetObj.clear_packets()
    #     packetObj.start_capture()
    #     output1 = PC1.send_commands(traffic_cmd)
    #     packetObj.stop_capture()
        # output2 = packetObj.export_captured_packets()
        # logger.info(f'----{output2}')
        # if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
        #      re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
        #     rc = True
        # else:
        #     rc = False
        #     st = re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I)
        #     logger.info('--search key words failed---')
        #     logger.info(f'------{st}---')
        # Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    # def test_05_restore_env(self):
    #     cmds = ['ifconfig eth0 inet6 del 2001:db0::112/64','ifconfig eth0 inet6 add 2001:db0::1093/64','ip addr']
    #     output = PC1.send_commands(cmds)
    #     if '2001:db0::112/64' not in str(output) and '2001:db0::1093/64'  in str(output):
        #     rc = True
        # else:
        #     rc = False
        # Assertion.assert_equal(rc, True, "ERR: restore env  failed")

##skip 1524015

class Test_IPv6_WAN_Failover_and_LB_53(Test):
    uuid = "SOSAIOT-TC-56756"
    description= show_testcase_info(TESTPLAN, '1524016', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524016')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6_radio)
        ref['failover_lb']['group'][0]['percent'][0]['percent']=20
        ref['failover_lb']['group'][0]['percent'][1]['percent']=80
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_check_traffic(self):
        time.sleep(15)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
                re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_WAN_Failover_and_LB_54(Test):
    uuid = "SOSAIOT-TC-56757"
    description= show_testcase_info(TESTPLAN, '1524017', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524017')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    # def test_01_check_result(self):
    #     if len(result['1524017'] ) == 4 and all(result['1524017']):
    #         rc = True
    #     else:
    #         rc = False
    #     Assertion.assert_equal(rc, True, "ERR: check result failed")
    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'physical'
        ref['failover_lb']['group'][0]['interface'][1]['probe_condition'] = 'always'
        ref['failover_lb']['group'][0]['preempt']=False
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        # result['1524017'] = [rc]
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_disable_x1(self):
        rc = interfacev4api.disable_interface(name='X1')
        # result['1524017'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: disable x1 interface failed")

    @repeat_method(3)
    def test_03_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) \
            and re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X2_IPV6), str(output2), re.S|re.I) \
            and not re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        # result['1524017'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")



class Test_IPv6_WAN_Failover_and_LB_55(Test):
    uuid = "SOSAIOT-TC-56758"
    description= show_testcase_info(TESTPLAN, '1524018', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524018')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref = copy.deepcopy(lb_ipv6)
        ref['failover_lb']['group'][0]['interface'][0]['probe_type'] = 'logical'
        ref['failover_lb']['group'][0]['interface'][0]['probe_condition'] = 'always'
        ref['failover_lb']['group'][0]['interface'][1]['probe_type'] = 'logical'
        ref['failover_lb']['group'][0]['interface'][1]['probe_condition'] = 'always'
        ref['failover_lb']['group'][0]['preempt']=False
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_disable_x1(self):
        rc = interfacev4api.disable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: disable x1 interface failed")

    @repeat_method(3)
    def test_03_check_traffic_via_x2(self):
        time.sleep(30)
        packetObj.clear_packets()
        packetObj.start_capture()
        output1 = PC1.send_commands(traffic_cmd)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if not re.search(r"100% packet loss", str(output1), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X2_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I) and\
            re.search(r"Src=\[{}\], Dst=\[{}\]".format( PC_Server_ETH0_IPV6,DUT_X2_IPV6), str(output2), re.S|re.I) \
            and not re.search(r"Src=\[{}\], Dst=\[{}\]".format(DUT_X1_IPV6, PC_Server_ETH0_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    def test_04_enable_x1(self):
        rc = interfacev4api.enable_interface(name='X1')
        Assertion.assert_equal(rc, True, "ERR: enable x1 interface failed")


class Test_IPv6_WAN_Failover_and_LB_56(Test):
    uuid = "SOSAIOT-TC-56759"
    description= show_testcase_info(TESTPLAN, '1524019', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524019')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref = copy.deepcopy(lb_ipv6)
        del ref['failover_lb']['group'][0]['interface'][1]
        del ref1['failover_lb']['group'][0]['interface'][0]
        del ref1['failover_lb']['group'][0]['interface'][0]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,x1_main)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        rc &= failover_obj.config_failover_groups_by_multi(**ref1)
        result['1524022'] = [rc]
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    @repeat_method(3)
    def test_02_check_target_package(self):
        time.sleep(8)
        packetObj.clear_packets()
        packetObj.start_capture()
        time.sleep(30)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if  re.search(r"Src=\[{}\], Dst=\[{}\]".format(PC_Server_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        result['1524022'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    @repeat_method(5)
    def test_03_config_lb_group_and_check_status(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref2 = copy.deepcopy(x1_main)
        ref2['main_target']['host']="2001:db4::1193"
        del ref1['failover_lb']['group'][0]['interface'][0]
        del ref1['failover_lb']['group'][0]['interface'][0]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,ref2)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        time.sleep(25)
        res1 = failover_obj.check_failover_members_status()
        if  'Failover' in  res1[1]['lb_status']:
            rc &= True
        else:
            rc &= False
        result['1524022'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_WAN_Failover_and_LB_57(Test):
    uuid = "SOSAIOT-TC-56760"
    description= show_testcase_info(TESTPLAN, '1524020', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524020')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref1['failover_lb']['group'][0]['interface']=[]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,x1_both)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        result['1524023'] = [rc]
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    @repeat_method(3)
    def test_02_check_target_package(self):
        time.sleep(18)
        packetObj.clear_packets()
        packetObj.start_capture()
        logger.info('time sleep 15s')
        time.sleep(15)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if  re.search(r"Src=\[{}\], Dst=\[{}\]".format(PC_Server_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(PC2_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        result['1524023'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    @repeat_method(3)
    def test_03_config_lb_group_and_check_target_package(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref2 = copy.deepcopy(x1_both)
        ref2['alternate_target']['host']="2001:db4::1193"
        ref1['failover_lb']['group'][0]['interface']=[]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,ref2)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        time.sleep(25)
        res1 = failover_obj.check_failover_members_status()
        if  'Failover' in  res1[1]['lb_status']:
            rc &= True
        else:
            rc &= False
        result['1524023'].append(rc)
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_WAN_Failover_and_LB_58(Test):
    uuid = "SOSAIOT-TC-56761"
    description= show_testcase_info(TESTPLAN, '1524021', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524021')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref1['failover_lb']['group'][0]['interface']=[]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,x1_either)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_check_target_package(self):
        packetObj.clear_packets()
        packetObj.start_capture()
        logger.info('time sleep 15s')
        time.sleep(15)
        packetObj.stop_capture()
        output2 = packetObj.export_captured_packets()
        logger.info(f'----{output2}')
        if  re.search(r"Src=\[{}\], Dst=\[{}\]".format(PC_Server_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I) and \
            re.search(r"Src=\[{}\], Dst=\[{}\]".format(PC2_ETH0_IPV6,DUT_X1_IPV6), str(output2), re.S|re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

    def test_03_config_lb_group(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref2 = copy.deepcopy(x1_either)
        ref2['main_target']['host']="2001:db4::1193"
        ref2['alternate_target']['host']=PC3_ETH0_IPV6
        ref1['failover_lb']['group'][0]['interface']=[]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref1['failover_lb']['group'][0]['interface'].insert(0,ref2)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    @repeat_method(3)
    def test_04_check_status(self):
        time.sleep(25)
        res1 = failover_obj.check_failover_members_status()
        if  'Failover' in  res1[1]['lb_status']:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")


class Test_IPv6_WAN_Failover_and_LB_59(Test):
    uuid = "SOSAIOT-TC-56762"
    description= show_testcase_info(TESTPLAN, '1524022', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524022')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_result(self):
        print('------------',len(result['1524022']))
        if len(result['1524022']) ==3 and all(result['1524022']):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check result failed")


class Test_IPv6_WAN_Failover_and_LB_60(Test):
    uuid = "SOSAIOT-TC-56763"
    description= show_testcase_info(TESTPLAN, '1524023', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524023')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_result(self):
        if len(result['1524023']) ==3 and all(result['1524023']) :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check result failed")


@repeat_class(3, sleep=10)
class Test_IPv6_WAN_Failover_and_LB_61(Test):
    uuid = "SOSAIOT-TC-56764"
    description= show_testcase_info(TESTPLAN, '1524024', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_group(self):
        ref1 = copy.deepcopy(lb_ipv6)
        ref2 = copy.deepcopy(x1_main)
        ref1['failover_lb']['group'][0]['interface']=[]
        ref1['failover_lb']['group'][0]['final_backup']='X2'
        ref2['main_target']['host']= '2001:db4::1193'
        ref2['default_target']['value']= PC3_ETH0_IPV6
        ref1['failover_lb']['group'][0]['interface'].insert(0,ref2)
        rc = failover_obj.config_failover_groups_by_multi(**ref1)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_02_check_default_ip(self):
        res = failover_obj.get_failover_groups_info()
        if res['failover_lb']['group'][1]['interface'][0]['default_target']['value'] == PC3_ETH0_IPV6:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check default ip failed")

      
class Test_IPv6_WAN_Failover_and_LB_62(Test):
    uuid = "SOSAIOT-TC-56765"
    description= show_testcase_info(TESTPLAN, '1524025', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524025')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_preference(self):
        rc = setting_obj.export_setting_exp()
        with open('/tmp/test.exp','rb') as f:
            f2 = base64.b64decode(f.read())
        with open('/tmp/test.txt','wb') as new_f:
            new_f.write(f2)
        res = PC1.send_command('cat /tmp/test.txt')
        if 'wlb_Enable=on&wlb_IsResponder=on' in res:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check setting exp failed")


class Test_IPv6_WAN_Failover_and_LB_63(Test):
    uuid = "SOSAIOT-TC-56767"
    description= show_testcase_info(TESTPLAN, '1524027', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524027')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_and_chack_tsr(self):
        res = diag_api.get_tsr_part(func='Network', lab1='Failover & LB')
        if 'Active    Default LB Group IPv6' in res and 'Failover & Load Balancing           : Enabled' in res:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: export and check tsr failed")


class Test_IPv6_WAN_Failover_and_LB_64(Test):
    uuid = "SOSAIOT-TC-56766"
    description= show_testcase_info(TESTPLAN, '1524026', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1524026')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_lb_and_check_log(self):
        log_api.clear_log()
        rc = failover_obj.config_failover_settings(**failover_json)
        time.sleep(2)
        res = log_api.export_log_txt()
        logger.info(res)
        if "Configuration succeeded:  'Respond to Probes' , changed from [enabled], changed to [disabled]" in res:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: config failover lb and check log failed")

    def test_02_restore_env(self):
        rc = failover_obj.config_failover_settings(**failover_port)
        Assertion.assert_equal(rc, True, "ERR: restore env failed")
        
#skip uuid 1524029,1524028







