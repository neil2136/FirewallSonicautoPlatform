from definition.init_param import *
from definition.download_and_upload_file import *


class TestConfigTB_00(Test):
    uuid = 'NonTC'
    description = "initial FW"

    def test_00_00_config_x1_interface(self):
        api_dict = {
        'sonicos-api': True,               ### Bool
        'basic': True,                      ### Bool
        }
        rc = sonic_api.sonicos_api(**api_dict)
        sleep(5)
        logger.info('config X1 interface.....')
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
        rc &= interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_00_01_config_x2_interface(self):
        logger.info('config X2 interface...')
        x2 = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv4.config_interface(**x2)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def test_00_02_config_x3_interface(self):
        logger.info('config X3 interface...')
        x3 = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X3_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv4.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    @repeat_method(5)
    def test_00_03_add_accessrule(self):
        rule_opt = {
            'name': 'WAN_to_LAN',
            'enable': True,
            'from': 'WAN',
            'to': 'LAN',
            'action': 'allow',
            'source': {
                "address":{
                    'any': True},
                "port":{"any":True}
            },
            'destination': {
                "address":{
                    "name":"X3 Subnet"},
            },
            'service': { 'any': True },
            'schedule': {"always_on": True},
            'geo_ip_filter': {'enable': False, 'global': True},
            'priority': { 'auto': True }
        }
        rc = acrObj.config_accessrule(**rule_opt)
        Assertion.assert_equal(rc, True, "ERR: Add accessrule failed") 

    def test_00_04_add_route_for_pc1(self):
        localhost.send_command(f'route add -net {Parameter.PC2_eth1_NET} netmask 255.255.255.0 gw {Parameter.FIREWALL}')
        out = localhost.send_command('route -n')
        Assertion.assert_regular(out, r'192.168.13.0\s+?192.168.168.168', "ERR: change route on mail client failed")

    def test_00_05_add_route_for_pc2(self):
        mail_server.send_command(f'route add -net {Parameter.PC1_eth0_NET} netmask 255.255.255.0 gw {Parameter.X3_IP}')
        out =mail_server.send_command('route -n')
        Assertion.assert_regular(out, r'192.168.168.0\s+?192.168.13.168', "ERR: change route on mail server failed")

    def test_00_06_config_ftp_automation(self):
        log_automation_json = {
                "log": {
                    "automation": {
                        "email_address": {
                            "log": "", 
                            "alert": "", 
                            "user": "", 
                            "audit": ""
                        }, 
                        "send_log": {
                            "when_full": True
                        }, 
                        "email_format_log": {
                            "plain_text": True
                        }, 
                        "include_all_log_information": False, 
                        "send_audit": {
                            "when_full": True
                        }, 
                        "email_format_audit": {
                            "plain_text": True
                        }, 
                        "health_check_email": {
                            "schedule": { }
                        }, 
                        "mail_server": "", 
                        "mail_from": "", 
                        "authentication_method": "none", 
                        "mail_server_advanced": {
                            "smtp_port": 25, 
                            "connection_security_method": { }, 
                            "smtp_authentication": False
                        }, 
                        "ftp_log": {
                            "send_log_to_ftp": True, 
                            "server": "192.168.13.200", 
                            "user_name": "root", 
                            "password": "password", 
                            "directory": "/tmp/ftp_log", 
                            "send_log": {
                                "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
                            }, 
                            "file_format": {
                                "plain_text": True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: test_00_07_config_ftp_automation")


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial FW"

    @repeat_method(5)
    def test_00_00_config_mail_server(self):
        rc= start_mail_server.start_mail_server(mail_server_host=mail_server_ip)
        Assertion.assert_not_equal(rc, False, "ERR: start email server failed")


class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = "initial FW"

    @repeat_method(5)
    def test_00_00_config_ftp_server(self):
        mail_server.send_command("sudo yum install vsftpd")
        mail_server.send_command("sed -i /root/d /etc/vsftpd/ftpusers")
        mail_server.send_command("sed -i /root/d /etc/vsftpd/user_list")
        mail_server.send_command("sudo systemctl start vsftpd")
        mail_server.send_command(f"cp -r {local_cert} /root/Downloads/")
        mail_server.send_command("mkdir /tmp/ftp_log")
        localhost.send_command("mkdir /tmp/ftp_log")
        Assertion.assert_equal(True, True, "ERR: config ftp server failed")


class TestConfigTB_03(Test):
    uuid = 'NonTC'
    description = "initial FW"

    def test_00_01_Configure_Interface(self):
        x1_static = {
            'if'     : 'X1',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.WANIP,
            'mask'   : '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1'   : Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
            'fragment_packets': True,
        }
        rc = interface_ipv4.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_00_02_Restore_Remote_FW(self):
        if not rm_device:
            logger.info("no remote device exists, skip this step")
            pass
        else:
            logger.info(" {} ".center(20, '-').format('Restore Remote FW'))
            for i in range(10):
                out = os.popen('ping {} -c 1 -w 1'.format(Parameter.REMOTEX1)).read()
                if ('100% packet loss' not in out):
                    logger.info(out)
                    break
                elif i == 9:
                    logger.info('Remote DUT is unreachable. Check the network configuration.')
                    ret = os.popen('route -n').read()
                    logger.info('----- The route policies on PC1 after reset: -----')
                    logger.info(ret)
                    os.system('service network restart')
                    ret = os.popen('route -n').read()
                    logger.info('----- The route policies on PC1 after reset: -----')
                    logger.info(ret)
            
            logger.info('Restore Remote FW...')
            
            path = cfg_path + 'restore_gw_rmt_tel.py'
            cmd = 'python3 {} -os=1 --testbed={} -device={} -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed, rm_device)
            logger.info(cmd)
            out = os.popen(cmd).read()
            logger.info(out)
            
            rc = False
            for i in range(10):
                out = os.popen('ping {} -c 2'.format(Parameter.REMOTEX0)).read()
                logger.info(out)
                if ('100% packet loss' not in out):
                    logger.info('Ping Remote success.')
                    rc = True
                    break
                elif i == 9:
                    rc = False
                    logger.info('Remote is unreachable.')
            
            logger.info(rc)
            Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    @repeat_method(3)
    def test_00_03_Enable_remote_api_basic(self):
        if not rm_device:
            logger.info("no remote device exists, skip this step")
            pass
        else:
            logger.info(" {} ".center(20, '-').format('Enable Remote Api Basic'))
            logger.info('time sleep 10 sec.')
            time.sleep(10)
            remote = AdminCli(rmt)
            api_dict = {'sonicos-api': True, 'basic': True,}
            try:
                result = remote.sonicos_api(**api_dict)
                if result:
                    logger.info('Success enable remote api basic')
                else:
                    logger.info('Failed enable remote api basic')
            except KeyError:
                logger.error('Failed enable remote api basic')

    def test_00_04_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "10:00:39",
                "date": "2022:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'set DUT time Failed.')

    def test_00_05_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_06_add_net_roule_for_pc2(self):
        mail_server.send_command(f'route add -net {Parameter.LOCALNET} netmask 255.255.255.0 gw {Parameter.REMOTEX0}')
        mail_server.send_command(f'route add -net {Parameter.WANNET} netmask 255.255.255.0 gw {Parameter.REMOTEX0}')
        out = mail_server.send_command('route -n')
        Assertion.assert_regular(out, r'192.168.168.0\s+?172.16.1.101', "ERR: change route on mail server failed")

    def test_00_07_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')