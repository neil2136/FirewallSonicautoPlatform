from definition.settings import *
from definition.utils import *


# path = '/logs/downloads/lezhang-1635491500072_sw_tz_370_eng.7.0.1-5018-P1710.bin.sig'
class Test_upgrade_previous_firmware_via_UI(Test):
    uuid = 'NonTC'
    goto_teardown = True
    def test_01_upgrade_previous_firmware_via_UI(self):
        upgraderes = upgrade_firmware_previous(Parameter.prebuild)
        if not upgraderes:
            upgrade_result_list.append(0)
        Assertion.assert_equal(upgraderes, True, "ERR: upgrade the old version failed")


class Test_check_configure_and_traffic_in_previous_firmware(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_add_nat_policy(self):
        addv4res = natpolicyconfapi.add_nat_policy(**nat_ipv4_dict)
        Assertion.assert_equal(addv4res, True, "ERR: add nat policy failed")

    @repeat_method(10)
    def test_02_traffic_check(self):
        time.sleep(20)
        res = hostconf.ping_from_eth(ip=Parameter.PC2_ETH0, eth='eth0')
        Assertion.assert_equal(res, True, "ERR: ping traffic check failed")


class Test_01_upgrade_current_firmware_via_UI(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = show_testcase_info(TESTPLAN,
                                     "01", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_upgrade_current_firmware(self):
        upgraderes = upgrade_firmware_current(Parameter.testbuild)
        Assertion.assert_equal(upgraderes, True, "ERR: upgrade the current version failed")


class Test_02_traffic_check_from_lan_to_wan(Test):
    if platform_name in uuid_dict.keys():
        uuid = uuid_dict[platform_name]
    else:
        uuid = False
        goto_teardown = True
    description = show_testcase_info(TESTPLAN, "02", description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(10)
    def test_02_traffic_check(self):
        time.sleep(20)
        res = hostconf.ping_from_eth(ip=Parameter.PC2_ETH0, eth='eth0')
        Assertion.assert_equal(res, True, "ERR: ping traffic check failed")


# check firewall type must march to the automation test bed.
class Test_03_platform_not_in_test_list(Test):
    uuid = False
    def test_00_check_platform(self):
        logger.info(f'platform: {platform_name} not in the valid list')
        Assertion.assert_equal(False, True, "ERR: this platform not fit for the platform upgrade test")
