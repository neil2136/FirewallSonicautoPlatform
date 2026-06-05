from definition.settings import *


# TC01 Enable Filename Logging
class TC001_Enable_Filename_Logging(Test):
    uuid = "SOSAIOT-TC-54740"

    def test_01_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519927')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": False,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC02 Disable Filename Logging
class TC002_Disable_Filename_Logging(Test):
    uuid = "SOSAIOT-TC-54751"

    def test_02_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519938')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_Step00_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC009 File name can be logged for http protocol
class TC009_Verify_filename_logging_http_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54767"

    def test_009_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519955')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_009_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_009_Step02_generate_http_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('wget http://' + PC2_ETH1_IP + '/test.html -O /tmp/wan_index.html --no-check-certificate')
        time.sleep(3)
        out1 = PC1_login.system("cat /tmp/wan_index.html").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")

    def test_009_Step03_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "test.html"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "test.html"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_009_Step04_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC03 Verify filename logging http protocol event log
class TC003_Verify_filename_logging_http_protocol_event_log(Test):
    uuid = "SOSAIOT-TC-54761"

    def test_003_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519949')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_003_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_003_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_003_Step03_generate_http_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('wget http://' + PC2_ETH1_IP + '/test.html -O /tmp/wan_index.html --no-check-certificate')
        time.sleep(3)
        out1 = PC1_login.system("cat /tmp/wan_index.html").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")

    def test_003_Step04_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: test.html"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_003_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC27 Restart the FW verify it works after it's up
class TC027_Verify_app_control_filename_post_restart(Test):
    uuid = "SOSAIOT-TC-54759"

    def test_027_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519946')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_027_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_027_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_027_Step03_reboot_fw(self):
        rc = restart_obj.restart_now()
        Assertion.assert_equal(rc, True, "ERR: restart fw failed")

    def test_027_Step04_check_settings(self):
        resp = appcontrolapi.get_appcontrol_setting()
        flag = False
        logger.info('=> check app control settings')
        resp_json = json.dumps(resp)
        check_list = ['"enable": true', '"log_all": true', '"log_filename": true']
        if all(item in resp_json for item in check_list):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check settings failed")

    def test_027_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC29 Verify 'Enable Filename Logging' is recorded
class TC029_Verify_tsr_Enable_Filename_Logging(Test):
    uuid = "SOSAIOT-TC-54760"

    def test_029_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519948')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_029_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_029_Step02_download_tsr(self):
        rc = system_api.download_tsr()
        logger.info(rc)
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

    def test_029_Step03_verify_tsr_for_app_filename_logging_enable(self):
        flag = False
        if os.path.exists("/tmp/techSupport"):
            tsr_content = os.popen('cat /tmp/techSupport').read()
            pattern = r"--App Control Advanced--(.*?)--App Control Categories--"
            match = re.search(pattern, tsr_content, re.DOTALL)
            if match:
                captured_text = match.group(1).strip()
                logger.info("##########################")
                logger.info(captured_text)
                logger.info("##########################")
                if "Enable App Control                  : Enabled" in captured_text:
                    flag = True
            else:
                logger.info("Not found the target tsr content part")
        else:
            logger.info("download tsr file failed")
        Assertion.assert_equal(flag, True, "ERR: Verify tsr failed")

    def test_029_Step04_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC010 File name can be logged for FTP protocol in syslog
class TC010_Verify_filename_logging_ftp_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54741"

    def test_010_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519928')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_010_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_010_Step02_set_logging_interval(self):
        default_global_cate = {
            "log": {
                "categories": {
                    "logging_level": "debug",
                    "alert_level": "alert"
                }
            }
        }
        rc = log_cat_api.config_global_categories(**default_global_cate)
        Assertion.assert_equal(rc, True, "ERR: config global categories failed")

    def test_010_Step03_enable_debug_log_for_ftp(self):
        resp = logsetting_api.enable_event(**application_control_detection)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        resp = logsetting_api.enable_event(**application_control_prevention)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        resp = logsetting_api.enable_event(**filename_logging_log_ftp)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_010_Step04_generate_ftp_traffic_lan_wan(self):
        my_ftp_v4.login()
        output = my_ftp_v4.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_010_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('tail -30 /var/log/messages')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "/var/www/html/virus/test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_010_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC04 Verify File name can be logged for ftp protocol in Event log
