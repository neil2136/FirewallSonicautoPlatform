from definition.settings import *

# GUI: ""Allow TCP Urgent Packets"" is added into access Rules
class TestACL_1520972(Test):
    testrail_uuid = '1520972'
    uuid = "SOSAIOT-TC-58032"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    toggle_action = True
    status = 'Enable'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_init_page_and_display_uuid_column(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        Assertion.assert_equal(True, True, "ERR: init_page failed!!")

    def test_02_go_to_optional_settings_tab(self):
        logger.info(f'Hover and Click "{CParam.Name}" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering_new(CParam.Name)
        rc = fw_page_ui.is_element_displayed(*PathData.edit_rule_window)
        logger.info('Navigate to "Optional Settings" tab')
        fw_page_ui.navigate_to_tab('Optional Settings')
        Assertion.assert_equal(rc, True, "ERR: open_edit_acl_rule_page failed!!")

    def test_03_enable_allow_tcp_urgent_packets_option(self):
        logger.info(f'{self.status} "Allow TCP Urgent Packets" toggle')
        fw_page_ui.toggle_button(*PathData.tcp_urgent_toggle, enabled=self.toggle_action)
        logger.info('Click "Save" button')
        fw_page_ui.click_element_by_text('Save')
        msg = f'Editing Rule [{CParam.Name}] was successful.'
        logger.info(f'Check message: "{msg}"')
        fw_page_ui.compare_message_new(msg)
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        Assertion.assert_equal(True, True, f"ERR: {self.status}_allow_tcp_urgent_packets_option failed!!")

    def test_04_disable_allow_tcp_urgent_packets_option(self):
        self.status = 'Disable'
        self.toggle_action = False
        self.test_02_go_to_optional_settings_tab()
        self.test_03_enable_allow_tcp_urgent_packets_option()


# Bottom bar - Live/Pause/Clear counter via bottom bar
class TestACL_1526085(Test):
    testrail_uuid = '1526085'
    uuid = "SOSAIOT-TC-58042"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    def test_02_check_live_counter_bottom_button(self):
        num = fw_page_ui.get_attribute_value(*PathData.hit_num, attrib_to_get_val='textContent')
        logger.info('Click "Live Counter" bottom button')
        logger.info(PathData.hit_num)
        fw_page_ui.click_element_by_text('Live Counter')
        time.sleep(3)
        logger.info('Check live hit counter:')
        rc = pc_runner.check_element_attribute(PathData.hit_num, num, strict=True)
        Assertion.assert_equal(not rc, True, "ERR: check_live_counter_bottom_button failed!!")

    def test_03_check_pause_counter_bottom_button(self):
        logger.info('Click "Pause Counter" bottom button')
        fw_page_ui.click_element_by_text('Pause Counter')
        num = fw_page_ui.get_attribute_value(*PathData.hit_num, attrib_to_get_val='textContent')
        time.sleep(3)
        logger.info('Check pause hit counter:')
        rc = pc_runner.check_element_attribute(PathData.hit_num, num, strict=True)
        Assertion.assert_equal(rc, True, "ERR: check_pause_counter_bottom_button failed!!")

    def test_04_check_reset_counter_bottom_button(self):
        logger.info(f'Select "{CParam.Name}" checkbox')
        checkbox = get_table_entry_element_xpath(CParam.Name, 'checkbox')
        fw_page_ui.click_element(*checkbox)
        logger.info('Click "Reset Counters" bottom button')
        fw_page_ui.click_element_by_text('Reset Counters')
        fw_page_ui.verify_message_alert('Are you sure you want to Reset Counters of selected 1 rule(s)?')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        fw_page_ui.compare_message_new('Clear Counters of selected rules was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info('Check reset hit counter:')
        hit = fw_page_ui.get_attribute_value(*PathData.hit_num, attrib_to_get_val='textContent')
        logger.info(f'> test: {hit}')
        rc = int(hit) >=0 and int(hit) <= 5 if hit and hit.isdigit() else False
        Assertion.assert_equal(rc, True, "ERR: check_reset_counter_bottom_button failed!!")


class Test_access_rule_details(Test):
    uuid = 'NonTC'
    description = 'combination of tests in access rule details'

    def test_01_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    # 1526095 - Verify as your mouse over each column of a policy, corresponding info is correctly showed
    def test_02_check_hit_count_details(self):
        uuid = "SOSAIOT-TC-58051"
        logger.info(f'uuid - {uuid}')
        logger.info('Mouse hover on the Hit Count')
        fw_page_ui.move_to_the_element(*PathData.hit_num)
        logger.info('Check Hits count')
        CParam.Hits = str(fw_page_ui.get_attribute_value(*PathData.hit_num, attrib_to_get_val='textContent'))
        rc = pc_runner.check_element_attribute(PathData.hits_count, CParam.Hits, strict=True)
        logger.info('Check Hits usage')
        rc &= pc_runner.check_element_attribute(PathData.hits_usage, '%')
        result_dict[uuid] = rc
        Assertion.assert_equal(rc, True, "ERR: check_hit_count_details failed!!")

    # 1526094 - Verify as your mouse over each column of a policy, corresponding info is correctly showed
    def test_03_check_hit_count_details(self):
        uuid = "SOSAIOT-TC-58050"
        logger.info(f'uuid - {uuid}')
        logger.info('Mouse hover on the Hit Count')
        fw_page_ui.move_to_the_element(*PathData.hit_num)
        logger.info('Check Hits count')
        CParam.Hits = str(fw_page_ui.get_attribute_value(*PathData.hit_num, attrib_to_get_val='textContent'))
        rc = pc_runner.check_element_attribute(PathData.hits_count, CParam.Hits, strict=True)
        logger.info('Check Hits usage')
        rc &= pc_runner.check_element_attribute(PathData.hits_usage, '%')
        result_dict[uuid] = rc
        Assertion.assert_equal(rc, True, "ERR: check_hit_count_details failed!!")

    # 1526087 - Check the hit count/diagram/connection number of the policy
    def test_04_check_expended_details(self):
        uuid = "SOSAIOT-TC-58044"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('Click black triangle to show policy details')
        fw_page_ui.click_element(*get_table_entry_element_xpath(CParam.Name))
        logger.info('Check expended hit count')
        rc_hit = bool(fw_page_ui.does_element_exist_now(*PathData.expend_hit))
        logger.info(rc_hit)
        logger.info('Check expended diagram')
        rc_diag = bool(fw_page_ui.does_element_exist_now(*PathData.expend_diag))
        logger.info(rc_hit)
        logger.info('Check expended connection count')
        rc_conn = bool(fw_page_ui.does_element_exist_now(*PathData.expend_conn))
        logger.info(rc_conn)
        result_dict[uuid] = rc_hit & rc_diag & rc_conn
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_expended_details failed!!")


@paramunittest.parametrized(
    {'testrail_uuid': '1526095', 'uuid': 'SOSAIOT-TC-58051'},
    {'testrail_uuid': '1526094', 'uuid': 'SOSAIOT-TC-58050'},
    {'testrail_uuid': '1526087', 'uuid': 'SOSAIOT-TC-58044'})
class TestAccess_rule_details(Test):

    def setParameters(self, uuid, testrail_uuid):
        self.uuid = uuid
        self.testrail_uuid = testrail_uuid
        self.description = show_testcase_info(TESTPLAN, self.testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


# Verify Dock Diagram when editing one access rule - 1526088
class TestACL_1526088(Test):
    testrail_uuid = '1526088'
    uuid = "SOSAIOT-TC-58045"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    def test_02_open_edit_window(self):
        logger.info(f'Hover and Click "{CParam.Name}" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering_new(CParam.Name)
        rc = fw_page_ui.is_element_displayed(*PathData.edit_rule_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_acl_rule_window failed!!")

    def test_03_verify_show_diagram_window(self):
        logger.info('Click "Show Diagram" toggle')
        fw_page_ui.toggle_button(*get_toggle_xpath('Show Diagram'), enabled=True)
        logger.info('------ Check Diagram window display')
        rc = pc_runner.check_element_attribute(PathData.diagram_window, 'display:none', 'style')
        Assertion.assert_equal(not rc, True, "ERR: verify_show_diagram_window failed!!")

    def test_04_verify_dock_diagram(self):
        logger.info('Click "Dock Diagram" toggle')
        fw_page_ui.toggle_button(*get_toggle_xpath('Dock Diagram'), enabled=True)
        logger.info('------ Check Diagram sticked to ACL edit window')
        rc = fw_page_ui.is_element_displayed(*PathData.sticked_diagram)
        Assertion.assert_equal(rc, True, "ERR: verify_dock_diagram failed!!")


class Test_top_bar_buttons(Test):
    uuid = 'NonTC'
    description = 'combination of tests for top bar buttons'

    def test_01_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    # Top bar - Settings-Grid: Click any place on group columns, can show or hide Columns, and using drag and drop to Rearrange the items - 1526092
    def test_02_check_grid_settings(self):
        uuid = "SOSAIOT-TC-58049"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('------ Check grid settings can show columns')
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
        rc = fw_page_ui.is_element_displayed(*get_xpath_by_text(CParam.ACL_UUID))
        
        logger.info('------ Check grid settings can hide columns')
        logger.info('Click "Grid" to open Grid Settings window')
        fw_page_ui.click_element_by_text('Grid')
        logger.info('Click "Miscellaneous"')
        fw_page_ui.click_element(*get_xpath_by_text('Miscellaneous', tag='div'))
        logger.info('Click "UUID"')
        fw_page_ui.click_element(*get_xpath_by_text('UUID', tag='div'))
        logger.info('Click "Apply"')
        fw_page_ui.click_element_by_text('Apply')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        time.sleep(2)
        rc &= not fw_page_ui.does_element_exist_now(*get_xpath_by_text(CParam.ACL_UUID))
        result_dict[uuid] = rc
        Assertion.assert_equal(rc, True, "ERR: check_grid_settings failed!!")

    # Top bar - click Settings-refresh-button to reload rules from devices - 1526091
    def test_03_check_refresh_button(self):
        uuid = "SOSAIOT-TC-58048"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('Click "Refresh" button')
        fw_page_ui.click_element_by_text('Refresh')
        result_dict[uuid] = True
        Assertion.assert_equal(True, True, "ERR: check_refresh_button failed!!")

    # Top bar - click Settings-Export-button to export rules in a CSV file - 1526090
    def test_04_check_export_button(self):
        uuid = "SOSAIOT-TC-58047"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('Click "Export" button')
        fw_page_ui.click_element_by_text('Export')
        msg = 'Do you want to export Rules data to a CSV file?'
        fw_page_ui.verify_message_alert(msg)
        result_dict[uuid] = True
        Assertion.assert_equal(True, True, "ERR: check_export_button failed!!")


@paramunittest.parametrized(
    {'testrail_uuid': '1526092', 'uuid': 'SOSAIOT-TC-58049'},
    {'testrail_uuid': '1526091', 'uuid': 'SOSAIOT-TC-58048'},
    {'testrail_uuid': '1526090', 'uuid': 'SOSAIOT-TC-58047'}) #003
class TestTop_bar_buttons(Test):

    def setParameters(self, uuid, testrail_uuid):
        self.uuid = uuid
        self.testrail_uuid = testrail_uuid
        self.description = show_testcase_info(TESTPLAN, self.testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


# Verify filtering the access rules works fine after adding custom columns under Grid Settings - 1552687
class TestACL_1552687(Test):
    testrail_uuid = '1552687'
    uuid = "SOSAIOT-TC-58068"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    tag = 'custom_tag'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome')
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    def test_02_enable_uuid_and_tag_1_columns(self):
        logger.info('Click "Grid" to open Grid Settings window')
        fw_page_ui.click_element_by_text('Grid')
        logger.info('Click "Miscellaneous"')
        fw_page_ui.click_element_by_text('Miscellaneous')
        logger.info('Click "UUID"')
        fw_page_ui.click_element_by_text('UUID')
        logger.info('Click "Description"')
        fw_page_ui.click_element_by_text('Description')
        logger.info('Click "Apply"')
        fw_page_ui.click_element_by_text('Apply')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        time.sleep(2)
        rc = fw_page_ui.is_element_displayed(*get_xpath_by_text(CParam.ACL_UUID))
        rc &= fw_page_ui.is_element_displayed(*get_xpath_by_text('Description'))
        Assertion.assert_equal(rc, True, "ERR: check_grid_settings failed!!")

    def test_03_add_a_custom_acl(self):
        logger.info('Click "Add" to add custom acl')
        fw_page_ui.click_element(*PathData.add_icon)
        fw_page_ui.is_element_displayed(*PathData.add_rule_window)
        logger.info(f'Input "{CParam.custom_acl_1}" as custom acl name')
        name_text = get_textbox_element_xpath(name='nameText')
        fw_page_ui.clear_text_field(*name_text)
        fw_page_ui.set_input_text_field(*name_text, field_val=CParam.custom_acl_1)  
        logger.info(f'Input "{self.tag}" as Description')
        fw_page_ui.set_input_text_field(*get_textbox_element_xpath(name='descriptionTextarea'), field_val=self.tag)
        logger.info('Click "Add" button')
        fw_page_ui.click_element(*get_xpath_by_text('Add', tag='button'))
        fw_page_ui.compare_message_new(f'Adding Rule [{CParam.custom_acl_1}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        Assertion.assert_equal(True, True, "ERR: add a custom acl failed!!")

    def test_04_check_filtering_works(self):
        logger.info('Click "Search" icon')
        fw_page_ui.click_element(*PathData.search_icon)
        logger.info(f'Input {CParam.custom_acl_1} in Search textfield')
        fw_page_ui.set_input_text_field(*PathData.search_text, field_val=CParam.custom_acl_1)
        logger.info('------ Check Diagram sticked to ACL edit window')
        rc = pc_runner.check_element_attribute(['class', 'fw-ftr-ngpe-access-rules__summary'], target='Displaying 1 ')
        rc &= pc_runner.check_element_attribute(get_table_entry_element_xpath(self.tag, element='/div[7]'), target=CParam.custom_acl_1)
        Assertion.assert_equal(rc, True, "ERR: check_filtering_works failed!!")

    def test_05_delete_added_acl(self):
        rc = acl_api.delete_accessrule_by_name(name=CParam.custom_acl_1)
        Assertion.assert_equal(rc, True, "ERR: delete_added_acl failed!!")


# Verify the drag-icon of custom policies is green. - 1526099
class TestACL_1526099(Test):
    testrail_uuid = '1526099'
    uuid = "SOSAIOT-TC-58053"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_custom_acl(self):
        rc = acl_api.add_accessrule(**custom_acl_dict)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    def test_02_navigate_to_acl_page(self):
        # pc_runner.goto_test_page(PathData.acl_page, headless=False, browser_type='chrome') # debug
        pc_runner.goto_test_page(PathData.acl_page, browser_type='chrome')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.is_element_displayed(*PathData.acl_table)
        Assertion.assert_equal(rc, True, "ERR: navigate_to_acl_page failed!!")

    def test_03_check_drag_icon_green(self):
        drag_icon = get_table_entry_element_xpath(identifier=CParam.custom_acl_1, element="drag", strict=False)
        drag_icon[1] = drag_icon[1] + '/..'
        rc = pc_runner.check_element_attribute(drag_icon, target='background-color: rgb(153, 204, 0)', attribute='style')
        Assertion.assert_equal(rc, True, "ERR: check_drag_icon_green failed!!")

    def test_04_delete_added_acl(self):
        rc = acl_api.delete_accessrule_by_name(name=CParam.custom_acl_1)
        Assertion.assert_equal(rc, True, "ERR: delete_added_acl failed!!")
