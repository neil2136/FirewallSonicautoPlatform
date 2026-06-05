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
            'dns1': Parameter.X1_DNS_1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True
        }
        rc = if_v4_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, 'ERR: config x1 failed')

    @repeat_method(10, sleep=10)
    def test_02_register_fw(self):
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_skip_automatic_update_window(self):
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


class Test_PreSettings(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_import_CA(self):
        rc = False
        cert_file = suite_path + '/definition/file/saml_cyuan.cer'
        pc1_login.send_command(f'\cp {cert_file} /tmp/')
        res = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
        if 'saml_cyuan.cer' in res.stdout:
            logger.info('cp cert file to PC1 success!!')
            rc = ca.import_ca_cert(file='/tmp/saml_cyuan.cer')
        else:
            logger.error('cp cert file to PC1 failed!!')
        Assertion.assert_equal(rc, True, "ERR: import ca file failed!!")

    def test_02_add_IDP(self):
        idp_add = {
            'name': "idp_azure_X0",
            "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            "group_name_attribute": "department",
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2",
            'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/",
            'trusted_certificate': 'Microsoft Azure Federated SSO Certificate (74321D8CAC6FF2B3491EC38B8F356108)',
            'user_name_attribute': "displayname"
        }
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_03_add_sp(self):
        sp = {
            'address_object': 'X0 IP',
            'name': "sp_azure",
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add saml sp failed!!")

    def test_04_add_related_ao(self):
        opt1 = {
            "object_type": "fqdn",
            "name": "Windows Azure Related",
            "zone": "WAN",
            'value': "*.windowsazure.com",
            'dns_ttl': 0
        }
        opt2 = {
            "object_type": "fqdn",
            "name": "Microsoft Auth",
            "zone": "WAN",
            'value': "aadcdn.msauth.net",
            'dns_ttl': 0
        }
        opt3 = {
            "object_type": "fqdn",
            "name": "Microsoft Auth Image",
            "zone": "WAN",
            'value': "aadcdn.msauthimages.net",
            'dns_ttl': 0
        }
        opt4 = {
            "object_type": "fqdn",
            "name": "Microsoft Live Related",
            "zone": "WAN",
            'value': "*.live.com",
            'dns_ttl': 0
        }
        opt5 = {
            "object_type": "fqdn",
            "name": "Microsoft Login Online Related",
            "zone": "WAN",
            'value': "*.microsoftonline.com",
            'dns_ttl': 0
        }
        opt6 = {
            "object_type": "fqdn",
            "name": "Microsoft Login Related",
            "zone": "WAN",
            'value': "*.microsoft.com",
            'dns_ttl': 0
        }
        for opt in (opt1, opt2, opt3, opt4, opt5, opt6):
            rc = ao_api.config_addressobject(**opt)
            if not rc:
                logger.error(f'======>add {opt["name"]} addr obj failed!!')
        Assertion.assert_equal(rc, True, 'ERR: add related ao failed!!')

    def test_05_add_related_addr_group(self):
        opt = {'address_groups': [{
            "ipv6": {
                "name": 'SAML Bypass List For Microsoft Entra',
                'address_object':
                    {
                        'fqdn': [
                            {'name': "Windows Azure Related"},
                            {'name': "Microsoft Auth"},
                            {'name': "Microsoft Auth Image"},
                            {'name': "Microsoft Live Related"},
                            {'name': "Microsoft Login Online Related"},
                            {'name': "Microsoft Login Related"}
                        ]
                    }
            }}]
        }
        rc = ag_api.add_addressgroup(**opt)
        Assertion.assert_equal(rc, True, 'ERR: add related addr group failed!!')

    def test_06_add_profile(self):
        saml_profile = {
            'certificate': "",
            'identity_provider': "idp_azure_X0",
            'management': True,
            'name': "profile_azure_X0",
            'service_provider': "sp_azure",
            'single_logout': True,
            'sslvpn': False,
            'use_certificate_sign_sp_request': False
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile failed!!")

    def test_07_add_access_rule_for_saml(self):
        opt1 = {"access_rules": [{
            "ipv4": {
                "name": "SAML Bypass List For Microsoft Entra (ipv4)",
                "from": "any",
                "to": "WAN",
                "service": {
                    "name": "HTTPS"
                },
                "destination": {"address": {'group': "SAML Bypass List For Microsoft Entra"}},
                "priority": {'manual': {'value': 1}}
            }
        }]}
        opt2 = {"access_rules": [{
            "ipv4": {
                'name': "SAML Bypass DNS Rule (ipv4)",
                "from": "any",
                "to": "WAN",
                "service": {
                    'group': "DNS (Name Service)"
                },
                "priority": {'manual': {'value': 2}}
            }
        }]}
        opt3 = {"access_rules": [{
            "ipv4": {
                'name': "redirect_saml",
                "from": "any",
                "to": "WAN",
                'saml_authentication': True,
                'saml_profile': "profile_azure_X0",
                "service": {
                    "name": "HTTPS"
                },
                'users': {'included': {'group': "Everyone"}, 'excluded': {'none': True}},
                "priority": {'manual': {'value': 30}}
                # 'priority': {'end': True}
            }
        }]}
        for opt in (opt1, opt2, opt3):
            rc = acl.add_accessrule(**opt)
            if not rc:
                logger.error(f'======> add access rule {opt["access_rules"][0]["ipv4"]["name"]} failed!!')
        Assertion.assert_equal(rc, True, 'ERR: add access rule for saml failed！！')

    def test_08_delete_default_LAN_to_WAN_acl(self):
        input_json = {
            'from': "LAN",
            'to': "WAN",
            'name': "Default Access Rule"
        }
        rc = acl.delete_accessrule_by_json(**input_json)
        api_logout = fw.api_logout()
        logger.info(f'-> API Logout Result: {api_logout}')
        Assertion.assert_equal(rc, True, 'ERR: delete default LAN to WAN acl failed!!')
