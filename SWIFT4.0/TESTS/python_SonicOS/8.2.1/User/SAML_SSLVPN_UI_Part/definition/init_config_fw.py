from definition.settings import *


class TestConfig_FW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1(self):
        x1_static = {
            'if': 'X1',
            'zone': "WAN",
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': "12.12.1.1",
            'dns1': Parameter.X1_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    def test_02_register_fw(self):
        for i in range(10):
            time.sleep(10)
            rc = license_cli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_x2(self):
        x2_static = {
            'if': 'X2',
            'zone': "LAN",
            'mode': 'static',
            'ip': '13.13.1.168',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_http': True,
            'user_https': True,
        }
        rc = if_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')

    def test_04_import_CA(self):
        rc = False
        cert_file = suite_path + '/definition/file/sonicauto.cer'
        pc1_login.send_command(f'\cp {cert_file} /tmp')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        print(res.stdout)
        if 'sonicauto.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca_api.import_ca_cert(file='/tmp/sonicauto.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import ca file failed!!")

    # @repeat_method(3)
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
        rc = setting_api.edit_firmware(**opt)
        Assertion.assert_equal(rc, True, "ERR: Skip Automatic Update window failed!!")
