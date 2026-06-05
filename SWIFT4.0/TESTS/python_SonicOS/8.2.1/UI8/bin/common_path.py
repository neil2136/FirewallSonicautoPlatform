from bin.global_var import *


def get_dropdown_box_element_xpath(identifier, element_type="arrow", strict=True):
    """get the specific type of element related to the dropdown_box with the identifier, and return the element xpath location

    :param str identifier: identifier of the dropdown box, 
        example:In Device/Settings/Administration/Firewall Administrator page, 'Wireless Controller Mode' dropdown box, the identifier is 'Wireless Controller Mode'
    :param str element_type: target element type related to the box, like arrow, text, pencil, or info, defaults to "arrow"
    :return list: return ['xpath', {path}]
    """
    if strict:
        common_path = f"//div[text()='{identifier}']/following-sibling::*[contains(@class, 'sw-form-row__field')]"
    else:
        common_path = f"//div[contains(text(), '{identifier}')]/following-sibling::*[contains(@class, 'sw-form-row__field')]"
    path = ['xpath', common_path + "/descendant::*[contains(@class, 'sw-select__icon')]"]
    if element_type.lower() == 'text':
        path = ['xpath', common_path + "/descendant::*[contains(@class, 'sw-select__label-cont')]"]
    if element_type.lower() == 'pencil':
        path = ['xpath', common_path + "/descendant::*[contains(@class, 'icon-pencil')]"]
    if element_type.lower() == 'info':
        path = ['xpath', common_path + "/descendant::*[contains(@class, 'icon-info')]"]
    return path
# example:
# mode_arrow = get_dropdown_box_element_xpath("Mode / IP Assignment", 'arrow')

def get_table_entry_element_xpath(identifier, element="arrow", strict=True):
    """get_table_entry_element_xpath, like arrow, checkbox, drag, hit, or identified path

    :param str identifier: identifier of the table entry, like entry name
    :param str element: element to find, like arrow, checkbox, drag, hit, or identified path, defaults to "arrow"
    :return list: return ['xpath', {path}]
    """
    path = ''
    if strict:
        common_path = f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-table-row--light")]'
    else:
        common_path = f'//*[contains(text(), "{identifier}")]/ancestor::*[contains(@class, "sw-table-row--light")]'
    if element == "arrow":
        path = common_path + '/descendant::*[contains(@class, "icon-arrow-up")]'
    elif element == "checkbox":
        path = common_path + '/descendant::*[contains(@class, "sw-checkbox--light")]'
    elif element == "drag":
        path = common_path + '/descendant::*[contains(@class, "sw-table-row__cell__handle__icon")]'
    elif element == "hit":
        path = common_path + '/descendant::*[contains(@class, "fw-ftr-ngpe-access-rules__hit-num")]'
    elif element:
        # identified element should not include ['], instead as ["]
        path = common_path + f'/{element}'
    else:
        logger.error("Need input element type or path!!")
        return []
    return ['xpath', path]


def get_xpath_by_text(name, tag='span'):
    """return the element xpath location by name

    :param str name: text to find element, can locate only one element.
    :param str tag: tag type, example: span/div/...or use wildcard "*", defaults to "span"
    :return list: return ['xpath', {path}]
    """
    path = ['xpath', f'//{tag}[text()="{name}"]']
    return path


def get_toggle_xpath(identifier):
    identifier_list = [
        f'//span[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-toggle")]',
        f'//span[text()="{identifier}"]/../following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "sw-toggle")]',
        f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "sw-toggle")]'
    ]
    path = ['xpath', '|'.join(identifier_list)]
    return path
# example:
# redirect_toggle = get_toggle_xpath('Add rule to enable redirect from HTTP to HTTPS')


