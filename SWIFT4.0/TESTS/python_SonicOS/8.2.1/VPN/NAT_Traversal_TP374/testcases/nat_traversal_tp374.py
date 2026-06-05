from definition.settings import *
from definition.utils import *


# Expect: Function: Initiator behind NAT - Manual Key
class TestNAT_Traversal_TC11(Test):
    uuid = "SOSAIOT-TC-54495"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_add_manual_vpn_on_local(self):
        man_local = {
            "type": "site_to_site",
            "name": "test_manual_local",
            'enable': True,
            "auth_mode": "manual",
            'pri_gate': "12.12.1.102",
            "ipversion": "ipv4",
            "local_net_type": "name",
            'local_net_name': "X0 Subnet",
            'remote_net_type': "name",
            "remote_net_name": "rem_sub_net",
            'ipsec_protocol':'esp',
            'ipsec_encryption': "des",
            'ipsec_auth': "none",
            'in_spi': "0x123",
            'out_spi': "0x456",
            'encryption_key': "1234567890123456"
        }
        res = vpn_api.add_vpn_policy(**man_local)
        Assertion.assert_equal(res, True, "ERR: add manual key vpn rule on local failed")

    def test_02_add_manual_vpn_on_remote(self):
        man_rem = {
            "type": "site_to_site",
            "name": "test_manual_rem",
            'enable': True,
            "auth_mode": "manual",
            'pri_gate': "12.12.1.101",
            "ipversion": "ipv4",
            "local_net_type": "name",
            'local_net_name': "X2 Subnet",
            'remote_net_type': "name",
            "remote_net_name": "local_sub_net",
            'ipsec_protocol': 'esp',
            'ipsec_encryption': "des",
            'ipsec_auth': "none",
            'in_spi': "0x456",
            'out_spi': "0x123",
            'encryption_key': "1234567890123456"
        }
        res = vpn_rem_api.add_vpn_policy(**man_rem)
        Assertion.assert_equal(res, True, "ERR: add manual key vpn rule on remote failed")

    @repeat_method(5)
    def test_03_check_traffic(self):
        time.sleep(30)
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")


