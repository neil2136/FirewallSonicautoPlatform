from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(10)
    def test_02_register_fw(self):
        rc = licenseObj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_GAV_in_SecurityService(self):
        logger.info('config gateway anti virus in Security Service...')
        gav_params = {
            'enable_GAV':True,
            'outbound_ftp': True,
            'inbound_ftp': True
        }
        rc = gavObj.config_gav(**gav_params)
        Assertion.assert_equal(rc, True, "ERR: config GAV in security service failed")

    def test_04_add_match_object(self):
        logger.info('add match object...')
        match_opt = {
            "name": "match_opt",
            "object_type": "file-extension",
            "match_type": "exact",
            "input_representation": "alphanumeric",
            "negative_matching": False,
            "content_entry": [
                {
                    "content_entry": "txt"
                }
            ]
        
        }

        rc = matchObj.config_matchobject(**match_opt)
        Assertion.assert_equal(rc, True, "ERR: add match object failed")

    def test_05_add_app_rule_for_ftp_download_specific_file_extension(self):
        logger.info('add app rule for ftp download specific file extension...')
        apprule_opt = {
            "app_rules": {
                "policy": [
                    {
                        "name": "ftp_file_extension",
                        "enable": True,
                        "type": {
                            "ftp": "client-download"
                        },
                        "source": {
                            "service": {
                                "any": True
                            },
                            "address": {
                                "any": True
                            }
                        },
                        "destination": {
                            "service": {
                                "name": "FTP Control"
                            },
                            "address": {
                                "any": True
                            }
                        },
                        "exclusion": {
                            "address": {},
                            "service": {}
                        },
                        "match_object": {
                            "object": "match_opt"
                        },
                        "action_object": "Reset/Drop",
                        "users": {
                            "included": {
                                "all": True
                            },
                            "excluded": {}
                        },
                        "schedule": {
                            "always_on": True
                        },
                        "flow_reporting": False,
                        "logging": True,
                        "log": {
                            "individual": False,
                            "redundancy": {
                                "global": True
                            }
                        },
                        "connection_side": "client",
                        "direction": {
                            "basic": "both"
                        }
                    }
                ]
            }
        }
        apprule_setting_dict = {
            "enable": True,
            "log_redundancy":{}
        }
        rc = appObj.config_apprule_setting(**apprule_setting_dict)
        rc &= appObj.add_apprule(**apprule_opt) 
        Assertion.assert_equal(rc, True, "ERR: add app rule failed")

    def test_06_add_match_obj_for_icmp(self):
        logger.info('add match obj for icmp...')
        match_opt_dict = {
            'name': 'icmp_match',
            'object_type': 'ips-signature-category-list',
            'ips': {"category": [{"id": 10}]}
        }
        res = matchObj.config_matchobject(**match_opt_dict)
        Assertion.assert_equal(res, True, "ERR:config icmp match object failed")

    def test_07_add_app_rule_for_icmp(self):
        logger.info('add app rule for icmp...')
        apprule_dict = {
            "app_rules": {
                "policy": [
                    {
                        "action_object": "Reset/Drop",
                        "address": {
                            "any": True
                        },
                        "enable": True,
                        "exclusion": {
                            "address": {},
                            "service": {}
                        },
                        "flow_reporting": False,
                        "ips_message_format": False,
                        "log": {
                            "individual": False,
                            "redundancy": {
                                "global": True
                            }
                        },
                        "logging": True,
                        "match_object": {
                            "object": 'icmp_match'
                        },
                        "name": 'icmp_app',
                        "schedule": {
                            "always_on": True
                        },
                        "type": {
                            "ips": True
                        },
                        "users": {
                            "excluded": {},
                            "included": {
                                "all": True
                            }
                        },
                        "zone": {
                            "any": True
                        }
                    }
                ]
            }
        }
        rc = appObj.add_apprule(**apprule_dict) 
        Assertion.assert_equal(rc, True, "ERR: add app rule failed")

    def test_08_add_customer_zone(self):
        logger.info('add customer zone...')
        zone_opt1 = {
            "zones": [
                {
                    "name": "trustZone",
                    "security_type": "trusted",
                    "interface_trust": False,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_to_lower": True,
                        "allow_from_higher": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "enable": False,
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            }
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {
                                "value": 15,
                                "unit": "minutes"
                            },
                            "auto_accept": False
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "header": {},
                            "footer": {}
                        }
                    }
                }
            ]
        }
        zone_opt2 = {
            "zones": [
                {
                    "name": "publicZone",
                    "security_type": "public",
                    "interface_trust": False,
                    "auto_generate_access_rules": {
                        "allow_from_to_equal": True,
                        "allow_to_lower": True,
                        "allow_from_higher": True,
                        "deny_from_lower": True
                    },
                    "guest_services": {
                        "enable": False,
                        "inter_guest": False,
                        "post_auth": "",
                        "bypass_guest_auth": {},
                        "smtp_redirect": {},
                        "deny_networks": {},
                        "pass_networks": {},
                        "max_guests": 10,
                        "external_auth": {
                            "enable": False,
                            "client_redirect": "https",
                            "web_server": {
                                "timeout": 15
                            },
                            "auth_pages": {
                                "web_server_1": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                },
                                "web_server_2": {
                                    "expiration": "",
                                    "login": "",
                                    "max_sessions": "",
                                    "timeout": "",
                                    "traffic_exceeded": ""
                                }
                            },
                            "web_content": {
                                "redirect": {
                                    "use_default": True
                                },
                                "server_down": {
                                    "use_default": True
                                }
                            },
                            "social_network": {
                                "enable": False,
                                "facebook": False,
                                "google": False,
                                "twitter": False
                            }
                        },
                        "captive_portal_authentication": {
                            "enable": False,
                            "internal_url": "",
                            "external_url": "",
                            "welcome_url_source": "from-radius",
                            "welcome_url": "",
                            "session_timeout_source": "from-radius",
                            "session_timeout": {},
                            "idle_timeout_source": "from-radius",
                            "idle_timeout": {},
                            "method": "chap"
                        },
                        "policy_page_non_authentication": {
                            "enable": False,
                            "idle_timeout": {
                                "value": 15,
                                "unit": "minutes"
                            },
                            "auto_accept": False
                        },
                        "custom_auth_page": {
                            "enable": False,
                            "header": {},
                            "footer": {}
                        }
                    }
                }
            ]
        }
        rc = zoneObj.add_zone_object(**zone_opt1)
        rc &= zoneObj.add_zone_object(**zone_opt2)
        Assertion.assert_equal(rc, True, "ERR: add zone object failed")


