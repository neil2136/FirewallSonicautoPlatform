from definition.settings import *
from definition.utils import *


@paramunittest.parametrized(
    {'check_list1': ["Unique Firewall Identifier' , changed from.*?changed to \[AAAAAA\]"],'check_list2':["'Unique Firewall Identifier'.*?AAAAAA"], 'uuid': '1516496'},
    {'check_list1': ["Added 'IPsec Name' , vpn_ti_share, changed to \[vpn_ti_share\]"],'check_list2':["vpn_ti_share.*?Added 'IPsec Name'"], 'uuid': '1516497'},
    {'check_list1': ["'Authentication Method' , vpn_ti_share.*?IKE using Preshared Secret.*?Manual Key"],'check_list2':["vpn_ti_share.*?IKE using Preshared Secret.*?Manual Key"], 'uuid': '1516498'},
    {'check_list1': ["'Local IKE ID Type' , vpn_ti_share.*?changed to \[DER ASN1 Distinguished Name\]"],'check_list2':["vpn_ti_share.*?'Local IKE ID Type'.*?DER ASN1 Distinguished Name"], 'uuid': '1516499'},
    {'check_list1': ["Added 'IPsec Name' , vpn_s2s"],'check_list2':["vpn_s2s.*?Added 'IPsec Name'"], 'uuid': '1516502'},
    {'check_list1': ["'Authentication Method' , vpn_s2s.*?Manual Key.*?IKE using Preshared Secret"],'check_list2':["vpn_s2s.*?Manual Key.*?IKE using Preshared Secret"], 'uuid': '1516500'},
    {'check_list1': ["'Phase 2 Authentication' , vpn_s2s.*?SHA1.*?SHA256"],'check_list2':["vpn_s2s.*?SHA1.*?SHA256"], 'uuid': '1516501'},
    {'check_list1': ["Added 'IPsec Name' , vpn_3rd"],'check_list2':["vpn_3rd.*?Added 'IPsec Name'"], 'uuid': '1516503'},
    {'check_list1': ["'Auto Provision user name' , vpn_client.*?user1.*?user5"],'check_list2':["vpn_client.*?'Auto Provision user name.*?user1.*?user5"], 'uuid': '1516504'},
    {'check_list1': ["Added 'IPsec Name' , vpn_server"],'check_list2':["vpn_server.*?Added 'IPsec Name'"], 'uuid': '1516505'},
    {'check_list1': ["'Send VPN Tunnel Traps only when tunnel status changes'.*?disabled.*?enabled"],'check_list2':["'Send VPN Tunnel Traps only when tunnel status changes'.*?disabled.*?enabled"], 'uuid': '1516506'},
   
    {'check_list1': ["'Send DHCP requests to the server addresses listed below'.*?disabled.*?enabled"],'check_list2':["'Send DHCP requests to the server addresses listed below'.*?disabled.*?enabled"], 'uuid': '1516507'},
    {'check_list1': ["'Enable L2TP Server'.*?disabled.*?enabled"],'check_list2':["'Enable L2TP Server'.*?disabled.*?enabled"], 'uuid': '1516508'},
) 
class Test_Config_Auditing_CLI_VPN_01(Test):

    def setParameters(self, check_list1,check_list2, uuid):
        self.check_list1 = check_list1
        self.check_list2 = check_list2
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
    
    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True , True , "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_01_clear_log(self):
        rc = clear_log_and_snmp_msg()
        Assertion.assert_equal(rc , True , "ERR: clear log and snmp server message failed")

    def test_01_02_config_DUT(self):
        global admin_name
        res = admin_obj.show_admin_setting()
        admin_name = res['administration']['firewall_name']
        logger.info(f'-------------{admin_name}')
        if self.uuid == '1516496':
            rc = fw_cli.do_cli_commands(commands=vpn_set_cmds)
            Assertion.assert_equal(rc, True , "ERR: configure vpn setting failed")
        elif self.uuid == '1516497':
            rc = Lvpn_cli.add_vpnpolicy(**TI_shared)
            Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')
        elif self.uuid == '1516498':
            rc = Lvpn_cli.edit_vpnpolicy(**TI_manual)
            Assertion.assert_equal(rc, True, 'Modify VPN m Policy Failed.')
        elif self.uuid == '1516499':
            rc = Lvpn_cli.edit_vpnpolicy(**TI_3rd)
            Assertion.assert_equal(rc, True, 'Modify VPN Policy Failed.')
        elif self.uuid =='1516502':
            rc = Lvpn_cli.add_vpnpolicy(**S2S_manual)
            Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')
        elif self.uuid =='1516500':
            rc = Lvpn_cli.edit_vpnpolicy(**S2S_shared)
            Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')
        elif self.uuid =='1516501':
            ref = copy.deepcopy(S2S_shared)
            ref['proposal ipsec authentication'] = 'sha-256'
            rc = Lvpn_cli.edit_vpnpolicy(**ref)
            Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')
        elif self.uuid =='1516503':
            rc = Lvpn_cli.add_vpnpolicy(**S2S_3rd)
            Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')
        elif self.uuid =='1516504':
            rc = fw_cli.do_cli_commands(commands=add_pro_client_cmds)
            rc &= fw_cli.do_cli_commands(commands=edit_pro_client_cmds)
            Assertion.assert_equal(rc, True, 'Add and edit VPN Policy Failed.')
        elif self.uuid =='1516505':
            rc = fw_cli.do_cli_commands(commands=add_pro_server_cmds)
            Assertion.assert_equal(rc, True, 'Add  VPN Policy Failed.')
        elif self.uuid == '1516506':
            rc = vpnadv_cli.vpn_advanced_setting(**adv_set)
            Assertion.assert_equal(rc, True, 'conifg advance setting Failed.')
        elif self.uuid == '1516507':
            rc = fw_cli.do_cli_commands(commands=centarl_cmds)
            Assertion.assert_equal(rc, True, 'conifg dhcp over vpn Failed.')
        elif self.uuid == '1516508':
            rc = fw_cli.do_cli_commands(commands=l2tp_cmd)
            Assertion.assert_equal(rc, True, 'conifg  L2TP Server Settings Failed.')

    def test_01_03_verify_syslog(self):
        msg = os.popen('cat /var/log/messages', 'r')
        info = msg.read().replace(' ','').replace('\n','')
        if info == '':
            logger.info('the syslog message is null!!!')
            pass
        else:
            time.sleep(10)
            rc =check_log_msg(mode ='syslog',check_list=self.check_list1)
            Assertion.assert_equal(rc, True, "ERR: check syslog failed")

    def test_01_04_verify_snmp(self):
        rc =check_log_msg(mode ='snmp',check_list=self.check_list1)
        Assertion.assert_equal(rc, True , "ERR: check snmp trap failed")

    def test_01_05_verify_audit_log(self):
        rc =check_log_msg(mode ='audit',check_list=self.check_list2)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_01_06_verify_log(self):
        rc =check_log_msg(mode ='log',check_list=self.check_list1)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_01_07_restore_env(self):
        if self.uuid == '1516496' :
            ref = copy.deepcopy(vpn_set)
            ref['firewall_identifier'] = admin_name
            rc = vpn_setting.config_vpnadvanced(**ref)
            Assertion.assert_equal(rc, True , "ERR: configure vpn setting failed")
        elif self.uuid in ['1516499','1516501','1516503','1516504','1516505']:
            rc = Lvpn_obj.del_all_vpn_policies()
            Assertion.assert_equal(rc, True, 'delete VPN Policy Failed.')
        elif self.uuid == '1516506':
            rc = vpn_setting.config_vpnadvanced(traps_on_change = False)
            Assertion.assert_equal(rc, True, 'conifg advance setting Failed.')
        elif self.uuid == '1516507':
            rc = dhcp_over_vpn.config_dhcpvpn_centralgw(send_requests=False)
            Assertion.assert_equal(rc, True, 'conifg dhcp over vpn Failed.')
        elif self.uuid == '1516508':
            rc = l2tpserver_obj.enable_or_disable_l2ptpserver(enable = False)
            Assertion.assert_equal(rc, True, 'conifg  L2TP Server Settings Failed.')


