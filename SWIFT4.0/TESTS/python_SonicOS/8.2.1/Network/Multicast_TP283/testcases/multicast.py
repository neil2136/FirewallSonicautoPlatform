from definition.settings import *
from definition.utils import *

# clients can not receive multicast data between x0 and x3 while timeout state.
class Testmulti_TC12(Test):
    uuid = "SOSAIOT-TC-52908"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_igmp_state_table(self):
        tag = False
        for i in range(3):
            logger.info(f'time {i}: start check the igmp state tale in fw...')
            cmd = "sendip -d '0x2200efe90000000104000000e00a0a0a' " + \
                  "-p ipv4 -ip 02 -is {} -it 1 -id 224.0.0.22 224.0.0.22".format(Parameter.LAN_PC)
            logger.info(f'sendip cmd: {cmd}')
            cmdres = PC1_login.send_command(cmd)
            logger.info(f'run cmd in pc1 result: {cmdres}')
            output = multicastapi.show_state_table()
            logger.info(f'check state table result: {output}')
            res = True if multicast_dict['value'] in str(output) else False
            if res:
                tag = True
                break
            else:
                logger.error("Get IGMP stat table failed.")
                time.sleep(10)
        Assertion.assert_equal(tag, True, "ERR: Check state table failed")

    def test_03_timeout_igmp_state_table(self):
        logger.info("Check IGMP state table after timeout")
        time.sleep(61)
        output = multicastapi.show_state_table()
        logger.info(f'show state table result: {output}')
        res = True if 'Time EXPIRED' in str(output) else False
        Assertion.assert_equal(res, True, "ERR: Check state table failed")


# Disable Multicast at the Multicast Page will disable all multicast data reception in X3
class Testmulti_TC16(Test):
    uuid = "SOSAIOT-TC-52909"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_enable_and_check_multicast_in_x0x3(self):
        serverres = run_igmp_server(script_path, 'run_server.py', 'igmpserver.py', Parameter.WAN_PC)
        logger.info(f'run igmp server in pc2 result: {serverres}')

        logger.info(f'client cmd: {IGMP_CLIENT_CMD}')
        pc1res = PC1_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc1 result: {pc1res}')

        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')
        clientres = True if 'TEST PASS' in pc1res and 'TEST PASS' in pc3res else False
        Assertion.assert_equal(clientres, True, "ERR: Test igmp traffic on X0, X3 failed")

    def test_03_disable_and_check_multicast_on_x3(self):
        multi_dict = {'multicast': False}
        confres = multicastapi.config_multicast(**multi_dict)
        logger.info(f'disable multicast result: {confres}')

        logger.info(f'client cmd: {IGMP_CLIENT_CMD}')
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')

        pc3res = True if 'TEST PASS' not in pc3res else False
        Assertion.assert_equal(confres & pc3res, True, "ERR: Test igmp traffic on X3 failed")

    def test_04_enable_multicast(self):
        multi_dict = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 1,
            'reception_name': multicast_dict["name"],
        }
        confres = multicastapi.config_multicast(**multi_dict)
        Assertion.assert_equal(confres, True, "ERR: enable multicast failed")


# igmp sending will be blocked after disabled multicast in X0,X1
class Testmulti_TC17(Test):
    uuid = "SOSAIOT-TC-52910"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_join_form_lan_to_wan(self):
        pcres = PC1_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc1 result: {pcres}')
        res = True if 'TEST PASS' in pcres else False
        Assertion.assert_equal(res, True, "ERR: Test igmp join failed")

    def test_03_disable_x0_multicast_and_check_join(self):
        logger.info("Disable multicast...")
        x0_static_dict['multicast'] = False
        x0confres = interfaceapi.config_interface(**x0_static_dict)
        logger.info(f'config x0 to disable multicast result: {x0confres}')

        logger.info(f'client cmd: {IGMP_CLIENT_CMD}')
        pcres = PC1_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc1 result: {pcres}')
        joinres = True if 'TEST PASS' not in pcres else False

        # init x0 settings
        x0_static_dict['multicast'] = True
        interfaceapi.config_interface(**x0_static_dict)
        Assertion.assert_equal(x0confres & joinres, True, "ERR: Test igmp join on X0 failed")


