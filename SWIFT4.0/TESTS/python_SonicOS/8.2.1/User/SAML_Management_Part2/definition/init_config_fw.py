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
            # 'dns2': Parameter.X1_DNS_2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True
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
            'zone': "DMZ",
            'mode': 'static',
            'ip': '13.13.1.168',
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            # 'user_http': True,
            'user_https': True,
        }
        rc = if_v4_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, 'ERR: config x2 failed')

    def test_04_skip_automatic_update_window(self):
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

    def test_05_import_CA(self):
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

    def test_06_add_idp(self):
        idp_add = {
            'name': "idp_azure",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "department",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': "Microsoft Azure Federated SSO Certificate (673F596265895E9643B1FD8B785D1EA4)",
            'user_name_attribute': "displayname"
        }
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_07_add_sp(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'name': "sp_azure",
            'service': {'https': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp https service failed!!")

    def test_08_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure",
            'management': True,
            'name': "profile_azure",
            'service_provider': "sp_azure",
            'single_sign_off': True,
            'single_logout': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile https failed!!")

    def test_09_enable_user_https_management_for_x0(self):
        x0_static = {
            'if': 'X0',
            'mode': 'static',
            'ip': Parameter.FIREWALL,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True
        }
        rc = if_v4_api.config_interface(**x0_static)
        Assertion.assert_equal(rc, True, 'ERR: enable_user_https_management_for_x0 failed')
