import os
import sys
import time
from runner.settings import logger
# sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append('/DEV_TESTS/python_SonicOS')
# sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_Management_UI_Part'
sys.path.append(suite_path)
from modules.ui.fw_page import FWPage


fw_page_ui = FWPage(password='sonicauto')


def login_via_x2():
    try:
        fw_page_ui.get_browser()
        fw_page_ui.go_to_url("https://13.13.1.168")
        res = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Single Sign On"]')
        logger.info(f'check the Single Sign On button result: {res}')
        fw_page_ui.quit()
        sys.exit(0) if not res else sys.exit(1)
    except Exception as e:
        logger.error(repr(e))
        sys.exit(1)

def single_sign_on_from_x2():
    try:
        fw_page_ui.get_chrome_with_head(headless=True)
        fw_page_ui.go_to_url("https://13.13.1.168")
        fw_page_ui.save_screen_shot()
        logger.info('- Click Single Sign On Button')
        fw_page_ui.click_element('xpath', '//*[text()="Single Sign On"]')
        logger.info('- Click Single Sign On Button SUCCESS')
        all_windows = fw_page_ui.get_browser_all_handles()
        time.sleep(3)
        fw_page_ui.switch_window()
        time.sleep(3)
        cur_url = fw_page_ui.get_current_browser_url()
        logger.info(f'current url is {cur_url}')
        fw_page_ui.quit()
        sys.exit(0) if 'https://login.microsoftonline.com' in cur_url else sys.exit(1)
    except Exception as e:
        logger.error(repr(e))
        sys.exit(1)


if __name__ == '__main__':
    if sys.argv[1] == '0':
        login_via_x2()
    elif sys.argv[1] == '1':
        single_sign_on_from_x2()