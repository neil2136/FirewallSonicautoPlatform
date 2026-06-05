# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/VPN/IKEv2_Dynamic_Client_Support_TP1339")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC01_check_default_ike_attributes_in_global_ikev2_policy',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC33_check_dynamic_client_ikev2_settings',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC34_check_default_dynamic_client_ikev2_proposal_in_cli',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC03_modify_ike_attributes_in_global_ikev2_policy',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC22_check_global_ike_settings_includes_aesgcm_encrytion',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC23_modify_ike_attributes_via_gui',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC24_modify_ike_attributes_via_cli',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC25_tsr',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC26_restart_test',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC27_prefs_export_and_import_test',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC09_negotiate_tunnel',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC14_rekey_event.test_04_check_system_logs',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC28_s2s_negotiate_aesgcm_encrytion',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC35_check_aesgcm_in_cli_when_tunnel_up',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC30_combination_test_s2s_negotiate_aesgcm_encrytion',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC32_s2s_auth_by_3rd_party_with_aesgcm',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC29_tunnel_negotiate_aesgcm_encrytion',
        'testcases.ikev2_dynamic_client_support_tp1339.TestTC31_combination_test_tunnel_negotiate_aesgcm_encrytion',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
