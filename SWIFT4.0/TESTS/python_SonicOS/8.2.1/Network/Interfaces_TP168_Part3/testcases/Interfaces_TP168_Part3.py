from definition.settings import *
from definition.utils import *
from definition.database import *

class Test_Default_columns(Test):
    uuid = 'NonTC'
    description = 'Default columns for Interfaces Table'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    # GUI: Default settings for Interfaces Table
    def test_01_check_default_interface_columns(self):
        init_test_page(interface_page)
        uuid = "SOSAIOT-TC-56176"
        logger.info(f'------ Check Interfaces table column details - {uuid}')
        target = ['Name', 'Zone', 'IP Address', 'Subnet Mask', 'IP Assignment', 'Status', 'Comment']
        result_dict[uuid] = check_elements_attribute(interface_column, target=target)
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_default_interface_columns failed!!")
    
    # Show TX Errors and RX Errors on Network > Interfaces page
    def test_02_check_interface_traffic_columns(self):
        uuid = "SOSAIOT-TC-56233"
        logger.info(f'------ Check Traffic Statistics table column details - {uuid}')
        fw_page_ui.click_element_by_text('Traffic Statistics')
        target = ['Tx Errors', 'Rx Errors']
        fw_page_ui.click_element_by_text('IPv4')
        rc = check_elements_attribute(interface_column, target=target)
        fw_page_ui.click_element_by_text('IPv6')
        rc &= check_elements_attribute(interface_column, target=target)
        result_dict[uuid] = rc
        Assertion.assert_equal(result_dict[uuid], True, "ERR: check_interface_traffic_columns failed!!")


@paramunittest.parametrized(
    {'testrail_uuid': '1515719', 'uuid': 'SOSAIOT-TC-56176'},
    {'testrail_uuid': '1515783', 'uuid': 'SOSAIOT-TC-56233'},)
