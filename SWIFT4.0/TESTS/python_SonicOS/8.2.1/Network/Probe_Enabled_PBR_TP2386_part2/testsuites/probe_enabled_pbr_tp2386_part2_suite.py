# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/Probe_Enabled_PBR_TP2386_part2")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf.TestInitConfig',
        'definition.init_pc_conf',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC01_GUI_functionality_format_check_for_name_field',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC10_GUI_functionality_edit_an_object_that_is_used_by_nm_policy',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC11_Negative_test_change_ao_used_by_nm_policy_to_a_wrong_type',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC14_GUI_functionality_boundary_check_for_port_option',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC15_GUI_functionality_format_check_for_probe_parameters',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC16_GUI_functionality_boundary_check_for_probe_interval',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC17_GUI_functionality_boundary_check_for_reply_timeout',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC18_GUI_functionality_boundary_check_for_failure_threshold',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC19_GUI_functionality_boundary_check_for_success_threshold',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC02_GUI_functionality_empty_name_is_not_allowed',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC20_GUI_functionality_all_must_respond_option_test',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC21_GUI_functionality_comment_field',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC25_Button_functionality_delete_all_nm_policies',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC26_Negative_test_delete_nm_policy_used_by_route',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC27_Button_functionality_clear_statistics',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC03_GUI_functionality_Policy_name_must_be_unique',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC04_GUI_functionality_max_length_of_the_name_field',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC08_GUI_functionality_Gateway_and_interface_can_be_specified',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC09_GUI_functionality_Delete_an_object_used_by_nm_policy',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC31_Auto_added_policies_can_not_be_deleted',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC32_Auto_added_nm_policies_can_be_edited_through_nat_policy',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC33_Auto_added_nm_policies_can_be_deleted_through_nat_policy',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC42_Probe_target_of_host_type',
        'testcases.probe_enabled_pbr_tp2386_part2.TestTC43_probe_target_of_range_type',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC44_Probe_target_of_FQDN_type',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC45_Probe_target_of_group_type',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC47_Functional_test_for_option_all_hosts_must_respond',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC57_Add_network_monitor_policy',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC58_Functional_test_for_option_disable_route_when_probe_succeeds',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC59_Functional_test_for_option_probe_default_state_is_up',
        # 'testcases.probe_enabled_pbr_tp2386_part2.TestTC72_Add_nm_policy_in_cli',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
