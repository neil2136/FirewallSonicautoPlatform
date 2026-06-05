from definition.settings import *


def init_test_page(refresh=0):
    base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
    url = base_url + 'system/administrator'
    fw_page_ui.login_ui_with_head(headless=True, browser_type='chrome')
    # fw_page_ui.login_ui()
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i + 1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()


def goto_saml_profile_tab_on_administration_page():
    init_test_page()
    logger.info('> Switch to Management tab on Administration/Management page')
    fw_page_ui.click_element('xpath', '//*[text()="Management"]')
    logger.info('> Switch to Management tab on Administration/Management page DONE')
    logger.info('> Click SAML Profile button on Administration/Management page')
    fw_page_ui.click_element('xpath', '//*[text()="SAML Profiles"]')
    logger.info('> Click SAML Profile button on Administration/Management page DONE')


def disable_profile_for_management(profile):
    locate_enable = ['xpath', f'//input[@name="{profile}"]/parent::div']
    goto_saml_profile_tab_on_administration_page()
    logger.info('> disable profile on Administration/Management page')
    e_obj = fw_page_ui.get_element(*locate_enable)
    print(e_obj.get_attribute('class'))

    if 'sw-toggle--off' in e_obj.get_attribute('class'):
        logger.info('it is disable now, do nothing')
    else:
        logger.info('it is enable now, disable it')
        fw_page_ui.click_element(*locate_enable)
        time.sleep(3)
        logger.info('disable it DONE, start to SAVE')
        fw_page_ui.click_element(*locate_apply)
        logger.info('SAVE DONE')
        time.sleep(3)
    fw_page_ui.quit()

    goto_saml_profile_tab_on_administration_page()
    e_obj2 = fw_page_ui.get_element(*locate_enable)
    print(e_obj2.get_attribute('class'))
    return 'sw-toggle--off' in e_obj2.get_attribute('class')


def enable_profile_for_management(profile):
    locate_enable = ['xpath', f'//input[@name="{profile}"]/parent::div']
    goto_saml_profile_tab_on_administration_page()
    logger.info('> enable profile on Administration/Management page')
    e_obj = fw_page_ui.get_element(*locate_enable)
    print(e_obj.get_attribute('class'))
    if 'sw-toggle--off' in e_obj.get_attribute('class'):
        logger.info('it is disable now, enable it')
        fw_page_ui.click_element(*locate_enable)
        time.sleep(3)
        logger.info('enable it DONE, start to SAVE')
        fw_page_ui.click_element(*locate_apply)
        logger.info('SAVE DONE')
        time.sleep(3)
    else:
        logger.info('it is enable now, do nothing')
    fw_page_ui.quit()

    time.sleep(3)
    goto_saml_profile_tab_on_administration_page()
    e_obj2 = fw_page_ui.get_element(*locate_enable)
    return 'sw-toggle--off' not in e_obj2.get_attribute('class')
