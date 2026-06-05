from definition.settings import *


class FWUI(FWPage):
    def __init__(self):
        super().__init__('192.168.168.168', 'admin', Params.G_NEW_PASSWORD)

    def verify_user_status_page(self, ip, user, timeout=0, expected_failure=False):
        try:
            time.sleep(timeout)
            self.get_browser()
            self.go_to_url(f"https://192.168.168.168")
            logger.info("Configure - Setting username")
            time.sleep(10)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', "admin")
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', Params.G_NEW_PASSWORD)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(10)
            if self.does_element_exist_now('xpath', "//button[@class='sw-button sw-button--light' and text()='Config']"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--light')]")
                logger.info("Action - Clicked Config")
                time.sleep(20)

            if self.does_element_exist_now('xpath', "//button[normalize-space()='Cancel']"):
                self.click_element('xpath', "//button[normalize-space()='Cancel']")
                logger.info("Clicked on Cancel")
            time.sleep(5)
            self.navigate_to_local_users_section()
            self.navigate_to_section("icon-user", "Status", labelName="Users")
            elements = self.get_element('class', 'sw-table-body__cont-native')
            time.sleep(5)
            logger.info(f"Sessions: {str(elements.text)}")
            if expected_failure:
                Assertion.assert_not_regular(str(elements.text), user, "ERR: username is present.")
                Assertion.assert_not_regular(str(elements.text), ip, "ERR: ip is present.")
            else:
                Assertion.assert_regular(str(elements.text), user, "ERR: username is wrong.")
                Assertion.assert_regular(str(elements.text), ip, "ERR: ip is wrong.")
            self.logout_ui()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Varifying user status from status page failed.")
    
    def user_logout_by_admin(self, user, timeout=0):
        try:
            time.sleep(timeout)
            self.get_browser()
            self.go_to_url(f"https://192.168.168.168")
            time.sleep(10)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', "admin")
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', Params.G_NEW_PASSWORD)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(10)
            if self.does_element_exist_now('xpath', "//button[@class='sw-button sw-button--light' and text()='Config']"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--light')]")
                logger.info("Action - Clicked Config")
                time.sleep(20)
            else:
                logger.info("Not found")

            if self.does_element_exist_now('xpath', "//button[normalize-space()='Cancel']"):
                self.click_element('xpath', "//button[normalize-space()='Cancel']")
                logger.info("Clicked on Cancel")

            time.sleep(5)
            self.navigate_to_local_users_section()
            self.navigate_to_section("icon-user", "Status", labelName="Users")
            time.sleep(5)
            logger.info('navigated to status page')
            self.click_element('xpath', "//div[contains(@class, 'sw-checkbox__box sw-flexbox__flex-none sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify')]")
            logger.info("Action - Checked all user checkbox")
            self.click_element('xpath', "//span[@class='sw-icon-button__label-cont sw-flexbox__flex-none' and text()='Logout']")
            logger.info("Action - Clicked Logout")
            time.sleep(5)
            self.click_element('xpath', "//button[@class='sw-button sw-button--light sw-button--default' and text()='Confirm']")
            logger.info("Action - Clicked Confirm")
            time.sleep(5)
            Assertion.assert_equal(self.does_page_have_text(user), False, "ERR: Failed to logout user from Status Page.")
            self.logout_ui()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Logging out user from status page failed.")
        
    def fw_config(self, url, user):
        try:
            time.sleep(30)
            self.get_browser()
            self.go_to_url(url)
            logger.info("Logging in")
            logger.debug("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.debug("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            if self.does_element_exist_now('xpath', "//button[@class='sw-button sw-button--light' and text()='Config']"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--light')]")
                logger.info("Action - Clicked config")
                time.sleep(20)
            # self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(10)
            # navigate to local users and add user
            self.navigate_to_local_users_section()
            time.sleep(5)
            elements = self.get_element('class', 'sw-table-body__cont-native')
            logger.info(f"Sessions: {str(elements.text)}")
            self.click_element('xpath', "//span[contains(@class, 'sw-icon__inner sw-font-icon icon-add')]")
            logger.info("Action - Clicked on Add")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", user)
            logger.info("Action - Entered username")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", 'S0nic@uto')
            logger.info("Action - Entered password")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", 'S0nic@uto')
            logger.info("Action - Entered confirm password")
            time.sleep(5)
            self.click_element('xpath', "//button[text()='Save']")
            logger.info("Action - Clicked on save")
            
            time.sleep(10)
            resp = self.does_page_have_text(user)
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")
            self.logout_ui()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to do fw configuration")

    def disable_automatic_updates_prompt(self):
        try:
            self.get_browser()
            self.go_to_url(f"https://192.168.168.168")
            logger.info("Configure - Setting username")
            time.sleep(10)
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', "admin")
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', Params.G_NEW_PASSWORD)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(20)
            if self.does_element_exist_now('xpath', "//button[@class='sw-button sw-button--light' and text()='Config']"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--light')]")
                logger.info("Action - Clicked Config")
                time.sleep(20)
            self.click_element('xpath', "//div[contains(@class, 'sw-checkbox__box sw-flexbox__flex-none sw-flexbox sw-flexbox--center-items sw-flexbox--center-justify')]")
            logger.info("Action - Checked Do not show this message again.")
            time.sleep(2)
            self.click_element('xpath', "//button[text()='OK']")
            logger.info("Clicked on OK")
            time.sleep(5)
            self.logout_ui()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Disabling Automatic Firmware Updates Prompt.")