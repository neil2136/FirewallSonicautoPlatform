from definition.global_v import *


class TestDHCPServer_01(Test):
    uuid = "SOSAIOT-TC-55865"
    description= show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Enable_DHCP_Server(self):
        dhcp_server_settings = {
            "dhcp_server": {
                "ipv4": {
                    "enable": True
                }
            }
        }
        ret = dhcp_obj.config_dhcp_server_settings( **dhcp_server_settings ) 
        Assertion.assert_equal(ret, True, "ERR: Enable DHCP Server failed") 

    def test_02_Verify_DHCP_Server_Status(self):
        flag = False
        ret = dhcp_obj.get_dhcp_server_settings()
        if ret['dhcp_server']['ipv4']['enable'] == True:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Enable DHCP Server failed") 


class TestDHCPServer_18(Test):
    uuid = "SOSAIOT-TC-55871"
    description= show_testcase_info(TESTPLAN, '18', description=True)['title']
    PC1_ETH1_MAC = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_get_X2_connetcted_PC1_interface_mac(self):
        ret = False
        TestDHCPServer_18.PC1_ETH1_MAC = os.popen("ifconfig eth1|grep HWaddr|awk '{print $5}'").read()
        TestDHCPServer_18.PC1_ETH1_MAC = TestDHCPServer_18.PC1_ETH1_MAC.replace('\n', '')
        logger.info(TestDHCPServer_18.PC1_ETH1_MAC)
        b = TestDHCPServer_18.PC1_ETH1_MAC.split(':')
        TestDHCPServer_18.PC1_ETH1_MAC = ''.join(b)
        logger.info(TestDHCPServer_18.PC1_ETH1_MAC)
        if len(TestDHCPServer_18.PC1_ETH1_MAC) == 12:
            ret = True
        Assertion.assert_equal(ret, True, "ERR: Get X2 connected PC1 interface mac failed")

    def test_02_add_valid_static_entry(self):
        static_entry = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "static": [
                            {
                                "ip": "2.2.2.200",
                                "mac": TestDHCPServer_18.PC1_ETH1_MAC,
                                "enable": True,
                                "name": "test",
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret = dhcp_obj.add_dhcp_server_scope_static( **static_entry)
        Assertion.assert_equal(ret, True, "ERR: Add valid static entry failed")

    def test_03_delete_the_added_static_entry(self):
        ret = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'static', p1 = '2.2.2.200', p2 = TestDHCPServer_18.PC1_ETH1_MAC )
        Assertion.assert_equal(ret, True, "ERR: Delete valid static entry failed")

 
class TestDHCPServer_30(Test):
    uuid = "SOSAIOT-TC-55884"
    description= show_testcase_info(TESTPLAN, '30', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '30')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_multiple_dynamic_entries_to_X2(self):
        dynamic_entry1 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.10",
                                "to": "2.2.2.20",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret1 = dhcp_obj.add_dhcp_server_scope_dynamic( **dynamic_entry1 )
        dynamic_entry2 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.30",
                                "to": "2.2.2.40",
                                "enable": True,
                                "lease_time": 1440,
                                "default_gateway": "2.2.2.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret2 = dhcp_obj.add_dhcp_server_scope_dynamic( **dynamic_entry2 )
        Assertion.assert_equal(ret1 & ret2, True, "ERR: Add dynamic entries failed")     

    def test_02_verify_multiple_clients_can_get_correct_leases(self):
        flag = 0
        os.system("ifconfig eth1 0.0.0.0")
        os.system("killall dhclient")
        output = os.popen("timeout 20 dhclient -v eth1 2>&1", 'r', 10).read()
        logger.info(output)
        m = re.search(r'bound to (2\.2\.2\.\d+).*renewal in', output, re.I)
        if m:
            logger.info("PC1 eth1 successfully get ip address {}".format(m.group(1)))
            flag = flag + 1
        else:
            logger.info("failed to get ip address for PC1 eth1")

        PC2_login.send_command("ifconfig eth1 0.0.0.0") 
        PC2_login.send_command("killall dhclient")
        output = PC2_login.send_command("dhclient -v eth1;sleep 10;")
        m = re.search(r'bound to (2\.2\.2\.\d+).*renewal in', output, re.I)
        if m:
            logger.info("PC2 eth1 successfully get ip address {}".format(m.group(1)))
            flag = flag + 1
        else:
            logger.info("failed to get ip address for PC2 eth1")
        Assertion.assert_equal(flag, 2, "ERR: Verify multiple clients can get correct leases failed")     
 
    def test_03_restore_test_environment(self):
        os.system("ifdown eth1; timeout 5 ifup eth1")
        PC2_login.send_command("ifdown eth1; timeout 5 ifup eth1") 
        ret1 = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'dynamic', p1 = '2.2.2.10', p2 = '2.2.2.20' )
        ret = dhcp_obj.get_dhcp_server_scope_dynamic()
        logger.info(ret)
        logger.info(ret['dhcp_server']['ipv4']['scope']['dynamic'][0])
        if ret['dhcp_server']['ipv4']['scope']['dynamic'][0]['from'] == '2.2.2.30':
            ret2 = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'dynamic', p1 = '2.2.2.30', p2 = '2.2.2.40' )
            Assertion.assert_equal(ret1 & ret2, True, "ERR: Restore test environment failed")
        else:
            Assertion.assert_equal(ret1, True, "ERR: Restore test environment failed")


