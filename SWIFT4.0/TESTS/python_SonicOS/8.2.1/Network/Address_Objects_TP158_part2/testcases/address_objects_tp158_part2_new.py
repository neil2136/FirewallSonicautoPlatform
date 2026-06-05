import json
import re
import ipaddress
from definition.settings import *
from definition.utils import *


# Expected: Address group and address objects that are displayed should be according to the view style selection.
class TestTC24_verify_address_object_view(Test):
    uuid = "SOSAIOT-TC-57777"
    description = show_testcase_info(TESTPLAN, 'tc24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_some_address_objects(self):
        reslist = []
        ao_dict1 = {
            'name': '20.1.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.1.1.0,255.255.255.0',
        }
        ao_dict2 = {
            'name': '20.2.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.2.1.0,255.255.255.0',
        }
        ao_dict3 = {
            'name': '20.3.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.3.1.0,255.255.255.0',
        }
        ao_dict4 = {
            'name': '20.4.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.4.1.0,255.255.255.0',
        }
        aolist = [ao_dict1, ao_dict2, ao_dict3, ao_dict4]
        for ao in aolist:
            res = addressobjectsapi.config_addressobject(**ao)
            reslist.append(res)
        logger.info(reslist)
        flag = all(reslist) if reslist is not None else False
        Assertion.assert_equal(flag, True, "ERR: add some address objects failed")

    def test_03_add_some_ao_groups_with_ao_as_member(self):
        group_dict1 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.1.1.0"
                                },
                                {
                                    "name": "20.2.1.0"
                                }
                            ]
                        },
                        "name": "group1"
                    }
                }
            ]
        }
        group_dict2 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.3.1.0"
                                },
                                {
                                    "name": "20.4.1.0"
                                }
                            ]
                        },
                        "name": "group2"
                    }
                }
            ]
        }
        res1 = addressobjectgroupapi.add_addressgroup(**group_dict1)
        res2 = addressobjectgroupapi.add_addressgroup(**group_dict2)
        Assertion.assert_equal(res1 & res2, True, "ERR: add ao groups failed")

    def test_04_check_address_object_view_list(self):
        initial_login_ui()
        view_arrow_xpath = "//div[contains(@class,'sw-content-toolbar__inner')]/div[contains(@class,'select-view-filter')]/div[contains(@class,'sw-select__icon')]"
        logger.info('click View arrow')
        fwpageui.click_element('xpath',view_arrow_xpath)
        # fwpageui.wait_for_element_to_be_visible('class', "//div[@class='sw-dropdown sw-typo-default']")
        res = fwpageui.does_element_exist('xpath', "//div[@class='sw-dropdown sw-typo-default']")
        if res:
            logger.info('get View drop down value')
            obj = fwpageui.get_elements('xpath', "//*[contains(@class, 'sw-dropdown-unit')]")
            all_values = [values.get_attribute('textContent') for values in obj]
            logger.info(all_values)
            Flag = True if all_values == ['All', 'Default', 'Custom'] else False
        else:
            logger.error("view drop down list doesn't exist,please check...")
        Assertion.assert_equal(Flag, True, "ERR: add ao groups failed")

    def test_05_check_address_objects_display_when_choose_all(self):
        fwpageui.move_to_the_element('xpath',"//div[contains(@class,'sw-dropdown__inner')]//span[text()='All']").click()
        fwpageui.wait_for_element_to_be_invisible('xpath',"//*[contains(@class, 'sw-dropdown-unit')]")
        checklist = ['X0 IP','X0 Subnet','20.1.1.0','20.2.1.0']
        checkres = []
        for check in checklist:
            res = fwpageui.does_element_exist_now('xpath',f"//div[contains(@class,'sw-table-body__cont__table')]//span[text()='{check}']")
            checkres.append(res)
        logger.info(f'checkres is :{checkres}')
        flag = True if checkres.count(True) == len(checkres) else False
        Assertion.assert_equal(flag, True, "ERR:  check address objects display when choose all failed")

    def test_06_check_address_objects_display_when_choose_default(self):
        select_ao_or_ao_group_view_item(viewitem='Default')
        checklist = ['X0 IP', 'X0 Subnet', '20.1.1.0', '20.2.1.0']
        checkres = []
        for check in checklist:
            res = fwpageui.does_element_exist_now('xpath',
                                              f"//div[contains(@class,'sw-table-body__cont__table')]//span[text()='{check}']")
            checkres.append(res)
        logger.info(f'checkres is :{checkres}')
        flag = True if checkres[0:2].count(True) == 2 and checkres[2:4].count(False) == 2 else False
        Assertion.assert_equal(flag, True, "ERR:  check address objects display when choose Default failed")

    def test_07_check_address_objects_display_when_choose_custom(self):
        select_ao_or_ao_group_view_item(viewitem='Custom')
        checklist = ['X0 IP', 'X0 Subnet', '20.1.1.0', '20.2.1.0']
        checkres = []
        for check in checklist:
            res = fwpageui.does_element_exist_now('xpath',
                                              f"//div[contains(@class,'sw-table-body__cont__table')]//span[text()='{check}']")
            checkres.append(res)
        logger.info(f'checkres is :{checkres}')
        flag = True if checkres[0:2].count(False) == 2 and checkres[2:4].count(True) == 2 else False
        Assertion.assert_equal(flag, True, "ERR:  check address objects display when choose custom failed")

