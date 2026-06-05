#!/usr/bin/python
import os
import sys
import time
from definition.settings import Parameter, logger, Assertion

sys.path.append(os.environ["PYTHON_COMMON_HOME"] + '/modules/ui')
from ui_wrapper import Browser


class FWPage(Browser):
    def __init__(self, url, turl, user, pwd):
        self.url = url
        self.turl = turl
        self.user = user
        self.password = pwd

    # ==================================login ui=======================================
    def login_gui(self):
        try:
            self.get_browser()
            self.go_to_url(self.url)
            logger.info("start logging...")
            logger.info("Configure - Setting username")
            self.set_text_field('class', 'sw-textfield__wrapper__input', self.user)
            logger.info("Configure - Setting password")
            self.set_text_field('class', 'sw-textfield__wrapper__input--with-icon-suffix', self.password)
            logger.info("Action - Clicked Login")
            self.click_element('class', 'sw-login__trigger')
            time.sleep(10)
            logger.info(f"Login fw successful.")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            Assertion.fail("Firewall login failed")

    # ==========================go to DHCP Server->DHCP Server Lease Scope=============
    def navigate_to_dhcp_server_page(self):
        try:
            logger.info('go to dhcp server page')
            self.go_to_url(self.turl)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            Assertion.fail("Firewall login failed")

    def navigate_to_level1_tab_dhcp_server_lease_scopes(self):
        try:
            time.sleep(8)
            logger.info('click DHCP Server Lease Scopes')
            self.navigate_to_tab('DHCP Server Lease Scopes')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            Assertion.fail("Firewall login failed")

    def navigate_to_level2_tab_ipv6(self):
        try:
            logger.info('click IPv6 tab')
            self.navigate_to_level2_tab('IPv6')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            Assertion.fail("Firewall login failed")

    # =======================================================================================

    def configure_dhcpv6_dynamic_scope_with_invalid_name(self, **kwargs):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            logger.info('click Add Dynamic button')
            # self.click_element('xpath', '//span[contains(text(),"Add Dynamic")]')
            self.click_element('xpath', "//div[contains(@class,'sw-content-toolbar__inner')]/span[2]")
            time.sleep(3)
            logger.info(kwargs)
            if 'prefix' not in kwargs.keys() and 'range start' not in kwargs.keys() and 'range end' not in kwargs.keys() and 'name_invalid' in kwargs.keys():
                logger.error(
                    'Please specify prefix,range start,range end,name_invalid, comment when add dynamic scope.')
            else:
                logger.info(f"input Prefix:{kwargs['prefix']}")
                self.configure_text_field('Prefix', kwargs['prefix'])
                logger.info(f"input Range Start:{kwargs['range start']}")
                self.configure_text_field('Range Start', kwargs['range start'])
                logger.info(f"input Range End:{kwargs['range end']}")
                self.configure_text_field('Range End', kwargs['range end'])
                for name_invalid in kwargs['name_invalid']:
                    if 'empty' in str(name_invalid):
                        logger.info(f"input empty name:{name_invalid['empty']}")
                        self.configure_text_field('Name', name_invalid['empty'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        res = self.compare_error_message('You need to give the scope a name')
                        logger.info(f'compare_error_message is {res}')
                        logger.info('compare successfully')
                    if 'long more than 50' in str(name_invalid):
                        logger.info(f"input Name with lenth of long more than 50:{name_invalid['long more than 50']}")
                        self.configure_text_field('Name', name_invalid['long more than 50'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message('Name is too long. It should be less than 50 characters')
                        logger.info('compare successfully')
                logger.info('ready to close browser')
                self.close_browser()
                logger.info('browser is closed')
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            Assertion.fail("ERR:Check popped error message failed")
            return False

    def configure_dhcpv6_dynamic_scope_with_preferred_lifetime_invalid(self, **kwargs):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            logger.info('click Add Dynamic button')
            # self.click_element('xpath', '//span[contains(text(),"Add Dynamic")]')
            self.click_element('xpath', "//div[contains(@class,'sw-content-toolbar__inner')]/span[2]")

            time.sleep(3)
            logger.info(kwargs)
            if 'name' not in kwargs.keys() and 'prefix' not in kwargs.keys() and 'range start' not in kwargs.keys() \
                    and 'range end' not in kwargs.keys() and "preferred_lifetime_invalid" not in kwargs.keys():
                logger.error('Please specify name,prefix,range start,range end,preferred_lifetime_invalid'
                             ' when add dynamic scope.')
            else:
                logger.info(f"input Name:{kwargs['name']}")
                self.configure_text_field('Name', kwargs['name'])
                logger.info(f"input Prefix:{kwargs['prefix']}")
                self.configure_text_field('Prefix', kwargs['prefix'])
                logger.info(f"input Range Start:{kwargs['range start']}")
                self.configure_text_field('Range Start', kwargs['range start'])
                logger.info(f"input Range End:{kwargs['range end']}")
                self.configure_text_field('Range End', kwargs['range end'])
                if 'comment' in kwargs.keys():
                    logger.info(f"input Comment:{kwargs['comment']}")
                    self.configure_text_field('Range End', kwargs['comment'])
                for lifetime in kwargs['preferred_lifetime_invalid']:
                    if 'pref more than valid' in str(lifetime):
                        logger.info(f"input Preferred Lifetime:{lifetime['pref more than valid']}")
                        self.configure_text_field('Preferred Lifetime', lifetime['pref more than valid'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message("Failed: Preferred Lifetime can't be larger than Valid Lifetime")
                        logger.info('compare successfully')
                    elif 'negative' in str(lifetime):
                        logger.info(f"input Preferred Lifetime:{lifetime['pref negative']}")
                        self.configure_text_field('Preferred Lifetime', lifetime['pref negative'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message('Please specify Preferred Lifetime between 0 and 71582789')
                        logger.info('compare successfully')
                logger.info('ready to close browser')
                self.close_browser()
                logger.info('browser is closed')
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    def configure_dhcpv6_dynamic_scope_with_valid_lifetime_invalid(self, **kwargs):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            logger.info('click Add Dynamic button')
            # self.click_element('xpath', '//span[contains(text(),"Add Dynamic")]')
            self.click_element('xpath', "//div[contains(@class,'sw-content-toolbar__inner')]/span[2]")
            time.sleep(3)
            logger.info(kwargs)
            if 'name' not in kwargs.keys() and 'prefix' not in kwargs.keys() and 'range start' not in kwargs.keys() \
                    and 'range end' not in kwargs.keys() and 'valid_lifetime_invalid' not in kwargs.keys():
                logger.error('Please specify name,prefix,range start,range end or valid_lifetime_invalid when add '
                             'dynamic scope.')
            else:
                logger.info(f"input Name:{kwargs['name']}")
                self.configure_text_field('Name', kwargs['name'])
                logger.info(f"input Prefix:{kwargs['prefix']}")
                self.configure_text_field('Prefix', kwargs['prefix'])
                logger.info(f"input Range Start:{kwargs['range start']}")
                self.configure_text_field('Range Start', kwargs['range start'])
                logger.info(f"input Range End:{kwargs['range end']}")
                self.configure_text_field('Range End', kwargs['range end'])
                if 'comment' in kwargs.keys():
                    logger.info(f"input Comment:{kwargs['comment']}")
                    self.configure_text_field('Range End', kwargs['comment'])
                for lifetime in kwargs['valid_lifetime_invalid']:
                    if 'empty' in str(lifetime):
                        logger.info('test empty:')
                        logger.info(f"input Valid Lifetime:{lifetime['empty']}")
                        self.configure_text_field('Valid Lifetime', lifetime['empty'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message("Failed: Preferred Lifetime can't be larger than Valid Lifetime")
                        logger.info('compare successfully')
                    elif 'negative' in str(lifetime):
                        logger.info('test negative')
                        logger.info(f"input Valid Lifetime:{lifetime['negative']}")
                        self.configure_text_field('Valid Lifetime', lifetime['negative'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message('Please specify Valid Lifetime between 0 and 71582789')
                        logger.info('compare successfully')
                    elif 'decimal' in str(lifetime):
                        logger.info('test decimal')
                        logger.info(f"input Valid Lifetime:{lifetime['decimal']}")
                        self.configure_text_field('Valid Lifetime', lifetime['decimal'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message("Failed: Schema validation error: property 'valid': invalid format")
                        logger.info('compare successfully')
                logger.info('ready to close browser')
                self.close_browser()
                logger.info('browser is closed')
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    def configure_dhcpv6_dynamic_scope_with_invalid_prefix(self, **kwargs):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            logger.info('click Add Dynamic button')
            # self.click_element('xpath', '//span[contains(text(),"Add Dynamic")]')
            self.click_element('xpath', "//div[contains(@class,'sw-content-toolbar__inner')]/span[2]")
            time.sleep(3)
            logger.info(kwargs)
            if 'name' not in kwargs.keys() and 'prefix' not in kwargs.keys() and 'range start' not in kwargs.keys() \
                    and 'range end' not in kwargs.keys() and 'prefix_invalid' not in kwargs.keys():
                logger.error('Please specify name,range start,range end and prefix_invalid when add dynamic '
                             'scope.')
            else:
                logger.info(f"input Name:{kwargs['name']}")
                self.configure_text_field('Name', kwargs['name'])
                logger.info(f"input Range Start:{kwargs['range start']}")
                self.configure_text_field('Range Start', kwargs['range start'])
                logger.info(f"input Range End:{kwargs['range end']}")
                self.configure_text_field('Range End', kwargs['range end'])
                if 'comment' in kwargs.keys():
                    logger.info(f"input Comment:{kwargs['comment']}")
                    self.configure_text_field('Range End', kwargs['comment'])
                for pref in kwargs['prefix_invalid']:
                    if 'invalid_value' in str(pref):
                        logger.info('test invalid value:')
                        logger.info(f"input Prefix:{pref['invalid_value']}")
                        self.configure_text_field('Prefix', pref['invalid_value'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message("Invalid Prefix")
                        logger.info('compare successfully')
                    elif 'invalid_format' in str(pref):
                        logger.info('test invalid format:')
                        logger.info(f"input Prefix:{pref['invalid_format']}")
                        self.configure_text_field('Prefix', pref['invalid_format'])
                        logger.info('click button OK ')
                        self.click_element('xpath', "//div/button[text()='OK']")
                        errormessage = self.get_element('class', "sw-status-info__text__message")
                        logger.info("Actual Error text\t: " + str(errormessage.text))
                        logger.info('verify error massge if it is correctly')
                        self.compare_error_message("Invalid Prefix")
                        logger.info('compare successfully')
                logger.info('ready to close browser')
                self.close_browser()
                logger.info('browser is closed')
                return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    def configure_dhcpv6_dynamic_scope_with_invalid_range(self, scope_list):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            logger.info('click Add Dynamic button')
            # self.click_element('xpath', '//span[contains(text(),"Add Dynamic")]')
            self.click_element('xpath', "//div[contains(@class,'sw-content-toolbar__inner')]/span[2]")
            time.sleep(3)
            for scope in scope_list:
                logger.info(scope)
                if 'name' not in scope.keys() and 'prefix' in scope.keys() and 'range start' in scope.keys() and 'range end' in scope.keys():
                    logger.error('Please specify name,prefix,range start,range end.')
                    return False
                else:
                    logger.info(f"input Name:{scope['name']}")
                    self.configure_text_field('Name', scope['name'])
                    logger.info(f"input Prefix:{scope['prefix']}")
                    self.configure_text_field('Prefix', scope['prefix'])
                    logger.info(f"input Range Start:{scope['range start']}")
                    self.configure_text_field('Range Start', scope['range start'])
                    logger.info(f"input Range End:{scope['range end']}")
                    self.configure_text_field('Range End', scope['range end'])
                    logger.info('click button OK ')
                    self.click_element('xpath', "//div/button[text()='OK']")
                    errormessage = self.get_element('class', "sw-status-info__text__message")
                    logger.info("Actual Error text\t: " + str(errormessage.text))
                    logger.info('verify error massge if it is correctly')
                    self.compare_error_message("Invalid Range Start IPv6 Address")
            logger.info('ready to close browser')
            self.close_browser()
            logger.info('browser is closed')
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    def configure_dhcpv6_dynamic_scope_with_invalid_dns_server(self, s_member, d_server_list):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            self.click_on_edit_element_after_hovering(s_member)
            logger.info('click DNS tab')
            self.navigate_to_tab('DNS')
            for d_server in d_server_list:
                logger.info(f"input the first dns server:{d_server}")
                self.configure_text_field('DNS Server 1', d_server)
                logger.info('click button OK')
                self.click_element('xpath', "//div/button[text()='OK']")
                errormessage = self.get_element('class', "sw-status-info__text__message")
                logger.info("Actual Error text\t: " + str(errormessage.text))
                logger.info('verify error massge if it is correctly')
                # self.compare_error_message(
                #     "Failed: Schema validation error: property 'primary': invalid format")  # this is 7.0.1
                self.compare_error_message("DNS Server IP address is invalid.")  # this is 7.1.1 error
                logger.info('compare successfully')
            logger.info('ready to close browser')
            self.close_browser()
            logger.info('browser is closed')
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    def configure_dhcpv6_dynamic_scope_with_invalid_domain_name(self, s_member, d_name_list):
        try:
            self.login_gui()
            self.navigate_to_dhcp_server_page()
            self.navigate_to_level1_tab_dhcp_server_lease_scopes()
            self.navigate_to_level2_tab_ipv6()
            self.click_on_edit_element_after_hovering(s_member)
            logger.info('click DNS tab')
            self.navigate_to_tab('DNS')
            for d_name in d_name_list:
                logger.info(f'input domain name:{d_name}')
                self.configure_text_field('Domain Name', d_name)
                self.click_element('xpath', "//div/button[text()='OK']")
                errormessage = self.get_element('class', "sw-status-info__text__message")
                logger.info("Actual Error text\t: " + str(errormessage.text))
                logger.info('verify error massge if it is correctly')
                self.compare_error_message("Invalid Domain Name.")
                # self.compare_error_message("DNS Server IP address is invalid.")
                logger.info('compare successfully')
            logger.info('ready to close browser')
            self.close_browser()
            logger.info('browser is closed')
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            logger.error("ERR:Check popped error message failed")

    # ====================================Navigates to Network page===============================

    def navigate_to_network_page(self):
        logger.debug2("Navigating to Network page")
        self.navigate_to_page("icon-topo")

    def navigate_to_page(self, page_identifier):
        icon = self.get_top_icon()
        return self.click_relative_element(icon, 'class', page_identifier)

    def get_top_icon(self):
        logger.debug2("Getting page navigation icon")
        icons = self.get_element('class', 'fw-app-header__head__top-nav')
        return icons

    def navigate_to_section(self, section_header, section_identifier, labelName=None):
        if self.does_element_exist_now('xpath',
                                       "//span[contains(@class, 'sw-breadcrumb__item__text') and text()='" + section_identifier + "']"):
            logger.info("Page :" + section_identifier)
        else:
            if self.does_element_exist_now('xpath',
                                           "//span[contains(@class, '" + section_header + "')]/following::div/span[text()='" + section_identifier + "']"):
                logger.info("Section is already expanded")
            else:
                logger.info("Expanding section")
                icon = self.get_left_panel()
                if labelName is not None:
                    element_xpath = "//span[contains(@class, '" + section_header + "')]/following::span[text()='" + labelName + "'] "
                    self.click_relative_element(icon, 'xpath', element_xpath)
                else:
                    self.click_relative_element(icon, 'class', section_header)
                logger.info("Expanded section successfully")
            self.click_element('xpath',
                               "//span[contains(@class, '" + section_header + "')]/following::div/span[text()='" + section_identifier + "']")
            self.wait_for_page_data_to_be_rendered()

    def navigate_to_tab(self, tab_identifier):
        tab_identifier_xpath1 = "//span[text()='" + tab_identifier + "']"
        tab_identifier_xpath2 = "//span[contains(text(),'" + tab_identifier + "')]"
        tab_level_identifier_xpath = "/ancestor::li[contains(@class, 'sw-tab--l1')]"
        class_value = self.get_attribute_value('xpath',
                                               tab_identifier_xpath1 + tab_level_identifier_xpath + "|" +
                                               tab_identifier_xpath2 + tab_level_identifier_xpath, 'class',visibility=False)
        if 'sw-tab--active' in class_value:
            logger.debug2("Tab : " + tab_identifier)
        else:
            self.click_element('xpath',
                               tab_identifier_xpath1 + tab_level_identifier_xpath + "|" +
                               tab_identifier_xpath2 + tab_level_identifier_xpath)
            self.wait_for_page_data_to_be_rendered()

    def navigate_to_level2_tab(self, tab_identifier):
        class_value = self.get_attribute_value('xpath',
                                               "//span[text()='" + tab_identifier + "']/ancestor::li[contains(@class, 'sw-tab--l2')]",
                                               'class')
        if 'sw-tab--active' in class_value:
            logger.debug2("Already is tab : " + tab_identifier)
        else:
            self.click_element('xpath',
                               "//span[text()='" + tab_identifier + "']/ancestor::li[contains(@class, 'sw-tab--l2')]")
            self.wait_for_page_data_to_be_rendered()

    def logout_ui(self):
        try:
            logger.info("Logging out")
            logger.debug("Action - Clicked drop down")
            self.click_element('xpath', '//div/span[contains(@class,"sw-avatar__initials")]')
            logger.debug("Action - Clicked logout")
            self.click_element('xpath', '//span[contains(text(),"Log Out")]')
            logger.debug("Action - Confirmed logout")
            self.click_element('xpath', '//div/button[contains(text(),"Continue")]')
            if self.does_element_exist('xpath', '//div[contains(text(), "You have been logged out.")]'):
                logger.info("Logged out")
            self.close_browser()
            self.quit()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            self.close_browser()
            self.quit()
            Assertion.fail("Firewall Logout Failed")

    def get_left_panel(self):
        logger.debug2("Getting left navigation panel")
        icons = self.get_element('class', 'sw-app__nav')
        return icons

    # =================================from ui_helper===================================
    def configure_radio_button(self, radio_button_label, group_name=None):
        try:
            logger.debug("Configure - Setting radio button \t: " + str(radio_button_label))
            if group_name is not None:
                self.click_element('xpath',
                                   "//span[contains(text(), '" + group_name + "')]/following::*[contains(text(), '" + radio_button_label + "')]")
            else:
                self.click_element('xpath', '//span[text()="' + radio_button_label + '"]')

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set radio button")


fwpage = FWPage(f'https://{Parameter.FIREWALL}', f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/network/dhcp-server', 'admin',
                'S0nic@uto')
