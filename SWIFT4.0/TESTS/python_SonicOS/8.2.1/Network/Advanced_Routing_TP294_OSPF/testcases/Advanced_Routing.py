from definition.settings import *
from definition.utils import *


# Verify that SonicWALL doesn't send any OSPF packets when the OSPF feature is disabled
class TestOSPF_TC88(Test):
    uuid = "SOSAIOT-TC-55733"
    description = show_testcase_info(TESTPLAN, 'OSPF_TC88', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'OSPF_TC88')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_ospf_must_disable_in_x3(self):
        output = dynaroutingapi.get_route_list_in_type(rtype='ospfv2')
        Assertion.assert_not_regular(str(output), 'OSPF Enabled', "ERR: check ospf must disable failed")

    def test_04_check_ospf_packets_not_in_fw_captures(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info('wait for 40s to capture fw packets...')
        time.sleep(40)
        packetmonitorapi.export_captured_packets_pcapng()
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        Assertion.assert_not_regular(packets, 'OSPF Packet Header', "ERR: check ospf packets not in fw failed")


#  Verify that Hello packets are sent every Hello Interval seconds to the IP multicast address (224.0.0.5).
class TestInterval_TC89(Test):
    uuid = "SOSAIOT-TC-55734"
    description = show_testcase_info(TESTPLAN, 'Interval_TC89', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Interval_TC89')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_packet_monitor_only_ospf(self):
        packer_monitor_config = {
            'monitor_filter': {
                'ip_types': 'ospf',
                'ether_types': '!0x69,!0x806,!0x6a',
            }
        }
        output = packetmonitorapi.conf_packmon(**packer_monitor_config)
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        Assertion.assert_equal(
            output, True, "ERR: Config packet monitor failed")

    def test_02_init_connected_networks_metric(self):
        ospf_dict = {
            'router_id': '10.0.0.10',
        }
        output = dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: init OSPF Connected Networks Metric failed")

    def test_03_configure_ospf_interval_to_10_for_x3_and_x2(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'hello_interval': CaseParams.interval_time})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3', 'mode': 'enable'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_04_check_ospf_interval_is_10_in_fw_captures(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info(f'wait for {CaseParams.interval_time}s to capture fw packets...')

        time.sleep(int(CaseParams.interval_time)-3)
        packetmonitorapi.export_captured_packets_pcapng()
        ospf_packet_filter = {
            'Protocol': 'Protocol: OSPF',
            'Destination': 'Destination: 224.0.0.5',
            'Area ID': 'Area ID: 0.0.0.112',
            'Hello Interval': f'Hello Interval: {CaseParams.interval_time} seconds',
            'Message Type': 'Message Type: Hello Packet',
        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        x2res, x3res = check_interval_packets(packets, ospf_packet_filter.values())
        res = True if x2res == 1 and x3res == 1 else False
        # if not res:
        #     time.sleep(10)
        Assertion.assert_equal(res, True, f"ERR: check ospf interval is {CaseParams.interval_time} failed")

    def test_05_configure_ospf_interval_to_25_for_x3_and_x2(self):
        CaseParams.interval_time = '25'
        self.test_03_configure_ospf_interval_to_10_for_x3_and_x2()

    def test_06_check_ospf_interval_is_25_in_fw_captures(self):
        CaseParams.interval_time = '25'
        self.test_04_check_ospf_interval_is_10_in_fw_captures()

    def test_07_init_ospf_configure(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'hello_interval': '10', 'mode': 'disable'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, f"ERR:init ospf configure failed")


# Verify that SonicWALL doesn't declare a DR or DBR in its Hello packets before the Wait timer reaches Dead Interval
class TestDeclare_TC90(Test):
    uuid = "SOSAIOT-TC-55736"
    description = show_testcase_info(TESTPLAN, 'Declare_TC90', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'Declare_TC90')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ospf_in_fws(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_02_check_ospf_declare_10s_in_fw_captures(self):
        logger.info(f'wait for 10s to capture fw packets...')
        # -2s is ospf configure time
        time.sleep(8)
        packetmonitorapi.export_captured_packets_pcapng()
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        Assertion.assert_not_regular(packets, 'OSPF DB Description', f"ERR: check ospf declare failed")

    def test_03_disable_ospf_in_fws(self):
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'mode': 'disable'})
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: disable ospf failed")


# Verify that disabled router disappears from SonicWALLs neighbour list after Dead Interval expires
class TestDeadInterval_TC91(Test):
    uuid = "SOSAIOT-TC-55737"
    description = show_testcase_info(TESTPLAN, 'DeadInterval_TC91', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DeadInterval_TC91')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_02_check_ospf_in_neighbor_list(self):
        logger.info(f'wait for 60s to check neighbor list...')
        time.sleep(60)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf neighbor list failed")

    def test_03_disable_ospf_in_remote_fw(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'mode': 'disable'})
        output = r_dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: disable remote ospf failed")

    def test_04_check_ospf_not_neighbor_list(self):
        logger.info(f'wait for 40s to check neighbor list...')
        time.sleep(40)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_not_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf establish neighbor failed")

    def test_05_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that if a Router Priority is set to 0, the SonicWALL is not eligible to become a DR.
class TestRouterPrior_TC93(Test):
    uuid = "SOSAIOT-TC-55738"
    description = show_testcase_info(TESTPLAN, 'RouterPrior_TC93', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RouterPrior_TC93')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_ospf_router_priority_to_0_in_fws(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'router_priority': '0'})
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    def test_02_check_ospf_not_dr_in_fw_captures(self):
        logger.info(f'wait for 60s to capture fw packets...')
        # -2s is ospf configure time
        time.sleep(58)
        packetmonitorapi.export_captured_packets_pcapng()
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])

        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_not_regular(packets, 'OSPF DB Description', f"ERR: check ospf declare failed")

    def test_03_check_ospf_status_is_2way(self):
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_regular(output, '2-Way', f"ERR: check ospf status is 2-Wan failed")

    def test_04_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that the Hello packet is dropped and a sender is not accepted as a neighbor if there is Hello mismatch.
