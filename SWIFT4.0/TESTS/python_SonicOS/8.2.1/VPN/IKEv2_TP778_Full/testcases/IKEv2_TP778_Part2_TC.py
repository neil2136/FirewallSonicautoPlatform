from definition.settings import *
from bin import check_traffic


class TestIKEv2_TP778_1522668(Test):
    uuid = "SOSAIOT-TC-54357"
    description = show_testcase_info(TESTPLAN, '1522668', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522668')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['site_to_site']
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('12.12.1.201', resp['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('remote_net', resp['network']['remote']['destination_network']['name'], "ERR: check VPN policy failed")

    def test_03_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522669(Test):
    uuid = "SOSAIOT-TC-54358"
    description = show_testcase_info(TESTPLAN, '1522669', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522669')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Lvpn)
        ref2['name'] = 'vpn2'
        ref2['pri_gate'] = 'test.com'
        ref2['remote_net_name'] = 'remote_net2'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        rc &= Lvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp1 = res['vpn']['policy'][0]['ipv4']['site_to_site']
        resp2 = res['vpn']['policy'][1]['ipv4']['site_to_site']
        Assertion.assert_equal('vpn1', resp1['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('12.12.1.201', resp1['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('remote_net', resp1['network']['remote']['destination_network']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('vpn2', resp2['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('test.com', resp2['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('remote_net2', resp2['network']['remote']['destination_network']['name'], "ERR: check VPN policy failed")

    def test_03_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522670(Test):
    uuid = "SOSAIOT-TC-54359"
    description = show_testcase_info(TESTPLAN, '1522670', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522670')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '1'
        ref1['prf'] = 'hmac-sha-384'
        ref1['ike_encryption'] = 'aes-gcm16-128'
        ref2['ike_dh_group'] = '1'
        ref2['prf'] = 'hmac-sha-384'
        ref2['ike_encryption'] = 'aes-gcm16-128'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522671(Test):
    uuid = "SOSAIOT-TC-54360"
    description = show_testcase_info(TESTPLAN, '1522671', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522671')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '2'
        ref1['prf'] = 'hmac-md5'
        ref1['ike_encryption'] = 'aes-gcm16-192'
        ref2['ike_dh_group'] = '2'
        ref2['prf'] = 'hmac-md5'
        ref2['ike_encryption'] = 'aes-gcm16-192'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522674(Test):
    uuid = "SOSAIOT-TC-54363"
    description = show_testcase_info(TESTPLAN, '1522674', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522674')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_3rd)
        ref2 = copy.deepcopy(Rvpn_3rd)
        ref1['ike_dh_group'] = '19'
        ref1['ike_auth'] = 'sha-512'
        ref1['ike_encryption'] = 'aes-128'
        ref2['ike_dh_group'] = '19'
        ref2['ike_auth'] = 'sha-512'
        ref2['ike_encryption'] = 'aes-128'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522676(Test):
    uuid = "SOSAIOT-TC-54365"
    description = show_testcase_info(TESTPLAN, '1522676', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522676')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_3rd)
        ref2 = copy.deepcopy(Rvpn_3rd)
        ref1['pri_gate'] = '0.0.0.0'
        ref2['keep_alive'] = True
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1532972(Test):
    uuid = "SOSAIOT-TC-54367"
    description = show_testcase_info(TESTPLAN, '1532972', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1532972')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_3rd)
        ref2 = copy.deepcopy(Rvpn_3rd)
        ref1['ike_lifetime'] = '120'
        ref1['ipsec_lifetime'] = '120'
        ref1['keep_alive'] = True
        ref2['ike_lifetime'] = '120'
        ref2['ipsec_lifetime'] = '120'
        ref2['keep_alive'] = True
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['IKEv2 negotiation complete']
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: Test log failed")

    def test_04_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1745858(Test):
    uuid = "SOSAIOT-TC-54368"
    description = show_testcase_info(TESTPLAN, '1745858', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1745858')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_cannot_be_edit(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['pri_gate'] = '0.0.0.0'
        ref1['ike_dh_group'] = '1'
        ref1['ike_auth'] = 'sha-1'
        ref1['ike_encryption'] = 'triple-des'
        ref1['local_ike_id'] = '1.1.1.1'
        ref1['peer_ike_id'] = '2.2.2.2'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['site_to_site']
        # logger.info(resp)
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('0.0.0.0', resp['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('aes-128', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")
        Assertion.assert_equal('sha-1', resp['proposal']['ike']['authentication'], "ERR: check VPN policy failed")
        Assertion.assert_equal('2', resp['proposal']['ike']['dh_group'], "ERR: check VPN policy failed")

    def test_03_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_04_add_vpn_policy_can_be_edit(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['pri_gate'] = '1.1.1.1'
        ref1['ike_dh_group'] = '1'
        ref1['ike_auth'] = 'sha-256'
        ref1['ike_encryption'] = 'triple-des'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_05_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['site_to_site']
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('1.1.1.1', resp['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('triple-des', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")
        Assertion.assert_equal('sha-256', resp['proposal']['ike']['authentication'], "ERR: check VPN policy failed")
        Assertion.assert_equal('1', resp['proposal']['ike']['dh_group'], "ERR: check VPN policy failed")

    def test_06_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1745860(Test):
    uuid = "SOSAIOT-TC-54370"
    description = show_testcase_info(TESTPLAN, '1745860', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1745860')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_cannot_be_edit(self):
        cmds = ['configure',
                'vpn policy tunnel-interface 333',
                'gateway primary 3.3.3.3',
                'auth-method shared-secret',
                'shared-secret 123456',
                'commit',
                'end',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        Assertion.assert_equal('333', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('3.3.3.3', resp['gateway']['primary'], "ERR: check VPN policy failed")
        Assertion.assert_equal('aes-256', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")
        Assertion.assert_equal('sha-256', resp['proposal']['ike']['authentication'], "ERR: check VPN policy failed")
        Assertion.assert_equal('2', resp['proposal']['ike']['dh_group'], "ERR: check VPN policy failed")

    def test_03_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1786222(Test):
    uuid = "SOSAIOT-TC-54379"
    description = show_testcase_info(TESTPLAN, '1786222', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1786222')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['ike_dh_group'] = '14'
        ref1['prf'] = 'hmac-sha-256'
        ref1['ike_encryption'] = 'aes-gcm16-256'
        ref2['ike_dh_group'] = '14'
        ref2['prf'] = 'hmac-sha-256'
        ref2['ike_encryption'] = 'aes-gcm16-256'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_test_log(self):
        log_list = ['943\s+VPN\s+VPN IKEv2\s+Accept IKE SA Proposal']
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_04_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'prf' : 'hmac-sha-384',
            'ike_encryption' : 'aes-gcm16-128',
        }
        edit_ref2 = {
            'type': 'site_to_site',
            'name': 'vpn2',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'prf' : 'hmac-sha-384',
            'ike_encryption' : 'aes-gcm16-128',
        }
        rc1 = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        rc2 = Rvpn_obj.edit_vpn_policy(**edit_ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_05_test_log(self):
        reg1 = "'Phase 1 Encryption' , vpn1, changed from \[AESGCM16-256\], changed to \[AESGCM16-128\]"
        reg2 = "'Phase 1 Authentication' , vpn1, changed from \[SHA256\], changed to \[SHA384\]"
        log_list = [str(reg1), str(reg2)]
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_06_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'prf' : 'hmac-sha-512',
            'ike_encryption' : 'aes-gcm16-192',
        }
        edit_ref2 = {
            'type': 'site_to_site',
            'name': 'vpn2',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'prf' : 'hmac-sha-512',
            'ike_encryption' : 'aes-gcm16-192',
        }
        rc1 = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        rc2 = Rvpn_obj.edit_vpn_policy(**edit_ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_07_test_log(self):
        str1 = "'Phase 1 Encryption' , vpn1, changed from \[AESGCM16-128\], changed to \[AESGCM16-192\]"
        str2 = "'Phase 1 Authentication' , vpn1, changed from \[SHA384\], changed to \[SHA512\]"
        log_list = [str1, str2]        
        rc = check_traffic.check_test_log_list(log_list)
        Assertion.assert_equal(rc, True, "ERR: check test log failed")

    def test_08_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826682(Test):
    uuid = "SOSAIOT-TC-54386"
    description = show_testcase_info(TESTPLAN, '1826682', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826682')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'triple_des'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp1 = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp1['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp1['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['triple_des'], "ERR: check VPN policy failed")

    def test_03_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'ipsec_encryption' : 'aes_gmac_128',
        }
        rc = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')

    def test_04_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['aes_gmac_128'], "ERR: check VPN policy failed")
        Assertion.assert_equal({}, resp['ipv4']['site_to_site']['proposal']['ipsec']['authentication'], "ERR: check VPN policy failed")

    def test_05_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'ipsec_encryption' : 'aes_gmac_256',
        }
        rc = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')

    def test_06_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['aes_gmac_256'], "ERR: check VPN policy failed")
        Assertion.assert_equal({}, resp['ipv4']['site_to_site']['proposal']['ipsec']['authentication'], "ERR: check VPN policy failed")

    def test_07_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_08_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'triple_des'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_09_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp1 = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp1['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp1['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['triple_des'], "ERR: check VPN policy failed")

    def test_10_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'ipsec_encryption' : 'aes_gcm16_128',
        }
        rc = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')

    def test_11_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['aes_gcm16_128'], "ERR: check VPN policy failed")
        Assertion.assert_equal({}, resp['ipv4']['site_to_site']['proposal']['ipsec']['authentication'], "ERR: check VPN policy failed")

    def test_12_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref1 = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'ipsec_encryption' : 'aes_gcm16_256',
        }
        rc = Lvpn_obj.edit_vpn_policy(**edit_ref1)
        Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')

    def test_13_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp = res['vpn']['policy'][0]
        Assertion.assert_equal('vpn1', resp['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['aes_gcm16_256'], "ERR: check VPN policy failed")
        Assertion.assert_equal({}, resp['ipv4']['site_to_site']['proposal']['ipsec']['authentication'], "ERR: check VPN policy failed")

    def test_14_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826636(Test):
    uuid = "SOSAIOT-TC-54380"
    description = show_testcase_info(TESTPLAN, '1826636', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826636')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Lvpn)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'aes_gmac_128'
        ref2['name'] = 'vpn2'
        ref2['ipsec_encryption'] = 'triple_des'
        ref2['remote_net_name'] = remote_l2['name']
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Lvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_s2svpnpolicy()
        resp1 = res['vpn']['policy'][0]
        resp2 = res['vpn']['policy'][1]
        Assertion.assert_equal('vpn1', resp1['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp1['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['aes_gmac_128'], "ERR: check VPN policy failed")
        Assertion.assert_equal('vpn2', resp2['ipv4']['site_to_site']['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp2['ipv4']['site_to_site']['proposal']['ipsec']['encryption']['triple_des'], "ERR: check VPN policy failed")

    def test_03_edit_vpn_policy(self):
        LogObj.clear_log()
        edit_ref2 = {
            'type': 'site_to_site',
            'name': 'vpn2',
            'auth_mode': 'shared_secret',
            'edit_proposal': True,
            'ipsec_encryption' : 'aes_gmac_128',
        }
        rc = Lvpn_obj.edit_vpn_policy(**edit_ref2)
        Assertion.assert_equal(rc, True, 'edit VPN Policy Failed.')

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826637(Test):
    uuid = "SOSAIOT-TC-54381"
    description = show_testcase_info(TESTPLAN, '1826637', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826637')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'aes_gmac_128'
        ref2['name'] = 'vpn2'
        ref2['ipsec_encryption'] = 'aes_gmac_128'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826639(Test):
    uuid = "SOSAIOT-TC-54383"
    description = show_testcase_info(TESTPLAN, '1826639', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826639')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['name'] = 'vpn1'
        ref1['ike_exchange'] = 'main'
        ref1['ipsec_encryption'] = 'aes_gmac_128'
        ref2['name'] = 'vpn2'
        ref2['ike_exchange'] = 'main'
        ref2['ipsec_encryption'] = 'aes_gmac_128'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826640(Test):
    uuid = "SOSAIOT-TC-54384"
    description = show_testcase_info(TESTPLAN, '1826640', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826640')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['name'] = 'vpn1'
        ref1['ike_exchange'] = 'aggressive'
        ref1['ipsec_encryption'] = 'aes_gmac_128'
        ref2['name'] = 'vpn2'
        ref2['ike_exchange'] = 'aggressive'
        ref2['ipsec_encryption'] = 'aes_gmac_128'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1968641(Test):
    uuid = "SOSAIOT-TC-54390"
    description = show_testcase_info(TESTPLAN, '1968641', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1968641')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'triple_des'
        ref2['name'] = 'vpn2'
        ref1['ipsec_encryption'] = 'triple_des'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_2649618(Test):
    uuid = "SOSAIOT-TC-54394"
    description = show_testcase_info(TESTPLAN, '2649618', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2649618')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_3rd)
        ref2 = copy.deepcopy(Rvpn_3rd)
        ref1['name'] = 'vpn1'
        ref2['name'] = 'vpn2'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1826638(Test):
    uuid = "SOSAIOT-TC-54382"
    description = show_testcase_info(TESTPLAN, '1826638', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1826638')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'aes_gmac_256'
        ref2['name'] = 'vpn2'
        ref2['ipsec_encryption'] = 'aes_gmac_256'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")
    
    def test_03_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_04_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_05_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1968621(Test):
    uuid = "SOSAIOT-TC-54387"
    description = show_testcase_info(TESTPLAN, '1968621', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1968621')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['name'] = 'vpn1'
        ref1['ike_encryption'] = 'aes-gcm16-256'
        ref1['prf'] = 'hmac-sha-256'
        ref2['name'] = 'vpn2'
        ref2['ike_encryption'] = 'aes-gcm16-256'
        ref2['prf'] = 'hmac-sha-256'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")
    
    def test_03_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_04_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('aes-gcm16-256', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")

    def test_05_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1968622(Test):
    uuid = "SOSAIOT-TC-54388"
    description = show_testcase_info(TESTPLAN, '1968622', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1968622')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'aes_gmac_256'
        ref2['name'] = 'vpn2'
        ref2['ipsec_encryption'] = 'aes_gmac_256'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")
    
    def test_03_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_04_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['proposal']['ipsec']['encryption']['aes_gmac_256'], "ERR: check VPN policy failed")

    def test_05_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_06_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1968623(Test):
    uuid = "SOSAIOT-TC-54389"
    description = show_testcase_info(TESTPLAN, '1968623', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1968623')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref2 = copy.deepcopy(Rvpn_TI_3rd)
        ref1['name'] = 'vpn1'
        ref1['ipsec_encryption'] = 'aes_gmac_256'
        ref2['name'] = 'vpn2'
        ref2['ipsec_encryption'] = 'aes_gmac_256'
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_add_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add Local Route Policy'))
        rc = fw_cli.do_cli_commands(route_policy1)
        logger.info(" {} ".center(20, '-').format('Add Remote Route Policy'))
        rc &= rm_cli.do_cli_commands(route_policy2)
        Assertion.assert_equal(rc, True, "ERR: Add Route Policy failed")
    
    def test_03_check_vpn_ping(self):
        rc = check_traffic.ping_from_local_to_remote()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_04_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        Assertion.assert_equal('vpn1', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['proposal']['ipsec']['encryption']['aes_gmac_256'], "ERR: check VPN policy failed")

    def test_05_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn_TI_3rd)
        ref1['name'] = 'vpn3'
        ref1['pri_gate'] = Parameter.REMOTEX2
        ref1['ipsec_encryption'] = 'aes_gmac_128'
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_06_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][1]['ipv4']['tunnel_interface']
        # logger.info(resp)
        Assertion.assert_equal('vpn3', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal(True, resp['proposal']['ipsec']['encryption']['aes_gmac_128'], "ERR: check VPN policy failed")

    def test_07_del_Route_Policy(self):
        logger.info(" {} ".center(20, '-').format('Del Local Route Policy'))
        rc = LRoutePolicyObj.del_route_policy_by_name(name='ti_route1')
        logger.info(" {} ".center(20, '-').format('Del Remote Route Policy'))
        rc &= RRoutePolicyObj.del_route_policy_by_name(name='ti_route2')
        Assertion.assert_equal(rc, True, "ERR: Del Route Policy failed")

    def test_08_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1768530(Test):
    uuid = "SOSAIOT-TC-54378"
    description = show_testcase_info(TESTPLAN, '1768530', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1768530')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy_cannot_be_edit(self):
        cmds = ['configure',
                'vpn policy tunnel-interface test_main',
                'gateway primary 3.3.3.3',
                'auth-method shared-secret',
                'shared-secret 123456',
                'exit',
                'proposal ike exchange main',
                'proposal ike encryption aes-gcm16-192',
                'commit',
                'end',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, False, 'Add VPN Policy Failed.')

    def test_02_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        # logger.info(resp)
        Assertion.assert_equal('test_main', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('main', resp['proposal']['ike']['exchange'], "ERR: check VPN policy failed")
        Assertion.assert_not_equal('aes-gcm16-192', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")

    def test_03_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_04_add_vpn_policy_cannot_be_edit(self):
        cmds = ['configure',
                'vpn policy tunnel-interface test_agg',
                'gateway primary 3.3.3.3',
                'auth-method shared-secret',
                'shared-secret 123456',
                'exit',
                'proposal ike exchange aggressive',
                'proposal ike encryption aes-gcm16-192',
                'commit',
                'end',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, False, 'Add VPN Policy Failed.')

    def test_05_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        Assertion.assert_equal('test_agg', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('aggressive', resp['proposal']['ike']['exchange'], "ERR: check VPN policy failed")
        Assertion.assert_not_equal('aes-gcm16-192', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")

    def test_06_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_07_add_vpn_policy_cannot_be_edit(self):
        cmds = ['configure',
                'vpn policy tunnel-interface test_ikev2',
                'gateway primary 3.3.3.3',
                'auth-method shared-secret',
                'shared-secret 123456',
                'exit',
                'proposal ike exchange ikev2',
                'proposal ike encryption aes-gcm16-192',
                'commit',
                'end',
                'exit',
            ]
        rc = fw_cli.do_cli_commands(cmds)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_08_check_vpn_policy(self):
        res = Lvpn_obj.show_tunnelvpnpolicy()
        resp = res['vpn']['policy'][0]['ipv4']['tunnel_interface']
        # logger.info(resp)
        Assertion.assert_equal('test_ikev2', resp['name'], "ERR: check VPN policy failed")
        Assertion.assert_equal('ikev2', resp['proposal']['ike']['exchange'], "ERR: check VPN policy failed")
        Assertion.assert_equal('aes-gcm16-192', resp['proposal']['ike']['encryption'], "ERR: check VPN policy failed")

    def test_09_remove_vpn_policy(self):
        rc = Lvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')


class TestIKEv2_TP778_1522663(Test):
    uuid = "SOSAIOT-TC-54352"
    description = show_testcase_info(TESTPLAN, '1522663', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1522663')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_vpn_policy(self):
        LogObj.clear_log()
        ref1 = copy.deepcopy(Lvpn)
        ref2 = copy.deepcopy(Rvpn)
        ref1['local_ike_type'] = 'ipv4'
        ref1['peer_ike_type'] = 'ipv4'
        ref1['local_ike_id'] = Parameter.DUT
        ref1['peer_ike_id'] = Parameter.REMOTEX0
        ref2['local_ike_type'] = 'ipv4'
        ref2['peer_ike_type'] = 'ipv4'
        ref2['local_ike_id'] = Parameter.REMOTEX0
        ref2['peer_ike_id'] = Parameter.DUT
        rc1 = Lvpn_obj.add_vpn_policy(**ref1)
        rc2 = Rvpn_obj.add_vpn_policy(**ref2)
        Assertion.assert_equal(rc1 & rc2, True, 'Add VPN Policy Failed.')

    def test_02_check_vpn_ping(self):
        rc = check_traffic.ping_from_remote_to_local()
        Assertion.assert_equal(rc, True, "ERR: check vpn ping failed")

    def test_03_remove_vpn_policy(self):
        rc1 = Lvpn_obj.del_all_vpn_policies()
        rc2 = Rvpn_obj.del_all_vpn_policies()
        Assertion.assert_equal(rc1 & rc2, True, 'Remove VPN Policy Failed.')
