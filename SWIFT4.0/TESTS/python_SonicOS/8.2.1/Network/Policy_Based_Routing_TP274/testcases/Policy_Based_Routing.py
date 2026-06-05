from definition.settings import *
from definition.utils import *


# Except: traffic passed via new route from X0 to X2.
class TestPBR_TC12(Test):
    uuid = "SOSAIOT-TC-58677"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']
    tc12routename = 'tc12_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_add_new_route_policy(self):
        route_base_dict['name'] = self.tc12routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_02_traffic_pass_via_new_route(self):
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res & checkres, True, "ERR: test new route failed.")

    def test_03_delete_route_policy_by_uuid(self):
        tag = False
        output = routepolicyapi.get_route_policy_by_name(self.tc12routename)
        if type(output) is dict and 'route_policies' in output.keys():
            if output['route_policies'][0]['ipv4']['name'] == self.tc12routename:
                logger.info(f'get route policy {self.tc12routename} successful.')
                routeuuid = output['route_policies'][0]['ipv4']['uuid']
                tag = routepolicyapi.del_route_policy_by_uuid(uuid=routeuuid)
            else:
                logger.error('edit source name failed')
        else:
            logger.error(f'can not get the route form policy: {self.tc12routename}')
        Assertion.assert_equal(tag, True, "ERR: Delete route policy failed.")

    def test_04_traffic_pass_via_default_route(self):
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        res &= False if checkres else True
        Assertion.assert_equal(res, True, "ERR: test default route failed.")

    def test_05_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        Assertion.assert_equal(True, True, "ERR: init failed")