def get_textbox_element_xpath(identifier='', name=''):
    if name:
        return ['name', name]
    path = ['xpath', f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-form-row__field-cont")]/descendant::*[contains(@class, "sw-textfield__wrapper__input")]']
    return path
# example:
# mask_textbox = get_textbox_element_xpath(identifier='Netmask / Prefix Length')


# fw urls
base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
dns_policy_page = base_url + 'policies/ngpe-dns-policies'
dns_profile_page = base_url + 'objects/dns-filtering-profile'
dns_security_settings_page = base_url + 'security-services/dns-security'
dns_security_report_page = base_url + 'security-services/dns-security-reports'
decryption_policies_page = base_url + 'policies/ngpe-decryption-policies'


# common path collection:
license_icon = ['css', '.sw-status-flag--normal']
license_info = ['xpath', '//div[contains(@class, "sw-typo-field-value")]']
information_icon = ['css', '.sw-status-flag--informational']
icon_info = ['css', '.sw-form-row__field.sw-typo-field-value']
config_button = ['xpath',
                 '//span[@class="fw-app-header__configurable"]/following-sibling::div[contains(@class, "sw-toggle")]']
status_info = ['xpath', '//div[contains(@class, "sw-status-info")]'] # prompted alert status info after submit actions
status_para_info = ['class', 'sw-status-info__text__message__para']
table_column_titles = ['css', '.sw-table-header__col__cell__wrapper__cont__text']



# need check:
filter_action = get_xpath_by_text('Filter')
status_info = ['xpath', '//div[contains(@class, "sw-status-info")]']
close_icon = ['css', '.sw-modal__close']
move_up_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[1]']
move_down_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[2]']
clone_up_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[1]']
clone_down_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[2]']
profile_arrow = get_dropdown_box_element_xpath("Profile", 'arrow')
profile_box_text = get_dropdown_box_element_xpath("Profile", 'text')
profile_pencil = get_dropdown_box_element_xpath("Profile", 'pencil')

# dns policy page
# filter_action = get_xpath_by_text('Filter')
# proxy_action = get_xpath_by_text('Proxy')
# policy_name = ['name', 'nameText']
# action_info = ['class', 'sw-tooltip__inner']
# selected_proxy_mode = ['xpath',
#                        '//span[contains(@class, "sw-radio__fake-radio-button--checked")]/following-sibling::span[1]']
# status_info = ['xpath', '//div[contains(@class, "sw-status-info")]']
# close_icon = ['css', '.sw-modal__close']
# policy_priority_part = 'div[5]'
# profile_priority_part = 'div[4]'
# move_up_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[1]']
# move_down_button = ['xpath', '//span[contains(text(), "Move")]/following-sibling::span[2]']
# clone_up_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[1]']
# clone_down_button = ['xpath', '//span[contains(text(), "Clone")]/following-sibling::span[2]']

# profile_arrow = get_dropdown_box_element_xpath("Profile", 'arrow')
# profile_box_text = get_dropdown_box_element_xpath("Profile", 'text')
# profile_pencil = get_dropdown_box_element_xpath("Profile", 'pencil')
# schedule_arrow = get_dropdown_box_element_xpath("Schedule", 'arrow')
# schedule_box_text = get_dropdown_box_element_xpath("Schedule", 'text')
# schedule_pencil = get_dropdown_box_element_xpath("Schedule", 'pencil')
# service_arrow = get_dropdown_box_element_xpath("Service", 'arrow')
# service_box_text = get_dropdown_box_element_xpath("Service", 'text')
# service_pencil = get_dropdown_box_element_xpath("Service", 'pencil')
# address_arrow = get_dropdown_box_element_xpath("Address", 'arrow')
# address_box_text = get_dropdown_box_element_xpath("Address", 'text')
# address_pencil = get_dropdown_box_element_xpath("Address", 'pencil')

# dns filtering profile page
# profile_top_button_class = 'sw-icon-button__label-cont'
# profile_column_class = 'sw-table-header__col__cell__wrapper__cont__text'
# profile_expanded_form = ['css', '.sw-form.dns-filtering-category-table-render__expanded-form']

# example:
# edit_interface_window = ['css', '.configure-modal-ipv4']


