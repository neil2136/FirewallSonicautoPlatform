from definition.settings import *


class TestLog_Monitor_12(Test):
    uuid = "SOSAIOT-TC-55490"
    description= show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Get_Log(self):
        log = log_obj.export_log_txt(log_switch=False)
        logger.info(log) 

    def test_02_Disable_this_kind_of_Log(self):
        out = log_settings.disable_event( event_id = '566')
        Assertion.assert_equal(out, True, "ERR: disable log failed")


class TestLog_Monitor_13(Test):
    uuid = "SOSAIOT-TC-55491"
    description= show_testcase_info(TESTPLAN, '13', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_log_settings(self):
        log_settings = {
            "log":{
                "display":{
                    "time_range":{
                        "all":True
                    },
                    "max_number":200
                }
            }
        } 
        output = log_obj.edit_log_display_time_and_entry( **log_settings )
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
            output = log_obj.get_log( id = 138 )
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
    description= show_testcase_info(TESTPLAN, '16', description=True)['title']
    jira = 'GEN7-42726'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_categories_alert(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log":{
                "category":[
                    {
                        "id":6,
                        "name":"Network",
                        "priority_level":"mixed",
                        "log_email":"",
                        "log_monitor":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "email_alert":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "syslog":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "ipfix":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "event_profile":{
                            "syslog_server_profile":0
                        },
                        "log_digest":{
                            "enabled":True
                        },
                        "color":{
                            "leave_unchanged":True
                        },
                        "alert_email":{}
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
        #Network->Advanced Routing id is 68
        event_settings = {
            "log":{
                "group":[
                    {
                        "id":68,
                        "name":"Advanced Routing",
                        "priority_level":"mixed",
                        "log_monitor":{},
                        "email_alert":{},
                        "syslog":{},
                        "ipfix":{"type":"enabled","redundancy_interval":{"value":50}},
                        "event_profile":{"syslog_server_profile":0},
                        "log_digest":{"enabled":True},"color":{"leave_unchanged":True},
                        "alert_email":{}
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
        Assertion.assert_equal(flag, 2,"ERR: verify main and sub categories alert failed")

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
        out = log_settings.edit_event( event_id = '5', **params)
        Assertion.assert_equal(out, True,"ERR: edit log event failed")

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
        out = log_automation.edit_log_automation( **output1 )
        Assertion.assert_equal(out, True,"ERR: edit log automation failed")

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
    description= show_testcase_info(TESTPLAN, '26', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_config_categories_and_create_template(self):
        flag = False
        category_settings = {
            "log":{
                "category":[
                    {
                        "id":6,
                        "name":"Network",
                        "priority_level":"mixed",
                        "log_email":"",
                        "log_monitor":{},
                        "email_alert":{},
                        "syslog":{},
                        "ipfix":{"type":"mixed"},
                        "event_profile":{"syslog_server_profile":0},
                        "log_digest":{"mixed":True},
                        "color":{"leave_unchanged":True},"alert_email":{}
                    }
                ]
            }
        }
        out1 = log_set.edit_log_categories_by_name( name="Network", **category_settings)
        out2 = log_set.log_save_template( description="in test")
        if out1 == True and out2 == None:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: config categories and create template failed ")


    def test_02_import_custom_template(self):
        out = log_set.import_template(template_name='custom')
        Assertion.assert_equal(out, True, "ERR: import custom template failed ")

    def test_03_config_categories_alert(self):
        # edit categories Network log_monitor to enabled status
        category_settings = {
            "log":{
                "category":[
                    {
                        "id":6,
                        "name":"Network",
                        "priority_level":"mixed",
                        "log_email":"",
                        "log_monitor":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "email_alert":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "syslog":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "ipfix":{
                            "type":"enabled",
                            "redundancy_interval":{}
                        },
                        "event_profile":{
                            "syslog_server_profile":0
                        },
                        "log_digest":{
                            "enabled":True
                        },
                        "color":{
                            "leave_unchanged":True
                        },
                        "alert_email":{}
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