# Except: traffic passed via edit route from X0 to X2.
class TestPBR_TC17(Test):
    uuid = "SOSAIOT-TC-58680"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']
    tc17routename = 'tc17_route_policy'
    tc17aoname = 'tc17_source_ao'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(res, None, "ERR: show test case info failed")

    def test_01_add_new_route_policy(self):
        route_base_dict['name'] = self.tc17routename
        route_base_dict['service'] = {'name': 'FTP'}
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_02_add_custom_address_object(self):
        ao_dict = {
            "object_type": "network",
            "name": self.tc17aoname,
            "zone": "LAN",
            "value": "192.168.168.0,255.255.255.0"
        }
        res = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, "ERR: Failed To Add Address Object")

    def test_03_edit_route_policy(self):
        route_base_dict['service'] = {'group': 'Ping'}
        route_base_dict['source'] = {"name": self.tc17aoname}
        res = routepolicyapi.edit_route_policy(self.tc17routename, **route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Edit route policy failed")

    def test_04_check_source_and_service_in_policy(self):
        tag = False
        output = routepolicyapi.get_route_policy_by_name(self.tc17routename)
        if type(output) is dict and 'route_policies' in output.keys():
            if output['route_policies'][0]['ipv4']['source']['name'] == self.tc17aoname:
                logger.info('edit source name successful')
                if output['route_policies'][0]['ipv4']['service']['group'] == "Ping":
                    logger.info('edit service group successful')
                    tag = True
                else:
                    logger.error('edit service group failed')
            else:
                logger.error('edit source name failed')
        else:
            logger.error(f'can not get the route form policy: {self.tc17routename}')
        Assertion.assert_equal(tag, True, "ERR: Verify Parameters Of Edited Route Policy Failed.")

    def test_05_traffic_pass_via_edit_route(self):
        tag = False
        for i in range(3):
            time.sleep(10)
            (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
            logger.info(f'packets captured on FW result: {packets}')
            (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
            logger.info(f'check icmp request forwarded result: {packet}')
            if res and checkres:
                tag = True
                break
        CasesParam.tc17_edit_res = tag
        Assertion.assert_equal(tag, True, "ERR: test traffic via new route failed.")

    def test_06_init_fw_route_ao(self):
        routepolicyapi.del_route_policy_by_name(self.tc17routename)
        aoapi.delete_addressobject('network',
                                   object_path='name',
                                   object_name_uuid=self.tc17aoname,
                                   ip_type='ipv4')
        route_base_dict.update(org_base_dict)
        Assertion.assert_equal(True, True, "ERR: init fw route and ao failed")


# Except: edit route policy successful.
class TestPBR_TC11(Test):
    uuid = "SOSAIOT-TC-58676"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(res, None, "ERR: show test case info failed")

    def test_01_edit_route_policy(self):
        editres = CasesParam.tc17_edit_res
        Assertion.assert_equal(editres, True, "ERR: edit route failed")


# Except: pc1 http traffic should be redirected to route1,
# pc3 http traffic should be redirected to route2,
# pc1 ftp traffic should be redirected to route3.
class TestPBR_TC23(Test):
    uuid = "SOSAIOT-TC-58681"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']
    tc23ao1 = 'tc23_pc1_eth1'
    tc23ao2 = 'tc23_pc3_eth1'
    tc23routename1 = 'tc23_route_policy1'
    tc23routename2 = 'tc23_route_policy2'
    tc23routename3 = 'tc23_route_policy3'

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_create_address_objects(self):
        ao_dict1 = {
            "object_type": "host",
            "name": self.tc23ao1,
            "zone": "LAN",
            "value": PC1_ETH1_IP
        }
        ao_dict2 = {
            "object_type": "host",
            "name": self.tc23ao2,
            "zone": "LAN",
            "value": PC3_ETH1_IP
        }
        res = aoapi.config_addressobject(**ao_dict1)
        res &= aoapi.config_addressobject(**ao_dict2)
        Assertion.assert_equal(res, True, "ERR: Failed To Add Address Object")

    def test_02_add_new_route_policy(self):
        tag = []
        rchange_dict1 = {
            'name': self.tc23routename1,
            'source': {"name": self.tc23ao1},
            'service': {'name': 'HTTPS'},
        }
        rchange_dict2 = {
            'name': self.tc23routename2,
            'interface': 'X3',
            'source': {"name": self.tc23ao2},
            'service': {'name': 'HTTPS'},
            'gateway': {'name': 'X3 Default Gateway'},
        }
        rchange_dict3 = {
            'name': self.tc23routename3,
            'source': {"name": self.tc23ao1},
            'service': {'name': 'FTP'},
        }
        route_lists = [rchange_dict1, rchange_dict2, rchange_dict3]
        for changed in route_lists:
            route_base_dict.update(changed)
            output = routepolicyapi.add_route_policy(**route_policy_dict)
            if output is False:
                logger.error(f'add route policy {changed["name"]} failed')
            tag.append(output)
            route_base_dict.update(org_base_dict)
        Assertion.assert_equal(all(tag), True, "ERR: Add route policy failed")

    def test_03_http_traffic_pass_on_pc1_via_route1(self):
        pc_run_http_dict = {
            'type': 'http',  # ping, cmd, http,script
            'url': 'https://mysonicwall.com',
        }
        (httpres, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_http_dict)
        logger.info(f'http request result: {httpres}')
        logger.info(f'packets captured on FW result: {packets}')
        (reqres, packet) = http_request_check(packets, src_ip=PC1_ETH1_IP)
        logger.info(f'check http request forwarded result: {packet}')
        (respres, packet) = http_reponse_check(packets, dst_ip=Parameter.X2_IP)
        logger.info(f'check http response forwarded result: {packet}')
        Assertion.assert_equal(httpres & reqres & respres, True, "ERR: test traffic via new route failed.")

    def test_04_http_traffic_pass_on_pc3_via_route2(self):
        pc_run_script_dict = {
            'type': 'script',  # ping, cmd, http,script
            'protocol': 'http',
            'url': 'https://mysonicwall.com',
            'path': SCRIPT_PATH
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC3_login, pc_run_script_dict)
        logger.info(f'http request result: {res}')
        httpres = True if '200' in res else False
        logger.info(f'packets captured on FW result: {packets}')
        (respres, packet) = http_reponse_check(packets, packet_in='X3', dst_ip=Parameter.X3_IP)
        logger.info(f'check http response forwarded result: {packet}')
        Assertion.assert_equal(httpres & respres, True, "ERR: test traffic via new route failed.")

    def test_05_ftp_traffic_pass_via_route3(self):
        pc_run_script_dict = {
            'type': 'script',  # ping, cmd, http,script
            'protocol': 'ftp',
            'url': 'ftp://gcc.gnu.org',
            'path': SCRIPT_PATH
        }
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_script_dict)
        logger.info(f'ftp request result: {res}')
        logger.info(f'packets captured on FW result: {packets}')
        (reqres, packet) = ftp_request_check(packets, src_ip=PC1_ETH1_IP)
        logger.info(f'check ftp request result: {packet}')
        (forres, packet) = ftp_request_check(packets, packet_in='--', src_ip=Parameter.X2_IP)
        logger.info(f'check ftp forwarded result: {packet}')
        Assertion.assert_equal(reqres & forres, True, "ERR: test traffic via new route failed.")

    def test_06_init_route_and_aos(self):
        routepolicyapi.del_route_policy_by_name(self.tc23routename1)
        routepolicyapi.del_route_policy_by_name(self.tc23routename2)
        routepolicyapi.del_route_policy_by_name(self.tc23routename3)
        aoapi.delete_addressobject(
            'host',
            object_path='name',
            object_name_uuid=self.tc23ao1,
            ip_type='ipv4')
        aoapi.delete_addressobject(
            'host',
            object_path='name',
            object_name_uuid=self.tc23ao2,
            ip_type='ipv4')
        route_base_dict.update(org_base_dict)
        Assertion.assert_equal(True, True, "ERR: init Failed")


# Except: route probe will control the new route
class TestPBR_TC27(Test):
    uuid = "SOSAIOT-TC-58683"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']
    tc27aoname = 'tc27_unreachable_ao'
    tc27nmalivename = 'tc27_probe_alive'
    tc27nmofflinename = 'tc27_probe_off_line'
    tc27routename = 'tc27_route_test1'

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_create_unreachable_address_object(self):
        ao_dict = {
            "object_type": "host",
            "name": self.tc27aoname,
            "zone": "WLAN",
            "value": "3.3.3.3"
        }
        res = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(res, True, "ERR: Failed To Add WLAN Host Address Object")

    def test_02_add_network_monitors_probe(self):
        nm_param_alive = {
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": self.tc27nmalivename,
                        'probe': {'target': {'name': 'X2 Default Gateway'},
                                  'type': {'ping': 'non-explicit'},
                                  'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        "comment": ""
                    }
                }
            }]
        }
        nm_param_offline = {
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": self.tc27nmofflinename,
                        'probe': {'target': {'name': self.tc27aoname},
                                  'type': {'ping': 'non-explicit'},
                                  'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        "comment": ""
                    }
                }
            }]
        }
        res = networkmonitorapi.add_network_monitor(**nm_param_alive)
        res &= networkmonitorapi.add_network_monitor(**nm_param_offline)
        Assertion.assert_equal(res, True, "ERR: Failed To Add Probe")

    def test_03_add_new_route_with_alive_probe(self):
        probe_dict = {
            "name": self.tc27routename,
            "probe": self.tc27nmalivename,
            "disable_when_probes_succeed": False,
            "default_probe_state_up": False,
        }
        route_base_dict.update(probe_dict)
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_04_traffic_pass_via_new_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res & checkres, True, "ERR: test ping failed.")

    def test_05_edit_route_to_offline_probe(self):
        route_base_dict['probe'] = self.tc27nmofflinename
        res = routepolicyapi.edit_route_policy(self.tc27routename, **route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: edit route policy failed")

    def test_06_traffic_not_pass_via_edit_route(self):
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, False, "ERR: test ping failed.")

    def test_07_init_route_and_aos(self):
        routepolicyapi.del_route_policy_by_name(self.tc27routename)
        networkmonitorapi.del_network_monitor(self.tc27nmalivename)
        networkmonitorapi.del_network_monitor(self.tc27nmofflinename)
        aoapi.delete_addressobject(
            'host',
            object_path='name',
            object_name_uuid=self.tc27aoname,
            ip_type='ipv4')
        route_base_dict.update(org_base_dict)
        del route_base_dict['disable_when_probes_succeed']
        del route_base_dict['default_probe_state_up']
        Assertion.assert_equal(True, True, "ERR: init Failed")


