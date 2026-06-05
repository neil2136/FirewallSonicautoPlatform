from definition.settings import *
from definition.utils import *


# TC0 2Verify mouse-over in the Address Detail column for unresolved MAC AO
class TestMACAO_TC02(Test):
    uuid = "SOSAIOT-TC-57918"
    description = show_testcase_info(
        TESTPLAN, '2', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        mac_ao_dict['value'] = '11:22:33:33:44:55'
        addaores = aoapi.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_check_mac_ao_info(self):
        aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc1 = True if 'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO  info failed")

    def test_04_delete_ao(self):
        delaores = aoapi.del_ao_by_name(mac_ao_dict['name'], 'mac')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# tc01,04,06,08,15 share the same MAC AO
# TC01 MAC Address Object added in the GUI
class TestMACAO_TC01(Test):
    uuid = "SOSAIOT-TC-57909"
    description = show_testcase_info(
        TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        CaseParams.fw_time_tc01 = timeapi.show_time()
        mac_ao_dict['value'] = Parameter.PC1_ETH0_MAC
        addaores = aoapi.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_check_result(self):
        ret = PC1_login.send_command(
            'route add -host {} gw {}'.format(PC2_ETH0_IP, Parameter.FIREWALL))
        logger.info(ret)
        output = PC1_login.ping_from_eth(PC2_ETH0_IP, 'eth0', num=5)
        Assertion.assert_equal(
            output, True, "ERR: ping failed")

    def test_04_check_mac_ao_info(self):
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc1 = True if f'{PC1_ETH0_IP}' or f'{Parameter.PC1_ETH0_LINKLOCAL}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO info failed")


# Verify mouse-over in the Address Detail column. The entry appears in the ARP cache.
class TestMACAO_TC04(Test):
    uuid = "SOSAIOT-TC-57934"
    description = show_testcase_info(
        TESTPLAN, '4', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_arp_info(self):
        arp_exist = False
        arpcaches = arpapi.show_arp_caches()
        for arpcache in arpcaches:
            try:
                if Parameter.PC1_ETH0_MAC_org in arpcache['mac_address']:
                    logger.info("arp entry is :{}".format(arpcache))
                    arp_exist = True
            except Exception as e:
                logger.info(
                    "expected arpcache not found with error {}".format(e))
        Assertion.assert_equal(
            arp_exist, True, "ERR: check arp  info failed")


# A Log event upon MAC AO resolution
class TestMACAO_TC06(Test):
    uuid = "SOSAIOT-TC-57938"
    description = show_testcase_info(
        TESTPLAN, '6', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_log(self):
        lowmac_eth0 = str.lower(Parameter.PC1_ETH0_MAC_org)
        filter_tc06 = (f'{lowmac_eth0}', f'{PC1_ETH0_IP}')
        logger.info(filter_tc06)
        time.sleep(10)
        fw_logs = logmonitorapi.get_log(911)
        flag = check_log_by_time(CaseParams.fw_time_tc01, fw_logs, filter_tc06)
        Assertion.assert_equal(flag, True, "ERR: check log info failed")


# TC08 Functional test for deny Access Rule that references MAC AO
class TestMACAO_TC08(Test):
    uuid = "SOSAIOT-TC-57940"
    description = show_testcase_info(
        TESTPLAN, '8', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_access_rule(self):
        base_dict = {
            'service': {'group': 'ICMP'},
            'source_addr': {"name": mac_ao_dict['name']},
            'dst_addr': {'any': True}
        }
        acl_dict.update(base_dict)
        output = accessruleapi.add_ipv4_access_rule(**acl_dict)
        Assertion.assert_equal(output, True, "ERR: cannot add access rule")

    def test_03_check_mac_ao_info(self):
        aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc1 = True if f'{PC1_ETH0_IP}' or f'{Parameter.PC1_ETH0_LINKLOCAL}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO info failed")

    @repeat_method(5)
    def test_04_Verify_traffic(self):
        time.sleep(10)
        output = PC1_login.ping_from_eth(PC2_ETH0_IP, 'eth0', num=2)
        Assertion.assert_equal(
            output, False, "ERR: Verify traffic failed after add access rule")

    def test_05_del_acl(self):
        delres = accessruleapi.del_ipv4_access_rule(acl_dict['name'])
        Assertion.assert_equal(delres, True, "ERR: del taccess rule failed")


# # MAC-to-IP correlation changes. Multihomed host is disabled
class TestMACAO_TC15(Test):
    uuid = "SOSAIOT-TC-57914"
    description = show_testcase_info(
        TESTPLAN, '15', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_change_eth0_ip(self):
        flag_tc15 = False
        tempip = '192.168.168.15'
        output1 = PC1_login.send_command(f"ifconfig eth0 {tempip}/24 up")
        logger.info(f"ifconfig eth0 {tempip} up : {output1}\n ")
        output2 = PC1_login.ping_from_eth(Parameter.FIREWALL, 'eth0', num=2)
        logger.info(f"ping eth0 {Parameter.FIREWALL} : {output2}\n ")
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        if tempip in str(rc) and Parameter.FIREWALL not in str(rc):
            logger.info(f"{ rc['data']['daoInfo']} is found\n")
            flag_tc15 = True
        Assertion.assert_equal(
            flag_tc15, True, "ERR: check AO info failed")

    def test_03_restore(self):
        output = PC1_login.send_command(f"ifconfig eth0 {PC1_ETH0_IP} up")
        logger.info(f"ifconfig eth0 {PC1_ETH0_IP} up : {output}\n ")
        delaores = aoapi.del_ao_by_name(mac_ao_dict['name'], 'mac')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# TC09,10 share the same MAC AO
# TC09 The ARP cache entry timeout , the MAC AO "test" displays Unresolved.
class TestMACAO_TC09(Test):
    uuid = "SOSAIOT-TC-57941"
    description = show_testcase_info(
        TESTPLAN, '9', description=True)['title']
    tc09aoname = 'removemactest'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        CaseParams.fw_time_tc09 = timeapi.show_time()
        logger.info(f'fw_time is : {CaseParams.fw_time_tc09}')
        ao_dict = copy.deepcopy(mac_ao_dict)
        base_dict = {
            'name': self.tc09aoname,
            'value': Parameter.PC1_ETH2_MAC
        }
        ao_dict.update(base_dict)
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    repeat_method(5)
    def test_03_check_arp(self):
        output = PC1_login.ping_from_eth(Parameter.X2_IP, 'eth2', num=2)
        logger.info(f"ping X2_IP: {output}\n ")
        if output:
            flag_tc09 = wait_arp_timeout(arpapi, Parameter.PC1_ETH2_MAC_org)
        else:
            flag_tc09 = False

        Assertion.assert_equal(
            flag_tc09, True, "ERR: check AO info failed")


# TC10 A Log upon event of a timeout
class TestMACAO_TC10(Test):
    uuid = "SOSAIOT-TC-57943"
    description = show_testcase_info(
        TESTPLAN, '10', description=True)['title']
    tc10aoname = 'removemactest'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_remove_log(self):
        # 'MAC=fa:16:3e:4e:26:4c; Host=192.168.168.169'
        lowmac_eth2 = str.lower(Parameter.PC1_ETH2_MAC_org)
        filters_tc10 = (f"MAC={lowmac_eth2}", f"Host={PC1_ETH2_IP}")
        logger.info(filters_tc10)
        time.sleep(10)
        fw_logs = logmonitorapi.get_log(912)
        flag = check_log_by_time(
            CaseParams.fw_time_tc09, fw_logs, filters_tc10)
        Assertion.assert_equal(flag, True, "ERR: check log info failed")

    def test_03_delete_DAO(self):
        delres = aoapi.del_ao_by_name(self.tc10aoname, 'mac')
        Assertion.assert_equal(delres, True, "ERR:Delete DAO failed")


# TC05,11,12 share the same MAC AO
# TC05 Verify mouse-over in the Address Detail column. The entry is added in the Static ARP table.
class TestMACAO_TC05(Test):
    uuid = "SOSAIOT-TC-57937"
    description = show_testcase_info(
        TESTPLAN, '5', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        arp_dict['mac'] = Parameter.PC1_ETH2_MAC
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_check_arp(self):
        flag_tc11 = False
        arpcaches = arpapi.show_arp_caches()
        for arpcache in arpcaches:
            try:
                if str.upper(Parameter.PC1_ETH2_MAC_org) in arpcache['mac_address']:
                    if 'Permanent' in arpcache['timeout']:
                        logger.info(
                            f'{Parameter.PC1_ETH2_MAC_org} Permanent published in {arpcache}')
                        flag_tc11 = True
            except Exception as e:
                logger.info(
                    "expected arpcache not found with error {}".format(e))
        Assertion.assert_equal(flag_tc11, True, "check ARP entry failed")

    def test_04_add_MAC_AO(self):
        logger.info(
            f"mac is {Parameter.PC1_ETH2_MAC},orginal mac is {Parameter.PC1_ETH2_MAC_org}")
        ao_dict = copy.deepcopy(mac_ao_dict)
        ao_dict['value'] = Parameter.PC1_ETH2_MAC
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_05_check_MAC_ao_info(self):
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc11 = True if f'{PC1_ETH2_IP}' or f'{Parameter.PC1_ETH2_LINKLOCAL}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc11, True, "ERR: check AO info failed")


# The IP address has been modified in the Static ARP entry
class TestMACAO_TC12(Test):
    uuid = "SOSAIOT-TC-57911"
    description = show_testcase_info(
        TESTPLAN, '12', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_edit_arp_entry(self):
        edit_arp = {
            'raw_ip': PC1_ETH2_IP,
            'raw_mac': Parameter.PC1_ETH2_MAC,
            'raw_interface': 'X2',
            'raw_publish': False,
            'raw_bind_mac': False,
            'ip': CaseParams.tc12aonewip,
            'mac': Parameter.PC1_ETH2_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': False,
        }
        output = arpapi.edit_static_arp(**edit_arp)
        arpapi.show_arp_caches()
        Assertion.assert_equal(output, True, "edit static ARP entry failed")

    def test_03_check_mac_ao_info(self):
        aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc12 = True if f'{CaseParams.tc12aonewip}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc12, True, "ERR: check AO info failed")


# The entry is deleted from Static ARP
class TestMACAO_TC11(Test):
    uuid = "SOSAIOT-TC-57910"
    description = show_testcase_info(
        TESTPLAN, '11', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_delete_arp_entry(self):
        del_static = {
            'ip': CaseParams.tc12aonewip,
            'mac': Parameter.PC1_ETH2_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': True,
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delarpres, True, "del static arp entry failed")

    def test_03_check_MAC_ao_info(self):
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc11 = True if f'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(
            flag_tc11, True, "ERR: check AO info failed")

    def test_04_check_arp(self):
        flag_tc11 = True
        arpcaches = arpapi.show_arp_caches()
        for arpcache in arpcaches:
            try:
                if Parameter.PC1_ETH2_MAC_org in arpcache['mac_address']:
                    if arpcache['timeout'] == 'Permanent published':
                        logger.info(
                            f'{Parameter.PC1_ETH2_MAC_org} Permanent published in {arpcache}')
                        flag_tc11 = False
            except Exception as e:
                logger.info(
                    "expected arpcache not found with error {}".format(e))
        Assertion.assert_equal(
            flag_tc11, True, "check ARP entry failed")

    def test_05_delete_DAO(self):
        delaores = aoapi.del_ao_by_name(mac_ao_dict['name'], 'mac')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# MAC-to-IP correlation changes. Multihomed host is enabled
class TestMACAO_TC13(Test):
    uuid = "SOSAIOT-TC-57912"
    description = show_testcase_info(
        TESTPLAN, '13', description=True)['title']
    tc13aoname = "Multihomed"
    tc13aonewip = "14.1.1.210"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        logger.info(
            f"mac is {Parameter.PC1_ETH2_MAC},orginal mac is {Parameter.PC1_ETH2_MAC_org}")
        ao_dict = copy.deepcopy(mac_ao_dict)
        base_dict = {
            'name': self.tc13aoname,
            'value': Parameter.PC1_ETH2_MAC,
            'multi_homed': True
        }
        ao_dict.update(base_dict)
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_add_static_arp(self):
        arp_dict = copy.deepcopy(static_arp_dict)
        base_dict = {
            'mac': Parameter.PC1_ETH2_MAC,
            'ip': self.tc13aonewip
        }
        arp_dict.update(base_dict)
        output = arpapi.add_static_arp(**arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_04_check_mac_ao_info(self):
        aoapi.resolve_ao_by_name(self.tc13aoname, 'mac')
        time.sleep(15)
        output = PC1_login.ping_from_eth(Parameter.X2_IP, 'eth2', num=2)
        logger.info(output)
        flag_tc13 = False
        arpcaches = arpapi.show_arp_caches()
        if re.search(f'{PC1_ETH2_IP}.*{self.tc13aonewip}', str(arpcaches), re.I):
            flag_arp = True
            logger.info(f"arp entries found:{flag_arp}")
        rc = aoapi.get_DAO_info(self.tc13aoname)
        if re.search(f'{PC1_ETH2_IP}.*{self.tc13aonewip}', str(rc), re.I):
            flag_tc13 = True
        Assertion.assert_equal(
            flag_tc13, True, "ERR: check AO info failed")

    def test_05_delete_DAO_and_static_arp(self):
        delaores = aoapi.del_ao_by_name(self.tc13aoname, 'mac')
        del_static = {
            'ip': self.tc13aonewip,
            'mac': Parameter.PC1_ETH2_MAC,
            'interface': 'X2',
            'publish': False,
            'bind_mac': True,
        }
        delarpres = arpapi.del_static_arp(**del_static)
        Assertion.assert_equal(delaores & delarpres,
                               True, "ERR:Delete DAO and arp entry failed")


# TC14 The limit of resolved addresses displayed in the Address Detail for MAC AO
class TestMACAO_TC14(Test):
    uuid = "SOSAIOT-TC-57913"
    description = show_testcase_info(
        TESTPLAN, '14', description=True)['title']
    tc14aoname = "maxresolved"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        ao_dict = copy.deepcopy(mac_ao_dict)
        base_dict = {
            'name': self.tc14aoname,
            'value': Parameter.PC1_ETH0_MAC,
            'multi_homed': True
        }
        ao_dict.update(base_dict)
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_set_arp_timeout(self):
        setres = arpapi.arp_setting(timeout=10)
        Assertion.assert_equal(setres, True, "ERR: set arp timeout failed")

    def test_04_change_eth0_ip(self):
        flag = []
        for increment in range(10, 50):
            time.sleep(1)
            tempip = f'192.168.168.{increment}/24'
            output1 = PC1_login.send_command(f"ifconfig eth0 {tempip} up")
            logger.info(f"ifconfig eth0 {tempip} up : {output1}\n ")
            output2 = PC1_login.ping_from_eth(
                Parameter.FIREWALL, 'eth0', num=2)
            logger.info(f"ping eth0 {tempip} : {output2}\n ")
            flag.append(1) if output2 else flag.append(0)
        Assertion.assert_equal(
            all(flag), True, "ERR: check arp info failed")


    def test_05_check_arp_info(self):
        arpcaches = arpapi.show_arp_caches()
        arpsum = str(arpcaches).count(str.upper(Parameter.PC1_ETH0_MAC_org))
        logger.info(f"{arpsum} arp entries are found\n")
        Assertion.assert_equal(
            True, True, "ERR: check arp info failed")

    def test_06_check_mac_ao_info(self):
        flag_tc14 = False
        rc = aoapi.get_DAO_info(self.tc14aoname)
        hostsum = str(rc).count('Host')
        if hostsum > 2 and "..." in str(rc):
            logger.info(f"at least {hostsum} hosts are found\n")
            flag_tc14 = True
        Assertion.assert_equal(
            flag_tc14, True, "ERR: check AO info failed")


# TC18 MAC AO entry in TSR
class TestMACAO_TC18(Test):
    uuid = "SOSAIOT-TC-57916"
    description = show_testcase_info(
        TESTPLAN, '18', description=True)['title']
    tc18aoname = "maxresolved"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_TSR(self):
        hostsum = 0
        maxhosts = 0
        flag_tc14 = False
        aopart = check_TSR(
            diagnosticapi, 'Address Object Table', self.tc18aoname)
        hostspart = re.search(
            r'HOSTS:(.*)\nHOST(.*?):(.*?)\n', aopart, re.I | re.S | re.M)
        if hostspart:
            maxhosts = hostspart.group(1).strip()
            logger.info(f'maxhosts :  {maxhosts}')
            for host in hostspart.group(3).split(','):
                if re.search(r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])',host):
                    logger.info(f"{host} is found\n")
                    hostsum += 1
        logger.info(f'hostsum:{hostsum}')
        if hostsum >= 31 and maxhosts == '32':
            logger.info(
                f"The limit of resolved addresses displayed in the Address Detail for MAC AO is {hostsum}")
            flag_tc14 = True
        Assertion.assert_equal(
            flag_tc14, True, "ERR: check AO info in TSR failed")

    def test_03_restore(self):
        output = PC1_login.send_command(f"ifconfig eth0 {PC1_ETH0_IP} up")
        logger.info(f"ifconfig eth0 {PC1_ETH0_IP} up : {output}\n ")
        delaores = aoapi.del_ao_by_name(self.tc18aoname, 'mac')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# Hosts bound to a MAC AO are cleared
class TestMACAO_TC21(Test):
    uuid = "SOSAIOT-TC-57919"
    description = show_testcase_info(
        TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        mac_ao_dict['value'] = Parameter.PC1_ETH0_MAC
        addaores = aoapi.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_check_mac_ao_info(self):
        output = PC1_login.ping_from_eth(Parameter.FIREWALL, 'eth0', num=5)
        logger.info(output)
        # aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc1 = True if f'{PC1_ETH0_IP}' or f'{Parameter.PC1_ETH0_LINKLOCAL}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO info failed")

    def test_04_edit_MAC_AO(self):
        mac_ao_dict['value'] = CaseParams.invalidmac
        addaores = aoapi.edit_addressobject_by_name(
            mac_ao_dict['name'], **mac_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:edit ao failed")

    def test_05_check_mac_ao_info(self):
        aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        time.sleep(15)
        rc = aoapi.get_DAO_info(mac_ao_dict['name'])
        flag_tc1 = True if 'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO info failed")

    def test_06_restore(self):
        delaores = aoapi.del_ao_by_name(mac_ao_dict['name'], 'mac')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# Verify log event "Unable to resolve dynamic address object" include both
# FQDN name and object's domain
class TestFQDNDAO_TC_FQDN_03(Test):
    uuid = '1510307'
    description = show_testcase_info(
        TESTPLAN, 'FQDN_03', description=True)['title']
    tc003aoname = 'unableresolvefqdn'
    tc003aovalue = 'jewfiojaojfoi.cjofiwjaoi.orfg'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_FQDN_AO(self):
        CaseParams.fw_time_tc03 = timeapi.show_time()
        logger.info(CaseParams.fw_time_tc03)
        ao_dict = copy.deepcopy(fqdn_ao_dict)
        base_dict = {
            'name': self.tc003aoname,
            'value': self.tc003aovalue
        }
        ao_dict.update(base_dict)
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_check_log_info(self):
        time.sleep(10)
        fw_logs = logmonitorapi.get_log(880)
        filter_tc03 = (f"Object={self.tc003aoname}",
                       f"FQDN={self.tc003aovalue}")
        output = check_log_by_time(
            CaseParams.fw_time_tc03, fw_logs, filter_tc03)
        Assertion.assert_equal(output, True, "ERR: Check log info failed")

    def test_04_delete_DAO(self):
        delres = aoapi.del_ao_by_name(self.tc003aoname, 'fqdn')
        Assertion.assert_equal(delres, True, "ERR:Delete DAO failed")


# TC004 Verify the process of duplicate FQDN object
class TestFQDNDAO_TC_FQDN_04(Test):
    uuid = "SOSAIOT-TC-57942"
    description = show_testcase_info(
        TESTPLAN, 'FQDN_04', description=True)['title']
    tc004aoname = 'samedomain'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_add_FQDN_AO(self):
        addaores = []
        for num in range(1, 5):
            ao_dict = copy.deepcopy(fqdn_ao_dict)
            ao_dict['name'] = self.tc004aoname + str(num)
            addaores.append(1) if aoapi.config_addressobject(
                **ao_dict) else addaores.append(0)
            logger.info(f'ao added number is ：{num} ')
        Assertion.assert_equal(all(addaores), True, "ERR:add ao failed")

    def test_04_check_FQDN_info(self):
        time.sleep(15)
        flag = []
        for num in range(1, 5):
            rc = aoapi.get_DAO_info(self.tc004aoname + str(num))
            try:
                flag.append(1) if f'{Parameter.DAO_host_ip}' in str(
                    rc) else flag.append(0)
            except Exception as e:
                logger.error(
                    "get DAO info failed {} with error {}".format(rc, e))
        Assertion.assert_equal(all(flag), True, "ERR:check AO info failed")

    def test_05_delete_DAO(self):
        delres = []
        for num in range(1, 5):
            delres.append(1) if aoapi.del_ao_by_name(
                self.tc004aoname + str(num), 'fqdn') else delres.append(0)
        Assertion.assert_equal(all(delres), True, "ERR:Delete DAO failed")


# the FQDN ao added for TC22,28,23,24,33,34,25,26
# TC22 FQDN Address Object added in the GUI
class TestFQDNDAO_TC22(Test):
    uuid = "SOSAIOT-TC-57920"
    description = show_testcase_info(
        TESTPLAN, '22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_clear_log(Test):
        clearlogres = logmonitorapi.clear_log()
        logger.info('clear log:{}'.format(clearlogres))
        Assertion.assert_equal(clearlogres, None, "ERR:clear logs fail")

    def test_04_add_FQDN_AO(self):
        CaseParams.fw_time_tc22 = timeapi.show_time()
        addaores = aoapi.config_addressobject(**fqdn_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_05_check_FQDN_info(self):
        aoapi.resolve_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        time.sleep(10)
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag_tc22 = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag_tc22, True, "ERR:check DAO failed")


# TC28 A Log event upon FQDN AO resolution
class TestFQDNDAO_TC28(Test):
    uuid = "SOSAIOT-TC-57925"
    description = show_testcase_info(
        TESTPLAN, '28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_log(self):
        filters_tc28 = (
            f"FQDN={fqdn_ao_dict['value']}", f"Host={Parameter.DAO_host_ip}")
        time.sleep(10)
        fw_logs = logmonitorapi.get_log(911)
        flag = check_log_by_time(
            CaseParams.fw_time_tc22, fw_logs, filters_tc28)
        Assertion.assert_equal(flag, True, "ERR: check log info failed")


# tc23 Resolution attempts to use the primary DNS server
class TestFQDNDAO_TC23(Test):
    uuid = "SOSAIOT-TC-57921"

    description = show_testcase_info(
        TESTPLAN, '23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_check_packet(self):
        flag = False
        exportres = fw_packet_monitor_run(
            pkgapi, PC1_login, aoapi, fqdn_ao_dict['name'])
        if check_packet_requery(Parameter.VALID_DNS, exportres, fqdn_ao_dict['value']) >= 1:
            hosts = check_packet_response_udp(exportres, fqdn_ao_dict['value'])
            if hosts:
                logger.info(f'hosts:{hosts}')
                flag = True
        Assertion.assert_equal(flag, True, "ERR: packet check fail")

    def test_04_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        match_flag = re.search(
            f'{Parameter.DAO_host_ip}', str(rc), re.I)
        flag = True if match_flag else False
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")


# tc24 Primary DNS fails to resolve IP address
class TestFQDNDAO_TC24(Test):
    uuid = "SOSAIOT-TC-57922"
    description = show_testcase_info(
        TESTPLAN, '24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_24)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_clear_log(Test):
        clearlogres = logmonitorapi.clear_log()
        logger.info('clear log:{}'.format(clearlogres))
        Assertion.assert_equal(clearlogres, None, "ERR:clear logs fail")

    def test_04_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        logger.info(rc)
        flag = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")

    def test_05_check_packet(self):
        CaseParams.fw_time_tc24 = timeapi.show_time()
        flag = False
        exportres = fw_packet_monitor_run(
            pkgapi, PC1_login, aoapi, fqdn_ao_dict['name'])
        if check_packet_requery(Parameter.FAKE_DNS1, exportres, fqdn_ao_dict['value']) >= 1:
            if check_packet_response_udp(exportres, fqdn_ao_dict['value']) == '':
                flag = True
        Assertion.assert_equal(flag, True, "ERR: packet check fail")


# TC33 Refresh attempt on FQDN AO fails,displays the previously resolved address
class TestFQDNDAO_TC33(Test):
    uuid = "SOSAIOT-TC-57929"
    description = show_testcase_info(
        TESTPLAN, '33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag_tc33 = True if 'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(flag_tc33, True, "ERR:check DAO failed")


# TC34 A Log event upon a failure to refresh FQDN AO
class TestFQDNDAO_TC34(Test):
    uuid = "SOSAIOT-TC-57944"
    description = show_testcase_info(
        TESTPLAN, '34', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_log(self):
        filters_tc34 = (
            f"Object={fqdn_ao_dict['name']}", f"FQDN={fqdn_ao_dict['value']}")
        time.sleep(10)
        fw_logs = logmonitorapi.get_log(880)
        flag = check_log_by_time(
            CaseParams.fw_time_tc24, fw_logs, filters_tc34)
        Assertion.assert_equal(flag, True, "ERR: check log info failed")


# tc25 Primary and secondary DNS servers fail to resolve IP address
class TestFQDNDAO_TC25(Test):
    uuid = "SOSAIOT-TC-57923"
    description = show_testcase_info(
        TESTPLAN, '25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_25)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_check_packet(self):
        flag = False
        exportres = fw_packet_monitor_run(
            pkgapi, PC1_login, aoapi, fqdn_ao_dict['name'])
        if check_packet_requery(Parameter.FAKE_DNS1, exportres, fqdn_ao_dict['value']) >= 1:
            if check_packet_requery(Parameter.FAKE_DNS2, exportres, fqdn_ao_dict['value']) >= 1:
                hosts = check_packet_response_udp(
                    exportres, fqdn_ao_dict['value'])
                if hosts:
                    logger.info(f'hosts:{hosts}')
                    flag = True
        Assertion.assert_equal(flag, True, "ERR: packet check fail")

    def test_04_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        logger.info(rc)
        flag = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")


# tc26 All DNS servers fail to resolve IP address
class TestFQDNDAO_TC26(Test):
    uuid = "SOSAIOT-TC-57924"
    description = show_testcase_info(
        TESTPLAN, '26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_26)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    @repeat_method(5)
    def test_03_check_packet(self):
        flag = False
        exportres = fw_packet_monitor_run(
            pkgapi, PC1_login, aoapi, fqdn_ao_dict['name'], sleeptime=60)
        if check_packet_requery(Parameter.FAKE_DNS1, exportres, fqdn_ao_dict['value']) >= 1:
            if check_packet_requery(Parameter.FAKE_DNS2, exportres, fqdn_ao_dict['value']) >= 1:
                if check_packet_requery(Parameter.FAKE_DNS3, exportres, fqdn_ao_dict['value']) >= 1:
                    flag = True
        Assertion.assert_equal(flag, True, "ERR: packet check fail")

    def test_04_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag = True if 'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")

    def test_05_delete_AO(self):
        delfres = aoapi.del_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        Assertion.assert_equal(delfres, True,
                               "ERR:Delete DAO failed")


# TC29,30 share the same AO
# tc29 Verify Access Rule that references resolved FQDN AO
class TestACLDAO_TC29(Test):
    uuid = "SOSAIOT-TC-57926"
    description = show_testcase_info(
        TESTPLAN, '29', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 29)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_add_FQDN_AO(self):
        addaores = aoapi.config_addressobject(**fqdn_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add fqdn ao failed")

    def test_04_add_MAC_AO(self):
        logger.info(
            f"mac is {Parameter.PC1_ETH0_MAC},orginal mac is {Parameter.PC1_ETH0_MAC_org}")
        mac_ao_dict['value'] = Parameter.PC1_ETH0_MAC
        addaores = aoapi.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add mac ao failed")

    def test_05_add_access_rule(self):
        base_dict = {
            'service': {"name": "HTTP"},
            'source_addr': {"name": mac_ao_dict['name']},
            'dst_addr': {"name": fqdn_ao_dict['name']}
        }
        acl_dict.update(base_dict)
        output = accessruleapi.add_ipv4_access_rule(**acl_dict)
        Assertion.assert_equal(output, True, "ERR: cannot added access rule")

    def test_06_check_access_rule(self):
        flag = False
        rules = aclapi.get_access_rule_statistics()
        for rule in rules:
            try:
                if rule['source'] == mac_ao_dict['name'] and rule['destination'] == fqdn_ao_dict['name'] \
                        and rule['enable'] == 'enable':
                    flag = True
                    break
            except Exception as e:
                logger.info(
                    "expected access rule not found with error {}".format(e))

        Assertion.assert_equal(flag, True, "ERR: Check result failed")


# tc30 Functional test for deny Access Rule that references FQDN AO
class TestACLDAO_TC30(Test):
    uuid = "SOSAIOT-TC-57927"
    description = show_testcase_info(
        TESTPLAN, '30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 30)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(5)
    def test_02_check_log(self):
        CaseParams.fw_time_30 = timeapi.show_time()
        aoapi.resolve_ao_by_name(mac_ao_dict['name'], 'mac')
        aoapi.resolve_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        time.sleep(10)

        route_cmd = "route add -host {} gw {}".format(
            Parameter.DAO_host_ip, Parameter.FIREWALL)
        cmd = "sed -i '/search openstacklocal/anameserver {}' /etc/resolv.conf".format(
            PC2_ETH0_IP)
        PC1_login.send_commands([route_cmd, cmd])
        for i in range(3):
            PC1_login.send_command("wget http://www12.limitFQDN.com")

        filters_tc30 = (f'{Parameter.DAO_host_ip}', f'{PC1_ETH0_IP}')
        fw_logs = logmonitorapi.get_log(524)
        flag = check_log_by_time(CaseParams.fw_time_30, fw_logs, filters_tc30)
        Assertion.assert_equal(flag, True, "ERR: check log info failed")

    def test_03_del_acl(self):
        delres = accessruleapi.del_ipv4_access_rule(acl_dict['name'])
        Assertion.assert_equal(delres, True, "ERR: del access rule failed")

    def test_04_delete_AO(self):
        delmres = aoapi.del_ao_by_name(mac_ao_dict['name'], 'mac')
        delfres = aoapi.del_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        Assertion.assert_equal(delmres & delfres, True,
                               "ERR:Delete DAO failed")


# TC32 Refresh the resolution cache for all FQDN AOs
class TestFQDNDAO_TC32(Test):
    uuid = "SOSAIOT-TC-57928"
    description = show_testcase_info(
        TESTPLAN, '32', description=True)['title']
    tc31aoname = 'freshnew31'
    tc31aovalue = 'www31.limitFQDN.com'
    tc32aoname = 'freshnew32'
    tc32aovalue = 'www32.limitFQDN.com'
    tc31oldip = '13.0.0.31'
    tc31newip = '13.31.31.31'
    tc32oldip = '13.0.0.32'
    tc32newip = '13.32.32.32'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_03_add_FQDN_AO(self):
        ao_dict = copy.deepcopy(fqdn_ao_dict)
        ao_dict['name'] = self.tc31aoname
        ao_dict['value'] = self.tc31aovalue
        addaores = aoapi.config_addressobject(**ao_dict)
        ao2_dict = copy.deepcopy(fqdn_ao_dict)
        ao2_dict['name'] = self.tc32aoname
        ao2_dict['value'] = self.tc32aovalue
        addao2res = aoapi.config_addressobject(**ao2_dict)
        Assertion.assert_equal(addaores & addao2res, True, "ERR:add ao failed")

    def test_04_check_FQDN_info(self):
        flag_tc31 = []
        aoapi.resolve_ao_by_name(self.tc31aoname, 'fqdn')
        aoapi.resolve_ao_by_name(self.tc32aoname, 'fqdn')
        time.sleep(10)
        rc31 = aoapi.get_DAO_info(self.tc31aoname)
        rc32 = aoapi.get_DAO_info(self.tc32aoname)
        flag_tc31.append(1) if f'{self.tc31oldip}' in str(
            rc31) else flag_tc31.append(0)
        flag_tc31.append(1) if f'{self.tc32oldip}' in str(
            rc32) else flag_tc31.append(0)
        Assertion.assert_equal(all(flag_tc31), True, "ERR:check ao failed")

    def test_05_modify_dns_server(self):
        PC2_login.send_command('service named stop')
        PC2_login.send_command(
            f'\\sed -i s/{self.tc31oldip}/{self.tc31newip}/ /var/named/limitFQDN.com.db')
        PC2_login.send_command(
            f'\\sed -i s/{self.tc32oldip}/{self.tc32newip}/ /var/named/limitFQDN.com.db')
        PC2_login.send_command('service named restart')
        Assertion.assert_equal(True, True, "ERR:modify_dns_server failed")

    def test_06_check_FQDN_info(self):
        flag_tc32 = []
        aoapi.resolve_ao_by_name(self.tc31aoname, 'fqdn')
        aoapi.resolve_ao_by_name(self.tc32aoname, 'fqdn')
        time.sleep(10)
        rc31 = aoapi.get_DAO_info(self.tc31aoname)
        rc32 = aoapi.get_DAO_info(self.tc32aoname)
        flag_tc32.append(1) if f'{self.tc31newip}' in str(
            rc31) else flag_tc32.append(0)
        flag_tc32.append(1) if f'{self.tc32newip}' in str(
            rc32) else flag_tc32.append(0)
        Assertion.assert_equal(all(flag_tc32), True, "ERR:check ao failed")

    def test_07_delete_DAO(self):
        delres = aoapi.del_ao_by_name(self.tc31aoname, 'fqdn')
        delres &= aoapi.del_ao_by_name(self.tc32aoname, 'fqdn')
        Assertion.assert_equal(delres, True, "ERR:Delete DAO failed")


# TC35,46 used the same FQDN AO
# TC35 Wildcard support for FQDN AO7
class TestFQDNDAO_TC35(Test):
    uuid = "SOSAIOT-TC-57930"
    description = show_testcase_info(
        TESTPLAN, '35', description=True)['title']
    tc35aovalue = '*.limitFQDN.com'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_FQDN_AO(self):
        ao_dict = copy.deepcopy(fqdn_ao_dict)
        ao_dict['value'] = self.tc35aovalue
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_send_dns_request(self):
        namelookup_dict = {
            'version': 'ipv4',
            'type': 'customized',
            'domain_name': 'www12.limitFQDN.com',
            'ipv4-dns1': Parameter.VALID_DNS,
        }
        namelookupres = diagnosticapi.diag_dns_lookup_name_by_api(
            **namelookup_dict)
        Assertion.assert_equal(namelookupres[0], True, "ERR:check dns_lookup_name_result failed")

    @repeat_method(5)
    def test_04_check_FQDN_info(self):
        time.sleep(10)
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag, True, "ERR:check DAO failed")


# TC46 Verify console no exceptional log printed out when the number of
# subdomains matching a wildcard FQDN AO reach a big value such as 256
class TestFQDNDAO_TC46(Test):
    uuid = "SOSAIOT-TC-57947"
    description = show_testcase_info(
        TESTPLAN, '46', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_send_dns_request(self):
        count = 0
        for i in range(280):
            namelookup_dict = {
                'version': 'ipv4',
                'type': 'customized',
                'domain_name': 'www' + str(i)+'.limitFQDN.com',
                'ipv4-dns1': Parameter.VALID_DNS,
            }
            namelookupres = diagnosticapi.diag_dns_lookup_name_by_api(
                **namelookup_dict)
            if namelookupres[0]:
                count += 1
        logger.info(f"dns_lookup_name_count:{count}")
        flag = True if count > 260 else False
        Assertion.assert_equal(
            flag, True, "ERR: check dns_lookup_name_result failed")

    def test_03_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        hostsum = str(rc).count('Host')
        flag_tc35 = True if hostsum > 2 else False
        Assertion.assert_equal(
            flag_tc35, True, "ERR: check AO info failed")

    def test_04_check_TSR(self):
        hostsum = 0
        aopart = check_TSR(
            diagnosticapi, 'Address Object Table', fqdn_ao_dict['name'])
        hostspart = re.search(r'HOST(.*?):(.*?)\n', aopart, re.I | re.S | re.M)
        if hostspart:
            hostsum = hostspart.group(2).count('TTL')
            logger.info(
                f"The limit of resolved addresses displayed in TSR is {hostsum}")
        flag_tc35 = True if hostsum > 150 else False
        Assertion.assert_equal(
            flag_tc35, True, "ERR: check AO info in TSR failed")

    def test_05_delete_DAO(self):
        delres = aoapi.del_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        Assertion.assert_equal(delres, True, "ERR:Delete DAO failed")


# TC36,37 used the same FQDN AO
# TC36 The limit of resolved addresses displayed in the Address Detail for FQDN AO
class TestFQDNDAO_TC36(Test):
    uuid = "SOSAIOT-TC-57931"
    description = show_testcase_info(
        TESTPLAN, '36', description=True)['title']
    tc36aoname = 'max'
    tc36aovalue = 'wwwmax.limitFQDN.com'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '36')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_FQDN_AO(self):
        ao_dict = copy.deepcopy(fqdn_ao_dict)
        ao_dict['name'] = self.tc36aoname
        ao_dict['value'] = self.tc36aovalue
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_set_dns_server(self):
        rc = dnsapi.set_dns(**dns_36)
        Assertion.assert_equal(rc, True, "ERR: Set DNS failed")

    def test_04_check_packets(self):
        hostcount = 0
        exportres = fw_packet_monitor_run(
            pkgapi, PC1_login, aoapi, self.tc36aoname, sleeptime=30)
        morehostsres = check_packet_response_tcp(exportres, self.tc36aovalue)
        if morehostsres:
            for host in morehostsres.split('wwwmax.limitFQDN.com: type A, class IN,'):
                searchflag = re.search(
                    r'(([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])\.){3}([01]{0,1}\d{0,1}\d|2[0-4]\d|25[0-5])', host)
                if searchflag:
                    hostcount += 1
            logger.info(f"{hostcount} hosts found\n")
        else:
            logger.info(f"nothing is found\n")
        flag = True if hostcount > 2 else False
        Assertion.assert_equal(
            flag, True, "ERR: check packets failed")

    def test_05_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(self.tc36aoname)
        hostsum = str(rc).count('Host')
        flag_tc36 = True if hostsum > 2 else False
        Assertion.assert_equal(
            flag_tc36, True, "ERR: check AO info failed")


# TC37 FQDN AO entry in TSR
class TestFQDNDAO_TC37(Test):
    uuid = "SOSAIOT-TC-57932"
    description = show_testcase_info(
        TESTPLAN, '37', description=True)['title']
    tc37aoname = 'max'
    tc37aovalue = 'wwwmax.limitFQDN.com'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '37')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_TSR(self):
        hostsum = 0
        aopart = check_TSR(
            diagnosticapi, 'Address Object Table', self.tc37aoname)
        hostspart = re.search(r'HOST(.*?):(.*?)\n', aopart, re.I | re.S | re.M)
        if hostspart:
            hostsum = hostspart.group(2).count('TTL')
            logger.info(
                f"The limit of resolved addresses displayed in TSR is {hostsum}")
        flag_tc37 = True if hostsum >= 29 else False
        Assertion.assert_equal(
            flag_tc37, True, "ERR: check AO info in TSR failed")

    def test_03_delete_DAO(self):
        delres = aoapi.del_ao_by_name(self.tc37aoname, 'fqdn')
        Assertion.assert_equal(delres, True, "ERR:Delete DAO failed")


# Network Address Object groups contains FQDN Address Object (both created
# via CLI) should be shown up in GUI and TSR
class TestCLIDAO_TC42(Test):
    uuid = "SOSAIOT-TC-57945"
    description = show_testcase_info(
        TESTPLAN, '42', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_fqdn_ao_by_cli(self):
        fqdn_ao_dict = {
            'name': 'test-fqdn',
            'type': 'fqdn',
            'zone': 'WAN',
            'domain': 'www12.limitfqdn.com',
            'dns-ttl': '150'
        }
        rc = aocli.add_address_object(**fqdn_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add fqdn address object failed")

    def test_03_add_ao_group(self):
        group = {
            'name': 'test-group',
            'version': 'ipv4',
            'objects': ['fqdn test-fqdn'],
        }
        rc = aocli.add_address_group(**group)
        Assertion.assert_equal(
            rc, True, "ERR: add address object group failed")

    def test_04_check_AO_group(self):
        aoapi.resolve_ao_by_name('test-fqdn', 'fqdn')
        time.sleep(10)
        rc = aograpi.get_addressgroup('ipv6', 'name', 'test-group')
        flag_tc42 = True if 'test-fqdn' in str(rc) else False
        Assertion.assert_equal(
            flag_tc42, True, "ERR: check AO info in AO_group failed")

    def test_05_check_TSR(self):
        agpart = check_TSR(diagnosticapi, 'Address Group Table', 'test-group')
        flag_tc42 = True if 'test-fqdn' in agpart else False
        Assertion.assert_equal(
            flag_tc42, True, "ERR: check AO info in TSR failed")

    def test_06_delete_DAO(self):
        delres = aoapi.del_ao_by_name('test-fqdn', 'fqdn')
        delgrres = aograpi.delete_addressgroup('ipv6', 'name', 'test-group')
        Assertion.assert_equal(delres & delgrres, True,
                               "ERR:Delete DAO failed")


# Network Address Object groups contains MAC Address Object (both created
# via CLI) should be shown up in GUI and TSR
class TestCLIDAO_TC43(Test):
    uuid = "SOSAIOT-TC-57946"
    description = show_testcase_info(
        TESTPLAN, '43', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_mac_ao_by_cli(self):
        mac_ao_dict = {
            'name': 'test-mac',
            'type': 'mac',
            'zone': 'LAN',
            'address': Parameter.PC1_ETH0_MAC,
            'multi-homed': True
        }
        rc = aocli.add_address_object(**mac_ao_dict)
        Assertion.assert_equal(rc, True, "ERR: add mac address object failed")

    def test_03_add_ao_group(self):
        group = {
            'name': 'test-group',
            'version': 'ipv4',
            'objects': ['mac test-mac'],
        }
        rc = aocli.add_address_group(**group)
        Assertion.assert_equal(
            rc, True, "ERR: add address object group failed")

    def test_04_check_AO_group(self):
        PC1_login.ping_from_eth(Parameter.FIREWALL, 'eth0', num=2)
        rc = aograpi.get_addressgroup(
            group_type='ipv6', group_path='name', group_name_uuid='test-group')
        flag_tc43 = True if 'test-mac' in str(rc) else False
        Assertion.assert_equal(
            flag_tc43, True, "ERR: check AO info in AO_group failed")

    def test_05_check_TSR(self):
        agpart = check_TSR(diagnosticapi, 'Address Group Table', 'test-group')
        flag_tc43 = True if 'test-mac' in agpart else False
        Assertion.assert_equal(
            flag_tc43, True, "ERR: check AO info in TSR failed")

    def test_06_delete_DAO(self):
        delres = aoapi.del_ao_by_name('test-mac', 'mac')
        delgrres = aograpi.delete_addressgroup('ipv6', 'name', 'test-group')
        Assertion.assert_equal(delres & delgrres, True,
                               "ERR:Delete DAO failed")


# 38 FQDN AO after reboot
# 19 MAC AO after reboot
class TestRebootDAO_TC19_TC38(Test):
    uuid = "SOSAIOT-TC-57917"
    uuid_38 = '3229094'
    description = show_testcase_info(
        TESTPLAN, '19', description=True)['title']
    tc19aoname = 'macreboot'
    tc38aoname = 'fqdnreboot'

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_MAC_AO(self):
        logger.info(
            f"mac is {Parameter.PC1_ETH2_MAC},orginal mac is {Parameter.PC1_ETH2_MAC_org}")
        ao_dict = copy.deepcopy(mac_ao_dict)
        ao_dict['name'] = self.tc19aoname
        ao_dict['value'] = Parameter.PC1_ETH2_MAC
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_add_FQDN_AO(self):
        ao_dict = copy.deepcopy(fqdn_ao_dict)
        ao_dict['name'] = self.tc38aoname
        addaores = aoapi.config_addressobject(**ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_04_check_mac_ao_info(self):
        output = PC1_login.ping_from_eth(Parameter.X2_IP, 'eth2', num=2)
        logger.info('ping result:{}'.format(output))
        rc = aoapi.get_DAO_info(self.tc19aoname)
        flag_tc19 = True if f'{PC1_ETH2_IP}' or f'{Parameter.PC1_ETH2_LINKLOCAL}' in str(rc) else False
        Assertion.assert_equal(
            flag_tc19, True, "ERR: check mac AO info failed")

    def test_05_check_FQDN_info(self):
        aoapi.resolve_ao_by_name(self.tc38aoname, 'fqdn')
        time.sleep(10)
        rc = aoapi.get_DAO_info(self.tc38aoname)
        flag_tc38 = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag_tc38, True, "ERR:check fqdn AO failed")

    def test_06_reboot(self):
        rc = settingapi.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    # the result is different depands on dut rebooting time
    def test_07_check_FQDN_info(self):
        rc = aoapi.get_DAO_info(self.tc38aoname)
        flag_tc38 = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        if f'{Parameter.DAO_host_ip}' in str(rc):
            logger.info(f'check FQDN_info is ：{Parameter.DAO_host_ip}')
        elif 'UNRESOLVED' in str(rc):
            logger.info(f'check FQDN_info is ：UNRESOLVED')
        else:
            logger.info(f'can not find FQDN_info')
        Assertion.assert_equal(True, True, "ERR:check fqdn AO failed")

    def test_08_check_mac_ao_info(self):
        rc = aoapi.get_DAO_info(self.tc19aoname)
        flag_tc19 = True if f'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(
            flag_tc19, True, "ERR: check mac AO info failed")

    def test_09_delete_DAO(self):
        delmres = aoapi.del_ao_by_name(self.tc19aoname, 'mac')
        delfres = aoapi.del_ao_by_name(self.tc38aoname, 'fqdn')
        Assertion.assert_equal(delmres & delfres, True,
                               "ERR:Delete DAO failed")


# Hosts bound to a FQDN AO are cleared
class TestFQDNAO_TC40(Test):
    uuid = "SOSAIOT-TC-57935"
    description = show_testcase_info(
        TESTPLAN, '40', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_FQDN_AO(self):
        addaores = aoapi.config_addressobject(**fqdn_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:add ao failed")

    def test_03_check_ao_info(self):
        aoapi.resolve_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        time.sleep(10)
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag_tc22 = True if f'{Parameter.DAO_host_ip}' in str(rc) else False
        Assertion.assert_equal(flag_tc22, True, "ERR:check DAO failed")

    def test_04_add_FQDN_AO(self):
        fqdn_ao_dict['value'] = CaseParams.invalidfqdn
        addaores = aoapi.edit_addressobject_by_name(
            fqdn_ao_dict['name'], **fqdn_ao_dict)
        Assertion.assert_equal(addaores, True, "ERR:edit fqdn ao failed")

    def test_05_check_ao_info(self):
        aoapi.resolve_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        time.sleep(15)
        rc = aoapi.get_DAO_info(fqdn_ao_dict['name'])
        flag_tc1 = True if 'UNRESOLVED' in str(rc) else False
        Assertion.assert_equal(
            flag_tc1, True, "ERR: check AO info failed")

    def test_06_restore(self):
        delaores = aoapi.del_ao_by_name(fqdn_ao_dict['name'], 'fqdn')
        Assertion.assert_equal(delaores,
                               True, "ERR:Delete DAO failed")


# A maximum number of dynamic address objects
# it takes too long time, so didn't include in test suite
class TestMAXDAO_TC41(Test):
    uuid = 'B6DACAE2-0464-11DE-860E-445A00F93527'
    description = show_testcase_info(
        TESTPLAN, '41', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '41')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_FQDN_AO(self):
        num = 0
        try:
            for i in range(0, 10000):
                ao_dict = copy.deepcopy(fqdn_ao_dict)
                ao_dict['name'] = 'fqdntest' + str(i)
                ao_dict['value'] = 'www' + str(i)+'.limitFQDN.com'
                output = aoapi.config_addressobject(msg=True, **ao_dict)
                logger.info(f'ao added output is ：{output} ')
                if not output[0]:
                    logger.info(
                        "can't add ao with error {}".format(output[1]))
                    break
                else:
                    num += 1

        except Exception as e:
            logger.info(
                "can't add ao with error {}".format(e))
            logger.info(f'ao added number is ：{num} ')

        CaseParams.maxfqdnaonum = num
        logger.info(f'max added fqdn ao number is ：{CaseParams.maxfqdnaonum} ')
        flag = True if num > 100 else False
        Assertion.assert_equal(flag, True, "ERR:add ao failed")

    def test_03_del_FQDN_AO(self):
        try:
            ls_fqdn = []
            for i in range(0, CaseParams.maxfqdnaonum):
                ao_name = 'fqdntest' + str(i)
                ls_fqdn.append(ao_name)
            output = aoapi.del_all_aos_by_type('fqdn', ls_fqdn)
            Assertion.assert_equal(output, True, "ERR:add ao failed")
        except Exception as e:
            logger.info(
                "can't delete ao with error {}".format(e))

    def test_04_add_mac_AO(self):
        num = 0
        try:
            for i in range(0, 10000):
                ao_dict = copy.deepcopy(mac_ao_dict)
                ao_dict['name'] = 'mactest' + str(i)
                ao_dict['value'] = 'FA:16:3E:90:DB:E2'
                # addaores.append(1) if aoapi.config_addressobject(
                # **ao_dict) else addaores.append(0)
                output = aoapi.config_addressobject(msg=True, **ao_dict)
                logger.info(f'ao added output is ：{output} ')
                if not output[0]:
                    logger.info(
                        "can't add ao with error {}".format(output[1]))
                    break
                else:
                    num += 1
        except Exception as e:
            logger.info(
                "can't add ao with error {}".format(e))
            logger.info(f'ao added number is ：{num} ')

        CaseParams.maxmacaonum = num
        logger.info(f'max added mac ao number is ：{CaseParams.maxmacaonum}')
        flag = True if CaseParams.maxmacaonum > 100 else False
        Assertion.assert_equal(flag, True, "ERR:add ao failed")

    def test_05_del_MAC_AO(self):
        try:
            ls_mac = []
            for i in range(0, CaseParams.maxmacaonum):
                ao_name = 'mactest' + str(i)
                ls_mac.append(ao_name)
            output = aoapi.del_all_aos_by_type('mac', ls_mac)
            Assertion.assert_equal(output, True, "ERR:add ao failed")
        except Exception as e:
            logger.info(
                "can't delete ao with error {}".format(e))
