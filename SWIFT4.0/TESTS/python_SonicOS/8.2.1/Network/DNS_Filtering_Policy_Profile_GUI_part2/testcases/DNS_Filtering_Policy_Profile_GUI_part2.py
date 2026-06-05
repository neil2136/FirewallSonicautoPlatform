from definition.settings import *
from definition.utils import *
from definition.database import *

# [GUI] Verify DNS Policy cannot be configured when GUI is in Non-config mode.
class TestPolicy_1521109(Test):
    uuid = "SOSAIOT-TC-51487"
    testrail_uuid = '1521109'
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_switch_to_non_config_mode(self):
        init_test_page(dns_policy_page)
        logger.info('Click "Non-Config"')
        fw_page_ui.toggle_button(*config_button, enabled=False)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = check_element_attribute(config_button, target='sw-toggle--off', attribute='class')
        Assertion.assert_equal(rc, True, "ERR: switch_to_non_config_mode failed!!")

    def test_02_add_dns_policy_failed(self):
        logger.info('Click Add to Open Add DNS Policy window')
        fw_page_ui.click_element_by_text("Top")
        logger.info('Click "Filter" Action')
        fw_page_ui.click_element_by_text('Filter')
        logger.info('Click "Add"')
        fw_page_ui.click_element_by_text('Add')
        logger.info('------ Check "Non config mode." message prompted')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        msg = ['Non config mode.', 'Non config mode', 'You have been successfully switched to non-config mode.']
        rc = fw_page_ui.compare_alert_message(msg)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy_should fail!!")


class Test_Policy_Page(Test):
    uuid = 'NonTC'
    description = 'Combination test of Action button and Name'

    def test_00_open_add_dns_policy_window(self):
        init_test_page(dns_policy_page)
        logger.info('Click Add to Open Add DNS Policy window')
        fw_page_ui.click_element_by_text("Top")
        Assertion.assert_equal(True, True, "ERR: open_add_dns_policy_window failed!!")

    # [GUI] Verify the correct info displays when mouse hovers on the Action buttons
    def test_01_check_action_info(self):
        uuid = "SOSAIOT-TC-51470"
        logger.info(f'------ Check Action Proxy info - {uuid}')
        fw_page_ui.move_to_the_element(*proxy_action, visible=True)
        rc_proxy = check_element_attribute(action_info, 'Firewall will proxy packets matching this rule.')
        logger.info(f'------ Check Action Filter info - {uuid}')
        fw_page_ui.move_to_the_element(*filter_action, visible=True)
        info = 'Firewall will proxy connections matching this rule with 4to4 mode and take actions specified in the profile. Actions could be allow/block/negative/forged ip.License is needed for DNS Filtering'
        rc_filter = check_element_attribute(action_info, info)
        result_dict[uuid] = rc_filter & rc_proxy
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_action info failed!!")

    #  [GUI] Verify the Mode options display when Action 'Proxy' is selected
    def test_02_check_mode_with_proxy(self):
        uuid = "SOSAIOT-TC-51471"
        logger.info(f'------ Check Mode with Proxy Action - {uuid}')
        logger.info('Click Proxy Action')
        fw_page_ui.click_element_by_text('Proxy')
        result_dict[uuid] = check_element_attribute(selected_proxy_mode, '4to4')
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_mode_with_proxy failed!!")

    #  [GUI] Verify the Filtering Profile drop-down box displays when Action 'Filter' is selected.
    def test_03_check_profile_dropdown_box_with_filter(self):
        uuid = "SOSAIOT-TC-51468"
        logger.info(f'------ Check Profile Dropdown box with Filter Action - {uuid}')
        logger.info('Click Filter Action')
        fw_page_ui.click_element_by_text('Filter')
        result_dict[uuid] = check_element_attribute(profile_box_text, 'Default Profile')
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_profile_dropdown_box_with_filter failed!!")

    # [GUI] Verify the DNS Policy is named as 'My Rule' by default
    def test_04_check_default_name(self):
        uuid = "SOSAIOT-TC-51508"
        logger.info(f'------ Check policy default name - {uuid}')
        result_dict[uuid] = check_element_attribute(policy_name, 'My Rule', attribute='value')
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_result failed!!")


