from definition.settings import *


def login_firewall(refresh=0):
    base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
    url = base_url + 'system/administrator'
    fw_page_ui.login_ui_with_head(headless=True, browser_type='chrome')
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i + 1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()


def https_access_SP_domain(browser_type='chrome'):
    if browser_type == 'chrome':
        fw_page_ui.get_chrome_with_head(headless=True)
    else:
        fw_page_ui.get_firefox_with_head(headless=True)
    fw_page_ui.go_to_url('https://shanghaiqa.com')
    fw_page_ui.wait_for_page_data_to_be_rendered()


def login_domain_type_Single_sign_on():
    logger.info('- Click Single Sign On Button...')
    fw_page_ui.click_element('xpath', '//*[text()="Single Sign On"]')
    logger.info('- Click Single Sign On Button SUCCESS...')
    fw_page_ui.get_browser_all_handles()
    time.sleep(3)
    fw_page_ui.switchToNewWindow()
    time.sleep(3)
    cur_url = fw_page_ui.get_current_browser_url()
    logger.info(f'current url is {cur_url}')
    if 'login.microsoftonline.com' in cur_url:
        logger.info('-> Click Single sign on SUCCESS')


def user_login_part(page_close=True):
    logger.info('-> Enter User...')
    fw_page_ui.set_text_field('xpath', '//input[@type="email"]', Parameter.USER)
    logger.info('-> Enter User Done...')
    time.sleep(1)
    logger.info('-> Click Next button...')
    fw_page_ui.click_element('xpath', '//input[@type="submit"]')
    logger.info('-> Click Next button Done...')
    time.sleep(1)
    if fw_page_ui.does_element_exist_now('xpath', '//div[text()="Enter password"]'):
        logger.info('-> Password text field pops out! Enter the password...')
        fw_page_ui.set_text_field('xpath', '//input[@type="password"]', Parameter.PASSWD)
        time.sleep(1)
        logger.info('-> Password save DONE...')
        logger.info('-> fill in password Done! submit it')
        fw_page_ui.click_element('xpath', '//input[@type="submit"]')
        time.sleep(1)
        logger.info('-> Submit it Done!')
        if fw_page_ui.does_element_exist_now('xpath', '//*[text()="Stay signed in?"]'):
            logger.info('-> Stay signed in exist, not select it...')
            fw_page_ui.click_element('xpath', '//input[@id="idBtn_Back"]')
            logger.info('-> Stay signed in exist, not select it Done...')

        # logger.info('User Login SUCCESS')
        return True
    logger.error('The password enter page pops out failed!!')
    return False


def manage_part():
    manage_rc = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Manage"]')
    logger.info(f'-> check Manage button if exists result: {manage_rc}')
    if not manage_rc:
        return False
    logger.info('-> Click Manage...')
    fw_page_ui.click_element('xpath', '//*[text()="Manage"]')
    time.sleep(20)
    logger.info('-> Switch to the Manage Page...')
    fw_page_ui.switchToDefaultWindow()
    url = fw_page_ui.get_current_browser_url()
    logger.info(f'The Current URL after Click Manage is: {url}')
    if 'dynUserLogin.html?fromSaml' in url:
        logger.error("-> Manage Firewall FAILED!! ")
        return False
    logger.info("-> Manage Firewall SUCCESS")
    return True


def manage_firewall_via_saml_user(browser_type='chrome'):
    rc = False
    https_access_SP_domain(browser_type)
    login_domain_type_Single_sign_on()
    for i in range(6):
        user_login_page = fw_page_ui.does_element_exist_now('xpath', '//input[@type="email"]')
        if user_login_page:
            user_login_rc = user_login_part()
            if user_login_rc:
                rc = manage_part()
                break
        else:
            refresh_saml_login_page(i)
    time.sleep(10)
    return rc


def get_session_time():
    logger.info('check the session time ...')
    obj_session = fw_page_ui.get_element('xpath',
                                         "//div[contains(text(), 'Remaining session time')]")
    session_time = obj_session.text
    logger.info(f'get the session time is: {session_time}')
    return int((re.search(r'' + '\d+', session_time)).group())


def refresh_saml_login_page(i, max=6):
    if i == max-1:
        logger.error("-> The User Login Page Load Failed after Max tries! Try another test")
    else:
        logger.error(f'-> The User Login Page Load failed after {i + 1} tries !!! Refresh this login page')
    time.sleep(9)
    fw_page_ui.refresh_browser()


def logout_saml_auth():
    for i in range(3):
        logger.info('-> Switch to New Page to Logout...')
        fw_page_ui.switchToNewWindow()
        # logger.info(f'-> Logout for the {i + 1} time...')
        fw_page_ui.click_element('xpath', "//a[contains(text(), 'Logout')]")
        time.sleep(5)
        logger.info('-> Switch the Default Window to Check User Logout if Success..')
        fw_page_ui.switchToDefaultWindow()
        # if fw_page_ui.does_element_exist_now('xpath', '//button[contains(text(), "Log Back In")]'):
        if fw_page_ui.does_element_exist_now('xpath', '//button[@type="button"]'):
            logger.info('Logout SUCCESS!!')
            return True
        # else:
        #     fw_page_ui.switchToNewWindow()
    else:
        logger.info('Logout FAILED!!')
        return False

def saml_user_relogin():
    logger.info('-> Switch to Default page to Click Back in...')
    fw_page_ui.switchToDefaultWindow()
    # fw_page_ui.click_element('xpath', '//button[contains(text(), "Log Back In")]')
    fw_page_ui.click_element('xpath', '//button[@type="button"]')
    logger.info('Log Back In DONE...')
    time.sleep(3)
    logger.info('- Click Single Sign On Button...')
    fw_page_ui.click_element('xpath', '//*[text()="Single Sign On"]')
    logger.info('- Click Single Sign On Button SUCCESS...')
    fw_page_ui.switchToNewWindow()

    if fw_page_ui.does_element_exist_now('xpath', '//*[text()="Manage"]'):
        logger.info('-> SAML User Re-login SUCCESS')
        return True
    else:
        logger.error('-> Manage Page Load Failed, Refresh the page...')
        for i in range(20):
            fw_page_ui.refresh_browser()
            if fw_page_ui.does_element_exist_now('xpath', '//*[text()="Manage"]'):
                logger.info('-> SAML User Re-login SUCCESS')
                return True
            time.sleep(10)
    return False