class TestHelloMismatch_TC96(Test):
    uuid = "SOSAIOT-TC-55739"
    description = show_testcase_info(TESTPLAN, 'HelloMismatch_TC96', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'HelloMismatch_TC96')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_ospf_router_priority_to_0_in_fws(self):
        CaseParams.interval_time = '5'
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X3'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X2', 'hello_interval': CaseParams.interval_time})
        output2 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_02_check_ospf_hello_message_in_fw(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info(f'wait for {CaseParams.interval_time}s to capture fw packets...')
        time.sleep(int(CaseParams.interval_time))
        packetmonitorapi.export_captured_packets_pcapng()
        ospf_packet_filter = {
            'Source': f'Source: {Parameter.REMOTE_X2_IP}',
            'Protocol': 'Protocol: OSPF',
            'Destination': 'Destination: 224.0.0.5',
            'Hello Interval': f'Hello Interval: {CaseParams.interval_time} seconds',
            'Message Type': 'Message Type: Hello Packet',
        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, ospf_packet_filter.values())
        if not res:
            time.sleep(10)
        Assertion.assert_equal(res, True, f"ERR: check ospf hello message failed")

    @repeat_method(5)
    def test_03_check_ospf_neighbor_list_is_empty(self):
        logger.info('wait for 10s to check neighbor list...')
        time.sleep(10)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_not_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf establish neighbor failed")

    def test_04_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that if an incoming OSPF packet is not from a local network,
# SonicWALL should not list a sender as a neighbor in its Hello packets.
class TestDiffIP_TC97(Test):
    uuid = "SOSAIOT-TC-55740"
    description = show_testcase_info(TESTPLAN, 'DiffIP_TC97', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'DiffIP_TC97')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_x3_ip_in_fw(self):
        lan_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': "28.1.1.46",
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        res = interfaceapi.config_interface(**lan_dict)
        Assertion.assert_equal(res, True, "ERR: Config X2 to static failed")

    def test_02_enable_ospf_in_fws(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X3'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X2'})
        output2 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    def test_03_check_ospf_hello_message_in_fw(self):
        CaseParams.interval_time = '10'
        TestHelloMismatch_TC96().test_02_check_ospf_hello_message_in_fw()

    def test_04_check_ospf_neighbor_list_is_empty(self):
        logger.info('wait for 50s to check neigbor list...')
        time.sleep(40)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_not_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf establish neighbor failed")

    def test_05_disable_ospf_in_fws(self):
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'mode': 'disable'})
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        output3 = interfaceapi.config_interface(**x3_lan_dict)
        Assertion.assert_equal(output1 & output2 & output3, True, "ERR: disable ospf failed")


