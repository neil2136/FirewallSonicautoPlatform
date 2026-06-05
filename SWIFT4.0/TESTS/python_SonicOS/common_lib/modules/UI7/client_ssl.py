from modules.UI7.common_require import *
from modules.API.dpissl import ClientSslApi
from pykeyboard import *

from utm import Firewall
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
clientssl_obj = ClientSslApi(fw)

class ClientSsl:

    # FUNCTIONALITY     : Checks the system time setting in the firewall
    # INPUT             : None
    # RETURNS           : Returns true if settings match
    def verify_dpissl_client_firewall(self):
        try:
            logger.info("Verifying DPISSL Client Settings in the firewall")
            data = clientssl_obj.get_sslclient_config()
            logger.info(data)
            effective_json = data['dpi_ssl']['client']
            effective_json1 = data['dpi_ssl']['client']['gateway']
            if self.testType == 'modify_certificate':
                if effective_json['resigning_authority']['default'] == 'none-2048-bit': 
                    logger.info("Verified firewall setting is right!")
                    return True
            #if self.testType == 'Exclude' or self.testType == 'Include':
            #    self.testType = self.testType.lower()
            #    if effective_json['cfs_categories'][self.testType] == True: 
            #        logger.info("Verified firewall setting is right!")
            #        return True
            if self.testType == 'positive_test':
                self.json_compare(effective_json, "expired_ca", self.allowExpiredCa)
            self.json_compare(effective_json, "enable", self.enableSslIns)            
            self.json_compare(effective_json, "intrusion_prevention", self.intrusPre)
            self.json_compare(effective_json1, "anti_virus", self.gatAntVir)
            self.json_compare(effective_json1, "anti_spyware", self.gatAntSpy)
            self.json_compare(effective_json, "application_firewall", self.appFirewall)
            self.json_compare(effective_json, "content_filter", self.conFilter)
            self.json_compare(effective_json, "authenticate_server_for_decrypted_connections", self.alwAutServer)

            self.json_compare(effective_json, "deployment_server_domains", self.proxySetup)
            self.json_compare(effective_json, "bypass_decryption", self.allowSSL)
            self.json_compare(effective_json, "audit_built_in_exclusion", self.audExcluDom)
            self.json_compare(effective_json, "authenticate_server", self.alwAuthServ)
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Compare given paramters with settings in the firewall
    # INPUT             : firewall_json, target_parameter, target_value
    # RETURNS           : Returns true if settings match
    def json_compare(firewall_json, target_parameter, target_value):
        try:
            flag = 0
            if firewall_json[target_parameter] == target_value:
                logger.info(str(target_parameter) + " is right!")
            else:
                logger.info(str(target_parameter) + " is not right!")
                flag += 1
            logger.info("flag is")
            logger.info(flag)
            Assertion.assert_equal(flag, 0, 'Firewall verification failed')   
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Configure parameters on general tab
    # INPUT             : None
    # RETURNS           : None
    def configure_general_tab_settings(self):
        try:
            self.navigation.navigate_to_client_ssl_general_section()
            logger.info("Configure - Client SSL General Tab Settings")
            time.sleep(1)
            if hasattr(self, 'enableSslIns'):
                logger.debug("Configure - Enable SSL Inspection \t: " + str(self.enableSslIns))
                self.ui_helper.configure_toggle_button('Enable SSl Inspection', self.enableSslIns)
            if hasattr(self, 'intrusPre'):
                logger.debug("Configure - Intrustion Prevention \t: " + str(self.intrusPre))
                self.ui_helper.configure_toggle_button("Intrusion Prevention", self.intrusPre)
            if hasattr(self, 'gatAntVir'):
                logger.debug("Configure - Gateway Anti-Virus \t: " + str(self.gatAntVir))
                self.ui_helper.configure_toggle_button('Gateway Anti-Virus', self.gatAntVir)
            if hasattr(self, 'gatAntSpy'):
                logger.debug("Configure - Gateway Anti-Spyware \t: " + str(self.gatAntSpy))
                self.ui_helper.configure_toggle_button('Gateway Anti-Spyware', self.gatAntSpy)
            if hasattr(self, 'appFirewall'):
                logger.debug("Configure - Application Firewall \t: " + str(self.appFirewall))
                self.ui_helper.configure_toggle_button('Application Firewall', self.appFirewall)
            if hasattr(self, 'conFilter'):
                logger.debug("Configure - Content Filter \t: " + str(self.conFilter))
                self.ui_helper.configure_toggle_button('Content Filter', self.conFilter)
            if self.testType == 'reverse_test':
                if hasattr(self, 'allowExpiredCa'):
                    logger.debug("Configure - Allow Expired CA \t: " + str(self.allowExpiredCa))
                    self.ui_helper.configure_toggle_button('Allow Expired CA', self.allowExpiredCa)
                if hasattr(self, 'alwAutServer'):
                    logger.debug("Configure - Always authenticate server for decrypted connections \t: " + str(self.alwAutServer))
                    self.ui_helper.configure_toggle_button('Always authenticate server for decrypted connections', self.alwAutServer)
            else:
                if hasattr(self, 'alwAutServer'):
                    logger.debug("Configure - Always authenticate server for decrypted connections \t: " + str(self.alwAutServer))
                    self.ui_helper.configure_toggle_button('Always authenticate server for decrypted connections', self.alwAutServer)
                    if hasattr(self, 'allowExpiredCa'):
                        logger.debug("Configure - Allow Expired CA \t: " + str(self.allowExpiredCa))
                        self.ui_helper.configure_toggle_button('Allow Expired CA', self.allowExpiredCa)
            if hasattr(self, 'proxySetup'):
                logger.debug("Configure - Deployments ...domains, ex: Proxy setup \t: " + str(self.proxySetup))
                self.ui_helper.configure_toggle_button('Deployments wherein the Firewall sees a single server IP for different server domains, ex: Proxy setup', self.proxySetup)
            if hasattr(self, 'allowSSL'):
                logger.debug("Configure - Allow SSL without decryption (bypass) when connection limit exceeded \t: " + str(self.allowSSL))
                self.ui_helper.configure_toggle_button('Allow SSL without decryption (bypass) when connection limit exceeded', self.allowSSL)
            if hasattr(self, 'audExcluDom'):
                logger.debug("Configure - Audit new default exclusion domain names prior to being added for exclusion \t: " + str(self.audExcluDom))
                self.ui_helper.configure_toggle_button('Audit new default exclusion domain names prior to being added for exclusion', self.audExcluDom)
            if hasattr(self, 'alwAuthServ'):
                logger.debug("Configure - Always authenticate server before applying exclusion policy \t: " + str(self.alwAuthServ))
                self.ui_helper.configure_toggle_button('Always authenticate server before applying exclusion policy', self.alwAuthServ)
            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            self.verify_dpissl_client_firewall()
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring Client SSL General Tab Failed")

    # FUNCTIONALITY     : Configure settings on certificate tab
    # INPUT             : None
    # RETURNS           : None
    def configure_certificate_tab_settings(self):
        try:
            self.navigation.navigate_to_client_ssl_certificate_section()
            logger.info("Configure - Client SSL Certificates Tab Settings")
            if self.testType == 'modify_certificate':
                logger.debug("Configure - certificate \t: " + str(self.certificate))
                self.ui_helper.select_drop_down_value("Certificate", self.certificate)
                self.ui_helper.submit_page()
                self.ui_helper.accept_alert()
                self.verify_dpissl_client_firewall()
            if self.testType == 'download_certificate':
                logger.info("Downloading the certificate...")
                self.ui_wrapper.click_element('xpath', '//button[text()="Download"]')
                self.ui_helper.accept_alert()
                pyk = PyKeyboard()
                pyk.tap_key(pyk.enter_key)
                time.sleep(2)
                target_file = '/root/Downloads/'+ str(self.certificate)
                Assertion.assert_equal(os.path.exists(target_file), True, 'Target file not exists')        
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring Client Certificate Tab Failed")
            
    # FUNCTIONALITY     : Configure settings on objects tab
    # INPUT             : value
    # RETURNS           : None
    def configure_objects_tab_settings(self):
        try:
            self.navigation.navigate_to_client_ssl_objects_section()
            logger.info("Configure - Client SSL Objects Tab Settings")
            selector = self.get_selenium_selector("class")
            if self.testarea == 'address':
                if self.testoption == 'Exclude':
                    button_num = 1
                    item_name = self.addressExclude
                    if self.addressExclude == 'X7 Subnet':
                        item_name = "None"
                if self.testoption == 'Include':
                    button_num = 2
                    item_name = self.addressInclude
                    if self.addressInclude == 'X7 Subnet':
                        item_name = "All"
            if self.testarea == 'service':
                if self.testoption == 'Exclude':
                    button_num = 3
                    item_name = self.serviceExclude
                    if self.serviceExclude == 'ZebTelnet':
                        item_name = "None"
                if self.testoption == 'Include':
                    button_num = 4
                    item_name = self.serviceInclude
                    if self.serviceInclude == 'ZebTelnet':
                        item_name = "All"
            if self.testarea == 'user':
                if self.testoption == 'Exclude':
                    button_num = 5
                    item_name = self.userExclude
                if self.testoption == 'Include':
                    button_num = 6
                    item_name = self.userInclude
            self.item_select(button_num, item_name)
            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            logger.info("Setting " + self.testarea + " " + self.testoption + " to: " + str(item_name) + " succeed!")
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring Client SSL General Failed")
            
    # FUNCTIONALITY     : Configure objects on certificate tab
    # INPUT             : value
    # RETURNS           : None
    def item_select(self, button_num, item_name):
        try:
            selector = self.get_selenium_selector("class")
            logger.info("Configure - " + self.testarea + " "+ self.testoption + " to: " + str(item_name))
            self.browser.find_elements(selector, 'icon-arrow-up')[button_num].click()
            if item_name == 'None' or item_name == 'All':
                js='var q=document.getElementsByClassName("sw-scroll-view__view__cont")[1].scrollTop=0'
            else:
                js='var q=document.getElementsByClassName("sw-scroll-view__view__cont")[1].scrollTop=100000'
            self.browser.execute_script(js) 
            self.ui_wrapper.click_element('xpath', "//div[contains(@class, 'sw-select-option')]/span[text()='" + item_name + "']")
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring Client SSL General Failed")

    # FUNCTIONALITY     : Checks the existence of the common name on UI
    # INPUT             : Common Name(optional)
    # RETURNS           : Returns true if the common name exists
    def does_common_name_exist(self, commonName=None):
        try:
            if commonName is None:
                commonName = self.commonName
            self.ui_helper.search_string(commonName)
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[text()='"+commonName+"']"):
                logger.info("Common name "+commonName+" exists")
                return True
            else:
                logger.info("Common name does not exist")
                return False
        except Exception as e:
            logger.info(e)
    
    # FUNCTIONALITY     : Add a common name  
    # INPUT             : None
    # RETURNS           : None
    def add_common_name(self):
        try:
            self.navigation.navigate_to_client_ssl_common_name_section()
            if self.does_common_name_exist():
                self.delete_common_name()   
            logger.info("Adding a common name: " + str(self.commonName))
            self.ui_helper.click_add_icon()
            self.ui_wrapper.set_text_field('xpath', '//span[text()="Please add new common name entries separated by comma or newline characters."]/following::textarea[@name="Default Textarea"]', self.commonName)
            if self.actionType == "Exclude":
                self.ui_helper.select_drop_down_value("Always authenticate server before applying exclusion policy", self.alwaysAuthServ)
            else:
                self.ui_wrapper.click_element('xpath', "//span[text()='" + self.actionType + "']")
            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            self.ui_helper.click_close_icon()
            Assertion.assert_equal(self.does_common_name_exist(), True, 'Target common name not found')
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Add Common Name Failed")

    # FUNCTIONALITY     : Delete a common name
    # INPUT             : Common_name(optional)
    # RETURNS           : None
    def delete_common_name(self, commonName=None):
        try:
            logger.info("Deleting the common name")
            if commonName is None:
                commonName = self.commonName
            self.ui_helper.click_on_delete_element_after_hovering(commonName)
            self.ui_helper.accept_alert()
            self.ui_helper.accept_alert()
            if self.does_common_name_exist(commonName):
                logger.info("Common name deleted failed")
            else:
                logger.info("Common name deleted successfully")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete common name failed")

    # FUNCTIONALITY     : Edit a common name
    # INPUT             : None
    # RETURNS           : None      
    def edit_common_name(self):
        try:
            self.navigation.navigate_to_client_ssl_common_name_section()
            if self.does_common_name_exist():
                logger.info("Editing the common name from baidu.com to:"+ str(self.commonName2))
                self.ui_helper.click_on_edit_element_after_hovering(self.commonName)
                self.ui_wrapper.set_text_field('xpath', '//span[text()="Please add new common name entries separated by comma or newline characters."]/following::textarea[@name="Default Textarea"]', self.commonName2)
                self.ui_wrapper.click_element('xpath', "//span[text()='" + self.actionType + "']")
                self.ui_helper.submit_page()
                self.ui_helper.accept_alert()
                self.ui_helper.click_close_icon()
                Assertion.assert_equal(self.does_common_name_exist(self.commonName2), True, 'Target common name not found')
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Edit Common Name Failed")
            
    # FUNCTIONALITY     : Import exclusions  
    # INPUT             : None
    # RETURNS           : None
    def import_exclusions(self):
        try:
            self.navigation.navigate_to_client_ssl_common_name_section() 
            logger.info("Import an exclusions file from: " + str(self.filePath))
            self.ui_wrapper.click_element('xpath', '//span[contains(@class,"icon-upload")]')
            pyk = PyKeyboard()
            pyk.type_string("/DEV_TESTS/python_SonicOS/7.0.0/UI7/client_ssl/default_all.txt")
            time.sleep(4)
            pyk.tap_key(pyk.enter_key)
            time.sleep(3)
            self.ui_wrapper.click_element('xpath', '//button[text()="Import"]')
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Add Common Name Failed")
            
    # FUNCTIONALITY     : Configure parameters on category based tab
    # INPUT             : None
    # RETURNS           : None
    def configure_cfs_category_based_tab_settings(self):
        try:
            if self.navigate_tag == True:
                self.navigation.navigate_to_client_ssl_cfs_category_section()
                js='var q=document.getElementsByClassName("sw-scroll-view__view__cont")[1].scrollTop=100000'
                self.browser.execute_script(js)
            logger.info("Configure - Client SSL CFS Category Tab Settings")
            if self.testType == 'Include':
                logger.debug("Configure - Select action with 'Include'.")
                self.ui_wrapper.click_element('xpath', '//span[text()="Include"]')
            elif self.testType == 'Exclude':
                logger.debug("Configure - Select action with 'Exclude'.")
                self.ui_wrapper.click_element('xpath', '//span[text()="Exclude"]')
            if hasattr(self, 'testArea'):
                if self.testArea == 'Button_Test':
                    if hasattr(self, 'selectAll'):
                        logger.debug("Configure - Select all Categories \t: " + str(self.selectAll))
                        self.ui_helper.configure_toggle_button('Select all Categories', self.selectAll)
                    if hasattr(self, 'exclConnction'):
                        logger.debug("Configure - Exclude connection if ... not available \t: " + str(self.exclConnction))
                        self.ui_helper.configure_toggle_button('Exclude connection if Content Filter Category is not available', self.exclConnction)
            else:
                self.ui_helper.configure_toggle_button(self.actionOpt, self.actionOptValue)
                self.navigate_tag = False
            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            time.sleep(1)
            #self.verify_dpissl_client_firewall()
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring Client SSL CFS Category Based Tab Failed")


