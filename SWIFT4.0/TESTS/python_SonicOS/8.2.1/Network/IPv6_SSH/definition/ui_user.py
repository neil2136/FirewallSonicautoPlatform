import argparse
import sys
import os
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from runner.settings import logger, Params
from runner.utils.assertion import Assertion
import time
from modules.ui.ui_wrapper import Browser


class FWPage(Browser):
    def __init__(self, url, user, pwd,browser_type):
        self.url = url
        self.user = user
        self.password = pwd
        self.browser_type = browser_type
        
    def login_ui(self):
        try:
            self.get_browser_2(browser_type = self.browser_type)
            logger.info('open url')
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info('time sleep 10s...')
            time.sleep(10)
            if not self.does_element_exist_now('class', 'sw-textfield__wrapper__input'):
                logger.info("Refresh browser ")
                self.refresh_browser()
            # time.sleep(5)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            logger.info("Login Test Flag.")
            time.sleep(15)
            # /html/body/div/div/div[7]/div/div[2]/div[1]/div/div
            self.move_to_the_element('xpath', '/html/body/div/div/div/div[7]/div/div/div[2]/div[1]/div/div/div[2]/div')
            logger.info('click connect...')
            self.click_element('xpath', '/html/body/div/div/div/div[7]/div/div/div[2]/div[1]/div/div/span/div/span[1]/span/span/span')
            logger.info("bookmark launched")
            logger.info("successfully logged in")
            time.sleep(5)
            logger.info(self.browser.current_url)
            logger.info('switch to new window....')
            cur_window = self.browser.current_window_handle
            logger.info(f'current window is {cur_window}')
            all_windows = self.browser.window_handles
            for handle in self.browser.window_handles:
                logger.info(handle)
            # self.browser.switch_to.window(all_windows[-1]) 
            self.browser.switch_to.window(all_windows[1]) 
            new_cur_window = self.browser.current_window_handle
            logger.info(f'current window is {new_cur_window}')
            return True
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False
        
    def connet_ssh_bookmark(self,user='root',password = 'password'):
        try:
            # time.sleep(5)
            logger.info(self.browser.current_url)
            for i in range(10):
                logger.info('time sleep 18s...')
                time.sleep(18+(i*5))
                logger.info(f'run {i+1} time...')

                if self.does_element_exist_now('class','sw-status-info--alert') or self.does_element_exist_now('xpath','/html/body/div[2]/div/div[2]/div/div/button'):
                    ###/html/body/div[2]/div/div[1]
                    logger.info('Warning pop-up!')
                    logger.info('exit warning....')
                    self.click_element('xpath', '/html/body/div[2]/div/div[2]/div/div/button')
                    logger.info('switch window')
                    all_windows = self.browser.window_handles
                    self.browser.switch_to.window(all_windows[0]) 
                    logger.info('move to element make connect visible....')
                    self.move_to_the_element('xpath', '/html/body/div/div/div/div[7]/div/div/div[2]/div[1]/div/div/div[2]/div')
                    logger.info('click connect...')
                    self.click_element('xpath', '/html/body/div/div/div/div[7]/div/div/div[2]/div[1]/div/div/span/div/span[1]/span/span/span')
                    logger.info("bookmark launched")
                    logger.info('switch window.....')
                    self.browser.switch_to.window(self.browser.window_handles[-1]) 
                    logger.info(self.browser.window_handles[-1])
                else:
                    logger.info('no warning pop-up, config username and password')
                    if self.does_element_exist_now('class','sw-textfield__wrapper__input') and self.does_element_exist_now('class','icon-checkmark'):
                        logger.info("Configure - Setting username part1")
                        self.set_text_field('class',  'sw-textfield__wrapper__input', user)
                        self.click_element('class', 'icon-checkmark')
                        logger.info("Configure - Setting password")
                        self.set_text_field('class',  'sw-textfield__wrapper__input', password)
                        self.click_element('class', 'icon-checkmark')
                        logger.info("successfully connect to sshv2 bookmark")
                        return True
                    elif self.does_element_exist_now('xpath','//*[@id="input"]') and self.does_element_exist_now('xpath','//*[@id="OK"]'):
                        logger.info("Configure - Setting username part 2")
                        self.set_text_field('xpath',  '//*[@id="input"]', user)
                        self.click_element('xpath', '//*[@id="OK"]')
                        logger.info("Configure - Setting password")
                        self.set_text_field('xpath',  '//*[@id="input"]', password)
                        self.click_element('xpath', '//*[@id="OK"]')
                        logger.info("successfully connect to sshv2 bookmark")
                        return True
                    else:
                        logger.error('The element not exist!!!')
            
            logger.info('try 10 times to connect ssh bookmark failed!!')
            return False
        except Exception as err:
            logger.info("Exception---- \t: " + str(err))
            logger.info("connect to sshv2 bookmark failed")
            return False
        
 
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Login group service by UI')
    parser.add_argument('-url', type=str, dest='url', required=False,default='https://[2001:db1::193]:4433', help='http server url')
    parser.add_argument('-user', type=str, dest='user', required=False,default='sslvpntest', help='user to login group service')
    parser.add_argument('-browser', type=str, dest='browser', required=False,default='firefox', help='the browser type')
    parser.add_argument('-pwd', type=str, dest='pwd', required=False,default=Params.G_NEW_PASSWORD,  help='pwd to login group service')
    parser.add_argument('-type', type=str, dest='type', required=False,default='connect_ssh_bookmark',  help='the bookmark type')
    args = parser.parse_args()
    os.environ["DISPLAY"] = ':1'
    os.system('pkill firefox')
    portal_ui = FWPage(url=args.url,user=args.user,pwd=args.pwd,browser_type=args.browser)
    print('---'*10)
    if args.type == 'connect_ssh_bookmark':
        rc = portal_ui.login_ui()
        rc &= portal_ui.connet_ssh_bookmark()
        logger.info(f'---{rc}---')
        Assertion.assert_equal(rc, True, "ERR: connect ssh bookmark failed")