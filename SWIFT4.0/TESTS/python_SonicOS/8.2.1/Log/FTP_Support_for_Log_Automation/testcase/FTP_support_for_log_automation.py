from time import sleep
from definition.init_param import *
from definition.download_and_upload_file import *


@repeat_class(3)
class ftp_support_for_log_automation_1513024(Test):
    uuid = '1513024'
    description = show_testcase_info(Parameter.TESTPLAN, '1513024', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513024')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_02_start_traffic_and_check_Log(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
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
                            "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
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
                                "plain_text":True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: config_ftp_automation failed")
        sleep(70)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log failed")

    def test_00_03_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), ' ', "ERR: check log failed")


@repeat_class(3)
class ftp_support_for_log_automation_1513025(Test):
    uuid = '1513025'
    description = show_testcase_info(Parameter.TESTPLAN, '1513025', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513025')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_02_start_traffic_and_check_log(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
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
                            "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
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
                                "plain_text":True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: config_ftp_automation failed")
        sleep(70)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log failed")

    def test_00_03_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), ' ', "ERR: check log")


class ftp_support_for_log_automation_1513028(Test):
    uuid = '1513028'
    description = show_testcase_info(Parameter.TESTPLAN, '1513028', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513028')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_02_start_traffic_and_check_log(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
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
                            "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
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
                                "plain_text":True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: test_00_01_config_ftp_automation")
        sleep(70)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log")

    def test_00_03_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.txt', "ERR: check ftp log")


class ftp_support_for_log_automation_1513029(Test):
    uuid = '1513029'
    description = show_testcase_info(Parameter.TESTPLAN, '1513029', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513029')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                            "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
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
                                "html":True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: test_00_01_config_ftp_automation")
    
    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_start_traffic_and_check_log(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
        sleep(60)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log")

    def test_00_04_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.html', "ERR: check ftp log")


class ftp_support_for_log_automation_1513030(Test):
    uuid = '1513030'
    description = show_testcase_info(Parameter.TESTPLAN, '1513030', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513030')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                                "attachment":{
                                "csv":True
                            }
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: test_00_01_config_ftp_automation failed")
    
    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_start_traffic(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
        sleep(60)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log failed")

    def test_00_04_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.csv', "ERR: check csv log failed")


class ftp_support_for_log_automation_1513033(Test):
    uuid = '1513033'
    description = show_testcase_info(Parameter.TESTPLAN, '1513033', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513033')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_try_to_download_tsr(self):
        system_obj.download_tsr()
        rc = localhost.send_command("ls /tmp | grep techSupport")
        Assertion.assert_regular(str(rc), 'techSupport', "ERR: test_00_01_try_to_download_tsr failed")

    def test_00_02_check_config(self):
        rc = localhost.send_command("cat /tmp/techSupport")
        logger.info(rc)
        Assertion.assert_regular(rc, '--FTP Log Automation--[\s\S]*Send Log to FTP[\s\S]*Enabled[\s\S]*FTP Server[\s\S]*192.168.13.200[\s\S]*Username[\s\S]*root[\s\S]*Directory[\s\S]*\/tmp\/ftp_log[\s\S]*Send Log Daily at 3:0 \(24-Hour Format\)[\s\S]*File Format[\s\S]*CSV Attachment', "ERR: test_00_02_check_config")

    
class ftp_support_for_log_automation_1513035(Test):
    uuid = '1513035'
    description = show_testcase_info(Parameter.TESTPLAN, '1513035', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513035')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_change_X3_to_LAN(self):
        logger.info('config X3 interface...')
        x3 = {
            'if': 'X3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv4.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(60)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.csv', "ERR: test_00_03_check_log")

    def test_00_04_change_X3_to_LAN(self):
        logger.info('config X3 interface...')
        x3 = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': '255.255.255.0',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = interface_ipv4.config_interface(**x3)
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPv4 failed")

    def test_00_05_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_06_check_log(self):
        sleep(60)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.csv', "ERR: test_00_06_check_log")


class ftp_support_for_log_automation_1513037(Test):
    uuid = '1513037'
    description = show_testcase_info(Parameter.TESTPLAN, '1513037', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513037')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_reboot(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, "ERR: show testcase info failed")

    def test_00_02_check_config(self):
        rc = log_automation.show_log_automation()
        logger.info(rc)
        Assertion.assert_regular(str(rc), """ftp_log.*send_log_to_ftp.*server.*192.168.13.200.*user_name.*root.*directory.*\/tmp\/ftp_log.*daily.*hour': 3, 'minute': 0.*file_format.*csv""", "ERR: test_00_02_check_config")


class ftp_support_for_log_automation_1513041(Test):
    uuid = '1513041'
    description = show_testcase_info(Parameter.TESTPLAN, '1513041', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513041')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                            "send_log_to_ftp": False, 
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation failed")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_start_traffic(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
        sleep(60)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_not_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log")

    def test_00_04_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), '\.txt', "ERR: check log failed")


class ftp_support_for_log_automation_1513043(Test):
    uuid = '1513043'
    description = show_testcase_info(Parameter.TESTPLAN, '1513043', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513043')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation failed")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:58:00",
                "date": "2023:03:30",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        log_obj.clear_log()
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(120)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), ' ', "ERR: check log failed")

    def test_00_04_set_dut_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_05_check_log(self):
        sleep(70)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.txt', "ERR: check log failed")

    def test_00_06_compare_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/").split("\n")
        file1 = f"/tmp/ftp_log/{rc[0]}"
        file2 = f"/tmp/ftp_log/{rc[1]}"
        ftp_download(hostname = "192.168.13.200", username = "root",password = "password",local_file_name = rc[0],remote_file_name = rc[0])
        ftp_download(hostname = "192.168.13.200", username = "root",password = "password",local_file_name = rc[1],remote_file_name = rc[1])
        print(file1,file2)
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            lines1 = set(f1.readlines()[1:])
            lines2 = set(f2.readlines()[1:])
        if lines1.intersection(lines2):
            rc = True
        else:
            rc =False
        Assertion.assert_equal(rc, False, "ERR: test_00_06_compare_log failed")


class ftp_support_for_log_automation_1513044(Test):
    uuid = '1513044'
    description = show_testcase_info(Parameter.TESTPLAN, '1513044', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513044')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_change_log_dir(self):
        mail_server.send_command("mkdir /var/www/html/tmp")
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
                            "directory": "/var/www/html/tmp", 
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
        Assertion.assert_equal(rc, True, "ERR: test_00_01_change_log_dir failed")

    def test_00_02_set_dut_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(70)
        rc = mail_server.send_command("ls /var/www/html/tmp")
        Assertion.assert_regular(str(rc), '\.txt', "ERR: test_00_03_check_log")


class ftp_support_for_log_automation_1513046(Test):
    uuid = '1513046'
    description = show_testcase_info(Parameter.TESTPLAN, '1513046', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513046')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
        Assertion.assert_equal(rc, True, "ERR: test_00_01_config_ftp_automation")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_start_traffic(self):
        rc = pm_obj.clear_packets()
        rc &= pm_obj.start_capture()
        logger.info("Start capture")
        sleep(60)
        rc = pm_obj.stop_capture()
        outputs = pm_obj.export_captured_packets()
        outputs = outputs.replace('\n','').replace('\r\n','')
        logger.info(outputs)
        Assertion.assert_regular(outputs, 'Src=\[192\.168\.13\.200\], Dst=\[192\.168\.13\.168\].*FTP Control', "ERR: check log failed")

    def test_00_04_check_log(self):
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.txt', "ERR: test_00_04_check_log")

    def test_00_05_config_ftp_automation(self):
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
                            "send_log_to_ftp": False, 
                            "server": "192.168.13.298", 
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
        Assertion.assert_equal(rc, False, "ERR: config_ftp_automation with error ip failed")

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
                            "send_log_to_ftp": False, 
                            "server": "192.168.13.", 
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
        Assertion.assert_equal(rc, False, "ERR: config_ftp_automation with error ip")
    
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
                            "send_log_to_ftp": False, 
                            "server": "192.168.13.6,192.168.13.200", 
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
        Assertion.assert_equal(rc, False, "ERR: config_ftp_automation with error ip")


class ftp_support_for_log_automation_1513052(Test):
    uuid = '1513052'
    description = show_testcase_info(Parameter.TESTPLAN, '1513052', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                                "html":True
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: config file format as html failed")

    def test_00_02_config_ftp_automation(self):
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
                                "attachment":{
                                "csv":True
                            }
                            }, 
                            "include_all_log_information": True
                        }, 
                    }
                }
            }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: config file format as csv failed")


class ftp_support_for_log_automation_1513068(Test):
    uuid = '1513068'
    description = show_testcase_info(Parameter.TESTPLAN, '1513068', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513068')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                            "user_name": "aaaaa", 
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation failed")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(70)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), '\.txt', "ERR: check log failed")


class ftp_support_for_log_automation_1513069(Test):
    uuid = '1513069'
    description = show_testcase_info(Parameter.TESTPLAN, '1513069', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513069')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
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
                            "password": "aaaaaaa", 
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation failed")

    def test_00_02_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(70)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_not_regular(str(rc), '\.txt', "ERR: check log failed")


class ftp_support_for_log_automation_1513038(Test):
    uuid = '1513038'
    description = show_testcase_info(Parameter.TESTPLAN, '1513038', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513038')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_check_config(self):
        rc = log_automation.show_log_automation()
        logger.info(rc)
        Assertion.assert_regular(str(rc), """ftp_log.*send_log_to_ftp.*server.*0.0.0.0.*user_name.*admin.*directory.*send_log.*when_full.*file_format.*text""", "ERR: check log failed")

    
class ftp_support_for_log_automation_1513042(Test):
    uuid = '1513042'
    description = show_testcase_info(Parameter.TESTPLAN, '1513042', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513042')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
        log_automation_json = {
            "log": {
                "automation": { 
                    "ftp_log": {
                        "send_log_to_ftp": False, 
                        "server": "0.0.0.0", 
                        "user_name": "admin", 
                        "password": "", 
                        "directory": "logs", 
                        "send_log": {
                            "when_full": True
                        }, 
                        "file_format": {
                            "plain_text": True
                        }, 
                        "include_all_log_information": False
                    }
                }
            }
        }
        rc = log_automation.edit_log_automation(**log_automation_json)
        Assertion.assert_equal(rc, True, "ERR: config ftp automation as default")


class ftp_support_for_log_automation_1513056(Test):
    uuid = '1513056'
    description = show_testcase_info(Parameter.TESTPLAN, '1513056', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513056')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_00_01_config_ftp_automation(self):
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation")

    def test_00_02_change_ftp_server_to_port_model(self):
        mail_server.send_command(f"cp {local_cert}/vsftpd.conf /etc/vsftpd/vsftpd.conf")
        mail_server.send_command(f"sudo systemctl restart vsftpd")
        rc = mail_server.send_command(f"sudo systemctl status vsftpd")
        Assertion.assert_regular(str(rc), """running""", "ERR: test_00_02_change_ftp_server_to_port_model")

    def test_00_03_set_dut_time(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_04_check_log(self):
        sleep(70)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '.txt', "ERR: test_00_04_check_log")


class ftp_support_for_log_automation_1513036(Test):
    uuid = '1513036'
    description = show_testcase_info(Parameter.TESTPLAN, '1513036', description=True)['title']

    def test_00_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1513036')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_00_01_config_ftp_automation(self):
        mail_server.send_command("rm -rf /tmp/ftp_log/*")
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
                            "daily": {
                                    "hour": 3, 
                                    "minute": 0
                                }
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
                            "server": "172.16.1.20", 
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
        Assertion.assert_equal(rc, True, "ERR: config ftp automation")

    def test_00_02_set_dut_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "02:59:00",
                "date": "2023:03:31",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = time_api.set_time(**time_json)
        Assertion.assert_equal(rc, True, "ERR: set firewall time failed")

    def test_00_03_check_log(self):
        sleep(120)
        rc = mail_server.send_command("ls /tmp/ftp_log/")
        Assertion.assert_regular(str(rc), '\.txt', "ERR: test_00_03_check_log")