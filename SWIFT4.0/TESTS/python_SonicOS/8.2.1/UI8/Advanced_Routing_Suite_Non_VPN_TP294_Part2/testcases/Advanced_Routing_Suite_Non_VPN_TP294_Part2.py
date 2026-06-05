from definition.settings import *

class Test_OSPFv2_edit_page(Test):
    uuid = 'NonTC'
    description = 'combination of tests in OSPFv2 edit page'

    def test_01_open_edit_ospfv2_page(self):
        pc_runner.goto_test_page(routing_page)
        # pc_runner.goto_test_page(routing_page, headless=False) # for debug
        logger.info('Navigate to "OSPFv2" tab')
        fw_page_ui.navigate_to_tab('OSPFv2')
        logger.info('Hover and Click "X0 (LAN)" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0 (LAN)')
        rc = fw_page_ui.is_element_displayed(*edit_ospfv2_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_ospfv2_page failed!!")

    # GUI: Verify the OSPFv2 drop-down list's content.- 1531393
    def test_02_check_OSPFv2_dropdown_box(self):
        uuid = "SOSAIOT-TC-55669"
        target_list = ['Disabled', 'Enabled', 'Passive']
        logger.info(f'uuid - {uuid}')
        logger.info('------ Check "OSPFv2" Dropdown box list values')
        logger.info('Click "OSPFv2" dropdown box arrow to expand')
        fw_page_ui.click_element(*ospfv2_arrow)
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Click "OSPFv2" dropdown box arrow to collapse')
        fw_page_ui.click_element(*ospfv2_arrow)
        Assertion.assert_equal(rc, True, "ERR: check_OSPFv2_dropdown_box failed!!")

    # GUI: Verify the Authentication drop-down list's content. - 1531397
    def test_03_check_Authentication_dropdown_box(self):
        uuid = "SOSAIOT-TC-55673"
        logger.info(f'uuid - {uuid}')
        logger.info('Select "OSPFv2" dropdown box as "Enabled"')
        fw_page_ui.select_drop_down_value_new('OSPFv2', 'Enabled')
        fw_page_ui.wait_for_element_to_be_visible(*auth_arrow)
        logger.info('------ Check "Authentication" Dropdown box list values')
        fw_page_ui.is_element_displayed(*auth_arrow)
        logger.info('Click "Authentication" dropdown box arrow to expand')
        fw_page_ui.click_element(*auth_arrow)
        target_list = ['Disabled', 'Simple Password', 'Message Digest', 'Key-Chain (Use CLI)']
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Click "Authentication" dropdown box arrow to collapse')
        fw_page_ui.click_element(*auth_arrow)
        Assertion.assert_equal(rc, True, "ERR: check_Authentication_dropdown_box failed!!")


@paramunittest.parametrized(
    {'uuid': 'SOSAIOT-TC-55669'},
    {'uuid': 'SOSAIOT-TC-55673'})
class TestOSPFv2_edit_page(Test):

    def setParameters(self, uuid):
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


class Test_Settings_page(Test):
    uuid = 'NonTC'
    description = 'combination of tests in settings page'

    def test_01_open_edit_settings_page(self):
        pc_runner.goto_test_page(routing_page)
        # pc_runner.goto_test_page(routing_page, headless=False) # for debug
        logger.info('Click "Settings" icon')
        fw_page_ui.click_element(*settings_icon)
        rc = fw_page_ui.is_element_displayed(*settings_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_settings_page failed!!")

    # GUI: Verify the ABR Type drop-down list's content. - 1531402
    def test_02_check_ABR_Type_dropdown_box(self):
        uuid = "SOSAIOT-TC-55678"
        logger.info(f'uuid - {uuid}')
        target_list = ['Standard', 'CISCO', 'IBM', 'Shortcut']
        logger.info('------ Check "ABR Type" Dropdown box list values')
        logger.info('Click "ABR Type" dropdown box arrow to expand')
        fw_page_ui.click_element(*abr_arrow)
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Click "ABR Type" dropdown box arrow to collapse')
        fw_page_ui.click_element(*abr_arrow)
        Assertion.assert_equal(rc, True, "ERR: check_ABR_Type_dropdown_box failed!!")

    # GUI: Verify the Metric Type drop-down list's content when the Original Default Route is used. - 1531406
    def test_03_check_Default_Route_Metric_Type_dropdown_box(self):
        uuid = "SOSAIOT-TC-55682"
        logger.info(f'uuid - {uuid}')
        logger.info('Select "Originate Default Route" dropdown box as "Always"')
        fw_page_ui.select_drop_down_value_new('Originate Default Route', 'Always')
        res = not pc_runner.check_element_attribute(default_metric_dropdown_box, 'sw-select--disabled', 'class')
        logger.info(f'Check "Metric Type" is editable...... {res}')
        logger.info('------ Check Default Route "Metric Type" Dropdown box list values')
        logger.info('Click "Metric Type" dropdown box to expand')
        fw_page_ui.click_element(*default_metric_dropdown_box)
        target_list = ['External Type 1', 'External Type 2']
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Select "Originate Default Route" dropdown box as "Never" to collapse dropdown box')
        fw_page_ui.select_drop_down_value_new('Originate Default Route', 'Never')
        Assertion.assert_equal(rc, True, "ERR: check_Default_Route_Metric_Type_dropdown_box failed!!")

    # GUI: Verify that the Metric, Tag, and Metric Type become available when the Advertise Static Routes check box is turned on. - 1531408
    def test_04_check_Redistribute_Static_Routes_Metric_settings_available(self):
        uuid = "SOSAIOT-TC-55684"
        logger.info(f'uuid - {uuid}')
        logger.info('Enable "Redistribute Static Routes" toggle')
        fw_page_ui.toggle_button(*asr_toggle, enabled=True)
        metric = not pc_runner.check_element_attribute(asr_metric, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Metric" is editable...... {metric}')
        tag = not pc_runner.check_element_attribute(asr_tag, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Tag" is editable...... {tag}')
        metric_type = not pc_runner.check_element_attribute(asr_dropdown_box, 'sw-select--disabled', 'class')
        logger.info(f'Check "Metric Type" is editable...... {metric_type}')
        result_dict[uuid] = metric & tag & metric_type
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check Redistribute_Static_Routes_Metric_settings  are available failed!!")

    # GUI: Verify the Metric Type drop-down list's content when the Advertise Static Routes is used. - 1531411
    def test_05_check_Redistribute_Static_Routes_Metric_Type_dropdown_box(self):
        uuid = "SOSAIOT-TC-55687"
        logger.info(f'uuid - {uuid}')
        logger.info('------ Check Redistribute Static Routes "Metric Type" Dropdown box list values')
        logger.info('Click "Metric Type" dropdown box to expand')
        fw_page_ui.click_element(*asr_dropdown_box)
        target_list = ['External Type 1', 'External Type 2']
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Disable "Redistribute Static Routes" toggle to to collapse dropdown box')
        fw_page_ui.toggle_button(*asr_toggle, enabled=False)
        Assertion.assert_equal(rc, True, "ERR: check_Redistribute_Static_Routes_Metric_Type_dropdown_box failed!!")

    # GUI: Verify that the Metric, Tag, and Metric Type become available when the Advertise Connected Networks check box is turned on. - 1531412
    def test_06_check_Redistribute_Connected_Networks_Metric_settings_available(self):
        uuid = "SOSAIOT-TC-55688"
        logger.info(f'uuid - {uuid}')
        logger.info('Enable "Redistribute Connected Networks" toggle')
        fw_page_ui.toggle_button(*rcn_toggle, enabled=True)
        metric = not pc_runner.check_element_attribute(rcn_metric, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Metric" is editable...... {metric}')
        tag = not pc_runner.check_element_attribute(rcn_tag, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Tag" is editable...... {tag}')
        metric_type = not pc_runner.check_element_attribute(rcn_dropdown_box, 'sw-select--disabled', 'class')
        logger.info(f'Check "Metric Type" is editable...... {metric_type}')
        result_dict[uuid] = metric & tag & metric_type
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_Redistribute_Connected_Networks_Metric_settings  are available failed!!")

    # GUI: Verify the Metric Type drop-down list's content when the Advertise Connected Networks is used. - 1531415
    def test_07_check_Redistribute_Connected_Networks_Metric_Type_dropdown_box(self):
        uuid = "SOSAIOT-TC-55691"
        logger.info(f'uuid - {uuid}')
        logger.info('------ Check Redistribute Connected Networks "Metric Type" Dropdown box list values')
        logger.info('Click "Metric Type" dropdown box to expand')
        fw_page_ui.click_element(*rcn_dropdown_box)
        target_list = ['External Type 1', 'External Type 2']
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Disable "Redistribute Connected Networks" toggle to to collapse dropdown box')
        fw_page_ui.toggle_button(*rcn_toggle, enabled=False)
        Assertion.assert_equal(rc, True, "ERR: check_Redistribute_Connected_Networks_Metric_Type_dropdown_box failed!!")

    # GUI: Verify that the Metric, Tag, and Metric Type become available when the Redistribute RIP Routes check box is turned on. - 1531416
    def test_08_check_Redistribute_RIP_Routes_Metric_settings_available(self):
        uuid = "SOSAIOT-TC-55692"
        logger.info(f'uuid - {uuid}')
        logger.info('Enable "Redistribute RIP Routes" toggle')
        fw_page_ui.toggle_button(*rrr_toggle, enabled=True)
        metric = not pc_runner.check_element_attribute(rrr_metric, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Metric" is editable...... {metric}')
        tag = not pc_runner.check_element_attribute(rrr_tag, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Tag" is editable...... {tag}')
        metric_type = not pc_runner.check_element_attribute(rrr_dropdown_box, 'sw-select--disabled', 'class')
        logger.info(f'Check "Metric Type" is editable...... {metric_type}')
        result_dict[uuid] = metric & tag & metric_type
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_Redistribute_RIP_Routes_Metric_settings  are available failed!!")

    # GUI: Verify the Metric Type drop-down list's content when the Redistribute RIP Routes is used. - 1531420
    def test_09_check_Redistribute_RIP_Routes_Metric_Type_dropdown_box(self):
        uuid = "SOSAIOT-TC-55695"
        logger.info(f'uuid - {uuid}')
        logger.info('------ Check Redistribute RIP Routes "Metric Type" Dropdown box list values')
        logger.info('Click "Metric Type" dropdown box to expand')
        fw_page_ui.click_element(*rrr_dropdown_box)
        target_list = ['External Type 1', 'External Type 2']
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Disable "Redistribute RIP Routes" toggle to to collapse dropdown box')
        fw_page_ui.toggle_button(*rrr_toggle, enabled=False)
        Assertion.assert_equal(rc, True, "ERR: check_Redistribute_RIP_Routes_Metric_Type_dropdown_box failed!!")

    # GUI: Verify that the Metric, Tag, and Metric Type become available when the Advertise Remote VPN Networks check box is turned on. - 1531421
    def test_10_check_Redistribute_Remote_VPN_Networks_Metric_settings_available(self):
        uuid = "SOSAIOT-TC-55696"
        logger.info(f'uuid - {uuid}')
        logger.info('Scroll view to "Redistribute Remote VPN Networks" toggle')
        fw_page_ui.scroll_view_to_element(*rrvn_toggle)
        logger.info('Enable "Redistribute Remote VPN Networks" toggle')
        fw_page_ui.toggle_button(*rrvn_toggle, enabled=True)
        metric = not pc_runner.check_element_attribute(rrvn_metric, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Metric" is editable...... {metric}')
        tag = not pc_runner.check_element_attribute(rrvn_tag, 'sw-textfield--disabled', 'class')
        logger.info(f'Check "Tag" is editable...... {tag}')
        metric_type = not pc_runner.check_element_attribute(rrvn_dropdown_box, 'sw-select--disabled', 'class')
        logger.info(f'Check "Metric Type" is editable...... {metric_type}')
        result_dict[uuid] = metric & tag & metric_type
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check Redistribute_Remote_VPN_Networks_Metric_settings are available failed!!")


@paramunittest.parametrized(
    {'uuid': 'SOSAIOT-TC-55678'},
    {'uuid': 'SOSAIOT-TC-55682'},
    {'uuid': 'SOSAIOT-TC-55684'},
    {'uuid': 'SOSAIOT-TC-55687'},
    {'uuid': 'SOSAIOT-TC-55688'},
    {'uuid': 'SOSAIOT-TC-55691'},
    {'uuid': 'SOSAIOT-TC-55692'},
    {'uuid': 'SOSAIOT-TC-55695'},
    {'uuid': 'SOSAIOT-TC-55696'}) #009
class TestSettings_page(Test):

    def setParameters(self, uuid):
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


class Test_RIP_page(Test):
    uuid = 'NonTC'
    description = 'combination of tests in RIP edit page'

    def test_01_open_edit_rip_window(self):
        pc_runner.goto_test_page(routing_page)
        logger.info('Navigate to "RIP" tab')
        fw_page_ui.navigate_to_tab('RIP')
        logger.info('Hover and Click "X0" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0 (LAN)')
        rc = fw_page_ui.is_element_displayed(*edit_rip_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_rip_window failed!!")

    # GUI: Verify the RIP drop-down list's content. - 1531437
    def test_02_check_RIP_dropdown_box(self):
        # jira = 'GEN8-10277'
        uuid = "SOSAIOT-TC-55712"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        target_list = ['Disabled', 'Send and Receive', 'Send Only', 'Receive Only', 'Passive'] # 8.0.3
        # target_list = ['Disabled', 'Send and Recieve', 'Send Only', 'Recieve Only', 'Passive']
        logger.info('------ Check "RIP" Dropdown box list values')
        logger.info('Click "RIP" dropdown box arrow to expand')
        fw_page_ui.click_element(*rip_arrow)
        rc = pc_runner.check_dropdown_list_value(target_list)
        result_dict[uuid] = rc
        logger.info('Click "RIP" dropdown box arrow to collapse')
        fw_page_ui.click_element(*rip_arrow)
        Assertion.assert_equal(rc, True, "ERR: check_ABR_Type_dropdown_box failed!!")

    # GUI: Verify that the Use Password check box is not available with RIPv1 selection. - 1531446
    def test_03_check_password_status(self):
        uuid = "SOSAIOT-TC-55720"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('Select "RIP" dropdown box as "Send and Receive"')
        # fw_page_ui.select_drop_down_value_new('RIP', 'Send and Recieve')
        fw_page_ui.select_drop_down_value_new('RIP', 'Send and Receive')
        logger.info('Select "Receive" dropdown box as "RIPv1"')
        fw_page_ui.select_drop_down_value_new('Receive', 'RIPv1')
        logger.info('Select "Send" dropdown box as "RIPv1"')
        fw_page_ui.select_drop_down_value_new('Send', 'RIPv1')
        logger.info('------ Check "Use Password" checkbox is not available')
        res = pc_runner.check_element_attribute(password_checkbox, 'sw-checkbox--disabled', 'class')
        logger.info('------ Check "Password" textfield is not available')
        rc = pc_runner.check_element_attribute(password_textbox, 'sw-textfield--disabled', 'class')
        result_dict[uuid] = rc & res
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_password_status failed!!")

    # GUI: GUI: Verify that the Poisoned Reverse check box is not available if Split Horizon is turned off. - 1531462
    def test_04_check_Poisoned_Reverse_checkbox(self):
        uuid = "SOSAIOT-TC-55735"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('------ Check "Split Horizon" checkbox is turned off')
        fw_page_ui.checkbox_button(*split_checkbox_edit, enable=False)
        logger.info('------ Check "Poisoned Reverse" checkbox is not available')
        rc_poison = pc_runner.check_element_attribute(poison_checkbox, 'sw-checkbox--disabled', 'class')
        result_dict[uuid] = rc_poison
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_Poisoned_Reverse_checkbox failed!!")

    # GUI: Verify that the Global RIP Configuration section is not available when Receive Only mode is used. - 1531454
    def test_05_check_receive_only_mode(self):
        uuid = "SOSAIOT-TC-55728"
        logger.info(f'uuid - {uuid}')
        result_dict[uuid] = False
        logger.info('Select "RIP" dropdown box as "Receive Only"')
        # fw_page_ui.select_drop_down_value_new('RIP', 'Recieve Only')
        fw_page_ui.select_drop_down_value_new('RIP', 'Receive Only') # 8.0.3
        logger.info('------ Check "Split Horizon" checkbox is not available')
        rc_split = pc_runner.check_element_attribute(split_checkbox, 'sw-checkbox--disabled', 'class')
        logger.info('------ Check "Poisoned Reverse" checkbox is not available')
        rc_poison = pc_runner.check_element_attribute(poison_checkbox, 'sw-checkbox--disabled', 'class')
        logger.info('------ Check "Send" dropdown box is not available')
        rc_send = pc_runner.check_element_attribute(send_dropdown, 'sw-select--disabled', 'class')
        result_dict[uuid] = rc_split & rc_poison & rc_send
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_receive_only_mode failed!!")


@paramunittest.parametrized(
    {'uuid': 'SOSAIOT-TC-55712'},
    {'uuid': 'SOSAIOT-TC-55720'},
    {'uuid': 'SOSAIOT-TC-55735'},
    {'uuid': 'SOSAIOT-TC-55728'}) #004
class TestRIP_page(Test):

    def setParameters(self, uuid):
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")
