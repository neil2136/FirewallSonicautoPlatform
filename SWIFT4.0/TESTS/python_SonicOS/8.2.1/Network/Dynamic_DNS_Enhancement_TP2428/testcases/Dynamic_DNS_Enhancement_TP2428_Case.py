from definition.settings import *
from datetime import datetime
from dateutil import parser

class TestDynamic_DNS_Enhancement_TP2428_001(Test):
    uuid = "SOSAIOT-TC-51757"
    description= show_testcase_info(Parameter.TESTPLAN, '2437257', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2437257')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ddns_profile(self):
        rc = ddns_obj.add_ddns_profile(**ddns_dyn_profile)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_ddns_profile failed")

    @repeat_method(6)
    def test_02_check_ddns_file(self):
        time.sleep(10)
        flag = False
        formatted_date = get_time()
        for i in range(100):
            rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='newv4ddnsprofile')
            if str(Parameter.X1_IP) in str(rc) and str(formatted_date) in str(rc):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: test_02_check_ddns_file failed")


class TestDynamic_DNS_Enhancement_TP2428_002(Test):
    uuid = "SOSAIOT-TC-51758"
    description= show_testcase_info(Parameter.TESTPLAN, '2437258', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2437258')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_ddns_profile_name(self):
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='newv4ddnsprofile' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit test_01_edit_ddns_profile_name failed")

    def test_02_change_domain_name_and_service_type(self):
        log_obj.clear_log()
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['domain'] = 'shqa2sonicwall.dvrdns.org'
        ref['service_type'] = 'custom'
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit test_02_change_domain_name_and_service_type failed")

    def test_03_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"Configuration succeeded.*?'ddnssRadioVar1'.*?editv4ddnsprofile.*?changed to \[Custom\]",
                      r"Configuration succeeded.*?'Domain Name'.*?editv4ddnsprofile.*?changed to \[shqa2sonicwall.dvrdns.org\]"]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_04_check_ddns_file(self):
        flag = False
        formatted_date = get_time()
        for i in range(100):
            rc = ddns_obj.show_ddns_profiles_ipv4()
            if 'shqa2sonicwall.dvrdns.org' in str(rc) and "'service_type': 'custom'" in str(rc):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: test_04_check_ddns_file failed")

class TestDynamic_DNS_Enhancement_TP2428_003(Test):
    uuid = "SOSAIOT-TC-51752"
    description= show_testcase_info(Parameter.TESTPLAN, '1525311', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525311')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ddns_profile_changeip(self):
        rc = ddns_obj.add_ddns_profile(**ddns_changeip_profile)
        Assertion.assert_equal(rc, True, "ERR: test_01_add_ddns_profile_changeip failed")

    def test_02_edit_ddns_profile_name(self):
        ref = copy.deepcopy(ddns_changeip_profile)
        ref['profile_name'] = 'test22'
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='test2' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit test_02_edit_ddns_profile_name failed")

    def test_03_change_domain_name(self):
        log_obj.clear_log()
        ref = copy.deepcopy(ddns_changeip_profile)
        ref['user_name'] = 'hding@sonicwall.com'
        ref['profile_name'] = 'test22'
        ref['password'] = 'password'
        ref['domain'] = 'hding.dynamic-dns.net'
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='test22' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: Edit test_03_change_domain_name failed")

    def test_04_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"Configuration succeeded.*?'Domain Name'.*?test22.*?changed to \[hding.dynamic-dns.net\]"]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_05_check_ddns_file(self):
        flag = False
        formatted_date = get_time()
        for i in range(100):
            rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='test22')
            if 'hding.dynamic-dns.net' in str(rc) and formatted_date in str(rc):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: test_05_check_ddns_file failed")


