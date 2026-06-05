from settings import *
ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
inter_obj = network.InterfaceIPv4Api(fw)
nat_obj = network.NatpolicyApi(fw)
snmp_obj = system.SNMPApi(fw)
pkg_api = system.PacketmonitorApi(fw)


class Test_12_Verify_Unnumbered_Interface(Test):
    uuid = "SOSAIOT-TC-57152"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_12_01_config_X2_ip(self):
        x2_lan_unnumber = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'unnumbered',
            'ip': Parameter.DUT_X2_IP,
            'netmask': '255.255.255.0',
        }
        rc = inter_obj.config_interface(**x2_lan_unnumber)
        Assertion.assert_equal(rc, True, "ERR: Config X2 failed.")

    def test_12_02_config_X1(self):
        x1_pppoe_unnumbered = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_unnumbered': 'X2',
            'pppoe_user': 'root',
            'pppoe_servicename': 'def',
            'pppoe_passwd': 'password',
            }   
        rc = inter_obj.config_interface(**x1_pppoe_unnumbered)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed.")
 
    @repeat_method(5)
    def test_12_03_verify_X1_get_IP(self):
        time.sleep(10)
        x1_dict = inter_obj.get_interface_address(name='X1')
        try:
            ip = x1_dict['ip_address']
        except:
            logger.error('Fail to get X1 ipv6.')
            logger.info(x1_dict)
            ip = ''
        Assertion.assert_regular(ip, Parameter.DUT_X2_IP, f"Error: X1 should obtain IP same with X2.")


class Test_15_Verify_NAT_Policy(Test):
    uuid = "SOSAIOT-TC-57153"
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_15_01_config_X2_ip(self):
        x2_lan_unnumber = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'unnumbered',
            'ip': Parameter.DUT_X2_IP,
            'netmask': '255.255.255.0',
        }
        rc = inter_obj.config_interface(**x2_lan_unnumber)
        Assertion.assert_equal(rc, True, "ERR: Config X2 failed.")

    def test_15_02_config_X1(self):
        x1_pppoe_unnumbered = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_unnumbered': 'X2',
            'pppoe_user': 'root',
            'pppoe_servicename': 'def',
            'pppoe_passwd': 'password',
            }   
        rc = inter_obj.config_interface(**x1_pppoe_unnumbered)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed.")
 
    def test_15_03_Check_NAT_Policy(self):
        rc = nat_obj.get_nat_policy()
        policy = 0
        try:
            for nat in rc['nat_policies']:
                try:
                    if nat['ipv4']['source']['name'] == 'X2 Subnet' and nat['ipv4']['translated_source']['original'] and nat['ipv4']['destination']['any'] and nat['ipv4']['translated_destination']['original']:
                        logger.info('Found nat policy from X2 Subnet to any translate to original to original')
                        policy += 1
                except:
                    pass
                try:
                    if nat['ipv4']['source']['any'] and nat['ipv4']['translated_source']['original'] and nat['ipv4']['destination']['name'] == 'X2 Subnet' and nat['ipv4']['translated_destination']['original']:
                        logger.info('Found nat policy from any to X2 Subnet translate to original to original')            
                        policy += 1
                except:
                    pass
                if policy ==2:
                    break
        except:
            logger.error('Get empty nat policy')
        Assertion.assert_equal(policy, 2, "ERR: two nat policy with unnumber interface subnet 'X2 Subnet' should be auto added.")


