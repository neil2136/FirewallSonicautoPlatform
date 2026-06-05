from definition.settings import *
from lib.utils import *


@pytest.mark.parametrize(
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'127.0.0.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51628', 'tcid': '1'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'169.254.1.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51629', 'tcid': '2'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'224.0.0.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51630', 'tcid': '3'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51631', 'tcid': '4'},
    {'ENABLE_DRAP': 'off','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51632', 'tcid': '5'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1,10.1.1.10', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51633', 'tcid': '6'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'DMZ','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51634', 'tcid': '7'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'LAN','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51635', 'tcid': '8'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'WAN','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51636', 'tcid': '9'},
    {'ENABLE_DRAP': 'on','ACTION':'log-attack-only', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'yes', 'uuid': 'SOSAIOT-TC-51637', 'tcid': '12'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51638', 'tcid': '13'},
    {'ENABLE_DRAP': 'on','ACTION':'return-query-refused', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51639', 'tcid': '14'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'test','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51640', 'tcid': '17'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'test_group','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51641', 'tcid': '18'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'com','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51642', 'tcid': '19'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'test_group','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51643', 'tcid': '20'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'10.1.1.10', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51644', 'tcid': '29'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'192.100.100.1', 'DNS_Server_IF': '', 'X2_Zone':'DMZ','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51645', 'tcid': '39'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'127.0.0.1,10.1.1.10', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51646', 'tcid': '41'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'169.254.1.1,10.1.1.10', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51647', 'tcid': '42'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'224.0.0.1,10.1.1.10', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': '', 'uuid': 'SOSAIOT-TC-51648', 'tcid': '43'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'127.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'DMZ','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51649', 'tcid': '44'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'169.254.1.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'DMZ','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51650', 'tcid': '45'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'224.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'DMZ','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51651', 'tcid': '46'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'127.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'LAN','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51652', 'tcid': '47'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'169.254.1.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'LAN','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51653', 'tcid': '48'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'224.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'LAN','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51654', 'tcid': '49'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'127.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'WAN','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51655', 'tcid': '50'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'169.254.1.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'WAN','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51656', 'tcid': '51'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'','DOMAIN':'','IP_ADDR':'224.0.0.1', 'DNS_Server_IF': 'X2', 'X2_Zone':'WAN','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51657', 'tcid': '52'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'aaa','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51658', 'tcid': '53'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'test_group2','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51659', 'tcid': '54'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'net','DOMAIN':'','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'no','Log': 'yes', 'uuid': 'SOSAIOT-TC-51660', 'tcid': '55'},
    {'ENABLE_DRAP': 'on','ACTION':'drop-dns-reply', 'ALLOW_DOMAIN':'com','DOMAIN':'TEST.COM','IP_ADDR':'192.168.168.1', 'DNS_Server_IF': '', 'X2_Zone':'','DNS_Reply':'yes','Log': 'no', 'uuid': 'SOSAIOT-TC-51661', 'tcid': '56'},
)
class Test_DNS_Rebinding_Attack_Prevention_2170(Test):

    def setParameters(self, ENABLE_DRAP,ACTION,ALLOW_DOMAIN,DOMAIN,IP_ADDR,DNS_Server_IF,X2_Zone,DNS_Reply,Log, uuid, tcid):
        self.ENABLE_DRAP = ENABLE_DRAP
        self.ACTION = ACTION
        self.ALLOW_DOMAIN = ALLOW_DOMAIN
        self.DOMAIN = DOMAIN
        self.IP_ADDR = IP_ADDR
        self.DNS_Server_IF = DNS_Server_IF
        self.X2_Zone = X2_Zone
        self.DNS_Reply = DNS_Reply if DNS_Reply else "no"
        self.Log = Log if Log else "yes"
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_config_X2(self):
        if self.X2_Zone:
            logger.info(" {} ".center(20, '-').format('configure X2 interface '))
            Lx2 = {
                'if': 'X2',
                'zone': self.X2_Zone,
                'mode': 'static',
                'ip': DUT_X2,
                'netmask': '255.255.255.0',
                'mgmt_https': True,
                'mgmt_ssh': True,
                'mgmt_snmp': True,
                'mgmt_ping': True,
            }
            rc = Linterface.config_interface(**Lx2)
            Assertion.assert_equal(rc, True, f"ERR: configure X2 failed")
        else:
            logger.info(" {} ".center(20, '-').format('not need configure X2 interface,test skip.... '))
        
    @repeat_method(3)
    def test_01_02_config_DNS_Server(self):
        logger.info(" {} ".center(20, '-').format('config DNS Server '))
        if self.DNS_Server_IF == 'X2':
            rc = start_dns_server_X2(self.IP_ADDR)
        else:
            rc = start_dns_server(self.IP_ADDR)
        Assertion.assert_equal(rc, True, "ERR: config DNS Server failed")
        
    def test_01_03_config_DNS_Rebinding_Attack_Prevention(self):
        logger.info(" {} ".center(20, '-').format('Confiugre DNS Rebinding Attack Prevention... '))
        ref = copy.deepcopy(dns_set)
        opt = ref['dns']['rebinding']
        if self.ENABLE_DRAP == 'on':
            opt['action'] = self.ACTION
            if self.ALLOW_DOMAIN:
                if 'group' in self.ALLOW_DOMAIN:
                    opt['allowed_domains'] = {"group":self.ALLOW_DOMAIN}
                else:
                    opt['allowed_domains'] = {"name":self.ALLOW_DOMAIN}
            else:
                opt['allowed_domains'] = {}
        else:
            ref['dns']['rebinding'] = {"enable":False}
        logger.info(f'-----------{ref}')
        rc = dnsObj.set_dns(**ref)
        Assertion.assert_equal(rc, True, "ERR: Confiugre DNS Rebinding Attack Prevention... failed")
    
    @repeat_method(3)
    def test_01_04_Lookup_DUT_Domain(self):
        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('Lookup the FQDN Domain ... '))
        LogObj.clear_log()
        dns_ip = PC2_WAN if self.DNS_Server_IF != "X2" else PC3_WAN
        domain = self.DOMAIN if self.DOMAIN else 'test.com'
        ip = get_ip_of_name(dns_ip,self.ACTION,domain)
        logger.info(f'ip:{ip}')
        rc = False if (ip and self.DNS_Reply == 'no') or (not ip and self.DNS_Reply == 'yes') else True
        Assertion.assert_equal(rc, True, "ERR: Lookup the FQDN Domain ... failed")
        
    @repeat_method(3)
    def test_01_05_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        time.sleep(20)
        alert_msg   = 'DNS Rebind Attack Detected'
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        if self.ACTION == 'log-attack-only':
            ret = 0 if alert_msg in export_log else 1
        else:
            ret = 0 if block_msg in export_log else 1
        rc = False if (ret == 0 and self.Log == 'no') or (ret != 0 and self.Log == 'yes') else True
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT ... failed")


