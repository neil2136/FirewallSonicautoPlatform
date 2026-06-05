from modules.UI7.common_require import *
class Administration:

    # def login_ui(self):
    #     try:
    #         self.ui_wrapper.get_browser()
    #         self.ui_wrapper.go_to_url(self.common.URL)
    #         logger.info("Logging in")
    #         if self.ui_wrapper.does_element_exist_now('xpath', '//div[text()="Manage using SonicWall Cloud"]'):
    #             logger.debug("Configure - Setting username")
    #             self.ui_wrapper.set_text_field('class', 'sw-textfield__wrapper__input', self.common.FW_USERNAME)
    #             logger.debug("Configure - Setting password")
    #             self.ui_wrapper.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.common.FW_PASSWORD)
    #         else:
    #             logger.debug("Configure - Setting username")
    #             # self.ui_wrapper.set_text_field('class', 'sw-email-input__input', self.common.FW_USERNAME)
    #             self.ui_wrapper.set_text_field('xpath', "//input[@type='text' and @name='emailInput']", self.common.FW_USERNAME)
    #             logger.debug("Configure - Setting password")
    #             self.ui_wrapper.set_text_field('xpath', "//input[@type='password' and @name='emailInput']", self.common.FW_PASSWORD)
    #             # logger.debug("Configure - Setting password")
    #             # self.ui_wrapper.set_text_field('class', 'sw-pw-input__input', self.common.FW_PASSWORD)
    #         logger.debug("Action - Clicked Login")
    #         self.ui_wrapper.wait_for_element_to_be_visible('class', 'sw-login__trigger')
    #         self.ui_wrapper.click_element('class', 'sw-login__trigger')
    #         time.sleep(1)
    #         alert = self.ui_wrapper.browser.switch_to.alert
    #         if alert:
    #             alert.dismiss()
    #         #time.sleep(1)
    #         time.sleep(3)
    #         if self.ui_wrapper.does_element_exist_now('xpath', '//div[text()="To manually configure SonicWall, "]'):
    #             self.ui_wrapper.click_element('xpath', '//div[text()="To manually configure SonicWall, "]/a[text()="click here."]')
    #         if self.ui_wrapper.does_element_exist_now('xpath', "//p[text()='No matching command found.']"):
    #             self.ui_helper.accept_alert()
    #         if self.ui_wrapper.does_element_exist_now('xpath', "//p[text()='Failed to open search db with error code [undefined]']"):
    #             self.ui_helper.accept_alert()
    #         if self.ui_wrapper.does_page_have_text("NETWORK SECURITY VIRTUAL"):
    #             logger.info("Logged in successfully")
    #     except Exception as err:
    #         logger.error("Exception \t: " + str(err))
    #         Assertion.fail("Firewall login failed")

    def login_ui(self):
        try:
            retries = 0
            while retries < 2:
                try:
                    self.ui_wrapper.get_browser()
                    logger.info("opened browser")
                    self.ui_wrapper.go_to_url(self.common.URL)
                    logger.info("opened URL success")
                    logger.info("Logging in")
                    logger.debug("Configure - Setting username")
                    self.ui_wrapper.set_text_field('xpath', "//input[@type='text' and @name='emailInput']", self.common.FW_USERNAME)
                    logger.debug("Configure - Setting password")
                    self.ui_wrapper.set_text_field('xpath', "//input[@type='password' and @name='emailInput']", self.common.FW_PASSWORD)
                    logger.debug("Action - Clicked Login")
                    self.ui_wrapper.click_element('class', 'sw-login__trigger')
                    time.sleep(40)
                    if self.ui_wrapper.did_page_load_successfully():
                        time.sleep(3)
                        current_url = self.ui_wrapper.browser.current_url
                        logger.debug("Current URL : " + str(current_url))
                        while not 'dashboard' in current_url:
                            current_url = self.ui_wrapper.browser.current_url
                            if "nsm-warning" in current_url:
                                logger.debug("Handling NSM warning")
                                self.get_element('xpath',
                                                 "//div[contains(@class, 'sw-action-bar-item')]/button[contains(text(), 'Proceed')]",
                                                 visible=False).click()
                                logger.debug("Handled NSM warning")
                            if "launchWizard" in current_url:
                                logger.debug("Handling Launch Wizard")
                                self.click_element('xpath', "//div[contains(text(), 'To manually configure SonicWall')]/a")
                                logger.debug("Handled Launch Wizard")
                            if "preempt" in current_url:
                                logger.debug("Handling Config Preempt")
                                self.click_element('xpath', "//button[contains(text(), 'Config')]")
                                logger.debug("Handled Config Preempt")
                            time.sleep(2)
                            current_url = self.ui_wrapper.browser.current_url
                            logger.debug("Current URL : "+ str(current_url))
                    # self.ui_wrapper.check_and_accept_multiple_alerts()                                  
                    # self.ui_wrapper.configure_toggle_button("Configuration", True, label=False)          
                    # self.ui_wrapper.check_and_accept_multiple_alerts()                                    
                    return True
                except Exception as err:
                    logger.error("Exception : " + str(err))
                    retries = retries + 1
                    if retries < 2:
                        self.ui_wrapper.close_browser()
                        continue
                    else:
                        logger.info("Exception \t: " + str(err))
                        Assertion.fail("Action - Unable to Login")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall login failed")

    def logout_ui(self):
        try:
            self.ui_wrapper.switchToWindow("Firewall Management")
            logger.info("Logging out")
            logger.debug("Action - Clicked drop down")
            self.navigation.navigate_to_home_page()
            time.sleep(1)
            self.ui_wrapper.click_element('class','sw-avatar__initials')
            logger.debug("Action - Clicked logout")
            self.ui_wrapper.click_element('xpath','//div/span[contains(text(),"Log Out")]')
            logger.debug("Action - Confirmed logout")
            self.ui_wrapper.click_element('xpath', '//div/button[contains(text(),"Continue")]')
            if self.ui_wrapper.does_element_exist('class', 'fw-mgmt-ftr-logout-confirmation__underline-text'):
                logger.info("Logged out")
            self.ui_wrapper.close_browser()
            self.ui_wrapper.quit()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.ui_wrapper.close_browser()
            self.ui_wrapper.quit()
            Assertion.fail("Firewall logout failed")

    def restart_firewall_ui(self):
        try:
            logger.info("Restarting Firewall")
            self.navigation.navigate_to_device_restart()
            self.ui_helper.click_button("Restart")
            self.ui_helper.accept_alert()
            self.ui_helper.accept_alert()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            