class Test_16_Verify_ping_FTP_HTTPS(Test):
    uuid = "SOSAIOT-TC-57154"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_16_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_16_01_config_X2_ip(self):
        x2_lan_unnumber = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'unnumbered',
            'ip': Parameter.DUT_X2_IP,
            'netmask': '255.255.255.0',
        }
        rc = inter_obj.config_interface(**x2_lan_unnumber)
        Assertion.assert_equal(rc, True, "ERR: Config X2 failed.")

    def test_16_02_config_X1(self):
        x1_pppoe_unnumbered = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_unnumbered': 'X2',
            'pppoe_user': 'root',
            'pppoe_servicename': 'def',
            'pppoe_passwd': 'password',
            }   
        rc = inter_obj.config_interface(**x1_pppoe_unnumbered)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed.")
 
    @repeat_method(5)
    def test_16_03_verify_X1_get_IP(self):
        time.sleep(10)
        x1_dict = inter_obj.get_interface_address(name='X1')
        try:
            ip = x1_dict['ip_address']
        except:
            logger.error('Fail to get X1 ipv6.')
            logger.info(x1_dict)
            ip = ''
        Assertion.assert_regular(ip, Parameter.DUT_X2_IP, f"Error: X1 should obtain IP same with X2.")

    def test_16_04_add_route_on_pc2(self):
        pc2 = Host(Parameter.PC2_SERVER)
        pc2.send_command(f'route add {Parameter.PC1_ETH1} gw {Parameter.DUT_X2_IP}')
        rc = pc2.send_command('route -n')
        Assertion.assert_regular(rc, f'{Parameter.PC1_ETH1}.*{Parameter.DUT_X2_IP}', f"Error: add route on pc2 fail.")

    def test_16_05_start_capture(self):
        logger.info('Clear the packet capture.')
        rc = pkg_api.clear_packets()
        logger.info('Start the packet capture.')
        rc = pkg_api.start_capture()
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed.")

    def test_16_06_ping_from_pc1_to_pc2(self):
        rc = trafficGen.ping(Parameter.PC2_ETH1)
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 fail.")

    def test_16_07_verify_packet(self):
        packets = pkg_api.export_captured_packets()
        rc =True
        for packet in re.split('Packet number: \d+\*', packets):
            pattern = f'Src=[{Parameter.DUT_X2_IP}], Dst=[{Parameter.PC2_ETH1}]'
            if re.search(pattern, packet, re.I):
                logger.error('the data flow should not do NAT')
                rc = False
                break
        Assertion.assert_equal(rc, True, "ERR: Packet nat.")
        
    def test_16_08_https_from_pc1_to_pc2(self):
        logger.info('Clear the packet capture.')
        rc = pkg_api.clear_packets()
        import requests
        resp=requests.get(f'https://{Parameter.PC2_ETH1}',verify=False)
        rc = resp.content.decode('utf-8')
        Assertion.assert_regular(rc, f'hello', f"Error:https from pc1 to pc2 fail.")

    def test_16_09_verify_packet(self):
        packets = pkg_api.export_captured_packets()
        rc =True
        for packet in re.split('Packet number: \d+\*', packets):
            pattern = f'Src=[{Parameter.DUT_X2_IP}], Dst=[{Parameter.PC2_ETH1}]'
            if re.search(pattern, packet, re.I):
                logger.error('the data flow should not do NAT')
                rc = False
                break
        Assertion.assert_equal(rc, True, "ERR: Packet nat.")

    def test_16_10_https_from_pc1_to_pc2(self):
        logger.info('Clear the packet capture.')
        rc = pkg_api.clear_packets()
        import requests
        logger.info(f'Access https://{Parameter.PC2_ETH1}')
        resp=requests.get(f'https://{Parameter.PC2_ETH1}',verify=False)
        rc = resp.content.decode('utf-8')
        Assertion.assert_regular(rc, f'hello', f"Error:https from pc1 to pc2 fail.")

    def test_16_11_verify_packet(self):
        packets = pkg_api.export_captured_packets()
        rc =True
        for packet in re.split('Packet number: \d+\*', packets):
            pattern = f'Src=[{Parameter.DUT_X2_IP}], Dst=[{Parameter.PC2_ETH1}]'
            if re.search(pattern, packet, re.I):
                logger.error('the data flow should not do NAT')
                rc = False
                break
        Assertion.assert_equal(rc, True, "ERR: Packet nat.")

    def test_16_12_ftp_from_pc1_to_pc2(self):
        logger.info('Clear the packet capture.')
        rc = pkg_api.clear_packets()
        ftp = trafficGen.MyFtp(Parameter.PC2_ETH1)
        rc = ftp.login()
        Assertion.assert_equal(rc, True, f"Error:ftp from pc1 to pc2 fail.")

    def test_16_13_verify_packet(self):
        packets = pkg_api.export_captured_packets()
        rc =True
        for packet in re.split('Packet number: \d+\*', packets):
            pattern = f'Src=[{Parameter.DUT_X2_IP}], Dst=[{Parameter.PC2_ETH1}]'
            if re.search(pattern, packet, re.I):
                logger.error('the data flow should not do NAT')
                rc = False
                break
        Assertion.assert_equal(rc, True, "ERR: Packet nat.")


