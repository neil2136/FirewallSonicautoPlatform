import re
import json
from definition.settings import *
from definition.utils import *


# Excepted:DHCP offer and DHCP ACK always shows the Generic options client requested
class TestBaseFunc_TC01(Test):
    uuid = "SOSAIOT-TC-55856"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']
    dest_ip = '100.100.100.100'
    router_ip = '50.50.50.50'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_33(self):
        dhcp_option_update = {
            "name": "option_33",
            "number": 33,
            "value": [
                {
                    "ip": self.dest_ip
                },
                {
                    "ip": self.router_ip
                }
            ],
            "array": True
        }
        dhcp_option_base_dict.update(dhcp_option_update)
        res = dhcpserverapi.add_dhcp_server_option_object(**dhcp_option_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option failed")

    def test_03_add_dhcp_scope_select_dhcp_option_and_enable_always_send_option_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "object": "option_33"
            },
            "always_send_option": True
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.add_dhcp_server_scope_dynamic(**dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True,
                               "ERR: add dhcp scope and select dhcp option and enable always send option for dynamic "
                               "scope failed")

    def test_04_config_packet_monitor(self):
        packetmonitorapi.monitor_default()
        monitor_conf_dict = {
            'monitor_filter': {
                'interfaces': 'x2',
                'ether_types': 'ip',
                'ip_types': 'udp',
                'destination_ports': '67,68',
            }
        }
        res = packetmonitorapi.conf_packmon(**monitor_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config packet monitor failed")

    def test_05_check_generic_option_in_dhcp_packets(self):
        flag = False
        list1 = ['(33) Static Route']
        list2 = ['(33) Static Route', f'Destination IP Address: {self.dest_ip}',
                 f'Destination Router: {self.router_ip}']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Discover', list1)
                checkres2 = check_dhcp_packets(packetslist, 'Offer', list2)
                checkres3 = check_dhcp_packets(packetslist, 'ACK', list2)
                logger.info(f'check Offer packet result is: {checkres2}, ACK packets result is:{checkres3} and '
                            f'Discover packets result is {checkres1} ')
                flag = True if checkres2 and checkres3 and (not checkres1) else False
        Assertion.assert_equal(flag, True, "ERR: check generic option failed")


# Excepted:DHCP offer /Ack shows Generic options only if the client requested these options using option55
class TestBaseFunc_TC02(Test):
    uuid = "SOSAIOT-TC-55857"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']
    dest_ip = '100.100.100.100'
    router_ip = '50.50.50.50'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_disable_always_send_option_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "object": "option_33"
            },
            "always_send_option": False
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True,
                               "ERR: disable always send option dynamic scope failed")

    def test_03_check_generic_option_in_dhcp_packets(self):
        flag = False
        list1 = ['(33) Static Route']
        list2 = ['(33) Static Route', f'Destination IP Address: {self.dest_ip}',
                 f'Destination Router: {self.router_ip}']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1', 'static-routes')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Discover', list1)
                checkres2 = check_dhcp_packets(packetslist, 'Offer', list2)
                checkres3 = check_dhcp_packets(packetslist, 'ACK', list2)
                logger.info(f'check Offer packet result is: {checkres2}, ACK packets result is:{checkres3} and '
                            f'Discover packets result is {checkres1} ')
                flag = True if checkres2 and checkres3 and checkres1 else False
        Assertion.assert_equal(flag, True, "ERR: check generic option failed")


# Excepted: DHCP Generic options doesnt interfere other DHCP options
class TestBaseFunc_TC03(Test):
    uuid = "SOSAIOT-TC-55858"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']
    option_ip = '10.10.10.1'
    call_manager_ip = '20.20.20.1'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_150(self):
        dhcp_option_update = {
            "name": "option_150",
            "number": 150,
            "value": [
                {
                    "ip": self.option_ip
                }
            ],
            "array": False
        }
        dhcp_option_base_dict.update(dhcp_option_update)
        res = dhcpserverapi.add_dhcp_server_option_object(**dhcp_option_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option 150 failed")

    def test_03_select_option_150_and_type_call_manager_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "object": "option_150"
            },
            "always_send_option": False,
            "call_manager": {
                "primary": self.call_manager_ip,
                "secondary": "",
                "tertiary": ""
            }
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True, "ERR: select option 150 and type call manager ip for dynamic scope failed")

    def test_04_check_option_150_in_dhcp_packets(self):
        flag = True
        list = ['(150) TFTP Server Address', 'TFTP Server Address: {self.call_manager_ip}',
                f'TFTP Server Address: {self.option_ip}']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1', 'local-150')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Offer', list)
                checkres2 = check_dhcp_packets(packetslist, 'ACK', list)
                logger.info(f'check Offer packet result is: {checkres1} and ACK packet result is:{checkres2}')
                if checkres1 and checkres2:
                    for packets in packetslist:
                        if 'DHCP: Offer' in packets:
                            matchres = re.findall(r'\(150\) TFTP Server Address', str(packets), re.I | re.DOTALL)
                            logger.info(matchres)
                            if matchres and len(matchres) == 2:
                                logger.info(
                                    'Option: (150) TFTP Server Address occurs occurs two times in offer packets')
                                flag = True
        Assertion.assert_equal(flag, True, "ERR: check generic option failed")