class TestDefault_columns(Test):

    def setParameters(self, uuid, testrail_uuid):
        self.uuid = uuid
        self.testrail_uuid = testrail_uuid
        self.description = show_testcase_info(TESTPLAN, self.testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_check_result(self):
        Assertion.assert_equal(result_dict[self.uuid], True, "ERR: check_result failed!!")


# GUI: Default settings for LAN interface configure dialog
class TestLAN_1515730(Test):
    uuid = "SOSAIOT-TC-56187"
    testrail_uuid = "1515730"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X0 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_labels(self):
        rc = []
        labels = ['Zone', 'Mode / IP Assignment', 'IP Address', 'Subnet Mask', 'Comment', 'Management', 'User Login']
        for label in labels:
            logger.info(f'> test label : {label}')
            if label in ['Management', 'User Login']:
                path = f"//*[contains(@class, 'sw-title-pane__title-cont--level2') and text()='{label}']"
            else:
                path = f"//*[contains(@class, 'sw-form-row__label') and text()='{label}']"
            res = fw_page_ui.does_element_exist('xpath', path)
            logger.info(res)
            if not res:
                logger.error(f'Check LAN interface label {label} failed!!')
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_labels failed!!")

    def test_03_check_default_lan_interface_zone_is_unchangeable(self):
        rc = check_element_attribute(disable_zone_dropdown, target='sw-select--disabled', attribute='class')
        Assertion.assert_equal(rc, True, "ERR: check_default_lan_interface_zone_is_unchangeable failed!!")

    def test_04_check_ip_assignment_dropdown_box(self):
        target_list = ['Static IP Mode', 'Transparent IP Mode (Splice L3 Subnet)', 'Layer 2 Bridged Mode']
        logger.info('------ Check "IP Assignment" Dropdown box default value')
        rc_default = check_element_attribute(mode_box_text, 'Static IP Mode')
        logger.info('------ Check "IP Assignment" Dropdown box list values')
        logger.info('Click "IP Assignment" dropdown box arrow to expand')
        fw_page_ui.click_element(*mode_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(target in test_fmt for target in target_list)
        logger.info(rc)
        logger.info('Click "IP Assignment" dropdown box arrow to collapse')
        fw_page_ui.click_element(*mode_arrow)
        Assertion.assert_equal(rc_default & rc, True, "ERR: check_ip_assignment_dropdown_box failed!!")

    def test_055_check_ip_netmask_comment(self):
        logger.info('------ Check "IP Address" Textbox')
        rc = check_element_attribute(ip_address_textbox, Parameter.FIREWALL, 'value')
        logger.info('------ Check "Netmask" Textbox')
        rc &= check_element_attribute(netmask_textbox, Parameter.Mask, 'value')
        logger.info('------ Check "Comment" Textbox')
        rc &= check_element_attribute(comment_textbox, 'Default LAN', 'value')
        Assertion.assert_equal(rc, True, "ERR: check_ip_netmask_comment failed!!")

    def test_05_check_management_and_user_login(self):
        res = []
        logger.info('------ Check "Management HTTPS" toggle is enabled')
        rc = not check_element_attribute(mgmt_https_toggle, 'sw-toggle--off', 'class')
        logger.info(rc)
        res.append(rc)
        logger.info('------ Check "Management Ping" toggle is enabled')
        rc = not check_element_attribute(ping_toggle, 'sw-toggle--off', 'class')
        logger.info(rc)
        res.append(rc)
        logger.info('------ Check "redirect" toggle is enabled')
        rc = not check_element_attribute(redirect_toggle, 'sw-toggle--off', 'class')
        logger.info(rc)
        res.append(rc)
        logger.info('------ Check "User Login HTTPS" toggle')
        rc = not check_element_attribute(login_https_toggle, 'sw-toggle--off', 'class')
        res.append(rc)
        logger.info('------ Check "User Login HTTP" toggle is disabled')
        rc = check_element_attribute(user_http_toggle, 'sw-toggle--off', 'class')
        res.append(rc)
        Assertion.assert_equal(all(res), True, "ERR: check_management_and_user_login failed!!")


# GUI: LAN in Transparent Mode objects for interfaces
class TestLAN_1515727(Test):
    uuid = "SOSAIOT-TC-56184"
    testrail_uuid = "1515727"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page_and_select_transparent_mode(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X0 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "Transparent"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Transparent IP Mode (Splice L3 Subnet)')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_transparent_dropdown_box_content(self):
        target_list = [
            'Create new address object...', 
            'X1 IP', 
            'Default Active WAN IP', 
            'X1 Default Gateway', 
            'WAN Interface IP'
        ]
        logger.info('Click "Transparent Range" dropdown box arrow to expand')
        fw_page_ui.click_element(*transparent_range_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        logger.info('Click "Transparent Range" dropdown box arrow to collapse')
        fw_page_ui.click_element(*transparent_range_arrow)
        logger.info('Check "Transparent Range" dropdown box content')
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(target in test_fmt for target in target_list)
        Assertion.assert_equal(rc, True, "ERR: check_transparent_dropdown_box_content failed!!")

    def test_03_check_specific_textbox_disappeared(self):
        logger.info('Check "IP Address" textbox disappeared')
        rc = not fw_page_ui.does_element_exist_now(*ip_address_textbox)
        logger.info(rc)
        logger.info('Check "Subnet Mask" textbox disappeared')
        rc &= not fw_page_ui.does_element_exist_now(*netmask_textbox)
        Assertion.assert_equal(rc, True, "ERR: check_specific_textbox_disappeared failed!!")

    def test_04_check_advanced_tab_new_toggles(self):
        logger.info('Click "Advanced" tab')
        fw_page_ui.navigate_to_tab('Advanced')
        logger.info('Check new toggles')
        rc = check_element_attribute(trans_new_toggle_G, 'sw-toggle--off', 'class')
        rc &= check_element_attribute(trans_new_toggle_A, 'sw-toggle--off', 'class')
        logger.info('Check new toggles can be enabled')
        fw_page_ui.toggle_button(*trans_new_toggle_G, enabled=True)
        fw_page_ui.toggle_button(*trans_new_toggle_A, enabled=True)
        Assertion.assert_equal(rc, True, "ERR: check_advanced_tab_new_toggles failed!!")


# Verify the "Create new address object..." works in Transparent Range
class TestLAN_1515728(Test):
    uuid = "SOSAIOT-TC-56185"
    testrail_uuid = "1515728"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_init_address_objects(self):
        rc = ao_cli.del_address_objects('ipv4')
        Assertion.assert_equal(rc, True, "ERR: init failed!!")

    def test_02_open_edit_interface_page_and_select_transparent_mode(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X0 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "Transparent"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Transparent IP Mode (Splice L3 Subnet)')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_03_check_transparent_create_address_object_display(self):
        logger.info('Select "Create new address object..."')
        fw_page_ui.select_drop_down_value_new('Transparent Range', 'Create new address object...')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        Assertion.assert_equal(True, True, "ERR: check_transparent_create_address_object_display failed!!")

    def test_04_create_transparent_new_host(self):
        fw_page_ui.wait_for_page_data_to_be_rendered()
        address = '172.17.1.100'
        logger.info(f'Config address "Name" as "{address}"')
        fw_page_ui.set_input_text_field('name', 'name', address)
        logger.info(f'Config address "IP Address" as "{address}"')
        fw_page_ui.set_input_text_field('name', 'ip-address', address)
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: create_transparent_new_host failed!!")

    def test_05_create_transparent_new_range(self):
        address = '172.17.1.201'
        logger.info(f'Config address "Name" as "{address}"')
        fw_page_ui.clear_text_field('name', 'name')
        fw_page_ui.set_input_text_field('name', 'name', address)
        logger.info('Config address "Type" as "Range"')
        fw_page_ui.select_drop_down_value_new('Type', 'Range')
        logger.info(f'Config address "Starting IP Address" as "{address}"')
        fw_page_ui.clear_text_field(*start_ip_textbox)
        fw_page_ui.set_input_text_field(*start_ip_textbox, field_val=address)
        logger.info('Config address "Ending IP Address" as "172.17.1.205"')
        fw_page_ui.clear_text_field(*end_ip_textbox)
        fw_page_ui.set_input_text_field(*end_ip_textbox, field_val='172.17.1.205')
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: create_transparent_new_range failed!!")

    def test_06_create_transparent_new_network(self):
        address = '172.17.1.0'
        # name = 'test_network'
        logger.info(f'Config address "Name" as "{address}"')
        fw_page_ui.clear_text_field('name', 'name')
        fw_page_ui.set_input_text_field('name', 'name', address)
        logger.info('Config address "Type" as "Network"')
        fw_page_ui.select_drop_down_value_new('Type', 'Network')
        logger.info(f'Config address "Network" as "{address}"')
        fw_page_ui.clear_text_field(*network_textbox)
        fw_page_ui.set_input_text_field(*network_textbox, field_val=address)
        logger.info(f'Config address "Netmask / Prefix Length" as "{Parameter.Mask}"')
        fw_page_ui.clear_text_field(*mask_textbox)
        fw_page_ui.set_input_text_field(*mask_textbox, field_val=Parameter.Mask)
        logger.info('Click "Save"')
        fw_page_ui.click_element_by_text('Save')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: create_transparent_new_range failed!!")

    def test_07_new_address_objects_display_in_the_transparent_range_dropdown_list(self):
        # correct address range is the same subnet as default WAN but exclude Default WAN IP
        logger.info('Click "GO BACK"')
        fw_page_ui.click_element_by_text('GO BACK')
        logger.info('Click "Transparent Range" dropdown box to expand')
        fw_page_ui.click_element(*transparent_range_arrow)
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        target_list = ['172.17.1.100', '172.17.1.201']
        logger.info(f'target: {target_list}')
        rc = all(target in test_fmt for target in target_list)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: new_address_objects_display_in_the_transparent_range_dropdown_list failed!!")


# GUI: LAN in Layer 2 Bridged Mode
class TestLAN_1515732(Test):
    uuid = "SOSAIOT-TC-56189"
    testrail_uuid = "1515732"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page_and_select_l2b_mode(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X0 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X0')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "Layer 2 Bridged Mode"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Layer 2 Bridged Mode')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")
    
    def test_02_check_bridge_to_dropdown_box_content(self):
        logger.info('Click "Bridged To" dropdown box to expand')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Bridged To'))
        test = fw_page_ui.get_drop_down_list_values()
        logger.info('Click "Bridged To" dropdown box to collapse')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Bridged To'))
        logger.info('Check "Transparent Range" dropdown box content')
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = 'X1' in test_fmt
        Assertion.assert_equal(rc, True, "ERR: check_bridge_to_dropdown_box_content failed!!")

    def test_03_check_three_new_toggles(self):
        rc = check_element_attribute(block_non_ip_toggle, 'sw-toggle--off', 'class')
        rc &= check_element_attribute(never_route_toggle, 'sw-toggle--off', 'class')
        if 'tz' not in Params.product.lower():
            rc &= check_element_attribute(sniff_toggle, 'sw-toggle--off', 'class')
        Assertion.assert_equal(rc, True, "ERR: check three new toggles failed!!")

    def test_04_check_vlan_filtering_tab(self):
        logger.info('Click "VLAN Filtering" tab')
        fw_page_ui.navigate_to_tab('VLAN Filtering')
        Assertion.assert_equal(True, True, "ERR: check_vlan_filtering_tab failed!!")


# GUI: Default settings for WAN interface configure dialog
class TestWAN_1515741(Test):
    uuid = "SOSAIOT-TC-56197"
    testrail_uuid = "1515741"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_labels(self):
        rc = []
        labels = [
            'Zone', 'Mode / IP Assignment', 'IP Address', 'Subnet Mask', 'Comment', 'Management', 'User Login',
            'Default Gateway (Optional)', 'DNS Server 1', 'DNS Server 2', 'DNS Server 3']
        for label in labels:
            logger.info(f'> test label : {label}')
            if label in ['Management', 'User Login']:
                path = f"//*[contains(@class, 'sw-title-pane__title-cont--level2') and text()='{label}']"
            else:
                path = f"//*[contains(@class, 'sw-form-row__label') and text()='{label}']"
            res = fw_page_ui.does_element_exist('xpath', path)
            logger.info(res)
            if not res:
                logger.error(f'Check LAN interface label {label} failed!!')
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_labels failed!!")

    def test_03_check_default_wan_interface_zone_list_value(self):
        target_list = ['Unassigned', 'Create new zone...', 'LAN', 'WAN', 'DMZ', 'WLAN']
        logger.info('------ Check "Zone" Dropdown box list values')
        logger.info('Click "Zone" dropdown box arrow to expand')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Zone'))
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(target in test_fmt for target in target_list)
        logger.info(rc)
        logger.info('Click "Zone" dropdown box arrow to collapse')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Zone'))
        Assertion.assert_equal(rc, True, "ERR: check_default_wan_interface_zone_list_value failed!!")

    def test_04_check_comment(self):
        rc = check_element_attribute(comment_textbox, 'Default WAN', 'value')
        Assertion.assert_equal(rc, True, "ERR: check_comment failed!!")

    def test_05_check_advanced_tab_sections(self):
        logger.info('Click "Advanced" tab')
        fw_page_ui.navigate_to_tab('Advanced')
        rc = []
        labels = ['Advanced Settings', 'Bandwidth Management']
        for label in labels:
            logger.info(f'> test label : {label}')
            path = f"//*[contains(@class, 'sw-title-pane__title-cont') and text()='{label}']"
            res = fw_page_ui.does_element_exist('xpath', path)
            logger.info(res)
            if not res:
                logger.error(f'Check WAN interface label {label} failed!!')
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_advanced_tab_sections failed!!")

    def test_06_check_link_speed_dropdown_box(self):
        target_list = ['10 Mbps - Half Duplex', '10 Mbps - Full Duplex', '100 Mbps - Half Duplex', '100 Mbps - Full Duplex', '1000 Mbps - Full Duplex', '1 Gbps - Full Duplex', 'Auto Negotiate']
        logger.info('------ Check "link speed" Dropdown box default value')
        rc = check_element_attribute(get_dropdown_box_element_xpath('Link Speed', 'text'), 'Auto Negotiate')
        logger.info('------ Check "link speed" Dropdown box list values')
        logger.info('Click "link speed" dropdown box arrow to expand')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Link Speed'))
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(x in target_list for x in test_fmt)
        logger.info(rc)
        logger.info('Click "link speed" dropdown box arrow to collapse')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('Link Speed'))
        Assertion.assert_equal(rc, True, "ERR: check_default_wan_interface_zone_list_value failed!!")


# GUI: WAN in DHCP mode
class TestWAN_1515747(Test):
    uuid = "SOSAIOT-TC-56200"
    testrail_uuid = "1515747"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "DHCP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'DHCP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")
    
    def test_02_check_new_label_and_toggle_display(self):
        logger.info('------ Check label : Host Name')
        rc = fw_page_ui.does_element_exist(*hostname_textbox)
        logger.info(rc)
        logger.info('------ Check toggle : Request renew of previous IP on startup')
        rc &= check_element_attribute(request_renew_toggle, 'sw-toggle--off', 'class')
        Assertion.assert_equal(rc, True, "ERR: check_hostname_label_display failed!!")

    def test_03_check_specific_labels_readonly(self):
        rc = []
        for name in [
            'textfield-ip-address', 'textfield-subnet-mask', 'textfield-default-gateway', 'textfield-dns-server-1',
            'textfield-dns-server-2', 'textfield-lease-expires']:
            logger.info(f'> test label : {name[10:]}')
            res = check_element_attribute(['name', name], 'true', 'readOnly')
            rc.append(res)
            time.sleep(1)
        Assertion.assert_equal(all(rc), True, "ERR: check_specific_labels_readonly failed!!")

    def test_04_check_three_new_buttons(self):
        rc = []
        for name in ['dhcp__button-renew', 'dhcp__button-release', 'dhcp__button-refresh']:
            logger.info(f'> test button : {name[13:]}')
            res = check_element_attribute(['css', f'.{name}'], name[13:].capitalize())
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check three new buttons failed!!")


# GUI: WAN in PPTP mode
class TestWAN_1515756(Test):
    uuid = "SOSAIOT-TC-56208"
    testrail_uuid = "1515756"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "PPTP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'PPTP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_specific_labels(self):
        labels = {
            'User Name': 'textfield-user-name',
            'User Password': 'textfield-user-password',
            'PPTP Server IP Address': 'textfield-server-ip',
            'PPTP (Client) Host Name': 'textfield-client-host-name'
        }
        rc = []
        for identifier, name in labels.items():
            logger.info(f'> test label : {identifier}')
            path = get_textbox_element_xpath(identifier=identifier)
            res = check_element_attribute(path, name, 'name')
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_specific_labels failed!!")

    def test_03_check_new_dropdown_box_and_toggle(self):
        logger.info('------ Check toggle : Inactivity Disconnect')
        rc_toggle = fw_page_ui.does_element_exist(*get_toggle_xpath('Inactivity Disconnect'))
        logger.info(rc_toggle)
        logger.info('------ Check dropdown box : PPTP IP Assignment')
        target_list = ['DHCP', 'Static']
        logger.info('Click "PPTP IP Assignment" dropdown box arrow to expand')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('PPTP IP Assignment'))
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(target in test_fmt for target in target_list)
        logger.info(rc)
        logger.info('Click "PPTP IP Assignment" dropdown box arrow to collapse')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('PPTP IP Assignment'))
        Assertion.assert_equal(rc_toggle & rc, True, "ERR: check_new_dropdown_box_and_toggle failed!!")

    def test_04_check_protocol_tab_sections(self):
        logger.info('Click "Protocol" tab')
        fw_page_ui.navigate_to_tab('Protocol')
        labels = ['SonicWall IP Address', 'Gateway (Router) Address', 'DNS Server 1', 'DNS Server 2']
        rc = []
        for label in labels:
            logger.info(f'> test label : {label}')
            path = ['xpath', f'//div[@class="protocol-pptp"]/descendant::div[text()="{label}"]']
            res = check_element_attribute(path, 'sw-form-row__label', 'class')
            rc.append(res)
        res = check_elements_attribute(path, 'sw-form-row__label', 'class')
        Assertion.assert_equal(all(rc), True, "ERR: check_protocol_tab_sections failed!!")


# PPTP Server IP Address validation check
class TestWAN_1515757(Test):
    uuid = "SOSAIOT-TC-56209"
    testrail_uuid = "1515757"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "PPTP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'PPTP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_config_invalid_server_ip_address_failed(self):
        name = 'textfield-server-ip'
        rc = []
        for invalid in ['123465789', '10.103.3.256']:
            logger.info(f'> test invalid Server IP address : {invalid}')
            logger.info(f'Set "Server IP" textbox as "{invalid}"')
            fw_page_ui.clear_text_field('name', name)
            fw_page_ui.set_input_text_field('name', name, invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid PPTP Server IP Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_server_ip_address should fail!!")

    def test_03_config_valid_server_ip_address(self):
        name = 'textfield-server-ip'
        logger.info(f'Set "Server IP" textbox as "{Parameter.X1_IP}"')
        fw_page_ui.clear_text_field('name', name)
        fw_page_ui.set_input_text_field('name', name, Parameter.X1_IP)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.verify_message_alert('Web management on this interface has been disabled. Please make sure it is enabled on another interface before proceeding.\nDo you wish to continue?')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: config_valid_server_ip_address failed!!")
            

# PPTP static IP Assignment validation check
class TestWAN_1515758(Test):
    uuid = "SOSAIOT-TC-56210"
    testrail_uuid = "1515758"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "PPTP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'PPTP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_config_invalid_ip_address_failed(self):
        logger.info('Select "PPTP IP Assignment" dropdown box as "Static"')
        fw_page_ui.select_drop_down_value_new('PPTP IP Assignment', 'Static')
        rc = []
        for invalid in ['123465789', '10.10.10.256']:
            logger.info(f'> test invalid IP Address : {invalid}')
            logger.info(f'Set "IP Address" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid IP Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_ip_address should fail!!")

    def test_03_config_invalid_netmask_failed(self):
        logger.info(f'Set "IP Address" textbox as "{Parameter.X1_IP}"')
        fw_page_ui.clear_text_field(*ip_address_textbox)
        fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=Parameter.X1_IP)
        invalid = '255.255.255.1'
        logger.info(f'> test invalid Subnet Mask : {invalid}')
        logger.info(f'Set "Subnet Mask" textbox as "{invalid}"')
        fw_page_ui.clear_text_field(*netmask_textbox)
        fw_page_ui.set_input_text_field(*netmask_textbox, field_val=invalid)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        rc = fw_page_ui.compare_message_new(targetMsg='Please enter a valid Subnet Mask',
                                        attrib='class', attrib_val='sw-status-info__text__message__para')
        Assertion.assert_equal(rc, True, "ERR: config_invalid_netmask should fail!!")

    def test_04_config_invalid_gateway_address_failed(self):
        logger.info(f'Set "Subnet Mask" textbox as "{Parameter.Mask}"')
        fw_page_ui.clear_text_field(*netmask_textbox)
        fw_page_ui.set_input_text_field(*netmask_textbox, field_val=Parameter.Mask)
        rc = []
        for invalid in ['212313', '10.10.256.1']:
            logger.info(f'> test invalid Gateway Address : {invalid}')
            logger.info(f'Set "Gateway (Router) Address" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*gateway_textbox)
            fw_page_ui.set_input_text_field(*gateway_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid Gateway Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_gateway_address should fail!!")



# GUI: WAN in L2TP mode
class TestWAN_1515762(Test):
    uuid = "SOSAIOT-TC-56214"
    testrail_uuid = "1515762"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "L2TP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'L2TP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_specific_labels(self):
        labels = {
            'User Name': 'textfield-user-name',
            'User Password': 'textfield-user-password',
            'L2TP Server IP Address': 'textfield-server-ip',
            'L2TP (Client) Host Name': 'textfield-client-host-name',
            'L2TP Shared Secret': 'textfield-shared-secret'
        }
        rc = []
        for identifier, name in labels.items():
            logger.info(f'> test label : {identifier}')
            path = get_textbox_element_xpath(identifier=identifier)
            res = check_element_attribute(path, name, 'name')
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_specific_labels failed!!")

    def test_03_check_new_dropdown_box_and_toggle(self):
        logger.info('------ Check toggle : Inactivity Disconnect')
        rc_toggle = fw_page_ui.does_element_exist(*get_toggle_xpath('Inactivity Disconnect'))
        logger.info(rc_toggle)
        logger.info('------ Check dropdown box : L2TP IP Assignment')
        target_list = ['DHCP', 'Static']
        logger.info('Click "L2TP IP Assignment" dropdown box arrow to expand')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('L2TP IP Assignment'))
        test = fw_page_ui.get_drop_down_list_values()
        test_fmt = [str(x).lstrip().rstrip() for x in test]
        logger.info(test_fmt)
        rc = all(target in test_fmt for target in target_list)
        logger.info(rc)
        logger.info('Click "L2TP IP Assignment" dropdown box arrow to collapse')
        fw_page_ui.click_element(*get_dropdown_box_element_xpath('L2TP IP Assignment'))
        Assertion.assert_equal(rc_toggle & rc, True, "ERR: check_new_dropdown_box_and_toggle failed!!")

    def test_04_check_protocol_tab_sections(self):
        logger.info('Click "Protocol" tab')
        fw_page_ui.navigate_to_tab('Protocol')
        labels = ['SonicWall IP Address', 'Gateway (Router) Address', 'DNS Server 1', 'DNS Server 2']
        rc = []
        for label in labels:
            logger.info(f'> test label : {label}')
            path = ['xpath', f'//div[@class="protocol-l2tp"]/descendant::div[text()="{label}"]']
            res = check_element_attribute(path, 'sw-form-row__label', 'class')
            rc.append(res)
        res = check_elements_attribute(path, 'sw-form-row__label', 'class')
        Assertion.assert_equal(all(rc), True, "ERR: check_protocol_tab_sections failed!!")


# L2TP Server IP Address validation check
class TestWAN_1515764(Test):
    uuid = "SOSAIOT-TC-56216"
    testrail_uuid = "1515764"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "L2TP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'L2TP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_config_invalid_server_ip_address_failed(self):
        name = 'textfield-server-ip'
        rc = []
        for invalid in ['123465789', '10.103.3.256']:
            logger.info(f'> test invalid Server IP address : {invalid}')
            logger.info(f'Set "Server IP" textbox as "{invalid}"')
            fw_page_ui.clear_text_field('name', name)
            fw_page_ui.set_input_text_field('name', name, invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid L2TP Server IP Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_server_ip_address should fail!!")

    def test_03_config_valid_server_ip_address(self):
        name = 'textfield-server-ip'
        logger.info(f'Set "Server IP" textbox as "{Parameter.X1_IP}"')
        fw_page_ui.clear_text_field('name', name)
        fw_page_ui.set_input_text_field('name', name, Parameter.X1_IP)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.verify_message_alert('Web management on this interface has been disabled. Please make sure it is enabled on another interface before proceeding.\nDo you wish to continue?')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: config_valid_server_ip_address failed!!")
            

# L2TP static IP Assignment validation check
class TestWAN_1515765(Test):
    uuid = "SOSAIOT-TC-56217"
    testrail_uuid = "1515765"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X1 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X1')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Mode" dropdown box as "L2TP"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'L2TP')
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_config_invalid_ip_address_failed(self):
        logger.info('Select "L2TP IP Assignment" dropdown box as "Static"')
        fw_page_ui.select_drop_down_value_new('L2TP IP Assignment', 'Static')
        rc = []
        for invalid in ['123465789', '10.10.10.256']:
            logger.info(f'> test invalid IP Address : {invalid}')
            logger.info(f'Set "IP Address" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid IP Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_ip_address should fail!!")

    def test_03_config_invalid_netmask_failed(self):
        logger.info(f'Set "IP Address" textbox as "{Parameter.X1_IP}"')
        fw_page_ui.clear_text_field(*ip_address_textbox)
        fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=Parameter.X1_IP)
        invalid = '255.255.255.1'
        logger.info(f'> test invalid Subnet Mask : {invalid}')
        logger.info(f'Set "Subnet Mask" textbox as "{invalid}"')
        fw_page_ui.clear_text_field(*netmask_textbox)
        fw_page_ui.set_input_text_field(*netmask_textbox, field_val=invalid)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        rc = fw_page_ui.compare_message_new(targetMsg='Please enter a valid Subnet Mask',
                                        attrib='class', attrib_val='sw-status-info__text__message__para')
        Assertion.assert_equal(rc, True, "ERR: config_invalid_netmask should fail!!")

    def test_04_config_invalid_gateway_address_failed(self):
        logger.info(f'Set "Subnet Mask" textbox as "{Parameter.Mask}"')
        fw_page_ui.clear_text_field(*netmask_textbox)
        fw_page_ui.set_input_text_field(*netmask_textbox, field_val=Parameter.Mask)
        rc = []
        for invalid in ['212313', '10.10.256.1']:
            logger.info(f'> test invalid Gateway Address : {invalid}')
            logger.info(f'Set "Gateway (Router) Address" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*gateway_textbox)
            fw_page_ui.set_input_text_field(*gateway_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid Gateway Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: config_invalid_gateway_address should fail!!")


# Error and wrong inputs
class TestError_1515752(Test):
    uuid = "SOSAIOT-TC-56204"
    testrail_uuid = "1515752"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_edit_interface_page(self):
        init_test_page(interface_page)
        logger.info('Hover and Click "X2 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X2')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        logger.info('Select "Zone" dropdown box as "LAN"')
        fw_page_ui.select_drop_down_value_new('Zone', 'LAN')
        logger.info('Select "Mode" dropdown box as "Static IP Mode"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Static IP Mode')
        logger.info('Enable Management "HTTPS" toggle')
        fw_page_ui.toggle_button(*mgmt_https_toggle, enabled=True)
        Assertion.assert_equal(rc, True, "ERR: open_edit_interface_page failed!!")

    def test_02_check_lan_ip_address_format(self):
        rc = []
        for invalid in ['0.0.0.0', 'test', '1.1.1.256']:
            logger.info(f'> test invalid Server IP address : {invalid}')
            logger.info(f'Set "Server IP" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid IP Address',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_ip_address_format should fail!!")

    def test_03_check_lan_ip_address_other_format_error(self, wan=False):
        msgs = {
            '255.1.1.1': 'Invalid IP Address', 
            '1.1.1.255': 'Invalid IP Address - Choose an address within the subnet'}
        if wan:
            msgs['1.1.1.255'] = 'Invalid IP Address'
        rc = []
        for ip, msg in msgs.items():
            logger.info(f'> test invalid Server IP address : {ip}')
            logger.info(f'Set "Server IP" textbox as "{ip}"')
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=ip)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg=msg,
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_ip_address_other_format_error failed!!")

    def test_04_check_wan_ip_address_other_format_error(self):
        logger.info('Select "Zone" dropdown box as "WAN"')
        fw_page_ui.select_drop_down_value_new('Zone', 'WAN')
        logger.info('Select "Mode" dropdown box as "Static"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Static')
        self.test_02_check_lan_ip_address_format()
        self.test_03_check_lan_ip_address_other_format_error(wan=True)

    def test_05_check_dmz_ip_address_other_format_error(self):
        logger.info('Select "Zone" dropdown box as "DMZ"')
        fw_page_ui.select_drop_down_value_new('Zone', 'DMZ')
        logger.info('Select "Mode" dropdown box as "Static IP Mode"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Static IP Mode')
        self.test_02_check_lan_ip_address_format()
        self.test_03_check_lan_ip_address_other_format_error()

    def test_06_check_wlan_ip_address_other_format_error(self):
        logger.info('Select "Zone" dropdown box as "WLAN"')
        fw_page_ui.select_drop_down_value_new('Zone', 'WLAN')
        logger.info('Select "Mode" dropdown box as "Static IP Mode"')
        fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', 'Static IP Mode')
        self.test_02_check_lan_ip_address_format()
        self.test_03_check_lan_ip_address_other_format_error()


# Subnet Mask validation check
class TestError_1515763(Test):
    uuid = "SOSAIOT-TC-56215"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    zone = 'LAN'
    mode = 'Static IP Mode'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_interface_page(self):
        init_test_page(interface_page)
        Assertion.assert_equal(True, True, "ERR: open_edit_interface_page failed!!")
    
    def test_02_init_lan_static_interface(self):
        logger.info('Hover and Click "X2 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X2')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        if rc:
            logger.info(f'Select "Zone" dropdown box as "{self.zone}"')
            fw_page_ui.select_drop_down_value_new('Zone', self.zone)
            logger.info(f'Select "Mode" dropdown box as "{self.mode}"')
            fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', self.mode)
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val='192.1.1.1')
        Assertion.assert_equal(rc, True, "ERR: init_lan_static_interface failed!!")

    def test_03_check_lan_invalid_subnet_mask_format(self):
        rc = []
        for invalid in ['', 'test', '1.1.1.256']:
            logger.info(f'> test invalid Subnet Mask : {invalid}')
            logger.info(f'Set "Subnet Mask" textbox as "{invalid}"')
            fw_page_ui.clear_text_field(*netmask_textbox)
            fw_page_ui.set_input_text_field(*netmask_textbox, field_val=invalid)
            logger.info('Click "OK"')
            fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
            res = fw_page_ui.compare_message_new(targetMsg='Please enter a valid Subnet Mask',
                                           attrib='class', attrib_val='sw-status-info__text__message__para')
            logger.info(res)
            rc.append(res)
        Assertion.assert_equal(all(rc), True, "ERR: check_lan_invalid_subnet_mask_format should fail!!")

    def test_04_check_lan_valid_subnet_mask(self):
        ip = '255.255.0.0'
        logger.info(f'> test valid Subnet Mask : {ip}')
        logger.info(f'Set "Subnet Mask" textbox as "{ip}"')
        fw_page_ui.clear_text_field(*netmask_textbox)
        fw_page_ui.set_input_text_field(*netmask_textbox, field_val=ip)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        Assertion.assert_equal(rc, True, "ERR: check_lan_valid_subnet_mask failed!!")

    def test_05_check_wan_ip_address_other_format_error(self):
        self.zone = 'WAN'
        self.mode = 'Static'
        self.test_02_init_lan_static_interface()
        self.test_03_check_lan_invalid_subnet_mask_format()
        self.test_04_check_lan_valid_subnet_mask()

    def test_06_check_dmz_ip_address_other_format_error(self):
        self.zone = 'DMZ'
        self.test_02_init_lan_static_interface()
        self.test_03_check_lan_invalid_subnet_mask_format()
        self.test_04_check_lan_valid_subnet_mask()

    def test_07_check_wlan_ip_address_other_format_error(self):
        self.zone = 'WLAN'
        self.test_02_init_lan_static_interface()
        self.test_03_check_lan_invalid_subnet_mask_format()
        self.test_04_check_lan_valid_subnet_mask()



# Domain Name can be set numerical character as start character from left on interface page
class TestCommon_1533417(Test):
    uuid = "SOSAIOT-TC-56240"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    zone = 'LAN'
    mode = 'Static IP Mode'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_open_interface_page(self):
        init_test_page(interface_page)
        Assertion.assert_equal(True, True, "ERR: open_interface_page failed!!")
    
    def test_02_init_interface(self):
        logger.info('Hover and Click "X2 interface" edit pencil')
        fw_page_ui.click_on_edit_element_after_hovering('X2')
        rc = fw_page_ui.is_element_displayed(*edit_interface_window)
        if rc:
            logger.info(f'Select "Zone" dropdown box as "{self.zone}"')
            fw_page_ui.select_drop_down_value_new('Zone', self.zone)
            logger.info(f'Select "Mode" dropdown box as "{self.mode}"')
            fw_page_ui.select_drop_down_value_new('Mode / IP Assignment', self.mode)
            ip = '192.1.1.1'
            logger.info(f'Set "IP Address" textbox as "{ip}"')
            fw_page_ui.clear_text_field(*ip_address_textbox)
            fw_page_ui.set_input_text_field(*ip_address_textbox, field_val=ip)
            mask = '255.255.0.0'
            logger.info(f'Set "Subnet Mask" textbox as "{mask}"')
            fw_page_ui.clear_text_field(*netmask_textbox)
            fw_page_ui.set_input_text_field(*netmask_textbox, field_val=mask)
            logger.info('Enable Management "HTTPS" toggle')
            fw_page_ui.toggle_button(*mgmt_https_toggle, enabled=True)
        Assertion.assert_equal(rc, True, "ERR: init_interface failed!!")

    def test_03_check_lan_domain_name(self):
        test = '1234567890abcd.corp.test.com'
        fw_page_ui.clear_text_field(*domain_textbox)
        fw_page_ui.set_input_text_field(*domain_textbox, field_val=test)
        logger.info('Click "OK"')
        fw_page_ui.click_element('css', '.configure-modal-ipv4__button-ok')
        fw_page_ui.wait_for_page_data_to_be_rendered()
        rc = fw_page_ui.compare_alert_message(['Changes made.', 'Changes made'])
        fw_page_ui.wait_for_element_to_be_invisible(*status_info)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        Assertion.assert_equal(rc, True, "ERR: check_domain_name failed!!")

    def test_04_check_wan_domain_name(self):
        self.zone = 'WAN'
        self.mode = 'Static'
        self.test_02_init_interface()
        self.test_03_check_lan_domain_name()

    def test_05_check_dmz_domain_name(self):
        self.zone = 'DMZ'
        self.test_02_init_interface()
        self.test_03_check_lan_domain_name()

    def test_06_check_wlan_domain_name(self):
        self.zone = 'WLAN'
        self.test_02_init_interface()
        self.test_03_check_lan_domain_name()


# Wiremode interface can be changed into pppoe/dhcp/pppoe mode or unassigned
@unittest.skipIf('tz80' in Params.product.lower(), "Skipping this case because TZ80 do NOT support wire-mode interface.")
class TestCommon_3585634(Test):
    uuid = "SOSAIOT-TC-56242"
    testrail_uuid = "3585634"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_set_X3_to_wire_mode(self):
        X3 = {
            'if': 'x3',
            'zone': 'WAN',
            'mode': 'wire-mode',
            'type': 'bypass',
            'wire_paired_interface': 'x4',
            'wire_paired_zone': 'WAN'
        }
        rc = interface_api.config_interface(**X3)
        Assertion.assert_equal(rc, True, "ERR: set_X3_to_wire_mode failed!!")

    def test_02_change_X3_to_pppoe(self):
        X3 = {
            'if': 'x3',
            'zone': 'WAN',
            'mode': 'pppoe'
        }
        rc = interface_api.config_interface(**X3)
        Assertion.assert_equal(rc, True, "ERR: set_X3_to_wire_mode failed!!")

    def test_03_change_X3_to_dhcp(self):
        self.test_01_set_X3_to_wire_mode()
        X3 = {
            'if': 'x3',
            'zone': 'WAN',
            'mode': 'dhcp'
        }
        rc = interface_api.config_interface(**X3)
        Assertion.assert_equal(rc, True, "ERR: set_X3_to_wire_mode failed!!")

    def test_04_change_X3_to_pptp(self):
        self.test_01_set_X3_to_wire_mode()
        X3 = {
            'if': 'x3',
            'zone': 'WAN',
            'mode': 'pptp',
            'pptp_server': '192.1.2.1',
        }
        rc = interface_api.config_interface(**X3)
        Assertion.assert_equal(rc, True, "ERR: set_X3_to_wire_mode failed!!")

    def test_05_change_X3_to_unassign(self):
        self.test_01_set_X3_to_wire_mode()
        rc = interface_api.unassign_interface(interface='X3')
        Assertion.assert_equal(rc, True, "ERR: set_X3_to_wire_mode failed!!")
    

# Verify default WAN interface can not be assigned to other Zone (not suitable for TZ serial)
class TestCommon_1515776(Test):
    uuid = "SOSAIOT-TC-56228"
    testrail_uuid = "1515776"
    description = show_testcase_info(TESTPLAN, testrail_uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.testrail_uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_set_wan_interface_to_other_zone(self):
        X1 = {
            'if': 'x1',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.Mask
        }
        rc = not interface_api.config_interface(**X1)
        Assertion.assert_equal(rc, True, "ERR: set_wan_interface_to_other_zone should fail!!")