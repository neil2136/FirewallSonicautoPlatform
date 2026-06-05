from settings import *
from utils import *


class Test_01_Zone_Check_1(Test):
    """
    1. Login to the box, go to network->interface page
    2. edit the MGMT interface
    3. you will find the ZONE of the MGMT interface is MGMT
    """
    uuid = "SOSAIOT-TC-56850"
    description = show_testcase_info(
        Parameter.TESTPLAN, "01", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_01_config_mgmt_interface(self):
        mgmt_static_opt = {
            'if': 'MGMT',
            'zone': 'MGMT',
            'ip': Parameter.MGMT_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ping': True,

        }
        output = interface.config_interface(**mgmt_static_opt)
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: Config MGMT failed")

    def test_01_02_check_zone_pass(self):
        tag = False
        output = zonemember.get_reporting_zones_objects()
        logger.info(output)
        for zone in output:
            if zone['name'] == 'MGMT' and zone['member_interfaces']:
                tag = True
        Assertion.assert_equal(tag,  True, "ERR: Cannot found the member_interfaces MGMT in Objects Zones")


class Test_02_Static_Mode_Check_2(Test):
    """
    1.Login to the box, go to network->interface page
    2.edit the MGMT interface
    3.the mode is static ip mode
    """
    uuid = "SOSAIOT-TC-56851"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "02", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_01_get_mgmt_interface(self):

        mgmtstatus = interface.get_interface_status('MGMT')
        logger.info(mgmtstatus)
        try:
            mgmtmode = mgmtstatus['interfaces'][0]['ipv4']['ip_assignment']['mode']
            checkresult = True if 'static' in mgmtmode.keys() else False
        except BaseException:
            checkresult = False
        Assertion.assert_equal(
            checkresult,
            True,
            "ERR: The ip assignment was not static for the MGMT.")

    def test_02_02_check_mgmt_mode(self):
        mgmt_dhcp_dict = {
            'if': 'MGMT',
            'zone': 'MGMT',
            'mode': 'dhcp',
            'force-discover-interval': '9',  # or False
            'initiate-renewals-with-discover': True,
            'mgmt-https': True,
            'mgmt-ssh': True,
            'mgmt-snmp': True,
        }
        mgmtstatus = interface.config_interface(**mgmt_dhcp_dict)
        logger.info(mgmtstatus)
        Assertion.assert_equal(
            mgmtstatus,
            False,
            "ERR: The mode can be changed to DHCP.")


class Test_03_MGMT_IP_Check_5(Test):
    """
    1.Traffic to SonicOS via MGMT interface is only allowed for the configured IPs
    """
    uuid = "SOSAIOT-TC-56852"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "03", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_03_01_config_packet_monitor(self):
        packer_monitor_config = {
            'monitor_filter': {
                "interfaces": "MGMT,X1",
                'ether_types': '!0x69,!0x806',
                'ip_types': 'icmp',
                'source_ips': Parameter.MGMT_HOST
            }
        }
        packetmonitor.conf_packmon(**packer_monitor_config)
        packetmonitor.start_capture()
        packetmonitor.clear_packets()
        output = packetmonitor.show_packmon_setting()
        logger.info(output)
        try:
            output = output['packet_monitor']['monitor_filter']['source_ips']
        except BaseException:
            output = None
        Assertion.assert_regular(
            output,
            Parameter.MGMT_HOST,
            "ERR: can not find source ip in FW packets")

    def test_03_02_ping_mgmt_interface(self):
        packet = {
            'IP': {
                'src': Parameter.MGMT_HOST,
                'dst': Parameter.MGMT_IP
            },
        }
        output = packetsend.send_icmp_packet(**packet)
        logger.info(output)

        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()
        result_packet = icmp_reply_check(
            resp, Parameter.MGMT_IP, Parameter.MGMT_HOST)
        logger.info(result_packet)
        output = True if len(result_packet) > 0 else False
        Assertion.assert_equal(
            output, True, "ERR: Firewall is not reply the ICMP request.")


class Test_MGMT_Route_Check_6(Test):
    """
    1.Traffic cannot be routed via MGMT interface
    """
    uuid = "SOSAIOT-TC-56853"
    description = show_testcase_info(Parameter.TESTPLAN,
                                     "04", description=True)['title']

    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_04_01_config_packet_monitor(self):
        packer_monitor_config = {
            'monitor_filter': {
                "interfaces": "MGMT,X0",
                'ether_types': '!0x69,!0x806,!0x6a',
                'ip_types': 'icmp',
                'source_ips': Parameter.MGMT_HOST
            }
        }
        packetmonitor.conf_packmon(**packer_monitor_config)
        packetmonitor.start_capture()
        packetmonitor.clear_packets()
        output = packetmonitor.show_packmon_setting()
        logger.info(output)
        try:
            output = output['packet_monitor']['monitor_filter']['source_ips']
        except BaseException:
            output = None
        Assertion.assert_regular(
            output,
            Parameter.MGMT_HOST,
            "ERR: can not find source ip in FW packets")

    def test_04_02_route_mgmt_interface(self):
        packet = {
            'IP': {
                'src': Parameter.MGMT_HOST,
                'dst': Parameter.X1_HOST
            },
        }
        output = packetsend.send_icmp_packet(**packet)
        logger.info(output)

        packetmonitor.stop_capture()
        resp = packetmonitor.export_captured_packets()
        result_packet = icmp_drop_check(
            resp, Parameter.MGMT_HOST, Parameter.X1_HOST)
        logger.info(result_packet)
        output = True if len(result_packet) > 0 else False
        Assertion.assert_equal(
            output, True, "ERR: Firewall is not drop the ICMP request.")