# Excepted:The DHCP server OFFER/ACK packet should show only one DHCP option with Tag Number 230
class TestBaseFunc_TC06(Test):
    uuid = "SOSAIOT-TC-55860"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_230(self):
        dhcp_option_update = {
            "name": "option_230",
            "number": 230,
            "value": [
                {
                    "ip": "130.130.130.130"
                }
            ],
            "array": False
        }
        dhcp_option_base_dict.update(dhcp_option_update)
        res = dhcpserverapi.add_dhcp_server_option_object(**dhcp_option_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option failed")

    def test_03_select_option_230_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "object": "option_230"
            },
            "always_send_option": False
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True, "ERR: select option 150 and type call manager ip for dynamic scope failed")

    def test_04_check_option_230_in_dhcp_packets(self):
        flag = False
        list = ['Option: (230) Private', 'Value: 82828282']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1', 'private1')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Offer', list)
                checkres2 = check_dhcp_packets(packetslist, 'ACK', list)
                logger.info(f'check Offer packet result is: {checkres1} and Ack packet result is:{checkres2}')
                if checkres1 and checkres2:
                    for packets in packetslist:
                        if 'DHCP: Offer' in packets:
                            matchres = re.findall(r'Option: \(230\) Private', str(packets), re.I | re.DOTALL)
                            logger.info(matchres)
                            if matchres and len(matchres) == 1:
                                logger.info('Option: (230) Private occurs occurs one time in discover packets')
                                flag = True
        Assertion.assert_equal(flag, True, "ERR: check generic option failed")


# Excepted: Removing/Editing option objects in the option group take in effect immediately.
class TestBaseFunc_TC07(Test):
    uuid = "SOSAIOT-TC-55861"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_231(self):
        dhcp_option_update = {
            "name": "option_231",
            "number": 231,
            "value": [
                {
                    "ip": "140.140.140.140"
                }
            ],
            "array": False
        }
        dhcp_option_base_dict.update(dhcp_option_update)
        res = dhcpserverapi.add_dhcp_server_option_object(**dhcp_option_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option failed")

    def test_03_add_dhcp_option_group_include_option_230_231(self):
        dhcp_option_group_update = {
            "name": "option_group_230_231",
            "option": {
                "object": [
                    {
                        "name": "option_230"
                    },
                    {
                        "name": "option_231"
                    }
                ]
            }
        }
        dhcp_option_group_base_dict.update(dhcp_option_group_update)
        res = dhcpserverapi.add_dhcp_server_option_group(**dhcp_option_group_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option failed")

    def test_04_select_dhcp_option_group_and_enable_always_send_option_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "group": "option_group_230_231"
            },
            "always_send_option": True
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True,
                               "ERR: select dhcp option and enable always send option for dynamic scope failed")

    def test_05_check_option_230_231_in_dhcp_packets(self):
        flag = False
        list = ['Option: (230) Private', 'Option: (231) Private', 'Value: 82828282', 'Value: 8c8c8c8c']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Offer', list)
                checkres2 = check_dhcp_packets(packetslist, 'ACK', list)
                logger.info(f'check Offer packet result is: {checkres1} and Ack packet result is:{checkres2}')
                if checkres1 and checkres2:
                    flag = True
        Assertion.assert_equal(flag, True, "ERR: check_generic_option_failed")

    def test_06_remove_option_231_from_group(self):
        dhcp_option_group_dict = {
            "option_object": [{"name": "option_230"}]
        }
        res = dhcpserverapi.edit_ipv4_dhcp_server_option_group('option_group_230_231', **dhcp_option_group_dict)
        Assertion.assert_equal(res, True, "ERR: remove dhcp option 231 failed")

    def test_07_check_option_230_231_in_dhcp_packets_after_remove_option_231_from_group(self):
        flag = False
        inlist = ['Option: (230) Private', 'Value: 82828282']
        outlist = ['Option: (231) Private', 'Value: 8c8c8c8c']
        start_capture_and_clear_packets(packetmonitorapi)
        ip_addr = get_dhcp_lease(PC2_Login, 'eth1')
        logger.info(f'get ip address :{ip_addr}')
        if ip_addr:
            packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
            if packetslist:
                checkres1 = check_dhcp_packets(packetslist, 'Offer', inlist)
                checkres2 = check_dhcp_packets(packetslist, 'Offer', outlist)
                logger.info(
                    f'check Offer packet list {inlist} result is: {checkres1} and list {outlist} result is:{checkres2}')
                if checkres1 and not checkres2:
                    flag = True
        Assertion.assert_equal(flag, True, "ERR: check generic option failed")


