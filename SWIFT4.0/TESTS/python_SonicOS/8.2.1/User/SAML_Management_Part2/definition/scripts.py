import os
import sys
import time
from runner.settings import logger,Params
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_Management'
sys.path.append(suite_path)
from modules.ui.fw_page import FWPage

fw_page_ui = FWPage(password=Params.G_NEW_PASSWORD)


def https_access_SP_domain(url='https://shanghaiqa.com'):
    fw_page_ui.get_chrome_with_head(headless=True)
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()


def login_domain_type_Single_sign_on():
    logger.info('- Click Single Sign On Button...')
    fw_page_ui.click_element('xpath', '//*[text()="Single Sign On"]')
    logger.info('- Click Single Sign On Button SUCCESS...')
    fw_page_ui.get_browser_all_handles()
    time.sleep(3)
    fw_page_ui.switch_window()
    time.sleep(3)
    cur_url = fw_page_ui.get_current_browser_url()
    logger.info(f'current url is {cur_url}')
    if 'login.microsoftonline.com' in cur_url:
        logger.info('Single sign on SUCCESS')


def user_login_part():
    USER = 'sonicauto@lusunshine1314163.onmicrosoft.com'
    PASSWD = 'fxhWAN$246'
    logger.info('-> Enter User...')
    fw_page_ui.set_text_field('xpath', '//input[@type="email"]', USER)
    logger.info('-> Enter User Done...')
    logger.info('-> Click Next button...')
    fw_page_ui.click_element('xpath', '//input[@type="submit"]')
    logger.info('-> Click Next button Done...')
    logger.info('Wait for the PASSWD pops out')
    if fw_page_ui.does_element_exist_now('xpath', '//div[text()="Enter password"]'):
        logger.info('-> Password text field pops out! Enter the password...')
        fw_page_ui.set_text_field('xpath', '//input[@type="password"]', PASSWD)
        logger.info('-> fill in password Done! submit it')
        fw_page_ui.click_element('xpath', '//input[@type="submit"]')
        logger.info('-> Submit it Done!')
        if fw_page_ui.does_element_exist_now('xpath', '//*[text()="Stay signed in?"]'):
            logger.info('-> Stay signed in exist, not select it...')
            fw_page_ui.click_element('xpath', '//input[@id="idBtn_Back"]')
            logger.info('-> Stay signed in exist, not select it Done...')
        rc = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Manage"]')
        logger.info(f'-> check Manage button if exists result: {rc}')
        return rc
    logger.error('The password enter page pops out failed!!')
    return False


def manage_part():
    logger.info('-> Click Manage...')
    fw_page_ui.click_element('xpath', '//*[text()="Manage"]')
    time.sleep(10)
    fw_page_ui.switch_window()
    url = fw_page_ui.get_current_browser_url()
    logger.info(f'The Current URL after Click Manage is: {url}')
    # https://shanghaiqa.com/dynUserLogin.html?fromSaml=1
    if 'dynUserLogin.html?fromSaml' in url:
        logger.error("-> Manage Firewall FAILED!! ")
        return False
    logger.info("-> Manage Firewall SUCCESS")
    return True


def check_user_authentication(url='https://shanghaiqa.com'):
    rc = False
    https_access_SP_domain(url)
    login_domain_type_Single_sign_on()
    for i in range(6):
        user_login = fw_page_ui.does_element_exist_now('xpath', '//input[@type="email"]')
        if user_login:
            user_login_rc = user_login_part()
            if user_login_rc:
                rc = True
                time.sleep(3)
                break
        else:
            logger.error(f'User Login Page Load failed after {i + 1} tries!!! refresh this login page')
            time.sleep(10)
            fw_page_ui.refresh_browser()
    return rc


def logout_saml_user():
    # for i in range(3):
    #     logger.info('-> Switch to New Page to Logout...')
    #     # fw_page_ui.switchToNewWindow()
    #     fw_page_ui.click_element('xpath', "//a[contains(text(), 'Logout')]")
    #     time.sleep(5)
    #     logger.info('-> Switch the Default Window to Check User Logout if Success..')
    #     fw_page_ui.switchToDefaultWindow()
    #     # if fw_page_ui.does_element_exist_now('xpath', '//button[contains(text(), "Log Back In")]'):
    #     if fw_page_ui.does_element_exist_now('xpath', '//button[@type="button"]'):
    #         logger.info('Logout SUCCESS!!')
    #         return True
    # else:
    #     logger.info('Logout FAILED!!')
    #     return False
    
    fw_page_ui.click_element('xpath', "//*[contains(text(), 'Logout')]")
    logger.info('-> Click Logout Done...')
    logger.info('-> Switch the Default Window to Check User Logout if Success..')
    time.sleep(3)
    # fw_page_ui.switchToDefaultWindow()
    page_source = fw_page_ui.get_page_source()
    if "You signed out of your account" in page_source:
        logger.info('Logout SUCCESS!!')
        return True
    else:
        logger.info('Logout FAILED!!')
        return False
    # if fw_page_ui.does_element_exist('xpath', '//div[contains(text(), "You have been logged out")]'):
    #     logger.info('-> SAML User Logout SUCCESS...')
    #     return True
    # logger.info('-> SAML User Logout FAILED ...')
    # return False


if __name__ == '__main__':
    if sys.argv[1] == 'TC03':
        if check_user_authentication():
            logout_saml_user()
            time.sleep(10)
            fw_page_ui.quit()
    if sys.argv[1] == 'TC05':
        check_user_authentication(url='https://13.13.1.168')
        fw_page_ui.quit()
