from definition.settings import *
from definition.utils import *


# [GUI] Verifty that it can create a nativebrige group
class TestGUI_TC005(Test):
    uuid = "SOSAIOT-TC-56884"
    description = show_testcase_info(
        TESTPLAN, '1525894', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525894')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_configure_x2_nativebridge(self):
        x2_native = {
            'if': 'X2',
            'zone': 'LAN',  # LAN, DMZ, custom zone name
            'mode': 'nativebridge',
            'native_bridge_to': 'X0',
            "firewalling": False,
        }
        rc = interfaceapi.config_interface(**x2_native)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 failed!")


# [FunctionI] Verify that physical interface can be nativebridged to physical interface
# and traffic work
class TestFunc_TC034(Test):
    uuid = "SOSAIOT-TC-56887"
    description = show_testcase_info(
        TESTPLAN, '1525898', description=True)['title']
    res_for_test_tc63 = ContextVar('res_for_test_tc63')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525898')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_traffic_between_pc(self):
        PC3_Login.send_command(f"ip addr del {Parameter.X2_GW}/24 dev eth1")
        PC3_Login.send_command(f"ip addr add {Parameter.X2_PC}/24 dev eth1")
        rc = PC3_Login.send_command("ifconfig eth1")
        flag = True if Parameter.X2_PC in str(rc) else False
        logger.info(f"change eth1 ip result： {flag}")  

        rc1 = PC3_Login.ping_from_eth(Parameter.X0_PC, 'eth1')
        rc2 = PC1_Login.ping_from_eth(Parameter.X2_PC, 'eth1')
        self.res_for_test_tc63.set(rc1 & rc2 )

        Assertion.assert_equal(rc1&rc2 , True, "ERR: check packet failed")

    def test_03_check_traffic_from_x2_to_x1(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)

        PC3_Login.send_command(f"ip route add {Parameter.DNS1} via {Parameter.FIREWALL} dev eth1")
        rc = PC3_Login.send_command("ip -4 r")
        flag = True if Parameter.DNS1 in str(rc) else False
        logger.info(f"add route result： {flag}")  
   
        pingres = PC3_Login.ping_from_eth(Parameter.DNS1, 'eth1')
        logger.info(f"ping {Parameter.DNS1} result is {pingres}")

        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("Echo (ping) request", Parameter.DNS1, 'X1')
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")


# [Function] Verify that traffic works when set NativeBridge host as LAN
class TestFunc_TC063(Test):
    uuid = "SOSAIOT-TC-56897"
    description = show_testcase_info(
        TESTPLAN, '1525909', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525909')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_traffic_between_pc(self):
        res = TestFunc_TC034().res_for_test_tc63.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


#  [FunctionI] Verify that physical interface can be nativebridged to Virtual interface
#  which parent interface is different to the physical interface and traffic work
class TestFunc_TC032(Test):
    uuid = "SOSAIOT-TC-56886"
    description = show_testcase_info(
        TESTPLAN, '1525897', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525897')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_configure_x3_vlan(self):
        x3_vlan1_dict = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID,
            'zone': 'dmz',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        (rc1, msg1) = interfaceapi.add_interface(msg=True, **x3_vlan1_dict)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Configure VLAN failed!")

    def test_03_configure_x4_nativebridge(self):
        x4_native = {
            'if': 'X4',
            'zone': 'LAN',  # LAN, DMZ, custom zone name
            'mode': 'nativebridge',
            'native_bridge_to': f'X3:V{X3_VLAN1_ID}',
            "firewalling": False,
        }
        rc = interfaceapi.config_interface(**x4_native)
        Assertion.assert_equal(rc, True, "ERR: Configure X4 failed!")

    def test_04_add_dhcp_lease_scope(self):
        (rc1, msg1) = dhcpserverapi.add_dhcp_server_scope_dynamic(msg=True, **dynamic_scope_base)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, 'ERR: add dhcp lease for x2 failed')

    def test_05_pc4_get_dhcp_lease(self):
        PC4_Login.send_command('cp /dev/null /etc/resolv.conf')
        PC4_Login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        (res, ip_addr) = pc_get_ip_lease(PC4_Login, 'eth1')
        CaseParams.tc48_pc4_ip = ip_addr
        Assertion.assert_equal(
            res, True, 'ERR: PC2 get dhcp lease from DUT failed')

    def test_06_pc5_get_dhcp_lease(self):
        PC5_Login.send_command('cp /dev/null /etc/resolv.conf')
        PC5_Login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        (res, ip_addr) = pc_get_ip_lease(PC5_Login, 'eth1')
        CaseParams.tc48_pc5_ip = ip_addr
        Assertion.assert_equal(
            res, True, 'ERR: PC2 get dhcp lease from DUT failed')

    def test_07_check_traffic_between_pc(self):
        rc1  = PC4_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        rc2  = PC5_Login.ping_from_eth(CaseParams.tc48_pc4_ip, 'eth1')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: check packet failed")


# [Function] Verify that hosts under nativebridged interfaces can access hosts belong to other zones
class TestFunc_TC073(Test):
    uuid = "SOSAIOT-TC-56898"
    description = show_testcase_info(
        TESTPLAN, '1525910', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525910')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_dmz_to_lan_deny_acl(self):
        acl_dict = copy.deepcopy(acl_base)
        update_dict ={
            "name": "dmz_to_lan",
            "from": "DMZ",
            "to": "LAN",
            "action": "allow"}
        acl_dict.update(update_dict)
        (res, msg) = acl_api.config_accessrule(msg=True, **acl_dict)
        if res is False:
            res = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(res, True, 'ERR: add acl allow wan to wan ipv4 failed!')

    def test_03_check_traffic_between_lan_dmz_zone(self):
        PC1_Login.send_command(f"ip route add 13.1.1.0/24 via {Parameter.FIREWALL} dev eth1")
        rc1 = PC1_Login.send_command("ip -4 r")
        flag1 = True if "13.1.1.0/24" in str(rc1) else False
        logger.info(f"add route result： {flag1}")  

        PC4_Login.send_command(f"ip route add {Parameter.X0_PC} via {Parameter.X3_IP} dev eth1")
        rc2 = PC4_Login.send_command("ip -4 r")
        flag2 = True if Parameter.X0_PC in str(rc2) else False
        logger.info(f"add route result： {flag2}")  

        PC5_Login.send_command(f"ip route add {Parameter.X0_PC} via {Parameter.X3_IP} dev eth1")
        rc3 = PC5_Login.send_command("ip -4 r")
        flag3 = True if Parameter.X0_PC in str(rc3) else False
        logger.info(f"add route result： {flag3}")  

        rc1 = PC5_Login.ping_from_eth(Parameter.X0_PC, 'eth1')
        rc2 = PC4_Login.ping_from_eth(Parameter.X0_PC, 'eth1')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: check packet failed")


# [GUI] Verify that nativebridge host should not be allowed to
# unassign when has at least one nativebridge member
class TestGUI_TC011(Test):
    uuid = "SOSAIOT-TC-56885"
    description = show_testcase_info(
        TESTPLAN, '1525895', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525895')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_unassign_x3_vlan(self):
        (rc, msg) = interfaceapi.unassign_vlan_interface( msg=True, interface='X3', vlan_id= f'{X3_VLAN1_ID}')
        logger.info(msg)
        #"Native bridge host interface can't be unassigned"
        Assertion.assert_equal(rc, False, "ERR: unassign X3 vlan!")

#  [Negative] Verify that the Virtual interface as nativebridged host can not be deleted
class TestFunc_TC074(Test):
    uuid = "SOSAIOT-TC-56899"
    description = show_testcase_info(
        TESTPLAN, '1525911', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525911')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_delete_vlan(self):
        x3_vlan1_dict = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID
        }
        (rc, msg) = interfaceapi.del_interface(msg=True, **x3_vlan1_dict)
        logger.info(msg)
        # 'message': 'Index of the interface.: This interface is used as NativeBridge host'
        Assertion.assert_equal(rc, False, "ERR: delete X3 vlan!")


# [FunctionI] Verify that Virtual interface can be nativebridged to physical interface
# which is different to its parent and traffic work
class TestFunc_TC036(Test):
    uuid = "SOSAIOT-TC-56888"
    description = show_testcase_info(
        TESTPLAN, '1525899', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525899')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_unassign_x4_and_x3_vlan(self):
        rc1 = interfaceapi.unassign_interface(interface='X4')
        Assertion.assert_equal(rc1, True, "ERR: unassign interface failed!")

    def test_03_config_interface_X4(self):
        x4_static = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        (rc1, msg1) = interfaceapi.config_interface(msg=True, **x4_static)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Config X4 to static failed")

    def test_04_configure_x3_vlan(self):
        x3_native = {
            'if': 'x3',
            'type': 'vlan',
            'vlan_tag': X3_VLAN1_ID,
            'zone': 'LAN',  # LAN, DMZ, custom zone name
            'mode': 'nativebridge',
            'native_bridge_to': 'X4',
            "firewalling": True,
        }
        (rc1, msg1) = interfaceapi.add_interface(msg=True, **x3_native)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, "ERR: Configure X3 VLAN failed!")

    def test_05_check_traffic_between_pc(self):
        rc1 = PC4_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        rc2 = PC5_Login.ping_from_eth(CaseParams.tc48_pc4_ip, 'eth1')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: check packet failed")

    def test_06_check_traffic_from_x3_to_x1(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)

        PC4_Login.send_command(f"ip route add {Parameter.DNS1} via {Parameter.X3_IP} dev eth1")
        rc = PC4_Login.send_command("ip -4 r")
        flag = True if Parameter.DNS1 in str(rc) else False
        logger.info(f"add route result： {flag}")
        
        pingres = PC4_Login.ping_from_eth(Parameter.DNS1, 'eth1')
        logger.info(f"ping {Parameter.DNS1} result is {pingres}")

        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("Echo (ping) request", Parameter.DNS1, 'X1')
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")


#  [Function] Verify that multi-interfaces are all nativebridged to
#  the same nativebridge host and all traffic work
class TestFunc_TC039(Test):
    uuid = "SOSAIOT-TC-56889"
    description = show_testcase_info(
        TESTPLAN, '1525900', description=True)['title']
    res_for_test_tc53 = ContextVar('res_for_test_tc53')

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525900')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_configure_x2_nativebridge(self):
        x2_native = {
            'if': 'X2',
            'zone': 'LAN',  # LAN, DMZ, custom zone name
            'mode': 'nativebridge',
            'native_bridge_to': 'X4',
            "firewalling": True,
        }
        rc = interfaceapi.config_interface(**x2_native)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 failed!")

    def test_03_check_traffic_from_x2_to_x0(self):
        PC3_Login.send_command(f"ip addr del {Parameter.X2_PC}/24 dev eth1")
        PC3_Login.send_command(f"ip addr add {Parameter.X2_PC_2}/24 dev eth1")
        rc = PC3_Login.send_command("ifconfig eth1")
        flag = True if Parameter.X2_PC_2 in str(rc) else False
        logger.info(f"change eth1 ip result： {flag}") 

        rc1 = PC5_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc2 = PC4_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc3 = PC3_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        rc4 = PC3_Login.ping_from_eth(CaseParams.tc48_pc4_ip, 'eth1')
        self.res_for_test_tc53.set(rc1 & rc2 & rc3 & rc4)
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4, True, "ERR: check packet failed")


# [Function] Verify that TCP traffic works among nativebridge member or through native host
class TestFunc_TC051(Test):
    uuid = "SOSAIOT-TC-56893"
    description = show_testcase_info(
        TESTPLAN, '1525904', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525904')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_send_packet_from_pc3(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)

        logger.info('cp send_packet_from_pc.py ...')
        PC3_Login.send_command('cp {} /tmp/'.format(defi_path + 'scripts/send_packet_from_pc.py'))
        result = PC3_Login.send_command('ls /tmp/')
        if 'send_packet_from_pc.py' in str(result):
            sendres = PC3_Login.send_command(
                "python3 {} -dst {} -protocol {}".format('/tmp/send_packet_from_pc.py', CaseParams.tc48_pc5_ip, "TCP"))
            logger.info('Send tcp packet result:{}'.format(sendres))

        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("TCP", 'X4', CaseParams.tc48_pc5_ip,'3389')
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")

    def test_03_send_packet_from_pc4(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)

        logger.info('cp send_packet_from_pc.py ...')
        PC4_Login.send_command('cp {} /tmp/'.format(defi_path + 'scripts/send_packet_from_pc.py'))
        result = PC4_Login.send_command('ls /tmp/')
        if 'send_packet_from_pc.py' in str(result):
            sendres = PC4_Login.send_command(
                "python3 {} -dst {} -protocol {}".format('/tmp/send_packet_from_pc.py', Parameter.X2_PC_2, "TCP"))
            logger.info('Send tcp packet result:{}'.format(sendres))

        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("TCP", 'X4', Parameter.X2_PC_2,'3389')
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")


#  [Function] Verify that UDP traffic works among nativebridge member or through native host
class TestFunc_TC052(Test):
    uuid = "SOSAIOT-TC-56894"
    description = show_testcase_info(
        TESTPLAN, '1525905', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525905')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_send_packet_from_pc3(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)
        result = PC3_Login.send_command('ls /tmp/')
        if 'send_packet_from_pc.py' in str(result):
            sendres = PC3_Login.send_command(
                "python3 {} -dst {} -protocol {}".format('/tmp/send_packet_from_pc.py', CaseParams.tc48_pc4_ip, "UDP"))
            logger.info('Send tcp packet result:{}'.format(sendres))
        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("UDP", 'X4', CaseParams.tc48_pc4_ip,'3389')
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")

    def test_03_send_packet_from_pc4(self):
        fw_packet_monitor_clear_start(pkgmonitorapi)

        logger.info('cp send_packet_from_pc.py ...')
        PC5_Login.send_command('cp {} /tmp/'.format(defi_path + 'scripts/send_packet_from_pc.py'))
        result = PC5_Login.send_command('ls /tmp/')
        if 'send_packet_from_pc.py' in str(result):
            sendres = PC5_Login.send_command(
                "python3 {} -dst {} -protocol {}".format('/tmp/send_packet_from_pc.py', Parameter.X2_PC_2, "UDP"))
            logger.info('Send tcp packet result:{}'.format(sendres))
        filteredpackets = fw_packet_monitor_stop_export(
            pkgmonitorapi, PC1_Login)
        expectpkt = ("UDP", 'X4','3389', Parameter.X2_PC_2)
        checkres = check_packets(filteredpackets, expectpkt)
        Assertion.assert_equal(checkres, True, "ERR: check packet failed")


# [Function] Verify that ICMP traffic works among nativebridge member or through native host
class TestFunc_TC053(Test):
    uuid = "SOSAIOT-TC-56895"
    description = show_testcase_info(
        TESTPLAN, '1525906', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525906')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_icmp_packet(self):
        res = TestFunc_TC039().res_for_test_tc53.get()
        Assertion.assert_equal(res, True, "ERR: check packet failed")


#  [Intergration] Reboot with NativeBridge settings
class TestFunc_TC090(Test):
    uuid = "SOSAIOT-TC-56902"
    description = show_testcase_info(
        TESTPLAN, '1525914', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525914')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_show_interface(self):
        count = 0
        res = interfaceapi.get_ipv4_interface()
        try:
            for interface_info in res["interfaces"]:
                if "native_bridge" in str(interface_info) and interface_info['ipv4']['native_bridge']:
                    logger.info(interface_info)
                    count = count + 1
        except Exception as e:
            logger.error(repr(e))
        Assertion.assert_equal(count, 2, "ERR: count native bridge interfaces failed")

    def test_03_reboot(self):
        rc = settingapi.boot_fw(1)
        Assertion.assert_equal(rc, True, f"ERR: reboot failed.")

    def test_04_show_interface(self):
        self.test_02_show_interface()


# [Integration] Static ARP works for NativeBridge host /member
class TestFunc_TC084(Test):
    uuid = "SOSAIOT-TC-56901"
    description = show_testcase_info(
        TESTPLAN, '1525913', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525913')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_static_arp_for_X2(self):
        Parameter.X2_PC_MAC = get_pc_int_mac(PC3_Login, 'eth1')
        logger.info(f'X2_PC_MAC is :{Parameter.X2_PC_MAC}')
        x2_arp_dict = {
            'ip': Parameter.X2_PC_2,
            'mac': Parameter.X2_PC_MAC,
            'interface': 'X4',
            'publish': False,
            'bind_mac': False,
            'dynamic': False
        }
        output = arpapi.add_static_arp(**x2_arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_03_add_static_arp_for_X4(self):
        Parameter.X4_PC_MAC = get_pc_int_mac(PC5_Login, 'eth1')
        logger.info(f'X4_PC_MAC is :{Parameter.X4_PC_MAC}')
        Parameter.X3_PC_MAC = get_pc_int_mac(PC4_Login, 'eth1')
        logger.info(f'X3_PC_MAC is :{Parameter.X3_PC_MAC}')
        x4_arp_dict = {
            'ip': CaseParams.tc48_pc5_ip,
            'mac': Parameter.X4_PC_MAC,
            'interface': 'X4',
            'publish': False,
            'bind_mac': False,
            'dynamic': False
        }
        output = arpapi.add_static_arp(**x4_arp_dict)
        Assertion.assert_equal(output, True, "add static ARP entry failed")

    def test_04_check_traffic_between_pc(self):
        rc1 = PC5_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc2 = PC3_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: check packet failed")


# [Function] Verify that dhcp traffic can flood among nativebridged member
class TestFunc_TC048(Test):
    uuid = "SOSAIOT-TC-56892"
    description = show_testcase_info(
        TESTPLAN, '1525903', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525903')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_dhcp_lease_scope(self):
        (rc1, msg1) = dhcpserverapi.add_dhcp_server_scope_dynamic(msg=True, **dynamic_scope_base)
        if rc1 is False:
            rc1 = True if 'Already exists' in str(msg1) else False
        Assertion.assert_equal(rc1, True, 'ERR: add dhcp lease for x2 failed')

    def test_03_pc4_get_dhcp_lease(self):
        PC3_Login.send_command("nohup tshark -i eth1 -a duration:300 -w /tmp/dhcp.pcap > /tmp/tsharkcapture.log 2>&1 &")
        PC4_Login.send_command('cp /dev/null /etc/resolv.conf')
        PC4_Login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        (res, ip_addr) = pc_get_ip_lease(PC4_Login, 'eth1')
        CaseParams.tc48_pc4_ip = ip_addr
        Assertion.assert_equal(
            res, True, 'ERR: PC2 get dhcp lease from DUT failed')

    def test_04_pc5_get_dhcp_lease(self):
        PC5_Login.send_command('cp /dev/null /etc/resolv.conf')
        PC5_Login.send_command(f'rm -rf {DHCLIEN_LEASE_FILE}')
        (res, ip_addr) = pc_get_ip_lease(PC5_Login, 'eth1')
        CaseParams.tc48_pc5_ip = ip_addr
        Assertion.assert_equal(
            res, True, 'ERR: PC2 get dhcp lease from DUT failed')

    def test_05_check_packet(self):
        rc1  = PC3_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        rc2  = PC4_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        rc3  = PC5_Login.ping_from_eth(CaseParams.tc48_pc3_ip, 'eth1')
        rc4  = PC5_Login.ping_from_eth(CaseParams.tc48_pc4_ip, 'eth1')
        Assertion.assert_equal(rc1 & rc2 & rc3 & rc4, True, "ERR: check packet failed")

    def test_06_check_dhcp_packet(self):
        PC3_Login.send_command("/usr/bin/pkill tshark")
        filterdnscmd = f'tshark -r /tmp/dhcp.pcap -V -T text'
        logger.info(f'filterdnscmd: {filterdnscmd}')
        filteredpackets = PC3_Login.send_command(filterdnscmd)
        expectpkt1 = ("DHCP", Parameter.X4_PC_MAC)
        checkres1 = check_packets(filteredpackets, expectpkt1, packet_from = "pc")
        expectpkt2 = ("DHCP", Parameter.X3_PC_MAC)
        checkres2 = check_packets(filteredpackets, expectpkt2, packet_from = "pc")
        Assertion.assert_equal(checkres1 | checkres2, True, "ERR: check packet failed")


# [Function] Verify that ARP traffic can flood among nativebridged member
class TestFunc_TC047(Test):
    uuid = "SOSAIOT-TC-56891"
    description = show_testcase_info(
        TESTPLAN, '1525902', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525902')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_check_arp_packet(self):
        filterdnscmd = f'tshark -r /tmp/dhcp.pcap -V -T text'
        logger.info(f'filterdnscmd: {filterdnscmd}')
        filteredpackets = PC3_Login.send_command(filterdnscmd)
        expectpkt1 = ("ARP","Address Resolution Protocol (request)", Parameter.X4_PC_MAC)
        checkres1 = check_packets(filteredpackets, expectpkt1, packet_from = "pc")
        expectpkt2 = ("ARP", "Address Resolution Protocol (request)", Parameter.X3_PC_MAC)
        checkres2 = check_packets(filteredpackets, expectpkt2, packet_from = "pc")
        Assertion.assert_equal(checkres1 & checkres2, True, "ERR: check packet failed")


#  [Function] Verify that access rule for the traffic through nativebridge members can work
#  after enable firewalling on this bridge interface
class TestFunc_TC041(Test):
    uuid = "SOSAIOT-TC-56890"
    description = show_testcase_info(
        TESTPLAN, '1525901', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1525901')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_lan_to_lan_deny_acl(self):
        acl_dict = copy.deepcopy(acl_base)
        acl_dict.update({"name": "lan_to_lan"})
        (res, msg) = acl_api.config_accessrule(msg=True, **acl_dict)
        if res is False:
            res = True if 'Already exists' in str(msg) else False
        Assertion.assert_equal(res, True, 'ERR: add acl allow wan to wan ipv4 failed!')

    def test_03_check_traffic_between_pc(self):
        rc1 = PC5_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc2 = PC4_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc3 = PC3_Login.ping_from_eth(CaseParams.tc48_pc4_ip, 'eth1')
        rc4 = PC3_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')

        Assertion.assert_equal(rc1 | rc2 | rc3 | rc4, False, "ERR: check packet failed")

    def test_04_configure_x2_nativebridge(self):
        x2_native = {
            'if': 'X2',
            'zone': 'LAN',  # LAN, DMZ, custom zone name
            'mode': 'nativebridge',
            'native_bridge_to': 'X4',
            "firewalling": False,
        }
        rc = interfaceapi.config_interface(**x2_native)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 failed!")

    def test_05_check_traffic_between_pc(self):
        rc1 = PC5_Login.ping_from_eth(Parameter.X2_PC_2, 'eth1')
        rc2 = PC3_Login.ping_from_eth(CaseParams.tc48_pc5_ip, 'eth1')
        Assertion.assert_equal(rc1 & rc2, True, "ERR: check packet failed")
