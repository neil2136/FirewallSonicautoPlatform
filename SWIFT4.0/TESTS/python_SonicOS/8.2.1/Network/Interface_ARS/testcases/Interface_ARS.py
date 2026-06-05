from definition.init_param import *


class Test_01_Interface_ARS_tc_01(Test):
    uuid = "SOSAIOT-TC-56164"
    description= show_testcase_info(Parameter.TESTPLAN, '1713727', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713727')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_X1_ARS(self):
        logger.info('enable interface X1 ARS...')
        flag = False
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': True,
        }
        rc = interface_obj.config_interface(**x1)
        output = interface_obj.get_interface_status('X1')
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable interface X1 ARS failed")

    def test_02_disable_X1_ARS(self):
        logger.info('disable interface X1 ARS...')
        flag = False
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': False,
        }
        rc = interface_obj.config_interface(**x1)
        output = interface_obj.get_interface_status('X1')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: disable interface X1 ARS failed")


class Test_02_Interface_ARS_tc_03(Test):
    uuid = "SOSAIOT-TC-56165"
    description= show_testcase_info(Parameter.TESTPLAN, '1713729', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713729')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_X2_ARS(self):
        logger.info('enable interface X2 ARS...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X2_GW,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR:enable interface X2 ARS failed")

    def test_02_download_TSR(self):
        logger.info('download TSR file...')
        rc = systemObj.download_tsr()
        file_size = 0
        if os.path.exists('/tmp/techSupport'):
            file_size = os.path.getsize("/tmp/techSupport")
            logger.info("tsr file size is " + str(file_size))
            if file_size:
                pass
            else:
                Assertion.assert_equal(False, True, "ERR: Download tsr failed")
        else:
            Assertion.assert_equal(False, True, "ERR: Download tsr failed")
            
    def test_03_verify_X2_ARS_status_with_TSR(self):
        logger.info('verify interface X2 ARS status...')
        flag = False
        output = systemObj.get_tsr_interface_part(lab1 = 'X2', lab2 = 'X3')
        logger.info(output)
        string = r'Enable Asymmetric Route Support\s*\W+Yes'
        if re.search(string, str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:verify interface X2 ARS status failed")


class Test_03_Interface_ARS_tc_06(Test):
    uuid = "SOSAIOT-TC-56173"
    description= show_testcase_info(Parameter.TESTPLAN, '1768196', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1768196')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_X3_X4_X5_with_ARS(self):
        logger.info('config interface X2 X3 X4 X5 with ARS...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'asymmetric_route': True,
        }
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'asymmetric_route': True,
        }
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'asymmetric_route': True,
        }
        x5 = {
            'if': 'X5',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'asymmetric_route': True,
        }
        rc_x2 = interface_obj.config_interface(**x2)
        output_x2 = interface_obj.get_interface_status('X2')
        rc_x3 = interface_obj.config_interface(**x3)
        output_x3 = interface_obj.get_interface_status('X3')
        rc_x4 = interface_obj.config_interface(**x4)
        output_x4 = interface_obj.get_interface_status('X4')
        rc_x5 = interface_obj.config_interface(**x5)
        output_x5 = interface_obj.get_interface_status('X5')
        
        if re.search(r'asymmetric_route\W+True', str(output_x2), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x3), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x4), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x5), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:enable interface X2 ARS failed")

    def test_02_add_address_obj(self):
        logger.info('add address object...')
        ao_1 = {
            "object_type": "host",
            "name": Client_PC_IP,
            "zone": "LAN",
            "value": Client_PC_IP,
        }
        ao_2 = {
            "object_type": "host",
            "name": Server_PC_IP,
            "zone": "LAN",
            "value": Server_PC_IP,
        }
        ao_3 = {
            "object_type": "host",
            "name": PC4_ETH1_IP,
            "zone": "LAN",
            "value": PC4_ETH1_IP,
        }
        ao_4 = {
            "object_type": "host",
            "name": PC3_ETH2_IP,
            "zone": "LAN",
            "value": PC3_ETH2_IP,
        }

        rc = addrObj.config_addressobject(**ao_1)
        rc &= addrObj.config_addressobject(**ao_2)
        rc &= addrObj.config_addressobject(**ao_3)
        rc &= addrObj.config_addressobject(**ao_4)
        Assertion.assert_equal(rc, True, "ERR: add address object  failed")

    def test_03_add_route_policy(self):
        logger.info('add route policy...')
        route_1 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "SERVER_PC_IP",
                        "comment": "",
                        "interface": "X2",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": PC4_ETH1_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Client_PC_IP,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        route_2 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "CLIENT_PC_IP",
                        "comment": "",
                        "interface": "X5",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": PC3_ETH2_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Server_PC_IP,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route_1)
        rc &= routeObj.add_route_policy(**route_2)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")


    def test_04_start_ping_traffic_from_pc1_to_pc2(self):
        logger.info('start ping traffic from pc1 to pc2...')
        flag = False
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if not re.search(r'100% packet loss', str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start ping traffic from pc1 to pc2 failed")

    def test_05_disable_ARS_on_x2_x3_x4_x5(self):
        logger.info('disable ARC on interface X2 X3 X4 X5...')
        logger.info('config interface X2 X3 X4 X5 with ARS...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'asymmetric_route': False,
        }
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'asymmetric_route': False,
        }
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'asymmetric_route': False,
        }
        x5 = {
            'if': 'X5',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'asymmetric_route': False,
        }
        rc_x2 = interface_obj.config_interface(**x2)
        output_x2 = interface_obj.get_interface_status('X2')
        rc_x3 = interface_obj.config_interface(**x3)
        output_x3 = interface_obj.get_interface_status('X3')
        rc_x4 = interface_obj.config_interface(**x4)
        output_x4 = interface_obj.get_interface_status('X4')
        rc_x5 = interface_obj.config_interface(**x5)
        output_x5 = interface_obj.get_interface_status('X5')
        
        if  re.search(r'asymmetric_route\W+False', str(output_x2), re.S|re.I) and \
            re.search(r'asymmetric_route\W+False', str(output_x3), re.S|re.I) and \
            re.search(r'asymmetric_route\W+False', str(output_x4), re.S|re.I) and \
            re.search(r'asymmetric_route\W+False', str(output_x5), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:disable interface X2 ARS failed")

    def test_06_start_ping_traffic_from_pc1_to_pc2(self):
        logger.info('start ping traffic from pc1 to pc2...')
        flag = False
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if re.search(r'100% packet loss', str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start ping traffic from pc1 to pc2 failed")


class Test_04_Interface_ARS_tc_12(Test):
    uuid = "SOSAIOT-TC-56167"
    description= show_testcase_info(Parameter.TESTPLAN, '1713738', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713738')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_X2_X3_X4_X5_with_ARS(self):
        logger.info('config interface X2 X3 X4 X5 with ARS...')
        flag = False
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'asymmetric_route': True,
        }
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'asymmetric_route': True,
        }
        x4 = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'asymmetric_route': True,
        }
        x5 = {
            'if': 'X5',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X5_IP,
            'asymmetric_route': True,
        }
        rc_x2 = interface_obj.config_interface(**x2)
        output_x2 = interface_obj.get_interface_status('X2')
        rc_x3 = interface_obj.config_interface(**x3)
        output_x3 = interface_obj.get_interface_status('X3')
        rc_x4 = interface_obj.config_interface(**x4)
        output_x4 = interface_obj.get_interface_status('X4')
        rc_x5 = interface_obj.config_interface(**x5)
        output_x5 = interface_obj.get_interface_status('X5')
        
        if re.search(r'asymmetric_route\W+True', str(output_x2), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x3), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x4), re.S|re.I) and \
            re.search(r'asymmetric_route\W+True', str(output_x5), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable interface X2 ARS failed")

    def test_02_config_PC2(self):
        logger.info('config PC2...')
        flag = False
        cmds = (
                "echo 'AUTOMATION' > /var/ftp/pub/FTP_Test_File",
                "echo 'AUTOMATION' > /tmp/index.html",
                "service vsftpd restart",
                "service httpd restart",
        )
        for cmd in cmds:
            logger.info('run cmd in PC2:{}'.format(cmd))
            pc2_ssh.send_command(cmd)

        cmd_check = 'service httpd status'
        logger.info('check:{}'.format(cmd_check))
        output = pc2_ssh.send_command(cmd_check)
        if re.search(r'httpd.*is running', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config PC2 failed")

    def test_03_http_connection_from_pc1_to_pc2(self):
        logger.info('http connection from pc1 to pc2...')
        flag = False
        cmd = 'perl -MLWP::Simple -e \'getprint "http://{}"\''.format(Server_PC_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if re.search(r'AUTOMATION', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: HTTP connection from pc1 to pc2 failed")


class Test_05_Interface_ARS_tc_13(Test):
    uuid = "SOSAIOT-TC-56168"
    description= show_testcase_info(Parameter.TESTPLAN, '1713739', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713739')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao = {
            "object_type": "host",
            "name": PC4_ETH2_IP,
            "zone": "LAN",
            "value": PC4_ETH2_IP,
        }

        rc = addrObj.config_addressobject(**ao)
        Assertion.assert_equal(rc, True, "ERR: add address object failed")

    def test_02_add_route_policy(self):
        logger.info('add route policy...')
        route = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "CLIENT_PC_IP",
                        "comment": "",
                        "interface": "X3",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": PC4_ETH2_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Server_PC_IP,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.add_route_policy(**route)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")

    def test_03_start_ping_traffic_from_pc1_to_pc2(self):
        logger.info('start ping traffic from pc1 to pc2...')
        flag = False
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if not re.search(r'100% packet loss', str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start ping traffic from pc1 to pc2 failed")


class Test_06_Interface_ARS_tc_14(Test):
    uuid = "SOSAIOT-TC-56169"
    description= show_testcase_info(Parameter.TESTPLAN, '1713740', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713740')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_address_object(self):
        logger.info('add address object...')
        ao = {
            "object_type": "host",
            "name": PC3_ETH1_IP,
            "zone": "LAN",
            "value": PC3_ETH1_IP,
        }

        rc = addrObj.config_addressobject(**ao)
        Assertion.assert_equal(rc, True, "ERR: add address object failed")

    def test_02_edit_route_policy(self):
        logger.info('edit route policy...')
        route_1 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "SERVER_PC_IP",
                        "comment": "",
                        "interface": "X4",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": PC3_ETH1_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Server_PC_IP,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        route_2 = {
            "route_policies": [
                {
                    "ipv4": {
                        "name": "CLIENT_PC_IP",
                        "comment": "",
                        "interface": "X2",
                        "metric": 1,
                        "service": {
                            "any": True
                        },
                        "gateway": {
                            "name": PC4_ETH1_IP
                        },
                        "source": {
                            "any": True
                        },
                        "destination": {
                            "name": Client_PC_IP,
                        },
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "distance": {
                            "auto": True
                        },
                        "tos": "0x00",
                        "mask": "0x00",
                        "type": "standard"
                    }
                }
            ]
        }
        rc = routeObj.del_route_policy_by_name('SERVER_PC_IP')
        rc &= routeObj.del_route_policy_by_name('CLIENT_PC_IP')
        rc &= routeObj.add_route_policy(**route_1)
        rc &= routeObj.add_route_policy(**route_2)
        Assertion.assert_equal(rc, True, "ERR: edit route policy failed")

    def test_03_start_ping_traffic_from_pc1_to_pc2(self):
        logger.info('start ping traffic from pc1 to pc2...')
        flag = False
        cmd = 'ping {} -c 10'.format(Server_PC_IP)
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if not re.search(r'100% packet loss', str(output), re.S|re.I|re.M):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start ping traffic from pc1 to pc2 failed")


class Test_07_Interface_ARS_tc_18(Test):
    uuid = "SOSAIOT-TC-56170"
    description= show_testcase_info(Parameter.TESTPLAN, '1713744', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713744')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_X1_ARS(self):
        logger.info('enable interface X1 ARS...')
        flag = False
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'asymmetric_route': True,
        }
        rc = interface_obj.config_interface(**x1)
        output = interface_obj.get_interface_status('X1')
        logger.info(output)
        if re.search(r'asymmetric_route\W+True', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: enable interface X1 ARS failed")

    def test_02_reboot_dut(self):
        logger.info('reboot DUT...')
        rc = settingObj.boot_fw(mode = 1)
        Assertion.assert_equal(rc, True, "ERR: reboot DUT failed")

    def test_03_check_interface_ARS(self):
        logger.info('check DUT interface ARS status...')
        output_x1 = interface_obj.get_interface_status('X1')
        flag = False
        if re.search(r'asymmetric_route\W+True', str(output_x1), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable interface X2 ARS failed")


class Test_08_Interface_ARS_tc_19(Test):
    uuid = "SOSAIOT-TC-56171"
    description= show_testcase_info(Parameter.TESTPLAN, '1713745', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713745')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_FTP_get_file_from_remote_PC(self):
        logger.info('FTP get file from remote PC...')
        cmd = 'rm -rf /tmp/ftp.txt'
        pc2_ssh.send_command(cmd)
        
        cmds = (
                'touch /tmp/ftp.txt',
                "echo '1234567890ewqxdAQWCGERTRTRBFDSKOKP' > /tmp/ftp.txt",
            )
        for cmd in cmds:
            logger.info('run cmd in pc2:{}'.format(cmd))
            pc2_ssh.send_command(cmd)

        flag = False
        ftp_file = '/tmp/ftp.txt'

        cmd_sftp = 'python3 {}'.format(toolPath + '/upload_or_download_file.py download sftp ') + \
                        ftp_file +' root ' + Server_PC_IP+ ' ' + ftp_file + ' password 22'
        logger.info('run cmd in pc1:{}'.format(cmd_sftp))
        local_host.send_command(cmd_sftp)
        
        cmd = 'ls -l /tmp'
        logger.info('run cmd in pc1:{}'.format(cmd))
        output = local_host.send_command(cmd)
        if re.search(r'.*ftp.txt', str(output), re.S|re.I) :
            flag = True
        Assertion.assert_equal(flag, True, "ERR: enable interface X2 ARS failed")


class Test_09_Interface_ARS_tc_21(Test):
    uuid = "SOSAIOT-TC-56172"
    description= show_testcase_info(Parameter.TESTPLAN, '1713747', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1713747')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reboot_dut(self):
        logger.info('reboot DUT...')
        rc = settingObj.boot_fw(mode = 2)
        Assertion.assert_equal(rc, True, "ERR: reboot DUT failed")

    def test_02_config_X1_and_verify_ARS_default(self):
        logger.info('config interface X1 and verify ARS default...')
        flag = False
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x1)
        output = interface_obj.get_interface_status('X1')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: verify interface X1 ARS failed")

    def test_03_config_X2_and_verify_ARS_default(self):
        logger.info('config interface X2 and verify ARS default...')
        flag = False
        x2 = {
           'if': 'X2',
            'zone': 'WLAN',
            'mode': 'static',
            'ip': '8.8.8.8',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.config_interface(**x2)
        output = interface_obj.get_interface_status('X2')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(rc&flag, True, "ERR: verify interface X2 ARS failed")

    def test_04_add_vlan_interface_and_verify_ARS(self):
        logger.info('add vlan interface and verify ARS status...')
        flag = False
        x0_vlan = {
            'if': 'X0',
            'type': 'vlan',
            'vlan_tag': 100,
            'zone': 'LAN',
            'mode': 'static',
            'ip': '100.1.1.100',
            'gateway': '100.1.1.1',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_obj.add_interface(**x0_vlan)
        output = interface_obj.get_vlan_interface_status(name = 'X0', vlan_id = '100')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X0 ARS failed")


    def test_05_add_vpn_policy(self):
        logger.info('add vpn policy...')
        vpn = {
            'type': 'tunnel_interface',  # site-to-site, tunnel_interface
            'name': 'vpn_interface',
            'enable': True,
            'auth_mode': 'shared_secret',  # certificate or shared-secret
            'pri_gate': '101.1.1.101',
            'secret': '123456',  # add local cert  
            'local_ike_type': 'ipv4',   ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
            'peer_ike_type': 'ipv4',  ### arg can be:ipv4, domain_name, email_address, firewall_id, key_id
               
        }
        rc = vpnObj.add_vpn_policy(**vpn)
        Assertion.assert_equal(rc, True, "ERR:add vpn policy failed")


    def test_06_add_interface_vpn_tunnel_and_verify_ARS(self):
        logger.info('add interface vpn tunnel and verify ARS status...')
        flag = False
        vpn_tunnel = {
            'zone': 'VPN',
            'type': 'vpn_tunnel',
            'tunnel_name': 'test_vpn',
            'vpn_policy': 'vpn_interface',
            'ip': '20.20.20.100',
            'netmask': '255.255.255.0',
            'multicast': True,
            'flow_reporting': True,
            'fragment_packets': True,
            'ignore_df_bit': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.add_interface(**vpn_tunnel)
        output = interface_obj.get_tunnel_interface_status(name = 'test_vpn', type = 'vpn')
        logger.info(output)
        if re.search(r'asymmetric_route\W+False', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: verify vlan interface X0 ARS failed")