#######add new 4 cases for dns proxy
class Test_DNS_Rebinding_Config_env_02(Test):
    uuid = 'NonTC'
    description = "add config for dns proxy"
    goto_teardown = True

    def test_02_Add_DNS_policy(self):
        rc = dnsPolicy.add_dns_policy(**dns_proxy_4to4)
        Assertion.assert_equal(rc, True, "ERR: Add DNS policy failed")

    def test_03_config_X2(self):
        logger.info(" {} ".center(20, '-').format('configure X2 interface '))
        Lx2 = {
            'if': 'X2',
            'zone': "WAN",
            'mode': 'static',
            'ip': DUT_X2,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
        }
        rc = Linterface.config_interface(**Lx2)
        Assertion.assert_equal(rc, True, f"ERR: configure X2 failed")

    def test_04_config_DNS_Rebinding_Attack_Prevention(self):
        logger.info(" {} ".center(20, '-').format('Confiugre DNS Rebinding Attack Prevention... '))
        ref = copy.deepcopy(dns_set)
        ref['dns']['server']['inherit'] =  False
        ref['dns']['server']['static']['primary'] = PC3_WAN
        opt = ref['dns']['rebinding']
        opt['action'] = "drop-dns-reply"
        opt['allowed_domains'] = {}
        logger.info(f'-----------{ref}')
        rc = dnsObj.set_dns(**ref)
        Assertion.assert_equal(rc, True, "ERR: Confiugre DNS Rebinding Attack Prevention... failed")

    def test_06_Set_LanPC_DNS(self):
        logger.info(" {} ".center(20, '-').format('Set DNS'))
        cmds = [f'echo "nameserver 192.168.168.168" > /etc/resolv.conf',"cat /etc/resolv.conf"]
        out = PC1.send_commands(cmds)
        if '192.168.168.168' in str(out):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'config lan pc dns server  Failed.')