class TestDynamic_DNS_Enhancement_TP2428_004(Test):
    uuid = "SOSAIOT-TC-51753"
    description= show_testcase_info(Parameter.TESTPLAN, '1525317', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525317')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_editprofile_Online_checkbox(self):
        log_obj.clear_log()
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['use_online'] = False
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: test_01_editprofile_Online_checkbox failed")

    def test_02_check_online_checkbox_status(self):
        rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        logger.info(rc['online'])
        Assertion.assert_equal(rc['online'], 'false', "ERR: Edit test_02_check_online_checkbox_status failed")

    def test_03_check_online_status(self):
        rc = False
        time.sleep(15)
        rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        logger.info(rc)
        check_list = [r"'Off-line: 172.17.1.168"]
        for check_str in check_list:
            if re.search(check_str,str(rc),re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: test_03_check_online_status failed")

    def test_04_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"Dynamic DNS.*?DDNS Taken Offline"]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_05_editprofile_Online_checkbox(self):
        log_obj.clear_log()
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['use_online'] = True
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: test_05_editprofile_Online_checkbox failed")

    def test_06_check_online_checkbox_status(self):
        rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        logger.info(rc['online'])
        Assertion.assert_equal(rc['online'], 'true', "ERR: test_06_check_online_checkbox_status failed")

    def test_07_check_online_status(self):
        rc = False
        time.sleep(45)
        rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        logger.info(rc)
        check_list = [r"On-line:172.17.1.168"]
        for check_str in check_list:
            if re.search(check_str,str(rc),re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: test_07_check_online_status failed")

    def test_08_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"Dynamic DNS.*?DDNS Association On-line",]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")


class TestDynamic_DNS_Enhancement_TP2428_005(Test):
    uuid = "SOSAIOT-TC-51754"
    description= show_testcase_info(Parameter.TESTPLAN, '1525318', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525318')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_editprofile_enable_checkbox(self):
        log_obj.clear_log()
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['enable'] = False
        rc = ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        Assertion.assert_equal(rc, True, "ERR: test_01_editprofile_enable_checkbox failed")

    def test_02_check_online_enable_status(self):
        rc = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        logger.info(rc['enabled'])
        Assertion.assert_equal(rc['enabled'], 'false', "ERR: test_02_check_online_enable_status failed")

    def test_03_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"Dynamic DNS.*?DDNS Association Disable"]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    @repeat_method(10)
    def test_04_editprofile_IP_manually(self):
        flag = False
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['online_settings'] = {'manual':'2.2.2.2'}
        ref['enable'] = False
        ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        max_attempts = 100
        attempts = 0
        while attempts < max_attempts:
            out = ddns_obj.get_ddns_profile_reporting(version='ipv4', name='editv4ddnsprofile')
            if '2.2.2.2' not in str(out):
                flag = True
                break
            attempts += 1
            time.sleep(1)
        
        Assertion.assert_equal(flag, True, "ERR: test_04_editprofile_IP_manually failed")

    @repeat_method(5)
    def test_05_enable_button_and_check_online_iP(self):
        log_obj.clear_log()
        flag = False
        ref = copy.deepcopy(ddns_dyn_profile)
        ref['profile_name'] = 'editv4ddnsprofile'
        ref['online_settings'] = {'manual':'2.2.2.2'}
        ddns_obj.edit_ddns_profile_name(prof_name ='editv4ddnsprofile' ,**ref)
        out = ddns_obj.get_ddns_profile_reporting(version='ipv4',name='editv4ddnsprofile')
        if "On-line: 2.2.2.2" in str(out['status']):
            flag = True 
        Assertion.assert_equal(flag, True, "ERR: test_05_enable_button_and_check_online_iP failed")

    def test_06_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"DDNS association 'shqasonicwall.dyndns.org' updated",]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")


class TestDynamic_DNS_Enhancement_TP2428_006(Test):
    uuid = "SOSAIOT-TC-51755"
    description= show_testcase_info(Parameter.TESTPLAN, '1525321', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525321')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_one_ddns_profile(self):
        log_obj.clear_log()
        ddns_obj.delete_ddns_profile(name='editv4ddnsprofile')
        rc = ddns_obj.show_ddns_profiles_ipv4()
        Assertion.assert_not_regular(str(rc), 'editv4ddnsprofile', "ERR: test_01_delete_one_ddns_profile failed")

    def test_02_check_logs(self):
        rc = False
        time.sleep(15)
        output = log_obj.export_log_txt()
        logger.info(output)
        check_list = [r"DDNS association 'shqasonicwall.dyndns.org' deleted",]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc = True
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_03_add_other_ddns_profile(self):
        ddns_obj.add_ddns_profile(**ddns_dyn_profile)
        rc = ddns_obj.show_ddns_profiles_ipv4()
        Assertion.assert_regular(str(rc), 'newv4ddnsprofile', "ERR: test_03_add_other_ddns_profile failed")

    def test_04_del_all_ddns_profile(self):
        log_obj.clear_log()
        rc = ddns_obj.delete_all_ddns_profile(name_list = ['newv4ddnsprofile','test22'])
        Assertion.assert_equal(rc, True, "ERR: Delete all ddns profile failed")

    def test_05_check_log(self):
        output = log_obj.export_log_txt()
        check_str1 = r"Configuration succeeded: Deleted 'Profile Name' , newv4ddnsprofile"
        check_str2 = r"Configuration succeeded: Deleted 'Profile Name' , test22"
        if re.search(check_str1,output,re.M) and  re.search(check_str2,output,re.M):
            rc  = True
        else:
            rc = False 
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check  log failed")


class TestDynamic_DNS_Enhancement_TP2428_007(Test):
    uuid = "SOSAIOT-TC-51756"
    description= show_testcase_info(Parameter.TESTPLAN, '1525323', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1525323')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_other_ddns_profile(self):
        ddns_obj.add_ddns_profile(**ddns_dyn_profile)
        rc = ddns_obj.show_ddns_profiles_ipv4()
        Assertion.assert_regular(str(rc), 'newv4ddnsprofile', "ERR: test_01_add_other_ddns_profile failed")

    @repeat_method(10)
    def test_02_check_ping_valid_domain(self):
        cmd = 'ping {} -w 3 '.format(ddns_dyn_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = os.popen(cmd).read()
            logger.info(out)
            if '100% packet loss' not in str(out) and Parameter.X1_IP in str(out):
                logger.info('Send ping from pc1 to domain success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")

    def test_03_check_ping_invalid_domain(self):
        cmd = 'ping {} -w 3 '.format(ddns_noip_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = os.popen(cmd).read()
            logger.info(out)
            if '100% packet loss' not in str(out) and Parameter.X1_IP in str(out):
                logger.info('Send ping from pc1 to domain failed.')
                rc = False
                break
            elif i == 9:
                logger.info('Ping successly.')
                rc = True
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")


def get_time():
    rc = time_obj.show_time()
    date_str = rc['time']['date']
    date_obj = datetime.strptime(date_str, '%Y:%m:%d')
    formatted_date = date_obj.strftime('%m/%d/%Y')
    return formatted_date