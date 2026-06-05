from definition.settings import *
from definition.utils import *


@paramunittest.parametrized(
    {'check_list1': ["Application Firewall Email match' , test_email, changed to \[Regex Match\]"],'check_list2':["test_email.*?Application Firewall Email match.*?Regex Match"], 'uuid': '1514640'},
    # {'check_list1': ["Application Firewall Email match' , test_email, changed to \[Exact Match\]"],'check_list2':["test_email.*?Application Firewall Email match.*?Exact Match"], 'uuid': '1514640'},
    {'check_list1': ["Deleted 'Application Firewall Email name' , test_email"],'check_list2':["test_email.*?Deleted 'Application Firewall Email name'"], 'uuid': '1514641'},
    {'check_list1': ["test_list_obj, changed from \[CFS List Keyword\], changed to \[CFS List Object\]"],'check_list2':["test_list_obj.*?CFS List Keyword.*?CFS List Object"], 'uuid': '1514642'},
    {'check_list1': ["Deleted 'CFS URL List Object Id' , test_list_obj"],'check_list2':["test_list_obj.*?Deleted 'CFS URL List Object Id'"], 'uuid': '1514643'},
    {'check_list1': ["test_uri_list, changed from \[test_uri_grp\], changed to \[test_uri_list\]"],'check_list2':["test_uri_list.*?test_uri_grp.*?test_uri_list"], 'uuid': '1514644'},
    {'check_list1': ["test_action, changed from \[enabled\], changed to \[disabled\]"],'check_list2':["test_action.*?enabled.*?disabled"], 'uuid': '1514645'},
    {'check_list1': ["Deleted 'CFS Action Object Id' , test_action"],'check_list2':["test_action.*?Deleted 'CFS Action Object Id'"], 'uuid': '1514646'},
    {'check_list1': ["CFS Profile Forbidden URLs Operation' , test_profile, changed from \[1\], changed to \[4\]"],'check_list2':["test_profile.*?CFS Profile Forbidden URLs Operation.*?1.*?4"], 'uuid': '1514647'},
    {'check_list1': ["CFS Policy Schedule Object Handle' , test_ploicy, changed to \[Work Hours\]"],'check_list2':["test_ploicy.*?CFS Policy Schedule Object Handle.*?Work Hours"], 'uuid': '1514657'},
    {'check_list1': ["Deleted 'CFS Policy Name' , test_ploicy"],'check_list2':["test_ploicy.*?Deleted 'CFS Policy Name"], 'uuid': '1514659'},
    {'check_list1': ["CFS Policy Enabled.*?changed from \[enabled\], changed to \[disabled\]","CFS Policy Enabled.*?changed from \[disabled\], changed to \[enabled\]"],
     'check_list2':["CFS Policy Enabled.*?disabled.*?enabled","CFS Policy Enabled.*?enabled.*?disabled"], 'uuid': '1514658'},
    {'check_list1': ["Policy Name.*?changed to \[test_acl\]"],'check_list2':["Policy Name.*?test_acl"], 'uuid': '1514648'},
    {'check_list1': ["Destination Service.*?changed to \[BGP\]"],'check_list2':["Destination Service.*?BGP"], 'uuid': '1514660'},
    {'check_list1': ["Enabled Policy.*?changed from \[enabled\], changed to \[disabled\]","Enabled Policy.*?changed from \[disabled\], changed to \[enabled\]"],
     'check_list2':["Enabled Policy.*?disabled.*?enabled","Enabled Policy.*?enabled.*?disabled"], 'uuid': '1514654'},
    {'check_list1': ["test_match, changed to \[NETSCAPE.FIREFOX\]","'Application Firewall object name' , match_modify, changed to \[match_modify\]","Application Firewall object type' , match_modify, changed to \[HTTP Host\]"],
     'check_list2':["test_match.*?NETSCAPE.FIREFOX","match_modify.*?Application Firewall object name","match_modify.*?Application Firewall object type.*?HTTP Host"], 'uuid': '1514661'},
    {'check_list1': ["Deleted 'Application Firewall object name' , match_modify",],'check_list2':["match_modify.*?Deleted 'Application Firewall object name'"], 'uuid': '1514662'},
    {'check_list1': ["Application Firewall object type' , test, changed to \[Application List\]"],'check_list2':["test.*?Application Firewall object type.*?Application List"], 'uuid': '1514663'},
    {'check_list1': ["Application Firewall policy destination address' , test_modify.*?changed to \[test_syslog\]","Application Firewall policy name' , test_modify"],
     'check_list2':["test_modify.*?Application Firewall policy destination address.*?test_syslog","test_modify.*?Application Firewall policy name"], 'uuid': '1514651'},
    {'check_list1': ["Application Firewall policy user exclude' , test_modify.*?changed to \[Guest Administrators\]"],'check_list2':["test_modify.*?Application Firewall policy user exclude.*?Guest Administrators"], 'uuid': '1514652'},

    # {'check_list1': ["Application Firewall policy destination address' , test_modify, changed to \[test_syslog\]","Application Firewall CFS forbid Ojbect name' , test_modify"],
    #  'check_list2':["test_modify.*?Application Firewall policy destination address.*?test_syslog","test_modify.*?Application Firewall CFS forbid Ojbect name"], 'uuid': '1514651'},
    # {'check_list1': ["Application Firewall policy user exclude' , test_modify, changed to \[Guest Administrators\]"],'check_list2':["test_modify.*?Application Firewall policy user exclude.*?Guest Administrators"], 'uuid': '1514652'},
    {'check_list1': ["Deleted 'Application Firewall policy name' , test_modify"],'check_list2':["test_modify.*?Deleted 'Application Firewall policy name"], 'uuid': '1514653'},
    {'check_list1': ["IS Appcontrol Enabled.*?changed to \[enabled\]"],'check_list2':["IS Appcontrol Enabled.*?enabled"], 'uuid': '1514655'},
    {'check_list1': ["Log Intrusions in this Category' , GAMING.*?changed to \[Disable\]"],'check_list2':["GAMING.*?Log Intrusions in this Category.*?Disable"], 'uuid': '1514656'},
    # {'check_list1': ["Use Global LRT for Category' , GAMING.*?changed to \[enabled\]"],'check_list2':["GAMING.*?Use Global LRT for Category.*?enabled"], 'uuid': '1514656'},
    {'check_list1': ["Application Firewall Action color' , test_action, changed to \[Blue\]"],'check_list2':["test_action.*?Application Firewall Action color.*?Blue"], 'uuid': '1514664'},
    {'check_list1': ["Deleted 'Application Firewall Action name' , test_action"],'check_list2':["test_action.*?Deleted 'Application Firewall Action name'"], 'uuid': '1514665'},
    {'check_list1': ["Address Object Zone' , test_addr_v4.*?changed to \[LAN\]"],'check_list2':["test_addr_v4.*?Address Object Zone.*?LAN"], 'uuid': '1514666'},
    {'check_list1': ["Deleted 'Address Object' , test_addr_v4"],'check_list2':["test_addr_v4.*?Deleted 'Address Object'"], 'uuid': '1514667'},
    {'check_list1': ["IPv6 Address Object Zone' , test_addr_v6.*?changed to \[VPN\]"],'check_list2':["test_addr_v6.*?IPv6 Address Object Zone.*?VPN"], 'uuid': '1514668'},
    {'check_list1': ["Address Object in Group' , test_addr_grp, changed to.*?IPv6 Link-Local Subnet"],'check_list2':["test_addr_grp.*?Address Object in Group.*?IPv6 Link-Local Subnet"], 'uuid': '1514669'},
    {'check_list1': ["Service Name' , test_service, changed to \[BGP\]"],'check_list2':["test_service.*?Service Name.*?BGP"], 'uuid': '1514670'},
    {'check_list1': ["Bandwidth Object Maximum Bandwidth' , test_bdw.*?changed to \[5000\]"],'check_list2':["test_bdw.*?Bandwidth Object Maximum Bandwidth.*?5000"], 'uuid': '1514671'},
    {'check_list1': ["Deleted 'Bandwidth Object Name' , test_bdw"],'check_list2':["test_bdw.*?Deleted 'Bandwidth Object Name'"], 'uuid': '1514672'},
    {'check_list1': ["Bandwidth Object Violation Action' , test_bdw2.*?changed to \[Delay\]"],'check_list2':["test_bdw2.*?Bandwidth Object Violation Action.*?Delay"], 'uuid': '1514673'},
    {'check_list1': ["Deleted 'Bandwidth Object Name' , test_bdw2"],'check_list2':["test_bdw2.*?Deleted 'Bandwidth Object Name'"], 'uuid': '1514674'},

    
) 
class Test_Config_Audit_CLI_Firewall_01(Test):

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
        if self.uuid == '1514640':
            rc = fw_cli.do_cli_commands(commands=modify_email)
            Assertion.assert_equal(rc, True , "ERR: Modify an email adderss object failed")
        elif self.uuid == '1514641':
            rc = fw_cli.do_cli_commands(commands=del_email)
            Assertion.assert_equal(rc, True , "ERR: Delete an email adderss object failed")
        elif self.uuid == '1514642':
            rc = fw_cli.do_cli_commands(commands=modify_uri_obj)
            Assertion.assert_equal(rc, True , "ERR: Modify an URI list object failed")
        elif self.uuid == '1514643':
            rc = fw_cli.do_cli_commands(commands=del_uri_obj)
            Assertion.assert_equal(rc, True , "ERR: Delete an URI list object failed")
        elif self.uuid == '1514644':
            rc = fw_cli.do_cli_commands(commands=modify_uri_group)
            Assertion.assert_equal(rc, True , "ERR:Modify an URI list group failed")
        elif self.uuid == '1514645':
            rc = fw_cli.do_cli_commands(commands=modify_cfs_action)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom CFS action object failed")
        elif self.uuid == '1514646':
            rc = fw_cli.do_cli_commands(commands=del_cfs_action)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom CFS action object failed")
        elif self.uuid == '1514647':
            rc = fw_cli.do_cli_commands(commands=modify_cfs_profile)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom CFS profile object failed")
        elif self.uuid == '1514657':
            rc = fw_cli.do_cli_commands(commands=modify_cfs_policy)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom CFS policy failed")
        elif self.uuid == '1514659':
            rc = fw_cli.do_cli_commands(commands=del_cfs_policy)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom CFS policy failed") 
        elif self.uuid == '1514658':
            rc = fw_cli.do_cli_commands(commands=enable_cfs_plicy)
            Assertion.assert_equal(rc, True , "ERR: Enable/Disable the default content filter policy failed") 
        elif self.uuid == '1514648':
            rc = fw_cli.do_cli_commands(commands=modify_acl_v6)
            Assertion.assert_equal(rc, True , "ERR: Modify an access rule of IPv6 type failed")
        elif self.uuid == '1514660':
            rc = fw_cli.do_cli_commands(commands=modify_acl_v4)
            Assertion.assert_equal(rc, True , "ERR: Modify an access rule of IPv4 type failed")
        elif self.uuid == '1514654':
            rc = fw_cli.do_cli_commands(commands=enable_acl_v4)
            Assertion.assert_equal(rc, True , "ERR: Enable/Disable an access rule of IPv4 type failed")
        elif self.uuid == '1514661':
            rc = fw_cli.do_cli_commands(commands=modify_match_obj)
            Assertion.assert_equal(rc, True , "ERR: Modify a match object failed")
        elif self.uuid == '1514662':
            rc = fw_cli.do_cli_commands(commands=del_match_obj)
            Assertion.assert_equal(rc, True , "ERR: Delete all match objects failed")
        elif self.uuid == '1514663':
            rc = fw_cli.do_cli_commands(commands=modify_app_list)
            Assertion.assert_equal(rc, True , "ERR: Modify an application list object failed")
        elif self.uuid == '1514651':
            rc = fw_cli.do_cli_commands(commands=modify_app_rule1)
            Assertion.assert_equal(rc, True , "ERR: Modify an app control policy Policy Name/Type and Source/Destination options failed")
        elif self.uuid == '1514652':
            rc = fw_cli.do_cli_commands(commands=modify_app_rule2)
            Assertion.assert_equal(rc, True , "ERR: Modify an app control policy Included/Excluded failed")
        elif self.uuid == '1514653':
            rc = fw_cli.do_cli_commands(commands=del_app_policy)
            Assertion.assert_equal(rc, True , "ERR: Delete an app control policy failed")
        elif self.uuid == '1514655':
            rc = fw_cli.do_cli_commands(commands=modify_control_settings)
            Assertion.assert_equal(rc, True , "ERR: Modify global settings of app control failed")
        elif self.uuid == '1514656':
            rc = fw_cli.do_cli_commands(commands=modify_category_settings)
            Assertion.assert_equal(rc, True , "ERR: Modify app control settings of a category failed")
        elif self.uuid == '1514664':
            rc = fw_cli.do_cli_commands(commands=modify_action_obj)
            Assertion.assert_equal(rc, True , "ERR: Modify an action object failed")
        elif self.uuid == '1514665':
            rc = fw_cli.do_cli_commands(commands=del_action_obj)
            Assertion.assert_equal(rc, True , "ERR: Delete all action objects failed")
        elif self.uuid == '1514666':
            rc = fw_cli.do_cli_commands(commands=modify_addr_v4)
            Assertion.assert_equal(rc, True , "ERR: Modify an address object of IPv4 type failed")
        elif self.uuid == '1514667':
            rc = fw_cli.do_cli_commands(commands=del_addr_v4)
            Assertion.assert_equal(rc, True , "ERR: Delete an address object of IPv4 type failed")
        elif self.uuid == '1514668':
            rc = fw_cli.do_cli_commands(commands=modify_addr_v6)
            Assertion.assert_equal(rc, True , "ERR: Modify an address object of IPv6 type failed")
        elif self.uuid == '1514669':
            rc = fw_cli.do_cli_commands(commands=modify_addr_group)
            Assertion.assert_equal(rc, True , "ERR: Modify an address group failed")
        elif self.uuid == '1514670':
            rc = fw_cli.do_cli_commands(commands=modify_service_grp)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom service group failed")
        elif self.uuid == '1514671':
            rc = fw_cli.do_cli_commands(commands=modify_bdw_obj)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom bandwitdth object failed")
        elif self.uuid == '1514672':
            rc = fw_cli.do_cli_commands(commands=del_bdw_obj)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom bandwitdth object failed")
        elif self.uuid == '1514673':
            rc = fw_cli.do_cli_commands(commands=modify_bdw_obj2)
            Assertion.assert_equal(rc, True , "ERR: Modify a custom bandwitdth object failed")
        elif self.uuid == '1514674':
            rc = fw_cli.do_cli_commands(commands=del_bdw_obj2)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom bandwitdth object failed")
        
    @repeat_method(3)
    def test_01_03_verify_syslog(self):
        time.sleep(2)
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
        if self.uuid == '1514644' :
            rc = fw_cli.do_cli_commands(commands=del_uri_group)
            Assertion.assert_equal(rc, True , "ERR: Delete an URI list group failed")
        elif self.uuid == '1514647':
            rc = fw_cli.do_cli_commands(commands=del_cfs_profile)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom CFS profile object failed")
        elif self.uuid == '1514648':
            rc = fw_cli.do_cli_commands(commands=del_acl_v6)
            Assertion.assert_equal(rc, True , "ERR: Delete an access rule of IPv6 type failed")
        elif self.uuid == '1514654':
            rc = fw_cli.do_cli_commands(commands=del_acl_v4)
            Assertion.assert_equal(rc, True , "ERR: Delete an access rule of IPv4 type failed")
        elif self.uuid == '1514653':
            rc = fw_cli.do_cli_commands(commands=del_match_obj)
            Assertion.assert_equal(rc, True , "ERR: Delete match obj failed")
        elif self.uuid == '1514668':
            rc = fw_cli.do_cli_commands(commands=del_addr_v6)
            Assertion.assert_equal(rc, True , "ERR: Delete an address object of IPv6 type failed")
        elif self.uuid == '1514669':
            rc = fw_cli.do_cli_commands(commands=del_addr_group)
            Assertion.assert_equal(rc, True , "ERR: Delete an address group failed")
        elif self.uuid == '1514670':
            rc = fw_cli.do_cli_commands(commands=del_service_grp)
            Assertion.assert_equal(rc, True , "ERR: Delete a custom service group failed")


