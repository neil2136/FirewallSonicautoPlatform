from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_X1_Interface(self):
        x1_static = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'gateway': '12.12.1.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_import_CA(self):
        rc = False
        pc1_login.send_command(f'\cp {cert_file} /tmp/sonicauto.cer')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        print(res.stdout)
        if 'sonicauto.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca_api.import_ca_cert(file='/tmp/sonicauto.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import ca file failed!!")
    
    def test_04_restart_fw_to_take_changes_effect(self):
        rc = restart_api.restart_now()
        Assertion.assert_equal(rc, True, "ERR: restart fw failed!!")
    
    def test_05_skip_automatic_update_window(self):
        opt = {
            "auto": {
                "update": True,
                "download": True,
                "critical_only": True,
                "install_firmware": True,
                'hide_advice': True
            }
        }
        rc = settings_api.edit_firmware(**opt)
        Assertion.assert_equal(rc, True, "ERR: Skip Automatic Update window failed!!")

    def test_06_create_idp(self):
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")
    
    def test_07_import_self_signed_cert(self):
        self_signed_cert = suite_path+'definition/2k-password.pfx'
        # cert_path="@" + certPath1k, name='dpi-ssl-client-1k', password='123456'
        rc = ca_api.import_cert_local(cert_path="@" +self_signed_cert, name='test', password='password')
        Assertion.assert_equal(rc, True, "ERR: import self-signed cert failed!!")
