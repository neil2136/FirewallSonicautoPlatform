from scapy.sendrecv import SndRcvHandler
from utils import *
from settings import *


class Test_38_IPv4_ECMP_PBR_with_4_gw_same_outgoing_physical_interface(Test):
    uuid = "SOSAIOT-TC-55947"

    def test_38_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '038')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_38_02_Add_Test_38_IPv4_ECMP_PBR_with_4_gw_same_interface(self):
        rc = routeapi.add_route_policy(**ecmp_1gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_38_03_check_route(self):
        ecmpname = ecmp_1gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        routefound = routeapi.show_route_policy_by_name(ecmpname)
        logger.info(routefound)
        res = True if ecmpname in str(routefound) else False

        # init route policy configure
        delres = routeapi.del_route_policy_by_name(ecmpname)
        logger.info('del route result: {}'.format(delres))

        Assertion.assert_equal(res, True, "ERR:check ecmp failed")


class Test_39_IPv4_ECMP_PBR_with_4_gw_different_outgoing_interface(Test):
    uuid = "SOSAIOT-TC-55948"

    def test_39_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '039')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_39_02_Add_IPv4_ECMP_PBR_with_4_gw_different_interface(self):
        rc = routeapi.add_route_policy(**ecmp_4gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_39_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        confpkgres = pkgmonitorapi.conf_packmon(**pkt_setting_dict)
        logger.info('Config capture result:{}'.format(confpkgres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))

        exportres = pkgmonitorapi.export_captured_packets()
        checkres = check_packets(exportres, expect_pkt_dict, fwports)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_39_04_del_route(self):
        ecmpname = ecmp_4gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        # init route policy configure
        delres = routeapi.del_route_policy_by_name(ecmpname)
        logger.info('del route result: {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")


class Test_219_TSR(Test):
    uuid = "SOSAIOT-TC-55973"

    def test_219_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '219')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_219_02_add_ecmp_routes(self):
        add1gwres = routeapi.add_route_policy(**ecmp_1gw_api_rt_dict)
        add4gwres = routeapi.add_route_policy(**ecmp_4gw_api_rt_dict)
        Assertion.assert_equal(
            add1gwres & add4gwres,
            True,
            "ERR:ADD ecmp failed")

    def test_219_03_check_route_info_in_TSR(self):
        gw_list = [gw1_ao_dict, gw2_ao_dict, gw3_ao_dict, gw4_ao_dict]
        port_list = ['X1', 'X2', 'X3', 'X4']

        tsr = diagapi.get_tsr_part('Network', 'Routing', 'Route Policies')
        logger.info('TSR Route Part:{}'.format(tsr))
        check1gwres = check_1gw_TSR(tsr, ecmp_1gw_api_rt_dict, gw_list)
        logger.info(
            'check route policy ecmp_1gw_api_rt_dict in TSR: {}'.format(check1gwres))
        check4gwres = check_4gw_TSR(tsr, ecmp_4gw_api_rt_dict, port_list)
        logger.info(
            'check route policy ecmp_4gw_api_rt_dict in TSR: {}'.format(check4gwres))

        Assertion.assert_equal(
            check1gwres & check4gwres,
            True,
            "ERR:the police in TSR check failed ")

    def test_219_04_del_route(self):
        ecmpname1gw = ecmp_1gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        ecmpname4gw = ecmp_4gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        del1gwres = routeapi.del_route_policy_by_name(ecmpname1gw)
        logger.info('delete route result : {}'.format(del1gwres))
        del4gwres = routeapi.del_route_policy_by_name(ecmpname4gw)
        logger.info('delete route result : {}'.format(del4gwres))
        Assertion.assert_equal(del4gwres & del1gwres,
                               True, "ERR:the police delete failed")


class Test_159_Edit_an_IPv4_ECMP_PBR_in_CLI_which_is_added_on_GUI(Test):
    uuid = "SOSAIOT-TC-55964"

    def test_159_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '159')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_159_02_Add_IPv4_ECMP_PBR_via_API(self):
        rc = routeapi.add_route_policy(**ecmp_4gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_159_03_Edit_IPv4_ECMP_PBR_via_CLI(self):
        ecmpname = ecmp_4gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        rc = routecli.edit_route_policy_by_name(
            version='ipv4', name=ecmpname, **ecmp_cli_new_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:edit ecmp failed")

    def test_159_04_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X4']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()
        checkres = check_packets(exportres, expect_pkt_dict, fwports)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_159_05_del_route(self):
        delres = routeapi.del_route_policy_by_name(
            ecmp_cli_new_rt_dict['name-new'])
        logger.info('del route result: {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")


class Test_179_Delete_an_IPv4_ECMP_PBR_in_CLI_which_is_added_on_GUI(Test):
    uuid = "SOSAIOT-TC-55971"

    def test_179_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '179')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_179_02_Add_IPv4_ECMP_PBR_via_API(self):
        rc = routeapi.add_route_policy(**ecmp_4gw_api_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_179_03_Delete_IPv4_ECMP_PBR_via_CLI(self):
        ecmpname = ecmp_4gw_api_rt_dict['route_policies'][0]['ipv4']['name']
        rc = routecli.del_route_policy_by_name(
            version='ipv4', name=ecmpname)
        Assertion.assert_equal(rc, True, "ERR:del ecmp failed")

    def test_179_04_send_traffic_and_check_packet(self):
        fwports = ['X1']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")


class Test_054_IPv4_ECMP_PBR_src_range_dst_network_4_gw(Test):
    uuid = "SOSAIOT-TC-55949"
    description = show_testcase_info(
        Parameter.TESTPLAN, '054', description=True)['title']

    def test_054_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '054')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_054_02_add_ecmp_routes(self):
        res = routeapi.add_route_policy(**ecmp_4gw_range_rt_dict)
        Assertion.assert_equal(res, True, "ERR:ADD ecmp failed")

    def test_054_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmp_dict['IP']['src'] = Parameter.SRC_RANGE
        icmp_dict['IP']['dst'] = Parameter.DST_NETWORK

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))

        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_054_04_del_route(self):
        ecmpname = ecmp_4gw_range_rt_dict['route_policies'][0]['ipv4']['name']
        delres = routeapi.del_route_policy_by_name(ecmpname)
        logger.info('delete route result : {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")


class Test_057_IPv4_ECMP_PBR_src_network_dst_network_4_gw(Test):
    uuid = "SOSAIOT-TC-55950"
    description = show_testcase_info(
        Parameter.TESTPLAN, '057', description=True)['title']

    def test_057_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '057')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_057_02_add_ecmp_routes(self):
        res = routeapi.add_route_policy(**ecmp_4gw_network_rt_dict)
        Assertion.assert_equal(res, True, "ERR:add ecmp route policy failed")

    def test_057_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmp_dict['IP']['src'] = Parameter.SRC_NETWORK

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_057_04_del_route(self):
        ecmpname = ecmp_4gw_network_rt_dict['route_policies'][0]['ipv4']['name']
        delres = routeapi.del_route_policy_by_name(ecmpname)
        logger.info('delete route result : {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")


class Test_147_Add_an_IPv4_ECMP_PBR_in_CLI_with_4_gw_different_interface(Test):
    uuid = "SOSAIOT-TC-55960"

    def test_147_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '147')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_147_02_Add_IPv4_ECMP_PBR_with_4_gw_different_interface(self):
        rc = routecli.add_route_policy(**ecmp_cli_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_147_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']
        icmp_dict['IP']['src'] = Parameter.SRC_HOST
        icmp_dict['IP']['dst'] = Parameter.DST_HOST

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()
        checkres = check_packets(exportres, expect_pkt_dict, fwports)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_147_04_del_route(self):
        delres = routeapi.del_route_policy_by_name(ecmp_cli_rt_dict['name'])
        logger.info('del route result: {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")


class Test_096_Function_test_when_has_4_gateways_the_third_one_is_down(Test):
    uuid = "SOSAIOT-TC-55956"

    def test_096_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '096')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_096_02_Add_IPv4_ECMP_PBR_via_CLI(self):
        rc = routecli.add_route_policy(**ecmp_cli_rt_dict)
        Assertion.assert_equal(rc, True, "ERR:ADD ecmp failed")

    def test_096_03_shutdown_X3(self):
        rc = interfacecli.shutdown_interface("X3")
        Assertion.assert_equal(rc, True, "ERR:shutdown X3 failed")

    def test_096_04_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X4']

        time.sleep(10)
        logger.info('wait for 10s')
        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_096_05_shutdown_X2(self):
        rc = interfacecli.shutdown_interface("X2")
        Assertion.assert_equal(rc, True, "ERR:shutdown X2 failed")

    def test_096_06_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X4']

        time.sleep(10)
        logger.info('wait for 10s')
        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_096_07_shutdown_X4(self):
        rc = interfacecli.shutdown_interface("X4")
        Assertion.assert_equal(rc, True, "ERR:shutdown X4 failed")

    def test_096_08_send_traffic_and_check_packet(self):
        fwports = ['X1']

        time.sleep(10)
        logger.info('wait for 10s')
        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")


class Test_100_Function_test_when_has_4_gateways_the_third_one_is_back(Test):
    uuid = "SOSAIOT-TC-55957"

    def test_100_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '100')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_100_02_no_shutdown_X3(self):
        noshutdownres = interfacecli.no_shutdown_interface("X3")
        logger.info('no shutdown X3 :'.format(noshutdownres))
        restartres = restartapi.restart_now()
        logger.info('restart DUT :'.format(restartres))
        Assertion.assert_equal(
            noshutdownres & restartres,
            True,
            "ERR:no shutdown X3 failed")

    def test_100_03_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X3']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_100_04_no_shutdown_X4(self):
        noshutdownres = interfacecli.no_shutdown_interface("X4")
        logger.info('no shutdown X4 :'.format(noshutdownres))
        restartres = restartapi.restart_now()
        logger.info('restart DUT :'.format(restartres))
        Assertion.assert_equal(
            noshutdownres & restartres,
            True,
            "ERR:no shutdown X4 failed")

    def test_100_05_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X3', 'X4']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()

        checkres = check_packets(exportres, expect_pkt_dict, fwports)
        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_100_06_no_shutdown_X2(self):
        noshutdownres = interfacecli.no_shutdown_interface("X2")
        logger.info('no shutdown X2 :'.format(noshutdownres))
        restartres = restartapi.restart_now()
        logger.info('restart DUT :'.format(restartres))
        Assertion.assert_equal(
            noshutdownres & restartres,
            True,
            "ERR:no shutdown X2 failed")

    def test_100_07_send_traffic_and_check_packet(self):
        fwports = ['X1', 'X2', 'X3', 'X4']

        clearres = pkgmonitorapi.clear_packets()
        logger.info('clear packets result: {}.'.format(clearres))
        startres = pkgmonitorapi.start_capture()
        logger.info('start capture result:{}'.format(startres))
        sendres = scapysend.send_icmp_packet(**icmp_dict)
        logger.info('Send icmp packet result:{}'.format(sendres))
        stopres = pkgmonitorapi.stop_capture()
        logger.info('stop capture result:{}.'.format(stopres))
        exportres = pkgmonitorapi.export_captured_packets()
        checkres = check_packets(exportres, expect_pkt_dict, fwports)

        Assertion.assert_equal(
            checkres, True, "ERR:the traffic is not as expected")

    def test_100_08_del_route(self):
        # init route configure
        delres = routeapi.del_route_policy_by_name(ecmp_cli_rt_dict['name'])
        logger.info('delete route result : {}'.format(delres))
        Assertion.assert_equal(delres, True, "ERR:the police delete failed")