@paramunittest.parametrized(
    {'testrail_uuid': '1521089', 'uuid': 'SOSAIOT-TC-51470'},
    {'testrail_uuid': '1521090', 'uuid': 'SOSAIOT-TC-51471'},
    {'testrail_uuid': '1521087', 'uuid': 'SOSAIOT-TC-51468'},
    {'testrail_uuid': '2268491', 'uuid': 'SOSAIOT-TC-51508'})
class TestPolicy_Page(Test):

    def setParameters(self, uuid, testrail_uuid):
        self.uuid = uuid
        self.testrail_uuid = testrail_uuid
        self.description = show_testcase_info(TESTPLAN, self.testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


class TestInit(Test):
    uuid = 'NonTC'
    description = 'init profile schedule address policies ...'

    def test_01_delete_added_profiles(self):
        rc = dnsFilter_cli.delete_filtering_profile()
        Assertion.assert_equal(rc, True, "ERR: init failed!!")

    def test_02_delete_added_schedules(self):
        rc = schedule_cli.rem_all_schedule()
        Assertion.assert_equal(rc, True, "ERR: init failed!!")

    def test_03_delete_added_address_objects(self):
        rc = ao_cli.del_address_objects('ipv4')
        Assertion.assert_equal(rc, True, "ERR: init failed!!")

    def test_04_delete_added_address_groups(self):
        rc = ao_cli.del_address_groups('ipv4')
        Assertion.assert_equal(rc, True, "ERR: init failed!!")

    def test_05_delete_added_policies(self):
        rc = dnsPolicy_cli.delete_dns_policy()
        Assertion.assert_equal(rc, True, "ERR: init failed!!")


# Verify Filtering Profile drop-down box and edit icon work.
class TestPolicy_1521088(Test):
    testrail_uuid = '1521088'
    uuid = "SOSAIOT-TC-51469"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    target_list = ['Default Profile',]

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_some_different_profiles(self):
        profile = copy.deepcopy(profile_dict)
        for i in range(3):
            name = CParam.Name + str(i)
            profile['dns_security']['dns_filtering']['profile'][0]['name'] = name
            logger.info(profile)
            rc = dnsFilter_api.add_dns_filtering_profile(**profile)
            if not rc:
                logger.error(f'Add dns filtering profile {i} failed!!')
                break
            self.target_list.append(name)
        Assertion.assert_equal(rc, True, "ERR: add_some_different_profiles failed!!")

    def test_02_check_and_select_profile(self):
        init_test_page(dns_policy_page)
        logger.info('Click Add "Top" to Open "Add DNS Policy" window')
        fw_page_ui.click_element_by_text("Top")
        logger.info('Click "Filter" Action')
        fw_page_ui.click_element_by_text("Filter")
        logger.info('------ Check dropdown box content')
        logger.info('Click "Profile" dropdown box')
        fw_page_ui.click_element(*profile_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info(test)
        fw_page_ui.click_element(*profile_arrow)
        rc = test == self.target_list
        logger.info(rc)
        logger.info('------ Check select custom profiles')
        for profile in self.target_list:
            logger.info(f'Select {profile}')
            fw_page_ui.select_drop_down_value_new('Profile', profile)
            rc &= check_element_attribute(profile_box_text, profile)
            if not rc:
                logger.error(f'Check and select profile {profile} failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: check_and_select_profile failed!!")

    def test_03_add_new_profile_via_edit_pencil(self):
        name = 'test'
        logger.info('Click "Profile" edit pencil')
        fw_page_ui.click_element(*profile_pencil)
        logger.info('Click "New Filter Profile Object"')
        fw_page_ui.click_element_by_text("New Filter Profile Object")
        logger.info(f'Config profile "Name" as "{name}"')
        fw_page_ui.set_input_text_field('name', 'profileObjectName', name)
        logger.info('Select "Adult" dropdown box as "Allow"')
        fw_page_ui.select_drop_down_value_new('Adult', 'Allow')
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc &= check_element_attribute(profile_box_text, name)
        Assertion.assert_equal(rc, True, "ERR: check_and_select_profile failed!!")

    def test_04_select_and_edit(self):
        logger.info('Click "Profile" edit pencil')
        fw_page_ui.click_element(*profile_pencil)
        logger.info('Click "Edit Filter Profile Object"')
        fw_page_ui.click_element_by_text("Edit Filter Profile Object")
        logger.info('Select "Adult" dropdown box as "Block"')
        fw_page_ui.select_drop_down_value_new('Adult', 'Block')
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: select_and_edit failed!!")


# [GUI] Verify the Schedule drop-down box and edit icon work.
class TestPolicy_1521092(Test):
    testrail_uuid = '1521092'
    uuid = "SOSAIOT-TC-51472"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_and_select_schedule(self):
        # # ---- debug ----
        init_test_page(dns_policy_page)
        logger.info('Click Add "Top" to Open "Add DNS Policy" window')
        fw_page_ui.click_element_by_text("Top")
        logger.info('Click "Filter" Action')
        fw_page_ui.click_element_by_text("Filter")
        # # --------
        logger.info('------ Check dropdown box content')
        logger.info('Click "Schedule" dropdown box')
        fw_page_ui.click_element(*schedule_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info(test)
        fw_page_ui.click_element(*schedule_arrow)
        res = [bool(test)]
        for schedule in test:
            logger.info(f'------ Check select schedule {schedule}')
            fw_page_ui.select_drop_down_value_new('Schedule', schedule)
            rc = check_element_attribute(schedule_box_text, schedule)
            if not rc:
                logger.error(f'Check and select schedule {schedule} failed!!')
            res.append(rc)
        Assertion.assert_equal(all(res), True, "ERR: check_and_select_schedule failed!!")

    def test_02_select_and_edit(self):
        schedule = 'Work Hours'
        logger.info(f'Select "Schedule" dropdown box as "{schedule}"')
        fw_page_ui.select_drop_down_value_new('Schedule', schedule)
        logger.info('Click "Schedule" edit pencil')
        fw_page_ui.click_element(*schedule_pencil)
        logger.info('Click "Edit Schedule Object"')
        fw_page_ui.click_element_by_text("Edit Schedule Object")
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_error_message(f'Edit Schedule Object [{schedule}] Successfully.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: select_and_edit failed!!")

    def test_03_add_new_schedule_via_edit_pencil(self):
        name = 'test'
        logger.info('Click "Schedule" edit pencil')
        fw_page_ui.click_element(*schedule_pencil)
        logger.info('Click "New Schedule Object"')
        fw_page_ui.click_element_by_text("New Schedule Object")
        logger.info(f'Config schedule "Name" as "{name}"')
        fw_page_ui.set_input_text_field('name', 'schedule-name', name)
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_error_message(f'Add Schedule Object [{name}] Successfully.')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc &= check_element_attribute(schedule_box_text, name)
        Assertion.assert_equal(rc, True, "ERR: check_and_select_schedule failed!!")


# [GUI] Verify the Address drop-down box and edit icon work.
class TestPolicy_1521097(Test):
    testrail_uuid = '1521097'
    uuid = "SOSAIOT-TC-51476"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    object = 'custom'
    group = 'custom_group'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_and_select_address(self):
        # ---- debug ----
        init_test_page(dns_policy_page)
        logger.info('Click Add "Top" to Open "Add DNS Policy" window')
        fw_page_ui.click_element_by_text("Top")
        logger.info('Click "Filter" Action')
        fw_page_ui.click_element_by_text("Filter")
        # --------
        logger.info('------ Check dropdown box content')
        logger.info('Click "Address" dropdown box')
        fw_page_ui.click_element(*address_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info(test)
        fw_page_ui.click_element(*address_arrow)
        res = [bool(test)]
        for address in test:
            logger.info(f'------ Check select address {address}')
            fw_page_ui.select_drop_down_value_new('Address', address)
            rc = check_element_attribute(address_box_text, address)
            if not rc:
                logger.error(f'Check and select address {address} failed!!')
            res.append(rc)
        Assertion.assert_equal(all(res), True, "ERR: check_and_select_address failed!!")

    def test_02_add_new_address_via_edit_pencil(self):
        logger.info('Click "Address" edit pencil')
        fw_page_ui.click_element(*address_pencil)
        logger.info('Click "New Address Object"')
        fw_page_ui.click_element_by_text("New Address Object")
        logger.info(f'Config address "Name" as "{self.object}"')
        fw_page_ui.set_input_text_field('name', 'name', self.object)
        fw_page_ui.set_input_text_field('name', 'ip-address', '1.2.3.4')
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_message_new(f'Add Address Object [{self.object}] successfully.')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc &= check_element_attribute(address_box_text, self.object)
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: check_and_select_address failed!!")

    def test_03_select_and_edit(self):
        logger.info(f'Select "Address" dropdown box as "{self.object}"')
        fw_page_ui.select_drop_down_value_new('Address', self.object)
        logger.info('Click "Address" edit pencil')
        fw_page_ui.click_element(*address_pencil)
        logger.info('Click "Edit Address Object"')
        fw_page_ui.click_element_by_text("Edit Address Object")
        fw_page_ui.set_input_text_field('name', 'ip-address', '1.2.3.5')
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_message_new(f'Edit Address Object [{self.object}] successfully.')
        # rc = fw_page_ui.compare_error_message(f'Edit Address Object [{self.object}] successfully.')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: select_and_edit failed!!")

    def test_04_add_new_address_group_via_edit_pencil(self):
        logger.info('Click "Address" edit pencil')
        fw_page_ui.click_element(*address_pencil)
        logger.info('Click "New Address Group"')
        fw_page_ui.click_element_by_text("New Address Group")
        logger.info(f'Config address group "Name" as "{self.group}"')
        fw_page_ui.set_input_text_field('name', 'name', self.group)
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_message_new(f'Add Address Object Group [{self.group}] successfully.')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc &= check_element_attribute(address_box_text, self.group)
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: check_and_select_address failed!!")

    def test_05_select_and_edit_group(self):
        logger.info(f'Select "Address" dropdown box as "{self.group}"')
        fw_page_ui.select_drop_down_value_new('Address', self.group)
        logger.info('Click "Address" edit pencil')
        fw_page_ui.click_element(*address_pencil)
        logger.info('Click "Edit Address Group"')
        fw_page_ui.click_element_by_text("Edit Address Group")
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        # rc = fw_page_ui.compare_error_message(f'Edit Address Object Group [{self.group}] successfully.')
        rc = fw_page_ui.compare_message_new(f'Edit Address Object Group [{self.group}] successfully.')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: select_and_edit failed!!")


# [GUI] Verify the Service drop-down box lists 3 entries and can be selected when Action is Proxy.
class TestPolicy_1521099(Test):
    testrail_uuid = '1521099'
    uuid = "SOSAIOT-TC-51478"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_and_select_service_proxy(self):
        target_list = ['DNS (Name Service)', 'DNS (Name Service) TCP', 'DNS (Name Service) UDP']
        init_test_page(dns_policy_page)
        logger.info('Click Add "Top" to Open "Add DNS Policy" window')
        fw_page_ui.click_element_by_text("Top")
        logger.info('Click "Proxy" Action')
        fw_page_ui.click_element_by_text("Proxy")
        logger.info('------ Check dropdown box content')
        logger.info('Click "Service" dropdown box')
        fw_page_ui.click_element(*service_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info(test)
        fw_page_ui.click_element(*service_arrow)
        res = [test == target_list]
        for service in test:
            logger.info(f'------ Check select service {service}')
            fw_page_ui.select_drop_down_value_new('Service', service)
            rc = check_element_attribute(service_box_text, service)
            if not rc:
                logger.error(f'Check and select service {service} failed!!')
            res.append(rc)
        Assertion.assert_equal(all(res), True, "ERR: check_and_select_service failed!!")

    def test_02_check_and_select_service_filter(self):
        target = 'DNS (Name Service) UDP'
        logger.info('Click "Filter" Action')
        fw_page_ui.click_element_by_text("Filter")
        res = [check_element_attribute(service_box_text, target)]
        logger.info('------ Check dropdown box content')
        logger.info('Click "Service" dropdown box')
        fw_page_ui.click_element(*service_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info(test)
        fw_page_ui.click_element(*service_arrow)
        res.append(len(test) == 1 and test[0] == target)
        logger.info(res[0])
        for service in test:
            logger.info(f'------ Check select service {service}')
            fw_page_ui.select_drop_down_value_new('Service', service)
            rc = check_element_attribute(service_box_text, service)
            if not rc:
                logger.error(f'Check and select service {service} failed!!')
            res.append(rc)
        Assertion.assert_equal(all(res), True, "ERR: check_and_select_service failed!!")


#  [GUI] Verify the Move icons and drag policy work.
class TestPolicy_1521105(Test):
    testrail_uuid = "1521105"
    uuid = "SOSAIOT-TC-51484"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    name = CParam.Name
    policy_priority = get_table_entry_element_xpath(name, policy_priority_part)

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_some_different_policies(self):
        policy = copy.deepcopy(dns_filter_dict)
        proxy = dnsRule_api.add_dns_rule(**dns_proxy_dict)
        for i in range(2):
            name = f'filter{i}'
            policy['dns_policies'][0]['name'] = name
            rc = dnsRule_api.add_dns_rule(**policy)
            if not rc:
                logger.error(f'Add dns policy {name} failed!!')
                break
        Assertion.assert_equal(proxy & rc, True, "ERR: add_some_different_policies failed!!")

    def test_02_select_and_move_up_policy(self):
        init_test_page(dns_policy_page)
        priority = fw_page_ui.get_attribute_value(*self.policy_priority, attrib_to_get_val='textContent')
        logger.info(priority)
        logger.info(f'Select proxy policy {self.name}')
        fw_page_ui.click_element(*policy_checkbox)
        logger.info('Click "Move UP"')
        fw_page_ui.click_element(*move_up_button)
        logger.info('Confirm "Move Up"')
        fw_page_ui.verify_error_message_alert(f'Are you sure you want to move rule [{self.name}]')
        fw_page_ui.compare_error_message(f'Moving rule [{self.name}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info('------ Check priority')
        rc = check_element_attribute(self.policy_priority, str(int(priority) - 1))
        Assertion.assert_equal(rc, True, "ERR: select_and_move_up_policy failed!!")

    def test_03_select_and_move_down_policy(self):
        priority = fw_page_ui.get_attribute_value(*self.policy_priority, attrib_to_get_val='textContent')
        logger.info(priority)
        logger.info('Click "Move Down"')
        fw_page_ui.click_element(*move_down_button)
        logger.info('Confirm "Move Down"')
        fw_page_ui.verify_error_message_alert(f'Are you sure you want to move rule [{self.name}]')
        fw_page_ui.compare_error_message(f'Moving rule [{self.name}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info('------ Check priority')
        rc = check_element_attribute(self.policy_priority, str(int(priority) + 1))
        Assertion.assert_equal(rc, True, "ERR: select_and_move_down_policy failed!!")

    def test_04_drag_and_move_policy(self):
        # init_test_page(dns_policy_page) #debug
        priority = fw_page_ui.get_attribute_value(*self.policy_priority, attrib_to_get_val='textContent')
        logger.info(priority)
        logger.info(f'Drag and move proxy policy {self.name}')
        fw_page_ui.drag_and_drop_by_offset(*policy_drag, xoffset=0, yoffset=-45)
        logger.info('Confirm "Drag and move"')
        fw_page_ui.verify_error_message_alert(f'Are you sure you want to move rule [{self.name}]?')
        fw_page_ui.compare_error_message(f'Moving rule [{self.name}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info('------ Check priority')
        rc = check_element_attribute(self.policy_priority, str(int(priority) - 1))
        Assertion.assert_equal(rc, True, "ERR: drag_and_move_policy failed!!")


#  [GUI] Verify the Clone buttons work.
class TestPolicy_1521107(Test):
    testrail_uuid = "1521107"
    uuid = "SOSAIOT-TC-51485"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    name = 'TestClone'
    policy_priority = get_table_entry_element_xpath(name, policy_priority_part)
    policy_checkbox = get_table_entry_element_xpath(name, 'checkbox')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_dns_policy(self):
        policy = copy.deepcopy(dns_filter_dict)
        policy['dns_policies'][0]['name'] = self.name
        rc = dnsRule_api.add_dns_rule(**policy)
        Assertion.assert_equal(rc, True, "ERR: add_dns_policy failed!!")

    def test_02_select_and_clone_up_policy(self):
        init_test_page(dns_policy_page)
        logger.info(f'Get dns policy {self.name} priority')
        policy_priority = get_table_entry_element_xpath(self.name, policy_priority_part)
        priority = fw_page_ui.get_attribute_value(*policy_priority, attrib_to_get_val='textContent')
        logger.info(priority)
        logger.info(f'Select dns policy {self.name}')
        policy_checkbox = get_table_entry_element_xpath(self.name, 'checkbox')
        fw_page_ui.click_element(*policy_checkbox)
        logger.info('Click "Clone UP"')
        fw_page_ui.click_element(*clone_up_button)
        logger.info('Confirm "Clone Up"')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.verify_error_message_alert(f"Are you sure you want to Clone Rule '{self.name}'?")
        fw_page_ui.compare_error_message(f'Cloning rule [{self.name}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info(f'Un-select dns policy {self.name}')
        fw_page_ui.click_element(*policy_checkbox)
        logger.info(f'------ Check {self.name} priority')
        rc = check_element_attribute(self.policy_priority, str(int(priority) + 1))
        logger.info(f'------ Check {self.name}_clone priority')
        clone_priority = get_table_entry_element_xpath(self.name + '_clone', policy_priority_part)
        rc_clone = check_element_attribute(clone_priority, priority)
        Assertion.assert_equal(rc & rc_clone, True, "ERR: select_and_clone_up_policy failed!!")

    def test_03_select_and_clone_down_policy(self):
        name = self.name + '_clone'
        policy_priority = get_table_entry_element_xpath(name, policy_priority_part)
        priority = fw_page_ui.get_attribute_value(*policy_priority, attrib_to_get_val='textContent')
        logger.info(f'Select dns policy {name}')
        policy_checkbox = get_table_entry_element_xpath(name, 'checkbox')
        fw_page_ui.click_element(*policy_checkbox)
        logger.info('Click "Clone Down"')
        fw_page_ui.click_element(*clone_down_button)
        logger.info('Confirm "Clone Down"')
        fw_page_ui.wait_for_element_to_load(*status_info)
        fw_page_ui.verify_error_message_alert(f"Are you sure you want to Clone Rule '{name}'?")
        fw_page_ui.compare_error_message(f'Cloning rule [{name}] was successful.')
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        logger.info(f'------ Check {name} priority')
        rc = check_element_attribute(policy_priority, priority)
        logger.info(f'------ Check {name}_clone priority')
        clone_priority = get_table_entry_element_xpath(name + '_clone', policy_priority_part)
        rc_clone = check_element_attribute(clone_priority, str(int(priority) + 1))
        Assertion.assert_equal(rc & rc_clone, True, "ERR: select_and_clone_up_policy failed!!")


#  [GUI] [GUI] Verify Export DNS Policies to CSV file.
class TestPolicy_1521108(Test):
    testrail_uuid = "1521108"
    uuid = "SOSAIOT-TC-51486"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_export_csv_file(self):
        init_test_page(dns_policy_page)
        logger.info('Click "Export"')
        fw_page_ui.click_element_by_text("Export")
        logger.info('Confirm "Export"')
        fw_page_ui.verify_error_message_alert("Do you want to export Rules data to a CSV file?")
        Assertion.assert_equal(True, True, "ERR: check_and_select_service failed!!")


class Test_Profile_Page(Test):
    uuid = 'NonTC'
    description = "DNS filtering profile page UI check"

    def test_00_navigate_to_profile_page(self):
        init_test_page(dns_profile_page)
        Assertion.assert_equal(True, True, "ERR: navigate_to_profile_page failed!!")

    #  [GUI] Verify the checkbox of the Default profile is grey and not selected.
    def test_01_check_default_profile_checkbox_is_unselected(self):
        uuid = "SOSAIOT-TC-51490"
        logger.info(f'------ Check the checkbox of the Default profile is unselected - {uuid}')
        default_profile_checkbox = get_table_entry_element_xpath('Default Profile', 'checkbox')
        rc = check_element_attribute(default_profile_checkbox, target='sw-checkbox--disabled', attribute='class')
        result_dict[uuid] = rc
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_default_profile_checkbox_is_unselected failed!!")

    # Verify the profile table columns: Name, Allow Category, Block Category, Negative reply Category,Forged IP Reply Category.
    def test_02_check_the_profile_table_columns_content(self):
        uuid = "SOSAIOT-TC-51495"
        logger.info(f'------ Check the profile table columns - {uuid}')
        rc = []
        for name in ['Name', 'Allow Category', 'Block Category', 'Negative Reply Category', 'Forged IP Reply Category']:
            path = get_xpath_by_text(name)
            res = check_element_attribute(path, target=profile_column_class, attribute='class')
            if not res:
                logger.error(f'Check column {name} failed!!')
            rc.append(res)
        result_dict[uuid] = all(rc)
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_the_profile_table_columns_content failed!!")

    # [GUI] Verify Add, Delete and Refresh buttons are provided at the top of the Profile Objects table.
    def test_03_check_the_table_top_buttons(self):
        uuid = "SOSAIOT-TC-51497"
        logger.info(f'------ Check the table top buttons - {uuid}')
        rc = []
        for name in ['Add', 'Delete', 'Refresh']:
            path = get_xpath_by_text(name)
            res = check_element_attribute(path, target=profile_top_button_class, attribute='class')
            if not res:
                logger.error(f'Check column {name} failed!!')
            rc.append(res)
        result_dict[uuid] = all(rc)
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_the_table_top_buttons failed!!")

    # [GUI] Verify the details of DNS Filtering status icons are correctly displayed.
    def test_04_check_the_status_icons(self):
        uuid = "SOSAIOT-TC-51498"
        logger.info(f'------ Check the license status icon - {uuid}')
        logger.info('Click "license icon"')
        fw_page_ui.click_element(*license_icon)
        rc_lcs = check_element_attribute(icon_info, 'Licensed')
        fw_page_ui.click_element(*license_icon)
        logger.info(f'------ Check the information icon - {uuid}')
        logger.info('Move to "information icon"')
        fw_page_ui.move_to_the_element(*information_icon)
        infos = fw_page_ui.get_elements(*icon_info)
        infos = [info.text for info in infos]
        logger.info(str(infos))
        rc_info = infos == ['DNS Security > Settings', 'Rules and Policies > DNS Rules']
        result_dict[uuid] = rc_lcs & rc_info
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_the_status_icons failed!!")

    # [GUI] Verify the profile can be expanded or collapsed by clicking the black triangle.
    def test_05_check_the_black_triangle(self):
        uuid = "SOSAIOT-TC-51494"
        logger.info(f'------ Check the profile can be expanded - {uuid}')
        logger.info('Click Default Profile "black triangle"')
        arrow_path = get_table_entry_element_xpath('Default Profile')
        fw_page_ui.click_element(*arrow_path)
        fw_page_ui.wait_for_element_to_be_visible(*profile_expanded_form)
        logger.info(f'------ Check the profile can be collapsed - {uuid}')
        logger.info('Click Default Profile "black triangle"')
        fw_page_ui.click_element(*arrow_path)
        fw_page_ui.wait_for_element_to_be_invisible(*profile_expanded_form)
        result_dict[uuid] = True
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_the_black_triangle failed!!")


@paramunittest.parametrized(
    {'testrail_uuid': '1521023', 'uuid': 'SOSAIOT-TC-51490'},
    {'testrail_uuid': '1521122', 'uuid': 'SOSAIOT-TC-51494'},
    {'testrail_uuid': '1521123', 'uuid': 'SOSAIOT-TC-51495'},
    {'testrail_uuid': '1521125', 'uuid': 'SOSAIOT-TC-51497'},
    {'testrail_uuid': '1521126', 'uuid': 'SOSAIOT-TC-51498'})
class TestProfile_Page(Test):

    def setParameters(self, uuid, testrail_uuid):
        self.uuid = uuid
        self.testrail_uuid = testrail_uuid
        self.description = show_testcase_info(TESTPLAN, self.testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


#  [GUI] Verify the profile table entries can be sorted by name.
class TestProfile_1521124(Test):
    testrail_uuid = "1521124"
    uuid = "SOSAIOT-TC-51496"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']
    jira = 'GEN7-27570'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_add_some_different_profiles(self):
        _ = dnsFilter_cli.delete_filtering_profile()
        profile = copy.deepcopy(profile_dict)
        for name in ['A', 'a', 'd']:
            profile['dns_security']['dns_filtering']['profile'][0]['name'] = name
            rc = dnsFilter_api.add_dns_filtering_profile(**profile)
            if not rc:
                logger.error(f'Add dns filtering profile {name} failed!!')
                break
        Assertion.assert_equal(rc, True, "ERR: add_some_different_profiles failed!!")

    def test_02_check_name_sort_profiles_descend(self):
        init_test_page(dns_profile_page)
        logger.info('Click column "NAME"')
        fw_page_ui.click_element_by_text("Name")
        fw_page_ui.wait_for_element_to_be_visible('css', '.icon-sorting-up')
        logger.info('------ Check Profile number')
        name_number = {
            'd': '1',
            'Default Profile': '2',
            'a': '3',
            'A': '4',
        }
        for name, num in name_number.items():
            path = get_table_entry_element_xpath(name, profile_priority_part)
            logger.info(path)
            rc = check_element_attribute(path, num)
            if not rc:
                break
        Assertion.assert_equal(rc, True, "ERR: check_name_sort_profiles_descend failed!!")

    def test_03_check_name_sort_profiles_ascend(self):
        logger.info('Click column "NAME"')
        fw_page_ui.click_element_by_text("Name")
        fw_page_ui.wait_for_element_to_be_visible('css', '.icon-sorting-up')
        logger.info('------ Check Profile number')
        name_number = {
            'A': '1',
            'a': '2',
            'Default Profile': '3',
            'd': '4',
        }
        for name, num in name_number.items():
            path = get_table_entry_element_xpath(name, profile_priority_part)
            logger.info(path)
            rc = check_element_attribute(path, num)
            if not rc:
                break
        Assertion.assert_equal(rc, True, "ERR: check_name_sort_profiles_ascend failed!!")
