from settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        res = interface_obj.config_interface(**x1_static)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_import_sslcert(self):
        rc = certapi.import_cert_local(cert_path='@' + certpath, name='dovecot_1k', password='password')
        Assertion.assert_equal(rc, True, "ERR: Import SSL Certificate into Firewall failed.")

    def test_03_add_local_users(self):
        rc = userlocalcli.add_local_user(**local_user_dict)
        Assertion.assert_equal(rc, True, "ERR: add local users into Firewall failed.")
