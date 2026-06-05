from definition.settings import *


def init_test_page(url, refresh=0):
    """init page steps, including start firefox, login, go to specific url and refresh if set

    :param str url: go to url address, example 'https://192.168.168.168/sonicui/7/m/mgmt/policies/ngpe-dns-policies'
    :param int refresh: refresh times, defaults to 0
    """
    PC1_LOGIN.send_command('pkill chrome')
    fw_page_ui.login_ui_with_head(headless=True, browser_type='chrome')
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i+1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()


def check_element_attribute(element: list, target, attribute='textContent'):
    """find a element and get its attribute then compare with the target 

    :param list element: one element to check, list should be ['{selector}', '{path}'], example ['css', '.sw-status-flag--normal']
    :param str or list target: target to compare with the attribute of element
    :param str attribute: attribute of element to check, example 'textContent'/'class'/'tagName'/..., defaults to 'textContent'
    :return bool: check result, True or False
    """
    text = fw_page_ui.get_attribute_value(*element, attrib_to_get_val=attribute)
    text = str(text).lstrip().rstrip()
    logger.info(f'> test: {text}')
    logger.info(f'> target: {target}')
    res = text in target or target in text if text and target else False
    logger.info(res)
    return res