class Test_20_Verify_Management(Test):
    uuid = "SOSAIOT-TC-57158"
    description= show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_20_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_20_01_config_X2_ip(self):
        x2_lan_unnumber = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'unnumbered',
            'ip': Parameter.DUT_X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
        }
        rc = inter_obj.config_interface(**x2_lan_unnumber)
        Assertion.assert_equal(rc, True, "ERR: Config X2 failed.")

    def test_20_02_config_X1(self):
        x1_pppoe_unnumbered = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'pppoe',
            'pppoe_unnumbered': 'X2',
            'pppoe_user': 'root',
            'pppoe_servicename': 'def',
            'pppoe_passwd': 'password',
            'mgmt_https': True,
            }   
        rc = inter_obj.config_interface(**x1_pppoe_unnumbered)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed.")
    
    def test_20_03_enable_snmp(self):
        logger.info("Add SNMP config")
        rc = []
        snmp_user_group = "snmpgGroup"
        snmp_user_dict = {
            "user_name": "snmpUser",
            "user_security": "",
            "user_group": snmp_user_group,
        }
        snmp_acc_dict = {
            "access_name": "snmpAcc",
            "access_security": "",
            "access_view": "root",
            "access_group": snmp_user_group,
        }

        rc_gp = snmp_obj.add_snmp_group(name=snmp_user_group)
        logger.info(f"Add SNMP group result = {rc_gp}")
        rc_user = snmp_obj.snmp_user_add(**snmp_user_dict)
        logger.info(f"Add SNMP user result = {rc_user}")
        rc_acc = snmp_obj.snmp_access_add(**snmp_acc_dict)
        logger.info(f"Add SNMP access result = {rc_acc}")

        resp = snmp_obj.show_snmp()
        if resp:
            snmp_v3 = resp["snmp"]
            snmp_v3["snmp3"]["mandatory"] = True
            rc_set = snmp_obj.snmp_base_settings(**snmp_v3)
            rc_enable = snmp_obj.enable_snmp()
            rc = [rc_set, rc_enable]
        logger.info(f"Enable SNMP v3 results = {rc}")
        Assertion.assert_equal(all(rc) and bool(rc), True, "ERR: Enable snmp failed.")

    def test_20_04_check_management(self):
        time.sleep(10)
        x2_ip = Parameter.DUT_X2_IP
        logger.info('Manage DUT via ping')
        rc = trafficGen.ping(x2_ip)
        Assertion.assert_equal(rc, True, "ERR: Manage DUT via ping failed.")
        logger.info('Manage DUT via SSH')
        fw = Firewall(x2_ip, user='admin', password='password', supported_config_mode='cli-ssh')
        rc =fw.do_cli_commands(['show status'])
        Assertion.assert_equal(rc, True, "ERR: Manage DUT via SSH failed.")

        user_name = "snmpUser"
        snmp_cmd = f"snmpwalk -c public -u {user_name} {x2_ip} -l noAuthNoPriv .1.3.6.1.2.1.1.1.0"
        snmp_res = os.popen(snmp_cmd).read()
        # Response example >> SNMPv2-MIB::sysDescr.0 = STRING: SonicWALL TZ 370 (SonicOS 7.1.1-7051-P5654)
        rc = "sonicwall" in snmp_res.lower()
        Assertion.assert_equal(rc, True, "ERR: Check PPPoE unnumbered interface MGMT via snmp from WAN failed",)

        logger.info('Manage DUT via HTTPS')
        fw = Firewall(x2_ip, user='admin', password='password', supported_config_mode='api')
        rc = fw.api_login()
        Assertion.assert_equal(rc, True, "ERR: Manage DUT via HTTPS failed.")
            
