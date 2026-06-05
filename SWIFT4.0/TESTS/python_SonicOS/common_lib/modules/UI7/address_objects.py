from modules.UI7.common_require import *
from modules.API.network import AddressobjectsApi
from modules.API.network import AddressgroupsApi
from utm import Firewall

fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
address_obj = AddressobjectsApi(fw)
addressgroup_obj = AddressgroupsApi(fw)

class AddressObjects:
    # FUNCTIONALITY     : Checks the address objects in the firewall
    # INPUT             : None
    # RETURNS           : Returns true if settings match
    def verify_address_object_firewall(self):
        try:
            logger.info("Verifying Address Object in the firewall")
            addressObjectType = self.addressObjectType.lower()
            data = address_obj.get_addressobject(addressObjectType, 'name', self.addressObjectName, self.testType)
            logger.info(data)
            testType = self.testType.lower()
            effective_json = data['address_objects'][0][testType]
            if effective_json['name'] == self.addressObjectName:
                logger.info("Name is right")
                if effective_json['zone'] == self.addressObjectZone:
                    logger.info("Zone is right")
                    if addressObjectType == "host":
                        effective_json_host = effective_json['host']
                        self.json_compare(effective_json_host, "ip", self.addressObjectIP)
                    if addressObjectType == "range":
                        effective_json_range = effective_json['range']
                        self.json_compare(effective_json_range, "begin", self.addressObjectIPStart)
                        self.json_compare(effective_json_range, "end", self.addressObjectIPEnd)
                    if addressObjectType == "network":
                        effective_json_network = effective_json['network']
                        self.json_compare(effective_json_network, "subnet", self.addressObjectIPStart)
                        self.json_compare(effective_json_network, "mask", self.addressObjectIPEnd)
                    if addressObjectType == "fqdn":
                        self.json_compare(effective_json, "domain", self.addressObjectHostName)
                        self.json_compare(effective_json, "dns_ttl", self.addressObjectTTL)
                    if addressObjectType == "mac":
                        self.json_compare(effective_json, "address", self.addressObjectMAC)
                        self.json_compare(effective_json, "multi_homed", self.multiHomed)
                    logger.info("Found Target Address Object In The Firewall Using API")
                    return True
                else:
                    logger.info("Zone is not right")
                    return False
            else:
                logger.info("Name is not right")
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Compare given paramters with settings in the firewall
    # INPUT             : firewall_json, target_parameter, target_value
    # RETURNS           : Returns true if settings match
    def json_compare(self, firewall_json, target_parameter, target_value):
        try:
            if firewall_json[target_parameter] == target_value:
                logger.info(str(target_parameter) + " is right!")
            else:
                logger.info(str(target_parameter) + " is not right!")
                return False    
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Checks the address groups in the firewall
    # INPUT             : None
    # RETURNS           : Returns true if settings match
    def verify_address_group_firewall(self, addressGroupName=None):
        try:
            if addressGroupName is None:
                addressGroupName = self.addressGroupName
            logger.info("Verifying Address Group in the firewall")
            data = addressgroup_obj.get_addressgroup( self.testType, 'name', addressGroupName)
            logger.info(data)
            testType = self.testType.lower()
            effective_json = data['address_groups'][0]
            if addressGroupName == "Backward-Icon-test":
                if len(effective_json['ipv4']['address_object']['ipv4']) == 2:
                    return True
            if effective_json[testType]['name'] == addressGroupName:
                logger.info("Address group name is right")
                if testType == 'ipv4':
                    if len(effective_json['ipv4']['address_object']['ipv4']) == len(self.addressGroupIn):
                        logger.info("IPv4 address objects is right ")
                        return True
                    else:
                        logger.info("IPv4 address objects is not right")
                        return False
                else:
                    if len(effective_json['ipv6']['address_group']['ipv6']) == len(self.addressGroupIn):
                        logger.info("IPv6 address objects is right")
                        return True
                    else:
                        logger.info("IPv6 address objects is not right")
                        return False
            else:
                logger.info("Address group name is not right")
                return False            
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Checks the existence of the address object on UI
    # INPUT             : NTP Server(optional)
    # RETURNS           : Returns true if the address object exists
    def does_address_object_exist(self, addressObjectName=None):
        try:
            if addressObjectName is None:
                addressObjectName = self.addressObjectName
            self.ui_helper.search_string(addressObjectName)
            if addressObjectName == "test-cancel-button":
                if self.ui_wrapper.does_element_exist_now('xpath', "//div[contains(@class, 'sw-table-row__cell__wrapper')]"
                                                                   "/div/span[text()='"+addressObjectName+"']"):
                    logger.info("Address Object "+addressObjectName+" unexpected exists")
                    return False
                else:
                    logger.info("Address Object does not exist as expected")
                    return True
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[contains(@class, 'sw-table-row__cell__wrapper')]"
                                                               "/div/span[text()='"+addressObjectName+"']"):
                logger.info("Address Object "+addressObjectName+" exists")
                return True
            else:
                logger.info("Address Object does not exist")
                return False
        except Exception as e:
            logger.info(e)

    # FUNCTIONALITY     : Checks the existence of the address group on UI
    # INPUT             : NTP Server(optional)
    # RETURNS           : Returns true if the address group exists
    def does_address_group_exist(self, addressGroupName=None):
        try:
            if addressGroupName is None:
                addressGroupName = self.addressGroupName
            self.ui_helper.search_string(addressGroupName)
            if addressGroupName == "test_cancel_button":
                if self.ui_wrapper.does_element_exist_now('xpath', "//div[contains(@class, 'sw-table-row__cell')]"
                                                                   "/div[text()='"+addressGroupName+"']"):
                    logger.info("Address Group "+addressGroupName+" unexpected exists")
                    return False
                else:
                    logger.info("Address Group does not exist as expected")
                    return True
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[contains(@class, 'sw-table-row__cell')]"
                                                               "/div[text()='"+addressGroupName+"']"):
                logger.info("Address Group "+addressGroupName+" exists")
                return True
            else:
                logger.info("Address Group does not exist")
                return False
        except Exception as e:
            logger.info(e)

    # FUNCTIONALITY     : Config an address object
    # INPUT             : None
    # RETURNS           : None
    def configure_address_object(self):
        try:
            if hasattr(self,'addressObjectName'):
                self.my_configure_text_field('Name', self.addressObjectName)             
                self.my_select_drop_down_value('Zone Assignment', self.addressObjectZone)
                if self.addressObjectTest == "create":
                    self.my_select_drop_down_value('Host', self.addressObjectType)
                if self.addressObjectType == "Range":
                    self.my_configure_text_field('Starting IP Address', self.addressObjectIPStart)
                    self.my_configure_text_field('Ending IP Address', self.addressObjectIPEnd)
                if self.addressObjectType == "Network":
                    self.my_configure_text_field('Network', self.addressObjectIPStart)
                    self.my_configure_text_field('Netmask / Prefix Length', self.addressObjectIPEnd)
                if self.addressObjectType == "FQDN":
                    self.my_configure_text_field('FQDN Hostname', self.addressObjectHostName)
                    if self.manualSetDNSEntries == True:
                        self.ui_helper.configure_toggle_button( "Manually set DNS entries", self.manualSetDNSEntries)
                        self.my_configure_text_field('TTL (120 ~ 86400s)', self.addressObjectTTL)
                if self.addressObjectType == "MAC":
                    self.my_configure_text_field('MAC Address', self.addressObjectMAC)
                    if self.multiHomed == True:
                        self.ui_helper.configure_toggle_button("Multi homed", self.multiHomed)
                if self.addressObjectType == "Host":
                    self.my_configure_text_field('IP Address', self.addressObjectIP)
                if self.addressObjectName == "test-cancel-button":
                    self.ui_helper.cancel_page()
                else:
                    self.ui_helper.submit_page()
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Config Address object Failed")

    # FUNCTIONALITY     : Valid address object creation
    # INPUT             :
    # RETURNS           : Address object is created
    def create_address_object(self):
        try:
            self.navigation.navigate_to_address_object_section()
            if self.addressObjectName == "test-cancel-button":
                self.ui_helper.click_add_icon()
                self.ui_wrapper.wait_for_text("Address Object Settings")
                self.configure_address_object()
                self.ui_helper.click_refresh_icon()
                self.does_address_object_exist(self.addressObjectName)
            else:
                if self.does_address_object_exist(self.addressObjectName):
                    self.delete_address_object()
                logger.info("Adding an address object: " + str(self.addressObjectName))
                self.ui_helper.click_add_icon()
                self.ui_wrapper.wait_for_text("Address Object Settings")
                self.configure_address_object()
                self.ui_helper.wait_for_success_banner()
                self.ui_helper.click_refresh_icon()
                self.does_address_object_exist(self.addressObjectName)
                self.verify_address_object_firewall()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Create Address Object Failed")

    # FUNCTIONALITY     : Edit the existing address object
    # INPUT             : Address Object name
    # RETURNS           : Address object is edited
    def edit_address_object(self, addressObjectName=None):
        try:
            self.navigation.navigate_to_address_object_section()
            logger.info("Editing the address object from:"+ str(self.originalAOName) + " to:" + str(self.addressObjectName))
            if self.does_address_object_exist(self.originalAOName): 
                self.ui_helper.click_on_edit_element_after_hovering(self.originalAOName)
                self.configure_address_object()
                self.ui_helper.wait_for_success_banner()
                self.ui_helper.click_refresh_icon()
                self.does_address_object_exist(self.addressObjectName)
                self.verify_address_object_firewall()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Edit Adderss Object Failed")

    # FUNCTIONALITY     : Config an address group
    # INPUT             : None
    # RETURNS           : None
    def configure_address_group(self, addressGroupName=None):
        try:
            if addressGroupName is None:
                addressGroupName = self.addressGroupName
            self.my_configure_text_field('Name', addressGroupName) 
            self.ui_helper.select_tree_values(self.addressGroupIn)
            if addressGroupName == "test_cancel_button":
                self.ui_helper.cancel_page()
            elif addressGroupName == "Backward-Icon-test":
                self.ui_helper.click_reverse_all_select_icon()
                targetAO = 'X0 Subnet'
                self.click_element('xpath', "//div/span[text()='" + targetAO + "']")
                self.ui_helper.click_forward_play_icon()
                self.ui_helper.submit_page()
            else:
                self.ui_helper.submit_page()
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Config Address group Failed")

    # FUNCTIONALITY     : Valid address group creation
    # INPUT             :
    # RETURNS           : Address group is created
    def create_address_group(self):
        try:
            self.navigation.navigate_to_address_group_section()
            if self.addressGroupName == "test_cancel_button":
                self.ui_helper.click_add_icon()
                self.ui_wrapper.wait_for_text("Address Group Settings")
                self.configure_address_group()
                self.ui_helper.click_refresh_icon()
                self.does_address_group_exist(self.addressGroupName)
            else:
                if self.does_address_group_exist(self.addressGroupName):
                    self.delete_address_group()
                logger.info("Adding an address group: " + str(self.addressGroupName))
                self.ui_helper.click_add_icon()
                self.ui_wrapper.wait_for_text("Address Group Settings")
                self.configure_address_group()
                self.ui_helper.wait_for_success_banner()
                self.ui_helper.click_refresh_icon()
                self.does_address_group_exist(self.addressGroupName)
                self.verify_address_group_firewall()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Create Address Group Failed")

    # FUNCTIONALITY     : Edits the existing address group
    # INPUT             : Address Group name
    # RETURNS           : Address Group is edited
    def edit_address_group(self):
        try:
            self.navigation.navigate_to_address_group_section()
            logger.info("Editing the address group from:"+ str(self.addressGroupName) + " to:" + str(self.targetAGName))
            if self.does_address_group_exist(self.addressGroupName):
                self.ui_helper.click_on_edit_element_after_hovering(self.addressGroupName)
                self.my_configure_text_field('Name', self.targetAGName)
                self.ui_helper.select_tree_values(self.addressGroupTargetIn)
                self.ui_helper.select_group_values(self.addressGroupTargetIn, tree='right')
                self.ui_helper.unselect_tree_values(self.addressGroupIn)
                self.ui_helper.submit_page()
                self.ui_helper.wait_for_success_banner()
                self.ui_helper.click_refresh_icon()
                self.does_address_group_exist(self.targetAGName)
                self.verify_address_group_firewall(self.targetAGName)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Edit Adderss Group Failed")

    # FUNCTIONALITY     : Delete the address object
    # INPUT             : target address object(optional)
    # RETURNS           : None
    def delete_address_object(self, addressObjectName=None):
        try:
            self.navigation.navigate_to_address_object_section()
            logger.info("Deleting the address object")
            if addressObjectName is None:
                addressObjectName = self.addressObjectName
            if self.does_address_object_exist(addressObjectName):
                self.ui_helper.click_on_delete_element_after_hovering(addressObjectName)
                self.ui_helper.accept_alert()
                time.sleep(1)
                self.ui_helper.accept_alert()
                if self.does_address_object_exist(addressObjectName):
                    logger.info("Delete address object failed")
                else:
                    logger.info("Delete address object successfully")
            else:
                logger.info("Address object need to delete does not exist")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete address object failed")

    # FUNCTIONALITY     : Delete the address group
    # INPUT             : target address group(optional)
    # RETURNS           : None
    def delete_address_group(self, addressGroupName=None):
        try:
            self.navigation.navigate_to_address_group_section()
            logger.info("Deleting the address group")
            if addressGroupName is None:
                addressGroupName = self.addressGroupName
            if self.does_address_group_exist(addressGroupName):
                self.ui_helper.click_on_delete_element_after_hovering(addressGroupName)
                self.ui_helper.accept_alert()
                time.sleep(1)
                self.ui_helper.accept_alert()
                if self.does_address_group_exist(addressGroupName):
                    logger.info("Delete address group failed")
                else:
                    logger.info("Delete address group successfully")
            else:
                logger.info("Address group need to delete does not exist")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete address group failed")

    # save more time than related function in ui_helpper
    def my_configure_text_field(self, text_box_label, text_value):
        try:
            logger.debug("Configure - Text field "+text_box_label+" with value  \t: "+ str(text_value))
            self.ui_wrapper.set_text_field('xpath', '//div[contains(@class,"label") and text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[text()="'+text_box_label+'"]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label")]/span[contains(text(), "'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]|'
                                                    '//div[contains(@class, "label") and contains(text(),"'+text_box_label+'")]/'
                                                    'following::input[@type="text" or @type="password"]', text_value)
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Configure - Unable to set text field")

    # save more time than related function in ui_helpper
    def my_select_drop_down_value(self, select_identifier, select_value, modal=False):
        try:
            logger.debug2("Selecting drop down value \t: "+ str(select_value))
            if modal is True:
                self.click_element('xpath', "//div[contains(@class, 'sw-modal__main-body')]"
                                            "//following::*[contains(text(), '"+select_identifier+"')]"
                                            "/following::*[contains(@class, 'sw-select__icon')]")
            else:
                self.click_element('xpath', "//span[contains(text(), '"+select_identifier+"')]/following::*"
                                        "[contains(@class, 'sw-select__icon')]")
            element = self.ui_wrapper.move_to_the_element('xpath',  "//span[contains(text(), '"+select_identifier+"')]"
                                                                    "/following::div[contains(@class, 'sw-dropdown')]/"
                                                                    "span[text()='"+ select_value+"']", False)
            element.click()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Action - Unable to select from drop down list")