# Except: traffic passed via default route after x2 link down.
class TestPBR_TC26(Test):
    uuid = "SOSAIOT-TC-58682"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']
    tc26routename = 'tc26_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_add_new_route_policy(self):
        route_base_dict['name'] = self.tc26routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_02_traffic_pass_via_new_route(self):
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res & checkres, True, "ERR: test new route failed.")

    @repeat_method(3)
    def test_03_x2_link_down(self):
        res = os_obj.set_node_interface_state('UTM', 'X2', 'disable')
        Assertion.assert_equal(res, True, "ERR: x2 link down failed")

    def test_04_traffic_pass_via_default_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        res &= False if checkres else True
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res, True, "ERR: test default route failed.")

    def test_05_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc26routename)
        os_obj.set_node_interface_state('UTM', 'X2', 'enable')
        time.sleep(10)
        Assertion.assert_equal(True, True, "ERR: init failed")


# Except: group2 can be added to group3 after add group3 to new route.
class TestPBR_TC43(Test):
    uuid = "SOSAIOT-TC-58687"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']
    tc43ao1 = 'Site_A'
    tc43ao2 = 'Site_B'
    tc43group1 = 'Site_A_Group'
    tc43group2 = 'Site_B_Group'
    tc43group3 = 'Test_Net'
    tc43routename = 'tc43route1'

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_create_aos_and_groups(self):
        ao_dict1 = {
            "object_type": "host",
            "name": self.tc43ao1,
            "zone": "LAN",
            "value": '12.3.4.5'
        }
        ao_dict2 = {
            "object_type": "host",
            "name": self.tc43ao2,
            "zone": "LAN",
            "value": '13.4.5.6'
        }
        aogroup_dict1 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {"ipv4": [{"name": self.tc43ao1}]},
                        "name": self.tc43group1
                    }
                }
            ]
        }
        aogroup_dict2 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {"ipv4": [{"name": self.tc43ao2}]},
                        "name": self.tc43group2
                    }
                }
            ]
        }
        aogroup_dict3 = {
            "address_groups": [{
                "ipv4": {
                    "address_group": {"ipv4": [{"name": self.tc43group1}]},
                    "name": self.tc43group3
                }}]}
        res = aoapi.config_addressobject(**ao_dict1)
        res &= aoapi.config_addressobject(**ao_dict2)
        res &= aogroupapi.add_addressgroup(**aogroup_dict1)
        res &= aogroupapi.add_addressgroup(**aogroup_dict2)
        res &= aogroupapi.add_addressgroup(**aogroup_dict3)
        Assertion.assert_equal(res, True, "ERR: Failed To Add Address Object and groups")

    def test_02_add_new_route_policy(self):
        route_base_dict['name'] = self.tc43routename
        route_base_dict['source'] = {"group": self.tc43group3}
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_03_add_group2_to_group3(self):
        aogroup_dict = {
            "address_groups": [{
                "ipv4": {
                    "address_group": {
                        "ipv4": [
                            {"name": self.tc43group1},
                            {"name": self.tc43group2}
                        ]},
                    "name": self.tc43group3
                }}]}
        res = aogroupapi.edit_addressgroup_by_name(name='Test_Net', **aogroup_dict)
        Assertion.assert_equal(res, True, "ERR: add group2 to group3 failed")

    def test_04_init_ao_zones_config(self):
        del_ao_dict1 = {
            'ip_type': 'ipv4',
            'name': self.tc43ao1,
        }
        del_ao_dict2 = {
            'ip_type': 'ipv4',
            'name': self.tc43ao2,
        }
        route_base_dict.update(org_base_dict)
        res = routepolicyapi.del_route_policy_by_name(self.tc43routename)
        aogroupapi.del_addressgroup(name=self.tc43group3)
        aogroupapi.del_addressgroup(name=self.tc43group2)
        aogroupapi.del_addressgroup(name=self.tc43group1)
        aoapi.del_addressobject(**del_ao_dict1)
        aoapi.del_addressobject(**del_ao_dict2)
        Assertion.assert_equal(res, True, "ERR: init fw config failed")


