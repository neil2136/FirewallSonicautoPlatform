from settings import *
from utils import *


class Test_01_MTU_NF_UDP_Packet_02(Test):
    """
    1. Send 1500 byte UDP packet while Ignore Don't Fragment Flag is disabled in X1. the packet do not be forwarded.
    2. Send 1500 byte UDP packet while Ignore Don't Fragment Flag is enabled in X1. the packet will forwarded.
    3. Send 512 byte UDP packet while Ignore Don't Fragment Flag is enabled in X1. the packet will forwarded.
    """
    uuid = "SOSAIOT-TC-56862"
    description = show_testcase_info(
        Parameter.TESTPLAN, "01", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_01_config_x1_mtu(self):
        output = interface.config_interface(**Parameter.x1_Config)
        Assertion.assert_equal(output, True, "ERR: Config X1 MTU failed")

    def test_01_02_config_packet_monitor(self):
        output = packetmonitor.conf_packmon(**packer_monitor_config)
        packetmonitor.start_capture()
        packetmonitor.clear_packets()
        Assertion.assert_equal(
            output, True, "ERR: Config packet monitor failed")

    def test_01_03_send_udp_packet_1500_NF(self):
        # Send 1500 byte UDP packet while Ignore Don't Fragment Flag is
        # disabled in X1. the packet do not be forwarded.
        udpconf = {'lenth': 1458, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        # sendoutput = packetsend.send_udp_packet(**udp_packet)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)

        # # Assertion.assert_regular(resp, 'Forwarded', "ERR: UDP packets were not be fragmented.")
        Assertion.assert_equal(
            forwarded,
            False,
            "ERR: UDP packets is be forwarded via X1.")

    def test_01_04_send_udp_packet_1492_ignoreNF(self):
        # Send 1500 byte UDP packet while Ignore Don't Fragment Flag is enabled
        # in X1. the packet will forwarded.
        ignorenf = {'ignore_df_bit': True}
        Parameter.x1_Config.update(ignorenf)
        interconf = interface.config_interface(**Parameter.x1_Config)
        logger.info(interconf)

        packetmonitor.start_capture()
        packetmonitor.clear_packets()

        udpconf = {'lenth': 1450, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)
        Assertion.assert_equal(
            forwarded,
            True,
            "ERR: UDP packets is not be forwarded via X1.")

    def test_01_05_send_udp_packet_512_ignoreNF(self):
        # Send 512 byte UDP packet while Ignore Don't Fragment Flag is enabled
        # in X1. the packet will forwarded.
        packetmonitor.start_capture()
        packetmonitor.clear_packets()

        udpconf = {'lenth': 460, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)
        Assertion.assert_equal(
            forwarded,
            True,
            "ERR: UDP packets is not be forwarded via X1.")


class Test_02_VPN_MTU_NF_UDP_Packet_05(Test):
    """
    1. VPN tunnel is up
    2. Send 1500 byte UDP packet while Ignore Don't Fragment Flag is disabled in VPN advanced. the packet do not be forwarded.
    3. Send 1500 byte UDP packet while Ignore Don't Fragment Flag is enabled in VPN advanced. the packet will forwarded.
    4. Send 512 byte UDP packet while Ignore Don't Fragment Flag is enabled in VPN advanced. the packet will forwarded.
    """
    uuid = "SOSAIOT-TC-56864"
    description = show_testcase_info(
        Parameter.TESTPLAN, "02", description=True)['title']
    GEN7-28917
    
    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_01_config_x1_mtu(self):
        output = interface.config_interface(**Parameter.x1_Config)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config X1 MTU failed")

    def test_02_02_add_s2s_local_vpn(self):
        localao.config_addressobject(**local_ao_dict)
        localvpn.add_vpn_policy(**local_s2svpn_dict)
        vpnentry = localvpn.show_s2svpnpolicy()
        output = vpn_name_check(vpnentry, local_s2svpn_dict['name'])
        logger.info(output)
        Assertion.assert_equal(
            output, True, "ERR: Add local vpn policy failed.")

    def test_02_03_add_s2s_remote_vpn(self):
        remoteinterface.config_interface(**remote_x0_config)
        remotevpn.delete_allvpnpolicy()

        remoteao.add_address_object(**remote_ao_dict)
        remotevpn.add_vpnpolicy(**remote_s2svpn_dict)
        output = remotevpn.show_allvpnpolicy()
        Assertion.assert_regular(
            output,
            remote_s2svpn_dict['name'],
            "ERR: Add remote vpn policy failed")

    def test_02_04_config_packet_monitor(self):
        output = packetmonitor.conf_packmon(**vpn_packer_monitor_config)
        packetmonitor.start_capture()
        packetmonitor.clear_packets()
        Assertion.assert_equal(
            output, True, "ERR: Config packet monitor failed")

    def test_02_05_send_udp_packet_1500_NF(self):
        # Send 1500 byte UDP packet while Ignore Don't Fragment Flag is
        # disabled in VPN advanced. the packet do not be forwarded.
        vpndf = {'ignore_df_bit': False}
        vpn_advanced_setting_dict.update(vpndf)
        advoutput = localvpnadvanced.config_vpnadvanced(
            **vpn_advanced_setting_dict)
        logger.info(advoutput)

        udpconf = {'dst': Parameter.VPN2_Host, 'lenth': 1458, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)

        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)

        # # Assertion.assert_regular(resp, 'Forwarded', "ERR: UDP packets were not be fragmented.")
        Assertion.assert_equal(
            forwarded,
            False,
            "ERR: UDP packets is be forwarded via X1.")

    def test_02_06_send_udp_packet_1492_ignoreNF(self):
        # Send 1500 byte UDP packet while Ignore Don't Fragment Flag is enabled
        # in VPN advanced. the packet will forwarded.
        vpndf = {'ignore_df_bit': True}
        vpn_advanced_setting_dict.update(vpndf)
        advoutput = localvpnadvanced.config_vpnadvanced(
            **vpn_advanced_setting_dict)
        logger.info(advoutput)

        packetmonitor.start_capture()
        packetmonitor.clear_packets()

        udpconf = {'dst': Parameter.VPN2_Host, 'lenth': 1450, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)
        Assertion.assert_equal(
            forwarded,
            True,
            "ERR: UDP packets is not be forwarded via X1.")

    def test_02_07_send_udp_packet_512_ignoreNF(self):
        # Send 512 byte UDP packet while Ignore Don't Fragment Flag is enabled
        # in VPN advanced. the packet will forwarded.
        packetmonitor.start_capture()
        packetmonitor.clear_packets()

        udpconf = {'dst': Parameter.VPN2_Host, 'lenth': 460, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)
        Assertion.assert_equal(
            forwarded,
            True,
            "ERR: UDP packets is not be forwarded via X1.")

    def test_02_08_send_udp_packet_1492_ignoreNF_nonvpn(self):
        # Send 1500 byte UDP packet while Ignore Don't Fragment Flag is enabled
        # in X1. the packet will forwarded.
        ignorenf = {'ignore_df_bit': True}
        Parameter.x1_Config.update(ignorenf)
        interconf = interface.config_interface(**Parameter.x1_Config)
        logger.info(interconf)

        packetmonitor.start_capture()
        packetmonitor.clear_packets()

        udpconf = {'lenth': 1450, 'flags': 2}
        send_udp_conf.update(udpconf)
        sendoutput = send_udp_data_packet(send_udp_conf)
        logger.info(sendoutput)
        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()

        forwarded = udp_forworded_check(
            resp, Parameter.X1_IP, Parameter.Dst_IP)
        logger.info(forwarded)
        Assertion.assert_equal(
            forwarded,
            True,
            "ERR: UDP packets is not be forwarded via X1.")
