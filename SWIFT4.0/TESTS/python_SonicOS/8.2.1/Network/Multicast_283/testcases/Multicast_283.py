from definition.settings import *

class Test_12_Multicast_IGMP_State_Table_Timeout_Working_Properly(Test):
    uuid = "SOSAIOT-TC-52908"
    description = '''This test ensures that IGMP State Table entries time out working properly.'''

    def test_12_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_12_Step02_Send_IGMPv3_Membership_Report_on_X0_and_Verify_IGMP_State_Table(self):
        cmd = "sendip -d '0x2200efe90000000104000000e00a0a0a' " + \
              "-p ipv4 -ip 02 -is {} -it 1 -id 224.0.0.22 224.0.0.22".format(LAN_PC)
        logger.info(cmd)
        os.popen(cmd)
        time.sleep(5)
        logger.info("Check IGMP state table")
        output = multicast_api.show_state_table()
        # # #[
        # # #    {
        # # #       'multicast_group_address': '224.10.10.10',
        # # #       'interface_vpn_tunnel': 'X0',
        # # #       'igmp_version': 'V3',
        # # #       'time_remaining': '20 minute 53 second'
        # # #   }
        # # #]
        rc = False
        if not output:
            logger.error("Get IGMP stat table failed.")
            Assertion.fail("ERR: Check state table failed")
        for item in output:
            if item['multicast_group_address'] == MULTICAST_IP:
                if item['igmp_version'].lower() == 'v3':
                    rc = True
        Assertion.assert_equal(rc, True, "ERR: Check state table failed")

    def test_12_Step03_Keep_FW_Idle_until_Timeout_and_Verify_no_entry_for_X0_in_IGMP_State_Table(self):
        time.sleep(61)
        logger.info("Check IGMP state table after timeout")
        output = multicast_api.show_state_table()
        # # #[
        # # #    {
        # # #        'multicast_group_address': '224.10.10.10',
        # # #        'interface_vpn_tunnel': 'X0',
        # # #        'igmp_version': 'V3',
        # # #        'time_remaining': 'Time EXPIRED'
        # # #    }
        # # #]
        rc = True
        if len(output) > 0:
            if output[0]['time_remaining'] == 'Time EXPIRED':
                logger.info("Item is still shown but time expired.")
            else:
                logger.error("There is still item in state table.")
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Check state table failed")


class Test_16_Disable_Multicast_at_Multicast_Page_Disable_All_Multicast_Data_Reception(Test):
    uuid = "SOSAIOT-TC-52909"
    description = '''This test ensures that globally disabling multicast disables multicast 
                     reception/forwarding on interfaces and VPN tunnel.'''

    def test_16_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_16_Step02_Server_on_X1_and_Client_on_X0_X3_Check_Client_Sends_IGMP_Join_and_Receive_Multicast(self):
        cmd = "sendip -d '0x2200efe90000000104000000e00a0a0a' " + \
              "-p ipv4 -ip 02 -is {} -it 1 -id 224.0.0.22 224.0.0.22".format(DMZ_PC)
        logger.info(cmd)
        os.popen(cmd)

        cmd = "nohup python3 {}/definition/server.py &".format(TESTPATH)
        os.system("python3 {}/definition/run_server.py -ip {} -c \"{}\"".format(TESTPATH, WAN_HOST_IP, cmd))
        logger.info("Server is running")

        out1 = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        logger.info(out1)
        out2 = DMZ_HOST.send_command("python3 {}/definition/client.py".format(TESTPATH))
        logger.info(out2)

        rc = 0
        if 'TEST PASS' in out1:
            logger.info("LAN part test passed.")
            rc += 1
        if 'TEST PASS' in out2:
            logger.info("DMZ part test passed.")
            rc += 1
        Assertion.assert_equal(rc, 2, "ERR: Test on X0 and X3 failed")

    def test_16_Step03_Disable_Multicast_and_Check_Client_Not_Receive_Multicast_Packet(self):
        logger.info("Disable multicast")
        multicast_conf = { 'multicast': False, }
        res = multicast_api.config_multicast(**multicast_conf)

        out1 = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        out2 = DMZ_HOST.send_command("python3 {}/definition/client.py".format(TESTPATH))
        rc = 0
        if 'TEST PASS' in out1:
            logger.info("LAN part got multicast.")
            rc += 1
        if 'TEST PASS' in out2:
            logger.info("DMZ part got multicast.")
            rc += 1

        multicast_conf = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 1,
            'reception_name': multicast_obj["name"],
        }
        res &= multicast_api.config_multicast(**multicast_conf)

        result = False
        if res and rc == 0:
            result = True

        Assertion.assert_equal(result, True, "ERR: Test on X0 and X3 failed")


class Test_17_Disable_Multicast_on_Interface_Disable_Multicast_Reception_on_Interface(Test):
    uuid = "SOSAIOT-TC-52910"
    description = '''This test ensures that Disabling multicast on a particular interface works'''

    def test_17_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_Step02_Server_on_X1_and_Client_on_X0_Check_Client_Sends_IGMP_Join_and_Receive_Multicast(self):
        out = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        rc = 0
        if 'TEST PASS' in out:
            logger.info("LAN part test passed.")
            rc += 1
        Assertion.assert_equal(rc, 1, "ERR: Test on X0 failed")

    def test_17_Step03_Disable_Multicast_on_X0_and_X1_and_Check_Client_not_Receive_Any_Multicast_Spacket(self):
        logger.info("Disable multicast")
        x0_static = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': FIREWALL,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
            'multicast': False
        }
        res = interface_api.config_interface(**x0_static)

        out = os.popen("python3 {}/definition/client.py".format(TESTPATH)).read()
        rc = 0
        if 'TEST PASS' in out:
            logger.info("LAN part got multicast.")
            rc += 1

        x0_static = {
            'if': 'X0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': FIREWALL,
            'netmask': MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
            'multicast': True
        }
        res &= interface_api.config_interface(**x0_static)

        result = False
        if res and rc == 0:
            result = True

        Assertion.assert_equal(result, True, "ERR: Test on X0 failed")

