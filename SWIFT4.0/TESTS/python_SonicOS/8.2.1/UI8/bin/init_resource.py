from bin.global_var import *


class FWConfigure(Test):
    uuid = 'NonTC'
    description = 'Initialize FW Configure'
    goto_teardown = True

    def test_01_config_X1(self):
        output = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(output, True, "ERR: Config X1 to static failed!!")

    # @repeat_method(10)
    # def test_02_register_fw(self):
    #     output = license_cli.register("online")
    #     if not rc:
    #         time.sleep(20)
    #     Assertion.assert_equal(output, True, "ERR: register fw failed!!")

    def test_03_admin_logout_timeout(self):
        admin = {
            "multiple_admin": True,
            "idle_logout_time": 5000
        }
        output = admin_api.conf_admin(**admin)
        Assertion.assert_equal(output, True, "ERR: config admin logout timeout failed")

    # @repeat_method(3)
    # def test_04_skip_automatic_update_window(self):
    #     try:
    #         fw_page_ui.login_ui()
    #         fw_page_ui.login_ui_with_head()
    #         fw_page_ui.wait_for_page_data_to_be_rendered()
    #         element_status = fw_page_ui.does_element_exist_now('xpath', '//*[text()="Do not show this message again"]')
    #         logger.info(f'check auto update window result: {element_status}')
    #         if element_status:
    #             logger.info(f'auto update window not show...')
    #             logger.info('Config - Select checkbox "Do not show this message again"')
    #             checkbox = (
    #                 'xpath',
    #                 '//div[text()="Do not show this message again"]/../div[contains(@class, "sw-checkbox__box")]')
    #             fw_page_ui.click_element(*checkbox)
    #             fw_page_ui.is_element_selected(*checkbox)
    #             logger.info('Action - Click button "OK"')
    #             fw_page_ui.click_element('xpath', "//div/button[text()='OK']")
    #             window = ('xpath', '//*[text()="Automatic Update Window"]')
    #             fw_page_ui.wait_for_element_to_be_invisible(*window)
    #             logger.info(f'configure the do not show this message successful.')
    #             output = True
    #         else:
    #             logger.info('auto update window not in current page, not need configure.')
    #             output = True
    #     except Exception as err:
    #         logger.error("Exception \t: " + str(err))
    #         output = False
    #         fw_page_ui.close_browser()
    #     Assertion.assert_equal(output, True, "ERR: Skip Automatic Update window failed!!")

    def test_05_skip_automatic_update_window(self):
        autoupdatedict = {
            "update": True,
            "download": True,
            "install_firmware": True,
            "hide_advice": True,
            "critical_only": False
        }
        res = setting_api.edit_firmware_auto_update(**autoupdatedict)
        Assertion.assert_equal(res, True, "ERR: Skip Automatic Update window failed!!")
