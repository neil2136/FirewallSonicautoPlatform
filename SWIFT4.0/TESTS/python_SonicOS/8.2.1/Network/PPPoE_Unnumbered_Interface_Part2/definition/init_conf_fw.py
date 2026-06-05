from definition.settings import *


class TestConfigFW(Test):
    uuid = "NonTC"
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_Config_X3(self):
        logger.info("config x3 interface... ")
        rc = interfaceapi.config_interface(**x3_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_04_add_snmp_config(self):
        logger.info("Add SNMP config")
        rc_gp = snmpapi.add_snmp_group(name=snmp_user_group)
        logger.info(f"Add SNMP group result = {rc_gp}")
        rc_user = snmpapi.snmp_user_add(**snmp_user_dict)
        logger.info(f"Add SNMP user result = {rc_user}")
        rc_acc = snmpapi.snmp_access_add(**snmp_acc_dict)
        logger.info(f"Add SNMP access result = {rc_acc}")
        rc = rc_gp and rc_user and rc_acc
        Assertion.assert_equal(rc, True, "ERR: Add SNMP config failed!")

    def test_05_enable_snmp(self):
        rc = []
        resp = snmpapi.show_snmp()
        if resp:
            snmp_v3 = resp["snmp"]
            snmp_v3["snmp3"]["mandatory"] = True
            rc_set = snmpapi.snmp_base_settings(**snmp_v3)
            rc_enable = snmpapi.enable_snmp()
            rc = [rc_set, rc_enable]
        Assertion.assert_equal(all(rc), True, "ERR: Enable snmp failed.")

    @repeat_method(10)
    def test_06_register_fw(self):
        logger.info("Sleep 20s before registering firewall")
        time.sleep(20)
        res = licensecli.register("online")
        Assertion.assert_equal(res, True, "ERR: Register fw failed")
