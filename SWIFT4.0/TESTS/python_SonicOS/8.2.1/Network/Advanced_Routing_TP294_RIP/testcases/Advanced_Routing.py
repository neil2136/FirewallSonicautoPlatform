from definition.settings import *
from definition.utils import *


# check ripv1 send packet in x3.
class TestRIP_TC47(Test):
    uuid = "SOSAIOT-TC-55698"
    description = show_testcase_info(TESTPLAN, 'RIP_TC47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC47')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        output = dynaroutingapi.set_rip(**set_rip_dict)
        Assertion.assert_equal(output, True, "ERR: config rip for x3 in local failed")

    def test_02_check_rip_send_packet_in_fw(self):
        reqres = False
        for i in range(3):
            logger.info('waiting for 30s to capture rip packets...')
            time.sleep(30)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, pcapng_filters.values())
            if reqres:
                logger.info(packet)
                break

        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check rip send packet failed")


# check RIPv2 - v1 send packet in x3.
class TestRIP_TC48(Test):
    uuid = "SOSAIOT-TC-55699"
    description = show_testcase_info(TESTPLAN, 'RIP_TC48', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC48')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv2_v1_for_x3_in_local(self):
        set_rip_dict['send'] = '1'
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_check_ripv2_v1_send_packet_in_fw(self):
        pcapng_filters['Version'] = 'Version: RIPv2'
        TestRIP_TC47().test_02_check_rip_send_packet_in_fw()


# check RIPv2 send packet in x3.
class TestRIP_TC49(Test):
    uuid = "SOSAIOT-TC-55700"
    description = show_testcase_info(TESTPLAN, 'RIP_TC49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC49')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv2_v1_for_x3_in_local(self):
        set_rip_dict['send'] = '2'
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_check_ripv2_v1_send_packet_in_fw(self):
        pcapng_filters['Destination'] = f'Destination: {CaseParams.rip_route_ip}'
        TestRIP_TC47().test_02_check_rip_send_packet_in_fw()


# Verify the correct RIP packets. Receive. RIPv1
class TestRIP_TC50(Test):
    uuid = "SOSAIOT-TC-55702"
    description = show_testcase_info(TESTPLAN, 'RIP_TC50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv1_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'receive',
            'receive': '0'
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_ripv1_for_x2_in_remote(self):
        remote_dict = {
            'interface': 'X2',
            'mode': 'disable'
        }
        output = r_dynaroutingapi.set_rip(**remote_dict)
        logger.info(f'disable remote x2 first: {output}')
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '0',
        }
        output1 = r_dynaroutingapi.set_rip(**rip_dict)
        output2 = r_dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        logger.info(f'set x2 rip: {output1}, rip config: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: config ripv1 for x2 in remote failed")

    def test_03_add_a_static_route_in_remote(self):
        ao_dict = {
            "object_type": "host",
            "name": CaseParams.external_ip1,
            "zone": "WAN",
            "value": CaseParams.external_ip1
        }
        output1, msg1 = r_aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in str(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_ip1
        output2, msg2 = r_routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in str(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route in remote failed")

    def test_04_check_ripv1_request_from_remote(self):
        reqres = False
        for i in range(3):
            logger.info('waiting for 30s to capture rip packets...')
            time.sleep(30)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, rip_packet_filter.values())
            if reqres:
                logger.info(packet)
                break
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check ripv1 request packet failed")

    def test_05_check_ripv1_response_from_remote(self):
        rip_packet_filter['Command'] = 'Command: Response'
        packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        reqres, packet = check_pcapng_packets(packets, rip_packet_filter.values())
        logger.info(f'check response result: {packet}')
        Assertion.assert_equal(reqres, True, "ERR: check ripv1 response packet failed")

    @repeat_method(5)
    def test_06_check_static_route_in_local(self):
        res = False
        logger.info('waiting for 20s to make sure static route can be sync to local fw...')
        time.sleep(20)
        output = routepolicyapi.get_dynamic_route_policy()
        try:
            for route in output:
                if route['destination'] == f'{CaseParams.external_ip1}/32' and route['metric'] == 120:
                    res = True
                    break
        except Exception as e:
            logger.info(f'check route error: {repr(e)}')
        Assertion.assert_equal(res, True, "ERR: check static route in local failed")

    def test_07_init_x3_and_x2_config(self):
        local_dict = {
            'interface': 'X3',
            'mode': 'disable'
        }
        output1 = dynaroutingapi.set_rip(**local_dict)
        remote_dict = {
            'interface': 'X2',
            'mode': 'disable'
        }
        output2 = r_dynaroutingapi.set_rip(**remote_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: init local x3 and remote x2 rip failed")


# Verify the correct RIP packets. Receive. RIPv2
class TestRIP_TC51(Test):
    uuid = "SOSAIOT-TC-55703"
    description = show_testcase_info(TESTPLAN, 'RIP_TC51', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv2_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'receive',
            'receive': '2'
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_ripv2_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config ripv2 for x2 in remote failed")

    def test_03_check_ripv2_request_from_remote(self):
        rip_packet_filter.update({
            'Destination': f'Destination: {CaseParams.rip_route_ip}',
            'Version': 'Version: RIPv2',
            'Command': 'Command: Request'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv2_response_from_remote(self):
        rip_packet_filter['Command'] = 'Command: Response'
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify the correct RIP packets. Send and Receive. Receive RIPv1, Send RIPv1.
class TestRIP_TC52(Test):
    uuid = "SOSAIOT-TC-55704"
    description = show_testcase_info(TESTPLAN, 'RIP_TC52', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv1_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '0',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_ripv1_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '0',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config ripv1 for x2 in remote failed")

    def test_03_check_ripv2_request_from_remote(self):
        rip_packet_filter.update({
            'Destination': 'Destination: 172.16.2.255',
            'Version': 'Version: RIPv1',
            'Command': 'Command: Request'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv2_response_from_remote(self):
        rip_packet_filter['Command'] = 'Command: Response'
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify the correct RIP packets. Send and Receive. Receive RIPv1, Send RIPv2 - v1 compatible.
class TestRIP_TC53(Test):
    uuid = "SOSAIOT-TC-55705"
    description = show_testcase_info(TESTPLAN, 'RIP_TC53', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC53')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv1_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '1',
            'receive': '0',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_ripv1_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config ripv1 for x2 in remote failed")

    def test_03_check_ripv1_request_from_remote(self):
        rip_packet_filter.update({
            'Destination': 'Destination: 172.16.2.255',
            'Version': 'Version: RIPv1',
            'Command': 'Command: Request'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv2_response_from_local(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.X3_IP,
            'Destination': 'Destination: 172.16.2.255',
            'Version': 'Version: RIPv2',
            'Command': 'Command: Response'
        })
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify the correct RIP packets. Send and Receive. Receive RIPv1, Send RIPv2.
class TestRIP_TC54(Test):
    uuid = "SOSAIOT-TC-55706"
    description = show_testcase_info(TESTPLAN, 'RIP_TC54', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC54')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_ripv1_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '0',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_ripv1_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config ripv1 for x2 in remote failed")

    def test_03_check_ripv1_request_from_remote(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.REMOTE_X2_IP,
            'Destination': 'Destination: 172.16.2.255',
            'Version': 'Version: RIPv1',
            'Command': 'Command: Request'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv2_response_from_local(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.X3_IP,
            'Destination': f'Destination: {CaseParams.rip_route_ip}',
            'Version': 'Version: RIPv2',
            'Command': 'Command: Response'
        })
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify the correct RIP packets. Send and Receive. Receive RIPv2, Send RIPv1.
class TestRIP_TC55(Test):
    uuid = "SOSAIOT-TC-55707"
    description = show_testcase_info(TESTPLAN, 'RIP_TC55', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC55')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '0',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_rip_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '0',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in remote failed")

    def test_03_check_ripv1_request_from_local(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.X3_IP,
            'Destination': 'Destination: 172.16.2.255',
            'Version': 'Version: RIPv1',
            'Command': 'Command: Request'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv1_response_from_local(self):
        rip_packet_filter.update({
            'Command': 'Command: Response'
        })
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify the correct RIP packets. Send and Receive. Receive RIPv2, Send RIPv2 - v1 compatible.
class TestRIP_TC56(Test):
    uuid = "SOSAIOT-TC-55708"
    description = show_testcase_info(TESTPLAN, 'RIP_TC56', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC56')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '1',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_rip_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in remote failed")

    def test_03_check_ripv2_response_from_remote(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.REMOTE_X2_IP,
            'Destination': f'Destination: {CaseParams.rip_route_ip}',
            'Version': 'Version: RIPv2',
            'Command': 'Command: Response'
        })
        TestRIP_TC50().test_04_check_ripv1_request_from_remote()

    def test_04_check_ripv2_response_from_local(self):
        rip_packet_filter.update({
            'Source': 'Source: ' + Parameter.X3_IP,
            'Destination': 'Destination: 172.16.2.255',
            'Command': 'Command: Response'
        })
        TestRIP_TC50().test_05_check_ripv1_response_from_remote()

    def test_05_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify The 0.0.0.0/0 route must not appear in the remote fw.
class TestRIP_TC58(Test):
    uuid = "SOSAIOT-TC-55710"
    description = show_testcase_info(TESTPLAN, 'RIP_TC58', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC58')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_config_rip_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in remote failed")

    def test_03_config_x3_to_dmz(self):
        x3_dmz_dict = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x3_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_04_diable_originate_default_route_in_local(self):
        output = r_dynaroutingapi.rip_config(**{'OriginateDefaultRoute': 'off'})
        Assertion.assert_equal(output, True, "ERR: disable originate default route in local failed")

    def test_05_check_default_route_not_in_remote(self):
        output = routecli.show_route_policies(version='ipv4', type='dynamic')
        Assertion.assert_not_regular(output, '0.0.0.0/0', "ERR: check default route not in remote failed")


# Verify static routes on FW should not appear in the remote fw.
class TestRIP_TC60(Test):
    uuid = "SOSAIOT-TC-55713"
    description = show_testcase_info(TESTPLAN, 'RIP_TC60', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC60')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_static_route_in_local(self):
        ao_dict = {
            "object_type": "host",
            "name": CaseParams.external_ip2,
            "zone": "WAN",
            "value": CaseParams.external_ip2
        }
        output1, msg1 = aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in str(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_ip2
        output2, msg2 = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in str(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route in local failed")

    def test_02_disable_static_route_in_local(self):
        output = dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'off'})
        Assertion.assert_equal(output, True, "ERR: disable static route in local failed")

    def test_03_check_dynamic_route_not_in_remote(self):
        output = routecli.show_route_policies(version='ipv4', type='dynamic')
        Assertion.assert_not_regular(output,
                                     f'{CaseParams.external_ip2}/32',
                                     "ERR: check dynamic route not in remote failed")


# Verify connected networks routes on FW should not appear in the remote fw.
class TestRIP_TC62(Test):
    uuid = "SOSAIOT-TC-55715"
    description = show_testcase_info(TESTPLAN, 'RIP_TC62', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC62')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_disable_connected_network_route_in_local(self):
        output = dynaroutingapi.rip_config(**{'RedistributeConnectedNetworks': 'off'})
        Assertion.assert_equal(output, True, "ERR: connected network route in local failed")

    def test_02_check_dynamic_route_not_in_remote(self):
        output = routecli.show_route_policies(version='ipv4', type='dynamic')
        res = True if Parameter.X2_SUBNET in output and Parameter.X0_SUBNET in output else False
        Assertion.assert_equal(res, False, "ERR: check dynamic route not in remote failed")


# Verify Split Horizon is not used, rip response form local have network1.
class TestRIP_TC68(Test):
    uuid = "SOSAIOT-TC-55718"
    description = show_testcase_info(TESTPLAN, 'RIP_TC68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC68')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_static_route_in_remote(self):
        output = r_dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        Assertion.assert_equal(output, True, "ERR: enable static route in remote failed")

    def test_02_add_a_network_static_route_in_remote(self):
        ao_dict = {
            "object_type": "network",
            "name": CaseParams.external_network1,
            "zone": "WAN",
            "value": CaseParams.external_network1 + ',255.255.255.0'
        }
        output1, msg1 = r_aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in str(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_network1
        output2, msg2 = r_routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in str(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: add static route in remote failed")

    def test_03_config_rip_for_x3_in_local(self):
        output = dynaroutingapi.set_rip(**{'interface': 'X3', 'mode': 'disable'})
        logger.info(f'disable x3 rip: {output}')
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_04_config_rip_for_x2_in_remote(self):
        remote_dict = {
            'interface': 'X2',
            'mode': 'disable'
        }
        output = r_dynaroutingapi.set_rip(**remote_dict)
        logger.info(f'disable remote x2 first: {output}')
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output1 = r_dynaroutingapi.set_rip(**rip_dict)
        output2 = r_dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        logger.info(f'set x2 rip: {output1}, rip config: {output2}')

        logger.info('waiting for 30s to capture rip packets...')
        time.sleep(30)
        Assertion.assert_equal(output1 & output2, True, "ERR: config rip for x2 in remote failed")

    def test_05_check_rip_response_form_local_have_network1(self):
        reqres = False
        filter_dict = copy.deepcopy(rip_local_filter_dict)
        filter_dict['IP Address'] = f'IP Address: {CaseParams.external_network1}'
        for i in range(3):
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, filter_dict.values())
            if reqres:
                logger.info(packet)
                break
            else:
                clearres = packetmonitorapi.clear_packets()
                logger.info(f'clear packets result: {clearres}')
                startres = packetmonitorapi.start_capture()
                logger.info(f'start capture result: {startres}')
                logger.info('waiting for 30s to retest...')
                logger.info(f'check filter values: {filter_dict.values()}')
                time.sleep(30)
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check rip response form local have network1 failed")


# Verify Split Horizon is not used, rip response form local not network1
class TestRIP_TC69(Test):
    uuid = "SOSAIOT-TC-55719"
    description = show_testcase_info(TESTPLAN, 'RIP_TC69', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC69')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        output = dynaroutingapi.set_rip(**{'interface': 'X3', 'mode': 'disable'})
        logger.info(f'disable x3 rip: {output}')
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'split_horizon': 'on',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_03_check_rip_response_form_local_not_network1(self):
        reqres = False
        for i in range(3):
            clearres = packetmonitorapi.clear_packets()
            logger.info(f'clear packets result: {clearres}')
            startres = packetmonitorapi.start_capture()
            logger.info(f'start capture result: {startres}')

            logger.info('waiting for 30s to capture rip packets...')
            time.sleep(30)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, rip_local_filter_dict.values())
            if reqres:
                reqres = True if f'IP Address: {CaseParams.external_network1}' in packet else False
                break
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, False, "ERR: check rip response form local not network1 failed")


# Verify Split Horizon is not used, rip response form local have network1
class TestRIP_TC70(Test):
    uuid = "SOSAIOT-TC-55721"
    description = show_testcase_info(TESTPLAN, 'RIP_TC70', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC70')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        output = dynaroutingapi.set_rip(**{'interface': 'X3', 'mode': 'disable'})
        logger.info(f'disable x3 rip: {output}')
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'split_horizon': 'on',
            'poison_reverse': 'on',
            'receive': '2',
        })
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_02_check_rip_response_form_local_network1_metric_is_16(self):
        reqres = False
        for i in range(3):
            clearres = packetmonitorapi.clear_packets()
            logger.info(f'clear packets result: {clearres}')
            startres = packetmonitorapi.start_capture()
            logger.info(f'start capture result: {startres}')

            logger.info('waiting for 30s to capture rip packets...')
            time.sleep(60)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, rip_local_filter_dict.values())
            if reqres:
                reqres = True if f'IP Address: {CaseParams.external_network1}, Metric: 16' in packet else False
                break
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check rip response form local network1 metric is 16 failed")


# Verify include static route 36.1.1.0 , but set metric infinity =16 in rip update message
class TestRIP_TC72(Test):
    uuid = "SOSAIOT-TC-55723"
    description = show_testcase_info(TESTPLAN, 'RIP_TC72', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC72')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_rip_for_x3_in_local(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        rip_dict = {
            'interface': 'X3',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output1 = dynaroutingapi.set_rip(**rip_dict)
        output2 = dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        logger.info(f'set x3 rip: {output1}, local rip config: {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: config rip for x2 in local failed")

    def test_02_config_rip_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        output2 = r_dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'off'})
        logger.info(f'enable remote static route: {output2}')
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in remote failed")

    def test_03_add_a_static_route_to_local(self):
        ao_dict = {
            "object_type": "network",
            "name": CaseParams.external_network2,
            "zone": "WAN",
            "value": f'{CaseParams.external_network2},255.255.255.0'
        }
        output1, msg1 = aoapi.config_addressobject(msg=True, **ao_dict)
        if not output1:
            output1 = True if 'Already exists'.lower() in str(msg1).lower() else False
        route_base_dict['destination']['name'] = CaseParams.external_network2
        output2, msg2 = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
        if not output2:
            output2 = True if 'Already exists'.lower() in str(msg2).lower() else False
        Assertion.assert_equal(output1 & output2, True, "ERR: config static route to local failed")

    def test_04_check_rip_update_response_form_local_network2_metric_is_1(self):
        reqres = False
        filter_dict = copy.deepcopy(rip_local_filter_dict)
        filter_dict['IP Address'] = f'IP Address: {CaseParams.external_network2}, Metric: 1'
        for i in range(3):
            logger.info('waiting for 30s to capture rip packets...')
            logger.info(f'check filter values: {filter_dict.values()}')
            time.sleep(30)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, filter_dict.values())
            if reqres:
                logger.info(packet)
                break
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check rip update response form local network2 metric is 1 failed")

    def test_05_check_dynamic_route_network2_in_remote(self):
        output = r_routecli.show_route_policies(version='ipv4', type='dynamic')
        res = True if CaseParams.external_network2 in output else False
        Assertion.assert_equal(res, True, "ERR: check dynamic route network2 in remote failed")

    def test_06_delete_the_static_route_in_local(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')
        output = routepolicyapi.del_route_policy_by_name(name=route_base_dict['name'])
        logger.info('waiting for 20s to capture rip packets...')
        time.sleep(20)
        Assertion.assert_equal(output, True, "ERR: delete static route in local failed")

    def test_07_check_rip_update_response_form_local_network2_metric_is_16(self):
        reqres = False
        filter_dict = copy.deepcopy(rip_local_filter_dict)
        filter_dict['IP Address'] = f'IP Address: {CaseParams.external_network2}, Metric: 16'
        for i in range(3):
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres, packet = check_pcapng_packets(packets, filter_dict.values())
            if reqres:
                logger.info(packet)
                break
            else:
                clearres = packetmonitorapi.clear_packets()
                logger.info(f'clear packets result: {clearres}')
                logger.info('waiting for 30s to retest...')
                logger.info(f'check filter values: {filter_dict.values()}')
                time.sleep(30)

        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(reqres, True, "ERR: check rip periodic response form local network2 metric is 16 failed")


# Verify include the static route 36.1.1.0 , but set metric infinity =16 in rip periodic update message
class TestRIP_TC71(Test):
    uuid = "SOSAIOT-TC-55722"
    description = show_testcase_info(TESTPLAN, 'RIP_TC71', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_rip_periodic_response_form_local(self):
        clearres = packetmonitorapi.clear_packets()
        logger.info(f'clear packets result: {clearres}')
        startres = packetmonitorapi.start_capture()
        logger.info(f'start capture result: {startres}')

        TestRIP_TC72().test_07_check_rip_update_response_form_local_network2_metric_is_16()

    def test_06_init_x3_and_x2_config(self):
        output = dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'off'})
        logger.info(f'enable remote static route: {output}')
        TestRIP_TC50().test_07_init_x3_and_x2_config()


# Verify  the authentication capability. Use Password
class TestRIP_TC77(Test):
    uuid = "SOSAIOT-TC-55725"
    description = show_testcase_info(TESTPLAN, 'RIP_TC77', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC77')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_a_static_route_in_local(self):
        TestRIP_TC72().test_03_add_a_static_route_to_local()

    def test_02_config_rip_for_x3_in_local(self):
        set_rip_dict.update({
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
            'password': 'test',
        })
        output2 = dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        logger.info(f'enable local static route: {output2}')
        TestRIP_TC47().test_01_config_rip_for_x3_in_local()

    def test_03_config_rip_for_x2_in_remote(self):
        rip_dict = {
            'interface': 'X2',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
            'password': 'test',
        }
        output = r_dynaroutingapi.set_rip(**rip_dict)
        output2 = r_dynaroutingapi.rip_config(**{'RedistributeStaticRoutes': 'on', 'StaticsMetric': '1'})
        logger.info(f'enable remote static route: {output2}')
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in remote failed")

    def test_04_check_static_route_in_local(self):
        TestRIP_TC50().test_06_check_static_route_in_local()

    def test_05_check_static_route_in_remote(self):
        TestRIP_TC72().test_05_check_dynamic_route_network2_in_remote()


# Verify interface X2:V100 can not be deleted with RIP enabled on it. GUI prompt error message.
class TestRIP_TC79(Test):
    uuid = "SOSAIOT-TC-55727"
    description = show_testcase_info(TESTPLAN, 'RIP_TC79', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC79')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_x2_vlan_to_dmz(self):
        dmz_dict = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': 100,
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '2.2.2.168',
        }
        rc = interfaceapi.add_interface(**dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to vlan dmz failed")

    def test_02_config_rip_for_x2_vlan_in_local(self):
        rip_dict = {
            'interface': 'X2:V100',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output = dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output, True, "ERR: config rip for x2 in local failed")

    def test_03_check_delete_X2_vlan(self):
        vlan_dict = {
            'type': 'vlan',
            'if': 'X2',
            'vlan_tag': '100'
        }
        output, msg = interfaceapi.del_interface(msg=True, **vlan_dict)
        Assertion.assert_regular(json.dumps(msg), 'Interface is in use by RIP', 'ERR: check delete x2 vlan failed')

    def test_04_init_x3_rip_and_x2_vlan_config(self):
        local_dict = {
            'interface': 'X2:V100',
            'mode': 'disable'
        }
        vlan_dict = {
            'type': 'vlan',
            'if': 'X2',
            'vlan_tag': '100'
        }
        output1 = dynaroutingapi.set_rip(**local_dict)
        output2 = interfaceapi.del_interface(**vlan_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: init x3 rip and x2 vlan failed")


# Verify interface X2:V100 can not be deleted with RIP enabled on it. GUI prompt error message.
class TestRIP_TC80(Test):
    uuid = "SOSAIOT-TC-55729"
    description = show_testcase_info(TESTPLAN, 'RIP_TC80', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'RIP_TC80')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_30_aos(self):
        aores = []
        for i in range(51, 81):
            ao_dict = {
                "object_type": "host",
                "name": f'66.66.66.{i}',
                "zone": "WAN",
                "value": f'66.66.66.{i}'
            }
            (output, aomsg) = aoapi.config_addressobject(msg=True, **ao_dict)
            if output is False:
                output = True if 'Already exists'.lower() in str(aomsg).lower() else False
            aores.append(output)
        logger.info(f'add aos counts: {len(aores)}')
        Assertion.assert_equal(len(aores), 30, "ERR: add 30 aos failed")

    def test_02_add_30_static_route_in_local(self):
        res1 = routepolicyapi.del_all_route_policies()
        res2 = r_routepolicyapi.del_all_route_policies()
        logger.info(f'delete route first: local: {res1}, remote: {res2}')
        time.sleep(10)
        routeres = []
        for i in range(51, 81):
            route_base_dict['destination']['name'] = f'66.66.66.{i}'
            output, msg = routepolicyapi.add_route_policy(msg=True, **route_policy_dict)
            if not output:
                output = True if 'Already exists'.lower() in str(msg).lower() else False
            routeres.append(output)
            logger.info(f'add routes counts: {len(routeres)}')
        Assertion.assert_equal(len(routeres), 30, "ERR: add 30 routes in local failed")

    def test_03_config_rip_in_local_and_remote(self):
        output = dynaroutingapi.set_rip(**{'interface': 'X3', 'mode': 'disable'})
        logger.info(f'disable x3 rip: {output}')
        rip_dict = {
            'interface': 'X3',
            'mode': 'send_and_receive',
            'send': '2',
            'receive': '2',
        }
        output1 = dynaroutingapi.set_rip(**rip_dict)
        rip_dict['interface'] = 'X2'
        output2 = r_dynaroutingapi.set_rip(**rip_dict)
        Assertion.assert_equal(output1 & output2, True, "ERR: config rip in local and remote failed")

    def test_04_check_2_packets_in_rip_route(self):
        reqres = []
        for i in range(3):
            clearres = packetmonitorapi.clear_packets()
            logger.info(f'clear packets result: {clearres}')
            startres = packetmonitorapi.start_capture()
            logger.info(f'start capture result: {startres}')

            logger.info('waiting for 40s to capture rip packets...')
            time.sleep(40)
            packetmonitorapi.export_captured_packets_pcapng()
            packets = PC1_login.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            reqres = check_max_routes_packets(packets, rip_local_filter_dict.values())
            if reqres:
                break
        stopres = packetmonitorapi.stop_capture()
        logger.info(f'stop capture result: {stopres}')
        Assertion.assert_equal(len(reqres), 2, "ERR: check 2 packets in rip route failed")

    def test_05_init_static_route_in_local(self):
        output = routepolicyapi.del_all_route_policies()
        Assertion.assert_equal(output, True, "ERR: init static route in local failed")

    def test_06_init_x3_and_x2_config(self):
        TestRIP_TC50().test_07_init_x3_and_x2_config()
