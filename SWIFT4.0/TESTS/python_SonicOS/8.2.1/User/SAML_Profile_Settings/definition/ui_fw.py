from definition.settings import *
# import pyautogui


def init_test_page(refresh=0):
    base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
    url = base_url + 'users/users-settings'
    status = os.system('pkill firefox')
    logger.info(f"kill firefox result:{status}")
    fw_page_ui.login_ui_with_head()
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i + 1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()


# def import_idp_xml_file_via_selenium():
#     init_test_page()
#     idp_config_button = ['xpath', '(//button[text()="Configure"])[6]']
#     logger.info('Click saml idp Configure button')
#     fw_page_ui.click_element(*idp_config_button)
#     # idp_check = ['xpath', "//div[text()='idp_test']"]
#     fw_page_ui.click_element(*['xpath', '//span[text()="Import from File"]'])
#     fw_page_ui.set_input_text_field(*['xpath', '//input[@name="name"]'], 'cyuan')
#     logger.info('====>click upload button')
#     fw_page_ui.click_element(*['xpath', "//*[text()='Add File']"])
#     time.sleep(2)
#     pyautogui.write(r'/tmp/sonicauto.xml')
#     pyautogui.press('enter')
#     time.sleep(2)
#     fw_page_ui.click_element(*['xpath', '//button[text()="Next"]'])
#
#     # logger.info('Cancle  Restart!!')
#     # fw_page_ui.click_element('xpath', '(//button[text()="Cancel"])[2]')
#     fw_page_ui.accept_alert()
#     time.sleep(2)
#
#     fw_page_ui.set_input_text_field(*['xpath', '//input[@name="idp-userName"]'], 'username')
#     fw_page_ui.set_input_text_field(*['xpath', '//input[@name="idp-groupName"]'], 'departname')
#     fw_page_ui.click_element('xpath', '//button[text()="Save"]')
#     logger.info('==========Saved success!')
#     fw_page_ui.click_element('xpath', '//button[text()="Continue"]')
#     logger.info('==========Continue success!')
#     fw_page_ui.click_element('xpath', '//button[text()="OK"]')
#     time.sleep(2)
#     fw_page_ui.click_element('xpath', '(//button[text()="Close"])[2]')
#

# def check_Restart_button_after_import_IDP_xml():
#     init_test_page()
#     idp_config_button = ['xpath', '(//button[text()="Configure"])[6]']
#     logger.info('Click saml idp Configure button')
#     fw_page_ui.click_element(*idp_config_button)
#     # idp_check = ['xpath', "//div[text()='idp_test']"]
#     fw_page_ui.click_element(*['xpath', '//span[text()="Import from File"]'])
#     fw_page_ui.set_input_text_field(*['xpath', '//input[@name="name"]'], 'cyuan')
#     logger.info('====>click upload button')
#     fw_page_ui.click_element(*['xpath', "//*[text()='Add File']"])
#     time.sleep(2)
#     pyautogui.write(r'/tmp/sonicauto.xml')
#     pyautogui.press('enter')
#     time.sleep(2)
#     fw_page_ui.click_element(*['xpath', '//button[text()="Next"]'])
#
#     return fw_page_ui.click_element(*['xpath', '//button[text()="Restart"]'])


def export_saml_sp():
    os.system('rm -rf /root/Downloads')
    sp_configure_button = ['xpath', '(//button[text()="Configure"])[5]']
    logger.info('Click saml sp Configure button')
    fw_page_ui.click_element(*sp_configure_button)
    export_button = ['xpath', '//span[contains(@class, "icon-export")]']
    logger.info('Click saml sp export button')
    fw_page_ui.click_element(*export_button)
    text_win = ['xpath', '//input[@name="name"]']
    logger.info('input text test01')
    fw_page_ui.set_input_text_field(*text_win, 'test01')
    export2_button = ['xpath', '//button[text()="Export"]']
    logger.info('Export sp xml file')
    fw_page_ui.click_element(*export2_button)
    logger.info('Export clicked')
    logger.info('check if sp file downloaded.....')
    time.sleep(10)
    return os.path.exists('/root/Downloads/sp_test.xml')


def check_idp_on_GUI():
    idp_config_button = ['xpath', '(//button[text()="Configure"])[6]']
    logger.info('Click saml idp Configure button')
    fw_page_ui.click_element(*idp_config_button)
    idp_check = ['xpath', "//div[text()='idp_test']"]
    return fw_page_ui.does_element_exist(*idp_check)
