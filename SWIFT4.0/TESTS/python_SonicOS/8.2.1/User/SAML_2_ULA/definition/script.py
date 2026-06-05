import os
import sys
import time

from runner.settings import logger

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_2_ULA'
sys.path.append(suite_path)
from modules.ui.fw_page import FWPage
from runner.settings import Params


fw_page_ui = FWPage(password=Params.G_NEW_PASSWORD)

def fill_in_user_info_part(user):
    logger.info(f'-> User Login Page Load SUCCESS...')
    logger.info('-> Enter User...')
    fw_page_ui.set_text_field('xpath', '//input[@type="email"]', user)
    logger.info('-> Enter User Done...')
    time.sleep(3)
    logger.info('-> Click Next button...')
    fw_page_ui.click_element('xpath', '//input[@type="submit"]')
    logger.info('-> Click Next button Done...')
    time.sleep(3)
    if fw_page_ui.does_element_exist('xpath', '//div[text()="Enter password"]'):
        logger.info('-> Password text field pops out! Enter the password...')
        fw_page_ui.set_text_field('xpath', '//input[@type="password"]', 'fxhWAN$246')
        time.sleep(3)
        logger.info('-> Password save DONE...')
        logger.info('-> fill in password Done! submit it')
        fw_page_ui.click_element('xpath', '//input[@type="submit"]')
        time.sleep(4)
        logger.info('-> Submit it Done!')
        if fw_page_ui.does_element_exist('xpath', '//*[text()="Stay signed in?"]'):
            logger.info('-> Stay signed in exist, not select it...')
            fw_page_ui.click_element('xpath', '//input[@id="idBtn_Back"]')
            logger.info('-> Stay signed in exist, not select it Done...')
            time.sleep(8)
            page_source = fw_page_ui.get_page_source()
            logger.info(page_source)
            rc = "you are now logged into the device" in page_source
            logger.info('-> SAML User Login SUCCESS...')
    return rc

def handle_login_page(user):
    """Handle the login page with retries."""
    MAX_RETRIES = 5
    SLEEP_TIME = 9
    
    for i in range(MAX_RETRIES):
        user_login_load = _safe_element_check('xpath', '//input[@type="email"]')
        if user_login_load:
            return fill_in_user_info_part(user)
        else:
            logger.info(f'-> User Login Page Load FAIL, Refresh The Page for the {i+1} time')
            time.sleep(SLEEP_TIME)
            fw_page_ui.refresh_browser()
    
    logger.error('-> Failed to load user login page after maximum retries')
    return False


def safe_element_check(attrib, attrib_val):
    """Safely check if an element exists without throwing assertion failures."""
    try:
        return fw_page_ui.does_element_exist(attrib, attrib_val)
    except:
        return False
 

def saml_user_ula_login(user='sonicauto@lusunshine1314163.onmicrosoft.com'):
    rc = False
    auth_page = False
    fw_page_ui.get_chrome_with_head(headless=True)
    fw_page_ui.go_to_url('https://12.12.1.169')
    time.sleep(1)
    
    # Check for user login page (email input field)
    fw_page_ui.switchToNewWindow()
    user_login_load = safe_element_check('xpath', '//input[@type="email"]')
    logger.info(f'-> Check User Login Page Load Result: {user_login_load}')
    
    if user_login_load:
        rc = fill_in_user_info_part(user)
        return rc
    else:
        fw_page_ui.switchToDefaultWindow()
    
        # Check for authentication required page
        auth_page = safe_element_check('xpath', '//*[contains(text(), "Authentication Required")]')
        logger.info(f'-> Check The Authentication Required Page Load Result: {auth_page}')
    if auth_page:
        logger.info('-> Click "Click here to log in"...')
        fw_page_ui.click_element('xpath', '//a[contains(text(), "Click here to log in")]')
        fw_page_ui.switchToNewWindow()
        time.sleep(10)
        rc = handle_login_page(user)
    else:
        logger.error('-> The Authentication Required Page Load Failed! Try Another Test...')
    time.sleep(10)
    return rc

def saml_user_logout():
    # logger.info('-> Switch to New Page to Logout...')
    # fw_page_ui.switchToNewWindow()
    fw_page_ui.click_element('xpath', "//*[contains(text(), 'Logout')]")
    logger.info('-> Click Logout Done...')
    logger.info('-> Switch the Default Window to Check User Logout if Success..')
    time.sleep(3)
    # fw_page_ui.switchToDefaultWindow()
    page_source = fw_page_ui.get_page_source()
    return "You signed out of your account" in page_source
    # if fw_page_ui.does_element_exist('xpath', '//div[contains(text(), "You have been logged out")]'):
    #     logger.info('-> SAML User Logout SUCCESS...')
    #     return True
    # logger.info('-> SAML User Logout FAILED ...')
    # return False


if __name__ == '__main__':
    login_rc = saml_user_ula_login()
    if login_rc:
        logger.info('saml user login from PC3 SUCCESS!!')
        # saml_user_logout()
