from definition.settings import *
from definition.utils import *


# Expected: Check audit log should display 'Group Name' after added/edited/deleted DNS Filtering policy
class TestSettings_1997288(Test):
    uuid = "SOSAIOT-TC-51538"
    description = show_testcase_info(TESTPLAN, '1997288', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1997288')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_config_dns_policy(self):
        rc_add = dnsRule_api.add_dns_rule(**dns_rule_dict)
        logger.info(f'Add dns policy result...... {rc_add}')
        rc_edit = dnsRule_api.edit_dns_rule(**{'name': CParam.Name, 'new-name': 'edit', "enable": False})
        logger.info(f'Edit dns policy result...... {rc_edit}')
        rc_delete = dnsRule_api.del_dns_rule_by_name(name='edit')
        logger.info(f'Delete dns policy result...... {rc_delete}')
        Assertion.assert_equal(rc_add & rc_edit & rc_delete, True, "ERR: config_dns_policy failed!!")

    def test_02_check_audit_log_dns_policy(self):
        rc = False
        audit_list = audit_api.show_audit_records()
        if not audit_list:
            logger.error('Get audit log failed!!')
        else:
            for audit in audit_list:
                if 'DNS Policy' in audit.get('description'):
                    rc = 'DNS Policy' in audit.get('group_name')
                    if not rc:
                        logger.error(f'Check Log group name failed!! Audit log details: <{json.dumps(audit)}>')
                        break
                    logger.info(json.dumps(audit))
        Assertion.assert_equal(rc, True, "ERR: check_audit_log_dns_policy failed!!")


# Expected: Verified the default status of DNS Filtering log settings are correct.
class TestSettings_1521051(Test):
    uuid = "SOSAIOT-TC-51526"
    description = show_testcase_info(TESTPLAN, '1521051', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521051')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_the_log_default_status(self):
        # logMonitor_api.reset_default_log_settings() # For debug 
        rc = False
        try:
            events = log_category_api.get_log_groups_events()
            event_list = events['log']['event']
            check_res = []
            for event_name, target in log_status_dict.items():
                logger.info(f'--- TEST Log Status --- "{event_name}" --- ')
                for event in event_list:
                    if event_name in event['name']:
                        event_id = event['id']
                        log_id_list.append(event_id)
                        logger.info(f'Log id: {event_id}')
                        if event_name == 'DNS Packet Dropped':
                            CParam.Log_id = event_id
                        status = 'redundancy_interval' in event['log_monitor'].keys()
                        logger.info(f'Actual Enabled: {status}')
                        logger.info(f'Target Enabled: {target}')
                        res = status == target
                        check_res.append(res)
                        logger.info(f'RESULT: {str(res).upper()}')
                        if not res:
                            logger.error(f'-> Log "{event_name}" gui default status is wrong!!')
                        break
                else:
                    logger.error(f'Not found Log "{event_name}"!!')
            rc = all(check_res)
        except KeyError:
            logger.error('Get log event failed!!')
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check_the_log_default_status failed!!")


# Expected: Disable the log switches of DNS Filtering.
class TestSettings_1521053(Test):
    uuid = "SOSAIOT-TC-51528"
    description = show_testcase_info(TESTPLAN, '1521053', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521053')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_disable_dns_filtering_logs(self):
        rc = False
        for event_id in log_id_list:
            rc = logSet_api.disable_event(event_id=str(event_id))
            if not rc:
                logger.error(f'Disable log <{event_id}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: disable_dns_filtering_logs failed!!")


# Expected: Enable the log switches of DNS Filtering.
class TestSettings_1521052(Test):
    uuid = "SOSAIOT-TC-51527"
    description = show_testcase_info(TESTPLAN, '1521052', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521052')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_filtering_logs(self):
        rc = False
        for event_id in log_id_list:
            enable_log_dict = {
                "log": {
                    "event": [
                        {
                            "id": event_id,
                            "log_monitor": {"redundancy_interval": 0}
                        }]}}
            rc = logSet_api.enable_event(**enable_log_dict)
            if not rc:
                logger.error(f'Enable log <{event_id}> failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: enable_dns_filtering_logs failed!!")


# Expected: Verify Matched DNS policy displays in DNS Filtering log details
class TestFunc_2045124(Test):
    uuid = "SOSAIOT-TC-51537"
    description = show_testcase_info(TESTPLAN, '2045124', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2045124')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_enable_dns_drop_logs(self):
        rc = logSet_api.edit_event(event_id=str(CParam.Log_id), **drop_log_dict)
        Assertion.assert_equal(rc, True, "ERR: enable_dns_drop_logs failed!!")

    def test_02_add_dns_policy(self):
        rc = dnsRule_api.add_dns_rule(**dns_rule_dict)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_03_do_dns_query_from_client(self):
        clear_res = logMonitor_api.clear_log()
        logger.info(f'Clear logs result...... {clear_res}')
        rc = check_dns_query_no_error(domain='adultswim.com')
        Assertion.assert_equal(rc, True, "ERR: do_dns_query_from_client failed!!")

    def test_04_check_drop_logs(self):
        rc = check_related_logs(target=f"Match policy: {CParam.Name}")
        Assertion.assert_equal(rc, True, "ERR: check_drop_logs failed!!")

    def test_05_delete_added_dns_policy(self):
        rc = dnsRule_api.del_dns_rule_by_name(name=CParam.Name)
        Assertion.assert_equal(rc, True, "ERR: delete_added_dns_policy failed!!")