class Test_Config_Auditing_CLI_VPN_02(Test):
    uuid = "SOSAIOT-TC-55193"
    description = show_testcase_info(TESTPLAN, '1516509', description=True )['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 1516509)
        Assertion.assert_equal(True , True , "ERR: show testcase info failed")

    def test_02_config_vpn(self):
        rc = Lvpn_cli.add_vpnpolicy(**TI_shared)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_03_downlaod_tsr_and_check_keywords(self):
        logger.info(" {} ".center(20, '-').format('download TSR'))
        content = diag_obj.get_tsr_part(func='System',lab1='Status')
        keywrd= "Configuration succeeded:  'Enable Keep Alive' , vpn_ti_share"
        logger.info(content)
        if keywrd in content:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'check key word in TSR  Failed.')

    def test_04_del_vpn(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'delete VPN Policy Failed.')


class Test_Config_Auditing_CLI_VPN_03(Test):
    uuid = "SOSAIOT-TC-55194"
    description = show_testcase_info(TESTPLAN, '1516510', description=True )['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 1516510)
        Assertion.assert_equal(True , True , "ERR: show testcase info failed")

    def test_02_config_mail_server(self):
        rc= start_mail_server.start_mail_server(mail_server_host=pc1_ip)
        Assertion.assert_not_equal(rc, False, "ERR: start email server failed")

    def test_03_config_automation(self):
        output = log_automation.show_log_automation()
        output["log"]["automation"]["email_address"] = {"log":"test@sonicauto.com",
                                                        "alert":"test@sonicauto.com",
                                                        "user":"test@sonicauto.com",
                                                        "audit":"test@sonicauto.com"
                                                        }
        output["log"]["automation"]["mail_server"] = pc1_ip
        output["log"]["automation"]["mail_from"] = 'test.@sonicauto.com'
        output["log"]["automation"]["authentication_method"] = 'none'
        output["log"]["automation"]["mail_server_advanced"] = {"smtp_port":25,
                                                                "connection_security_method":{},
                                                                "smtp_authentication":False
                                                                }
        rc = log_automation.edit_log_automation(**output)
        Assertion.assert_equal(rc, True,"ERR: edit log automation failed")

    def test_04_config_log_vpn(self):
         rc = log_category.edit_log_categories_by_name(name = 'VPN',**log_vpn_category)
         PC1.send_command('rm -rf /home/test/Maildir/new/* ')
         Assertion.assert_equal(rc, True, "ERR: edit vpn log category failed")

    def test_05_config_vpn(self):
        rc = Lvpn_cli.add_vpnpolicy(**TI_shared)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_06_check_mail(self):
        logger.info(" {} ".center(20, '-').format('check mail'))
        time.sleep(10)
        keywrd= "VPN.*?Policy.*?Added"
        rc = False
        for root,dirs,files in os.walk("/home/test/Maildir/new"):
            for file in files:
                file_path = os.path.join(root,file)
                logger.info(f'------------------{file_path}')
                content = PC1.send_command(f'cat {file_path} ')
                logger.info(content)
                if re.search(keywrd, content, re.M | re.I):
                    rc = True
                    break
        Assertion.assert_equal(rc, True, 'check key word in mail Failed.')

    def test_07_del_vpn(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        PC1.send_command(f'hostname {Params.testbed}-PC1')
        Assertion.assert_equal(rc, True, 'delete VPN Policy Failed.')
    
        


