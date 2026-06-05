import re
import sys
import argparse
import sys
import time

sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')
# sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
print(sys.path)
from runner.settings import logger
from modules.ui.ui_wrapper import Browser
# from modules.ui.ui_wrapper_test import Browser
from runner.utils.assertion import Assertion

class FWPage(Browser):

    def __init__(self, url, user, pwd):
        self.url = url
        self.user = user
        self.password = pwd

    def login_ui(self):
        try:
            logger.info("Opening the Firefox Browser")
            self.get_browser()
            logger.info("Browser Successfully Invoked")
            self.go_to_url(self.url)
            logger.info("Logging in")
            logger.info("Configure - Setting username")
            self.set_input_text_field('xpath', '//input[@name="username"]', self.user)
            logger.info("Configure - Setting password")
            self.set_input_text_field('xpath', '//input[@name="password"]', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info("Login Test Flag.")
            return True, "Logged in Success"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            logger.info("Firewall login failed")
            return False, str(err)
        
        
    def close_browser(self):
        self.browser.close()


    def verify_configure_sso_ldap_user_group_button(self,option):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Users']")
            if option == "Local Configuration":
                self.click_element("xpath", "//label[@class='sw-radio sw-radio--light sw-flexbox sw-flexbox--inline sw-flexbox--center-items sso-users__auto-logn-usr-grp-method-1']//span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none']")
                logger.info("Chosen Local Configuration")
            if option == "LDAP":
                self.click_element("xpath", "//label[@class='sw-radio sw-radio--light sw-flexbox sw-flexbox--inline sw-flexbox--center-items sso-users__auto-logn-usr-grp-method-0']//span[@class='sw-radio__fake-radio-button sw-flexbox__flex-none']")
                logger.info("Chosen LDAP Configuration")

            self.click_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-settings']")
            if self.does_element_exist_now('xpath', "//span[normalize-space()='Referrals']"):
                self.close_browser()
                return True, "Configure Button is not dimmed"
            else:
                self.close_browser()
                return False, "Configure Button is dimmed out"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_updating_polling_rate_minutes_value(self, value):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[@class='sw-tab__inner__piece sw-flexbox__flex sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify'][normalize-space()='Users']")
            logger.info("Entering Polling Rate Value")
            self.set_input_text_field('xpath', "//input[@name='cia-auth-poll-period']", value)
            if self.does_element_exist_now('xpath', "//p[@class='sw-status-info__text__message__para']"):
                return False, "Invalid Input"
            self.click_element('xpath', "//button[normalize-space()='Save']")
            if self.does_element_exist_now('xpath', "//div[@class='sw-status-info__text__title sw-flexbox sw-flexbox--center-items']"):
                self.close_browser()
                return False, "Invalid Input"
            else:
                self.close_browser()
                return True, "Polling Rate Value Updated"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_updating_windows_service_agent(self, user, options=None):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//span[normalize-space()='General Settings']")
            logger.info("Adding the Window Service USER Agent")
            self.click_element("xpath", "//span[@class='sw-icon__inner sw-font-icon icon-add']")
            self.set_input_text_field('xpath', "//input[@name='enter-name']", user)    
            self.click_element('xpath', "//button[normalize-space()='Save']")
            logger.info("Checking if the user is created or not")
            if self.does_element_exist_now('xpath', f"//div[contains(text(),'{user}')]"):
                if options != None:
                    if self.does_element_exist_now('xpath', "//span[@class='sw-icon__inner sw-font-icon icon-add']"):
                        if not self.does_element_exist_now('xpath', "//span[@name='__delete-all']//span[@class='sw-icon__inner sw-font-icon icon-trash']"):
                            self.close_browser()
                            return False, "Options are not present"
                        self.close_browser()
                        return True, "Window Service User and Options are Present"                     
                self.close_browser()
                return True, "Windows Service User is Present"

        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_editing_windows_service_agent(self, user, new_user):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[normalize-space()='General Settings']")
            logger.info("Editing existing Window Service USER Agent")
            self.move_to_the_element("xpath", f"//div[contains(text(),'{user}')]")      
            self.click_element("xpath", "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-pencil']")      
            logger.info("Entering the new name")
            self.set_input_text_field('xpath', "//input[@name='enter-name']", new_user)       
            self.click_element('xpath', "//button[normalize-space()='Save']")
            logger.info("Checking if the user is edited or not")
            if self.does_element_exist_now('xpath', f"//div[contains(text(),'{new_user}')]"):
                self.close_browser()
                return True, "Edited Window Service User"                     
            self.close_browser()
            return False, "Failed to Edit Windows Service User"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_deleting_windows_service_user(self, user):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[normalize-space()='General Settings']")
            logger.info("Deleting Window Service USER Agent")
            self.move_to_the_element("xpath", f"//div[contains(text(),'{user}')]")      
            self.click_element("xpath", "//div[@class='sw-table-row-float-actions sw-flexbox sw-flexbox--center-items']//span[@class='sw-icon__inner sw-font-icon icon-trash']")      
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            logger.info("Checking if the user is deleted or not")
            if not self.does_element_exist_now('xpath', f"//div[contains(text(),'{user}')]"):
                self.close_browser()
                return True, "Deleted Window Service User"                     
            self.close_browser()
            return False, "Failed to Delete Windows Service User"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_windows_service_user(self, user):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[normalize-space()='General Settings']")
            logger.info("Verifying Window Service USER Agent")
            if self.does_element_exist_now('xpath', f"//div[contains(text(),'{user}')]"):
                self.close_browser()
                return True, "Verified Window Service User"                     
            self.close_browser()
            return False, "Failed to Verify Windows Service User"
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))


    def verify_deleting_all_windows_service_user(self):
        try:
            login_res = self.login_ui()
            if not login_res[0]:
                return False, login_res[1]
            
            time.sleep(40)
            if self.browser.find_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]'):
                    logger.info("Popup detected close it")  
                    self.click_element('xpath', '(//span[@class="sw-icon__inner sw-font-icon icon-close-thin"])[2]') 
            else: 
                 logger.info("No popup detected")
            time.sleep(5)
            logger.info("Clicking on DEVICE Tab")
            self.click_element("xpath", "//span[normalize-space()='Device']")
            logger.info("Clicking on Users Tab")
            self.click_element("xpath", "//span[normalize-space()='Users']")
            logger.info("Clicking on Intrusion Prevention Tab")
            self.click_element("xpath", "//li[@class='sw-nav-group sw-nav-group--dark sw-nav-group--compact']//span[contains(text(),'Settings')]")
            logger.info("Clicking on Configure SSO")
            self.click_element("xpath", "//button[@class='sw-button sw-button--light users-settings-auth__configure-sso']")
            self.click_element("xpath", "//span[normalize-space()='General Settings']")
            logger.info("Selecting All Window Service USER Agent")
            self.click_element("xpath", "//span[contains(@class,'sw-table-header')]//div[@class='sw-flexbox sw-flexbox--center-items']")      
            self.click_element('xpath', "//span[@name='__delete-all']//span[@class='sw-icon__inner sw-font-icon icon-trash']")
            logger.info("Deleting All Window Service USER Agent")
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default']")
            self.click_element('xpath', "//button[normalize-space()='Save']")
            logger.info("Successfully Deleted All Windows Service User")
            self.close_browser()
            return True, "Deleted Window Service User"                     
        
        except Exception as err:
            logger.info("Exception \t: " + str(err))
            