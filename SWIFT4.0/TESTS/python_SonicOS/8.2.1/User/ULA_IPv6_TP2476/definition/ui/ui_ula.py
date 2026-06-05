from definition.settings import *


class UIULA(FWPage):

    def sslvpn_portal_login(self, url, user, password, timeout=30):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Configure - Setting username")
            time.sleep(10)
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(timeout)

            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("ULA login failed")

    def ula_login_ui(self, url, user, password, timeout=30):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Configure - Setting username")
            time.sleep(10)
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(10)
            Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), True, "ERR: Login failed.")
            self.click_element("xpath", "//button[text()='Continue']")
            logger.info("Action - Clicked Continue")
            time.sleep(timeout)

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("ULA login failed")
    
    def ula_manage_fw(self, url, user, password, timeout=5):
        try:
            self.ula_login_ui(url, user, password, timeout)
            all_handles = self.get_browser_all_handles()
            self.browser.switch_to.window(self.browser.window_handles[1])
            time.sleep(5)
            self.click_element('xpath', "/html/body/div/div/div/div/div[3]/div[3]/div[2]/button")
            logger.info("Action - Clicked Manage")
            time.sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(5)
            logger.info("window switched")
            if self.does_element_exist_now('xpath', "//button[contains(@class, 'sw-buttton sw-button--light')]"):
                self.click_element('xpath', "//button[contains(@class, 'sw-buttton sw-button--light')]")
                logger.info("Action - Clicked Config")
            elif self.does_element_exist_now('xpath', "//button[contains(@class, 'sw-button sw-button--dark')]"):
                self.click_element('xpath', "//button[contains(@class, 'sw-button sw-button--dark')]")
                logger.info("Action - Clicked Non-Config")
            time.sleep(10)

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("ULA login failed")
    
    def read_only_mode_ui(self, url, user, password):
        try:
            self.ula_manage_fw(url, user, password)
            
            # verify read only mode
            Assertion.assert_equal(self.does_page_have_text('Read-Only Mode'), True, "ERR: Failed to verify Read-Only Mode.")

            # navigate to local users and try to add any user
            self.navigate_to_local_users_section()
            time.sleep(10)
            elements = self.get_element('class', 'sw-table-body__cont-native')
            logger.info(f"Sessions: {str(elements.text)}")
            self.click_element('xpath', "//span[contains(@class, 'sw-icon__inner sw-font-icon icon-add')]")
            logger.info("Action - Clicked on Add")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", 'dummy_user')
            logger.info("Action - Entered username")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", 'Password@40')
            logger.info("Action - Entered password")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", 'Password@40')
            logger.info("Action - Entered confirm password")
            time.sleep(5)
            self.click_element('xpath', "//button[text()='Save']")
            logger.info("Action - Clicked on save")
            time.sleep(10)
            Assertion.assert_equal(self.does_page_have_text('Read-Only user does not have the privilege for config mode'), True, "ERR: Failed to verify Read-Only Mode warning.")
            
            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("login as read only failed")

    
    def limited_privilege_ui(self, url, user, password):
        try:
            self.get_browser()
            self.go_to_url(url)
            logger.info("Configure - Setting username")
            time.sleep(10)
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(10)
            self.click_element("xpath", "//button[text()='Continue']")
            logger.info("Action - Clicked Continue")
            time.sleep(5)
            all_handles = self.get_browser_all_handles()
            self.browser.switch_to.window(self.browser.window_handles[1])
            self.click_element('xpath', "/html/body/div/div/div/div/div[3]/div[3]/div[2]/button")
            logger.info("Action - Clicked Manage")
            time.sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(5)
            logger.info("window switched")
            time.sleep(10)
            
            # verifying Policy and Object tab should not be visible
            tabs = self.get_element('xpath', "//div[contains(@class, 'fw-app-header__head sw-flexbox sw-flexbox--center-items')]")
            Assertion.assert_not_regular(tabs.text, "OBJECT", 'ERR: Object tab is available')
            Assertion.assert_not_regular(tabs.text, "POLICY", 'ERR: Policy tab is available')

            self.navigate_to_users_guest_accounts()
            time.sleep(5)
            self.click_element('xpath', "//span[contains(@class, 'sw-icon__inner sw-font-icon icon-add')]")
            logger.info("Action - Clicked on Add")
            time.sleep(2)
            element = self.get_element('name', 'name')
            guest_name = element.get_attribute('value')
            
            logger.info(f"Guest Name: {guest_name}")
            self.set_text_field('name', "Password", 'Password@50')
            logger.info("Action - Entered password")
            time.sleep(5)
            self.set_text_field('name', "ConfirmPassword", 'Password@50')
            logger.info("Action - Entered confirm password")
            time.sleep(5)
            self.click_element('xpath', "//button[text()='Save']")
            logger.info("Action - Clicked on Save")
            time.sleep(5)

            Assertion.assert_equal(self.does_page_have_text(guest_name), True, "ERR: Failed to add guest account.")
            
            self.close_browser()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("login as limited privilege failed.")
    
    def full_admin_mode_ui(self, url, user, password):
        try:
            self.ula_manage_fw(url, user, password)
            # self.click_element('xpath', "//button[normalize-space()='Cancel']")
            time.sleep(5)
            # verifying Policy and Object tab should not be visible
            tabs = self.get_element('xpath', "//div[contains(@class, 'fw-app-header__head sw-flexbox sw-flexbox--center-items')]")
            Assertion.assert_regular(tabs.text, "HOME", 'ERR: HOME tab is available')
            Assertion.assert_regular(tabs.text, "MONITOR", 'ERR: MONITOR tab is available')
            Assertion.assert_regular(tabs.text, "DEVICE", 'ERR: DEVICE tab is available')
            Assertion.assert_regular(tabs.text, "NETWORK", 'ERR: NETWORK tab is available')
            Assertion.assert_regular(tabs.text, "OBJECT", 'ERR: OBJECT tab is available')
            Assertion.assert_regular(tabs.text, "POLICY", 'ERR: POLICY tab is available')

            # navigate to local users and add user
            self.navigate_to_local_users_section()
            time.sleep(5)
            users = self.get_element('class', 'sw-table-body__cont-native')
            logger.info(f"Sessions: {str(users.text)}")
            self.click_element('xpath', "//span[contains(@class, 'sw-icon__inner sw-font-icon icon-add')]")
            logger.info("Action - Clicked on Add")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter Name...']", 'dummy_user')
            logger.info("Action - Entered username")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Enter password...']", 'Password@60')
            logger.info("Action - Entered password")
            time.sleep(5)
            self.set_text_field('xpath', "//input[@placeholder='Confirm Password']", 'Password@60')
            logger.info("Action - Entered confirm password")
            time.sleep(5)
            self.click_element('xpath', "//button[text()='Save']")
            logger.info("Action - Clicked on save")
            time.sleep(10)
            resp = self.does_page_have_text('dummy_user')
            Assertion.assert_equal(resp, True, "ERR: Local user is not created")

            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("login as full admin privilege failed.")
    
    def lockout_user_ui(self, url, user, password, attempt=0):
        try:
            self.get_browser()
            self.go_to_url(url)
            for i in range(attempt):
                logger.info("Configure - Setting username")
                self.set_text_field('class', 'sw-textfield__wrapper__input', user)
                logger.info("Configure - Setting password")
                self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', "wrongpassword")
                self.click_element('class', 'sw-login__trigger')
                logger.info("Action - Clicked Login")
                time.sleep(10)

            # try to login
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', password)
            self.click_element('class', 'sw-login__trigger')
            logger.info("Action - Clicked Login")
            time.sleep(5)
            Assertion.assert_equal(self.does_page_have_text("You have logged in successfully!"), False, "ERR: Logged in.")
            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Lockout user ula failed.")
    
    def ula_user_fw_logout(self, url, user, pwd):
        try:
            self.ula_manage_fw(url, user, pwd, timeout=10)
            all_handles = self.get_browser_all_handles()
            self.browser.switch_to.window(self.browser.window_handles[1])
            time.sleep(5)
            self.click_element('xpath', '/html/body/div/div/div/div/div[3]/div[1]/div')
            logger.info("Action - Clicked Log out")
            time.sleep(5)
            self.browser.switch_to.window(self.browser.window_handles[0])
            logger.info("Switched Window")
            time.sleep(5)
            Assertion.assert_equal(self.does_page_have_text("You have been logged out."), True, "ERR: Failed to logout from fw")

            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Ula logout failed.")
    
    def verify_ula_user_logout_window(self, url, user, pwd, timeout=30):
        try:
            self.ula_manage_fw(url, user, pwd)
            all_handles = self.get_browser_all_handles()
            time.sleep(30)

            if self.does_element_exist_now('xpath', "//button[@class='sw-button sw-button--light' and text()='OK']"):
                self.click_element('xpath', "//button[@class='sw-button sw-button--light' and text()='OK']")
                logger.info("Action - Clicked on Ok")
            time.sleep(timeout - 30)
            self.refresh_browser()
            time.sleep(5)
            Assertion.assert_equal(self.does_page_have_text("You have been logged out."), True, "ERR: Failed to get logged out.")
            self.close_browser()

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Ula logout by admin failed.")