# Except: traffic will pass via x2 after configured failover x1 and x2.
class TestPBR_TC44(Test):
    uuid = "SOSAIOT-TC-58688"
    description = show_testcase_info(TESTPLAN, '44', description=True)['title']
    tc44routename = 'tc44_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '44')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_configure_dut_failover(self):
        res = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config DUT failover failed")

    def test_02_add_new_route_policy(self):
        route_base_dict['name'] = self.tc44routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_03_traffic_pass_via_new_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res & checkres, True, "ERR: test new route failed.")

    def test_04_init_lb_route_config(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc44routename)
        Assertion.assert_equal(True, True, "ERR: init fw config failed")


# Except: traffic passed via default route after set new route to invalid service.
class TestPBR_TC45(Test):
    uuid = "SOSAIOT-TC-58689"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']
    tc45routename = 'tc45_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_add_new_route_policy(self):
        route_base_dict['name'] = self.tc45routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_02_traffic_pass_via_new_route(self):
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(res & checkres, True, "ERR: test new route failed.")

    def test_03_edit_route_policy(self):
        route_base_dict['service'] = {'name': 'HTTP'}
        res = routepolicyapi.edit_route_policy(self.tc45routename, **route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Edit route policy failed")

    def test_04_traffic_pass_via_default_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        res &= False if checkres else True
        Assertion.assert_equal(res, True, "ERR: test default route failed.")

    def test_05_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc45routename)
        Assertion.assert_equal(True, True, "ERR: init failed")


