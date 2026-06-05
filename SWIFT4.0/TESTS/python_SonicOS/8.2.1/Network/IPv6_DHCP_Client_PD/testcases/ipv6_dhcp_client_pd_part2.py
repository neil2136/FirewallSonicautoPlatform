from definition.settings import *
from definition.utils import *


# Expect: To verify that the requesting router transmits the correct prefix options format
class Test_IPv6_PD_TC101(Test):
    uuid = "SOSAIOT-TC-56475"
    description = show_testcase_info(TESTPLAN, '101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '101')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')
    
    def test_01_config_pkt_mon(self):
        param = {
            'monitor_filter': {
                'ip_types': 'udp',
                'destination_ports': '546,547'
            }
        }
        res = pkt_api.conf_packmon(**param)
        Assertion.assert_equal(res, True, 'ERR: config packet monitor failed.')

    def test_02_set_ipv6_x1_to_dhcpv6(self):
        init_packet_capture()
        x1_v6_dict = {
            'name': 'X1',
            'mode': 'dhcpv6',
            'dhcpv6': {
                # 'prefix_delegation': True,
                'prefix_delegation': {"preferred": {}},
                "mode": "manual",
            },
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res = if_v6_api.config_interface_ipv6(**x1_v6_dict)
        Assertion.assert_equal(res, True, 'set x1 to dhcpv6 mode failed.')

    def test_03_check_x1_v6_addr(self):
        res = False
        time.sleep(60)
        for i in range(3):
            ip_res = check_interface_v6_addr('x1', Parameter.V6_Prefix)
            if ip_res:
                res = True
                break
            if_v6_cli.click_dhcpv6_renew('x1')
            time.sleep(30)
        stop_res = pkt_api.stop_capture()
        logger.info(f'=> stop capture result: {stop_res}')
        Assertion.assert_equal(res, True, 'ERR: x1 get v6 addr failed.')

    def test_04_check_x1_obtained_pd(self):
        CasePara.tsr_msg = diag_api.get_tsr_part(func='Network', lab1='Interfaces')
        res = check_pd_in_tsr(Parameter.X1_PD1, CasePara.tsr_msg)
        Assertion.assert_equal(res, True, 'ERR: x1 obtained pd failed')

    def test_05_verify_solicit_message(self):
        res = False
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c.pcapng -V')
        CasePara.captured_pkts1 = pkts.split('\n\n')
        for pkt in CasePara.captured_pkts1:
            msg_type = get_dhcpv6_packet_type(pkt)
            if msg_type == 'Solicit':
                logger.info('check IA_PD option values'.center(40, '='))
                msg = get_iapd_part_from_packet(pkt)
                if msg:
                    check_list = ['Option: Identity Association for Prefix Delegation (25)', 'Length', 'IAID', 'T1',
                                  'T2']
                    res = all([x in pkt for x in check_list])
                    CasePara.rc_case101 = res
                break
        Assertion.assert_equal(res, True, 'verify Socilit message failed.')

    def test_06_verify_request_message(self):
        res = False
        for pkt in CasePara.captured_pkts1:
            msg_type = get_dhcpv6_packet_type(pkt)
            if msg_type == 'Request':
                logger.info('\n(1)check Server Identifier option in request packet.\n(2)check IA_PD option in request '
                            'packet.')
                msg1 = get_Server_Identifier_part_from_packet(pkt)
                msg2 = get_iapd_part_from_packet(pkt)
                if not msg1 or not msg2:
                    return False
                check_list1 = ['Option: Server Identifier', 'Length', 'DUID']
                check_list2 = ['Option: Identity Association for Prefix Delegation (25)', 'Length',
                               'Value', 'IAID', 'T1', 'T2', 'IA Prefix', 'Option: IA Prefix (26)',
                               'Preferred lifetime', 'Valid lifetime', 'Prefix length', 'Prefix address']
                rc1 = all([x in msg1 for x in check_list1])
                rc2 = all([x in msg2 for x in check_list2])
                res = rc1 and rc2
                break
        Assertion.assert_equal(res, True, 'ERR: verify Request message failed.')


# Expect: When clicking Renew button, the interface should do Solicit process before getting a PD prefix
class Test_IPv6_PD_TC012(Test):
    uuid = "SOSAIOT-TC-56460"
    description = show_testcase_info(TESTPLAN, '012', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '012')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_Solicit_before_renew(self):
        rc = CasePara.rc_case101
        Assertion.assert_equal(rc, True, "ERR: check the Solicit process before getting PD failed!")


# Expect: To verify a DHCP requesting router device properly handles the reception of Reply messages during a basic
# message exchange
class Test_IPv6_PD_TC102(Test):
    uuid = "SOSAIOT-TC-56476"
    description = show_testcase_info(TESTPLAN, '102', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '102')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_Valid_Reply_message_in_response_to_Request(self):
        res = False
        tran_id_req = '0'
        tran_id_rep = '0'
        for pkt in CasePara.captured_pkts1:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Request':
                tran_id_req = get_transaction_id(pkt)
                logger.info(f'request transacation id is {tran_id_req}')
            if pkt_type == 'Reply':
                tran_id_rep = get_transaction_id(pkt)
                logger.info(f'reply transacation id is {tran_id_rep}')
            if tran_id_rep == tran_id_req and tran_id_req != '0':
                res = True
                break
        else:
            if tran_id_req == '0':
                logger.error('get request packet failed.')
            if tran_id_rep == '0':
                logger.error('get reply packet failed.')
            if tran_id_req != tran_id_rep:
                logger.error('get the reply message which response to request failed')
        Assertion.assert_equal(res, True, 'ERR: verify Valid_Reply_message_in_response_to_Request failed.')

    def test_02_capture_renew_and_reply_packets(self):
        init_packet_capture()
        time.sleep(100)
        stop_res = pkt_api.stop_capture()
        logger.info(f'=> stop capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c_2.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c_2.pcapng -V')
        CasePara.captured_pkts2 = pkts.split('\n\n')
        Assertion.assert_equal(True, True, 'ERR: export packets failed')

    def test_03_Valid_Reply_message_in_response_to_a_Renew_message(self):
        res = False
        tran_id_renew = '0'
        tran_id_reply = '0'
        for pkt in CasePara.captured_pkts2:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Renew':
                tran_id_renew = get_transaction_id(pkt)
            if pkt_type == 'Reply':
                tran_id_reply = get_transaction_id(pkt)
            if tran_id_renew == tran_id_reply and tran_id_renew != '0':
                logger.info('get the valid reply message response to renew message.')
                res = True
                break
        else:
            if tran_id_renew == '0':
                logger.error('get renew packet failed.')
            if tran_id_reply == '0':
                logger.error('get reply packet failed.')
            if tran_id_renew != tran_id_reply:
                logger.error('get the valid reply message response to renew message failed')
        Assertion.assert_equal(res, True, 'ERR: verify Valid_Reply_message_in_response_to_a_Renew_message failed.')


# Expect: To verify that the requesting router listens on the correct UDP port and transmits messages to the correct
# DHCP constant address
class Test_IPv6_PD_TC103(Test):
    uuid = "SOSAIOT-TC-56477"
    description = show_testcase_info(TESTPLAN, '103', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '103')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_solicit_dest_addr(self):
        CasePara.solicit_pkt = get_solicit_packet(CasePara.captured_pkts1)
        m = re.findall(r'Dst: ([\w:]+)', CasePara.solicit_pkt, re.M | re.S)
        res = m[1] == 'ff02::1:2' if len(m) >= 2 else False
        Assertion.assert_equal(res, True, 'ERR: verify solicit packet destination address is ff02::1:2 failed')

    def test_02_verfiy_solicit_dest_port(self):
        res = False
        m = re.search(r'Destination port: dhcpv6-server \((\d+)\)', CasePara.solicit_pkt, re.M | re.S)
        if m:
            res = m.group(1) == '547'
        else:
            logger.error('search dest port in solicit packet failed.')
        Assertion.assert_equal(res, True, "ERR: verify solicit packet destination port is 547 failed")


# Expect: To verify that the requesting router transmits a DHCPv6 message with the proper format
class Test_IPv6_PD_TC104(Test):
    uuid = "SOSAIOT-TC-56478"
    description = show_testcase_info(TESTPLAN, '104', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '104')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_Message_Type_ID(self):
        res = False
        if CasePara.solicit_pkt:
            m = re.search(r'Message type: Solicit \((\d+)\)', CasePara.solicit_pkt, re.M | re.S)
            if m:
                res = m.group(1) == '1'
            else:
                logger.error('search Message type id in solicit packet failed.')
        Assertion.assert_equal(res, True, 'ERR: verify Message type id failed')

    def test_02_verify_Transaction_ID(self):
        res = False
        if CasePara.solicit_pkt:
            m = re.search(r'Transaction ID: (\w+)\n', CasePara.solicit_pkt, re.M | re.S)
            if m:
                logger.info(m.group(1))
                res = m.group(1) != '0'
            else:
                logger.error('search Transaction ID in solicit packet failed')
        Assertion.assert_equal(res, True, 'ERR: verify Transaction ID in solicit packet failed.')


# Expect: To verify that the DHCP requesting router transmits the correct Client Identifier Option format
class Test_IPv6_PD_TC105(Test):
    uuid = "SOSAIOT-TC-56479"
    description = show_testcase_info(TESTPLAN, '105', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '105')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_option_code(self):
        res = False
        m = re.search(r'Option: Client Identifier \((\d+)\)', CasePara.solicit_pkt, re.M)
        if m:
            res = m.group(1) == '1'
        else:
            logger.error('search Client Identifier option code failed')
        Assertion.assert_equal(res, True, 'ERR: verify Client Identifier option code is 1 failed.')

    def test_02_verify_option_length(self):
        res = False
        c_id_info = get_Client_Identifier_part_from_packet(CasePara.solicit_pkt)
        if c_id_info:
            m1 = re.search(r'DUID: (\w+)', c_id_info, re.M)
            m2 = re.search(r'Length: (\d+)', c_id_info, re.M)
            if bool(m1) & bool(m2):
                duid = m1.group(1)
                length = m2.group(1)
                res = len(duid) == int(length) * 2
        else:
            logger.error('search DUID value in packet failed')
        Assertion.assert_equal(res, True, 'ERR: verify_option_length set to length of DUID in octets ')

    def test_03_verify_DUID_Field(self):
        res = False
        c_id_info = get_Client_Identifier_part_from_packet(CasePara.solicit_pkt)
        if c_id_info:
            m = re.search(r'DUID: (\w+)', c_id_info, re.M)
            res = m.group(1) != 0
        else:
            logger.error('search DUID value in packet failed')
        Assertion.assert_equal(res, True, 'ERR: verify DUID Field set to any non_zero value failed')


# Expect: To verify that the DHCP requesting router transmits the correct Elapsed Time Option format.
class Test_IPv6_PD_TC107(Test):
    uuid = "SOSAIOT-TC-56480"
    description = show_testcase_info(TESTPLAN, '107', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '107')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_option_code(self):
        res = False
        ela_time_info = get_Elapsed_time_part_from_packet(CasePara.solicit_pkt)
        if ela_time_info:
            m = re.search(r'Option: Elapsed time \((\d+)\)', ela_time_info, re.M)
            if m:
                res = m.group(1) == '8'
            else:
                logger.error('search Elapsed Time option code failed!!')
        Assertion.assert_equal(res, True, "ERR: verify Elapsed Time option code set to 8 failed")

    def test_02_verify_option_length(self):
        res = False
        ela_time_info = get_Elapsed_time_part_from_packet(CasePara.solicit_pkt)
        if ela_time_info:
            m = re.search(r'Length: (\d+)', ela_time_info, re.M)
            if m:
                res = m.group(1) == '2'
            else:
                logger.error('search Elapsed Time option code failed!!')
        Assertion.assert_equal(res, True, "ERR: verify Elapsed Time option length set to 2 failed")

    def test_03_verify_elapsed_time_value(self):
        res = False
        ela_time_info = get_Elapsed_time_part_from_packet(CasePara.solicit_pkt)
        if ela_time_info:
            m = re.search(r'Elapsed-time: (\d+) ms', ela_time_info, re.M)
            if m:
                logger.info(f'get Elapsed-time in packet is {m.group(1)}')
                res = True
            else:
                logger.error('search Elapsed Time value failed!!')
        Assertion.assert_equal(res, True, "ERR: verify Elapsed Time set to number failed")


# Expect: To verify that the DHCP requesting router transmits properly formatted Rebind messages for Prefix Delegation.
class Test_IPv6_PD_TC111(Test):
    uuid = "SOSAIOT-TC-56481"
    description = show_testcase_info(TESTPLAN, '111', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '111')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_packets(self):
        init_packet_capture()
        time.sleep(100)
        stop_res = pkt_api.stop_capture()
        logger.info(f'=> stop capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c_3.pcapng')
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c_3.pcapng -V')
        CasePara.captured_pkts3 = pkts.split('\n\n')
        Assertion.assert_equal(True, True, "ERR: export packets failed")

    def test_02_verify_renew_message(self):
        res = False
        found = 0
        time_list = []
        for pkt in CasePara.captured_pkts3:
            if found == 2:
                break
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Renew':
                found += 1
                p_time = get_packet_captured_time_from_packet(pkt)
                time_list.append(p_time)
        if len(time_list) < 2:
            logger.error('get 2 renew packets failed')
        else:
            res = 51 > float(time_list[1]) - float(time_list[0]) >= 50
        Assertion.assert_equal(res, True, 'ERR: verify renew message delta time failed')

    def test_03_verify_reply_message(self):
        res = False
        for pkt in CasePara.captured_pkts3:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Reply':
                res = 'T1: 50' in pkt and 'T2: 80' in pkt
                break
        Assertion.assert_equal(res, True, 'ERR: verify T1 and T2 value in reply message failed.')


# Expect: To verify that the DHCP requesting router transmits properly formatted Request messages for Prefix Delegation.
class Test_IPv6_PD_TC112(Test):
    uuid = "SOSAIOT-TC-56482"
    description = show_testcase_info(TESTPLAN, '112', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '112')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_request_message(self):
        res = False
        for pkt in CasePara.captured_pkts1:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Request':
                res = f"Prefix address: {Parameter.X1_PD1}" in pkt
                break
        Assertion.assert_equal(res, True, 'ERR: verify Prefix Delegation value in Request message failed.')


# Expect: To verify that the DHCP requesting router properly handles the reception of Advertise messages for Prefix Delegation.
class Test_IPv6_PD_TC114(Test):
    uuid = "SOSAIOT-TC-56484"
    description = show_testcase_info(TESTPLAN, '114', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '114')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_advertise_message(self):
        res = False
        for pkt in CasePara.captured_pkts1:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Advertise':
                res = f"Prefix address: {Parameter.X1_PD1}" in pkt
                break
        Assertion.assert_equal(res, True, 'ERR: verify Prefix Delegation value in Advertise message failed.')


# Expect: To verify that the DHCP requesting router properly handles the reception of Reply messages for Prefix Delegation.
class Test_IPv6_PD_TC115(Test):
    uuid = "SOSAIOT-TC-56485"
    description = show_testcase_info(TESTPLAN, '115', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '115')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_verify_Reply_message(self):
        res = False
        for pkt in CasePara.captured_pkts1:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Reply':
                iapd_msg = get_iapd_part_from_packet(pkt)
                res = 'T1: 50' in pkt and 'T2: 80' in iapd_msg
                break
        Assertion.assert_equal(res, True, 'ERR: verify Prefix Delegation value in Advertise message failed.')


# Expect: To verify that the DHCP requesting router transmits properly formatted Release messages for Prefix Delegation.
class Test_IPv6_PD_TC113(Test):
    uuid = "SOSAIOT-TC-56483"
    description = show_testcase_info(TESTPLAN, '113', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '113')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_packets(self):
        init_packet_capture()
        if_v6_cli.click_dhcpv6_release('x1')
        time.sleep(60)
        stop_res = pkt_api.stop_capture()
        logger.info(f'=> stop capture result: {stop_res}')
        pkt_api.export_captured_packets_pcapng('/tmp/packet-c_4.pcapng')
        Assertion.assert_equal(True, True, 'ERR: export packets failed.')

    def test_02_verify_release_message(self):
        res = False
        pkts = pc1_login.send_command('tshark -r /tmp/packet-c_4.pcapng -V')
        pkt_list = pkts.strip().split('\n\n')
        for pkt in pkt_list:
            pkt_type = get_dhcpv6_packet_type(pkt)
            if pkt_type == 'Release':
                iapd_msg = get_iapd_part_from_packet(pkt)
                res = f"Prefix address: {Parameter.X1_PD1}" in iapd_msg
                break
        else:
            logger.error('find Release packet failed.')
        Assertion.assert_equal(res, True, 'ERR: verify Prefix Delegation value in Advertise message failed.')