# igmp sending are received on X0 but not on X2
class Testmulti_TC02(Test):
    uuid = "SOSAIOT-TC-52911"
    description = show_testcase_info(TESTPLAN, '02', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_join_form_x0_and_x2_to_wan(self):
        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()

        logger.info(f'client cmd: {IGMP_CLIENT_CMD}')
        pcres = PC1_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc1 result: {pcres}')

        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()
        (res1, checkres1) = packet_igmp_check(resp, Parameter.FIREWALL, Parameter.MULTI_GROUP_IP)
        logger.info(checkres1)
        (res2, checkres2) = packet_igmp_check(resp, Parameter.X2_IP, Parameter.MULTI_GROUP_IP)
        logger.info(checkres2)
        res = res1 & (True if not res2 else False)
        Assertion.assert_equal(res, True, "ERR: Multicast packets are received failed")


# Enable/Disable Multicast Checkbox will control all multicast data reception in X3
class Testmulti_TC33(Test):
    uuid = "SOSAIOT-TC-52912"
    description = show_testcase_info(TESTPLAN, '33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_and_check_multicast_on_x3(self):
        multi_dict = {'multicast': False}
        confres = multicastapi.config_multicast(**multi_dict)
        logger.info(f'disable multicast result: {confres}')

        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')

        pc3res = True if 'TEST PASS' not in pc3res else False
        Assertion.assert_equal(confres & pc3res, True, "ERR: Test igmp sending on X3 failed")

    def test_03_enable_multicast(self):
        multi_dict = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 4,
            'reception_name': 'all',
        }
        res = multicastapi.config_multicast(**multi_dict)
        Assertion.assert_equal(res, True, "ERR: enable multicast in page failed")

    def test_04_conf_acl_dmz_to_multi_allow(self):
        res = True
        show_accessrule = {
            'version': 'ipv4',
            'from': 'DMZ',
            'to': 'MULTICAST',
        }
        showaclres = accessrulecli.show_access_rules(**show_accessrule)
        splitres = showaclres.split('access-rule ipv4')
        for rule in splitres:
            rule_dict = {
                'from': 'DMZ',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in rule:
                searchres = re.search(r'service (\w+)\s?(\w+)?', rule, re.I | re.S)
                if searchres:
                    if searchres.group(1) == 'group':
                        rule_dict['service_group'] = searchres.group(2)
                else:
                    logger.info('can not search service group in current rule str')
                res &= accessrulecli.edit_access_rule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: config acl dmz to multi allow failed")

    def test_05_check_multicast_in_dmz_host(self):
        # serverres = run_igmp_server(script_path, 'run_server.py', 'igmpserver.py', Parameter.WAN_PC)
        # logger.info(f'run igmp server in pc2 result: {serverres}')

        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')
        res = True if 'TEST PASS' in pc3res else False
        Assertion.assert_equal(res, True, "ERR: Test igmp sending on X3 failed")

# Enable/Disable Multicast Checkbox will control all multicast data reception in X3
class Testmulti_TC34(Test):
    uuid = "SOSAIOT-TC-52913"
    description = show_testcase_info(TESTPLAN, '34', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_igmp_membership_and_check(self):
        multi_dict = {
            'multicast': True,
            'require_igmp_membership': False,
            'timeout': 4,
            'reception_name': 'all',
        }
        confres = multicastapi.config_multicast(**multi_dict)
        logger.info(f'disable multicast result: {confres}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        time.sleep(5)
        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()
        (res, checkres) = packet_membership_disable_check(resp, Parameter.WAN_PC, Parameter.MULTI_GROUP_IP)
        logger.info(checkres)
        Assertion.assert_equal(res, True, "ERR: check igmp membership failed")

    def test_03_enable_igmp_membership_and_check(self):
        multi_dict = {
            'multicast': True,
            'require_igmp_membership': True,
            'timeout': 4,
            'reception_name': 'all',
        }
        confres = multicastapi.config_multicast(**multi_dict)
        logger.info(f'disable multicast result: {confres}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        time.sleep(5)
        packetmonitorapi.stop_capture()
        resp = packetmonitorapi.export_captured_packets()
        (res, checkres) = packet_membership_enable_check(resp, Parameter.WAN_PC, Parameter.MULTI_GROUP_IP)
        logger.info(checkres)
        Assertion.assert_equal(res, True, "ERR: check igmp membership failed")

# Enable/Disable Multicast in x3 will control multicast data reception.
class Testmulti_TC38(Test):
    uuid = "SOSAIOT-TC-52914"
    description = show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_disable_and_check_multicast_on_x3(self):
        x1_static_dict['multicast'] = False
        x1res = interfaceapi.config_interface(**x1_static_dict)

        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        pc3cmdres = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3cmdres}')

        pc3res = True if 'TEST PASS' not in pc3cmdres else False
        Assertion.assert_equal(x1res & pc3res, True, "ERR: Test igmp traffic on X3 failed")

    def test_03_enable_X1_multicast_and_conf_wan_to_multi_acl(self):
        show_acl_dict = {
            'version': 'ipv4',
            'from': 'WAN',
            'to': 'MULTICAST',
        }
        x1_static_dict['multicast'] = True
        res = interfaceapi.config_interface(**x1_static_dict)

        showaclres = accessrulecli.show_access_rules(**show_acl_dict)
        splitres = showaclres.split('access-rule ipv4')
        for rule in splitres:
            rule_dict = {
                'from': 'WAN',
                'to': 'MULTICAST',
                'action': 'deny',
                'action_new': 'allow',
            }
            if 'action deny' in rule:
                searchres = re.search(r'service (\w+)\s?(\w+)?', rule, re.I | re.S)
                if searchres:
                    if searchres.group(1) == 'group':
                        rule_dict['service_group'] = searchres.group(2)
                else:
                    logger.info('can not search service group in current rule str')
                res &= accessrulecli.edit_access_rule(**rule_dict)
        Assertion.assert_equal(res, True, "ERR: disable multicast in X1 and config acl failed")

    @repeat_method(3)
    def test_03_enable_and_check_multicast_on_x3(self):
        serverres = run_igmp_server(script_path, 'run_server.py', 'igmpserver.py', Parameter.WAN_PC)
        logger.info(f'run igmp server in pc2 result: {serverres}')
        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        time.sleep(20)
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')
        clientres = True if 'TEST PASS' in pc3res else False
        Assertion.assert_equal(clientres, True, "ERR: Test igmp traffic from lan to wan failed")


# igmp v2 and v3 sending are received from wan host
class Testmulti_TC06(Test):
    uuid = "SOSAIOT-TC-52916"
    description = show_testcase_info(TESTPLAN, '06', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_igmp_v3_check(self):
        serverres = run_igmp_server(script_path, 'run_server.py', 'igmpserver.py', Parameter.WAN_PC)
        logger.info(f'run igmp server in pc2 result: {serverres}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')
        packetmonitorapi.stop_capture()
        packetmonitorapi.export_captured_packets_pcapng()
        cmd2 = 'tshark -R "ip.addr == 224.0.0.22 and igmp.version == 3" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres = PC1_login.send_command(cmd2)
        logger.info(f'fitter igmp packet result: {pc1cmdres}')
        res = True if 'IGMP Version: 3' in pc1cmdres else False
        Assertion.assert_equal(res, True, "ERR: check igmp v3 membership failed")

    def test_03_change_igmpv3_to_v2_check(self):
        cmd = 'echo "2" > /proc/sys/net/ipv4/conf/eth1/force_igmp_version'
        pc3res = PC3_login.send_command(cmd)
        logger.info(f'change pc3 eth1 igmp version result: {pc3res}')

        packetmonitorapi.start_capture()
        packetmonitorapi.clear_packets()
        logger.info(f'start run client cmd: {IGMP_CLIENT_CMD}')
        pc3res = PC3_login.send_command(IGMP_CLIENT_CMD)
        logger.info(f'run igmp client in pc3 result: {pc3res}')
        packetmonitorapi.stop_capture()
        packetmonitorapi.export_captured_packets_pcapng()
        cmd2 = 'tshark -R "ip.addr == 224.0.0.2 and igmp.version == 2" -r /tmp/packet-c.pcapng -V -T text'
        pc1cmdres = PC1_login.send_command(cmd2)
        logger.info(f'fitter igmp packet result: {pc1cmdres}')
        res = True if 'IGMP Version: 2' in pc1cmdres else False
        Assertion.assert_equal(res, True, "ERR: check igmp v2 membership failed")

    def test_04_init_igmp_version(self):
        cmd = 'echo "3" > /proc/sys/net/ipv4/conf/eth1/force_igmp_version'
        pc3res = PC3_login.send_command(cmd)
        logger.info(f'change pc3 eth1 igmp version result: {pc3res}')
        Assertion.assert_equal(True, True, "ERR: init igmp version failed")
