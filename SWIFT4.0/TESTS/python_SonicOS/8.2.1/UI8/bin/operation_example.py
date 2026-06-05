from bin.global_var import *
from bin.common_operation import *
from bin.common_path import *

### PC_Runner()
pc_runner = PCRunner()

### init_test_page()
url = 'https://192.168.168.168/sonicui/7/m/mgmt/policies/ngpe-dns-policies'
pc_runner.goto_test_page(url)
pc_runner.goto_test_page(url, refresh=2)


### check_element_attribute()
# check default metric dropdown box is not available
default_metric_dropdown_box = ['xpath', '//input[@name="metricTypeOption"]/..']
rc = not pc_runner.check_element_attribute(default_metric_dropdown_box, 'sw-select--disabled', 'class')

# check user name textbox is available
path = get_textbox_element_xpath(identifier='UserName')
rc = pc_runner.check_element_attribute(path, 'textfield-user-name', 'name')

# check mode dropdown box textContent displays 'Static IP Mode'
mode_box_text = get_dropdown_box_element_xpath("Mode / IP Assignment", 'text')
rc_default = pc_runner.check_element_attribute(mode_box_text, 'Static IP Mode')

# check comment textbox displays 'Default LAN'
comment_textbox = ['name', 'textfield-comment']
rc = pc_runner.check_element_attribute(comment_textbox, 'Default LAN', 'value')


### check_elements_attribute()
# Check Interfaces "table column" details
interface_column = ['css', '.sw-table-header__col__cell__wrapper__cont__text']
target = ['Name', 'Zone', 'IP Address', 'Subnet Mask', 'IP Assignment', 'Status', 'Comment']
rc = pc_runner.check_elements_attribute(interface_column, target=target)

# Check multiple entries are not available
# rc = pc_runner.check_elements_attribute(path, 'sw-select--disable', 'class')


### check_dropdown_list_value()
rip_arrow = get_dropdown_box_element_xpath('RIP', 'arrow')
target_list = ['Disabled', 'Send and Receive', 'Send Only', 'Receive Only', 'Passive']
logger.info('------ Check "RIP" Dropdown box list values')
logger.info('Click "RIP" dropdown box arrow to expand')
fw_page_ui.click_element(*rip_arrow) #Click is necessary. after clicking, the dropdown list displays correctly.
rc = pc_runner.check_dropdown_list_value(target_list)