# Expect: Responder behind NAT - Manual Key
class TestNAT_Traversal_TC17(Test):
    uuid = "SOSAIOT-TC-54498"
    description = show_testcase_info(TESTPLAN, '17', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_traffic_from_rem(self):
        res = pc2_login.ping(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from remote failed.")


# Expect: Function: Both Initiator and Responder behind NAT - Manual Key
class TestNAT_Traversal_TC23(Test):
    uuid = "SOSAIOT-TC-54501"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_traffic_from_local_and_rem(self):
        res1 = pc2_login.ping(PC1_ETH1_IP)
        logger.info(f'ping from local result: {res1}')
        res2 = pc1_login.ping(PC2_ETH1_IP)
        logger.info(f'ping from remote result: {res2}')
        Assertion.assert_equal(res1 and res2, True, "ERR: check vpn traffic failed.")


#Expect: Function: Initiator behind NAT - Initiator: Main mode with pershared secret; Responder: Main mode with Preshared secret
class TestNAT_Traversal_TC12(Test):
    uuid = "SOSAIOT-TC-54496"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_set_log_level_to_debug(self):
        res1 = log_set_api.logging_level(level='debug')
        logger.info(f'set log level on local firewall result: {res1}')
        res2 = log_set_rem_api.logging_level(level='debug')
        logger.info(f'set log level on remote firewall result: {res2}')
        Assertion.assert_equal(res1 and res2, True, 'ERR: set log level failed.')

    def test_03_clear_logs(self):
        cls_res1 = log_mon_api.clear_log()
        time.sleep(3)
        logger.info(f"clear logs on local firewall result: {cls_res1}")
        cls_res2 = log_mon_rem_api.clear_log()
        time.sleep(3)
        logger.info(f"clear logs on remote firewall result: {cls_res2}")
        Assertion.assert_equal(True, True, 'ERR: clear logs failed.')

    def test_04_add_main_mode_vpn_on_local(self):
        main_local = copy.deepcopy(s2s_local)
        main_local.update({"name": "main_mode_local", 'ike_exchange': "main"})
        res = vpn_api.add_vpn_policy(**main_local)
        Assertion.assert_equal(res, True, 'ERR: create main mode vpn on local failed.')

    def test_05_add_main_mode_vpn_on_remote(self):
        main_rem = copy.deepcopy(s2s_remote)
        main_rem.update({"name": "main_mode_remote", 'ike_exchange': "main"})
        res = vpn_rem_api.add_vpn_policy(**main_rem)
        Assertion.assert_equal(res, True, 'ERR: create main mode vpn on remote failed.')

    @repeat_method(10, 60)
    def test_06_check_traffic(self):
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")


# Expect: Function: Responder behind NAT - Initiator: Main mode with pershared secret; Responder: Main mode with Preshared secret
class TestNAT_Traversal_TC18(Test):
    uuid = "SOSAIOT-TC-54499"
    description = show_testcase_info(TESTPLAN, '18', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(10, 10)
    def test_01_check_traffic_from_remote(self):
        res = pc2_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check traffic from remote failed.")


# Expect: Function: Log message (Local IPSec Security Gateway behind a NAT device) local
class TestNAT_Traversal_TC2(Test):
    uuid = "SOSAIOT-TC-54500"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_logs_on_local(self):
        logs = log_mon_api.export_log_txt()
        Assertion.assert_regular(logs, 'Local IPsec Security Gateway behind a NAT/NAPT Device', "ERR: check log on local firewalll failed.")


# Expect: Function: Log message (Local IPSec Security Gateway behind a NAT device) remote
class TestNAT_Traversal_TC3(Test):
    uuid = "SOSAIOT-TC-54502"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_export_logs_on_remote(self):
        logs = log_mon_rem_api.export_log_txt()
        Assertion.assert_regular(logs, 'Peer IPsec Security Gateway behind a NAT/NAPT Device', "ERR: check log on local firewalll failed.")


# Expect:  Function: Initiator behind NAT - Initiator: Aggressive mode with Preshared secret; Responder: Aggressive mode with Preshared secret
class TestNAT_Traversal_TC15(Test):
    uuid = "SOSAIOT-TC-54497"
    description = show_testcase_info(TESTPLAN, '15', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_create_aggressive_mode_vpn_on_local(self):
        agg_local = copy.deepcopy(s2s_local)
        agg_local.update({"name": "agg_mode_local", 'ike_exchange': "aggressive"})
        res = vpn_api.add_vpn_policy(**agg_local)
        Assertion.assert_equal(res, True, 'ERR: create aggressive mode vpn on local failed.')

    def test_03_create_aggressive_mode_vpn_on_remote(self):
        agg_rem = copy.deepcopy(s2s_remote)
        agg_rem.update({"name": "agg_mode_rem", 'ike_exchange': "aggressive"})
        res = vpn_rem_api.add_vpn_policy(**agg_rem)
        Assertion.assert_equal(res, True, 'ERR: create aggressive mode vpn on remote failed.')

    @repeat_method(10, 60)
    def test_04_check_traffic(self):
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic on aggressive mode from local failed.")


# Expect:  Function: Initiator behind NAT - Initiator: IKEv2 mode with pershared secret; Responder: IKEv2 mode with pershared secret
class TestNAT_Traversal_TC37(Test):
    uuid = "SOSAIOT-TC-54506"
    description = show_testcase_info(TESTPLAN, '37', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_create_ikev2_mode_vpn_on_local(self):
        ikev2_local = copy.deepcopy(s2s_local)
        ikev2_local.update({"name": "ikev2_mode_local", 'ike_exchange': "ikev2"})
        res= vpn_api.add_vpn_policy(**ikev2_local)
        Assertion.assert_equal(res, True, 'ERR: create ikev2 vpn on local failed')

    def test_03_create_ikev2_mode_vpn_on_remote(self):
        ikev2_rem = copy.deepcopy(s2s_remote)
        ikev2_rem.update({"name": "ikev2_mode_remote", 'ike_exchange': "ikev2"})
        res = vpn_rem_api.add_vpn_policy(**ikev2_rem)
        Assertion.assert_equal(res, True, 'ERR: create ikev2 vpn on remote failed')

    @repeat_method(10, 60)
    def test_04_check_traffic(self):
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")


# Expect: Function: Responder behind NAT - Initiator: IKEv2 mode with pershared secret; Responder: IKEv2 mode with pershared secret
class TestNAT_Traversal_TC39(Test):
    uuid = "SOSAIOT-TC-54507"
    description = show_testcase_info(TESTPLAN, '39', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')
        
    @repeat_method(10, 60)
    def test_01_check_traffic_from_remote(self):
        res = pc2_login.ping(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from remote failed.")


# Expect: Function: Both Initiator and Responder behind NAT - Initiator: IKEv2 with pershared secret; Responder:IKEv2 with Preshared secret
class TestNAT_Traversal_TC42(Test):
    uuid = "SOSAIOT-TC-54508"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_check_traffic_from_local(self):
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, 'ERR: check traffic from local failed.')

    @repeat_method(10, 60)
    def test_02_check_traffic_from_remote(self):
        res = pc2_login.ping(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check traffic from remote failed.")


# Expect: Function: Both Initiator and Responder behind NAT - Initiator: IKEv2 with certificate; Responder:IKEv2 with certificate
class TestNAT_Traversal_TC43(Test):
    uuid = "SOSAIOT-TC-54509"
    description = show_testcase_info(TESTPLAN, '43', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '43')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_import_root_cert(self):
        res1 = cert_api.import_ca_cert(file=ca_cert_path)
        logger.info(f'import ca on local firewall result: {res1}')
        res2 = cert_rem_api.import_ca_cert(file=ca_cert_path)
        logger.info(f'import ca on remote firewall result: {res2}')
        Assertion.assert_equal(res1 and res2, True, 'ERR: import root cert on firewall failed')

    def test_03_import_local_cert(self):
        res1 = cert_api.import_cert_local(cert_path='@' + cert_path, name='my_cert', password='123456')
        logger.info(f'import cert on local firewall result: {res1}')
        res2 = cert_rem_api.import_cert_local_with_json(cert_path='@' + cert_path, name='my_cert', password='123456')
        logger.info(f'import cert on remote firewall result: {res2}')
        Assertion.assert_equal(res1 and res2, True, 'ERR: import certs failed.')

    def test_04_add_vpn(self):
        res1 = vpn_api.add_vpn_policy(**cert_local)
        logger.info(f'add vpn policy on local result: {res1}')
        res2 = vpn_rem_api.add_vpn_policy(**cert_remote)
        logger.info(f'add vpn policy on remote result: {res2}')
        Assertion.assert_equal(res1 and res2, True, 'ERR: add vpn on local failed')

    @repeat_method(10, 60)
    def test_05_init_traffic_from_local(self):
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")

    @repeat_method(10, 60)
    def test_06_init_traffic_from_remote(self):
        res = pc2_login.ping(PC1_ETH1_IP)
        Assertion.assert_equal(True, True, "ERR: check vpn traffic from remote failed.")


# Expect: Function: Tunnel Interface - Initiator Behind NAT - Initiator: Main mode with pershared secret; Responder: Main mode with Preshared secret
class TestNAT_Traversal_TC47(Test):
    uuid = "SOSAIOT-TC-54503"
    description = show_testcase_info(TESTPLAN, '47', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '47')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_add_main_mode_TI_vpn_on_local(self):
        cls_res = log_mon_api.clear_log()
        logger.info('clear log result: %s'%cls_res)
        ti_local = copy.deepcopy(ti_vpn_local)
        ti_local.update({'ike_exchange': "main"})
        res = vpn_api.add_vpn_policy(**ti_local)
        Assertion.assert_equal(res, True, 'ERR: add tunnel interface vpn on local failed.')

    def test_03_add_main_mode_TI_vpn_on_remote(self):
        ti_rem = copy.deepcopy(ti_vpn_remote)
        ti_rem.update({'ike_exchange': "main"})
        res = vpn_rem_api.add_vpn_policy(**ti_rem)
        Assertion.assert_equal(res, True, 'ERR: add tunnel interface vpn on remote failed.')

    def test_04_add_route_to_remote(self):
        route_rem = copy.deepcopy(route_vpn)
        route_rem["route_policies"][0]["ipv4"].update({"interface": "ti_remote", "source": {"name": "X2 Subnet"}, "destination": {"name": "local_sub_net"}})
        res = route_rem_api.add_route_policy(**route_rem)
        Assertion.assert_equal(res, True, "ERR: add route on remote failed.")

    def test_05_add_route_to_local(self):
        route_local = copy.deepcopy(route_vpn)
        route_local["route_policies"][0]["ipv4"].update({"interface": "ti_local", "source": {"name": "X0 Subnet"}, "destination": {"name": "rem_sub_net"}})
        res = route_api.add_route_policy(**route_local)
        Assertion.assert_equal(res, True, "ERR: add route on local failed.")

    @repeat_method(5)
    def test_06_check_traffic(self):
        time.sleep(60)
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")

    def test_07_check_negotiation_logs(self):
        time.sleep(30)
        logs = log_mon_api.export_log_txt()
        Assertion.assert_regular(logs, 'Tunnel Up', "ERR: check negotiation logs failed")


# Expect:Function: Tunnel Interface - Initiator Behind NAT - Initiator: IKEv2 mode with pershared secret; Responder: IKEv2 mode with Preshared secret
class TestNAT_Traversal_TC49(Test):
    uuid = "SOSAIOT-TC-54504"
    description = show_testcase_info(TESTPLAN, '49', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '49')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    def test_01_del_previous_vpn(self):
        res = del_vpn_policies()
        Assertion.assert_equal(res, True, 'ERR: delete previous vpn policy failed.')

    def test_02_add_TI_vpn_on_local(self):
        ti_local = copy.deepcopy(ti_vpn_local)
        ti_local.update({'ike_exchange': "ikev2"})
        res = vpn_api.add_vpn_policy(**ti_local)
        Assertion.assert_equal(res, True, 'ERR: add tunnel interface vpn on local failed.')

    def test_03_add_TI_vpn_on_remote(self):
        ti_rem = copy.deepcopy(ti_vpn_remote)
        ti_rem.update({'ike_exchange': "ikev2"})
        res = vpn_rem_api.add_vpn_policy(**ti_rem)
        Assertion.assert_equal(res, True, 'ERR: add tunnel interface vpn on local failed.')

    def test_04_add_route_to_remote(self):
        route_rem = copy.deepcopy(route_vpn)
        update_dict = {
            "interface": "ti_remote",
            "source": {"name": "X2 Subnet"},
            "destination": {"name": "local_sub_net"}
        }
        route_rem["route_policies"][0]["ipv4"].update(update_dict)
        res = route_rem_api.add_route_policy(**route_rem)
        Assertion.assert_equal(res, True, "ERR: add route on remote failed.")

    def test_05_add_route_to_local(self):
        route_local = copy.deepcopy(route_vpn)
        update_dict = {
            "interface": "ti_local",
            "source": {"name": "X0 Subnet"},
            "destination": {"name": "rem_sub_net"}
        }
        route_local["route_policies"][0]["ipv4"].update(update_dict)
        res = route_api.add_route_policy(**route_local)
        Assertion.assert_equal(res, True, "ERR: add route on local failed.")

    @repeat_method(5)
    def test_06_check_traffic(self):
        time.sleep(30)
        res = pc1_login.ping(PC2_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from local failed.")


# Expect: Function: Tunnel Interface - Both Behind NAT - Initiator: IKEv2 mode with pershared secret; Responder: IKEv2 mode with Preshared secret
class TestNAT_Traversal_TC52(Test):
    uuid = "SOSAIOT-TC-54510"
    description = show_testcase_info(TESTPLAN, '52', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, 'ERR: show testcases info failed')

    @repeat_method(3)
    def test_01_check_traffic(self):
        time.sleep(10)
        res = pc2_login.ping(PC1_ETH1_IP)
        Assertion.assert_equal(res, True, "ERR: check vpn traffic from remote failed.")
