from definition.init_param import *


class Test_01_IPv6_ISATAP_Tunnel_Interface_tc_12(Test):
    uuid = "SOSAIOT-TC-56599"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},            
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Address Objects')
        logger.info(output)
        if re.search(r"ISATAP IPv6 Primary Dynamic Address", str(output), re.S|re.I|re.M) and \
            re.search(r"ISATAP IPv6 Primary Dynamic Address Subnet", str(output), re.S|re.I|re.M)  :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in address object Failed!")

    def test_04_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_05_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_02_IPv6_ISATAP_Tunnel_Interface_tc_13(Test):
    uuid = "SOSAIOT-TC-56600"
    description= show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X0"},
            'prefix': {"name": "testisatap"},  
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_snmp': True,          
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_verify_list_access_rule(self):
        logger.info('verify list in access rule...')
        flag = False
        output = systemObj.get_tsr_part2(func = 'Blade_1_ACCESS_RULES')
        logger.info(output)
        if re.search(r"DMZ -> DMZ Allow Service Any -> HTTP Management \(Enabled\)", str(output), re.S|re.I|re.M) and \
             re.search(r"DMZ -> DMZ Allow Service Any -> SNMP \(Enabled\)", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in access rule Failed!")

    def test_04_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_05_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_03_IPv6_ISATAP_Tunnel_Interface_tc_14(Test):
    uuid = "SOSAIOT-TC-56601"
    description= show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},            
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Routing')
        logger.info(output)
        if re.search(r"2002::/64\s+Any\s+N/A\s+Any\s+::\s+ISATAP1", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in address object Failed!")

    def test_04_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_05_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_04_IPv6_ISATAP_Tunnel_Interface_tc_15(Test):
    uuid = "SOSAIOT-TC-56602"
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},            
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    @repeat_method(3)
    def test_03_verify_interface_list(self):
        logger.info('verify interface list...')
        flag = False
        sleep(10)
        output = systemObj.get_tsr_interface_part(lab1 = 'ISATAP1')
        logger.info(output)
        if re.search(r"{}".format(tunnel_ipv6), str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify interface list Failed!")

    def test_04_config_interface_X2(self):
        logger.info('config interface X2...')
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': x2_ip_15,
            'netmask': '255.255.255.0',
          
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_05_verify_interface_list(self):
        logger.info('verify interface list...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Interfaces')
        logger.info(output)
        if re.search(r"{}".format(tunnel_ipv6_2), str(output), re.S|re.I|re.M) or \
            re.search(r"2002::200:5efe:202:2.2.2.9", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify interface list Failed!")

    def test_06_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_07_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')

    def test_08_config_interface_x2(self):
        logger.info("config x2 interface... ")
        x2 = {
            'if': 'X2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.0.0',
          
        }
        rc = interface_obj.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")


class Test_05_IPv6_ISATAP_Tunnel_Interface_tc_20(Test):
    uuid = "SOSAIOT-TC-56603"
    description= show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},  
            'mgmt_https': True,
            'mgmt_ping': True,
            'mgmt_snmp': True,             
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_04_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Routing')
        logger.info(output)
        if not re.search(r"2002::/64\s+Any\s+N/A\s+Any\s+::\s+ISATAP1", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in address object Failed!")
    
    def test_05_verify_list_access_rule(self):
        logger.info('verify list in access rule...')
        flag = False
        output = systemObj.get_tsr_part2(func = 'Blade_1_ACCESS_RULES')
        logger.info(output)
        if not re.search(r"DMZ -> DMZ Allow Service Any -> HTTP Management \(Enabled\)", str(output), re.S|re.I|re.M) and \
            not re.search(r"DMZ -> DMZ Allow Service Any -> SNMP \(Enabled\)", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in access rule Failed!")

    def test_06_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Address Objects')
        logger.info(output)
        if not re.search(r"ISATAP IPv6 Primary Dynamic Address", str(output), re.S|re.I|re.M) and \
            not re.search(r"ISATAP IPv6 Primary Dynamic Address Subnet", str(output), re.S|re.I|re.M)  :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify list in address object Failed!")

    def test_07_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_06_IPv6_ISATAP_Tunnel_Interface_tc_25(Test):
    uuid = "SOSAIOT-TC-56604"
    description= show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '3003::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},  
            'mgmt_ping': True          
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def killprocess(self):
        cmd = 'pkill isatapd'
        os.system(cmd)
        pc2_ssh.send_command(cmd)

    @repeat_method(3)
    def test_03_config_pc1_site_add_route(self):
        logger.info('config pc1 site add route')
        flag = False
        t1 = threading.Thread(target=self.killprocess, name='killprocess')
        t1.start()
        cmd1 = 'isatapd -d {} &'.format(Parameter.X2_IP)
        cmd2 = 'ip -6 r'
        logger.info('run cmd in pc1:{}'.format(cmd1))
        local_host.send_command(cmd1)
        sleep(10)
        output = local_host.send_command(cmd2)
        logger.info(output)
        t1.join()
        if re.search(r"3003::", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config pc1 site add route Failed!")

    @repeat_method(3)
    def test_04_config_pc2_site_and_test_ping(self):
        logger.info('config pc2 site and test ping...')
        flag = False
        t1 = threading.Thread(target=self.killprocess, name='killprocess')
        t1.start()
        cmd1 = 'service network restart'
        cmd2 = 'isatapd -d {} &'.format(Parameter.X2_IP)
        cmd3 = 'ping6 {} -c 5'.format(tunnel_ipv6_3)
        logger.info('run cmd in pc1:{}'.format(cmd1))
        local_host.send_command(cmd1)
        local_host.send_command(cmd2)
        pc2_ssh.send_command(cmd2)
        sleep(3)
        output = pc2_ssh.send_command(cmd3)
        logger.info(output)
        
        t1.join()
        if not re.search(r"100% packet loss", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config pc2 site and test ping Failed!")

    def test_05_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_06_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_07_IPv6_ISATAP_Tunnel_Interface_tc_27(Test):
    uuid = "SOSAIOT-TC-56605"
    description= show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '3003::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},  
            'mgmt_ping': True          
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def killprocess(self):
        cmd = 'pkill isatapd'
        os.system(cmd)

    @repeat_method(3)
    def test_03_config_pc1_site_add_route(self):
        logger.info('config pc1 site add route')
        flag = False
        t1 = threading.Thread(target=self.killprocess, name='killprocess')
        t1.start()
        cmd1 = 'isatapd -d {} &'.format(Parameter.X2_IP)
        cmd2 = 'ip -6 r'
        logger.info('run cmd in pc1:{}'.format(cmd1))
        local_host.send_command(cmd1)
       
        cmds = (
            'ip -6 r del default',
            'ip -6 r add default via 3003::200:5efe:{}'.format(Parameter.X2_IP),
            'ip -6 route add 2004:c03:1a8::/64 via 3003::200:5efe:{}'.format(Parameter.X2_IP)

        )
        for cmd in cmds:
            local_host.send_command(cmd)
        
        sleep(15)
        output = local_host.send_command(cmd2)
        logger.info(output)
        
        t1.join()
        if re.search(r"3003::", str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config pc1 site add route Failed!")

    def test_04_add_NAT_policy(self):
        logger.info('add NAT policy...')
        nat = {
            "nat_policies": [
                {
                    "ipv6": {
                        "name": "isatap1",
                        "reflexive": False,
                        "source_port_remap": True,
                        "inbound": "any",
                        "outbound": "X1",
                        "comment": "",
                        "enable": True,
                        "translated_destination": {
                            "original": True
                        },
                        "translated_source": {
                            "name": "X1 IPv6 Primary Static Address Subnet"
                        },
                        "translated_service": {
                            "original": True
                        },
                        "source": {
                            "name": "ISATAP1 IPv6 Primary Static Address Subnet"
                        },
                        "destination": {
                            "any": True
                        },
                        "service": {
                            "any": True
                        },
                        "priority": {
                            "auto": True
                        },
                        "ticket": {
                            "tag1": "",
                            "tag2": "",
                            "tag3": ""
                        }
                    }
                }
            ]
        }
        rc = natObj.add_nat_policy(**nat)
        Assertion.assert_equal(rc, True, "ERR: add NAT policy Failed!")

    @repeat_method(3)
    def test_05_verify_to_remote_host(self):
        logger.info('verify to remote host...')
        flag = False
        sleep(10)
        packetObj.clear_packets()
        packetObj.start_capture()
        cmd = 'ping6 -c 5 {}'.format(pc3_ipv6_ip)
        output1 = local_host.send_command(cmd)
        logger.info(output1)
        sleep(5)
        packetObj.stop_capture()
        packetObj.export_captured_packets_text_file()
        output2 = local_host.send_command('cat /tmp/packetcaptute')
        logger.info(output2)
        if not re.search(r"100% packet loss", str(output1), re.S|re.I|re.M) and \
            re.search(r"IP Type:\s*6OVER4\(0x29\),\s*Src=\[2\.2\.2\.6\],\s*Dst=\[2\.2\.2\.7\]", str(output2), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:verify to remote host Failed!")

    def test_06_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_07_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')



class Test_08_IPv6_ISATAP_Tunnel_Interface_tc_31(Test):
    uuid = "SOSAIOT-TC-56606"
    description= show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '2002::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},  
            'mgmt_ping': True          
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_export_preferences_file(self):
        logger.info('export preferences file...')
        rc = settingObj.export_setting_exp()
        Assertion.assert_equal(rc, True, "ERR: export preferences file failed")

    def test_04_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_05_import_preferences_file_to_fw(self):
        logger.info('import preferences file to fw...')
        rc = settingObj.import_setting_exp(filepath = '/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: import preferences file to fw failed")

    def test_06_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Interfaces')
        logger.info(output)
        if re.search(r"{}".format(tunnel_ipv6), str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify interface list Failed!")

    def test_07_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_08_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')


class Test_09_IPv6_ISATAP_Tunnel_Interface_tc_33(Test):
    uuid = "SOSAIOT-TC-56607"
    description= show_testcase_info(Parameter.TESTPLAN, '33', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object_ipv6(self):
        logger.info('add address object ipv6...')
        ao_param ={
            "object_type": "network",
            "name": "testisatap",
            "zone": "DMZ",
            "subnet": '3003::2',
            'mask': '64'
        }
        rc = addrObj.config_ipv6_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: add address object ipv6 failed')

    def test_02_add_isatap_ipv6_tunnel_interface(self):
        logger.info('add isatap ipv6 tunnel interface...')
        ti = {
            'name':'ISATAP1',
            "zone": "DMZ",
            "type": "isatap",
            'bound_to': { "interface": "X2"},
            'prefix': {"name": "testisatap"},  
            'mgmt_ping': True          
        }
        rc = interface_ipv6_obj.add_tunnel_interface(**ti)
        Assertion.assert_equal(rc, True, 'ERR:add isatap ipv6 tunnel interface failed')

    def test_03_reboot_fw(self):
        logger.info('reboot fw...')
        rc = settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, 'ERR: reboot fw failed')

    def test_04_verify_list_in_address_object(self):
        logger.info('verify list in address object...')
        flag = False
        output = systemObj.get_tsr_part(func = 'Network', lab1 = 'Interfaces')
        logger.info(output)
        if re.search(r"3003::", str(output), re.S|re.I|re.M) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify interface list Failed!")

    def test_05_delete_isatap_ipv6_tunnel_interface(self):
        logger.info('delete isatap ipv6 tunnel interface...')
        rc = interface_ipv6_obj.delete_tunnel_interface(name = 'ISATAP1')
        Assertion.assert_equal(rc, True, 'ERR: delete isatap ipv6 tunnel interface failed')

    def test_06_delete_address_object_ipv6(self):
        logger.info('delete address object ipv6...')
        ao_param = {
            'ip_type': 'ipv6',
            'name': 'testisatap',
        }
        rc = addrObj.del_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: delete address object ipv6 failed')