# Excepted: DHCP option 43 accept all types of option values on DHCP Advanced Settings page
class TestBaseFunc_TC08(Test):
    uuid = "SOSAIOT-TC-55862"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_43(self):
        dhcp_option_update = {
            "name": "option_43",
            "number": 43,
            "value": [
                {
                    "ip": "11.11.11.1"
                }
            ],
            "array": False
        }
        dhcp_option_base_dict.update(dhcp_option_update)
        res = dhcpserverapi.add_dhcp_server_option_object(**dhcp_option_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option failed")

    def test_03_select_option_43_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "object": "option_43"
            },
            "always_send_option": True
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True, "ERR: select option 150 and type call manager ip for dynamic scope failed")

    def test_04_check_dhcp_option_all_types(self):
        valuelist = [{"ip": "11.11.11.1"}, {"string": "good"}, {"one_byte": "254"}, {"two_byte": "65534"},
                     {"four_byte": "4294967295"}, {"hex_string": "c0a86401"}, {"domain_name": "www.google.com"},
                     {"boolean": 1}]
        checklist = ["Option: (43) Vendor-Specific Information"]
        checkres = []
        checklog = []
        for value in valuelist:
            logger.info(f'----------------start to test option 43:{value}---------------------------')
            dhcp_option_update = {"name": "option_43", "number": 43, "value": [value], "array": False}
            logger.info(dhcp_option_update)
            dhcp_option_base_dict.update(dhcp_option_update)
            logger.info(dhcp_option_dict)
            res = dhcpserverapi.edit_dhcp_server_option_object('option_43', **dhcp_option_dict)
            if res:
                start_capture_and_clear_packets(packetmonitorapi)
                ip_addr = get_dhcp_lease(PC2_Login, 'eth1')
                logger.info(f'get ip address :{ip_addr}')
                if ip_addr:
                    packetslist = get_packets_txt(packetmonitorapi, PC1_Login)
                    time.sleep(5)
                    if packetslist:
                        res = check_dhcp_packets(packetslist, 'Offer', checklist)
                        checkres.append(res)
                        checklog.append(f'check option value {value} is: {res}')
                    else:
                        logger.error("Error:didn't capture dhcp packets")
                        checkres.append(False)
                else:
                    logger.error("Error:PC2 didn't get ip address")
                    checkres.append(False)
            else:
                logger.error('Error: edit option 43 failied')
                checkres.append(False)
            releaseres = release_dhcp_lease(PC2_Login, 'eth1')
            logger.info(releaseres is {releaseres})
        else:
            logger.info(f'checkres is {checkres}, checklog is {checklog}')
        Assertion.assert_equal(all(checkres), True, "ERR: check_generic_option_failed")


# Excepted: DHCP option 43 accept all types of option values DHCP Generic Option Group
class TestBaseFunc_TC09(Test):
    uuid = "SOSAIOT-TC-55863"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_dhcp_option_group_include_option_43(self):
        dhcp_option_group_update = {
            "name": "option_group_43",
            "option": {
                "object": [
                    {
                        "name": "option_43"
                    }
                ]
            }
        }
        dhcp_option_group_base_dict.update(dhcp_option_group_update)
        res = dhcpserverapi.add_dhcp_server_option_group(**dhcp_option_group_dict)
        Assertion.assert_equal(res, True, "ERR: add dhcp option group failed")

    def test_03_select_dhcp_option_and_enable_always_send_option_for_dynamic_scope(self):
        dhcp_scope_update = {
            "from": Parameter.START_IP,
            "to": Parameter.END_IP,
            "enable": True,
            "lease_time": 1440,
            "default_gateway": Parameter.X2_IP,
            "generic_option": {
                "group": "option_group_43"
            },
            "always_send_option": True
        }
        dhcp_server_dynamic_base_dict.update(dhcp_scope_update)
        logger.info(f'dict is {dhcp_server_dynamic_scope_dict}')
        res = dhcpserverapi.edit_dhcp_server_scope_v4('dynamic', Parameter.START_IP, Parameter.END_IP,
                                                      **dhcp_server_dynamic_scope_dict)
        Assertion.assert_equal(res, True,
                               "ERR: select dhcp option and enable always send option for dynamic scope failed")

    def test_04_check_dhcp_option_all_types_in_group(self):
        TestBaseFunc_TC08().test_04_check_dhcp_option_all_types()


# Excepted: Configuration imported/exported properly. Shows DHCP option and option groups settings preserved.
class TestBaseFunc_TC04(Test):
    uuid = "SOSAIOT-TC-55859"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_export_exp_file(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/dhcp_server_generic_option_settings_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_03_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_04_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/dhcp_server_generic_option_settings_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_05_check_dhcp_options_settings(self):
        time.sleep(10)
        optionlist = ['option_43', 'option_230', 'option_231', 'option_33', 'option_150']
        # optionlist = ['option_43', 'option_230', 'option_231', 'option_33', 'option_150']
        output = dhcpserverapi.get_dhcp_server_option_object()
        checkres = [i in str(json.dumps(output)) for i in optionlist]
        logger.info(f'option check result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check dhcp options settings failed.")

    def test_06_check_dhcp_option_group_settings(self):
        time.sleep(10)
        optiongrouplist = ['option_group_43', 'option_group_230_231']
        output = dhcpserverapi.get_dhcp_server_option_group()
        flag = True if all(i in str(output) for i in optiongrouplist) else False
        Assertion.assert_equal(flag, True, "ERR: check dhcp option groups settings failed.")
