from ast import Param
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

    @repeat_method(15)
    def test_02_Restore_Remote_FW(self):
        logger.info('Restore Remote FW...')
        path = '/SWIFT4.0/TESTS/python_SonicOS/common_lib/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN5 -if=X1 -zone=WAN -ip={} -restore=1'.\
              format(path, Params.testbed, REMOTEX1)

        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(REMOTEX1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')

        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")

    def test_03_enable_sso_by_radius_accounting(self):
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
        rc =  user_sso_obj.config_sso_base_settings(**edit)
        rc &= user_sso_obj_remote.config_sso_base_settings(**edit)
        Assertion.assert_equal(rc, True, "ERR: test_02_enable_sso_by_radius_accounting failed")

    @repeat_method(5)
    def test_04_register_fw(self):
        license_obj = LicenseCli(fw_cli)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

