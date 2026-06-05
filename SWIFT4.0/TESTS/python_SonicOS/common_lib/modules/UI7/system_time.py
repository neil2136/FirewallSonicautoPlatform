from modules.UI7.common_require import *
from modules.API.system import TimeApi

from utm import Firewall
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
time_obj = TimeApi(fw)

class SystemTime:
    # FUNCTIONALITY     : Checks the system time setting in the firewall
    # INPUT             : None
    # RETURNS           : Returns true if settings match
    def verify_system_time_firewall(self):
        try:
            logger.info("Verifying System Time Settings in the firewall")
            data = time_obj.show_time()
            logger.info(data)
            data['time']['time_zone'] = data['time']['time_zone'].lower()
            self.timeZone = self.timeZone.lower()
            effective_json = data['time']
            self.json_compare(effective_json, "time_zone", self.timeZone)
            self.json_compare(effective_json, "daylight_savings", self.AutoAdjustClock)
            self.json_compare(effective_json, "universal", self.displayUTCinLogs)
            self.json_compare(effective_json, "international_format", self.displayDateInternational)
            self.json_compare(effective_json, "only_custom_ntp", self.onlyCustomNTP)
            self.json_compare(effective_json, "use_ntp", self.setTimeUsingNTP)
            updateInterval = int(self.updateInterval)
            self.json_compare(effective_json, "ntp_update_interval", updateInterval)            
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
            Assertion.assert_equal(flag, 0, 'Firewall verification failed')   
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Checks the existence of the ntp server on UI
    # INPUT             : NTP Server(optional)
    # RETURNS           : Returns true if the NTP server exists
    def does_ntp_server_exist(self, ntpServerName=None):
        try:
            if ntpServerName is None:
                ntpServerName = self.ntpServerName
            self.ui_helper.search_string(ntpServerName)
            self.ui_helper.click_refresh_icon()
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[text()='"+ntpServerName+"']"):
                logger.info("NTP Server "+ntpServerName+" exists")
                return True
            else:
                logger.info("NTP server does not exist")
                return False
        except Exception as e:
            logger.info(e)

    # FUNCTIONALITY     : Checks the existence of the ntp server by API
    # INPUT             : None
    # RETURNS           : Returns true if the NTP server exists
    def verify_ntp_server_firewall(self):
        try:
            logger.info("Verifying in the firewall")
            data = time_obj.show_ntp_server()
            logger.info(data)
            if self.ntpServerName == 'CancelButtonTest':
                if data['time'] == {}:
                    logger.info("NTP server: CancelButtonTest not found in the firewall as expected") 
                    return True
                else:
                    logger.info("Found NTP server: CancelButtonTest in the firewall unexpected")
                    return False  
            else:
                if self.ntpServerName == data['time']['ntp_server'][0]['name']:
                    logger.debug2("Data of the NTP servers from the firewall : " + json.dumps(data))
                    return True
                else:
                    logger.info("Target NTP server not found in the firewall ")
                    return False               
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Configuring parameters on System Time Settings tab
    # INPUT             : None
    # RETURNS           : None
    def configure_system_time_settings(self):
        try:
            self.navigation.navigate_to_system_time_settings_section()
            logger.info("Configure - System- Time Settings")
            if hasattr(self, 'setTimeUsingNTP'):
                logger.debug("Configure - Seting Time Using NTP \t: " + str(self.setTimeUsingNTP))
                self.ui_helper.configure_toggle_button('Set time automatically using NTP', self.setTimeUsingNTP)
            if hasattr(self, 'timeZone'):
                logger.debug("Configure - Seting Time Zone \t: " + str(self.timeZone))
                self.ui_helper.select_drop_down_value("Time Zone", self.timeZone)
            if hasattr(self, 'AutoAdjustClock'):
                logger.debug("Configure - Automatically Adjust Clock For Daylight Saving Time \t: " + str(self.AutoAdjustClock))
                self.ui_helper.configure_toggle_button('Automatically adjust clock for daylight saving time', self.AutoAdjustClock)
            if hasattr(self, 'displayUTCinLogs'):
                logger.debug("Configure - Display UTC In Logs \t: " + str(self.displayUTCinLogs))
                self.ui_helper.configure_toggle_button('Display UTC in logs (instead of local time)', self.displayUTCinLogs)
            if hasattr(self, 'displayDateInternational'):
                logger.debug("Configure - Display Date In International Format \t: " + str(self.displayDateInternational))
                self.ui_helper.configure_toggle_button('Display date in International format', self.displayDateInternational)
            if hasattr(self, 'onlyCustomNTP'):
                logger.debug("Configure - Only Using Custom NTP Servers \t: " + str(self.onlyCustomNTP))
                self.ui_helper.configure_toggle_button('Only use custom NTP servers', self.onlyCustomNTP)
            if hasattr(self, 'updateInterval'):
                logger.debug("Configure - Update Interval Every \t" + str(self.updateInterval) + "\tminutes")
                self.ui_wrapper.clear_text_field('name', 'Update Interval every')
                self.ui_helper.configure_text_field('Update Interval every', self.updateInterval)

            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Configuring System Time Settings Tab Failed")

    # FUNCTIONALITY     : Test the limitation of update interval textbox
    # INPUT             : minimum/maximum
    # RETURNS           : None
    def neg_configure_updateInterval_textbox(self, range_value):
        try:
            if range_value == "minimum":
                updateInterval = self.updateInterval_1
            else:
                updateInterval = self.updateInterval_2
            self.navigation.navigate_to_system_time_settings_section()          
            logger.info("Configure - Update Interval Every \t" + str(updateInterval) + "\tminutes")
            self.ui_wrapper.clear_text_field('name', 'Update Interval every')
            self.ui_helper.configure_text_field('Update Interval every', updateInterval)
            self.ui_helper.submit_page()
            self.ui_helper.compare_error_message("Out of bounds condition.")
            self.ui_helper.accept_alert()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Configuring updateInterval textbox Failed")

    # FUNCTIONALITY     : Test all values of time zone dropdown box
    # INPUT             : value
    # RETURNS           : None
    def configure_timezone_dropdown_box(self):
        try:
            self.navigation.navigate_to_system_time_settings_section()
            logger.info(self.timeZone_1)
            logger.info(self.timeZone_2)
            logger.info("Configure - Seting Time Zone \t: " + str(self.timeZone_1))
            self.ui_helper.select_drop_down_value("Time Zone", self.timeZone_1)
            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            logger.info("Setting Time Zone to: " + str(self.timeZone_1) + "succeed")
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Configuring timezone dropdown box Failed")
    
    # FUNCTIONALITY     : Configure NTP server  
    # INPUT             : None
    # RETURNS           : None
    def configure_ntp_server(self):
        try:
            if hasattr(self,'ntpServerName'):
                self.ui_wrapper.clear_text_field('name', 'NTP Server')
                self.ui_helper.configure_text_field('NTP Server', self.ntpServerName)
                if self.ntpAuthType == "MD5":
                    self.ui_helper.select_drop_down_value("NTP Auth Type", self.ntpAuthType)
                    self.ui_helper.configure_text_field('Trust Key No', self.trustKey)
                    self.ui_helper.configure_text_field('Key Number', self.keyNumber)
                    self.ui_helper.configure_text_field('Password', self.NTPPassWord)
                if self.ntpServerName == "CancelButtonTest":
                    self.ui_helper.cancel_page()
                else:
                    self.ui_wrapper.click_element('xpath', '//div/button[text()="Add"]')
                    self.ui_helper.click_close_icon()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Edit NTP Server Failed")

    # FUNCTIONALITY     : Delete the NTP server
    # INPUT             : NTP server(optional)
    # RETURNS           : None
    def delete_ntp_server(self, ntpServerName=None):
        try:
            self.navigation.navigate_to_system_ntp_servers_section()
            logger.info("Deleting the NTP server ")
            if ntpServerName is None:
                ntpServerName = self.ntpServerName
            if self.does_ntp_server_exist(ntpServerName):
                self.ui_helper.click_on_delete_element_after_hovering(ntpServerName)
                if self.does_ntp_server_exist(ntpServerName):
                    logger.info("NTP server deleted failed")
                else:
                    logger.info("NTP server deleted successfully")
            else:
                logger.info("NTP server need to delete does not exist")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete NTP server failed")

    def edit_system_time_settings(self):
        self.navigation.navigate_to_system_time_settings_section()
        self.configure_system_time_settings()
        self.verify_system_time_firewall()
        
    def create_ntp_server(self):
        self.navigation.navigate_to_system_ntp_servers_section()
        if self.does_ntp_server_exist():
            self.delete_ntp_server()   
        logger.info("Adding a ntp server: " + str(self.ntpServerName))
        self.ui_helper.click_add_icon()
        self.configure_ntp_server()
        if self.ntpServerName == 'CancelButtonTest':
            self.ui_helper.click_refresh_icon()
            self.verify_ntp_server_firewall()
        else:
            self.ui_helper.wait_for_success_banner()
            self.ui_helper.click_refresh_icon()
            self.verify_ntp_server_firewall()

    # FUNCTIONALITY     : Edit a NTP server
    # INPUT             : None
    # RETURNS           : None      
    def edit_ntp_server(self):
        self.navigation.navigate_to_system_ntp_servers_section()
        if self.does_ntp_server_exist():
            self.ui_wrapper.click_element('class', 'icon-close')
            logger.info("Editing the ntp server from:"+ str(self.ntpServerName) + " to:" + str(self.ntpServerName2))
            self.ui_helper.click_on_edit_element_after_hovering(self.ntpServerName)
            self.ntpServerName = self.ntpServerName2
            self.configure_ntp_server()
            self.ui_helper.wait_for_success_banner()
            self.ui_helper.click_refresh_icon()
            self.verify_ntp_server_firewall()
