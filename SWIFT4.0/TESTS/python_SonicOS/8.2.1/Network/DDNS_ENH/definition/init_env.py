from definition.settings import *

class  TestInitConfig(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_01_config_interface(self):
        logger.info('-'*10+'config x1  ip'+'-'*10)
        rc = interface.config_interface(**Parameter.x1_static_opt)
        Assertion.assert_equal(rc, True, 'config x1  ip Failed.')

    @repeat_method(5)
    def test_00_02_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_00_03_config_doamin_name(self):
        res = PC1.send_commands(['echo 13.0.0.168 shautomation.changeip.net >> /etc/hosts','cat /etc/hosts'])
        logger.info(res)
        if '13.0.0.168 shautomation.changeip.net' in res:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: config host doamin failed")