class TestDHCPServer_39(Test):
    uuid = "SOSAIOT-TC-55893"
    description= show_testcase_info(TESTPLAN, '39', description=True)['title']
    pc1_eth1_ip = ''

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_entry_to_X2(self):
        dynamic_entry1 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.10",
                                "to": "2.2.2.20",
                                "enable": True,
                                "lease_time": 1,
                                "default_gateway": "2.2.2.168",
                                "netmask": "255.255.255.0",
                            }
                        ]
                    }
                }
            }
        }
        ret1 = dhcp_obj.add_dhcp_server_scope_dynamic( **dynamic_entry1 )
        Assertion.assert_equal(ret1, True, "ERR: Add dynamic entries failed")     

    def test_02_verify_client_can_get_correct_lease(self):
        flag = 0
        os.system("ifconfig eth1 0.0.0.0")
        os.system("killall dhclient")
        output = os.popen("timeout 20 dhclient -v eth1 2>&1", 'r', 10).read()
        logger.info(output)
        m = re.search(r'bound to (2\.2\.2\.\d+).*renewal in', output, re.I)
        if m:
            logger.info("PC1 eth1 successfully get ip address {}".format(m.group(1)))
            TestDHCPServer_39.pc1_eth1_ip = m.group(1)
            flag = flag + 1
        else:
            logger.info("failed to get ip address for PC1 eth1")
        Assertion.assert_equal(flag, 1, "ERR: Verify multiple clients can get correct leases failed")

    def test_03_verify_dhcp_server_can_send_DHCPACK(self):
        flag = False
        packet_content = ''
        if os.path.exists("/tmp/packet.txt"):
            os.system("rm -rf /tmp/packet.txt") 
        logger.info("will start tshark...")
        os.system('pkill tshark')
        cmd = "tshark -V -i eth1 '((port 67) or (port 68))' &> /tmp/packet.txt &\n";
        rc = os.system(cmd)
        time.sleep(30)
        for i in range(0,6):
            if os.path.getsize('/tmp/packet.txt'):
                break
            else:
                time.sleep(10)
        logger.info(os.path.getsize('/tmp/packet.txt'))
        logger.info("will pkill tshark...")
        rc = rc + os.system('pkill tshark')
        time.sleep(3)
        with open('/tmp/packet.txt', "r", encoding="utf-8") as f:
            packet_content = f.read()
        logger.info(packet_content)
        for packet in re.split('Frame \d+:', packet_content):
            logger.info(packet)
            m = re.search(r'Your \(client\) IP address: (\d+\.\d+\.\d+\.\d+).*DHCP: ACK \(5\)', packet, re.I|re.S)
            if m and m.group(1) == TestDHCPServer_39.pc1_eth1_ip:
                flag = True 
        Assertion.assert_equal(flag, True, "ERR: Verify dhcp server can send DHCPACK failed")

    def test_04_restore_test_environment(self):
        os.system("ifdown eth1; timeout 5 ifup eth1")
        PC2_login.send_command("ifdown eth1; timeout 5 ifup eth1") 
        ret1 = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'dynamic', p1 = '2.2.2.10', p2 = '2.2.2.20' )
        Assertion.assert_equal(ret1, True, "ERR: Restore test environment failed")


class TestDHCPServer_38(Test):
    uuid = "SOSAIOT-TC-55892"
    description= show_testcase_info(TESTPLAN, '38', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '38')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_dynamic_entry_to_X2(self):
        dynamic_entry1 = {
            "dhcp_server": {
                "ipv4": {
                    "scope": {
                        "dynamic": [
                            {
                                "from": "2.2.2.10",
                                "to": "2.2.2.20",
                                "enable": True,
                                "lease_time": 1,
                                "default_gateway": "2.2.2.168",
                                "netmask": "255.255.255.0",
                                "dns": {
                                    "server": {
                                        "inherit": True
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }
        ret1 = dhcp_obj.add_dhcp_server_scope_dynamic( **dynamic_entry1 )
        Assertion.assert_equal(ret1, True, "ERR: Add dynamic entries failed")     

    def test_02_verify_client_can_get_correct_lease(self):
        flag = 0
        os.system("ifconfig eth1 0.0.0.0")
        os.system("killall dhclient")
        output = os.popen("timeout 20 dhclient -v eth1 2>&1", 'r', 10).read()
        logger.info(output)
        m = re.search(r'bound to (2\.2\.2\.\d+).*renewal in', output, re.I)
        if m:
            logger.info("PC1 eth1 successfully get ip address {}".format(m.group(1)))
            TestDHCPServer_39.pc1_eth1_ip = m.group(1)
            flag = flag + 1
        else:
            logger.info("failed to get ip address for PC1 eth1")
        Assertion.assert_equal(flag, 1, "ERR: Verify multiple clients can get correct leases failed")

    def test_03_verify_DNS_info_pass_from_the_WAN(self):
        flag = False
        dns_content = ''
        dns_content = os.popen('cat /etc/resolv.conf | grep nameserver').read()
        logger.info(dns_content)
        if dns_content.count('nameserver') == 2 and  X1_DNS1 in dns_content and X1_DNS2 in dns_content:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify DNS info pass from the WAN failed")

    def test_04_restore_test_environment(self):
        os.system("ifdown eth1; timeout 5 ifup eth1")
        ret1 = dhcp_obj.delete_dhcp_server_scope_v4( scope = 'dynamic', p1 = '2.2.2.10', p2 = '2.2.2.20' )
        Assertion.assert_equal(ret1, True, "ERR: Restore test environment failed")
