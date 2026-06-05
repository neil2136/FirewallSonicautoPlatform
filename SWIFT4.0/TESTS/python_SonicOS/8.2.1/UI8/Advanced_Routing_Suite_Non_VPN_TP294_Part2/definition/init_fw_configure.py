from definition.settings import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    @repeat_method(5)
    def test_01_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: register fw failed!!")