# Except: traffic passed via default route after probe failover the x2 in lb.
class TestPBR_TC46(Test):
    uuid = "SOSAIOT-TC-58690"
    description = show_testcase_info(TESTPLAN, '46', description=True)['title']
    tc46routename = 'tc46_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_configure_invalid_x2_failover_lb(self):
        x2_lb_dict = {
            "default_target": {
                "value": "0.0.0.0"
            },
            "main_target": {
                "host": "66.66.66.66",
                "protocol": {
                    "ping": True
                }
            },
            "name": "X2",
            "probe_condition": "main",
            "probe_type": "logical",
            "rank": 2
        }
        org_wanlb_dict = copy.deepcopy(wlb_conf_dict)
        org_wanlb_dict['failover_lb']['group'][0]['interface'][1] = x2_lb_dict
        res = failoverapi.config_failover_groups_by_multi(**org_wanlb_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failover lb to invalid ip failed")

    def test_02_add_new_route_policy(self):
        route_base_dict['name'] = self.tc46routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_03_traffic_pass_via_default_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        # res &= False if checkres else True
        Assertion.assert_equal(checkres, False, "ERR: test default route failed.")

    def test_04_configure_valid_x2_failover_lb(self):
        res = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failover lb to invalid ip failed")

    def test_05_traffic_pass_via_new_route(self):
        time.sleep(30)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        CasesParam.tc47_traffic_res = checkres
        Assertion.assert_equal(checkres, True, "ERR: test new route failed.")

    def test_06_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc46routename)
        Assertion.assert_equal(True, True, "ERR: init failed")


