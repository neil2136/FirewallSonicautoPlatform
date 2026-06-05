from modules.UI7.common_require import *
from modules.API.system import ScheduleApi

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from utm import Firewall
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
schedule_obj = ScheduleApi(fw)

class ScheduleObjects:
    # FUNCTIONALITY     : Checks the schedule object in the firewall
    # INPUT             : None
    # RETURNS           : Returns true if settings match
    def verify_schedule_object_firewall(self):
        try:
            logger.info("Verifying Schedule Object in Firewall")
            if self.scheduleObjectName == "test-cancel-button":
                return True
            data = schedule_obj.get_schedule(self.scheduleObjectName)
            logger.info(data)
            if data['schedules'][0]['name'] == self.scheduleObjectName:
                logger.info("Target schedule object exist in firewall!")
                return True
            else:
                logger.info("Target schedule object not exist in firewall!")
                return False
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")

    # FUNCTIONALITY     : Checks the existence of the schedule object on UI
    # INPUT             : name of schedule object(optional)
    # RETURNS           : Returns true if the schedule object exists
    def does_schedule_object_exist(self, scheduleObjectName=None):
        try:
            if scheduleObjectName is None:
                scheduleObjectName = self.scheduleObjectName
            if scheduleObjectName == "test-cancel-button":
                if self.ui_wrapper.does_element_exist_now('xpath', 
                                                          "//div[text()='"+scheduleObjectName+"']"):
                    logger.info("Schedule Object "+scheduleObjectName+" unexpected exists")
                    return False
                else:
                    logger.info("Schedule Object does not exist as expected")
                    return True
            if self.ui_wrapper.does_element_exist_now('xpath', "//div[text()='"+scheduleObjectName+"']"):
                logger.info("Schedule Object "+scheduleObjectName+" exists")
                return True
            else:
                logger.info("Schedule Object does not exist")
                return False
        except Exception as e:
            logger.info(e)

    # FUNCTIONALITY     : Config a schedule object
    # INPUT             : None
    # RETURNS           : None
    def configure_schedule_object(self):
        try:
            if hasattr(self,'scheduleObjectName'):
                self.ui_helper.configure_text_field('Schedule Name', self.scheduleObjectName)             
                if self.scheduleObjectType == "once":
                    self.once_part_configuration()
                if self.scheduleObjectType == "recurring":
                    self.ui_wrapper.set_radio_button('class', 'create-schedule__schedule-recurring')
                    self.recurring_part_configuration()
                if self.scheduleObjectType == "mixed":
                    self.ui_wrapper.set_radio_button('class', 'create-schedule__schedule-mixed')
                    self.once_part_configuration()
                    self.recurring_part_configuration()
                if self.scheduleObjectType == "recurring_multi_list":
                    self.ui_wrapper.set_radio_button('class', 'create-schedule__schedule-recurring')
                    logger.info("Selecting Day...")
                    if self.scheduleSunday == True:
                        self.ui_helper.configure_toggle_button('Sunday', str(self.scheduleSunday))
                        self.clock_select_for_recurring()
                    if self.scheduleMonday == True:
                        self.ui_helper.configure_toggle_button('Monday', str(self.scheduleMonday))
                        self.clock_select_for_recurring()
                    if self.scheduleTuesday == True:
                        self.ui_helper.configure_toggle_button('Tuesday', str(self.scheduleTuesday))
                        self.clock_select_for_recurring()
                    if self.scheduleWednesday == True:
                        self.ui_helper.configure_toggle_button('Wednesday', str(self.scheduleWednesday))
                        self.clock_select_for_recurring()
                    if self.scheduleThursday == True:
                        self.ui_helper.configure_toggle_button('Thursday', str(self.scheduleThursday))
                        self.clock_select_for_recurring()
                    if self.scheduleFriday == True:
                        self.ui_helper.configure_toggle_button('Friday', str(self.scheduleFriday))
                        self.clock_select_for_recurring()
                    if self.scheduleSaturday == True:
                        self.ui_helper.configure_toggle_button('Saturday', str(self.scheduleSaturday))
                        self.clock_select_for_recurring()
                if self.scheduleObjectName == "test-cancel-button":
                    self.ui_helper.cancel_page()
                else:
                    self.ui_helper.submit_page()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Config Schedule object Failed")

    # FUNCTIONALITY     : Config a schedule object on once part
    # INPUT             : None
    # RETURNS           : None
    def once_part_configuration(self):
        try:           
            if self.scheduleObjectType == "once" or self.scheduleObjectType == "mixed":
                self.ui_wrapper.click_element('class', "icon-calendar-date-range")
                logger.info("Selecting time range...")
                if hasattr(self,'scheduleObjectName_1'):
                    self.scheduleStartMonth = self.scheduleStartMonth_1
                self.range_select_for_once()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Configure once part Failed")

    # FUNCTIONALITY     : Config a schedule object on recurring part
    # INPUT             : None
    # RETURNS           : None
    def recurring_part_configuration(self):
        try:          
            logger.info("Selecting Day...")
            if hasattr(self,'scheduleButtonSeleteAll'):
                self.ui_helper.configure_toggle_button('Select All', str(self.scheduleButtonSeleteAll))
            else:
                if self.scheduleSunday == True:
                    self.ui_helper.configure_toggle_button('Sunday', str(self.scheduleSunday))
                if self.scheduleMonday == True:
                    self.ui_helper.configure_toggle_button('Monday', str(self.scheduleMonday))
                if self.scheduleTuesday == True:
                   self.ui_helper.configure_toggle_button('Tuesday', str(self.scheduleTuesday))
                if self.scheduleWednesday == True:
                    self.ui_helper.configure_toggle_button('Wednesday', str(self.scheduleWednesday))
                if self.scheduleThursday == True:
                    self.ui_helper.configure_toggle_button('Thursday', str(self.scheduleThursday))
                if self.scheduleFriday == True:
                    self.ui_helper.configure_toggle_button('Friday', str(self.scheduleFriday))
                if self.scheduleSaturday == True:
                    self.ui_helper.configure_toggle_button('Saturday', str(self.scheduleSaturday))
            self.clock_select_for_recurring()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Configure recurring part Failed")

    # FUNCTIONALITY     : Add a schedule object
    # INPUT             : None
    # RETURNS           : None
    def create_schedule_object(self):
        try:
            self.navigation.navigate_to_schedule_object_section()
            if self.scheduleObjectName != "test-cancel-button":
                if self.does_schedule_object_exist(self.scheduleObjectName):
                    self.delete_schedule_object()
            logger.info("Adding a schedule object: " + str(self.scheduleObjectName))
            self.ui_helper.click_add_icon()
            self.ui_wrapper.wait_for_text("Add Schedule")
            self.configure_schedule_object()
            if self.scheduleObjectName != "test-cancel-button":
                self.ui_helper.wait_for_success_banner()
                self.click_refresh_icon()
            self.does_schedule_object_exist(self.scheduleObjectName)
            self.verify_schedule_object_firewall()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Add Schedule object Failed")

    # FUNCTIONALITY     : Edit a schedule object
    # INPUT             : None
    # RETURNS           : None
    def edit_schedule_object(self):
        try:
            self.navigation.navigate_to_schedule_object_section()
            logger.info("Editing schedule object name from"
                       ": " + str(self.scheduleObjectName) + " to " + str(self.scheduleObjectName_1))
            if self.does_schedule_object_exist(self.scheduleObjectName):
                self.ui_helper.click_on_edit_element_after_hovering(self.scheduleObjectName)
                self.ui_wrapper.wait_for_text("Edit this Schedule")
                self.ui_helper.configure_text_field('Schedule Name', self.scheduleObjectName_1)
                if self.scheduleObjectType == "once":
                    self.once_part_configuration()
                if self.scheduleObjectType == "recurring":
                    self.scheduleSunday     = True
                    self.scheduleMonday     = False
                    self.scheduleTuesday    = False
                    self.scheduleWednesday  = False
                    self.scheduleThursday   = False
                    self.scheduleFriday     = False
                    self.scheduleSaturday   = False
                    self.recurring_part_configuration()
                    self.ui_helper.submit_page()
                    self.ui_helper.accept_alert()
                if self.scheduleObjectType == "recurring_multi_list":
                    self.ui_wrapper.move_to_the_element('xpath', '//span[text()="Tue 01:02 to 01:07"]')
                    self.ui_wrapper.click_element('xpath', "//span[text()='Tue 01:02 to 01:07']"
                                                           "/following::*[contains(@class,'icon-trash')]")
                if self.scheduleObjectType == "mixed":
                    self.once_part_configuration()
                    self.scheduleSunday     = False
                    self.scheduleMonday     = False
                    self.scheduleTuesday    = True
                    self.scheduleWednesday  = False
                    self.scheduleThursday   = False
                    self.scheduleFriday     = False
                    self.scheduleSaturday   = False
                    self.recurring_part_configuration()
                    self.ui_helper.submit_page()
                    self.ui_helper.accept_alert()

                self.ui_helper.submit_page()
                self.ui_helper.wait_for_success_banner()
                self.click_refresh_icon()
                self.does_schedule_object_exist(self.scheduleObjectName_1)
                self.scheduleObjectName = self.scheduleObjectName_1
                self.verify_schedule_object_firewall()
        except Exception as err:
            logger.err(str(err))
            Assertion.fail("Add Schedule object Failed")

    # FUNCTIONALITY     : Select date and time range for once object
    # INPUT             : None
    # RETURNS           : None
    def range_select_for_once(self):
        try:
            selector = self.get_selenium_selector("class")
            logger.info("Action - config on date range")
            self.browser.find_elements(selector, 'sw-flexbox-center--items')[0].click()
            self.ui_wrapper.click_element('xpath', '//div[contains(@class,"sw-datepicker__popup")]'
                                                   '/div[1]/div[2]/span[text()="' + self.scheduleStartMonth + '"]')
            self.ui_wrapper.click_element('xpath', '//div[contains(@class,"sw-datepicker__popup")]'
                                                   '/div[1]/div[3]/span[text()=15]')
            self.ui_wrapper.click_element('xpath', '//div[contains(@class,"sw-datepicker__popup")]'
                                                   '/div[1]/div[3]/span[text()=20]')
            logger.info("Action - config on time range")
            Action = ActionChains(self.browser)
            dragElement_start_hour = self.browser.find_elements(selector, 'sw-slider__thumb')[0]
            Action.drag_and_drop_by_offset(dragElement_start_hour,45,200).perform()
            #dragElement_start_min = self.browser.find_elements(selector, 'sw-slider__thumb')[1]
            #Action.drag_and_drop_by_offset(dragElement_start_min,45,210).perform()
            #dragElement_start_sec = self.browser.find_elements(selector, 'sw-slider__thumb')[2]
            #Action.drag_and_drop_by_offset(dragElement_start_sec,45,220).perform()
            #dragElement_end_hour = self.browser.find_elements(selector, 'sw-slider__thumb')[3]
            #Action.drag_and_drop_by_offset(dragElement_end_hour,45,230).perform()
            #dragElement_end_min = self.browser.find_elements(selector, 'sw-slider__thumb')[4]
            #Action.drag_and_drop_by_offset(dragElement_end_min,45,240).perform()
            #dragElement_end_sec = self.browser.find_elements(selector, 'sw-slider__thumb')[5]
            #Action.drag_and_drop_by_offset(dragElement_end_sec,45,250).perform()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to clicking on month select")

    # FUNCTIONALITY     : Add time range for recurring object
    # INPUT             : None
    # RETURNS           : None
    def clock_select_for_recurring(self):
        try:
            selector = self.get_selenium_selector("class")
            logger.info("Action - config on clock: Start Time")
            self.browser.find_elements(selector, 'icon-calendar-date')[0].click()
            dragElement_start_hour = self.browser.find_elements(selector, 'sw-slider__thumb')[0]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_start_hour,5,0).perform()
            dragElement_start_min = self.browser.find_elements(selector, 'sw-slider__thumb')[1]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_start_min,5,0).perform()
            dragElement_start_sec = self.browser.find_elements(selector, 'sw-slider__thumb')[2]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_start_sec,5,0).perform()
            logger.info("Action - config on clock: End Time")
            self.browser.find_elements(selector, 'icon-calendar-date')[1].click()
            dragElement_end_hour = self.browser.find_elements(selector, 'sw-slider__thumb')[0]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_end_hour,10,0).perform()
            dragElement_end_min = self.browser.find_elements(selector, 'sw-slider__thumb')[1]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_end_min,20,0).perform()
            dragElement_end_sec = self.browser.find_elements(selector, 'sw-slider__thumb')[2]
            ActionChains(self.browser).drag_and_drop_by_offset(dragElement_end_sec,30,0).perform()
            self.ui_wrapper.click_element('xpath', '//div/button[text()="Add"]')
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Failed to clicking on month select")

    # FUNCTIONALITY     : Delete ScheDule Object
    # INPUT             : target schedule object
    # RETURNS           : None
    def delete_schedule_object(self, scheduleObjectName=None):
        try:
            self.navigation.navigate_to_schedule_object_section()
            logger.info("Deleting the schedule object")
            if scheduleObjectName is None:
                scheduleObjectName = self.scheduleObjectName
            if self.does_schedule_object_exist(scheduleObjectName):
                self.ui_wrapper.move_to_the_element('xpath', "//div[text()='" + scheduleObjectName + "']")
                self.ui_wrapper.click_element('xpath', "//*[text()='" + scheduleObjectName + "']"
                                                       "/following::*[contains(@class,'icon-trash')]")
                self.ui_helper.accept_alert()
                self.ui_helper.accept_alert()
                if self.does_schedule_object_exist(scheduleObjectName):
                    logger.info("Delete schedule object failed")
                else:
                    logger.info("Delete schedule object successfully")
            else:
                logger.info("Schedule object need to delete does not exist")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete schedule object failed")

    # FUNCTIONALITY     : Delete ScheDule Object
    # INPUT             : target schedule object
    # RETURNS           : None
    def delete_all_schedule_objects(self):
        try:
            self.navigation.navigate_to_schedule_object_section()
            logger.info("Deleting all the custom schedule objects")
            if self.does_schedule_object_exist(self.scheduleObjectName) and \
                    self.does_schedule_object_exist(self.scheduleObjectName_1):
                selector = self.get_selenium_selector("class")
                self.browser.find_elements(selector, 'icon-checkmark')[0].click()
                self.ui_helper.click_delete_icon()
                self.ui_helper.accept_alert()
                self.ui_helper.accept_alert()
                if self.does_schedule_object_exist(self.scheduleObjectName) or \
                        self.does_schedule_object_exist(self.scheduleObjectName_1):
                    logger.info("Delete schedule objects failed")
                else:
                    logger.info("Delete schedule objects successfully")
            else:
                logger.info("Schedule objects need to delete does not exist")
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Delete schedules object failed")