# Verify that the E bit of the Options field in a Hello packet is set if the attached area is not a stub area.
class TestEBit_TC98(Test):
    uuid = "SOSAIOT-TC-55741"
    description = show_testcase_info(TESTPLAN, 'EBit_TC98', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'EBit_TC98')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X3'})
        output = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_02_check_hello_exist_ebit_in_fw(self):
        output = False
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info(f'wait for 10s to capture fw packets...')
        time.sleep(10)
        packetmonitorapi.export_captured_packets_pcapng()
        ospf_packet_filter = {
            'Source': f'Source: {Parameter.X3_IP}',
            'Protocol': 'Protocol: OSPF',
            'Destination': 'Destination: 224.0.0.5',
            'Message Type': 'Message Type: Hello Packet',
        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, ospf_packet_filter.values())
        if res:
            if '1. = E: External Routing Capability' in packet:
                logger.info('check E bit is 1 successful.')
                output = True
        else:
            time.sleep(10)
        Assertion.assert_equal(output, True, f"ERR: check hello exist E bit failed")

    def test_03_change_ospf_area_to_stub_in_fw(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X3', 'area_type': 'stub area'})
        output = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_04_check_hello_not_exist_ebit_in_fw(self):
        output = False
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info(f'wait for 10s to capture fw packets...')
        time.sleep(10)
        packetmonitorapi.export_captured_packets_pcapng()
        ospf_packet_filter = {
            'Source': f'Source: {Parameter.X3_IP}',
            'Protocol': 'Protocol: OSPF',
            'Destination': 'Destination: 224.0.0.5',
            'Message Type': 'Message Type: Hello Packet',
        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, ospf_packet_filter.values())
        if res:
            if '0. = E: NO External Routing Capability' in packet:
                logger.info('check E bit is 0 successful.')
                output = True
        else:
            time.sleep(10)
        Assertion.assert_equal(output, True, f"ERR: check hello not exist E bit failed")

    def test_05_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that Master/Slave is properly negotiated if SonicWALL has a lower Router ID than the other router.
class TestMasterSlave_TC101(Test):
    uuid = "SOSAIOT-TC-55644"
    description = show_testcase_info(TESTPLAN, 'MasterSlave_TC101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MasterSlave_TC101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_ospf_configure(self):
        ospf_dict = {'router_id': Parameter.X3_IP}
        output1 = dynaroutingapi.ospf2_config(**ospf_dict)
        ospf_dict = {'router_id': Parameter.REMOTE_X2_IP}
        output2 = r_dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: set ospf configure failed")

    def test_02_enable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    def test_03_check_defferent_dd_sequence_number_between_fws(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        logger.info(f'wait for 60s to capture fw packets...')
        time.sleep(60)
        packetmonitorapi.export_captured_packets_pcapng()
        dd_filter = {
            'Source': f'Source: {Parameter.X3_IP}',
            'Destination': f'Destination: {Parameter.REMOTE_X2_IP}',
            'Protocol': 'Protocol: OSPF',
            'Message Type': 'Message Type: DB Description',
            'MS bit': '1 = MS: Master/Slave bit is SET'
        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, dd_filter.values())
        if res:
            fwres = re.findall('(?<=DD Sequence: )\S+', packet, re.I)
            logger.info(f'check fw sequence result: {fwres}')
            if fwres:
                CaseParams.fw_sequence = int(fwres[0])
        else:
            logger.info(f'can not find dd packet in fw captures send fw')

        dd_filter.update(
            {'Source': f'Source: {Parameter.REMOTE_X2_IP}',
             'Destination': f'Destination: {Parameter.X3_IP}'})
        res, packet = check_pcapng_packets(packets, dd_filter.values())
        if res:
            routerres = re.findall('(?<=DD Sequence: )\S+', packet, re.I)
            logger.info(f'check router sequence result: {routerres}')
            if routerres:
                CaseParams.router_sequence = int(routerres[0])
        else:
            logger.info(f'can not find dd packet in fw captures, send router')
        Assertion.assert_not_equal(CaseParams.fw_sequence,
                                   CaseParams.router_sequence,
                                   f"ERR: check different DD sequence number in fws failed")

    def test_04_check_fw_becomes_slave_in_same_sequence(self):
        dd_filter = {
            'Source': f'Source: {Parameter.X3_IP}',
            'Destination': f'Destination: {Parameter.REMOTE_X2_IP}',
            'Protocol': 'Protocol: OSPF',
            'Message Type': 'Message Type: DB Description',
            'DD Sequence': f'DD Sequence: {CaseParams.router_sequence}',
            'MS bit': '0 = MS: Master/Slave bit is NOT set'

        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, dd_filter.values())
        Assertion.assert_equal(res, True, "ERR: check sonicwall becomes slave failed")

    def test_05_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that Master/Slave is properly negotiated if SonicWALL has a higher Router ID than the other router.
class TestMasterSlave_TC102(Test):
    uuid = "SOSAIOT-TC-55645"
    description = show_testcase_info(TESTPLAN, 'MasterSlave_TC102', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'MasterSlave_TC102')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_ospf_configure(self):
        ospf_dict = {'router_id': Parameter.REMOTE_X2_IP}
        output1 = dynaroutingapi.ospf2_config(**ospf_dict)
        ospf_dict = {'router_id': Parameter.X3_IP}
        output2 = r_dynaroutingapi.ospf2_config(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: set ospf configure failed")

    def test_02_enable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    def test_03_check_defferent_dd_sequence_number_between_fws(self):
        TestMasterSlave_TC101().test_03_check_defferent_dd_sequence_number_between_fws()

    def test_04_check_router_becomes_slave_in_same_sequence(self):
        dd_filter = {
            'Source': f'Source: {Parameter.REMOTE_X2_IP}',
            'Destination': f'Destination: {Parameter.X3_IP}',
            'Protocol': 'Protocol: OSPF',
            'Message Type': 'Message Type: DB Description',
            'DD Sequence': f'DD Sequence: {CaseParams.fw_sequence}',
            'MS bit': '0 = MS: Master/Slave bit is NOT set'

        }
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        res, packet = check_pcapng_packets(packets, dd_filter.values())
        Assertion.assert_equal(res, True, "ERR: check router becomes slave failed")

    def test_05_disable_ospf_in_fws(self):
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# Verify that the interfaces involved in Transparent mode do not allow RIP or OSPF to be enabled
# note: in transpart mode still configrue ospf, but it will auto enable wan interface ospf and use it.
class TestTransMode_TC125(Test):
    uuid = "SOSAIOT-TC-55661"
    description = show_testcase_info(TESTPLAN, 'TransMode_TC125', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'TransMode_TC125')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_change_X5_to_LAN_zone(self):
        ao_dict = {
            "object_type": "range",
            "name": CaseParams.x1_sub_range,
            "zone": "LAN",
            "value": '12.12.1.200,12.12.1.220'
        }
        (res1, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
        if res1 is False:
            res1 = True if 'Already exists'.lower() in str(aomsg).lower() else False

        x5_transparent_dict = {
            'if': 'X5',
            'comment': 'auto_transmode',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'name': CaseParams.x1_sub_range},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True
        }
        res2 = interfaceapi.config_interface(**x5_transparent_dict)
        Assertion.assert_equal(res1 & res2, True, "ERR: change x5 to lan zone failed")

    def test_02_enable_ospf_in_x5(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X5'})
        output = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output, True, "ERR: enable ospf in x5 failed")

    def test_03_check_x5_configure_must_enable_ospf_in_x1(self):
        res = False
        output = dynaroutingapi.get_route_list_in_type(rtype='ospfv2')
        try:
            convres = str_2_csv(text=str(output))
            for convents in convres:
                logger.info(convents)
                if 'X1' in convents and 'OSPF Enabled' in convents:
                    logger.info('check X1 must ospf enable success.')
                    res = True
                    break
            else:
                logger.info('can not march interface and ospf status failed.')
        except Exception as e:
            logger.info(repr(e))
        Assertion.assert_equal(res, True, "ERR: check x5 configure must enable x1 ospf failed")

    def test_04_disable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': 'X5', 'mode': 'disable'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X1'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        output3 = interfaceapi.unassign_interface(interface='X5')
        Assertion.assert_equal(output1 & output2 & output3, True, "ERR: disable ospf failed")


# Verify the PBR's parameter(gateway/destination/interface) changes can be updated to nsm and can be restributed to the neighbo
class TestNSM_TC153(Test):
    uuid = "SOSAIOT-TC-55667"
    description = show_testcase_info(TESTPLAN, 'NSM_TC153', description=True)['title']
    ao_network = CaseParams.external_network2
    modify_ao_network = '99.1.1.0'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'NSM_TC153')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_static_route_in_fw(self):
        ao_dict = {
            "object_type": "network",
            "name": CaseParams.external_network2,
            "zone": "WAN",
            "value": CaseParams.external_network2 + ',255.255.255.0'
        }
        output1, msg1 = aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in json.dumps(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_network2
        output2, msg2 = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in json.dumps(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route in remote failed")

    def test_02_enable_ospf_in_fws(self):
        ospf_dict = {'router_id': Parameter.X3_IP, 'static_route': 'on'}
        output3 = dynaroutingapi.ospf2_config(**ospf_dict)
        ospf_dict = {'router_id': Parameter.REMOTE_X2_IP, 'static_route': 'on'}
        output4 = r_dynaroutingapi.ospf2_config(**ospf_dict)

        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2 & output3 & output4, True, "ERR: enable ospf failed")

    def test_03_show_nsm_database_and_neighbor(self):
        output = routecli.show_nsm_database()
        filter_list = [
            self.ao_network,
            f'via {Parameter.REMOTE_X1_GW}',
            'X1'
        ]
        filterres = [x in output for x in filter_list]
        logger.info(f'check nsm result: {filterres}')
        res1 = all(filterres)
        logger.info('wait for 40s to check router neighbor list...')
        time.sleep(40)
        routerres = r_routepolicyapi.get_dynamic_route_policy()
        res2 = True if self.ao_network in str(routerres) else False
        logger.info(f'show nsm result: {res1}, show router neighbor result: {res2}')
        Assertion.assert_equal(res1 & res2, True, f"ERR: check nsm and neighbor list failed")

    def test_04_selete_another_ao(self):
        ao_dict = {
            "object_type": "network",
            "name": CaseParams.external_network3,
            "zone": "WAN",
            "value": CaseParams.external_network3 + ',255.255.255.0'
        }
        output1, msg1 = aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in json.dumps(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_network3
        output2 = routepolicyapi.edit_route_policy(name=route_base_dict['name'], **route_policy_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route in fw failed")

    def test_05_show_nsm_database_and_neighbor(self):
        self.ao_network = CaseParams.external_network3
        self.test_03_show_nsm_database_and_neighbor()

    def test_06_modify_ao_network(self):
        ao_dict = {
            "object_type": "network",
            "name": CaseParams.external_network3,
            "zone": "WAN",
            "value": self.modify_ao_network + ',255.255.255.0'
        }
        output = aoapi.edit_addressobject_by_name(oldname=ao_dict['name'], **ao_dict)
        Assertion.assert_equal(output, True, "ERR: config static route in fw failed")

    def test_07_show_nsm_database_and_neighbor(self):
        self.ao_network = self.modify_ao_network
        self.test_03_show_nsm_database_and_neighbor()

    def test_08_modify_interface_x1_to_x2(self):
        route_base_dict.update({
            "destination": {
                "name": CaseParams.external_network3
            },
            "gateway": {
                "name": "X2 IP"
            },
            "interface": "X2",
        })
        output = routepolicyapi.edit_route_policy(name=route_base_dict['name'], **route_policy_dict)
        Assertion.assert_equal(output, True, "ERR: modify static route in fw failed")

    def test_09_check_inactive_router_not_in_neighbor(self):
        logger.info('wait for 40s to check router neighbor list...')
        time.sleep(40)
        routerres = r_routepolicyapi.get_dynamic_route_policy()
        output = True if self.ao_network in str(routerres) else False
        Assertion.assert_not_equal(output, True, f"ERR: check inactive router not in neighbor failed")

    def test_10_init_ao_and_routing_settings(self):
        output1 = routepolicyapi.del_route_policy_by_name(name=route_base_dict['name'])
        output2 = aoapi.del_ao_by_name(name=CaseParams.external_network2, version='ipv4')
        output3 = aoapi.del_ao_by_name(name=CaseParams.external_network3, version='ipv4')
        logger.info(f'del route: {output1}, del network2: {output2}, del network3: {output3}')
        TestDeclare_TC90().test_03_disable_ospf_in_fws()


# OSPF: Verify correct behavior with vlan interfaces
class TestVLAN_TC117(Test):
    uuid = "SOSAIOT-TC-55656"
    description = show_testcase_info(TESTPLAN, 'VLAN_TC117', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'VLAN_TC117')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_vlan_for_fws(self):
        output1, msg1 = interfaceapi.add_interface(msg=True, **x1_vlan_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in json.dumps(msg1).lower() else False
        output2, msg2 = r_interfaceapi.add_interface(msg=True, **r_x1_vlan_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in json.dumps(msg2).lower() else False
        logger.info(f'config X1 vlan interface result: {output1}, {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: Config X1 vlan for fws failed")

    def test_02_add_a_static_route_in_remote(self):
        ao_dict = {
            "object_type": "host",
            "name": CaseParams.external_ip1,
            "zone": "WAN",
            "value": CaseParams.external_ip1
        }
        output1, msg1 = r_aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in json.dumps(msg1).lower() else False
        route_base_dict.update({
            "destination": {
                "name": CaseParams.external_ip1
            },
            "gateway": {
                "name": "X1 Default Gateway"
            },
            "interface": "X1",
        })
        output2, msg2 = r_routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in json.dumps(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route in remote failed")

    def test_03_enable_ospf_in_fws(self):
        ospf_dict = {'router_id': Parameter.X1_VLAN_IP, 'static_route': 'on'}
        output3 = dynaroutingapi.ospf2_config(**ospf_dict)
        ospf_dict = {'router_id': Parameter.REMOTE_X1_VLAN, 'static_route': 'on'}
        output4 = r_dynaroutingapi.ospf2_config(**ospf_dict)

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': f'X1:V{L_X1_VLAN}'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': f'X1:V{L_X1_VLAN}'})
        output2 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2 & output3 & output4, True, "ERR: enable ospf failed")

    @repeat_method(5)
    def test_04_check_ospf_neighbor_list(self):
        logger.info('wait for 60s to check neighbor list...')
        time.sleep(60)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_not_regular(output, CaseParams.external_ip1, f"ERR: check ospf establish neighbor failed")

    def test_05_check_static_route_in_local(self):
        res = False
        output = routepolicyapi.get_dynamic_route_policy()
        try:
            for route in output:
                if route['destination'] == f'{CaseParams.external_ip1}/32' and route['interface'] == f'X1:V{L_X1_VLAN}':
                    res = True
                    break
        except Exception as e:
            logger.info(f'check route error: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: check static route in local failed")


# OSPF: Verify correct behavior when vlan interfaces are added and deleted
class TestVLAN_TC118(Test):
    uuid = "SOSAIOT-TC-55657"
    description = show_testcase_info(TESTPLAN, 'VLAN_TC118', description=True)['title']
    vlan_dict = {
        'type': 'vlan',
        'if': 'X1',
        'vlan_tag': L_X1_VLAN,
    }

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'VLAN_TC118')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_dele_vlan_error_msg(self):
        output, msg = interfaceapi.del_interface(msg=True, **self.vlan_dict)
        error_msg = ' Interface is in use by OSPF'
        Assertion.assert_regular(str(msg), error_msg, f"ERR: check delete vlan failed")

    def test_02_disable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': f'X1:V{L_X1_VLAN}', 'mode': 'disable'})
        output1 = dynaroutingapi.set_ospf2(**ospf_dict)
        output2 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: disable ospf failed")

    def test_03_check_seccess_delete_vlan_in_fw(self):
        output = interfaceapi.del_interface(**self.vlan_dict)
        Assertion.assert_equal(output, True, f"ERR: check delete vlan failed")

    def test_04_delete_vlan_in_router(self):
        output = r_interfaceapi.del_interface(**self.vlan_dict)
        Assertion.assert_equal(output, True, f"ERR: check delete vlan failed")


# AO Group used in site to site VPN
class TestVPN_TC152(Test):
    uuid = "SOSAIOT-TC-55666"
    description = show_testcase_info(TESTPLAN, 'VPN_TC152', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'VPN_TC152')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vlan_interface_for_fws(self):
        TestVLAN_TC117().test_01_config_vlan_for_fws()

    def test_02_add_aos(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "LAN",
            "value": Parameter.REMOTE_X0_NET + ',255.255.255.0'
        }
        res1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists'.lower() in str(msg1).lower():
            res1 = True
        local_ag_dict = {"address_groups": [{
            "ipv4": {"address_object": {
                "ipv4": [{"name": "remote_vpn_net"}]},
                "name": "vpn_ag_name01"
            }}]}
        res2, msg2 = aogroupapi.add_addressgroup(msg=True, **local_ag_dict)
        if 'Already exists'.lower() in str(msg2).lower():
            res2 = True
        remote_ao_dict = {
            "object_type": "network",
            "name": "local_vpn_net",
            "zone": "LAN",
            "value": f'{Parameter.X0_SUBNET},{Parameter.MASK}'
        }
        res3, msg3 = r_aoapi.config_addressobject(msg=True, **remote_ao_dict)
        if 'Already exists'.lower() in str(msg3).lower():
            res3 = True
        remote_ag_dict = {"address_groups": [{
            "ipv4": {"address_object": {
                "ipv4": [{"name": "local_vpn_net"}]},
                "name": "vpn_ag_name01"
            }}]}
        res4, msg4 = r_aogroupapi.add_addressgroup(msg=True, **remote_ag_dict)
        if 'Already exists'.lower() in str(msg4).lower():
            res4 = True
        logger.info(f'add aos result: {res1}, {res3}')
        logger.info(f'add ags result: {res2}, {res4}')
        Assertion.assert_equal(res1 & res2 & res3 & res4, True, "ERR: add aos failed")

    def test_03_s2s_vpn_configure(self):
        res1, msg1 = vpnapi.add_vpn_policy(msg=True, **l_s2s_vpn_dict)
        if 'Already exists'.lower() in str(msg1).lower():
            res1 = True
        res2, msg2 = r_vpnapi.add_vpn_policy(msg=True, **r_s2s_vpn_dict)
        if 'Already exists'.lower() in str(msg2).lower():
            res2 = True
        logger.info(f'add s2s vpn result: {res1, res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: add vpn failed")

    @repeat_method(5)
    def test_04_check_s2s_vpn_status(self):
        time.sleep(20)
        output = vpnapi.get_active_vpn_tunnels()
        Assertion.assert_regular(str(output), l_s2s_vpn_dict['name'], "ERR: check s2s vpn status failed")

    def test_05_enable_ospf_in_fws(self):
        ospf_dict = {
            'router_id': '10.0.0.10',
            'vpn_network': 'on'
        }
        output3 = dynaroutingapi.ospf2_config(**ospf_dict)

        ospf_dict = copy.deepcopy(ospf_port_dict)
        ospf_dict.update({'interface': f'X1:V{L_X1_VLAN}'})
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2 & output3, True, "ERR: enable ospf failed")

    def test_06_check_ospf_neighbor_list(self):
        logger.info(f'wait for 40s to check fw route...')
        time.sleep(40)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_regular(output, Parameter.REMOTE_X1_VLAN, f"ERR: check ospf neighbor list failed")


# Verify the ability to transition between Advanced and non-Advanced routing
class TestALLRouting_TC124(Test):
    uuid = "SOSAIOT-TC-55660"
    description = show_testcase_info(TESTPLAN, 'ALLRouting_TC124', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'ALLRouting_TC124')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_ospf_in_fws(self):
        ospf_dict = copy.deepcopy(ospf_port_dict)
        output1 = r_dynaroutingapi.set_ospf2(**ospf_dict)
        ospf_dict.update({'interface': 'X3'})
        output2 = dynaroutingapi.set_ospf2(**ospf_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: enable ospf failed")

    def test_02_config_rip_for_local_and_remote(self):
        output1 = dynaroutingapi.set_rip(**set_rip_dict)
        set_rip_dict['interface'] = 'X2'
        output2 = r_dynaroutingapi.set_rip(**set_rip_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: config rip for local and remote failed")

    def test_03_set_router_mode_to_advanced_and_enable_bgp(self):
        opt = {
            'advanced': True,
            'BGP': True
        }
        res1 = dynaroutingapi.set_advanced_routing_mode(**opt)
        res2 = dynaroutingapi.set_BGP(**opt)
        Assertion.assert_equal(res1 & res2, True, "ERR: Set router mode and enable BGP failed")

    def test_04_check_ospf_neighbor_list(self):
        logger.info(f'wait for 40s to check fw route...')
        time.sleep(40)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf neighbor list failed")

    def test_05_check_rip_neighbor_list(self):
        output = routecli.show_rip()
        Assertion.assert_regular(output, Parameter.X3_SUBNET, f"ERR: check rip neighbor list failed")

    def test_06_disable_and_enable_advanced(self):
        disableres = dynaroutingapi.set_advanced_routing_mode(**{'advanced': False})
        enableres = dynaroutingapi.set_advanced_routing_mode(**{'advanced': True})
        Assertion.assert_equal(disableres & enableres, True, "ERR: disable and enable advanced failed")

    def test_07_check_ospf_neighbor_list(self):
        logger.info(f'wait for 40s to check fw route...')
        time.sleep(40)
        output = routecli.show_ospf2(mode='neighbor')
        Assertion.assert_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check ospf neighbor list failed")

    def test_08_check_rip_neighbor_list(self):
        output = routecli.show_rip()
        Assertion.assert_regular(output, Parameter.X3_SUBNET, f"ERR: check rip neighbor list failed")

    def test_09_check_bgp_neighbor_list(self):
        output = routecli.show_BGP(mode='summary')
        Assertion.assert_not_regular(output, Parameter.REMOTE_X2_IP, f"ERR: check bgp neighbor list failed")

