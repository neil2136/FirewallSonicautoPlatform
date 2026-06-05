from definition.settings import *


class Test_01_Add_profile_01(Test):
    """
    1. insure no ddns profiles at first.
    2. add one dyn ddns profile.
    3. verify the ddns profile added successfully and online.
    4. delete the dns proflie
    """
    uuid = "SOSAIOT-TC-51369"
    description = show_testcase_info(Parameter.TESTPLAN, "1525128", description=True)['title']

    def test_01_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525128')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_ddns_profile_dyn(self):
        log_obj.clear_log()
        rc = ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
        logger.info(rc)
        for i in range(7):
            logger.info(f'add profile time {i+1}')
            time.sleep(10)
            output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name=Parameter.ddns_dyn_profile['profile_name'])
            if output['status'] is None or 'On-line:13.0.0.168' not in (output['status']).replace(' ',''):
              rc &=  ddnsApi.delete_ddns_profile(version='ipv4',name=Parameter.ddns_dyn_profile['profile_name'])
              rc &= ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
            else:
                break
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")
    
    def test_01_02_check_log(self):
        rc = True
        time.sleep(15)
        output = log_obj.export_log_txt()
        check_list = [r"Configuration succeeded.*?Domain Name.*?test1.*?shqasonicwall.dyndns.org",
                      r"DDNS Update success for domain 'shqasonicwall.dyndns.org'. Online IP updated"]
        for check_str in check_list:
            if re.search(check_str,output,re.M):
                rc  &= True
            else:
                rc &= False 
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def test_01_03_check_ddns_profile_ip(self):
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name=Parameter.ddns_dyn_profile['profile_name'])
        if 'On-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check ip failed")
    
    @repeat_method(3)
    def test_01_04_check_ping(self):
        time.sleep(5)
        cmd = 'ping {} -w 3 '.format(Parameter.ddns_dyn_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to domain success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")

    @repeat_method(3)
    def test_01_05_check_domain_resolved_to_right_ip(self):
        time.sleep(3)
        cmd = f"nslookup {Parameter.ddns_dyn_profile['domain']}"
        out = PC1.send_command(cmd)
        logger.info(out)
        if Parameter.x1_static_opt['ip'] in out:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check domain resolved to right ip failed")

    def test_01_06_edit_ddns_invalid(self):  
        log_obj.clear_log()
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        ref['user_name'] = 'user'
        rc = ddnsApi.edit_ddns_profile(**ref)
        Assertion.assert_equal(rc, True, "ERR: edit invalid user ddns profiles failed")

    def test_01_07_check_invalid_log(self):
        time.sleep(35)
        output = log_obj.export_log_txt()
        check_str = r"DDNS Failure: Provider  'dyn.com' reports"
        if re.search(check_str,output,re.M):
            rc  = True
        else:
            rc = False 
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check invalid log failed")

    def test_01_08_check_invalid_ddns_profile_status(self):
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name=Parameter.ddns_dyn_profile['profile_name'])
        if 'invalid account' in output['status'] or  'Network error' in output['status']:
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check invalid ddns profile status failed")
    
    def test_01_09_delete_added_ddns_profile(self):
        output = ddnsApi.delete_ddns_profile(version='ipv4',name=Parameter.ddns_dyn_profile['profile_name'])
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: the ddns profile isn't deleted")


class Test_02_Delete_Association_Profile_02(Test):
    
    uuid = "SOSAIOT-TC-51372"
    description = show_testcase_info(Parameter.TESTPLAN, "1525132", description=True)['title']

    def test_02_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525132')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_add_ddns_profile(self):
        rc = ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
        rc &= ddnsApi.add_ddns_profile(**Parameter.ddns_changeip_profile)
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")

    def test_02_02_del_all_ddns_profile(self):
        log_obj.clear_log()
        rc = ddnsApi.delete_all_ddns_profile(name_list = ['test1','test2'])
        Assertion.assert_equal(rc, True, "ERR: Delete all ddns profile failed")

    def test_02_03_check_log(self):
        output = log_obj.export_log_txt()
        check_str1 = r"Configuration succeeded: Deleted 'Profile Name' , test1"
        check_str2 = r"Configuration succeeded: Deleted 'Profile Name' , test2"
        if re.search(check_str1,output,re.M) and  re.search(check_str2,output,re.M):
            rc  = True
        else:
            rc = False 
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check  log failed")


