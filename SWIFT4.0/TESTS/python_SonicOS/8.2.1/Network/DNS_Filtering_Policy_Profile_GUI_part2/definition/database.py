from definition.settings import *



def get_dropdown_box_element_xpath(identifier, element_type="arrow"):
    path = ['xpath', f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "sw-select__icon")]']
    if element_type.lower() == 'text':
        path = ['xpath', f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "sw-select__label-cont")]']
    if element_type.lower() == 'pencil':
        path = ['xpath', f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "icon-pencil")]']
    if element_type.lower() == 'info':
        path = ['xpath', f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "icon-info")]']
    return path

def get_table_entry_element_xpath(identifier, element="arrow"):
    """get_table_entry_element_xpath, like arrow, checkbox, drag, or identified path

    :param str identifier: identifier of the table entry, like entry name
    :param str element: element to find, like arrow, checkbox, drag or identified path, defaults to "arrow"
    :return list: return ['xpath', {path}]
    """
    path = ''
    if element == "arrow":
        path = f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-table-row--light")]/descendant::*[contains(@class, "icon-arrow-up")]'
    elif element == "checkbox":
        path = f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-table-row--light")]/descendant::*[contains(@class, "sw-checkbox--light")]'
    elif element == "drag":
        path = f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-table-row--light")]/descendant::*[contains(@class, "sw-table-row__cell__handle__icon")]'
    elif element:
        # identified element should not include ['], instead as ["]
        path = f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-table-row--light")]/{element}'
    else:
        logger.error("Need input element type or path!!")
        return []
    return ['xpath', path]

def get_xpath_by_text(name):
    path = ['xpath', f'//span[text()="{name}"]']
    return path

#urls
base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
dns_policy_page = base_url + 'policies/ngpe-dns-policies'
dns_profile_page = base_url + 'objects/dns-filtering-profile'
dns_security_settings_page = base_url + 'security-services/dns-security'
dns_security_report_page = base_url + 'security-services/dns-security-reports'

# path
# common
license_icon = ['css', '.sw-status-flag--normal']
license_info = ['xpath', '//div[contains(@class, "sw-typo-field-value")]']
icon_info = ['css', '.sw-form-row__field.sw-typo-field-value']
information_icon = ['css', '.sw-status-flag--informational']
config_button = ['xpath', '//span[@class="fw-app-header__configurable"]/following-sibling::div[contains(@class, "sw-toggle")]']


# dns policy page
filter_action = get_xpath_by_text('Filter')
proxy_action = get_xpath_by_text('Proxy')
policy_name = ['name', 'nameText']
# register_icon = ['xpath', '//div[contains(@class, "sw-status-flag")]/descendant::*[contains(@class, "sw-icon__inner")]']
action_info = ['class', 'sw-tooltip__inner']
selected_proxy_mode = ['xpath', '//span[contains(@class, "sw-radio__fake-radio-button--checked")]/following-sibling::span[1]']
# adult_dropdown = ['xpath', '//span[text()="Adult"]/../following-sibling::div/div/div[1]/span']
# schedule_dropdown = ['xpath', '//div[contains(@class, "sw-form-row__label") and text()="Schedule"]/following-sibling::div/div/div[1]/span']
status_info = ['xpath', '//div[contains(@class, "sw-status-info")]']
close_icon = ['css', '.sw-modal__close']
policy_priority_part = 'div[5]'
profile_priority_part = 'div[4]'
policy_checkbox = get_table_entry_element_xpath(CParam.Name, "checkbox")
move_up_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[1]']
move_down_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[2]']
policy_drag = get_table_entry_element_xpath(CParam.Name, 'drag')
clone_up_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[1]']
clone_down_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[2]']

profile_arrow = get_dropdown_box_element_xpath("Profile", 'arrow')
profile_box_text = get_dropdown_box_element_xpath("Profile", 'text')
profile_pencil = get_dropdown_box_element_xpath("Profile", 'pencil')
schedule_arrow = get_dropdown_box_element_xpath("Schedule", 'arrow')
schedule_box_text = get_dropdown_box_element_xpath("Schedule", 'text')
schedule_pencil = get_dropdown_box_element_xpath("Schedule", 'pencil')
service_arrow = get_dropdown_box_element_xpath("Service", 'arrow')
service_box_text = get_dropdown_box_element_xpath("Service", 'text')
service_pencil = get_dropdown_box_element_xpath("Service", 'pencil')
address_arrow = get_dropdown_box_element_xpath("Address", 'arrow')
address_box_text = get_dropdown_box_element_xpath("Address", 'text')
address_pencil = get_dropdown_box_element_xpath("Address", 'pencil')


# dns filtering profile page
profile_top_button_class = 'sw-icon-button__label-cont'
profile_column_class = 'sw-table-header__col__cell__wrapper__cont__text'
profile_expanded_form = ['css', '.sw-form.dns-filtering-category-table-render__expanded-form']