class TC004_Verify_filename_logging_ftp_protocol_event_log(Test):
    uuid = "SOSAIOT-TC-54762"

    def test_004_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519950')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_004_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_004_Step02_enable_inform_log_for_ftp(self):
        resp = logsetting_api.enable_event(**application_control_detection)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        resp = logsetting_api.enable_event(**application_control_prevention)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

        resp = logsetting_api.enable_event(**filename_logging_log_ftp)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_004_Step03_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_004_Step04_generate_ftp_traffic_lan_wan(self):
        my_ftp_v4.login()
        output = my_ftp_v4.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_004_Step05_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: /var/www/html/virus/test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_004_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC15 IPv6: Verify File name can be logged for http protocol in Event log
class TC015_Verify_filename_logging_http_protocol_event_log_ipv6(Test):
    uuid = "SOSAIOT-TC-54746"

    def test_015_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519933')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_015_Step02_enable_debug_log_for_http(self):
        resp = logsetting_api.enable_event(**filename_logging_log_http)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_015_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_015_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_015_Step03_generate_http_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('wget http://[' + PC2_ETH1_IPV6 + ']/test.html -O /tmp/wan_index.html --no-check-certificate')
        time.sleep(3)
        out1 = PC1_login.system("cat /tmp/wan_index.html").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")

    def test_015_Step04_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: test.html"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_015_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC009 IPv6: Verify File name can be logged for http protocol in syslog server(server in WAN zone)
class TC021_Verify_filename_logging_http_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54753"

    def test_021_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519940')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_021_Step01_enable_debug_log_for_http(self):
        resp = logsetting_api.enable_event(**filename_logging_log_http)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_021_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_021_Step03_generate_http_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('wget http://[' + PC2_ETH1_IPV6 + ']/test.html -O /tmp/wan_index.html --no-check-certificate')
        time.sleep(3)
        out1 = PC1_login.system("cat /tmp/wan_index.html").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")

    def test_021_Step04_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "test.html"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "test.html"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_021_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC022 File name can be logged for FTP protocol in syslog
class TC022_Verify_filename_logging_ftp_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54754"

    def test_022_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519941')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_022_Step01_enable_inform_log_for_ftp(self):
        resp = logsetting_api.enable_event(**filename_logging_log_ftp)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_022_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_022_Step03_enable_alert_log_for_app_control_filename(self):
        resp = logsetting_api.enable_event(**filename_logging_log_ftp)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_022_Step04_generate_ftp_traffic_lan_wan(self):
        my_ftp_v6.login()
        output = my_ftp_v6.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_022_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('tail -30 /var/log/messages')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "/var/www/html/virus/test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_022_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC16 Verify File name can be logged for ftp protocol in Event log
class TC016_Verify_filename_logging_ftp_protocol_event_log_ipv6(Test):
    uuid = "SOSAIOT-TC-54747"

    def test_016_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519934')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_016_Step01_enable_inform_log_for_ftp(self):
        resp = logsetting_api.enable_event(**filename_logging_log_ftp)
        Assertion.assert_equal(resp, True, "ERR: enable log event failed")

    def test_016_Step02_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_016_Step03_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_016_Step04_generate_ftp_traffic_lan_wan(self):
        my_ftp_v6.login()
        output = my_ftp_v6.download_file(localfile, remotefile)
        Assertion.assert_equal(output, True, 'ERR: check ftp traffic failed')

    def test_016_Step05_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: /var/www/html/virus/test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_016_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC012 File name can be logged for smtp protocol
