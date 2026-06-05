# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/Address_Objects_TP158_part2")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.address_objects_tp158_part2.TestTC02_Create_new_range_objects_for_lan_zone',
        'testcases.address_objects_tp158_part2.TestTC03_Create_new_network_objects_for_lan_zone',
        'testcases.address_objects_tp158_part2.TestTC04_Create_new_host_objects_for_WAN_zone',
        'testcases.address_objects_tp158_part2.TestTC05_Create_new_range_objects_for_wan_zone',
        'testcases.address_objects_tp158_part2.TestTC06_Create_new_network_objects_for_wan_zone',
        'testcases.address_objects_tp158_part2.TestTC08_Create_new_range_objects_for_dmz_zone',
        'testcases.address_objects_tp158_part2.TestTC09_Create_new_network_objects_for_dmz_zone',
        'testcases.address_objects_tp158_part2.TestTC10_Create_new_host_objects_for_vpn_zone',
        'testcases.address_objects_tp158_part2.TestTC11_Create_new_range_objects_for_vpn_zone',
        'testcases.address_objects_tp158_part2.TestTC12_Create_new_network_objects_for_vpn_zone',
        'testcases.address_objects_tp158_part2.TestTC13_Create_new_host_objects_for_multicast_zone',
        'testcases.address_objects_tp158_part2.TestTC14_Create_new_range_objects_for_multicast_zone',
        'testcases.address_objects_tp158_part2.TestTC15_Create_new_network_objects_for_multicast_zone',
        'testcases.address_objects_tp158_part2.TestTC17_Create_new_range_objects_for_wlan_zone',
        'testcases.address_objects_tp158_part2.TestTC18_Create_new_network_objects_for_wlan_zone',
        'testcases.address_objects_tp158_part2.TestTC20_Create_addrss_group_negative_test',
        'testcases.address_objects_tp158_part2.TestTC21_Delete_address_objects',
        'testcases.address_objects_tp158_part2.TestTC22_Delete_address_groups',
        'testcases.address_objects_tp158_part2.TestTC27_Create_new_objects_for_fqdn',
        'testcases.address_objects_tp158_part2.TestTC28_Verify_fqdn_objects_can_be_resolved_successfully',
        'testcases.address_objects_tp158_part2.TestTC31_add_edit_delete_mac_ao',
        'testcases.address_objects_tp158_part2.TestTC32_Apply_mac_ao_into_content_filter_policy',
        'testcases.address_objects_tp158_part2.TestTC33_Apply_mac_ao_group_into_content_filter_policy',
        'testcases.address_objects_tp158_part2.TestTC34_Verify_ao_or_groups_can_be_modified_which_used_in_ip_helper_policy',
        'testcases.address_objects_tp158_part2.TestTC35_check_ipv4_ipv6_default_generated_aos',
        'testcases.address_objects_tp158_part2.TestTC36_Create_supergroup_that_use_other_address_groups_as_member',
        'testcases.address_objects_tp158_part2.TestTC23_Verify_default_address_objects',

        # new added case
        'definition.init_fw_conf',
        'testcases.address_objects_tp158_part2_new.TestTC24_verify_address_object_view',
        'testcases.address_objects_tp158_part2_new.TestTC01_new_verify_default_address_groups',
        'testcases.address_objects_tp158_part2_new.TestTC02_new_verify_filter_function',
        'testcases.address_objects_tp158_part2_new.TestTC03_new_verify_alert_pops_up_when_ao_groups_contain_each',
        'testcases.address_objects_tp158_part2_new.TestTC04_new_verify_create_new_object_with_special_address',
        'testcases.address_objects_tp158_part2_new.TestTC05_new_add_exist_custom_ao_and_ao_group',
        'testcases.address_objects_tp158_part2_new.TestTC06_new_add_exist_default_ao_and_ao_group',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
