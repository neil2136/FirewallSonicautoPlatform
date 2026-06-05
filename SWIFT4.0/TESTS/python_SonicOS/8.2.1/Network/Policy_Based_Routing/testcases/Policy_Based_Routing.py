from definition.initial_parameter import *


class TestStaticFounction(Test):
    @staticmethod
    def _start_packet_monitor():
        result = packet_obj.stop_capture()
        time.sleep(2)
        result += packet_obj.clear_packets()
        time.sleep(3)
        result += packet_obj.start_capture()
        time.sleep(2)
        if result == 3:
            return True
        else:
            return False


class TestPolicyBasedRouting_12(Test):
    uuid = '1524889'
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Add_New_Route_Policy(self):
        time.sleep(5)
        route_policy = Parameter.default_route_policy_json 
        rc = route_policy_obj.add_route_policy(**route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add route policy failed")

    def test_02_Send_Traffic_On_PC1_And_Verify_Function_Of_New_Added_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        os.popen('ping www.baidu.com -c 10').read()
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.')
            logger.info(ret)
            rc = False
        # if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.')
            # logger.info(ret)
            # rc = False
        Assertion.assert_equal(rc, True, "ERR: Verify Function Of New Added Route Policy Failed.")

    def test_03_Delete_Route_Policy(self):
        rc = route_policy_obj.del_route_policy_by_name('route_policy_tc12')
        Assertion.assert_equal(rc, True, "ERR: Delete route policy failed")

    def test_04_Send_Traffic_On_PC1_And_Verify_The_Function_Without_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        os.popen('ping www.baidu.com -c 10').read()
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Traffic Should Not Go Through Interface X2, Check Packet Monitor Info Failed:\n' + ret)
            rc = False        
        if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.') 
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Verify Function Without Route Policy Failed.")


class TestPolicyBasedRouting_17(Test):
    uuid = '1524917'
    description= show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Add_New_Route_Policy(self):
        route_policy = Parameter.default_route_policy_json
        route_policy['route_policies'][0]['ipv4']['service'] = {'name': 'FTP'}
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc17"
        rc = route_policy_obj.add_route_policy(**route_policy)
        route_policy['route_policies'][0]['ipv4']['service'] = {'group': 'Ping'}
        Assertion.assert_equal(rc, True, "ERR: Add route policy failed")

    def test_02_Add_Custom_Address_Object(self):
        ao_param ={
            "object_type": "network",
            "name": "tc17_source_ao",
            "zone": "LAN",
            "value": "192.168.168.0,255.255.255.0"
        }
        rc = address_obj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Object")

    def test_03_Edit_Route_Policy(self):
        route_policy = Parameter.default_route_policy_json
        route_policy['route_policies'][0]['ipv4']['source'] = {"name": "tc17_source_ao"}
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc17"
        rc = route_policy_obj.edit_route_policy('route_policy_tc17', **route_policy)
        route_policy['route_policies'][0]['ipv4']['source'] = {"any": True}
        Assertion.assert_equal(rc, True, "ERR: Edit route policy failed")

    def test_04_Verify_Parameters_Of_Edited_Route_Policy(self):
        MYFLAG = 0
        rc = route_policy_obj.get_route_policy_by_name('route_policy_tc17')
        if rc['route_policies'][0]['ipv4']['source']['name'] == "tc17_source_ao":
            logger.info('AO is right.')
            MYFLAG += 1
        else:
            logger.info('AO is not right.')
        if rc['route_policies'][0]['ipv4']['service']['group'] == "Ping":
            logger.info('Service is right.')
            MYFLAG += 1
        else:
            logger.info('Service is not right.')
        Assertion.assert_equal(MYFLAG, 2, "ERR: Verify Parameters Of Edited Route Policy Failed.")

    def test_05_Send_Traffic_On_PC1_And_Verify_Function_Of_Edited_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        os.popen('ping www.baidu.com -c 10').read()
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        # if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        Assertion.assert_equal(rc, True, "ERR: Verify Function Of Edited Route Policy Failed.")

    def test_06_Restore(self):
        rc = route_policy_obj.del_route_policy_by_name('route_policy_tc17')
        rc += address_obj.delete_addressobject('network', object_path='name', object_name_uuid='tc17_source_ao', ip_type='ipv4')
        Assertion.assert_equal(rc, 2, "ERR: Restore Failed") 


class TestPolicyBasedRouting_23(Test):
    uuid = '1524896'
    description= show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Address_Object(self):
        ao_param ={
            "object_type": "host",
            "name": "PC1_ETH1",
            "zone": "LAN",
            "value": PC1_ETH1_IP
        }
        ao_param_1 ={
            "object_type": "host",
            "name": "PC3_ETH1",
            "zone": "LAN",
            "value": PC3_ETH1_IP
        }
        rc = address_obj.config_addressobject(**ao_param)
        rc += address_obj.config_addressobject(**ao_param_1)
        Assertion.assert_equal(rc, 2, "ERR: Failed To Add Address Object")

    def test_02_Add_New_Route_Policy(self): 
        route_policy = Parameter.default_route_policy_json
        route_policy['route_policies'][0]['ipv4']['source'] = {"name": "PC1_ETH1"}
        route_policy['route_policies'][0]['ipv4']['service'] = {'name': 'HTTP'}
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc23_1st"
        rc = route_policy_obj.add_route_policy(**route_policy)
        route_policy['route_policies'][0]['ipv4']['interface'] = 'X3'
        route_policy['route_policies'][0]['ipv4']['source'] = {"name": "PC3_ETH1"}
        route_policy['route_policies'][0]['ipv4']['service'] = {'name': 'HTTP'}
        route_policy['route_policies'][0]['ipv4']['gateway'] = {'name': 'X3 Default Gateway'}
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc23_2nd"
        rc += route_policy_obj.add_route_policy(**route_policy)
        route_policy['route_policies'][0]['ipv4']['source'] = {"name": "PC1_ETH1"}
        route_policy['route_policies'][0]['ipv4']['service'] = {'name': 'FTP'}
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc23_3rd"
        rc += route_policy_obj.add_route_policy(**route_policy)
        route_policy['route_policies'][0]['ipv4']['interface'] = 'X2'
        route_policy['route_policies'][0]['ipv4']['source'] = {"any": True}
        route_policy['route_policies'][0]['ipv4']['service'] = {'group': 'Ping'}
        route_policy['route_policies'][0]['ipv4']['gateway'] = {'name': 'X2 Default Gateway'}
        Assertion.assert_equal(rc, 3, "ERR: Add route policy failed")

    def test_03_Simulate_HTTP_Access_On_PC1_And_Verify_1st_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        response = requests.get('http://www.baidu.com')
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.\n' + ret)
            rc = False
        if re.search('in:X0\*\(interface\), out:X3', str(ret), re.I):
            logger.info('Traffic Should Not Go Through Interface X3, Check Packet Monitor Info Failed.\n' + ret)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify Function Of 1st Route Policy.")

    def test_04_Simulate_HTTP_Access_On_PC3_And_Verify_2nd_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        ret = PC3_login.send_command( "python3 " + Parameter.FILE_PATH_TEST_HTTP )
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X3', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        # if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        # if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X2, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify Function Of 2nd Route Policy.")

    def test_05_Simulate_FTP_Access_On_PC1_And_Verify_3rd_Route_Policy(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        #ftp_request.urlopen('ftp://gcc.gnu.org')#if access Vcenter FTP server, trafic would go through PC1_ETH0
        import ftplib
        try:
            f = ftplib.FTP('gcc.gnu.org')
            f.login('root', 'password')
        except Exception:
            pass
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X3', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        # if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        # if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X2, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify Function Of 3rd Route Policy.")

    def test_06_Restore(self):
        rc = route_policy_obj.del_route_policy_by_name('route_policy_tc23_1st')
        rc += route_policy_obj.del_route_policy_by_name('route_policy_tc23_2nd')
        rc += route_policy_obj.del_route_policy_by_name('route_policy_tc23_3rd')
        rc += address_obj.delete_addressobject('host', object_path='name', object_name_uuid='PC1_ETH1', ip_type='ipv4')
        rc += address_obj.delete_addressobject('host', object_path='name', object_name_uuid='PC3_ETH1', ip_type='ipv4')
        Assertion.assert_equal(rc, 5, "ERR: Restore Failed")


class TestPolicyBasedRouting_27(Test):
    uuid = '1524899'
    description= show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        rc = show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(rc, None, "ERR: show testcase info failed")

    def test_01_Create_Unreachable_Address_Object(self):
        ao_param ={
            "object_type": "host",
            "name": "unreachable_address_object",
            "zone": "WLAN",
            "value": "3.3.3.3"
        }
        rc = address_obj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add WLAN Host Address Object")

    def test_02_Add_Probe(self):
        nm_param_alive={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": "tc27_probe_alive",
                        'probe': {'target': {'name': 'X2 Default Gateway'}, 'type': {'ping': 'non-explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        "comment": ""
                    }
                }
            }]
        }
        nm_param_offline={
            "network_monitors": [{
                "policy": {
                    "ipv4": {
                        "name": "tc27_probe_offline",
                        'probe': {'target': {'name': 'unreachable_address_object'}, 'type': {'ping': 'non-explicit'}, 'interval': 5},
                        'reply_timeout': 1,
                        'interval': {'missed': 3, 'successful': 3},
                        'must_respond': False,
                        "comment": ""
                    }
                }
            }]
        }
        rc = network_monitor_obj.add_network_monitor(**nm_param_alive)
        rc += network_monitor_obj.add_network_monitor(**nm_param_offline)
        Assertion.assert_equal(rc, 2, "ERR: Failed To Add Probe") 

    def test_03_Add_New_Route_Policy_With_Alive_Probe(self):
        route_policy = Parameter.route_policy_json_with_probe
        route_policy['route_policies'][0]['ipv4']['probe'] = "tc27_probe_alive"
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc27" 
        rc = route_policy_obj.add_route_policy(**route_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policy With Alive Probe")  

    def test_04_Send_Traffic_On_PC1_And_Verify_Function_Of_Route_Policy_Probe_Alive(self):
        rc = False
        time.sleep(30)
        TestStaticFounction._start_packet_monitor()
        os.popen('ping www.baidu.com -c 20').read()
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.')
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        # if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            # logger.info('Traffic Should Not Go Through Interface X1, Check Packet Monitor Info Failed.\n' + ret)
            # rc = False
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify Function Of Route Policy Probe Alive.")

    def test_05_Edit_Route_Policy_With_Probe_Offline(self):
        route_policy = Parameter.route_policy_json_with_probe
        route_policy['route_policies'][0]['ipv4']['probe'] = "tc27_probe_offline"
        route_policy['route_policies'][0]['ipv4']['name'] = "route_policy_tc27"  
        rc = route_policy_obj.edit_route_policy('route_policy_tc27', **route_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed To Edit Route Policy With Probe Offline")

    def test_06_Send_Traffic_On_PC1_And_Verify_Function_Of_Route_Policy_Probe_Offline(self):
        rc = False
        TestStaticFounction._start_packet_monitor()
        os.popen('ping www.baidu.com -c 10').read()
        packet_obj.stop_capture()
        ret = packet_obj.export_captured_packets()
        if re.search('in:X0\*\(interface\), out:X2', str(ret), re.I):
            logger.info('Traffic Should Not Go Through Interface X2, Check Packet Monitor Info Failed.\n' + ret)
            rc = False
        if re.search('in:X0\*\(interface\), out:X1', str(ret), re.I):
            logger.info('Check Packet Monitor Info Successful.') 
            rc = True
        else:
            logger.error('Error: Could not Found Target Info.\n' + ret)
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Failed Verify Function Of Route Policy Probe Offline.")

    def test_07_Restore(self):
        rc = route_policy_obj.del_route_policy_by_name('route_policy_tc27')
        rc += network_monitor_obj.del_network_monitor("tc27_probe_alive")
        rc += network_monitor_obj.del_network_monitor("tc27_probe_offline")
        rc += address_obj.delete_addressobject('host', object_path='name', object_name_uuid='unreachable_address_object', ip_type='ipv4')
        Assertion.assert_equal(rc, 4, "ERR: Restore Failed")