# Expected: Default Address Groups should be available
class TestTC01_new_verify_default_address_groups(Test):
    uuid = "SOSAIOT-TC-57794"
    description = show_testcase_info(TESTPLAN, 'tc01_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_global_address_for_x0(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        res = interfaceipv6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X0 IPv6 static failed")

    def test_03_get_x0_link_local_address(self):
        output = interfaceipv6api.get_interface_address(name = 'X0')
        logger.info(f'output is : {output}')
        match = re.search(r'(fe80::[0-9a-f:]+)', output['ip_address'], re.IGNORECASE)
        x0_link_local = ''
        if match:
            x0_link_local = match.group(1)
            logger.info(f'ipv6_link_local is:{x0_link_local}')
            ParamCases.tc01_x0linklocal = x0_link_local
        flag = True if x0_link_local else False
        Assertion.assert_equal(flag, True, "ERR: get X0 Link Local failed")

    def test_04_check_all_default_address_groups_class_item(self):
        initial_login_ui()
        fwpageui.click_element('xpath',"//span[text()='Address Groups']")
        time.sleep(10)
        select_ao_or_ao_group_view_item(viewitem='Default')
        ip_version_selected_xpath = "//div[contains(@class,'sw-content-toolbar__inner')]/div[contains(@class,'ip-version')]"
        ip_version_value = fwpageui.get_element('xpath', ip_version_selected_xpath)
        ip_version_value_text = ip_version_value.text
        logger.info(f'ip_version_value_text is :{ip_version_value_text}')
        checkres = []
        flag = False
        if ip_version_value_text == 'IPv4 & IPv6':
            # res = fwpageui.does_element_exist_now('xpath',"//div[@class = 'sw-table-body__cont__table']")
            row_xpath =  "//div[@class='sw-table-body__cont__table']/div[contains(@class,'sw-table-row--light')]"
            rows = fwpageui.get_elements('xpath', row_xpath)
            for index, row in enumerate(rows, start=1):
                cell_10 = row.find_element('xpath', "./div[10]")
                cell_10_text = cell_10.text

                if cell_10_text == 'Default':
                    checkres.append(True)
                else:
                    checkres.append(False)
                    logger.info(f"Row {index} is not 'Default', actual value is: {cell_10_text}")
            logger.info(f"checkres is :{checkres}")
            flag = True if checkres.count(True) == len(checkres) else False
        else:
            logger.info("current view is not 'Default' and current ip version is not 'IPv4 & IPv6'" )
        Assertion.assert_equal(flag, True, "ERR:  check all default address groups are displayed failed")

    def test_05_check_default_address_groups_details(self):
        x0_interface_row_xpath = "//span[text()='X0 IPv6 Addresses']/ancestor::div[contains(@class, 'sw-table-row--light')]"
        logger.info("Find default address group : 'X0 IPv6 Address'")
        row = fwpageui.get_element('xpath', x0_interface_row_xpath)
        expand_xpath = ".//div[contains(@class,'sw-table-row__cell__trigger__cont')]"
        logger.info('expand this group')
        row.find_element('xpath', expand_xpath).click()
        x0_interface_details_row_xpath = "//div[contains(@class,'sw-table-expand-row__cont')]//div[contains(@class,'sw-table-row--light')]"
        logger.info("get details about this group ")
        expand_row = fwpageui.get_elements('xpath', x0_interface_details_row_xpath)
        x0_ipv6_address = {}
        for index, row in enumerate(expand_row, start=1):
            cell_name_text = row.find_element('xpath', ".//div[3]").text  # The name is in the fourth column.
            cell_detail_text = row.find_element('xpath', ".//div[4]").text  # details is in the fifth column
            x0_ipv6_address[cell_name_text] = cell_detail_text
        logger.info(f'x0_ipv6_address is :{x0_ipv6_address}')
        checkres = [False]
        if ParamCases.tc01_x0linklocal:
            checklist = [
                        f"'X0 IPv6 Link-Local Address': '{ParamCases.tc01_x0linklocal}/128'" ,
                        f"'X0 IPv6 Primary Static Address': '{Parameter.X0_V6_IP}/128'",
                        "'X0 IPv6 Primary Dynamic Address': '::/128'"
                         ]
            checkres = [i in str(x0_ipv6_address) for i in checklist]
            logger.info(f'checkres is :{checkres}')
            logger.info(f'checklist is:{checklist}')
        else:
            logger.info(f'ParamCases.tc01_x0linklocal actual value is:{ParamCases.tc01_x0linklocal},please check...')
        Assertion.assert_equal(all(checkres), True, "ERR:  check X0 ipv6 address defaultgroups are displayed failed")

# Expected: all Groups where the Address Object is a member of are filtered out.
class TestTC02_new_verify_filter_function(Test):
    uuid = "SOSAIOT-TC-57795"
    description = show_testcase_info(TESTPLAN, 'tc02_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc02_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_ao_group_with_same_ao_as_group1(self):
        group_dict1 = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.1.1.0"
                                }
                            ]
                        },
                        "name": "group3"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.add_addressgroup(**group_dict1)
        Assertion.assert_equal(res, True, "ERR: add ao group with same ao as group1 failed")

    def test_03_test_ao_group_fileter_function(self):
        initial_login_ui()
        fwpageui.click_element('xpath', "//span[text()='Address Groups']")
        time.sleep(10)
        search_xpath = "//input[@placeholder='Search...']"
        logger.info("input '20.1.1.0' in Search field")
        fwpageui.set_text_field('xpath',search_xpath,'20.1.1.0')
        time.sleep(5)
        res1 = fwpageui.does_element_exist_now('xpath',"//span[text()='group1']")
        res2 = fwpageui.does_element_exist_now('xpath',"//span[text()='group3']")
        logger.info(f'res1 is:{res1},res2 is :{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: test ao group filter failed")

# Expected: Alert pops up and fail to create address groups,added from GEN7-48193
class TestTC03_new_verify_alert_pops_up_when_ao_groups_contain_each(Test):
    uuid = "SOSAIOT-TC-57796"
    description = show_testcase_info(TESTPLAN, 'tc03_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_three_ao_groups(self):
        checkres = []
        for i in range(1,4):
            group_dict = {
                "address_groups": [
                    {
                        "ipv6": {
                            "name": f"tc03group{i}"
                        }
                    }
                ]
            }
            res = addressobjectgroupapi.add_addressgroup(**group_dict)
            checkres.append(res)
        logger.info(f'checkres is :{checkres}')
        flag = True if checkres.count(True) == len(checkres) else False
        Assertion.assert_equal(flag, True, "ERR: add ao groups failed")

    def test_03_add_tc03group1_include_tc03group2_and_tc03group3(self):
        group1_dict ={
            "address_groups": [
                {
                    "ipv6": {
                        "address_group": {
                            "ipv6": [
                                {
                                    "name": "tc03group2"
                                },
                                {
                                    "name": "tc03group3"
                                }
                            ]
                        },
                        "name": "tc03group1"
                    }
                }
            ]
        }
        res = addressobjectgroupapi.edit_addressgroup_by_name(version='v6',name='tc03group1', msg=False, **group1_dict)
        Assertion.assert_equal(res, True, "ERR: add group1 include group2 and group3 failed")

    def test_04_add_tc03group2_include_tc03group1_and_tc03group3(self):
        group2_dict ={
            "address_groups": [
                {
                    "ipv6": {
                        "address_group": {
                            "ipv6": [
                                {
                                    "name": "tc03group1"
                                },
                                {
                                    "name": "tc03group3"
                                }
                            ]
                        },
                        "name": "tc03group2"
                    }
                }
            ]
        }
        res, msg = addressobjectgroupapi.edit_addressgroup_by_name(version='v6',name='tc03group2', msg=True, **group2_dict)
        logger.info(f'res is:{res},msg is:{msg}')
        flag = True if not res and 'Circular Group reference' in str(msg) else False
        Assertion.assert_equal(flag, True, "ERR: add tc03group2 include tc03group2 and tc03group3 failed")

# Expected: Added from GEN7-50821
class TestTC04_new_verify_create_new_object_with_special_address(Test):
    uuid = "SOSAIOT-TC-57797"
    description = show_testcase_info(TESTPLAN, 'tc04_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc04_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_special_address_objects_with_network_type(self):
        masklist = ['255.0.0.0','255.128.0.0','0.0.0.0','255.255.255.0']
        checkres = []
        for index, member in enumerate(masklist, start=1):
            test_dict = {
                'name': f'tc04netao{index}',
                'zone': 'LAN',
                'object_type': 'network',
                'value': f'0.0.0.0,{member}',
            }
            logger.info(f'------test_dict is :{test_dict}')
            res = addressobjectsapi.config_addressobject(**test_dict)
            checkres.append(res)
        logger.info(f'checkres is:{checkres}')
        flag = True if checkres.count(True) == len(checkres) else False
        Assertion.assert_equal(flag, True, "ERR: add special address with network type failed")

    def test_03_add_special_address_objects_with_host_type(self):
        test_dict = {
            'name': 'tc04hostao5',
            'zone': 'LAN',
            'object_type': 'host',
            'value': '0.0.0.0',
        }
        res = addressobjectsapi.config_addressobject(**test_dict)
        Assertion.assert_equal(res, True, "ERR: add special address with host type failed")

    def test_04_check_added_specical_address_objects_display(self):
        # cannot get IP and mask for ao by api,so use selenium
        initial_login_ui()
        view_arrow_xpath = "//div[contains(@class,'sw-content-toolbar__inner')]/div[contains(@class,'select-view-filter')]/div[contains(@class,'sw-select__icon')]"
        logger.info('click View arrow')
        fwpageui.click_element('xpath', view_arrow_xpath)
        fwpageui.wait_for_element_to_be_visible('xpath', "//div[@class='sw-dropdown sw-typo-default']")
        fwpageui.move_to_the_element('xpath',
                                     "//div[contains(@class,'sw-dropdown__inner')]//span[text()='Custom']").click()
        fwpageui.wait_for_element_to_be_invisible('xpath', "//*[contains(@class, 'sw-dropdown-unit')]")

        checklist = ["0.0.0.0/255.255.255.255", "0.0.0.0/255.0.0.0",
                     "0.0.0.0/255.128.0.0", "0.0.0.0/0.0.0.0", "0.0.0.0/255.255.255.0"]
        checkres = []
        for check in checklist:
            logger.info(f"now begin to check address object detail :{check}")
            res = fwpageui.does_element_exist_now('xpath',f"//div[text()='{check}']")
            checkres.append(res)
        logger.info(f'checkres is :{checkres}')
        flag = True if checkres.count(True)==len(checklist) else False
        Assertion.assert_equal(flag, True, "ERR:  check special address objects display failed")

# Expected: "already exists." will pops up when add existed custom ao or ao group
class TestTC05_new_add_exist_custom_ao_and_ao_group(Test):
    uuid = "SOSAIOT-TC-57798"
    description = show_testcase_info(TESTPLAN, 'tc05_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc05_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_existed_custom_address_objects(self):
        ao_dict = {
            'name': '20.1.1.0',
            'zone': 'LAN',
            'object_type': 'network',
            'value': '20.1.1.0,255.255.255.0',
        }
        res, msg = addressobjectsapi.config_addressobject(msg=True, **ao_dict)
        promptmsg = "'address-object ipv4 name 20.1.1.0' already exists"
        Assertion.assert_regular(str(msg), promptmsg, "ERR:  check prompt message when add existed custom ao failed")

    def test_03_add_existed_custom_address_object_group(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "20.1.1.0"
                                },
                                {
                                    "name": "20.2.1.0"
                                }
                            ]
                        },
                        "name": "group1"
                    }
                }
            ]
        }
        res , msg = addressobjectgroupapi.add_addressgroup(msg=True, **group_dict)
        promptmsg = "'address-group ipv4 name group1' already exists."
        Assertion.assert_regular(str(msg), promptmsg, "ERR:  check prompt message when add existed custom ao group failed")

