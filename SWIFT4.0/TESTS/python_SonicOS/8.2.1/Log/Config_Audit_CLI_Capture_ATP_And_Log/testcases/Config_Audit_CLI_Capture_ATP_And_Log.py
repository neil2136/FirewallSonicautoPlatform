from definition.settings import *
from definition.utils import *


@paramunittest.parametrized(
    {'check_list1': ["Clear All Log"],'check_list2':["Clear All Log"], 'uuid': '1518482'},
    {'check_list1': ["Log Group Priority' , Log Group \[General\].*?changed to \[ALERT\]"],'check_list2':["Log Group Priority.*?ALERT"], 'uuid': '1518483'},
    {'check_list1': ["'Log Global Email Address' , Log Global Settings, changed to \[123456@sonicwall.com\]"],'check_list2':["Log Global Settings.*?Log Global Email Address.*?123456@sonicwall.com"], 'uuid': '1518484'},
    {'check_list1': ["Reset Log Event Count"],'check_list2':["Reset Log Event Count"], 'uuid': '1518485'},
    {'check_list1': ["Save To Template 'Log Custom Template Description'","Import Log Template 'logTemplateNum'"],'check_list2':["Save To Template 'Log Custom Template Description'","Import Log Template 'logTemplateNum'"], 'uuid': '1518486'},
    {'check_list1': ["Log Category \[Anti-Spam\], changed to \[3344_category@sonicwall.com\]"],'check_list2':["Log Category Email Address.*?3344_category@sonicwall.com"], 'uuid': '1518487'},
    {'check_list1': ["Log Group Alert Email.*?Log Group \[General\].*?changed to \[123_group@sonicwall.com\]"],'check_list2':["Log Group \[General\].*?Log Group Alert Email.*?123_group@sonicwall.com"], 'uuid': '1518488'},
    {'check_list1': ["Log Event Alert Email.*?Log Event \[CSE Disabled\].*?changed to \[678_event@sonicwall.com\]"],'check_list2':["Log Event \[CSE Disabled\].*?Log Event Alert Email.*?678_event@sonicwall.com"], 'uuid': '1518489'},
    {'check_list1': ["Reset Log Event Count"],'check_list2':["Reset Log Event Count"], 'uuid': '1518490'},
    {'check_list1': ["Display Time Stamp in UTC' , changed from \[disabled\], changed to \[enabled\]"],'check_list2':["Display Time Stamp in UTC.*?disabled.*?enabled"], 'uuid': '1518491'},
    {'check_list1': ["SonicWall Capture ATP status' , changed from \[disabled\], changed to \[enabled\]","SonicWall Capture ATP status' , changed from \[enabled\], changed to \[disabled\]"],
     'check_list2':["SonicWall Capture ATP status.*?disabled.*?enabled","SonicWall Capture ATP status.*?enabled.*?disabled"], 'uuid': '1518492'},
    {'check_list1': ["Aux Syslog Server Address Object.*?changed to \[test_syslog\]"],'check_list2':["Aux Syslog Server Address Object.*?test_syslog"], 'uuid': '1518493'},
    {'check_list1': ["Syslog Server Enabled.*?changed from \[enabled\], changed to \[disabled\]","Syslog Server Enabled.*?changed from \[disabled\], changed to \[enabled\]"],
     'check_list2':["Syslog Server Enabled.*?disabled.*?enabled","Syslog Server Enabled.*?enabled.*?disabled"], 'uuid': '1518494'},
    {'check_list1': ["Enable Data Rate Limiting.*?changed from \[disabled\], changed to \[enabled\]"],'check_list2':["Enable Data Rate Limiting.*?disabled.*?enabled"], 'uuid': '1518495'},
    {'check_list1': ["Deleted 'Aux Syslog Server Address"],'check_list2':["Deleted 'Aux Syslog Server Address"], 'uuid': '1518496'},
    {'check_list1': ["Name Resolution Method' , changed from \[None\], changed to \[DNS\]"],'check_list2':["Name Resolution Method.*?None.*?DNS"], 'uuid': '1518497'},
    {'check_list1': ["Reset Name Cache"],'check_list2':["Reset Name Cache"], 'uuid': '1518498'},
    {'check_list1': ["Toggle Reports"],'check_list2':["Toggle Reports"], 'uuid': '1518499'},
    {'check_list1': ["Send Log to E-mail Address' , changed to \[test@sonicauto.com"],'check_list2':["Send Log to E-mail Address.*?test@sonicauto.com"], 'uuid': '1518501'},
    {'check_list1': ["Enable BWM File Type PDF' , changed from \[disabled\], changed to \[enabled\]","Enable BWM File Type PDF' , changed from \[enabled\], changed to \[disabled\]"],
     'check_list2':["Enable BWM File Type PDF.*?disabled.*?enabled","Enable BWM File Type PDF.*?enabled.*?disabled"], 'uuid': '1518502'},
    {'check_list1': ["Mail Server.*?changed to \[192.168.168.200\]"],'check_list2':["Mail Server.*?192.168.168.200"], 'uuid': '1518503'},
    {'check_list1': ["Connection Security Method.*?changed to \[STARTTLS\]"],'check_list2':["Connection Security Method.*?STARTTLS"], 'uuid': '1518504'},
    {'check_list1': ["Report Logs by FTP.*?disabled\], changed to \[enabled\]"],'check_list2':["Report Logs by FTP.*?disabled.*?enabled"], 'uuid': '1518506'},
    {'check_list1': ["SonicWall Capture ATP status' , changed from \[disabled\], changed to \[enabled\]"],'check_list2':["SonicWall Capture ATP status.*?disabled.*?enabled"], 'uuid': '1518507'},
    {'check_list1': ["Maximum size of files transfered.*?changed to \[1234\]"],'check_list2':["Maximum size of files transfered.*?1234"], 'uuid': '1518508'},
    {'check_list1': ["Enable Sbox Exclusion object.*?changed to \[test_syslog\]"],'check_list2':["Enable Sbox Exclusion object.*?test_syslog"], 'uuid': '1518509'},
    {'check_list1': ["Sbox MD5 Exclusion list' , changed to \[11223344556677889900aabbccddeeff\]"],'check_list2':["Sbox MD5 Exclusion list.*?11223344556677889900aabbccddeeff"], 'uuid': '1518510'},
    {'check_list1': ["Max number for showing log view.*?changed to \[123\]"],'check_list2':["Max number for showing log view.*?123"], 'uuid': '1518511'},
    {'check_list1': ["Test Mail Settings"],'check_list2':["Test Mail Settings"], 'uuid': '1518505'},
    # 1518512 export not trigger log

) 
class Test_Capture_ATP_And_Log_01(Test):

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
        if self.uuid == '1518482':
            rc = clear_log.clear_log()
            Assertion.assert_equal(rc, True , "ERR: Clear log failed")
        elif self.uuid == '1518483':
            rc = fw_cli.do_cli_commands(commands=edit_alert_cmds1)
            Assertion.assert_equal(rc, True , "ERR: Edit Alert Level failed")
        elif self.uuid == '1518484':
            rc = fw_cli.do_cli_commands(commands=edit_attri_cmds1)
            time.sleep(8)
            Assertion.assert_equal(rc, True , "ERR: Edit Attributes of All Catetories failed")
        elif self.uuid == '1518485':
            rc = fw_cli.do_cli_commands(commands=reset_count_cmd)
            Assertion.assert_equal(rc, True , "ERR: Reset All Event Count failed")
        elif self.uuid == '1518486':
            rc = fw_cli.do_cli_commands(commands=temp_cmds)
            Assertion.assert_equal(rc, True , "ERR: save and import Template failed")
        elif self.uuid == '1518487':
            rc = fw_cli.do_cli_commands(commands=edit_category_cmds1)
            Assertion.assert_equal(rc, True , "ERR: edit category alert email failed")
        elif self.uuid == '1518488':
            rc = fw_cli.do_cli_commands(commands=edit_group_cmds1)
            Assertion.assert_equal(rc, True , "ERR: edit group alert email failed")
        elif self.uuid == '1518489':
            rc = fw_cli.do_cli_commands(commands=edit_event_cmds1)
            Assertion.assert_equal(rc, True , "ERR: edit event alert email failed")
        elif self.uuid == '1518490':
            rc = fw_cli.do_cli_commands(commands=reset_event_count)
            Assertion.assert_equal(rc, True , "ERR: Reset  Event Count  for each Entry failed")
        elif self.uuid == '1518491':
            rc = fw_cli.do_cli_commands(commands=edit_syslog_setting1)
            Assertion.assert_equal(rc, True , "ERR: Edit syslog setting failed")
        elif self.uuid == '1518492':
            rc = fw_cli.do_cli_commands(commands=cap_cmds)
            Assertion.assert_equal(rc, True , "ERR:  Enable/Disable Capture ATP failed")
        elif self.uuid == '1518493':
            rc = fw_cli.do_cli_commands(commands=add_syslog_cmds)
            Assertion.assert_equal(rc, True , "ERR:  Add Syslog Servers failed")
        elif self.uuid == '1518494':
            rc = fw_cli.do_cli_commands(commands=dis_syslog_cmds)
            Assertion.assert_equal(rc, True , "ERR:   Enable/Disable Syslog Servers failed")
        elif self.uuid == '1518495':
            rc = fw_cli.do_cli_commands(commands=edit_syslog_cmd)
            Assertion.assert_equal(rc, True , "ERR:   Modify Syslog Servers  failed")
        elif self.uuid == '1518496':
            rc = fw_cli.do_cli_commands(commands=del_syslog_cmd)
            Assertion.assert_equal(rc, True , "ERR:   Delete Syslog Servers failed")
        elif self.uuid == '1518497':
            rc = fw_cli.do_cli_commands(commands=edit_name_cmd1)
            Assertion.assert_equal(rc, True , "ERR:  Config DNS Settings failed")
        elif self.uuid == '1518498':
            rc = fw_cli.do_cli_commands(commands=reset_name_cmds)
            Assertion.assert_equal(rc, True , "ERR:  Reset Name Cache  failed")
        elif self.uuid == '1518499':
            rc = fw_cli.do_cli_commands(commands=data_collect_cmds)
            Assertion.assert_equal(rc, True , "ERR:    Start/Stop Data Collection failed")
        elif self.uuid == '1518501':
            rc = fw_cli.do_cli_commands(commands=edit_email_cmds1)
            Assertion.assert_equal(rc, True , "ERR:    Config E-mail Log Automation f failed")
        elif self.uuid == '1518502':
            rc = fw_cli.do_cli_commands(commands=edit_file_type)
            Assertion.assert_equal(rc, True , "ERR: Select/Unselect the file type f failed")
        elif self.uuid == '1518503':
            rc = fw_cli.do_cli_commands(commands=edit_mail_server1)
            Assertion.assert_equal(rc, True , "ERR: Config Mail Server Settings f failed")
        elif self.uuid == '1518504':
            rc = fw_cli.do_cli_commands(commands=edit_mail_server_adv1)
            Assertion.assert_equal(rc, True , "ERR: Config Mail Server Advanced Settings  failed")
        elif self.uuid == '1518505':
            start_mail_server.start_mail_server(mail_server_host=pc1_ip)
            rc = fw_cli.do_cli_commands(commands=test_cmds)
            Assertion.assert_equal(rc, True , "ERR: Test Settings for Mail Server failed")
        elif self.uuid == '1518506':
            rc = fw_cli.do_cli_commands(commands=edit_ftp_cmds1)
            Assertion.assert_equal(rc, True , "ERR:  Config FTP Log Automation failed")
        elif self.uuid == '1518507':
            rc = fw_cli.do_cli_commands(commands=enable_cap_cmds)
            Assertion.assert_equal(rc, True , "ERR: Makes changes in Capture ATP failed")
        elif self.uuid == '1518508':
            rc = fw_cli.do_cli_commands(commands=edit_filesize_cmds1)
            Assertion.assert_equal(rc, True , "ERR: Modify the maximum file size failed")
        elif self.uuid == '1518509':
            rc = fw_cli.do_cli_commands(commands=edit_capture_cmds1)
            Assertion.assert_equal(rc, True , "ERR: Choose AO for exlcusion failed")
        elif self.uuid == '1518510':
            rc = fw_cli.do_cli_commands(commands=md5_cmds1)
            Assertion.assert_equal(rc, True , "ERR: Config MD5 exclusion  failed")
        elif self.uuid == '1518511':
            rc = fw_cli.do_cli_commands(commands=edit_display_cmds1)
            Assertion.assert_equal(rc, True , "ERR: config Display Options failed")
        

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
        if self.uuid == '1518483' :
            rc = fw_cli.do_cli_commands(commands=edit_alert_cmds2)
            Assertion.assert_equal(rc, True , "ERR: Edit Alert Level failed")
        elif self.uuid == '1518484' :
            rc = fw_cli.do_cli_commands(commands=edit_attri_cmds2)
            Assertion.assert_equal(rc, True , "ERR: Edit Attributes of All Catetories failed")
        elif self.uuid == '1518487':
            rc = fw_cli.do_cli_commands(commands=edit_category_cmds2)
            Assertion.assert_equal(rc, True , "ERR: edit category alert email failed")
        elif self.uuid == '1518488':
            rc = fw_cli.do_cli_commands(commands=edit_group_cmds2)
            Assertion.assert_equal(rc, True , "ERR: edit group alert email failed")
        elif self.uuid == '1518489':
            rc = fw_cli.do_cli_commands(commands=edit_event_cmds2)
            Assertion.assert_equal(rc, True , "ERR: edit event alert email failed")
        elif self.uuid == '1518491':
            rc = fw_cli.do_cli_commands(commands=edit_syslog_setting2)
            Assertion.assert_equal(rc, True , "ERR: Edit syslog setting failed")
        elif self.uuid == '1518497':
            rc = fw_cli.do_cli_commands(commands=edit_name_cmd2)
            Assertion.assert_equal(rc, True , "ERR:  Config DNS Settings failed")
        elif self.uuid == '1518501':
            rc = fw_cli.do_cli_commands(commands=edit_email_cmds2)
            Assertion.assert_equal(rc, True , "ERR:    Config E-mail Log Automation f failed")
        elif self.uuid == '1518503':
            rc = fw_cli.do_cli_commands(commands=edit_mail_server2)
            Assertion.assert_equal(rc, True , "ERR: Config Mail Server Settings f failed")
        elif self.uuid == '1518504':
            rc = fw_cli.do_cli_commands(commands=edit_mail_server_adv2)
            Assertion.assert_equal(rc, True , "ERR: Config Mail Server Advanced Settings  failed")
        elif self.uuid == '1518505':
            rc = fw_cli.do_cli_commands(commands=test_clear_cmds)
            Assertion.assert_equal(rc, True , "ERR: Config Mail Settings  failed")
        elif self.uuid == '1518506':
            rc = fw_cli.do_cli_commands(commands=edit_ftp_cmds2)
            Assertion.assert_equal(rc, True , "ERR:  Config FTP Log Automation failed")
        elif self.uuid == '1518508':
            rc = fw_cli.do_cli_commands(commands=edit_filesize_cmds2)
            Assertion.assert_equal(rc, True , "ERR: Modify the maximum file size failed")
        elif self.uuid == '1518509':
            rc = fw_cli.do_cli_commands(commands=edit_capture_cmds2)
            Assertion.assert_equal(rc, True , "ERR: Choose AO for exlcusion failed")
        elif self.uuid == '1518510':
            rc = fw_cli.do_cli_commands(commands=md5_cmds2)
            Assertion.assert_equal(rc, True , "ERR: Config MD5 exclusion  failed")
        elif self.uuid == '1518511':
            rc = fw_cli.do_cli_commands(commands=edit_display_cmds2)
            Assertion.assert_equal(rc, True , "ERR: config Display Options failed")
        




