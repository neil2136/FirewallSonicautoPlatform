from definition.settings import *

def get_dropdown_box_element_xpath(identifier, element_type="arrow"):
    """get_dropdown_box_element_xpath, like arrow, text, pencil, or info

    :param str identifier: identifier of the dropdown box,
    :param str element_type: element to find, like arrow, text, pencil, or info, defaults to "arrow"
    :return list: return ['xpath', {path}]
    """
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

def get_toggle_xpath(identifier):
    path = ['xpath', f'//div[text()="{identifier}"]/following-sibling::*[contains(@class, "sw-form-row__field")]/descendant::*[contains(@class, "sw-toggle")]']
    return path

def get_textbox_element_xpath(identifier='', name=''):
    if name:
        return ['name', name]
    path = ['xpath', f'//*[text()="{identifier}"]/ancestor::*[contains(@class, "sw-form-row__field-cont")]/descendant::*[contains(@class, "sw-textfield__wrapper__input")]']
    return path


#urls
base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
interface_page = base_url + 'network/interfaces'

# path
## common
license_icon = ['css', '.sw-status-flag--normal']
license_info = ['xpath', '//div[contains(@class, "sw-typo-field-value")]']
icon_info = ['css', '.sw-form-row__field.sw-typo-field-value']
information_icon = ['css', '.sw-status-flag--informational']
config_button = ['xpath', '//span[@class="fw-app-header__configurable"]/following-sibling::div[contains(@class, "sw-toggle")]']
status_info = ['xpath', '//div[contains(@class, "sw-status-info")]']


## interface page
interface_column = ['css', '.sw-table-header__col__cell__wrapper__cont__text']

### Edit interface window
edit_interface_window = ['css', '.configure-modal-ipv4']
ip_address_textbox = ['name', 'textfield-ip-address']
netmask_textbox = ['name', 'textfield-subnet-mask']
gateway_textbox = ['name', 'textfield-default-gateway']
comment_textbox = ['name', 'textfield-comment']
hostname_textbox = ['name', 'textfield-host-name']
domain_textbox = ['name', 'textfield-domain-name']
disable_zone_dropdown = ['xpath', '//div[text()="Zone"]/following-sibling::*[contains(@class, "sw-form-row__field")]/div']
mode_arrow = get_dropdown_box_element_xpath("Mode / IP Assignment", 'arrow')
mode_box_text = get_dropdown_box_element_xpath("Mode / IP Assignment", 'text')
redirect_toggle = get_toggle_xpath('Add rule to enable redirect from HTTP to HTTPS')
mgmt_https_toggle = ['xpath', '//*[contains(@class, "toggle-enable-https")]']
login_https_toggle = ['css', '.static-ip-mode__toggle-enable-login-https']
ping_toggle = get_toggle_xpath('Ping')
user_http_toggle = get_toggle_xpath('HTTP')

### transparent mode
trans_new_toggle_G = get_toggle_xpath('Enable Gratuitous ARP Forwarding Towards WAN')
trans_new_toggle_A = get_toggle_xpath('Enable Automatic Gratuitous ARP Generation Towards WAN')
transparent_range_arrow = get_dropdown_box_element_xpath("Transparent Range", 'arrow')

### l2b mode
never_route_toggle = ['css', '.layer-2-bridged-mode__toggle-never-route-traffic']
block_non_ip_toggle = ['css', '.layer-2-bridged-mode__toggle-block-non-ip-traffic']
sniff_toggle = ['css', '.layer-2-bridged-mode__toggle-only-sniff']

### dhcp mode
request_renew_toggle = ['css', '.dhcp__toggle-request-renew']

### Add address window
start_ip_textbox = get_textbox_element_xpath(identifier='Starting IP Address')
end_ip_textbox = get_textbox_element_xpath(identifier='Ending IP Address')
network_textbox = get_textbox_element_xpath(identifier='Network')
mask_textbox = get_textbox_element_xpath(identifier='Netmask / Prefix Length')