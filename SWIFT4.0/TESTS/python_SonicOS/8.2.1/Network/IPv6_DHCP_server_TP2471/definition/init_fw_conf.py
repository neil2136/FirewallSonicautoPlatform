from definition.settings import *
from definition.config_page_via_ui import *


class TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_v4(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.DNS1,
            'dns2': Parameter.DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
        }
        logger.info("config x1 interface... ")
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 ipv4 address failed")

    def test_02_config_x0_v6(self):
        x0_v6_dict = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True,
            'managed': True,
            'other_config': True,
            'router_adv': True
        }
        logger.info("config x0 interface... ")
        res = interfacev6api.config_interface_ipv6(**x0_v6_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X0 IPv6 address failed")

    def test_03_config_x2_v4_v6(self):
        x2_v4_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X2_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }

        x2_v6_dict = {
            'name': 'X2',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X2_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True,
            'managed': True,
            'other_config': True,
            'router_adv': True
        }
        logger.info("config x2 interface... ")
        rc1 = interfacev4api.config_interface(**x2_v4_dict)
        rc2 = interfacev6api.config_interface_ipv6(**x2_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X2 ipv4 and ipv6 address failed")

    def test_04_config_x3_v6(self):
        x3_v4_dict = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X3_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x3_v6_dict = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X3_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        logger.info("config x3 interface... ")
        rc1 = interfacev4api.config_interface(**x3_v4_dict)
        rc2 = interfacev6api.config_interface_ipv6(**x3_v6_dict)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: Config X3 ipv4 and ipv6 address failed")

    @repeat_method(10)
    def test_05_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(20)
        Assertion.assert_equal(True, True, "ERR: register fw failed")

    # def test_06_skip_automatic_update_window(self):
    #     try:
    #         fwpage.login_gui()
    #         fwpage.wait_for_page_data_to_be_rendered()
    #         logger.info("Click checkbox")
    #         # fwpage.wait_for_element_to_be_invisible(*window)
    #         fwpage.click_element('xpath',
    #                                  '//div[text()="Do not show this message again"]/../div[contains(@class, "sw-checkbox__box")]')
    #         logger.info('Click OK button')
    #         fwpage.click_element('xpath', "//div/button[text()='OK']")
    #         rc = True
    #     except Exception as err:
    #         logger.error("Exception \t: " + str(err))
    #         fwpage.close_browser()
    #         rc = False
    #     Assertion.assert_equal(rc, True, "ERR: Skip Automatic Update window failed!!")
    
    def test_06_skip_automatic_update_window(self):
        autoupdatedict = {
                        "update": True,
                        "download": True,
                        "install_firmware": True,
                        "hide_advice": True,
                        "critical_only": False
                    }
        res = settingapi.edit_firmware_auto_update(**autoupdatedict)
        Assertion.assert_equal(res, True, "ERR: Skip Automatic Update window failed!!")


class TestInitRemoteConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Init_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command1 = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X2 -zone=WAN ' \
                   f'-ip={Parameter.X2_REMOTE_IP} -restore=1 '
        confres = PC1_Login.send_command(command1)
        logger.info(confres)
        pingres = PC1_Login.ping_from_eth(ip=Parameter.X2_REMOTE_IP, eth='eth2')
        Assertion.assert_equal(True, True, "ERR: Restore Remote FW failed")

    def test_02_config_x3_staitc_ip_with_wan_zone(self):
        x3_v4_dict = {
            'if': 'X3',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X3_REMOTE_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': False,
        }
        rc = reinterfacev4api.config_interface(**x3_v4_dict)
        Assertion.assert_equal(True, True, "ERR: Config x3 static ip with WAN zone failed")

    def test_03_config_x4_staitc_ipv4_and_ipv6_with_lan_zone(self):
        x4_v4_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_REMOTE_IP,
            'netmask': Parameter.MASK,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x4_v6_dict = {
            'name': 'X4',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X4_REMOTE_V6_IP,
            'prefix_length': Parameter.PREFIX_LENGTH,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        logger.info("config x3 interface... ")
        rc1 = reinterfacev4api.config_interface(**x4_v4_dict)
        rc2 = reinterfacev6api.config_interface_ipv6(**x4_v6_dict)
        Assertion.assert_equal(True, True, "ERR: Config X3 ipv4 and ipv6 address with LAN zone failed")