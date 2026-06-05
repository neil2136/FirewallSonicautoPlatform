from definition.settings import *
from definition.utils import *


#Box deleted entries from the ARP cache table
class Test_TC03(Test):
    uuid = "SOSAIOT-TC-55780"
    description = show_testcase_info(
        TESTPLAN, '3', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_clear_arp_cache(self):
        # clear arp cache
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')

    def test_03_unassign_interface(self):
        output = interfaceapi.unassign_interface(interface="X2")
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: unassign X2 failed")

    def test_04_check_arp_cache(self):
        output = arpapi.show_arp_caches()
        logger.info(output)
        Assertion.assert_not_regular(str(output), Parameter.DUT_X2_MAC,
                                     "ERR: Can found X2_MAC in arp cache")


# Box added new entries into the ARP cache table, include interface and host
class Test_TC02(Test):
    uuid = "SOSAIOT-TC-55760"
    description = show_testcase_info(
        TESTPLAN, '2', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_x2_interface(self):
        x2_static = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_check_arp_cache_pass(self):
        output = arpapi.show_arp_caches()
        logger.info(output)
        Assertion.assert_regular(str(output), Parameter.DUT_X2_MAC,
                                 "ERR: Cannot found DUT_X2_MAC in arp cache")

    def test_04_check_arp_cache_host_fail(self):
        output = arpapi.show_arp_caches()
        logger.info(output)
        Assertion.assert_not_regular(str(output), Parameter.X2_PC_MAC,
                                     "ERR: Can found X2_PC_MAC in arp cache")

    def test_05_check_arp_cache_host_pass(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        output1 = arpapi.show_arp_caches()
        logger.info(output1)
        Assertion.assert_regular(str(output1), Parameter.X2_PC_MAC,
                                 "ERR: Cannot found X2_PC_MAC in arp cache")


# Box responds to ARP request on LAN interface
class Test_TC01(Test):
    uuid = "SOSAIOT-TC-55760"
    description = show_testcase_info(
        TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_capture_packet_and_check_arp_response(self):
        res1 = PC2_login.send_command('arp -a')
        if Parameter.X2_IP in res1:
            PC2_login.send_command(f'arp -d {Parameter.X2_IP}')

        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')
        ping_from_pc_dict = {
            'pc_obj': PC2_login,
            'dest': Parameter.X2_IP
        }
        exportres = fw_packet_monitor_run(action='ping_from_pc', **ping_from_pc_dict)

        arpfilter = [
            'Address Resolution Protocol',
            'reply',
            f'Sender MAC address: {Parameter.DUT_X2_MAC}',
            f'Sender IP address: {Parameter.X2_IP}',
            f'Target MAC address: {Parameter.X2_PC_MAC}',
            f'Target IP address: {Parameter.DMZ_PC}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True, "ERR:  Firewall returned invalid ARP response")


# ARP Cache entry timeout (minutes) field accept correct value
class Test_TC04(Test):
    uuid = "SOSAIOT-TC-55781"
    description = show_testcase_info(
        TESTPLAN, '4', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_invalid_arp_timeout(self):
        reslist = []
        invalid_timeout = [0, 1, 601, 0.5, -3, '@', '~', '!#$%^&*(']
        for timeout in invalid_timeout:
            setres = arpapi.arp_setting(timeout=timeout)
            reslist.append(setres)
        Assertion.assert_equal(all(reslist), False, "ERR: set arp timeout failed")

    def test_03_set_valid_arp_timeout(self):
        reslist = []
        valid_timeout = [600, 50, 10, 2]
        for timeout in valid_timeout:
            setres = arpapi.arp_setting(timeout=timeout)
            reslist.append(setres)
        Assertion.assert_equal(all(reslist), True, "ERR: set arp timeout failed")


# ARP Countdown timer decrease expiration time.
class Test_TC05(Test):
    uuid = "SOSAIOT-TC-55782"
    description = show_testcase_info(
        TESTPLAN, '5', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_arp_cache(self):
        # clear arp cache
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')

        # ping from X2 pc
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")

        # check arp cache every 30 sec util disappear
        arp_timeout_list = []
        flaglist = []
        sleep_time = 30
        try:
            for each in range(0, 8):
                time.sleep(sleep_time)
                arpcaches = arpapi.show_arp_caches()
                if str.upper(Parameter.X2_PC_MAC) in str(arpcaches):
                    for arpcache in arpcaches:
                        if str.upper(Parameter.X2_PC_MAC) in str(arpcache):
                            arp_timeout = arpcache['expires_in_minutes']
                            arp_timeout_list.append(arp_timeout)
                            logger.info("arp entry is :{}".format(arpcache))
                else:
                    logger.info(
                        f'{Parameter.X2_PC_MAC} in arp is detele after {(each + 1) * sleep_time}s')
                    break

        except Exception as e:
            logger.info(
                "expected arpcache not found with error {}".format(
                    repr(e)))

        logger.info(arp_timeout_list)
        count = len(arp_timeout_list)
        for i in range(count - 1):
            if arp_timeout_list[i + 1] <= arp_timeout_list[i]:
                flaglist.append(True)
                i = i + 1
            else:
                flaglist.append(False)
        logger.info(flaglist)
        Assertion.assert_equal(all(flaglist), True, 
                               "ERR: ARP Countdown timer didn't decrease expiration time")


# ARP Statistics printed
class Test_TC06(Test):
    uuid = "SOSAIOT-TC-55783"
    description = show_testcase_info(
        TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_show_arp_statistics(self):
        statistics = arpapi.show_arp_statistics()
        checklist = [
            'entries',
            'lookups',
            'failures',
            'hits',
            'misses',
            'hit_rate']
        checkres = [x in statistics for x in checklist]
        logger.info(f'check result: {checkres}')
        flag = True if all(checkres) else False
        Assertion.assert_equal(flag, True, "ERR: ARP Statistics didn't print")


# Flush ARP connections Button working
class Test_TC07(Test):
    uuid = "SOSAIOT-TC-55784"
    description = show_testcase_info(
        TESTPLAN, '7', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_arp_cache_before_flush(self):
        # ping from X2 pc
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")

        # check arp cache
        arpcaches = arpapi.show_arp_caches()
        if str.upper(Parameter.X2_PC_MAC) in str(arpcaches):
            logger.info('arp chace is found')
            flag = True
        else:
            logger.info('arp chace can not find')
            flag = False

        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    @repeat_method(5)
    def test_03_check_arp_cache_after_flush(self):
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')

        time.sleep(5)
        # check arp cache
        arpcaches = arpapi.show_arp_caches()
        if str.upper(Parameter.X2_PC_MAC) in str(arpcaches):
            logger.info('arp chace is found')
            flag = False
        else:
            logger.info('arp chace can not find')
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ARP entry can find")


#  IP Address Validation check
class Test_TC13(Test):
    uuid = "SOSAIOT-TC-55764"
    description = show_testcase_info(
        TESTPLAN, '13', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp(self):
        reslist = []
        invalid_ip_list = [
            '256.1.1.1',
            '1.256.1.1',
            '1.1.256.1',
            '1.1.1.256',
            'badip',
            '~!@#$%^&*()']
        for invalid_ip in invalid_ip_list:
            arp_dict = copy.deepcopy(static_arp_dict)
            arp_dict['mac'] = Parameter.X2_PC_MAC
            arp_dict['ip'] = invalid_ip
            setres = arpapi.add_static_arp(**arp_dict)
            reslist.append(setres)
        logger.info(f'result list: {reslist}')
        Assertion.assert_equal(all(reslist), False, "ERR: invalid arp entry can be added")


#  MAC Validation check
class Test_TC14(Test):
    uuid = "SOSAIOT-TC-55765"
    description = show_testcase_info(
        TESTPLAN, '14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp(self):
        reslist = []
        invalid_mac_list = ['BADMACADDRES', '~!@#$%^&*()_-', '123:456:789:012']
        for invalid_mac in invalid_mac_list:
            arp_dict = copy.deepcopy(static_arp_dict)
            arp_dict['mac'] = invalid_mac
            arp_dict['ip'] = Parameter.DMZ_PC
            setres = arpapi.add_static_arp(**arp_dict)
            reslist.append(setres)
        logger.info(f'result list: {reslist}')
        Assertion.assert_equal(all(reslist), False, "ERR: invalid arp entry can be added")


# 17 Functional test for Static Arp Entry
class Test_TC17(Test):
    uuid = "SOSAIOT-TC-55768"
    description = show_testcase_info(
        TESTPLAN, '17', description=True)['title']
    res_17_for_tc15 = ContextVar('res_17_for_tc15')
    res_17_for_tc23 = ContextVar('res_17_for_tc23')
    res_17_for_tc24 = ContextVar('res_17_for_tc24')
    res_17_for_tc16 = ContextVar('res_17_for_tc16')
    res_17_for_tc18_01 = ContextVar('res_17_for_tc18_01')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp_verify_tc15(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.DMZ_PC
        arp_dict['mac'] = Parameter.X2_PC_MAC
        output = arpapi.add_static_arp(**arp_dict)
        self.res_17_for_tc15.set(output)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_check_arp_cache_verify_tc23(self):
        flag = False
        arpcaches = arpapi.show_arp_caches()
        checklist = (
            Parameter.DMZ_PC,
            str.upper(
                Parameter.X2_PC_MAC),
            'Permanent')
        logger.info(checklist)
        if Parameter.DMZ_PC in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp chace is found: {arpcache}')
                    flag = True
        else:
            logger.info('arp cache can not find')

        self.res_17_for_tc23.set(flag)
        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    @repeat_method(5)
    def test_04_check_arp_cache_after_flush_caches_verify_tc24(self):
        flag = False
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')
        arpcaches = arpapi.show_arp_caches()
        checklist = (
            Parameter.DMZ_PC,
            str.upper(
                Parameter.X2_PC_MAC),
            'Permanent')
        logger.info(checklist)

        if Parameter.DMZ_PC in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    flag = True
                    logger.info('arp cache is found')
        else:
            logger.info('arp chace can not find')

        self.res_17_for_tc24.set(flag)
        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    def test_05_ping_from_X2_pc(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, True, "ERR: ping fails")

    def test_06_ping_from_dut_and_capture_packet(self):
        ping_from_dut_dict = {
            'dest' : Parameter.DMZ_PC
        }
        exportres = fw_packet_monitor_run(action='ping_from_dut', **ping_from_dut_dict)
        logger.info(exportres)
        arpfilter = [
            'Address Resolution Protocol',
            'out:X2',
            'request',
            f'Target IP address: {Parameter.DMZ_PC}',
        ]
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, False, 
                               "ERR:  Firewall returned the valid ARP response")

    def test_07_edit_arp_entry_verify_tc16(self):
        edit_arp = {
            'raw_ip': Parameter.DMZ_PC,
            'raw_mac': Parameter.X2_PC_MAC,
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': Parameter.DMZ_PC,
            'mac': Parameter.FAKE_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpapi.edit_static_arp(**edit_arp)
        self.res_17_for_tc16.set(output)
        arpapi.show_arp_caches()
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_08_ping_from_X2_pc(self):
        # ping from X2 pc
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, False, "ERR: ping pass")

    def test_09_delete_arp_entry_verify_tc18(self):
        del_static = {
            'ip': Parameter.DMZ_PC,
            'mac': Parameter.FAKE_MAC,
            'interface': 'X2',
        }
        delarpres = arpapi.del_static_arp(**del_static)
        self.res_17_for_tc18_01.set(delarpres)
        Assertion.assert_equal(delarpres,
                               True, "ERR:Delete DAO and arp entry failed")

# 15 Add Static Arp Entry


class Test_TC15(Test):
    uuid = "SOSAIOT-TC-55766"
    description = show_testcase_info(
        TESTPLAN, '15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Add_Static_Arp_Entry(self):
        res = Test_TC17.res_17_for_tc15.get()
        logger.info(
            'Add Static Arp Entry: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Add Static Arp Entry failed")


# 16 Edit Static Arp Entry
class Test_TC16(Test):
    uuid = "SOSAIOT-TC-55767"
    description = show_testcase_info(
        TESTPLAN, '16', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Edit_Static_Ar_Entry(self):
        res = Test_TC17.res_17_for_tc16.get()
        logger.info(
            ' Edit Static Arp Entry: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR:  Edit Static Arp Entry failed")


# 23 Verify if the Static Arp Entry is Permanent in the Arp Cache and is
# not deletable
class Test_TC23(Test):
    uuid = "SOSAIOT-TC-55774"
    description = show_testcase_info(
        TESTPLAN, '23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Verify_Static_Arp_Entr_is_Permanent_in_the_Arp_Cache(self):
        res = Test_TC17.res_17_for_tc23.get()
        logger.info(
            'Verify if the Static Arp Entry is Permanent in the Arp Cache: {}'.format(res))
        Assertion.assert_equal(
            res, True, "ERR:  Static Arp Entry is not Permanent ")


# 24 Verify if the Static Arp Entries are not deleted when Flushing Arp Cache
class Test_TC24(Test):
    uuid = "SOSAIOT-TC-55775"
    description = show_testcase_info(
        TESTPLAN, '24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_result(self):
        res = Test_TC17.res_17_for_tc24.get()
        logger.info(
            'Verify the Static Arp Entries are not deleted when Flushing Arp Cache :{}'.format(res))
        Assertion.assert_equal(
            res, True, "ERR: Verify the Static Arp Entries failed")


# Functional test for Bind MAC Address
class Test_TC20(Test):
    uuid = "SOSAIOT-TC-55772"
    description = show_testcase_info(
        TESTPLAN, '20', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.DMZ_PC
        arp_dict['mac'] = Parameter.X2_PC_MAC
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_check_arp_entry_pass(self):
        output = arpapi.show_static_arp_entries()
        Assertion.assert_regular(str(output), Parameter.DMZ_PC,
                                 "ERR: Cannot found X2_IP in arp cache")

    def test_04_ping_interface_pass(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, True, "cannot ping X2 success")

    def test_05_change_ip_ping_interface_pass(self):
        output1 = PC2_login.send_command(
            f"ifconfig eth0 {Parameter.FAKE_IP} netmask 255.255.255.0 up")
        logger.info(f"ifconfig eth0 {Parameter.FAKE_IP} up : {output1}\n ")
        output2 = PC2_login.send_command('ifconfig')
        Assertion.assert_regular(str(output2), Parameter.FAKE_IP, "ERR: change pc ip fail")

    def test_06_ping_interface_pass(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, True, "cannot ping X2 success")

    def test_07_check_arp_entry_pass(self):
        flag = False
        arpcaches = arpapi.show_arp_caches()
        checklist = [
            Parameter.FAKE_IP,
            str.upper(
                Parameter.X2_PC_MAC),
            'Dynamic']
        logger.info(f'checklist:{checklist}')
        if Parameter.FAKE_IP in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp cache is found:{arpcache}')
                    flag = True
        else:
            logger.info('arp cache can not find')

        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    def test_08_edit_arp_entry(self):
        edit_arp = {
            'raw_ip': Parameter.DMZ_PC,
            'raw_mac': Parameter.X2_PC_MAC,
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': Parameter.DMZ_PC,
            'mac': Parameter.X2_PC_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': True,
        }
        output = arpapi.edit_static_arp(**edit_arp)
        arpapi.show_arp_caches()
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_09_ping_interface_fail(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, False, "cannot ping X2 success")

    def test_10_add_static_arp(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.FAKE_IP
        arp_dict['mac'] = Parameter.X2_PC_MAC
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, False, "add static ARP entry pass")

    def test_11_change_ip_ping_interface_pass(self):
        output1 = PC2_login.send_command(
            f"ifconfig eth0 {Parameter.DMZ_PC} netmask 255.255.255.0 up")
        logger.info(f"ifconfig eth0 {Parameter.DMZ_PC} up : {output1}\n ")
        output2 = PC2_login.send_command('ifconfig')
        Assertion.assert_regular(str(output2), Parameter.DMZ_PC, "ERR: change pc ip fail")

    def test_12_ping_interface_pass(self):
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} from pc2 : {output}\n ")
        Assertion.assert_equal(output, True, "cannot ping X2 success")

    def test_13_delete_arp_entry_verify_tc18(self):
        del_static = {
            'ip': Parameter.DMZ_PC,
            'mac': Parameter.X2_PC_MAC,
            'interface': 'X2',
            'bind_mac': True,
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delarpres,
                               True, "ERR:Delete DAO and arp entry failed")


# Functional test for Publishing Static Arp Entry
class Test_TC19(Test):
    uuid = "SOSAIOT-TC-55770"
    description = show_testcase_info(
        TESTPLAN, '19', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_arp_with_non_existent_IP(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.FAKE_IP
        arp_dict['mac'] = Parameter.DUT_X2_MAC
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_ping_from_pc_and_capture_packet(self):
        ping_from_pc_dict ={
            'dest' : Parameter.FAKE_IP,
            'pc_obj': PC2_login
        }
        exportres = fw_packet_monitor_run(action='ping_from_pc', **ping_from_pc_dict)
        logger.info(exportres)
        arpfilter = [
            'Address Resolution Protocol',
            'out:X2',
            'reply',
            f'Target IP address: {Parameter.FAKE_IP}',
        ]
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, False, 
                               "ERR:  Firewall returned the valid ARP response")

    def test_04_edit_arp_entry(self):
        edit_arp = {
            'raw_ip': Parameter.FAKE_IP,
            'raw_mac': Parameter.DUT_X2_MAC,
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': Parameter.FAKE_IP,
            'mac': Parameter.DUT_X2_MAC,
            'interface': 'X2',
            'publish': True,
            'bind_mac': False,
        }
        output = arpapi.edit_static_arp(**edit_arp)
        arpapi.show_arp_caches()
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_05_check_arp_cache(self):
        flag = False
        arpcaches = arpapi.show_arp_caches()
        checklist = [
            Parameter.FAKE_IP,
            str.upper(
                Parameter.DUT_X2_MAC),
            'Permanent published']
        logger.info(f'checklist:{checklist}')
        if Parameter.FAKE_IP in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp cache is found:{arpcache}')
                    flag = True
        else:
            logger.info('arp cache can not find')

        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    def test_06_ping_from_pc_and_capture_packet(self):

        ping_from_pc_dict = {
            'pc_obj': PC2_login,
            'dest': Parameter.FAKE_IP
        }
        exportres = fw_packet_monitor_run(action='ping_from_pc', **ping_from_pc_dict)

        logger.info(exportres)
        arpfilter = [
            'Address Resolution Protocol',
            'out:X2',
            'reply',
            f'Sender IP address: {Parameter.FAKE_IP}',
        ]
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True, 
                               "ERR:  Firewall returned the valid ARP response")

    def test_07_Configure_PC_with_default_gateway_as_FAKE_IP(self):
        cmds = [f'route del default gw 192.168.2.1',
                f'route add default gw {Parameter.FAKE_IP}',
                'ip -4 r'
                ]
        output = PC2_login.send_commands(cmds)
        flag = True if f'default via {Parameter.FAKE_IP}' in output else False
        Assertion.assert_equal(flag, 
                               True, "ERR:Configure_PC_with_default_gateway_as_FAKE_IP failed")

    def test_08_Ping_to_WAN_from_pc(self):
        output = PC2_login.ping_from_eth('10.103.202.200', 'eth0', num=2)
        Assertion.assert_equal(output, True, "ERR:ping to wan fail")

    def test_09_Configure_PC_with_default_gateway_as_X2_IP(self):
        cmds = [f'route del default gw {Parameter.FAKE_IP}',
                f'route add default gw {Parameter.X2_IP}',
                'ip -4 r']
        output = PC2_login.send_commands(cmds)
        flag = True if f'default via {Parameter.X2_IP}' in output else False
        Assertion.assert_equal(flag,
                               True, "ERR:Configure_PC_with_default_gateway_as_X2_IP failed")

    def test_10_delete_arp_entry(self):
        del_static = {
            'ip': Parameter.FAKE_IP,
            'mac': Parameter.DUT_X2_MAC,
            'interface': 'X2',
            'publish': True,
            'bind_mac': False,
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delarpres,
                               True, "ERR:Delete DAO and arp entry failed")


# Functional test for Update IP address Dynamically
class Test_TC21(Test):
    uuid = "SOSAIOT-TC-55773"
    description = show_testcase_info(
        TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_arp(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.DMZ_PC
        arp_dict['mac'] = Parameter.X2_PC_MAC
        arp_dict['bind_mac'] = True
        arp_dict['dynamic'] = True
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_check_arp_cache(self):
        flag = False
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} : {output}\n ")
        arpcaches = arpapi.show_arp_caches()
        checklist = (
            Parameter.DMZ_PC,
            str.upper(
                Parameter.X2_PC_MAC),
            'Dynamic')
        logger.info(f'checklist:{checklist}')
        if str.upper(Parameter.X2_PC_MAC) in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp cache is found:{arpcache}')
                    flag = True
        else:
            logger.info('arp chace can not find')

        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")

    def test_04_change_pc_ip(self):
        output1 = PC2_login.send_command(
            f"ifconfig eth0 {Parameter.FAKE_IP} netmask 255.255.255.0 up")
        logger.info(f"ifconfig eth0 {Parameter.FAKE_IP} up : {output1}\n ")
        output2 = PC2_login.send_command('ifconfig')
        Assertion.assert_regular(str(output2),  Parameter.FAKE_IP, "ERR: change pc ip fail")

    def test_05_check_arp_cache(self):
        flag = False
        output = PC2_login.ping_from_eth(Parameter.X2_IP, 'eth0', num=2)
        logger.info(f"ping {Parameter.X2_IP} : {output}\n ")
        arpcaches = arpapi.show_arp_caches()
        checklist = (
            Parameter.FAKE_IP,
            str.upper(
                Parameter.X2_PC_MAC),
            'Dynamic')
        logger.info(f'checklist:{checklist}')
        if str.upper(Parameter.X2_PC_MAC) in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp cache is found:{arpcache}')
                    flag = True
        else:
            logger.info('arp chace can not find')

        Assertion.assert_equal( flag, True, "ERR: ARP entry can't find")

    def test_06_change_pc_ip_back(self):
        output1 = PC2_login.send_command(
            f"ifconfig eth0 {Parameter.DMZ_PC} netmask 255.255.255.0 up")
        logger.info(f"ifconfig eth0 {Parameter.DMZ_PC} up : {output1}\n ")
        output2 = PC2_login.send_command('ifconfig')
        Assertion.assert_regular(
            str(output2),
            Parameter.DMZ_PC,
            "ERR: change pc ip fail")

    def test_07_delete_arp_entry(self):
        del_static = {
            'ip': '0.0.0.0',
            'mac': Parameter.X2_PC_MAC,
            'interface': 'X2',
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delarpres,
                               True, "ERR:Delete arp entry failed")


#Option: "Dont glean source data from arp request" is disabled
class Test_TC30(Test):
    uuid = "SOSAIOT-TC-63119"
    description = show_testcase_info(
        TESTPLAN, '30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_flush_arp_caches(self):
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')
        arpcaches = arpapi.show_arp_caches()
        if Parameter.DMZ_PC in str(arpcaches):
            flag = False
        else:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: flush arp caches failed")

    def test_03_disable_glean(self):
        setres = arpapi.arp_setting(timeout=2, glean=True)
        Assertion.assert_equal(
            setres, True, "ERR: Don't glean source data from ARP requests")

    def test_04_check_arp_cache(self):
        flag = False
        send_arp_dict = {
            'srcmac': Parameter.X2_PC_MAC,
            'iface' :'eth0',
            'psrc':Parameter.DMZ_PC,
            'pdst':Parameter.X2_IP,
            'pc_obj':PC2_login
        }
        sendres = send_traffic(action ='send_arp_from_PC',**send_arp_dict)
        logger.info(f"send traffic result : {sendres}")
        arpcaches = arpapi.show_arp_caches()
        checklist = (
            Parameter.DMZ_PC,
            str.upper(
                Parameter.X2_PC_MAC),
            'Dynamic')
        logger.info(f'checklist:{checklist}')
        if Parameter.DMZ_PC in str(arpcaches):
            for arpcache in arpcaches:
                checkres = [x in str(arpcache) for x in checklist]
                logger.info(f'check arp cache result: {checkres}')
                if all(checkres):
                    logger.info(f'arp cache is found:{arpcache}')
                    flag = True
        else:
            logger.info('arp chace can not find')

        Assertion.assert_equal( flag, True, "ERR: ARP entry can't find")


# Enable Option: "Dont glean source data from arp request"
class Test_TC31(Test):
    uuid = "SOSAIOT-TC-63120"
    description = show_testcase_info(
        TESTPLAN, '31', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_flush_arp_caches(self):
        delcacheres = arpcli.flush_arp_entry('all')
        logger.info(f'delete caches: {delcacheres}')
        arpcaches = arpapi.show_arp_caches()
        if Parameter.DMZ_PC in str(arpcaches):
            flag = False
        else:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: flush arp caches failed")

    def test_03_enbale_glean(self):
        setres = arpapi.arp_setting(timeout=2, glean=False)
        Assertion.assert_equal(
            setres, True, "ERR: Don't glean source data from ARP requests")

    def test_04_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X2_PC_MAC,
            'iface' :'eth0',
            'psrc':Parameter.DMZ_PC,
            'pdst':Parameter.X2_IP,
            'pc_obj':PC2_login
        }
        sendres = send_traffic(action ='send_arp_from_PC',**send_arp_dict)
        logger.info(f"send traffic from pc2 result : {sendres}")
        arpcaches = arpapi.show_arp_caches()
        if Parameter.DMZ_PC in str(arpcaches):
            flag = False
        else:
            flag = True

        Assertion.assert_equal(flag, True, "ERR: ARP entry can't find")


# 08 Box rejects any ARP requests from WAN IP that it does not own.
class Test_TC08(Test):
    uuid = "SOSAIOT-TC-55785"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X1_PC_MAC,
            'iface' :'eth2',
            'psrc':Parameter.WAN_PC,
            'pdst':Parameter.FAKE_WAN_IP,
            'pc_obj':PC1_login
        }
        exportres = fw_packet_monitor_run(action='send_arp_from_PC', **send_arp_dict)
        arpfilter = [
            'Address Resolution Protocol',
            'request',
            f'Sender MAC address: {Parameter.X1_PC_MAC}',
            f'Sender IP address: {Parameter.WAN_PC}',
            f'DROPPED',
            f' Drop Code: 64(Not for me.)',
            f'Target IP address: {Parameter.FAKE_WAN_IP}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True,
                               "ERR:  Firewall returned the valid ARP response")


# 09  The box must process and respond to ARP requests on its WAN for
# valid IP addresses it owns on that WAN.
class Test_TC09(Test):
    uuid = "SOSAIOT-TC-55786"
    description = show_testcase_info(TESTPLAN, '9', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_wan_to_lan_nat_policy(self):
        res = False
        base_dict = {
            'name': 'test_for_case_09',
            "destination": {"name": 'X1_public_ip'},
            "translated_destination": {"name": 'lan pc'}
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        if addres:
            natgetres = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(natgetres) else False
        else:
            logger.error('add nat policy failed')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed')

    @repeat_method(3)
    def test_04_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X1_PC_MAC,
            'iface' :'eth2',
            'psrc':Parameter.WAN_PC,
            'pdst':Parameter.FAKE_WAN_IP,
            'pc_obj':PC1_login
        }
        exportres = fw_packet_monitor_run(action='send_arp_from_PC', **send_arp_dict)
        arpfilter = [
            'Address Resolution Protocol',
            'reply',
            f'Sender MAC address: {Parameter.DUT_X1_MAC}',
            f'Sender IP address: {Parameter.FAKE_WAN_IP}',
            f'Target MAC address: {Parameter.X1_PC_MAC}',
            f'Target IP address: {Parameter.WAN_PC}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal( checkres,True,
                               "ERR:  Firewall returned the valid ARP response")

    def test_05_delete_wan_to_lan_nat_policy(self):
        delres = natpolicyapi.del_nat_policy_by_name('test_for_case_09')
        Assertion.assert_equal(delres, True, 'ERR: delete nat policy failed')

# The secondary WAN does not arp respond for requests of the primary WAN IP
class Test_TC10(Test):
    uuid = "SOSAIOT-TC-55761"
    description = show_testcase_info(TESTPLAN, '10', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_config_interface_X2_as_Second_WAN(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to WAN failed")

    def test_02_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X2_PC_MAC,
            'iface' :'eth0',
            'psrc':Parameter.DMZ_PC,
            'pdst':Parameter.X1_IP,
            'pc_obj':PC2_login
        }
        exportres=fw_packet_monitor_run(action='send_arp_from_PC',
                                        **send_arp_dict)
        arpfilter = [
            'Address Resolution Protocol',
            'request',
            f'Sender MAC address: {Parameter.X2_PC_MAC}',
            f'Sender IP address: {Parameter.DMZ_PC}',
            f'DROPPED',
            f'Target IP address: {Parameter.X1_IP}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True,
                               "ERR:  Firewall returned the valid ARP response")


# The box must process and respond to ARP requests on its secondary WAN
# for valid IP addresses it owns on that secondary WAN
class Test_TC11(Test):
    uuid = "SOSAIOT-TC-55762"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_wan_to_lan_nat_policy(self):
        res = False
        base_dict = {
            'name': 'test_for_case_11',
            "destination": {"name": 'X2_public_ip'},
            "translated_destination": {"name": 'lan pc'}
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        if addres:
            natgetres = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(natgetres) else False
        else:
            logger.error('add nat policy failed')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed')

    @repeat_method(3)
    def test_03_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X2_PC_MAC,
            'iface' :'eth0',
            'psrc':Parameter.DMZ_PC,
            'pdst':Parameter.FAKE_IP,
            'pc_obj':PC2_login
        }
        exportres = fw_packet_monitor_run(action='send_arp_from_PC',**send_arp_dict)
        arpfilter = [
            'Address Resolution Protocol',
            'reply',
            f'Sender MAC address: {Parameter.DUT_X2_MAC}',
            f'Sender IP address: {Parameter.FAKE_IP}',
            f'Target MAC address: {Parameter.X2_PC_MAC}',
            f'Target IP address: {Parameter.DMZ_PC}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True,
                               "ERR:  Firewall returned the valid ARP response")

    def test_05_delete_wan_to_lan_nat_policy(self):
        delres = natpolicyapi.del_nat_policy_by_name('test_for_case_11')
        Assertion.assert_equal(delres, True, 'ERR: delete nat policy failed')


# The primary WAN does not arp respond for requests of the secondary WAN IP.
class Test_TC12(Test):
    uuid = "SOSAIOT-TC-55763"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_arp_cache(self):
        send_arp_dict = {
            'srcmac': Parameter.X1_PC_MAC,
            'iface' :'eth2',
            'psrc': Parameter.WAN_PC,
            'pdst':Parameter.X2_IP,
            'pc_obj':PC1_login
        }
        exportres = fw_packet_monitor_run(
            action ='send_arp_from_PC',**send_arp_dict)
        arpfilter = [
            'Address Resolution Protocol',
            'request',
            f'Sender MAC address: {Parameter.X1_PC_MAC}',
            f'Sender IP address: {Parameter.WAN_PC}',
            f'DROPPED',
            f'Target IP address: {Parameter.X2_IP}']
        logger.info(f'arpfilter:{arpfilter}')

        checkres = check_arp_packet(exportres, arpfilter)
        Assertion.assert_equal(checkres, True,
                               "ERR:  Firewall returned the valid ARP response")

    def test_03_config_interface_X2_as_DMZ(self):
        x2_static = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = interfaceapi.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to DMZ failed")


# Static ARP - Secondary LAN
class Test_TC28(Test):
    uuid = "SOSAIOT-TC-55779"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_arp_with_second_IP(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['ip'] = Parameter.SECONDARY_IP
        arp_dict['mac'] = Parameter.DUT_X2_MAC
        arp_dict['publish'] = True
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_add_route_policy_for_second_network(self):
        route_dict = copy.deepcopy(route_base_dict)
        rt_update_dict = {
            "name": 'test_28',
            "interface": "X2",
            'destination': {"name": '2rd_net'},
            'gateway': {'name': 'Default Gateway'}
        }
        route_dict.update(rt_update_dict)
        route_policy_dict = {"route_policies": [{"ipv4": route_dict}]}
        resrt = routeapi.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(resrt, True, "ERR:add route fail")

    def test_04_change_pc_ip(self):
        cmds = [
            f'route del default gw {Parameter.X2_IP}',
            f'ifconfig eth0 {Parameter.SECONDARY_PC} netmask 255.255.255.0 up',
            f'route add default gw {Parameter.SECONDARY_IP}',
            'ifconfig',
            'ip -4 r']
        output1 = PC2_login.send_commands(cmds)
        logger.info(f"config eth0 {Parameter.SECONDARY_PC}: {output1}\n ")
        if f'default via {Parameter.SECONDARY_IP}' in output1 and Parameter.SECONDARY_PC in output1 :
            flag = True 
        else:
            flag = False
        Assertion.assert_equal(flag, True, "ERR: change pc ip fail")

    def test_05_Ping_to_WAN_from_pc(self):
        output = PC2_login.ping_from_eth('10.103.202.200', 'eth0', num=2)
        Assertion.assert_equal(output, True, "ERR:ping to wan fail")

    def test_06_edit_acl_wan_to_dmz(self):
        output = False
        try:
            output1 = accessruleapi.get_ipv4_access_rule_given_from_to("WAN", "DMZ")
            logger.info('output')
            uuid = output1['access_rules'][0]['ipv4']['uuid']
            logger.info(uuid)
            output = accessruleapi.edit_ipv4_access_rule_uuid(uuid, **wan_to_dmz_dict)
        except Exception as e:
            logger.info("edit acl with error {}".format(repr(e)))

        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_07_add_wan_to_dmz_nat_policy(self):
        res = False
        base_dict = {
            'name': 'test_for_case_28',
            "destination": {"name": 'X1_public_ip'},
            "translated_destination": {"name": '2rd_pc'}
        }
        nat_base_new = copy.deepcopy(nat_base_dict)
        nat_base_new.update(base_dict)
        nat_dict = {"nat_policies": [{"ipv4": nat_base_new}]}
        addres = natpolicyapi.add_nat_policy(**nat_dict)
        if addres:
            natgetres = natpolicyapi.get_nat_policy(name=base_dict['name'])
            res = True if base_dict['name'] in str(natgetres) else False
        else:
            logger.error('add nat policy failed')
        Assertion.assert_equal(res, True, 'ERR: add nat policy failed')

    def test_08_Ping_from_WAN_to_DMZ(self):
        output = PC1_login.ping_from_eth(Parameter.FAKE_WAN_IP, 'eth2', num=10)
        Assertion.assert_equal(output, True, "ERR:ping to wan fail")

    def test_09_Configure_PC_with_default_gateway_as_X2_IP(self):
        cmds = [f'route del default gw {Parameter.SECONDARY_IP}',
                f'ifconfig eth0 {Parameter.DMZ_PC} netmask 255.255.255.0 up',
                f'route add default gw 192.168.2.1',
                'ifconfig',
                'ip -4 r']
        output1 = PC2_login.send_commands(cmds)
        if f'default via 192.168.2.1' in output1 and Parameter.DMZ_PC in output1 :
            flag = True 
        else:
            flag = False
        Assertion.assert_equal(flag, True, "ERR: change pc ip fail")

    def test_10_delete_arp_entry(self):
        del_static = {
            'ip': Parameter.SECONDARY_IP,
            'mac': Parameter.DUT_X2_MAC,
            'interface': 'X2',
            'publish': True,
            'bind_mac': False,
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delarpres, True, "ERR:Delete DAO and arp entry failed")

    def test_11_delete_wan_to_lan_nat_policy(self):
        delres = natpolicyapi.del_nat_policy_by_name('test_for_case_28')
        Assertion.assert_equal(delres, True, 'ERR: delete nat policy failed')


# 25 Preferences Import/Export support for the Static Arp
class Test_TC25(Test):
    uuid = "SOSAIOT-TC-55776"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']
    filter_tuple = (Parameter.LAN_PC, Parameter.WAN_PC, Parameter.DMZ_PC, Parameter.X0_PC_MAC,
                    Parameter.X1_PC_MAC, Parameter.X2_PC_MAC, 'X0', 'X1', 'X2')
    res_25_for_tc18_02 = ContextVar('res_25_for_tc18_02')
    res_25_for_tc26 = ContextVar('res_25_for_tc26')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp(self):
        reslist = []
        ip_list = [Parameter.LAN_PC, Parameter.WAN_PC, Parameter.DMZ_PC]
        mac_list = [
            Parameter.X0_PC_MAC,
            Parameter.X1_PC_MAC,
            Parameter.X2_PC_MAC]
        interface_list = ['X0', 'X1', 'X2']
        for i in range(3):
            arp_dict = copy.deepcopy(static_arp_dict)
            arp_dict['mac'] = mac_list[i]
            arp_dict['ip'] = ip_list[i]
            arp_dict['interface'] = interface_list[i]
            setres = arpapi.add_static_arp(**arp_dict)
            reslist.append(setres)
        Assertion.assert_equal(all(reslist), True, "ERR: Add arp entry failed")

    def test_03_check_static_arp_in_tsr_verify_tc26(self):
        tsr = diagapi.get_tsr_part('Network', 'ARP')
        logger.info(tsr)
        checkres = [x in tsr for x in self.filter_tuple]
        logger.info(f'check arp entries in TSR result: {checkres}')
        flag = True if all(checkres) else False
        self. res_25_for_tc26.set(flag)
        Assertion.assert_equal(flag, True, "ERR: Add arp entry failed")

    def test_04_export_exp_verify_tc25(self):
        res = settingapi.export_setting_exp()
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_05_delete_all_static_arp_verify_tc18(self):
        res = arpcli.del_all_arp_entries()
        logger.info(f"Delete all arp entries:{res}")
        self.res_25_for_tc18_02.set(res)
        arpcaches = arpapi.show_static_arp_entries()
        checkres = [x in str(arpcaches) for x in self.filter_tuple]
        logger.info(f'check arp cache result: {checkres}')
        Assertion.assert_equal(all(checkres), False, "ERR: Add arp entry failed")

    def test_06_import_exp_verify_tc25(self):
        res = settingapi.import_setting_exp(filepath='/tmp/test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")

    def test_07_check_arp_caches(self):
        arpcaches = arpapi.show_static_arp_entries()
        checkres = [x in str(arpcaches) for x in self.filter_tuple]
        logger.info(f'check arp cache result: {checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check arp cache failed")

    def test_08_delete_all_static_arp(self):
        res = arpcli.del_all_arp_entries()
        logger.info(f"Delete all arp entries:{res}")
        arpcaches = arpapi.show_static_arp_entries()
        checkres = [x in str(arpcaches) for x in self.filter_tuple]
        logger.info(f'check arp cache result: {checkres}')
        Assertion.assert_equal(all(checkres), False, "ERR: check arp cache failed")


# 18 Delete and Delete all Static Arp Entries
class Test_TC18(Test):
    uuid = "SOSAIOT-TC-55769"
    description = show_testcase_info(
        TESTPLAN, '18', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_Delete_Static_Arp_Entry(self):
        res = Test_TC17.res_17_for_tc18_01.get()
        logger.info(
            'Verify Delete one Static Arp Entry :{}'.format(res))
        Assertion.assert_equal(res, True, "ERR: delete arp entries failed")

    def test_02_check_Delete_all_Static_Arp_Entries(self):
        res = Test_TC25.res_25_for_tc18_02.get()
        logger.info(
            'Verify Delete all Static Arp Entries :{}'.format(res))
        Assertion.assert_equal(res, True, "ERR: delete arp entries failed")


# 26 Verify the TSR for Static Arp Entries on different Interfaces
class Test_TC26(Test):
    uuid = "SOSAIOT-TC-55777"
    description = show_testcase_info(
        TESTPLAN, '26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_TSR(self):
        res = Test_TC25.res_25_for_tc26.get()
        logger.info(
            'Verify the TSR for Static Arp Entries on different Interfaces: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: check TSR failed")