class Test_Config_Audit_CLI_Firewall_02(Test):
    uuid = "SOSAIOT-TC-54970"
    description= show_testcase_info(TESTPLAN, '1514649', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514649')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(3)
    def test_01_clear_log(self):
        rc = clear_log_and_snmp_msg()
        Assertion.assert_equal(rc , True , "ERR: clear log and snmp server message failed")

    def test_02_config_acl_fail(self):
        rc = fw_cli.do_cli_commands(commands=wrong_cmd)
        Assertion.assert_equal(rc, False, f"ERR: config acl fail.")

    def test_03_verify_audit_log(self):
        check_list = "Auto Priority.*?FailedPolicy Action: Invalid priority! "
        rc =check_log_msg(mode ='audit',check_list=check_list)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_04_verify_log(self):
        "Configuration failed: 'Priority for policy' , Allow 'Any' from 'Any' to 'Any', changed from [Auto Priority], changed to [17]"
        check_list = "Configuration failed: 'Priority for policy'.*?changed from \[Auto Priority\], changed to"
        rc =check_log_msg(mode ='log',check_list=check_list)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_05_check_tsr(self):
        "Configuration failed:  'Priority for policy' , Allow 'Any' from 'Any' to 'Any', changed from [Auto Priority], changed to [17]"
        # check_str = "Configuration failed:  'Priority for policy'.*?changed from \[Auto Priority\], changed to"
        check_str = "Configuration failed:  'Policy priority'"
        content = diag_obj.get_tsr_part(func="System",lab1="Status",lab2="Last Alerts")
        logger.info(f"----The content is ---{content}----")
        if re.search(check_str, content, re.M):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check tsr failed")


##base 2
class Test_Config_Audit_CLI_Firewall_03(Test):
    uuid = "SOSAIOT-TC-54971"
    description= show_testcase_info(TESTPLAN, '1514650', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1514650')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    @repeat_method(3)
    def test_01_clear_log(self):
        rc = clear_log_and_snmp_msg()
        Assertion.assert_equal(rc , True , "ERR: clear log and snmp server message failed")

    def test_01_delete_acl(self):
        rc = fw_cli.do_cli_commands(commands=del_acl)
        Assertion.assert_equal(rc, True, f"ERR: delete acl fail.")

    def test_03_verify_audit_log(self):
        check_list = "Deleted 'Policy Action'.*?Succeeded"
        rc =check_log_msg(mode ='audit',check_list=check_list)
        Assertion.assert_equal(rc, True, "ERR: check audit log failed")

    def test_04_verify_log(self):
        check_list = "Configuration succeeded: Deleted 'Policy Action'"
        rc =check_log_msg(mode ='log',check_list=check_list)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_05_check_tsr(self):
        # "Configuration succeeded:  "
        check_str = "Configuration succeeded: Deleted 'Policy Action'"
        content = diag_obj.get_tsr_part(func="System",lab1="Status",lab2="Last Alerts")
        logger.info(f"----The content is ---{content}----")
        if re.search(check_str, content, re.M):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check tsr failed")

