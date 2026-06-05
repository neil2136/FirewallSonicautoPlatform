from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    @repeat_method(5)
    def test_02_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestConfigTB(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = "config pc as ftp server"

    def test_01_config_ftp(self):
        out= PC1.send_commands(ftp_commands)
        rc = True if "#root" in out and 'userlist_deny=NO' in out else False
        Assertion.assert_not_equal(rc, False, "ERR: config FTP server conf and userlist failed")

    def test_02_active_ftp_server(self):
        out = PC1.send_commands(active_ftp)
        rc = True if "active (running)" in out else False
        Assertion.assert_not_equal(rc, False, "ERR: active ftp server failed")
        


  