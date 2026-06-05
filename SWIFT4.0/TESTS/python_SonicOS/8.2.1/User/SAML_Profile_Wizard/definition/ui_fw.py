from definition.settings import *
# import pyautogui


def init_test_page(refresh=0):
    base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
    url = base_url + 'users/users-settings'
    fw_page_ui.login_ui_with_head(browser_type='chrome', headless=True)
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i + 1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()
    
    wizard_xpath = '(//span[contains(@class, "icon-wizard")])[2]'
    logger.info('click wizard element...')
    fw_page_ui.click_element('xpath', wizard_xpath)
    
    
def configure_wizard_profile_part(profile_name):
    logger.info('configure profile part'.center(40, '='))
    time.sleep(3)
    logger.info('fill in profile_name')
    profile_name_xpath = '//input[@name="profile-name"]'
    fw_page_ui.set_input_text_field(*['xpath', profile_name_xpath], profile_name) 
    logger.info('fill in comment')
    time.sleep(3)
    comment_xpath = '//input[@name="comment"]' 
    fw_page_ui.set_input_text_field(*['xpath', comment_xpath], 'add saml profile via wizard')      
    logger.info('click next button')
    fw_page_ui.click_element('xpath', next_button_xpath)

def configure_wizard_sp_from_exists(sp_name):
    logger.info('configure sp part'.center(40, '='))
    logger.info('click select_down')
    select_down_xpath = '(//div[contains(@class, "sw-select__icon")])[4]'
    fw_page_ui.click_element('xpath', select_down_xpath)
    logger.info('click creat profile from select drop down list...')
    sp_xpath = f'//span[text()="{sp_name}"]'
    fw_page_ui.click_element('xpath', sp_xpath)
    logger.info('click Next...')
    fw_page_ui.click_element('xpath', next_button_xpath)
    
def configure_wizard_sp_part(sp_name):
    logger.info('configure sp part'.center(40, '='))
    logger.info('click select_down')
    select_down_xpath = '(//div[contains(@class, "sw-select__icon")])[4]'
    fw_page_ui.click_element('xpath', select_down_xpath)
    logger.info('click creat profile from select drop down list...')
    create_profile_button_xpath = '//span[text()="--Create New Service Provider--"]'
    fw_page_ui.click_element('xpath', create_profile_button_xpath)
      
    logger.info('fill in sp name')
    time.sleep(3)
    sp_name_xpath = '//input[@name="sp-name"]'
    fw_page_ui.set_input_text_field(*['xpath', sp_name_xpath], sp_name) 
    sp_type_xpath = '//span[text()="IP"]'
    logger.info('sp type IP or Domain, select Domain...')
    fw_page_ui.click_element('xpath', sp_type_xpath) 
    domain_type_xpath = '//span[text()="Domain"]'
    fw_page_ui.click_element('xpath', domain_type_xpath)
    domain_name_xpath = '//input[@name="sp-domain-name"]'
    fw_page_ui.set_input_text_field(*['xpath', domain_name_xpath], 'example.com')
    logger.info('select Service type as SSLVPN...')
    select_service_type_xpath = '(//div[contains(@class, "sw-select__icon")])[6]'
    fw_page_ui.click_element('xpath', select_service_type_xpath)
    sslvpn_xpath = '//span[text()="SSL VPN (4433)"]'
    fw_page_ui.click_element('xpath', sslvpn_xpath)
    logger.info('click Next...')
    fw_page_ui.click_element('xpath', next_button_xpath)
    
    
def export_sp_part():
    logger.info('export sp part'.center(40, '='))
    logger.info('click export...')
    export_xpath = '//*[text()="Export"]'
    fw_page_ui.click_element('xpath', export_xpath)
    time.sleep(3)
    logger.info('Then click Next...')
    fw_page_ui.click_element('xpath', next_button_xpath)

