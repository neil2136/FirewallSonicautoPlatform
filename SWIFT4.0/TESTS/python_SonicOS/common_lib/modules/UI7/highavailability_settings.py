from modules.UI7.common_require import *

class HighAvailabilitySettings:
    ''' HighAvailabilitySettings '''

    def __init__(self):
        self.common_attr = 'fw-mgmt-ftr-high-availability-settings'
        self.select_list = {
            'mode': ['class', self.get_class_name('__select-list')],
            'ctrl_if': ['class', self.get_class_name('__select-list')],
            'data_if': ['class', self.get_class_name('__select-list')]
        }
        self.toggles = {
            #'enable_stat_sync': ['name', 'cbEnableStatefulSynch'],
            #'enable_preempt_mode': ['name', 'cbEnablePreemptMode'],
            #'enable_encryption_ctrl': ['name', 'cbEnableEncryption'],
            #'enable_l3_mode': ['name', 'l3Mode'],
            'enable_stat_sync': ['class', self.get_class_name('__toggle-enable-sm1')],
            # 'generate_backup': ['class', self.get_class_name('__toggle-enable-sm2')],
            'enable_preempt_mode': ['class', self.get_class_name('__toggle-enable-sm3')],
            # 'enable_vmac': ['class', self.get_class_name('__toggle-enable-sm4')],
            'enable_encryption_ctrl': ['class', self.get_class_name('__toggle-enable-sm5')],
            'enable_l3_mode': ['class', self.get_class_name('__toggle-l3Mode')],
        }
        self.text_fields = {
            'sec_serial': ['name', 'textSecondarySerialNumber'],
            'pri_unit_ip': ['name', 'l3primaryUnitIP'],
            'pri_unit_gw': ['name', 'l3primaryUnitGateway'],
            'sec_unit_ip': ['name', 'l3secondaryUnitIP'],
            'sec_unit_gw': ['name', 'l3secondaryUnitGateway']
        }

    def get_class_name(self, sub_attr: str):
        return self.common_attr + sub_attr

    def get_all_drop_list(self):
        self.navigation.navigate_to_ha_settings_section()
        objs = self.ui_wrapper.get_elements('class', 'fw-mgmt-ftr-high-availability-settings__select-list')
        return objs

    def config_ha(self, **kwargs):
        self.navigation.navigate_to_ha_settings_section()
        drop_list = self.get_all_drop_list()
        mode = drop_list[0].text
        if mode == 'None' and 'mode' not in kwargs.keys():
            logger.error('Please specify HA mode first')
            Assertion.fail("Config HA failed.")
        if ('enable_l3_mode' in kwargs.keys() and kwargs['enable_l3_mode']) and 'pri_unit_ip' not in kwargs.keys():
            logger.error("L3 mode at leat needs primary unit IP to be set.")
            Assertion.fail("Config HA failed.")
        if 'mode' in kwargs.keys() and kwargs['mode'].lower() == 'none':
            try:
                self.ui_helper.select_obj_drop_down_value(drop_list[0], 'None')
                self.ui_wrapper.click_element('class', self.get_class_name('__button-update'))
                self.ui_helper.wait_for_success_alert()
            except Exception as err:
                logger.error("Exception \t: " + str(err))
                Assertion.fail("Config HA failed.")
        if 'mode' in kwargs.keys():
            self.ui_helper.select_obj_drop_down_value(drop_list[0], kwargs['mode'])
        for key in kwargs.keys():
            logger.info('========' + str(key) + '========')
            if key.lower() == 'mode':
                continue
            elif key.lower() == 'ctrl_if':
                logger.info('Config control interface: ' + str(kwargs[key]))
                self.ui_helper.select_obj_drop_down_value(drop_list[1], kwargs[key])
            elif key.lower() == 'data_if':
                logger.info('Config data interface: ' + str(kwargs[key]))
                self.ui_helper.select_obj_drop_down_value(drop_list[2], kwargs[key])
            elif key.lower() in self.toggles.keys():
                logger.info('Config toggle button: ' + key + ' ' + str(kwargs[key]))
                self.ui_wrapper.toggle_button(self.toggles[key][0], self.toggles[key][1], kwargs[key])
                self.ui_helper.wait_for_info_alert()
            elif key in self.text_fields.keys():
                logger.info('Config text field: ' + str(kwargs[key]))
                if self.ui_wrapper.is_element_enabled(self.text_fields[key][0], self.text_fields[key][1]):
                    self.ui_wrapper.clear_text_field(self.text_fields[key][0], self.text_fields[key][1])
                    self.ui_wrapper.set_text_field(self.text_fields[key][0], self.text_fields[key][1], kwargs[key])
                else:
                    logger.error(str(key) + " field is not enabled. Please check the page.")
            time.sleep(3)
        try:
            self.ui_wrapper.click_element('class', self.get_class_name('__button-update'))
            self.ui_helper.wait_for_success_alert()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Config HA failed.")