class TC012_Verify_filename_logging_smtp_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54743"

    def test_012_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519930')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_012_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_016_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_012_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_012_Step04_get_email(self):
        logger.info('Fetching email with POP3 protocol.....')
        received_mail = get_mail_pop3('12.12.1.169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_012_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS SMTP"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_012_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC013 File name can be logged for pop3 protocol
class TC013_Verify_filename_logging_pop3_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54744"

    def test_013_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519931')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_013_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_013_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_013_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_013_Step04_get_email(self):
        logger.info('Fetching email with POP3 protocol.....')
        received_mail = get_mail_pop3('12.12.1.169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_013_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS POP3"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_013_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC014 File name can be logged for imap protocol
class TC014_Verify_filename_logging_imap_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54745"

    def test_014_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519932')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_014_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_014_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_014_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_014_Step04_get_email(self):
        logger.info('Fetching email with IMAP protocol.....')
        received_mail = get_mail_imap('12.12.1.169', 'sahil', 'password')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_014_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS IMAP"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_014_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC006 Verify filename logging http protocol event log
class TC006_Verify_filename_logging_smtp_protocol_eventlog(Test):
    uuid = "SOSAIOT-TC-54764"

    def test_006_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519952')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_006_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_006_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_006_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_006_Step04_get_email(self):
        received_mail = get_mail_pop3('12.12.1.169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_006_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS SMTP"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_006_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC007 Verify filename logging pop3 protocol event log
class TC007_Verify_filename_logging_pop3_protocol_eventlog(Test):
    uuid = "SOSAIOT-TC-54765"

    def test_007_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519953')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_007_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_007_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_007_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_007_Step04_get_email(self):
        received_mail = get_mail_pop3('12.12.1.169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_007_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS POP3"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_007_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC008 Verify filename logging imap protocol event log
class TC008_Verify_filename_logging_imap_protocol_eventlog(Test):
    uuid = "SOSAIOT-TC-54766"

    def test_008_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519954')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_008_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_008_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_008_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_008_Step04_get_email(self):
        received_mail = get_mail_imap('12.12.1.169', 'sahil', 'password')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_008_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS IMAP"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_008_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC018 IPv6:Verify File name can be logged for SMTP protocol in Event log
class TC018_Verify_filename_logging_smtp_protocol_eventlog_ipv6(Test):
    uuid = "SOSAIOT-TC-54749"

    def test_018_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519936')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_018_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_018_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('2001::169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_018_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="2001::169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_018_Step04_get_email(self):
        received_mail = get_mail_pop3('2001::169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_018_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS SMTP"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_018_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC019 IPv6: Verify File name can be logged for POP3 protocol in Event log
class TC019_Verify_filename_logging_pop3_protocol_eventlog_ipv6(Test):
    uuid = "SOSAIOT-TC-54750"

    def test_019_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519937')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_019_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_019_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('2001::169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_019_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="2001::169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_019_Step04_get_email(self):
        received_mail = get_mail_pop3('2001::169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_019_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS POP3"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_019_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC020 IPv6: Verify File name can be logged for IMAP protocol in Event log
class TC020_Verify_filename_logging_imap_protocol_eventlog_ipv6(Test):
    uuid = "SOSAIOT-TC-54752"

    def test_020_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519939')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_020_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_020_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('2001::169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_020_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="2001::169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_020_Step04_get_email(self):
        received_mail = get_mail_imap('2001::169', 'sahil', 'password')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_020_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "PROTOCOLS IMAP"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_020_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC024 IPv6: Verify File name can be logged for SMTP protocol in syslog server
class TC024_Verify_filename_logging_smtp_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54756"

    def test_024_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519943')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_024_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_024_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('2001::169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_024_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="2001::169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_024_Step04_get_email(self):
        logger.info('Fetching email with POP3 protocol.....')
        received_mail = get_mail_pop3('2001::169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_024_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS SMTP"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_024_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC013 File name can be logged for pop3 protocol
class TC013_Verify_filename_logging_pop3_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54757"

    def test_013_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519944')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_013_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_013_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_013_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_013_Step04_get_email(self):
        logger.info('Fetching email with POP3 protocol.....')
        received_mail = get_mail_pop3('12.12.1.169', 'sahil')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_013_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS POP3"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_013_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC014 File name can be logged for imap protocol
class TC014_Verify_filename_logging_imap_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54758"

    def test_014_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519945')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_014_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_014_Step02_Clear_test1_inbox(self):
        try:
            ret = delete_email('12.12.1.169', 'sahil', 'password')
            time.sleep(10)
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_014_Step03_generate_smtp_traffic_lan_wan(self):
        logger.info('Sending email with SMTP protocol.....')
        attachment = ['/tmp/test.txt']
        rc = send_mail_smtps_or_starttls(
            server="12.12.1.169",
            mail_from="root@sonicauto.com",
            mail_to="sahil@sahil.com",
            mail_subject="test subject",
            mail_content="test content",
            mail_attach=attachment
        )
        Assertion.assert_equal(rc[0], True, "ERR: send email failed")

    def test_014_Step04_get_email(self):
        logger.info('Fetching email with IMAP protocol.....')
        received_mail = get_mail_imap('12.12.1.169', 'sahil', 'password')
        logger.info('8' * 60)
        logger.info(f'this is email resp {received_mail}')
        logger.info('8' * 60)

    def test_014_Step05_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "PROTOCOLS IMAP"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Application Control Detection Alert"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_014_Step06_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC011 Verify File name can be logged for NetBios/CIFS protocol in syslog server
class TC011_Verify_filename_logging_NetBios_protocol_syslog(Test):
    uuid = "SOSAIOT-TC-54742"

    def test_011_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519929')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_011_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_011_Step02_generate_smb_traffic_lan_wan(self):
        PC1_login.system('smbclient //12.12.1.169/shared_sbharaj -U sambauser%Sonicauto -c "get test.txt"')
        time.sleep(3)
        out1 = PC1_login.system("cat /root/test.txt").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")
        flag = True if "CONTENT FROM SHARED DIRECTORY OVER SMB PROTOCOL" in out1 else False
        Assertion.assert_equal(flag, True, "ERR: Unable to fetch file through SMB")

    def test_011_Step03_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "Filename"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Filename: test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_011_Step04_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC17 IPv6: Verify File name can be logged for NetBios/CIFS protocol in Event log
class TC017_Verify_filename_logging_NetBios_protocol_event_log_ipv6(Test):
    uuid = "SOSAIOT-TC-54748"

    def test_017_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519935')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_017_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_017_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_017_Step03_generate_smb_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('smbclient //2001::169/shared_sbharaj -U sambauser%Sonicauto -c "get test.txt"')
        time.sleep(3)
        out1 = PC1_login.system("cat /root/test.txt").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")
        flag = True if "CONTENT FROM SHARED DIRECTORY OVER SMB PROTOCOL" in out1 else False
        Assertion.assert_equal(flag, True, "ERR: Unable to fetch file through SMB")

    def test_017_Step04_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_017_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")


# TC023 IPv6: Verify File name can be logged for NetBios/CIFS protocol in syslog server
class TC023_Verify_filename_logging_NetBios_protocol_syslog_ipv6(Test):
    uuid = "SOSAIOT-TC-54755"

    def test_023_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519942')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_023_Step01_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_023_Step02_generate_smb_traffic_lan_wan(self):
        PC1_login.system('smbclient //2001::169/shared_sbharaj -U sambauser%Sonicauto -c "get test.txt"')
        time.sleep(3)
        out1 = PC1_login.system("cat /root/test.txt").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")
        flag = True if "CONTENT FROM SHARED DIRECTORY OVER SMB PROTOCOL" in out1 else False
        Assertion.assert_equal(flag, True, "ERR: Unable to fetch file through SMB")

    def test_023_Step03_verify_syslog_for_app_control_filename_logging(self):
        flag = False
        time.sleep(3)
        output = PC2_login.send_command('cat /var/log/messages | grep "Filename"')
        logger.info("########################")
        logger.info(output)
        logger.info("########################")
        match_string = "Filename: test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check syslog failed")

    def test_023_Step04_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Disable App Control And Filename Logging")


# TC005 Verify File name can be logged for NetBios/CIFS protocol in Event log
class TC005_Verify_filename_logging_NetBios_protocol_event_log(Test):
    uuid = "SOSAIOT-TC-54763"

    def test_005_Step00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1519951')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_005_Step01_Clear_Log(self):
        rc = log_api.clear_log()
        time.sleep(3)
        rc = log_cat_api.enable_all_log_category()
        Assertion.assert_equal(True, True, "ERR: Clear log failed")

    def test_005_Step02_Enable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": True,
            "log_all": True,
            "log_filename": True,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")

    def test_005_Step03_generate_smb_traffic_lan_wan(self):
        PC1_login.system('rm -rf /tmp/wan_index.html')
        PC1_login.system('smbclient //12.12.1.169/shared_sbharaj -U sambauser%Sonicauto -c "get test.txt"')
        time.sleep(3)
        out1 = PC1_login.system("cat /root/test.txt").decode()
        logger.info("################")
        logger.info(out1)
        logger.info("################")
        flag = True if "CONTENT FROM SHARED DIRECTORY OVER SMB PROTOCOL" in out1 else False
        Assertion.assert_equal(flag, True, "ERR: Unable to fetch file through SMB")

    def test_005_Step04_verify_event_log_for_app_control_filename_logging(self):
        flag = True
        time.sleep(3)
        output = log_api.export_log_txt(log_switch=False)
        logger.info('===================== LOG START======================')
        logger.info(output)
        logger.info('===================== LOG END ======================')
        match_string = "Filename: test.txt"
        flag = True if (match_string in output) else False
        Assertion.assert_equal(flag, True, "ERR: check event logs failed")

    def test_005_Step05_Disable_App_Control_And_Logging(self):
        app_control_global = {
            "enable": False,
            "log_all": False,
            "log_filename": False,
            "log_redundancy": 60,
        }
        resp = appcontrolapi.config_appcontrol_global(**app_control_global)
        Assertion.assert_equal(resp, True, "ERR: Failed To Enable App Control And Filename Logging")