class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = 'test download and decode viruses on server'
    goto_teardown = True


    def test_01_00_upload_viruses_to_pc4(self):
        viruses = (
                '1.cab.bin.base.base',
                'klez.h.bin.base.base',
                'normal.txt.base.base',
                'test.txt.base.base',
                'packed_upx.exe.base.base'
                )
        flag = False
        logger.info('create {} to store downloaded virus files..'.format(Parameter.TMP_PATH))
        pc4_ssh.send_command('mkdir {}'.format(Parameter.TMP_PATH))
        
        output = pc4_ssh.send_command('ping -c 5 {}'.format(Parameter.WEB_SERVER))
        pattern = r". packets transmitted, . received, 0% packet loss"
        match = re.search(pattern, output, re.S)
        if match:
            logger.info("check network status,normally")
            flag = True 
        else:
            logger.error('the network has down!')

        logger.info('upload decode_viruses.py to pc4...')
        cmd = 'python3 {}'.format(toolPath + '/upload_or_download_file.py upload scp ') + '{}/decode_viruses.py '.format(toolPath) +' root ' + Parameter.PC4_ETH1 + \
             ' /home '  + ' password 22'
        logger.info('run cmd on PC1:{}'.format(cmd))
        local_host.send_command(cmd)
        # download from web server
        logger.info('Download virus files from {}, and decode them'.format(Parameter.WEB_SERVER))
        for virus in viruses: 
            cmd = 'wget -O {}/{} http://{}/DPISSL/POP3S/{}'.format(Parameter.TMP_PATH, virus, Parameter.WEB_SERVER, virus)
            pc4_ssh.send_command(cmd)
        # decode viruses files
        logger.info('Already download viruses file from server, start to decode..')
        cmd = 'python {} {}'.format( '/home/decode_viruses.py', Parameter.TMP_PATH)
        pc4_ssh.send_command(cmd)
        logger.info('Check if the virus is decompressed...')
        cmd_check = 'ls -l {}'.format(Parameter.TMP_PATH)
        output_check = pc4_ssh.send_command(cmd_check)
        logger.info(output_check)
        if re.search(r'klez.h.bin', str(output_check), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: download and decode viruses on pc4 failed')

    def test_01_01_config_static_route_on_pc3(self):
        logger.info('config static route on pc3...')
        flag = False
        cmds = (
            "echo 'any net 172.16.4.0/24 dev eth0' > /etc/sysconfig/static-routes",
            "service network restart",
            "echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse",
            "echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle"
        )
        for cmd in cmds:
            logger.info('run cmd on pc3:{}'.format(cmd))
            pc3_ssh.send_command(cmd)

        output = pc3_ssh.send_command('route -n')
        if re.search(r'172.16.4.0.*eth0', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: config static route on pc3 failed')

    def test_01_02_config_static_route_on_pc4(self):
        logger.info('config static route on pc4...')
        flag = False
        cmds = (
            "echo 'any net 172.16.3.0/24 dev eth0' > /etc/sysconfig/static-routes",
            "service network restart",
            "echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse",
            "echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle"
        )
        for cmd in cmds:
            logger.info('run cmd on pc3:{}'.format(cmd))
            pc4_ssh.send_command(cmd)

        output = pc4_ssh.send_command('route -n')
        if re.search(r'172.16.3.0.*eth0', str(output), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: config static route on pc4 failed')
        
    def test_01_03_initialize_environment(self):
        config_ftp_cmds =(
                'sed -i /root/d /etc/vsftpd/ftpusers',
                'sed -i /root/d /etc/vsftpd/user_list',
                'systemctl restart vsftpd ',
        )
        for cmd in config_ftp_cmds:
            logger.info('run cmd on pc server:{}'.format(cmd))
            pc3_ssh.send_command(cmd)
            pc4_ssh.send_command(cmd)

        output1 = pc3_ssh.send_command('systemctl status vsftpd')
        output2 = pc4_ssh.send_command('systemctl status vsftpd')

        if re.search(r"active \(running", str(output1), re.S|re.I) and \
            re.search(r"active \(running", str(output2), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: setup http and ftp server failed")




class TestSetup_Https_Server(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_02_00_initialize_environment(self):
        logger.info('[ SET UP 1/4 ] on PC4, copy html files...')
        logger.info('run cmd: cp -r {}/* /var/www/https')
        pc4_ssh.send_command('mkdir -p /var/www/https')
        pc4_ssh.send_command('cp -r {}/* /var/www/https'.format(WWW_PATH))

        logger.info("[ SET UP 2/4 ] on PC4, install 'mod_ssl' for Apache to get SSL support...")
        pc4_ssh.send_command('yum -y install mod_ssl openssl')

        for i in range(2):
            logger.info('Modify the ssl.conf fro the {} time!'.format(i))
            pc4_ssh.send_command('rm -f /etc/httpd/conf.d/ssl.conf')
            pc4_ssh.send_command('\cp -fr {}/ssl.conf /etc/httpd/conf.d/'.format(configPath))
            output = pc4_ssh.send_command('grep /www/https /etc/httpd/conf.d/ssl.conf')
            if re.search(r'/www/https', str(output), re.S|re.I):
                logger.info('Overwrite ssl.conf successfully in the {} times...'.format(i))
            else:
                logger.info('Fail to modify ssl.conf in the {} times...'.format(i))
        logger.info('upload httpd.conf to pc4...')
        cmd_httpd = 'python3 {}'.format(toolPath+'/upload_or_download_file.py upload scp ')  + '{}/httpd.conf'.format(resPath) +' root ' + PC4_ETH1_IP + \
            ' /etc/httpd/conf/' + ' password 22'
        logger.info('run cmd:{}'.format(cmd_httpd))
        local_host.send_command(cmd_httpd)

        logger.info('upload index.html to pc4...')
        cmd_html = 'python3 {}'.format(toolPath+'/upload_or_download_file.py upload scp ')  + '{}/index.html'.format(resPath) +' root ' + PC4_ETH1_IP + \
            ' /var/www/https/' + ' password 22'
        logger.info('run cmd:{}'.format(cmd_html))
        local_host.send_command(cmd_html)
        pc4_ssh.send_command('echo "this is http server!" > /var/www/https/index.html')

        logger.info('[ SET UP 3/4 ] on PC4, copy certificate files and key files...')
        pc4_ssh.send_command('install {}/* /etc/pki/tls/certs/'.format(certPath))
        pc4_ssh.send_command('install {}/* /etc/pki/tls/private/'.format(certPath))

        logger.info('[ SET UP 4/4 ] on PC4, copy socat to PC4...')
        pc4_ssh.send_command('install {}/socat /usr/local/bin/'.format(binPath))

        Assertion.assert_equal(True, True, "ERR: initialize the environment failed")


    def test_02_01_start_https_server(self):
        logger.info('Starting Httpd...!')
        flag = False
        httpd_status = pc4_ssh.send_command('systemctl status httpd')
        if re.search(r'active \(running\)', str(httpd_status), re.S|re.I):
            logger.info('Httpd is already running! Stop it!')
            pc4_ssh.send_command('systemctl restart httpd')
        else:
            pc4_ssh.send_command('systemctl start httpd')

        httpd_status = pc4_ssh.send_command('systemctl status httpd')
        logger.info(httpd_status)
        if re.search(r'active \(running\)', str(httpd_status), re.S|re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: start https server failed")
