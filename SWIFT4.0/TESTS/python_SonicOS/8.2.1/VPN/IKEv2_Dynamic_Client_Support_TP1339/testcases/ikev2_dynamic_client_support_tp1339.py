import json
from definition.settings import *
from definition.utils import *


# Excepted: the Global IKEv2 Policy is created by default with the following attributes for IKE proposal. DH Group=2,
# Encryption=3DES, and Authentication=SHA1.
class TestTC01_check_default_ike_attributes_in_global_ikev2_policy(Test):
    uuid = "SOSAIOT-TC-54404"
    description = show_testcase_info(TESTPLAN, 'tc01', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_ikev2_dynamic_client_proposal_configuration_in_vpn_advanced_page(self):
        output = vpnadvancedsettingapi.show_vpnadvanced()
        logger.info(f'output is :{output}')
        checklist = ["'dh_group': '2'", "'encryption': 'aes-256'", "'authentication': 'sha-256'"]
        checkres = [i in str(output) for i in checklist]
        logger.info(f'checkres is :{checkres}')
        ParamCases.tc01ikev2settings = all(checkres)
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")


# Excepted:the dynamic client proposal is DH group 2 + AES-256 + SHA256
class TestTC33_check_dynamic_client_ikev2_settings(Test):
    uuid = "SOSAIOT-TC-54419"
    description = show_testcase_info(TESTPLAN, 'tc33', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc33')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_ikev2_dynamic_client_proposal_configuration_in_vpn_advanced_page(self):
        logger.info(f'ParamCases.tc01ikev2settings is:{ParamCases.tc01ikev2settings}')
        Assertion.assert_equal(ParamCases.tc01ikev2settings, True,
                               "ERR: check IKEv2 Dynamic Client Proposal configuration failed")


# Excepted:Check dynamic client ikev2 phase 1 default proposal value from CLI after default default.
class TestTC34_check_default_dynamic_client_ikev2_proposal_in_cli(Test):
    uuid = "SOSAIOT-TC-54420"
    description = show_testcase_info(TESTPLAN, 'tc34', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc34')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_tunnel_policy_with_gateway_full_zero_in_cli(self):
        localvpn_proposal_dict = {
            'type': 'tunnel-interface',
            'name': 'vpn1',
            'mode': 'shared-secret',
            'pri_gate': '0.0.0.0',
            'secret': '123456',
            'local_ike_id': 'ipv4 12.12.1.200',
            'peer_ike_id': 'ipv4 12.12.1.200',
        }
        res = vpnbasesettingscli.add_vpnpolicy(**localvpn_proposal_dict)
        Assertion.assert_equal(res, True, "ERR: add tunnel policy with zero gateway failed")

    def test_03_check_tunnel_policy_phase_1_proposal_in_cli(self):
        show_dict = {
            'type': 'tunnel-interface',
            'name': 'vpn1'
        }
        output = vpnbasesettingscli.show_vpnpolicy(**show_dict)
        logger.info(f'output is :{output}')
        checklist = ['ike encryption aes-256', 'ike authentication sha-256', 'ike dh-group 2']
        checkres = [i in str(output) for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check tunnel policy proposal in cli failed")

    def test_04_del_tunnel_policy(self):
        del_dict = {
            'name': 'vpn1'
        }
        delres = vpnbasesettingapi.del_tunnelvpn_policy(**del_dict)
        Assertion.assert_equal(delres, True, "ERR: delete tunnel policy failed")


# Excepted: IKE attributes in a VPN policy with IKEv2 exchange mode and zero IPSec gateway should be modified in the
# Global IKEv2 Policy.
class TestTC03_modify_ike_attributes_in_global_ikev2_policy(Test):
    uuid = "SOSAIOT-TC-54406"
    description = show_testcase_info(TESTPLAN, 'tc03', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_s2s_vpn_with_ikev2_aesgcm_encrytion_on_local_dut(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': '0.0.0.0',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            # 'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '1.1.1.1',
            'peer_ike_id': '2.2.2.2',
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_subnet',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_03_check_ikev2_dynamic_client_proposal_configuration_in_vpn_advanced_page(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-256'", "'authentication': 'sha-256'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")

    def test_04_change_ikev2_dynamic_client_proposal_configuration_in_vpn_advanced_page(self):
        logger.info('change Encryption from AES-256 to AES-128')
        proposalupdate = {
            "dh_group": "2",
            "encryption": "aes-128",
            "authentication": 'sha-256'
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_05_check_ike2_encryption_value_when_click_add_vpn_policy_proposal_tab(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-128'", "'authentication': 'sha-256'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")


# Excepted: AESGCM encrytion is inclluding in Global IKE settings
class TestTC22_check_global_ike_settings_includes_aesgcm_encrytion(Test):
    uuid = "SOSAIOT-TC-54408"
    description = show_testcase_info(TESTPLAN, 'tc22', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc22')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_configure_aesgcm_encrytion_aesgcm16_128(self):
        reslist = []
        prf_algorithmlist = ['hmac-md5', 'hmac-sha-1', 'hmac-sha-256', 'hmac-sha-384', 'hmac-sha-512']
        for prf_algorithm in prf_algorithmlist:
            proposalupdate = {
                "dh_group": "2",
                "encryption": "aes-gcm16-128",
                "prf": prf_algorithm
            }
            modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
            modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
            res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
            logger.info(f'res is :{res}')
            reslist.append(res)
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: configure aesgcm16_128 failed.")

    def test_03_configure_aesgcm_encrytion_aesgcm16_192(self):
        reslist = []
        prf_algorithmlist = ['hmac-md5', 'hmac-sha-1', 'hmac-sha-256', 'hmac-sha-384', 'hmac-sha-512']
        for prf_algorithm in prf_algorithmlist:
            proposalupdate = {
                "dh_group": "2",
                "encryption": "aes-gcm16-192",
                "prf": prf_algorithm
            }
            modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
            modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
            res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
            logger.info(f'res is :{res}')
            reslist.append(res)
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: configure aesgcm16_192 failed.")

    def test_04_configure_aesgcm_encrytion_aesgcm16_256(self):
        reslist = []
        prf_algorithmlist = ['hmac-md5', 'hmac-sha-1', 'hmac-sha-256', 'hmac-sha-384', 'hmac-sha-512']
        for prf_algorithm in prf_algorithmlist:
            proposalupdate = {
                "dh_group": "2",
                "encryption": "aes-gcm16-256",
                "prf": prf_algorithm
            }
            modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
            modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
            res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
            logger.info(f'res is :{res}')
            reslist.append(res)
        logger.info(f'reslist is:{reslist}')
        Assertion.assert_equal(all(reslist), True, "ERR: configure aesgcm16_256 failed.")


# Excepted: AESGCM encrytion in the Global IKEv2 settings can be saved and auto changed in IKEv2 peer policy
class TestTC23_modify_ike_attributes_via_gui(Test):
    uuid = "SOSAIOT-TC-54409"
    description = show_testcase_info(TESTPLAN, 'tc23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_ikev2_dynamic_client_proposal_configuration_in_vpn_advanced_page(self):
        logger.info('change Encryption to AESGCM16-128')
        proposalupdate = {
            "dh_group": "2",
            "encryption": "aes-gcm16-128",
            "prf": "hmac-sha-256"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_03_check_ike2_encryption_value_for_created_vpn_policy(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-256'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 encryption configuration failed")

    def test_04_inital_ikev2_dynamic_client_proposal_configuration(self):
        proposalupdate = {
            "dh_group": "2",
            "encryption": "aes-256",
            "authentication": "sha-256"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: inital ikev2 dynamic client proposal configuration failed")


# Excepted: AESGCM encrytion in the Global IKEv2 settings can be saved via CLI
class TestTC24_modify_ike_attributes_via_cli(Test):
    uuid = "SOSAIOT-TC-54410"
    description = show_testcase_info(TESTPLAN, 'tc24', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc24')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_ike_attributes_to_aesgcm_in_global_ikev2_settings_via_cli(self):
        vpnadvanced_dict = {
            'proposal dh-group': '2',
            'proposal encryption': 'aes-gcm16-128',
            'proposal prf': 'hmac-sha-384'
        }
        res = vpnadvancedsettingscli.vpn_advanced_setting(**vpnadvanced_dict)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal via CLI failed")

    def test_03_check_ike2_encryption_value_for_created_vpn_policy(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-384'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 encryption configuration failed")


# Excepted: TSR shows the Global IKEv2 Settings from the VPN>Advances page and settings for a VPN policy with IKEv2
# exchange mode.
class TestTC25_tsr(Test):
    uuid = "SOSAIOT-TC-54411"
    description = show_testcase_info(TESTPLAN, 'tc25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_download_tsr_and_check_ikev2_procosal_configuration_in_vpn_policy(self):
        checkres = [False]
        output = diagnosticapi.get_tsr_part('VPN', lab1='Settings')
        vpnsettings_sp = output.split('--- SA')
        for vpnsetting in vpnsettings_sp:
            logger.info(vpnsetting)
            checklist = ['localvpn', 'DH Group 2; Encrypt/Prf - AESGCM16-128/PRF-HMAC-SHA384', 'IKEv2 Mode']
            checkres = [i in vpnsetting for i in checklist]
            logger.info(f'checkres is:{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check tsr ikev2 procosal encrytion in vpn policy failed")

    def test_03_download_tsr_and_check_ikev2_procosal_configuration_in_vpn_advanced_page(self):
        output = diagnosticapi.get_tsr_part('VPN', lab1='Advanced')
        logger.info(f'output is:{output}')
        flag = True if 'DH Group 2; Encrypt/Prf - AESGCM16-128/PRF-HMAC-SHA384' in output else False
        Assertion.assert_equal(flag, True, "ERR: check tsr ikev2 procosal encrytion in vpn advanced page")


# Excepted:IKEv2 Dynamic Client Proposal Encrytion is AESGCM settings should be keep after firewall reboot
class TestTC26_restart_test(Test):
    uuid = "SOSAIOT-TC-54412"
    description = show_testcase_info(TESTPLAN, 'tc26', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc26')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_restart_dut(self):
        res = restartapi.restart_now()
        Assertion.assert_equal(res, True, "ERR: Restart DUT failed")

    def test_03_check_ikev2_dynamic_client_proposal_encrytion_configuration_after_restart(self):
        output = vpnadvancedsettingapi.show_vpnadvanced()
        logger.info(f'output is :{output}')
        checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-384'"]
        checkres = [i in str(output) for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")

    def test_04_check_ike2_encryption_value_when_click_add_vpn_policy_proposal_tab_after_restart(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-384'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Proposal configuration in vpn policy failed")


# Excepted:IKEv2 Dynamic Client Proposal Encrytion is AESGCM settings should be keep after exp file import
class TestTC27_prefs_export_and_import_test(Test):
    uuid = "SOSAIOT-TC-54413"
    description = show_testcase_info(TESTPLAN, 'tc27', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_export_prefs(self):
        logger.info('=> export exp file.')
        res = settingapi.export_setting_exp('/tmp/jlian_ikev2_dynamic_client_test.exp')
        Assertion.assert_equal(res, True, "ERR: export exp file failed")

    def test_03_restore_fw(self):
        logger.info('=> restore DUT.')
        res = settingapi.boot_fw(mode=2)
        Assertion.assert_equal(res, True, "ERR: restore unit failed")

    def test_04_00_import_exp_file(self):
        logger.info('=> import exp file.')
        res = settingapi.import_setting_exp(
            filepath='/tmp/jlian_ikev2_dynamic_client_test.exp')
        Assertion.assert_equal(res, True, "ERR: import exp file failed")
    
    def test_04_01_register_fw(self):
        for i in range(5):
            time.sleep(10)
            rc = licensecli.register("online")
            if rc:
                break
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_05_check_ikev2_dynamic_client_proposal_encrytion_configuration_after_import_exp_file(self):
        output = vpnadvancedsettingapi.show_vpnadvanced()
        logger.info(f'output is :{output}')
        checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-384'"]
        checkres = [i in str(output) for i in checklist]
        logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")

    def test_06_check_ike2_encryption_value_when_click_add_vpn_policy_proposal_tab_after_import_exp_file(self):
        checkres = [False]
        vpnpolicy = get_site_to_site_vpn_policy_by_name(vpnbasesettingapi, 'localvpn')
        logger.info(f'********vpnpolicy is:{vpnpolicy}')
        if vpnpolicy:
            proposalike = vpnpolicy['ipv4']['site_to_site']['proposal']['ike']
            logger.info(f'*************proposalike is :{proposalike}')
            checklist = ["'dh_group': '2'", "'encryption': 'aes-gcm16-128'", "'prf': 'hmac-sha-384'"]
            checkres = [i in str(vpnpolicy) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check IKEv2 Dynamic Client Proposal configuration failed")

    def test_07_delete_local_vpn_policy(self):
        del_dict = {
            'name': 'localvpn'
        }
        res = vpnbasesettingapi.del_s2svpn_policy(**del_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: del vpn policy failed")


# Excepted: Negotiate a tunnel using a VPN policy with IKEv2 exchange mode and zero IPSec gateway.
class TestTC09_negotiate_tunnel(Test):
    uuid = "SOSAIOT-TC-54407"
    description = show_testcase_info(TESTPLAN, 'tc09', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc09')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_inital_ikev2_dynamic_client_proposal_configuration(self):
        proposalupdate = {
            "dh_group": "2",
            "encryption": "aes-128",
            "authentication": "sha-1"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: inital ikev2 dynamic client proposal configuration failed")

    def test_03_add_vpn_policy_with_ikev2_exchange_mode_and_zero_ipsec_gateway_on_local_dut(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': '0.0.0.0',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '270',
            'ipsec_lifetime': '120',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '1.1.1.1',
            'peer_ike_id': '2.2.2.2',
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_subnet',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_04_add_vpn_policy_on_remote_dut(self):
        rvpn = {
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            'ike_lifetime': '270',
            'ipsec_lifetime': '120',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '1.1.1.1',
            'local_net_type': 'name',
            'local_net_name': 'X3 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x2_subnet',
            'keep_alive': True,
        }
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    @repeat_method(2)
    def test_05_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status('localvpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    @repeat_method(2)
    def test_06_check_remote_vpn_status(self):
        time.sleep(10)
        (res, status) = r_vpnbasesettingapi.get_vpn_status('remotevpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check remote vpn status failed.")

    @repeat_method(2)
    def test_07_check_vpn_traffic_from_local_lan_host_to_remote_lan_host(self):
        output = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    @repeat_method(2)
    def test_08_check_traffic_from_remote_lan_host_to_local_lan_host(self):
        output = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")


# Excepted:This test verifies that IKEv2 dynamic peer policy is renegotiated  when IKE/IPSec lifetime expires.
class TestTC14_rekey_event(Test):
    uuid = "SOSAIOT-TC-54405"
    description = show_testcase_info(TESTPLAN, 'tc14', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_change_central_log_level(self):
        editdict73 = {
            "log": {
                "group": [
                    {
                        "id": 73,
                        "name": "VPN IKEv2",
                        "log_monitor": {
                            "type": "mixed",
                            "redundancy_interval": {}
                        },
                    }
                ]
            }
        }
        editdict14 = {
            "log": {
                "group": [
                    {
                        "id": 14,
                        "name": "VPN IPSec",
                        "log_monitor": {
                            "type": "mixed",
                            "redundancy_interval": {}
                        },
                    }
                ]
            }
        }
        logsetres = logcategoryapi.logging_level(level='debug')
        logset73res = logcategoryapi.edit_log_category_groups_by_id(73, **editdict73)
        logset14res = logcategoryapi.edit_log_category_groups_by_id(14, **editdict14)
        logger.info(f'logsetres is:{logsetres},logset73res is:{logset73res},logset14res is:{logset14res}')
        Assertion.assert_equal(logsetres & logset73res & logset14res, True, "ERR: change central log failed.")

    def test_03_renegotiate_Tunnel_stats(self):
        res = vpnbasesettingapi.Renegotiate_Tunnel_stats()
        Assertion.assert_equal(res, True, "ERR: renegotiate vpn failed")

    def test_04_check_system_logs(self):
        flag = False
        res = logmonitorapi.clear_log()
        logger.info(f'res is :{res}')
        if res == None:
            time.sleep(240)
            getlog978res = logmonitorapi.get_log(id=978)
            logger.info(f'getlog978res is:{getlog978res}')
            getlog427res = logmonitorapi.get_log(id=427)
            logger.info(f'getlog427res is:{getlog427res}')
            if 'IPsec Tunnel status changed' in str(getlog427res) and 'IKEv2 negotiation complete' in str(getlog978res):
                flag = True
        Assertion.assert_equal(flag, True, "ERR: check renegotiation log failed ")


# Excepted: IKE and IPSec tunnel can be created using a VPN policy with IKEv2 exchange mode phase1 using AESGCM
# encrytion and zero IPSec gateway.
class TestTC28_s2s_negotiate_aesgcm_encrytion(Test):
    uuid = "SOSAIOT-TC-54414"
    description = show_testcase_info(TESTPLAN, 'tc28', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_local_and_remote_vpn_policy(self):
        del_dict1 = {
            'name': 'localvpn'
        }
        del_dict2 = {
            'name': 'remotevpn'
        }
        res1 = vpnbasesettingapi.del_s2svpn_policy(**del_dict1)
        res2 = r_vpnbasesettingapi.del_s2svpn_policy(**del_dict2)
        logger.info(f'res1 is: {res1},res2 is:{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: del vpn policy failed")

    def test_03_configure_ikev2_dynamic_client_proposal_configuration(self):
        proposalupdate = {
            "dh_group": "1",
            "encryption": "aes-gcm16-256",
            # "authentication": "hmac-sha-512",
            "prf": "hmac-sha-512"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = proposalupdate
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: configure ikev2 dynamic client proposal configuration failed")

    def test_04_add_s2s_vpn_with_ikev2_aesgcm_encrytion_on_local_dut(self):
        lvpn = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': '0.0.0.0',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes-128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'sha-1',
            # 'ike_dh_group': '2',
            # 'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '1.1.1.1',
            'peer_ike_id': '2.2.2.2',
            'local_net_type': 'name',
            'local_net_name': 'X2 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x3_subnet',
            'keep_alive': True,
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_05_add_s2s_vpn_with_ikev2_aesgcm_encrytion_on_remote_dut(self):
        rvpn = {
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-256',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-512',
            'ike_dh_group': '1',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '1.1.1.1',
            'local_net_type': 'name',
            'local_net_name': 'X3 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_x2_subnet',
            'keep_alive': True,
        }
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_s2svpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    @repeat_method(2)
    def test_06_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status('localvpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    @repeat_method(2)
    def test_07_check_remote_vpn_status(self):
        time.sleep(10)
        (res, status) = r_vpnbasesettingapi.get_vpn_status('remotevpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check remote vpn status failed.")

    @repeat_method(2)
    def test_08_check_vpn_traffic_from_local_lan_host_to_remote_lan_host(self):
        output = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    @repeat_method(2)
    def test_09_check_traffic_from_remote_lan_host_to_local_lan_host(self):
        output = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")


# Excepted: Dynamic client VPN tunnel up on phase 1 AESGCM, CLI command 'show vpn tunnels' or 'show vpn tunnel
# <policy name>' can show the algorithm and prf algorithm.
class TestTC35_check_aesgcm_in_cli_when_tunnel_up(Test):
    uuid = "SOSAIOT-TC-54421"
    description = show_testcase_info(TESTPLAN, 'tc35', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc35')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_aesgcm_encrytion_in_cli_when_tunnel_up(self):
        checkres = [False]
        (res, status) = vpnbasesettingapi.get_vpn_status('localvpn')
        logger.info(f'vpn status:{res},{status}')
        if res and status == 'up':
            show_dict = {
                'type': 'site-to-site',
                'name': 'localvpn'
            }
            output = vpnbasesettingscli.show_vpnpolicy(**show_dict)
            logger.info(f'output is :{output}')
            checklist = ['ike encryption aes-gcm16-256', 'ike prf hmac-sha-512', 'ike dh-group 1']
            checkres = [i in str(output) for i in checklist]
            logger.info(f'checkres is :{checkres}')
        Assertion.assert_equal(all(checkres), True, "ERR: check aesgcm proposal in cli failed")


# Excepted: IKE and IPSec S2S tunnel can be created using a VPN policy with IKEv2 exchange mode phase1 using
# different AESGCM encrytion and PRF Algorithm with zero IPSec gateway.
class TestTC30_combination_test_s2s_negotiate_aesgcm_encrytion(Test):
    uuid = "SOSAIOT-TC-54416"
    description = show_testcase_info(TESTPLAN, 'tc30', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc30')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_ikev2_proposal_encryption_aesgcm16_128_and_prf_algorithm_prf_hmac_md5_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-128",
            "prf": "hmac-md5"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_03_modify_ikev2_proposal_encryption_aesgcm16_128_and_prf_algorithm_prf_hmac_md5_for_vpn_policy_on_remote_dut(
            self):
        modify_vpn_dict = {
            'edit_proposal': True,
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',

            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-128',
            'ipversion': 'ipv4',
            'prf': 'hmac-md5',
            'ike_dh_group': '2',
        }
        res = r_vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 proposal encryption for vpn policy on remote dut failed")

    def test_04_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-128 PRF-HMAC-MD5, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")

    @repeat_method(2)
    def test_05_check_traffic_between_local_lan_host_and_remote_lan_host(self):
        output1 = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        output2 = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output1 is:{output1}')
        logger.info(f'output2 is:{output2}')
        flag = True if "100% packet loss" not in output1 and "100% packet loss" not in output2 else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    def test_06_modify_ikev2_proposal_encryption_aesgcm16_192_and_prf_algorithm_prf_hmac_384_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-192",
            "prf": "hmac-sha-384"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_07_modify_ikev2_proposal_encryption_aesgcm16_192_and_prf_algorithm_prf_hmac_384_for_vpn_policy_on_remote_dut(
            self):
        modify_vpn_dict = {
            'edit_proposal': True,
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',

            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-192',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-384',
            'ike_dh_group': '2',
        }
        res = r_vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 proposal encryption for vpn policy on remote dut failed")

    def test_08_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-192 PRF-HMAC-SHA384, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")

    def test_09_check_traffic_between_local_lan_host_and_remote_lan_host(self):
        self.test_05_check_traffic_between_local_lan_host_and_remote_lan_host()

    def test_10_modify_ikev2_proposal_encryption_aesgcm16_192_and_prf_algorithm_prf_hmac_384_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-256",
            "prf": "hmac-sha-512"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_11_modify_ikev2_proposal_encryption_aesgcm16_256_and_prf_algorithm_prf_hmac_512_for_vpn_policy_on_remote_dut(
            self):
        modify_vpn_dict = {
            'edit_proposal': True,
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',

            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-256',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-512',
            'ike_dh_group': '2',
        }
        res = r_vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is:{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 proposal encryption for vpn policy on remote dut failed")

    def test_12_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-256 PRF-HMAC-SHA512, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")

    def test_13_check_traffic_between_local_lan_host_and_remote_lan_host(self):
        self.test_05_check_traffic_between_local_lan_host_and_remote_lan_host()


# Excepted:S2S VPN auth by 3rd party certificate, under DH group 14 + AESGCM16-256 + PRF_HMAC_SHA256.'
class TestTC32_s2s_auth_by_3rd_party_with_aesgcm(Test):
    uuid = "SOSAIOT-TC-54418"
    description = show_testcase_info(TESTPLAN, 'tc32', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc32')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_import_certificate_pfx_on_local_dut(self):
        (res, output) = locertificateapi.import_cert_local('@' + CERT4k_PATH, name="localcert", password='12345678',
                                                           msg=True)
        logger.info(output)
        Assertion.assert_equal(res, True, 'import local cert Failed.')

    def test_03_show_import_cert_on_local_dut(self):
        output = locertificateapi.show_imported_certs()
        flag = True if "'certificate': 'localcert'" in str(output) else False
        Assertion.assert_equal(flag, True, ' check cert Failed.')

    def test_04_import_certificate_pfx_on_remote_dut(self):
        (res, output) = recertificateapi.import_cert_local_with_json('@' + CERT4k_PATH, name="localcert", password='12345678',
                                                           msg=True)
        logger.info(output)
        Assertion.assert_equal(res, True, 'import local cert Failed.')

    def test_05_show_import_cert_on_remote_dut(self):
        output = recertificateapi.show_imported_certs()
        flag = True if "'certificate': 'localcert'" in str(output) else False
        Assertion.assert_equal(flag, True, ' check cert Failed.')

    def test_06_modify_ikev2_dynamic_proposal_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "14",
            "encryption": "aes-gcm16-256",
            "prf": "hmac-sha-256"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_07_edit_s2s_local_vpn_local_to_3rd_auth_mode(self):
        modify_vpn_dict = {
            'edit_auth': True,
            'type': 'site_to_site',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'certificate',
            'local_cert': 'localcert',
            'local_ike_type': 'distinguished-name',
            'peer_ike_type': 'distinguished_name',
            'peer_ike_id': 'C=CN,ST=SH,L=SH,O=kun,OU=kun,CN=rsa4k,emailAddress=kun@163.com',
        }
        res = vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: edit vpn policy failed.")

    def test_08_edit_s2s_local_vpn_local_to_3rd_auth_mode_on_remote_dut(self):
        modify_vpn_dict = {
            'edit_proposal': True,
            'edit_auth': True,
            'type': 'site_to_site',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'certificate',
            'local_cert': 'localcert',
            'local_ike_type': 'distinguished-name',
            'peer_ike_type': 'distinguished_name',
            'peer_ike_id': 'C=CN,ST=SH,L=SH,O=kun,OU=kun,CN=rsa4k,emailAddress=kun@163.com',

            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-256',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-256',
            'ike_dh_group': '14',
        }
        res = r_vpnbasesettingapi.edit_vpn_policy(**modify_vpn_dict)
        logger.info(f'res is: {res}')
        Assertion.assert_equal(res, True, "ERR: edit vpn policy failed.")

    def test_09_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-256 PRF-HMAC-SHA256, DH Group 14' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")

    @repeat_method(2)
    def test_10_check_traffic_between_local_lan_host_and_remote_lan_host(self):
        output1 = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        output2 = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output1 is:{output1}')
        logger.info(f'output2 is:{output2}')
        flag = True if "100% packet loss" not in output1 and "100% packet loss" not in output2 else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")


# Excepted:[tunnel]Negotiate a tunnel VPN with IKEv2 exchange mode phase1 using AESGCM encrytion and zero IPSec gateway
class TestTC29_tunnel_negotiate_aesgcm_encrytion(Test):
    uuid = "SOSAIOT-TC-54415"
    description = show_testcase_info(TESTPLAN, 'tc29', description=True)['title']
    pbr_name = "pbrti"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc29')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_delete_s2s_vpn_policy(self):
        del_dict1 = {
            'name': 'localvpn'
        }
        del_dict2 = {
            'name': 'remotevpn'
        }
        res1 = vpnbasesettingapi.del_s2svpn_policy(**del_dict1)
        res2 = r_vpnbasesettingapi.del_s2svpn_policy(**del_dict2)
        logger.info(f'res1 is: {res1},res2 is:{res2}')
        Assertion.assert_equal(res1 & res2, True, "ERR: del vpn policy failed")

    def test_03_modify_ikev2_dynamic_proposal_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-256",
            "prf": "hmac-sha-512"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_04_add_tunnel_vpn_policy_with_ikev2_aesgcm_encrytion_on_local_dut(self):
        lvpn = {
            'type': 'tunnel_interface',
            'name': 'localvpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': '0.0.0.0',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            # 'ike_encryption': 'aes_gcm16_128',
            'ipversion': 'ipv4',
            # 'ike_auth': 'hmac-sha-256',
            # 'ike_dh_group': '2',
            # 'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '1.1.1.1',
            'peer_ike_id': '2.2.2.2',
        }
        res = vpnbasesettingapi.add_vpn_policy(**lvpn)
        logger.info(res)
        vpnentry = vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), "localvpn", "ERR: Add local vpn policy failed.")

    def test_05_add_tunnle_vpn_policy_with_ikev2_aesgcm_encrytion_on_remote_dut(self):
        rvpn = {
            'type': 'tunnel_interface',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-256',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-512',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '1.1.1.1',
            'keep_alive': True,
        }
        res = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(res)
        vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
        logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    def test_06_create_vpn_tunnel_interface_local(self):
        tunnel_interface = {
            'zone': 'VPN',
            'type': "vpn_tunnel",
            'mode': 'static',
            'ip': '11.1.1.1',
            'netmask': '255.255.255.0',
            "tunnel_name": 'TI',
            'comment': '',
            "vpn_policy": 'localvpn',
            'mgmt_ping': True,
        }
        res = interfacev4api.add_interface(**tunnel_interface)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on local dut failed")

    def test_07_create_vpn_tunnel_interface_on_remote_DUT(self):
        tunnel_interface = {
            'zone': 'VPN',
            'type': "vpn_tunnel",
            'mode': 'static',
            'ip': '11.1.1.2',
            'netmask': '255.255.255.0',
            "tunnel_name": 'TI',
            'comment': '',
            "vpn_policy": 'remotevpn',
            'mgmt_ping': True,
        }
        res = r_interfacev4api.add_interface(**tunnel_interface)
        Assertion.assert_equal(res, True, "ERR: create tunnel interface on remote dut failed")

    def test_08_add_pbr_with_tunnel_interface_on_local_dut(self):
        pbr_update = {
            "name": self.pbr_name,
            "interface": 'TI',
            "destination": {
                "name": "remote_x3_subnet"
            },
            "probe": "",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        res = routepolicyapi.add_route_policy(**pbr_dict)
        Assertion.assert_equal(res, True, "ERR: add pbr with tunnel interface on local dut failed")

    def test_09_add_pbr_with_tunnel_interface_on_remote_dut(self):
        pbr_update = {
            "name": self.pbr_name,
            "interface": 'TI',
            "destination": {
                "name": "remote_x2_subnet"
            },
            "probe": "",
        }
        pbr_dict = copy.deepcopy(initial_pbr_dict)
        pbr_dict["route_policies"][0]["ipv4"].update(pbr_update)
        logger.info(f'new is:{pbr_dict}')
        res = r_routepolicyapi.add_route_policy(**pbr_dict)
        Assertion.assert_equal(res, True, "ERR: add pbr with tunnel interface on remote dut failed")

    @repeat_method(2)
    def test_10_check_local_vpn_status(self):
        time.sleep(10)
        (res, status) = vpnbasesettingapi.get_vpn_status('localvpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check local vpn status failed.")

    @repeat_method(2)
    def test_11_check_remote_vpn_status(self):
        time.sleep(10)
        (res, status) = r_vpnbasesettingapi.get_vpn_status('remotevpn')
        logger.info(f'vpn status:{res},{status}')
        flag = True if res and status == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: check remote vpn status failed.")

    @repeat_method(2)
    def test_12_check_vpn_traffic_from_local_lan_host_to_remote_lan_host(self):
        output = PC2_Login.send_command(f'ping {PC3_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    @repeat_method(2)
    def test_13_check_traffic_from_remote_lan_host_to_local_lan_host(self):
        output = PC3_Login.send_command(f'ping {PC2_ETH1_IP} -I eth1 -c 5')
        logger.info(f'output is:{output}')
        flag = True if "100% packet loss" not in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn traffic failed")

    def test_14_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-256 PRF-HMAC-SHA512, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")


# Excepted:IKE and IPSec tunnel VPN connection can be created using a VPN policy with IKEv2 exchange mode phase1
# using different AESGCM encrytion and PRF Algorithm with zero IPSec gateway.
class TestTC31_combination_test_tunnel_negotiate_aesgcm_encrytion(Test):
    uuid = "SOSAIOT-TC-54417"
    description = show_testcase_info(TESTPLAN, 'tc31', description=True)['title']
    pbr_name = "pbrti"

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, 'tc31')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_modify_ikev2_proposal_encryption_aesgcm16_128_and_prf_algorithm_prf_hmac_sha256_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-128",
            "prf": "hmac-sha-256"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_03_add_ikev2_proposal_encryption_aesgcm16_128_and_prf_algorithm_prf_hmac_sha256_for_vpn_policy_on_remote_dut(self):
        vpnentry = ''
        del_dict = {
            'name': 'remotevpn'
        }
        rvpn = {
            'type': 'tunnel_interface',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-128',
            'ipversion': 'ipv4',
            'prf': 'hmac-sha-256',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '1.1.1.1',
            'keep_alive': True,
        }
        delpbrres = r_routepolicyapi.del_route_policy_by_name('pbrti')
        deltires = r_interfacev4api.del_tunnel_interface_by_name('TI')
        delvpnpolicyres = r_vpnbasesettingapi.del_tunnelvpn_policy(**del_dict)
        logger.info(f'*******delpbrres is :{delpbrres}.deltires is:{deltires} and delvpnpolicyres is:{delvpnpolicyres}')
        if delpbrres and deltires and delvpnpolicyres:
            addres = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
            if addres:
                vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
            logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    def test_04_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-128 PRF-HMAC-SHA256, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike failed")

    def test_05_modify_ikev2_proposal_encryption_aesgcm16_192_and_prf_algorithm_prf_hmac_384_on_local_dut(self):
        ikev2_proposal_dict = {
            "dh_group": "2",
            "encryption": "aes-gcm16-192",
            "prf": "hmac-md5"
        }
        modify_dict = copy.deepcopy(modify_vpn_advanced_dict)
        modify_dict["vpn"]["ikev2"]["proposal"] = ikev2_proposal_dict
        res = vpnadvancedsettingapi.modify_vpnadvanced(**modify_dict)
        logger.info(f'res is :{res}')
        Assertion.assert_equal(res, True, "ERR: modify ike2 dynamic proposal in vpn advanced page failed")

    def test_06_add_ikev2_proposal_encryption_aesgcm16_128_and_prf_algorithm_prf_hmac_md5_for_vpn_policy_on_remote_dut(self):
        vpnentry = ''
        del_dict = {
            'name': 'remotevpn'
        }
        rvpn = {
            'type': 'tunnel_interface',
            'name': 'remotevpn',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.X1_IP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'ike_exchange': 'ikev2',
            'ike_encryption': 'aes-gcm16-192',
            'ipversion': 'ipv4',
            'prf': 'hmac-md5',
            'ike_dh_group': '2',
            'ike_lifetime': '28800',
            'ipsec_lifetime': '28800',
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_gcm16_256',
            # 'ipsec_pfs': True,
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '1.1.1.1',
            'keep_alive': True,
        }
        delres = r_vpnbasesettingapi.del_tunnelvpn_policy(**del_dict)
        addres = r_vpnbasesettingapi.add_vpn_policy(**rvpn)
        logger.info(f'delres is :{delres} and addres is:{addres}')
        if delres and addres:
            vpnentry = r_vpnbasesettingapi.show_tunnelvpnpolicy()
            logger.info(f'vpnentry is :{vpnentry}')
        Assertion.assert_regular(str(vpnentry), 'remotevpn', "ERR: Add remote vpn policy failed.")

    def test_07_check_vpn_tunnel_ike_in_cli(self):
        output = vpnbasesettingscli.show_vpn_tunnel('localvpn', 'ike')
        logger.info(f'output is:{output}')
        flag = True if 'IKEv2 Mode, AESGCM16-192 PRF-HMAC-MD5, DH Group 2' in output else False
        Assertion.assert_equal(flag, True, "ERR: check vpn tunnel ike in cli failed")