# Except: traffic passed via new route after probe back the x2 in lb.
class TestPBR_TC47(Test):
    uuid = "SOSAIOT-TC-58691"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(res, None, "ERR: show test case info failed")

    def test_05_traffic_pass_via_new_route(self):
        res = CasesParam.tc47_traffic_res
        Assertion.assert_equal(res, True, "ERR: test traffic failed")


# Except: traffic passed via new route after switch logical probe to physical.
class TestPBR_TC48(Test):
    uuid = "SOSAIOT-TC-58692"
    description = show_testcase_info(TESTPLAN, '48', description=True)['title']
    tc48routename = 'tc48_route_policy'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '48')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_configure_invalid_x2_failover_lb(self):
        x2_lb_dict = {
            "default_target": {
                "value": "0.0.0.0"
            },
            "main_target": {
                "host": '66.66.66.66',
                "protocol": {
                    "ping": True
                }
            },
            "name": "X2",
            "probe_condition": "main",
            "probe_type": "logical",
            "rank": 2
        }
        org_wanlb_dict = copy.deepcopy(wlb_conf_dict)
        org_wanlb_dict['failover_lb']['group'][0]['interface'][1] = x2_lb_dict
        res = failoverapi.config_failover_groups_by_multi(**org_wanlb_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failover lb to invalid ip failed")

    def test_02_add_new_route_policy(self):
        route_base_dict['name'] = self.tc48routename
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_03_traffic_pass_via_default_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        # res &= False if checkres else True
        Assertion.assert_equal(checkres, False, "ERR: test default route failed.")

    def test_04_disable_x2_logical_probe(self):
        x2_lb_dict = {
            "name": "X2",
            "probe_condition": "always",
            "probe_type": "physical",
            "rank": 2
        }
        org_wanlb_dict = copy.deepcopy(wlb_conf_dict)
        org_wanlb_dict['failover_lb']['group'][0]['interface'][1] = x2_lb_dict
        res = failoverapi.config_failover_groups_by_multi(**org_wanlb_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 failover lb to invalid ip failed")

    def test_05_traffic_pass_via_new_route(self):
        time.sleep(20)
        (res, packets) = fw_packet_monitor_run(packetmonitorapi, PC1_login, pc_run_dict)
        logger.info(f'packets captured on FW result: {packets}')
        (checkres, packet) = icmp_request_check(packets, PC1_ETH1_IP, Parameter.DNS1)
        logger.info(f'check icmp request forwarded result: {packet}')
        Assertion.assert_equal(checkres, True, "ERR: test new route failed.")

    def test_06_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc48routename)
        Assertion.assert_equal(True, True, "ERR: init failed")


# Except: Importing and Exporting prefs with PBR routes.
class TestPBR_TC28(Test):
    uuid = "SOSAIOT-TC-58684"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']
    tc28routename1 = 'tc28_route_policy01'
    tc28routename2 = 'tc28_route_policy02'

    def test_00_show_testcase_info(self):
        res = show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(res, None, "ERR: show testcase info failed")

    def test_01_add_new_route_policy(self):
        route_base_dict['name'] = self.tc28routename1
        res = routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: Add route policy failed")

    def test_02_export_settings(self):
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export setting failed")

    def test_03_edit_custom_routes(self):
        res = routepolicyapi.del_route_policy_by_name(self.tc28routename1)
        route_base_dict['name'] = self.tc28routename2
        route_base_dict['service'] = {'name': 'HTTP'}
        res &= routepolicyapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(res, True, "ERR: export setting failed")

    def test_04_import_settings(self):
        res = settingapi.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import setting failed")

    def test_05_check_route_policy(self):
        output = routepolicyapi.get_route_policy()
        res = True if self.tc28routename1 in str(output) and \
                      self.tc28routename2 not in str(output) else False
        Assertion.assert_equal(res, True, "ERR: check route policy failed.")

    def test_06_init_route_dict(self):
        route_base_dict.update(org_base_dict)
        routepolicyapi.del_route_policy_by_name(self.tc28routename1)
        Assertion.assert_equal(True, True, "ERR: init failed")
