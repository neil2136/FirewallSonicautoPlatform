from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"

    def test_01_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': DUTX1,
            'netmask': MASK,
            'gateway': Gateway,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
        }
        rc = interface_ipv4.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 failed")

    def test_02_enable_sso_by_radius_accounting(self):
        logger.info('Enable SSO by RADIUS accounting......')
        edit = {
            "user": {
                "sso": {
                    "method": {
                        "radius_accounting": True,
                    }
                }
            }
        }
        rc = user_sso_obj.config_sso_base_settings(**edit)
        Assertion.assert_equal(rc, True, "ERR: test_02_enable_sso_by_radius_accounting failed")

    @repeat_method(5)
    def test_03_register_fw(self):
        try:
            license_obj = LicenseCli(fw_cli)
            rc = license_obj.register("online")
            Assertion.assert_equal(rc, True, "ERR: register fw failed")
        except Exception as e:
            logger.info(e)