# Expected: "already exists." will pops up when add existed default ao or ao group
class TestTC06_new_add_exist_default_ao_and_ao_group(Test):
    uuid = "SOSAIOT-TC-57799"
    description = show_testcase_info(TESTPLAN, 'tc06_new', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc06_new')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_existed_default_address_object(self):
        test_dict = {
            'name': 'X1 IP',
            'zone': 'WAN',
            'object_type': 'host',
            'value': Parameter.X1_IP,
        }
        res, msg = addressobjectsapi.config_addressobject(msg = True, **test_dict)
        promptmsg = "'X1 IP' already exists."
        Assertion.assert_regular(str(msg), promptmsg, "ERR: add existed default address object failed")

    def test_03_add_existed_ipv6_default_address_object_group_ipv6(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv6": {
                        "address_object": {
                            "ipv6": [
                                {
                                    "name": "X0 IPv6 Primary Dynamic Address Subnet"
                                }
                            ]
                        },
                        "name": "LAN IPv6 Subnets"
                    }
                }
            ]
        }
        res, msg = addressobjectgroupapi.add_addressgroup(msg = True, **group_dict)
        promptmsg = r"address-group ipv6 name \"LAN IPv6 Subnets\".*already exists"
        Assertion.assert_regular(str(msg), promptmsg, "ERR: add existed default address object failed")

    def test_04_add_existed_ipv4_default_address_object_group(self):
        group_dict = {
            "address_groups": [
                {
                    "ipv4": {
                        "address_object": {
                            "ipv4": [
                                {
                                    "name": "X0 Subnet"
                                }
                            ]
                        },
                        "name": "LAN Subnets"
                    }
                }
            ]
        }
        res, msg = addressobjectgroupapi.add_addressgroup(msg = True, **group_dict)
        # promptmsg = r"Creating LAN Subnets: Name \(already exists\)"
        promptmsg = "'LAN Subnets' already exists."
        Assertion.assert_regular(str(msg), promptmsg, "ERR: add existed default address object failed")

