from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed!!")

    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed!!")

    def test_03_admin_logout_timeout(self):
        admin = {
            "multiple_admin": True,
            "idle_logout_time": 5000
        }
        rc = admin_api.conf_admin(**admin)
        Assertion.assert_equal(rc, True, "ERR: config admin logout timeout failed")

    # skip Automated Update window ==> support over 8.0.0 build
    # @repeat_method(3)
    # def test_04_skip_automatic_update_window(self):
    #     try:
    #         fw_page_ui.login_ui()
    #         fw_page_ui.wait_for_page_data_to_be_rendered()
    #         logger.info('Config - Select checkbox "Do not show this message again"')
    #         checkbox = ('xpath', '//div[text()="Do not show this message again"]/../div[contains(@class, "sw-checkbox__box")]')
    #         fw_page_ui.click_element(*checkbox)
    #         fw_page_ui.is_element_selected(*checkbox)
    #         logger.info('Action - Click button "OK"')
    #         fw_page_ui.click_element('xpath', "//div/button[text()='OK']")
    #         window = ('xpath', '//*[text()="Automatic Update Window"]')
    #         fw_page_ui.wait_for_element_to_be_invisible(*window)
    #         return True
    #     except Exception as err:
    #         logger.error("Exception \t: " + str(err))
    #         fw_page_ui.close_browser()
    #         rc = False
    #     Assertion.assert_equal(rc, True, "ERR: Skip Automatic Update window failed!!")

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
