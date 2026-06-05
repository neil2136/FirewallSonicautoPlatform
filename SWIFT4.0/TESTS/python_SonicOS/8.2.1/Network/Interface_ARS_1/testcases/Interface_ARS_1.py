from definition.init_param import *

class Test_01_Interface_ARS_tc_07(Test):
    uuid = "SOSAIOT-TC-56166"
    description= show_testcase_info(Parameter.TESTPLAN, '1713733', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713733')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_verify_log_when_start_ping_traffic_from_client_to_server(self):
        logger.info('verify log when start ping traffic from client to server...')
        flag = False
        rc = logObj.enable_all_log_category()
        logger.info('set log level as debug...')
        rc &= logObj.logging_level(level='debug')
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        rc = systemlogObj.clear_log()
        logger.info('run cmd in client:{}'.format(cmd))
        rc = local_host.send_command(cmd)
        output = systemlogObj.get_log()
        logger.info(output)
        if re.search(r'ip spoof dropped', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify log when start ping traffic from client to server failed.")

    
    def test__02_config_X3_vlan_on_local_dut(self):
        logger.info('add vlan interface x3 and verify ARS status...')
        flag = False
        x3_vlan = {
            'if': 'X3',
            'type': 'vlan',
            'vlan_tag': vlan_id_X3,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'asymmetric_route': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.del_interface(**x3_vlan)
        rc = interface_obj.add_interface(**x3_vlan)
        output = interface_obj.get_vlan_interface_status(name = 'X3', vlan_id = str(vlan_id_X3))
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X3 ARS failed")

    def test_03_config_X4_vlan_on_local_dut(self):
        logger.info('add vlan interface x4 and verify ARS status...')
        flag = False
        x4_vlan = {
            'if': 'X4',
            'type': 'vlan',
            'vlan_tag': vlan_id_X4,
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'asymmetric_route': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.del_interface(**x4_vlan)
        rc = interface_obj.add_interface(**x4_vlan)
        output = interface_obj.get_vlan_interface_status(name = 'X4', vlan_id = str(vlan_id_X4))
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X4 ARS failed")

    def test_04_verify_log_when_start_ping_traffic_from_client_to_server(self):
        logger.info('verify log when start ping traffic from client to server...')
        flag = False
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        rc = systemlogObj.clear_log()
        logger.info('run cmd in client:{}'.format(cmd))
        output = local_host.send_command(cmd)
        logger.info(output)
        if  not re.search(r'100% packet loss', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify log when start ping traffic from client to server failed.")