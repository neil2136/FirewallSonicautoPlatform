from modules.UI7.common_require import *

sys.path.append(os.environ["PYTHON_COMMON_HOME"])


class DHCPObjects:
    def add_dhcp_object(self, dhcpObjectValue=None):
        try:
            self.navigation.navigate_to_dhcp_options_section()
            self.ui_helper.click_add_icon()

##            self.ui_wrapper.wait_for_text("Add DHCP Option Object")
##            self.ui_wrapper.wait_for_text("ADD DHCP OPTION OBJECT")

            self.ui_wrapper.wait_for_text("Option Object")
            self.configure_dhcp_object(dhcpObjectValue)
            self.ui_helper.wait_for_success_banner()
            self.ui_helper.click_refresh_icon()
            self.defined_dhcp_object(self.dhcpObjectName)
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Create DHCP object failed")	               


    def add_dhcp_object_ipv6(self):
        try:
            self.navigation.navigate_to_dhcp_options_ipv6_section()
            self.ui_helper.click_add_icon()

##            self.ui_wrapper.wait_for_text("Add DHCP Option Object")
##            self.ui_wrapper.wait_for_text("ADD DHCP OPTION OBJECT")

            self.ui_wrapper.wait_for_text("Option Object")
            self.configure_dhcp_object_ipv6()
            self.ui_helper.wait_for_success_banner()
            self.ui_helper.click_refresh_icon()
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Create DHCP object failed")	               


    def configure_dhcp_object(self, dhcpObjectValue=None):
        try:
            logger.info("Configure DHCP object name " + str(self.dhcpObjectName))
            logger.info("Configure DHCP object value " + str(dhcpObjectValue))

            self.ui_helper.configure_text_field('Option Name', self.dhcpObjectName)
            self.ui_helper.select_drop_down_value('Option Number', self.dhcpObjectNumber)	

#            self.ui_helper.configure_text_area('Option Value', dhcpObjectValue)
            self.ui_helper.add_text_list('Option Value', dhcpObjectValue)

#            self.browser.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .sw-form-row .sw-icon__inner").click()
#            self.browser.find_element(By.CSS_SELECTOR, "#sw-select__option-13863804111-5 > .sw-flexbox__flex").click()
#            self.browser.find_element(By.NAME, "Option Value").click()
#            self.browser.find_element(By.NAME, "Option Value").send_keys("9.7.1.0")

            self.ui_helper.submit_page()
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Configure DHCP object failed")


    def configure_dhcp_object_ipv6(self):
        try:
            logger.info("Configure DHCP object " + str(self.dhcpObjectName))

            self.ui_helper.configure_text_field('Option Name', self.dhcpObjectName)
            self.ui_helper.select_drop_down_value('Option Number', self.dhcpObjectNumber)	

#            self.ui_helper.configure_text_area('Option Value', self.dhcpObjectValue)
#            self.ui_helper.add_text_list('Option Value', self.dhcpObjectValue)

            self.browser.find_element(By.CSS_SELECTOR, "div:nth-child(2) > .sw-form-row .sw-icon__inner").click()
            self.browser.find_element(By.CSS_SELECTOR, "#sw-select__option-13863804111-5 > .sw-flexbox__flex").click()
            self.browser.find_element(By.NAME, "Option Value").click()
            self.browser.find_element(By.NAME, "Option Value").send_keys("::1")

            self.ui_helper.submit_page()
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Configure DHCP object failed")


    def edit_dhcp_object(self, dhcpObjectValue=None):
        try:
            logger.info("Edit DHCP object " + str(self.dhcpObjectName) + " from value " + str(self.dhcpObjectValue_0) + " to value " + str(dhcpObjectValue))

            self.navigation.navigate_to_dhcp_options_section()
            self.ui_wrapper.move_to_the_element('xpath', "//td/div/div/span[text()='" + self.dhcpObjectName_0 + "']")
            self.click_element('xpath', "//*[text()='" + self.dhcpObjectName_0 + "']/following::*[contains(@class,'icon-pencil')]")
            self.configure_dhcp_object(dhcpObjectValue)
            self.ui_helper.wait_for_success_banner()
            self.ui_helper.click_refresh_icon()
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Edit DHCP object failed")
            

    def delete_dhcp_object(self, dhcpObjectName=None):      
        try:
            logger.info("Delete DHCP object " + str(dhcpObjectName))

            self.navigation.navigate_to_dhcp_options_section()

            if self.defined_dhcp_object(dhcpObjectName):
                logger.info("DHCP object " + str(dhcpObjectName) + " is defined, deleting...")

                self.ui_helper.click_on_delete_element_after_hovering(dhcpObjectName)
                self.ui_helper.accept_alert()
                time.sleep(5)

#                self.ui_wrapper.move_to_the_element('xpath', "//td/div/div/span[text()='" + self.dhcpObjectName + "']")
#                self.click_element('xpath', "//*[text()='" + self.dhcpObjectName + "']/following::*[contains(@class,'icon-trash')]")

                self.ui_helper.accept_alert()
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Delete DHCP object failed")


    def defined_dhcp_object(self, dhcpObjectName=None):
        try:
            self.ui_helper.search_string(dhcpObjectName)
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[contains(@class, 'sw-table-row__cell__wrapper')]"
                                                               "/div/span[text()='"+dhcpObjectName+"']"):
                logger.info("DHCP object "+dhcpObjectName+" is defined")
                return True
            else:
                logger.info("DHCP object is not defined")
                return False
        except Exception as e:
            logger.error(str(e))
            Assertion.fail("Defined DHCP object failed")