class Test_DNS_Rebinding_Prevention_2170_03(Test):
    uuid = "SOSAIOT-TC-51662"
    description = show_testcase_info(TESTPLAN, "2499023", description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "2499023")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_03_01_config_DNS_Server(self):
        logger.info(" {} ".center(20, '-').format('config DNS Server '))
        rc = start_dns_server_X2("127.0.0.1")
        Assertion.assert_equal(rc, True, "ERR: config DNS Server failed")
    
    @repeat_method(3)
    def test_03_02_check_pkt_resolve(self):
        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('check packet dropped ... '))
        LogObj.clear_log()
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        out = PC1.send_command('ping test.com -c 2')
        logger.info(f'ping result: {out}')
        time.sleep(3)
        LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng( filepath='/tmp/packet-c.pcapng')
        rc = check_packet(pkt_path='/tmp/packet-c.pcapng',filter='dns.flags.response == 1',key_word='Packet dropped - DNS Rebind attack')
        Assertion.assert_equal(rc, True, "ERR: check packet dropped ... ... failed")
        
    @repeat_method(3)
    def test_03_03_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        time.sleep(20)
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        rc = True if block_msg in export_log else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT ... failed")

    @repeat_method(3)
    def test_03_04_config_DNS_Server(self):
        logger.info(" {} ".center(20, '-').format('config DNS Server '))
        rc = start_dns_server_X2("192.168.168.1")
        Assertion.assert_equal(rc, True, "ERR: config DNS Server failed")
    
    @repeat_method(3)
    def test_03_05_check_pkt_resolve(self):
        time.sleep(10)
        logger.info(" {} ".center(20, '-').format('check packet dropped ... '))
        LogObj.clear_log()
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        out = PC1.send_command('ping test.com -c 2')
        logger.info(f'ping result: {out}')
        time.sleep(3)
        LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng( filepath='/tmp/packet-c.pcapng')
        rc = check_packet(pkt_path='/tmp/packet-c.pcapng',filter='dns.flags.response == 1',key_word='Packet dropped - DNS Rebind attack')
        Assertion.assert_equal(rc, True, "ERR: check packet dropped ... ... failed")
        
    @repeat_method(3)
    def test_03_06_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        time.sleep(20)
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        rc = True if block_msg in export_log else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT ... failed")


##not stable 
class Test_DNS_Rebinding_Prevention_2170_04(Test):
    uuid = "SOSAIOT-TC-51663"
    description = show_testcase_info(TESTPLAN, "2499024", description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "2499024")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_04_01_config_DNS_Server(self):
        logger.info(" {} ".center(20, '-').format('config DNS Server '))
        rc = start_dns_server_X2("127.0.0.1")
        Assertion.assert_equal(rc, True, "ERR: config DNS Server failed")
    
    @repeat_method(3)
    def test_04_02_check_pkt_resolve(self):
        logger.info(" {} ".center(20, '-').format('check packet not dropped ... '))
        LogObj.clear_log()
        LPackageMonitObj.clear_packets()
        time.sleep(2)
        LPackageMonitObj.start_capture()
        diag_obj.diag_ping(dn='test.com')
        out = diag_obj.get_Ping_Result()
        logger.info(f'diag ping result: {out}')
        rc = True if '127.0.0.1' in out['data']['line1'] else False
        # LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng( filepath='/tmp/packet-c.pcapng')
        rc &= not check_packet(pkt_path='/tmp/packet-c.pcapng',filter='dns.flags.response == 1',key_word='Packet dropped - DNS Rebind attack')
        Assertion.assert_equal(rc, True, "ERR: check packet not dropped . failed")
        
    def test_04_03_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        rc = True if block_msg not in export_log else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT ... failed")

    @repeat_method(3)
    def test_04_05_check_pkt_resolve(self):
        logger.info(" {} ".center(20, '-').format('check packet dropped ... '))
        LogObj.clear_log()
        LPackageMonitObj.clear_packets()
        time.sleep(2)
        LPackageMonitObj.start_capture()
        diag_obj.real_time_lookup(ip='185.167.98.85',domain='dnsbl.sorbs.net',dnsServer=PC3_WAN)
        out = diag_obj.get_RBL_lookup_result()
        logger.info(f'ping result: {out}')
        # LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng( filepath='/tmp/packet-c.pcapng')
        rc = not check_packet(pkt_path='/tmp/packet-c.pcapng',filter='dns.flags.response == 1',key_word='Packet dropped - DNS Rebind attack')
        Assertion.assert_equal(rc, True, "ERR: check packet not dropped ... ... failed")
        
    def test_04_06_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        rc = True if block_msg not in export_log else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT ... failed")

    
