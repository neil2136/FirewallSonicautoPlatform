from definition.settings import *
import datetime
import os
import re


class TestLog_Monitor_12(Test):
    uuid = "SOSAIOT-TC-55490"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_Log(self):
        log = log_obj.export_log_txt(log_switch=False)
        logger.info(log)

    def test_02_Disable_this_kind_of_Log(self):
        out = log_settings.disable_event(event_id='566')
        Assertion.assert_equal(out, True, "ERR: disable log failed")


class TestLog_Monitor_13(Test):
    uuid = "SOSAIOT-TC-55491"
    description = show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_log_settings(self):
        log_settings = {
            "log": {
                "display": {
                    "time_range": {
                        "all": True
                    },
                    "max_number": 200
                }
            }
        }
        output = log_obj.edit_log_display_time_and_entry(**log_settings)
        Assertion.assert_equal(output, True, "ERR: set log settings failed")

    def test_02_Update_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP_TMP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interface_obj.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_03_get_target_log_by_id(self):
        num = 0
        flag = False
        try:
            output = log_obj.get_log(id=138)
            logger.info("8" * 60)
            logger.info(output)
            logger.info("8" * 60)
            for entry in output:
                if entry['message'] == 'Wan IP Changed':
                    num += 1
            if output:
                if num == len(output):
                    flag = True
            else:
                logger.info("ERROR:the return value of get_log is empty...")
            logger.info(len(output))
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, True, "ERR: get target log by id failed")


