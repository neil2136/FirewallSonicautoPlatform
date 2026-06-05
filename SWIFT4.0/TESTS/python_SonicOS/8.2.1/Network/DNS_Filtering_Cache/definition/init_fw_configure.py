from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True


    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(5)
    def test_02_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")
