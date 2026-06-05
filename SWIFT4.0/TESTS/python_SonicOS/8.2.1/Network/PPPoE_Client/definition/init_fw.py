from settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interfaceapi.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
