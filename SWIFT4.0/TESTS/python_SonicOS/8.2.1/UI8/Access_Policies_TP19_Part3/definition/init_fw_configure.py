from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    @repeat_method(5)
    def test_01_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed!!")

    def test_02_get_default_policy_uuid(self):
        json = {
            "action": "allow",
            "from": "LAN",
            "to": "LAN",
            "service": {"name": "HTTPS Management"},
            "destination": {"address": {"group": "All X0 Management IP"}}
        }
        uuid_list = acl_api.get_access_rules_uuid_by_json(**json)
        CParam.ACL_UUID = uuid_list.pop()
        Assertion.assert_not_equal(CParam.ACL_UUID, '', "ERR: get_default_policy_uuid failed!!")

    def test_03_get_default_policy_name(self):
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        logger.info('Click "Grid" to open Grid Settings window')
        fw_page_ui.click_element_by_text('Grid')
        logger.info('Click "Miscellaneous"')
        fw_page_ui.click_element_by_text('Miscellaneous')
        logger.info('Click "UUID"')
        fw_page_ui.click_element_by_text('UUID')
        logger.info('Click "Apply"')
        fw_page_ui.click_element_by_text('Apply')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        time.sleep(2)
        logger.info('Get ACL Name by uuid')
        name_path = get_table_entry_element_xpath(CParam.ACL_UUID, element='/descendant::*[contains(text(), "Default Access Rule")]')
        CParam.Name = str(fw_page_ui.get_attribute_value(*name_path, attrib_to_get_val='textContent'))
        PathData.hit_num = get_table_entry_element_xpath(CParam.Name, 'hit')
        Assertion.assert_not_equal(CParam.Name, "", "ERR: get_default_policy_name failed!!")