def configure_wizard_idp_from_exists(idp_name='idp_azure'):
    logger.info('configure idp part'.center(40, '='))
    logger.info('click idp select down...')
    select_idp_xpath = '(//div[contains(@class, "sw-select__icon")])[4]'
    fw_page_ui.click_element('xpath', select_idp_xpath)
    logger.info('slect idp_azure from drop-down list')
    idP_xpath = f'//span[text()="{idp_name}"]'
    fw_page_ui.click_element('xpath', idP_xpath)
    logger.info('click Next...')
    fw_page_ui.click_element('xpath', next_button_xpath)

def configure_wizard_idp_part(idp_name):
    logger.info('configure idp part'.center(40, '='))
    time.sleep(3)
    logger.info('click idp select down...')
    select_idp_xpath = '(//div[contains(@class, "sw-select__icon")])[4]'
    fw_page_ui.click_element('xpath', select_idp_xpath)
    logger.info('select Create New IDP from drop-down list')
    creat_new_idp_xpath = '//span[text()="--Create New Identity Provider--"]'
    fw_page_ui.click_element('xpath', creat_new_idp_xpath)
        
    logger.info('choose manually configure the IDP')
    manual_button_xpath = '(//input[@name="idp-manual"]/following-sibling::span)[1]'
    fw_page_ui.click_element('xpath', manual_button_xpath)
        
    logger.info('manual configure idp part'.center(40, '='))
    idp_name_xpath = '//input[@name="idp-name"]'
    idp_server_id_xpath = '//input[@name="idp-serverId"]'
    auth_service_url_xpath = '//input[@name="idp-authServiceUrl"]'
    logout_service_url_xpath = '//input[@name="idp-logoutServiceUrl"]'
    user_name_xpath = '//input[@name="idp-userName"]'
    group_name_xpath = '//input[@name="idp-groupName"]'
    cert_select_down_xpath = '//div[contains(@class, "sw-select__label-cont") and .//span[text()="--Select Certificate--"]]/following-sibling::div'
        
    logger.info('fill in idp name...')
    fw_page_ui.set_input_text_field(*['xpath', idp_name_xpath], idp_name)
    logger.info('fill in idp server id...')
    fw_page_ui.set_input_text_field(*['xpath', idp_server_id_xpath], 'https://idp_server_id_wizard.com')
    logger.info('fill in auth service url...')
    fw_page_ui.set_input_text_field(*['xpath', auth_service_url_xpath], 'https://idp.example.com/auth')
    logger.info('fill in logout service url...')
    fw_page_ui.set_input_text_field(*['xpath', logout_service_url_xpath], 'https://idp.example.com/logout')
    logger.info('fill in user name...')
    fw_page_ui.set_input_text_field(*['xpath', user_name_xpath], 'user_name_wizard')
    logger.info('fill in group name...')
    fw_page_ui.set_input_text_field(*['xpath', group_name_xpath], 'group_name_wizard')
    fw_page_ui.click_element('xpath', cert_select_down_xpath)
    cert_xpath = '//span[contains(text(), "Microsoft Azure")]'
    logger.info('select cert as Microsoft Azure...')
    fw_page_ui.click_element('xpath', cert_xpath)
    logger.info('click Next...')
    fw_page_ui.click_element('xpath', next_button_xpath)
    

def configure_wizard_address_and_acs_part():
    logger.info('configure Address and ACS part'.center(40, '='))
    logger.info('click Next Button...')
    time.sleep(10)
    exist_rc = fw_page_ui.does_element_exist_now('xpath', next_button_xpath)
    logger.info(f'check Next button exists result: {exist_rc}')
    if exist_rc:
        time.sleep(3)
        fw_page_ui.click_element('xpath', next_button_xpath)
    else:
        raise Exception("Element not found")

def apply_wizard_configuration_and_close():
    logger.info('apply configuration'.center(40, '='))
    logger.info('click Apply...')
    time.sleep(10) 
    fw_page_ui.click_element('xpath', apply_xpath)
    logger.info('wait 5s to close...')
    fw_page_ui.click_element('xpath', close_xpath)
    fw_page_ui.quit()