class TestLog_Monitor_16(Test):
    uuid = "SOSAIOT-TC-55493"
    description = show_testcase_info(TESTPLAN, '16', description=True)['title']
    jira = 'GEN7-42726'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_categories_alert(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "syslog": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "ipfix": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_02_verify_sub_event_and_sub_category_alert_checkbox_status(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['log_monitor']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["log_monitor"]:
                    num += 1
                else:
                    logger.info("8" * 60)
                    logger.info(cate)
                    logger.info("8" * 60)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 2, "ERR: verify sub event and sub category failed")

    def test_03_config_event_Alert_checkbox(self):
        # Network->Advanced Routing id is 68
        event_settings = {
            "log": {
                "group": [
                    {
                        "id": 68,
                        "name": "Advanced Routing",
                        "priority_level": "mixed",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {"type": "enabled", "redundancy_interval": {"value": 50}},
                        "event_profile": {"syslog_server_profile": 0},
                        "log_digest": {"enabled": True}, "color": {"leave_unchanged": True},
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_category_groups_by_id(id=68, **event_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_04_verify_main_and_sub_category_showed_mixed_mode_on_Alert_checkbox(self):
        flag = 0
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            logger.info("8" * 60)
            logger.info(out1)
            logger.info("8" * 60)
            if out1['log']['category'][0]['log_monitor']['type'] == 'mixed':
                flag = 1
            out2 = log_set.get_global_categories()
            if out2['log']['categories']['global_category_attribute']['log_monitor']['type'] == 'mixed':
                flag += 1
            logger.info(out2)
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 2, "ERR: verify main and sub categories alert failed")

    def test_05_edit_log_event(self):
        params = {
            "log": {
                "event": [{
                    "id": 5,
                    "name": "Clear Log",
                    "priority_level": "alert",
                    "log_monitor": {
                        "redundancy_interval": 0
                    },
                    "email_alert": {
                        "redundancy_interval": 0
                    },
                    "syslog": {
                        "redundancy_interval": 60
                    },
                    "trap": {},
                    "ipfix": {
                        "redundancy_interval": 60
                    },
                    "event_profile": {
                        "syslog_server_profile": 0
                    },
                    "log_digest": True,
                    "color": {
                        "hex": "0x00000000"
                    },
                    "alert_email": {
                        "address": "test1@smtpstest.com"
                    }
                }]
            }
        }
        out = log_settings.edit_event(event_id='5', **params)
        Assertion.assert_equal(out, True, "ERR: edit log event failed")

    def test_06_edit_log_automation(self):
        output1 = log_automation.show_log_automation()
        logger.info("8" * 60)
        logger.info(output1)
        logger.info("8" * 60)
        try:
            output1 = log_automation.show_log_automation()
            logger.info("8" * 60)
            logger.info(output1)
            logger.info("8" * 60)
            output1["log"]["automation"]["mail_server"] = PC1_ETH1_IP
            output1["log"]["automation"]["mail_from"] = "test1@smtpstest.com"
        except:
            logger.error("show log automation failed")
        out = log_automation.edit_log_automation(**output1)
        Assertion.assert_equal(out, True, "ERR: edit log automation failed")

    def test_07_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    @repeat_method(5)
    def test_09_Verify_email(self):
        logger.info('Clear log and check whether it has related info in email')
        log_obj.clear_log()
        time.sleep(10)
        try:
            ret = pop3_client.get_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info('8' * 60)
            logger.info(ret)
            logger.info('8' * 60)
        except Exception as err:
            logger.error(err)
        Assertion.assert_regular(str(ret), "Log - Alert - Log Cleared", "ERR: clear test1 inbox failed")


class TestLog_Monitor_26(Test):
    uuid = "SOSAIOT-TC-55498"
    description = show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_categories_and_create_template(self):
        flag = False
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {"type": "mixed"},
                        "event_profile": {"syslog_server_profile": 0},
                        "log_digest": {"mixed": True},
                        "color": {"leave_unchanged": True}, "alert_email": {}
                    }
                ]
            }
        }
        out1 = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        out2 = log_set.log_save_template(description="in test")
        if out1 == True and out2 == None:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config categories and create template failed ")

    def test_02_import_custom_template(self):
        out = log_set.import_template(template_name='custom')
        Assertion.assert_equal(out, True, "ERR: import custom template failed ")

    def test_03_config_categories_alert(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "syslog": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "ipfix": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_04_verify_catetories(self):
        flag = False
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['log_monitor']['type'] == "enabled":
                flag = True
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, True, "ERR: verify catetories failed ")

    def test_05_restore_to_default_template(self):
        out = log_set.import_template(template_name='default')
        Assertion.assert_equal(out, True, "ERR: import custom template failed ")


class TestLog_Monitor_Export_CSV(Test):
    uuid = "SOSAIOT-TC-55496"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_Log_CSV(self):
        log = log_obj.export_log_csv()
        default_string = "192.168.168.169"

        flag = False
        if default_string in log:
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")


class TestLog_Monitor_Export_TXT(Test):
    uuid = "SOSAIOT-TC-55501"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_Log_TXT(self):
        log = log_obj.export_log_txt()
        default_string = "192.168.168.169"

        flag = False
        if default_string in log:
            flag = True
        Assertion.assert_equal(True, flag, "ERR: export log and check info failed")


class TestLog_Monitor_Clear_Log(Test):
    uuid = "SOSAIOT-TC-55510"
    description = show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_clear_log(self):
        log_obj.clear_log()
        resp = log_obj.export_log_csv()
        Assertion.assert_regular(str(resp), "Log Cleared", "ERR: export log and check info failed")


class TestLog_Monitor_Log_Monitor_fw_reboot(Test):
    uuid = "SOSAIOT-TC-55507"
    description = show_testcase_info(TESTPLAN, '45', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '45')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_log_mail(self):
        before_reboot = log_set.get_log_categories_by_name(name='Firewall')

        fw_restart.restart_now()
        time.sleep(10)
        after_reboot = log_set.get_log_categories_by_name(name='Firewall')

        assert before_reboot == after_reboot, "Configuration is not intact after fw restart"


class TestLog_Monitor_Import_from_template_Default(Test):
    uuid = "SOSAIOT-TC-55499"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_log_mail(self):
        initial_json = log_settings.show_event(event_id=999)

        # configuring a event and saving it as template
        config_event_json = {
            "log": {
                "event": [
                    {
                        "id": 999,
                        "name": "Website Found in Blacklist",
                        "category": "Firewall Settings",
                        "group": "SSL Control",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        config_event = log_settings.enable_event(**config_event_json)
        Assertion.assert_equal(config_event, True, "ERR: enable log event failed")

        save_as_template = log_set.log_save_template(description="in test")
        # importing template
        import_temp = log_set.import_template(template_name='default')
        Assertion.assert_equal(import_temp, True, "ERR: import custom template failed ")
        # FW boot in factory default mode
        boot_fw = fw_boot.boot_fw(2)
        Assertion.assert_equal(boot_fw, True, "ERR: Boot current firmware with factory default settings fail.")
        # verify configuration after bootup
        final_json = log_settings.show_event(event_id=999)

        assert initial_json == final_json, "Configuration is not intact after fw boot up"


class TestLog_Monitor_Import_from_template_Minimal(Test):
    uuid = "SOSAIOT-TC-55500"
    description = show_testcase_info(TESTPLAN, '28', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '28')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_log_mail(self):
        initial_json = log_settings.show_event(event_id=999)

        # configuring a event
        config_event_json = {
            "log": {
                "event": [
                    {
                        "id": 999,
                        "name": "Website Found in Blacklist",
                        "category": "Firewall Settings",
                        "group": "SSL Control",
                        "priority_level": "inform",
                        "log_monitor": {
                            "redundancy_interval": 0
                        },
                        "email_alert": {
                            "redundancy_interval": 0
                        },
                        "syslog": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "trap": {},
                        "ipfix": {},
                        "log_digest": False,
                        "alert_email": {}
                    }
                ]
            }
        }
        config_event = log_settings.enable_event(**config_event_json)
        Assertion.assert_equal(config_event, True, "ERR: enable log event failed")

        # importing template
        import_temp = log_set.import_template(template_name='minimal')
        Assertion.assert_equal(import_temp, True, "ERR: import minimal template failed ")

        # verify configuration after import
        final_json = log_settings.show_event(event_id=999)

        assert initial_json['log']['event'][0]['color']['hex'] == final_json['log']['event'][0]['color'][
            'hex'], "Color configuration got changed"
        assert initial_json['log']['event'][0]['log_monitor'] == final_json['log']['event'][0][
            'log_monitor'], "GUI selection did not change"


class TestLog_Monitor_Rules_name_should_contain_policy_ID_and_name_for_Access_and_NAT_in_System_Logs_page(Test):
    uuid = "SOSAIOT-TC-55512"
    description = show_testcase_info(TESTPLAN, '50', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '50')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_Log_CSV(self):
        log = log_obj.export_log_csv()
        logger.info(log)
        access_rule = 'Default Access Rule'
        policy_id = '11'
        Assertion.assert_regular(str(log), access_rule, "ERR: export log and check info failed")
        Assertion.assert_regular(str(log), policy_id, "ERR: export log and check info failed")


class TestLog_Monitor_Send_log_to_email(Test):
    uuid = "SOSAIOT-TC-55509"
    description = show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_send_log_to_mail(self):
        # configure mail server value
        log_automation_json = {
            "log": {
                "automation": {
                    "email_address": {
                        "log": "test1@smtpstest.com",
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
                    "include_all_log_information": True,
                    "send_audit": {
                        "when_full": True
                    },
                    "email_format_audit": {
                        "plain_text": True
                    },
                    "health_check_email": {
                        "schedule": {}
                    },
                    "mail_server": "192.168.168.169",
                    "mail_from": "test1@smtpstest.com",
                    "authentication_method": "none",
                    "mail_server_advanced": {
                        "smtp_port": 25,
                        "connection_security_method": {},
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
        Assertion.assert_equal(rc, True, "ERR: config failed")

        # export the mail
        log = log_obj.export_log_mail()
        logger.info(log)

        Assertion.assert_regular(log["status"]["info"][0]["message"], "The log will be sent by email.",
                                 "Err: log not sent to mail")
        logger.info("Log sent to mail")


class TestLog_Monitor_Reset_category_event_count(Test):
    uuid = "SOSAIOT-TC-55497"
    description = show_testcase_info(TESTPLAN, '24', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '24')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_reset_event_count(self):
        # Configure sub category and click the Reset Event Count button
        reset_event_group = log_set.log_reset_event_count_by_group(category='Users', group='Authentication Access')
        assert reset_event_group == True, "Reset count failed"

        # Configure event and click the Reset Event Count button
        reset_event_id = log_set.log_reset_event_count_by_event_id(eventid=1659)
        assert reset_event_id == True, "Reset count failed"

        # Configure Main category and click the Reset Event Count button
        log_clear = log_set.log_reset_event_count('Users')
        resp = log_set.get_log_categories_statistics_by_name('Users')
        event_count = resp['event_count']
        assert event_count == 0, "Reset count failed"


class TestLog_Monitor_Edit_category_entry_GUI(Test):
    uuid = "SOSAIOT-TC-55492"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_category_entry_GUI(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_02_verify_sub_event_and_sub_category_gui_checkbox_status(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['log_monitor']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["log_monitor"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 2, "ERR: verify sub event and sub category failed")

    def test_03_edit_category_entry_GUI_disable(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_04_verify_sub_event_and_sub_category_gui_checkbox_status_disabled(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['log_monitor']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["log_monitor"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 0, "ERR: verify sub event and sub category failed")


class TestLog_Monitor_Edit_category_entry_Syslog(Test):
    uuid = "SOSAIOT-TC-55494"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_category_entry_syslog(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_02_verify_sub_event_and_sub_category_syslog_checkbox_status(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['syslog']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["syslog"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 2, "ERR: verify sub event and sub category failed")

    def test_03_edit_category_entry_syslog_disable(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_04_verify_sub_event_and_sub_category_syslog_checkbox_status_disabled(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['syslog']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["syslog"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 0, "ERR: verify sub event and sub category failed")


class TestLog_Monitor_Edit_category_entry_email(Test):
    uuid = "SOSAIOT-TC-55495"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_category_entry_email(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_02_verify_sub_event_and_sub_category_email_checkbox_status(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['email_alert']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["email_alert"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 2, "ERR: verify sub event and sub category failed")

    def test_03_edit_category_entry_email_disable(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {},
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_04_verify_sub_event_and_sub_category_email_checkbox_status_disabled(self):
        flag = 0
        num = 0
        network_log_events = []
        try:
            out1 = log_set.get_log_categories_by_name(name="Network")
            if out1['log']['category'][0]['email_alert']['type'] == "enabled":
                flag += 1
            out2 = log_settings.get_event_log_categories()
            for entry in out2['log']['event']:
                if entry['category'] == 'Network':
                    network_log_events.append(entry)
            for cate in network_log_events:
                if "redundancy_interval" in cate["email_alert"]:
                    num += 1
                else:
                    logger.info(cate)
            if len(network_log_events) == num:
                flag += 1
            else:
                logger.error(f"network_log_events len is {len(network_log_events)}, and num is {num}")
        except Exception as err:
            logger.error(err)
        Assertion.assert_equal(flag, 0, "ERR: verify sub event and sub category failed")


class TestLog_Monitor_Log_Monitor_preference_file(Test):
    uuid = "SOSAIOT-TC-55506"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Log_Monitor_preference_file(self):
        # configuring log monitor
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

        initial_json = log_set.get_log_categories_by_name(name="Network")
        logger.info('initial_json', initial_json)

        # export preference file
        rc = fw_boot.export_setting_exp(filepath='/tmp/testlog1.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to export the settings...")
        # import preference file
        rc1 = fw_boot.import_setting_exp(filepath='/tmp/testlog1.exp')
        Assertion.assert_equal(rc1, True, "Error: Failed to import the settings...")
        final_json = log_set.get_log_categories_by_name(name="Network")
        assert initial_json == final_json, "Configuration is not intact after import pref file"
        # # FW boot in factory default mode
        boot_fw = fw_boot.boot_fw(2)
        Assertion.assert_equal(boot_fw, True, "ERR: Boot current firmware with factory default settings fail.")
        # import preference file after factory default mode
        rc2 = fw_boot.import_setting_exp(filepath='/tmp/testlog1.exp')
        Assertion.assert_equal(rc2, True, "Error: Failed to import the settings...")
        final_json1 = log_set.get_log_categories_by_name(name="Network")

        assert initial_json['log']['category'][0]['log_monitor'] == final_json1['log']['category'][0][
            'log_monitor'], "Configuration is not intact after fw boot"


class TestLog_Monitor_Name_Resolution(Test):
    uuid = "SOSAIOT-TC-55508"
    description = show_testcase_info(TESTPLAN, '46', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '46')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_name_resolution(self):
        # clearing log
        # log_obj.clear_log()
        # Configure to use DNS then Netbios and apply DNS server address
        resolution_json = {
            "log": {
                "name_resolution": {
                    "method": "dns-then-netbios",
                    "dns": {
                        "inherit": True
                    }
                }
            }
        }
        rc = log_res.edit_resolution(**resolution_json)
        Assertion.assert_equal(rc, True, "ERR: Edit Resolution log failed")

        time.sleep(20)
        # export csv file and verify source name
        log = log_obj.export_log_csv()
        search_string = 'sonicwall.com'
        Assertion.assert_regular(str(log), search_string, "ERR: name resolution failed")


class TestLog_Monitor_Select_Columns_to_Display(Test):
    uuid = "SOSAIOT-TC-55508"
    description = show_testcase_info(TESTPLAN, '4', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_coloums_to_display(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/definition/ui_user.py -method firewall_login ' + '-url ' + url + ' -user admin -pwd sonicauto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"


class TestLog_Monitor_Refresh_every_amount_seconds(Test):
    uuid = "SOSAIOT-TC-55511"
    description = show_testcase_info(TESTPLAN, '8', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Refresh_every_amount_seconds(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/definition/ui_user.py -method refresh_log ' + '-url ' + url + ' -user admin -pwd sonicauto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"

    def test_02_Refresh_every_amount_seconds(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Log/Log_Monitor_TP2582/definition/ui_user.py -method refresh_log_new ' + '-url ' + url + ' -user admin -pwd sonicauto '
        out = static_client.send_command(cmd)
        logger.info("login with user\n" + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', "Testcase failed"


class TestLog_Monitor_Syslog_format(Test):
    uuid = "SOSAIOT-TC-55502"
    description = show_testcase_info(TESTPLAN, '32', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '32')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_category_to_send_syslog(self):
        category_settings = {
            "log": {
                "category": [
                    {
                        "id": 6,
                        "name": "Network",
                        "priority_level": "mixed",
                        "log_email": "",
                        "log_monitor": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "syslog": {
                            "type": "enabled",
                            "redundancy_interval": {}
                        },
                        "email_alert": {},
                        "syslog": {},
                        "ipfix": {},
                        "event_profile": {
                            "syslog_server_profile": 0
                        },
                        "log_digest": {
                            "enabled": True
                        },
                        "color": {
                            "leave_unchanged": True
                        },
                        "alert_email": {}
                    }
                ]
            }
        }
        out = log_set.edit_log_categories_by_name(name="Network", **category_settings)
        Assertion.assert_equal(out, True, "ERR: config categories alert failed")

    def test_02_add_syslog_server_as_default(self):
        # clearing log
        # log_obj.clear_log()
        # creating address object for custom syslog
        ao_param = {
            "object_type": "host",
            "name": "test_syslog",
            "zone": "LAN",
            "value": "192.168.168.169",
        }
        rc = addrObj.config_addressobject(**ao_param)
        Assertion.assert_equal(rc, True, 'ERR: Add mail server address object failed')

        json_data = {
            "log": {
                "syslog": {
                    "server": [
                        {
                            "address": {
                                "name": "test_syslog"
                            },
                            "port": 514,
                            "profile": 0,
                            "type": "syslog-server",
                            "format": "default",
                            "facility": "local-use0",
                            "id": "firewall",
                            "enabled": True,
                            "event_rate_limiting": {
                                "enabled": False
                            },
                            "data_rate_limiting": {
                                "enabled": False
                            },
                            "outbound_interface": ""
                        }
                    ]
                }
            }
        }
        rc = log_sys.add_syslog_server_custom(**json_data)
        logger.info('create response', rc)

        # check_log_to_verify_default
        log = log_obj.export_log_csv()
        default_string = "Configuration succeeded"

        flag = False
        if default_string in log:
            flag = True
        Assertion.assert_equal(True, flag,
                               "ERR: Verify the syslog received log with correct format and information failed")

    def test_03_check_log_to_verify_webtrends(self):
        # clearing log
        log_obj.clear_log()
        # update format to webtrends
        json_data = {
            "log": {
                "syslog": {
                    "server": [
                        {
                            "address": {
                                "name": "test_syslog"
                            },
                            "port": 514,
                            "profile": 0,
                            "type": "syslog-server",
                            "format": "webtrends",
                            "facility": "local-use0",
                            "id": "firewall",
                            "enabled": True,
                            "event_rate_limiting": {
                                "enabled": False
                            },
                            "data_rate_limiting": {
                                "enabled": False
                            },
                            "outbound_interface": ""
                        }
                    ]
                }
            }
        }
        rc = log_sys.edit_syslog_server_custom_by_servername(servername='test_syslog', event_profile=0, **json_data)
        Assertion.assert_equal(True, rc, "ERR: Update syslog server failed")

        # check_log_to_verify_webtrends
        log = log_obj.export_log_csv()
        default_string = ['m=', 'port', 'interface', 'n=', 'c=']

        flag = False
        for i in range(0, len(default_string)):
            if re.search(fr'\b{re.escape(default_string[i])}\b', log):
                flag = True

        logger.info('flagggg', flag)
        Assertion.assert_equal(False, flag, "ERR: Verify syslog didnt contain m=,port,interface, n=,c= failed")