class Test_03_Edit_Update_profile_03(Test):
    uuid = "SOSAIOT-TC-51373"
    description = show_testcase_info(Parameter.TESTPLAN, "1525133", description=True)['title']

    def test_03_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525133')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_add_ddns_profile_dyn(self):
        rc = ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
        logger.info(rc)
        for i in range(7):
            logger.info(f'add profile time {i+1}')
            time.sleep(10)
            output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name=Parameter.ddns_dyn_profile['profile_name'])
            if output['status'] is None or 'On-line:13.0.0.168' not in (output['status']).replace(' ',''):
              rc &=  ddnsApi.delete_ddns_profile(version='ipv4',name=Parameter.ddns_dyn_profile['profile_name'])
              rc &= ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
            else:
                break
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")

    def test_03_02_edit_ddns_profile_dyn_name(self):
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        ref['profile_name'] = 'test_update'
        output = ddnsApi.edit_ddns_profile_name(prof_name ='test1' ,**ref)
        Assertion.assert_equal(output, True,"ERR: edit ddns profile name failed")
    
    def test_03_03_check_edited_ddns_profile_status(self):
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test_update')
        if 'On-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check ip failed")
    
    def test_03_04_check_ping(self):
        cmd = 'ping {} -w 3 '.format(Parameter.ddns_dyn_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to domain success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")

    @repeat_method(5)
    def test_03_05_edit_ddns_profile_ipand_check_status(self):
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        ref['profile_name'] = 'test_update'
        ref['online_settings'] = {'manual':'13.0.0.168'}
        rc = ddnsApi.edit_ddns_profile(**ref)
        time.sleep(20)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test_update')
        if 'On-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc &= True
        else:
            rc &= False
        logger.info(output)
        Assertion.assert_equal(rc, True,"ERR: edit ddns profile name and check status  failed")
    
    def test_03_06_check_ping(self):
        time.sleep(25)
        cmd = 'ping {} -w 3 '.format(Parameter.ddns_dyn_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to domain success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")
    
    @repeat_method(5)
    def test_03_07_edit_ddns_profile_invalid_ip_and_check_status(self):
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        ref['profile_name'] = 'test_update'
        ref['online_settings'] = {'manual':'13.0.0.166'}
        rc = ddnsApi.edit_ddns_profile(**ref)
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test_update')
        if 'On-line:13.0.0.166' in (output['status']).replace(' ',''):
            rc &= True
        else:
            rc &= False
        logger.info(output)
        Assertion.assert_equal(rc, True,"ERR: edit ddns profile name and check status failed")
    
    def test_03_08_delete_added_ddns_profile(self):
        output = ddnsApi.delete_ddns_profile(version='ipv4', name='test_update')
        Assertion.assert_equal(output, True, "ERR: the ddns profile isn't deleted")


class Test_04_Edit_Update_profile_09(Test):

    uuid = "SOSAIOT-TC-51374"
    description = show_testcase_info(Parameter.TESTPLAN, "1525135", description=True)['title']

    def test_04_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525135')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_add_ddns_profile_dyn(self):
        rc = ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
        logger.info(rc)
        for i in range(7):
            logger.info(f'add profile time {i+1}')
            time.sleep(10)
            output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name=Parameter.ddns_dyn_profile['profile_name'])
            if output['status'] is None or 'On-line:13.0.0.168' not in (output['status']).replace(' ',''):
              rc &=  ddnsApi.delete_ddns_profile(version='ipv4',name=Parameter.ddns_dyn_profile['profile_name'])
              rc &= ddnsApi.add_ddns_profile(**Parameter.ddns_dyn_profile)
            else:
                break
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")

    def test_04_02_check_edited_ddns_profile_status(self):
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test1')
        if 'On-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check ip failed")

    @repeat_method(5)
    def test_04_03_edit_ddns_profile_ip_and_check_status(self):
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        ref['online_settings'] = {'manual':'13.0.0.166'}
        rc = ddnsApi.edit_ddns_profile(**ref)
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test1')
        if 'On-line:13.0.0.166' in (output['status']).replace(' ',''):
            rc &= True
        else:
            rc &= False
        logger.info(output)
        Assertion.assert_equal(rc, True,"ERR: edit ddns profile name and check status failed")

    @repeat_method(3)
    def test_04_04_edit_ddns_profile_invalid_ip_and_check_status(self):
        ref = copy.deepcopy(Parameter.ddns_dyn_profile)
        rc = ddnsApi.edit_ddns_profile(**ref)
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test1')
        if 'On-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc &= True
        else:
            rc &= False
        logger.info(output)
        Assertion.assert_equal(rc, True,"ERR: edit ddns profile name and check status failed")

    def test_04_05_delete_added_ddns_profile(self):
        output = ddnsApi.delete_ddns_profile(version='ipv4', name='test1')
        Assertion.assert_equal(output, True, "ERR: the ddns profile isn't deleted")


class Test_05_changeip_ddns_profile_11(Test):

    uuid = "SOSAIOT-TC-51370"
    description = show_testcase_info(Parameter.TESTPLAN, "1525129", description=True)['title']

    def test_05_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525129')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_add_ddns_profile_changeip(self):
        ref = copy.deepcopy(Parameter.ddns_changeip_profile)
        ref['use_online'] =  True
        rc = ddnsApi.add_ddns_profile(**ref)
        time.sleep(10)
        rc &= ddnsApi.edit_ddns_profile(**Parameter.ddns_changeip_profile)
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")

    @repeat_method(3)
    def test_05_02_check_ddns_profile_status(self):
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test2')
        if 'Off-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check ip failed")
    
    def test_05_03_check_ping(self):
        PC1.send_command('ifconfig eth1 1.1.1.9')
        cmd = 'ping {} -w 3 '.format(Parameter.ddns_changeip_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss'  in str(out) and '13.0.0.168' in str(out) :
                rc = True
                break
            elif i == 9:
                rc = False
        PC1.send_command('ifconfig eth1 13.0.0.200')
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")

    def test_05_04_delete_ddns_profile(self):
        output = ddnsApi.delete_ddns_profile(version='ipv4', name='test2')
        Assertion.assert_equal(output, True, "ERR: the ddns profile isn't deleted")


class Test_06_changeip_ddns_profile_12(Test):

    uuid = "SOSAIOT-TC-51371"
    description = show_testcase_info(Parameter.TESTPLAN, "1525130", description=True)['title']

    def test_06_00_show_testplan(self):
        show_testcase_info(Parameter.TESTPLAN, '1525130')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_add_ddns_profile_changeip(self):
        ref = copy.deepcopy(Parameter.ddns_changeip_profile)
        ref1 = copy.deepcopy(Parameter.ddns_changeip_profile)
        ref['use_online'] =  True
        rc = ddnsApi.add_ddns_profile(**ref)
        time.sleep(10)
        ref1['offline_settings'] = {'manual':'13.0.0.168'}
        rc &= ddnsApi.edit_ddns_profile(**ref1)
        Assertion.assert_equal(rc, True, "ERR: Add ddns profile failed")

    def test_06_02_check_ddns_profile_status(self):
        time.sleep(15)
        output = ddnsApi.get_ddns_profile_reporting(version='ipv4', name='test2')
        if 'Off-line:13.0.0.168' in (output['status']).replace(' ',''):
            rc = True
        else:
            rc = False
        logger.info(output)
        Assertion.assert_equal(rc, True, "ERR: check ip failed")

    def test_06_03_check_ping(self):
        cmd = 'ping {} -w 3 '.format(Parameter.ddns_changeip_profile['domain'])
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss'  not in str(out) and '13.0.0.168' in str(out) :
                rc = True
                break
            elif i == 9:
                rc = False
        Assertion.assert_equal(rc, True, "ERR: Send ping from pc1 to domain failed")

    def test_06_04_delete_ddns_profile(self):
        output = ddnsApi.delete_ddns_profile(version='ipv4', name='test2')
        Assertion.assert_equal(output, True, "ERR: the ddns profile isn't deleted")