class Test_DNS_Rebinding_Prevention_2170_05(Test):
    uuid = "SOSAIOT-TC-51664"
    description = show_testcase_info(TESTPLAN, "2499025", description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "2499025")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_05_01_config_DNS_Server(self):
        logger.info(" {} ".center(20, '-').format('config DNS Server '))
        rc = start_dns_server_X2("127.0.0.1")
        Assertion.assert_equal(rc, True, "ERR: config DNS Server failed")
    
    @repeat_method(3)
    def test_05_02_check_pkt_resolve(self):
        logger.info(" {} ".center(20, '-').format('check packet not dropped ... '))
        LogObj.clear_log()
        LPackageMonitObj.clear_packets()
        time.sleep(2)
        LPackageMonitObj.start_capture()
        diag_obj.diag_ping(dn='test.com')
        out = diag_obj.get_Ping_Result()
        logger.info(f'diag ping result: {out}')
        rc = True if '127.0.0.1' in out['data']['line1'] else False
        # LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng( filepath='/tmp/packet-d.pcapng')
        rc &= not check_packet(pkt_path='/tmp/packet-d.pcapng',filter='dns.flags.response == 1',key_word='Packet dropped - DNS Rebind attack')
        Assertion.assert_equal(rc, True, "ERR: check packet not dropped . failed")
        
    def test_05_03_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        block_msg   = 'DNS rebind attack blocked'
        export_log = LogObj.export_log_txt() 
        rc = True if block_msg not in export_log else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT  failed")


class Test_DNS_Rebinding_Prevention_2170_06(Test):
    uuid = "SOSAIOT-TC-51665"
    description = show_testcase_info(TESTPLAN, "3038692", description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, "3038692")
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_Get_Log_of_DUT(self):
        logger.info(" {} ".center(20, '-').format('get the log of DUT ...'))
        LogObj.clear_log()
        time.sleep(2)
        PC1.send_command("nslookup gate.yukika.net")
        msg1   = 'DNS rebind attack blocked'
        # msg2 = "FQDN=gate.yukika.net"
        export_log = LogObj.export_log_txt() 
        rc = True if msg1 in export_log  else False
        logger.info(export_log)
        Assertion.assert_equal(rc, True, "ERR: get the log of DUT  failed")

    # def test_06_02_restore_LanPC_DNS(self):
    #     logger.info(" {} ".center(20, '-').format('restore dns server'))
    #     PC1.send_command(f'echo "nameserver 10.190.202.200" > /etc/resolv.conf')
    #     PC1.send_command(f'echo "nameserver 10.50.56.148" >> /etc/resolv.conf')
    #     out = PC1.send_command('cat /etc/resolv.conf')
    #     if '10.50.56.148' in str(out):
    #         rc = True
    #     else:
    #         rc = False
    #     Assertion.assert_equal(rc, True, 'restore pc1 dns server  Failed.')

    # @repeat_method(3)
    # def test_06_03_resolve_dns(self):
    #     out = PC1.send_command("nslookup gate.yukika.net")
    #     rc = True if "192.168.9.254" in out else False
    #     Assertion.assert_equal(rc, True, 'dns lookup  Failed.')



