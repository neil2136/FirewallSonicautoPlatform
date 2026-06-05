# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/IPv6_DHCP_server_TP2471")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',

        # about disable/enable/delete
        'testcases.ipv6_dhcp_server_tp2471.TestTC01_Verify_DHCPv6_Server_can_be_disabled_and_enabled',
        'testcases.ipv6_dhcp_server_tp2471.TestTC17_Verify_DHCPv6_server_single_dynamic_entry_can_be_deleted',
        'testcases.ipv6_dhcp_server_tp2471.TestTC18_Verify_DHCPv6_server_multiple_dynamic_entries_can_be_deleted',

        # input valid values for dynamic dhcpv6 scope
        'testcases.ipv6_dhcp_server_tp2471.TestTC02_Verify_valid_name_can_be_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC05_Verify_valid_dynamic_addresses_can_be_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC07_Verify_valid_prefix_is_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC09_Verify_valid_lifetime_value_is_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC11_Verify_valid_preferred_lifetime_value_is_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC12_Verify_comment_can_be_configured_successfully',
        'testcases.ipv6_dhcp_server_tp2471.TestTC14_Verify_valid_dns_value_can_be_configured_successfully',

        # input invalid values for dynamic dhcpv6 scope
        'testcases.ipv6_dhcp_server_tp2471.TestTC03_Verify_invalid_name_is_not_be_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC04_Verify_invalid_dynamic_range_is_not_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC06_Verify_invalid_prefix_value_is_not_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC08_Verify_invalid_valid_lifetime_value_is_not_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC10_Verify_invalid_preferred_lifetime_value_is_not_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC13_Verify_invalid_dns_value_is_not_allowed',
        'testcases.ipv6_dhcp_server_tp2471.TestTC16_Verify_invalid_domain_is_not_allowed',

        # function test
        'testcases.ipv6_dhcp_server_tp2471.TestTC15_Verify_DHCPv6_scope_with_inherit_dns',
        'testcases.ipv6_dhcp_server_tp2471.TestTC19_Check_IAID_in_each_DHCPv6_lease',
        'testcases.ipv6_dhcp_server_tp2471.TestTC20_Check_DUID_in_each_DHCPv6_lease',
        'testcases.ipv6_dhcp_server_tp2471.TestTC21_Verify_LAN_zone_with_statefull_mode',
        'testcases.ipv6_dhcp_server_tp2471.TestTC30_Verify_disable_DHCPv6_scope',
        'testcases.ipv6_dhcp_server_tp2471.TestTC33_Verify_multiple_client_in_same_interface',
        'testcases.ipv6_dhcp_server_tp2471.TestTC34_Verify_multiple_client_in_different_interface',
        'testcases.ipv6_dhcp_server_tp2471.TestTC39_Verify_client_number_bigger_than_scope_range',
        'testcases.ipv6_dhcp_server_tp2471.TestTC35_Verify_rapid_commit_option',
        'testcases.ipv6_dhcp_server_tp2471.TestTC28_Verify_DHCP_server_act_correct_at_t1_time',
        'testcases.ipv6_dhcp_server_tp2471.TestTC31_Verify_renew_ipv6_address',
        'testcases.ipv6_dhcp_server_tp2471.TestTC32_Verify_release_ipv6_address',
        'testcases.ipv6_dhcp_server_tp2471.TestTC45_Verify_send_Information_request_message',
        'testcases.ipv6_dhcp_server_tp2471.TestTC46_Verify_stateless_with_multiple_client_in_same_interface',
        'testcases.ipv6_dhcp_server_tp2471.TestTC51_Verify_exchange_between_stateless_and_stateful_mode',
        'testcases.ipv6_dhcp_server_tp2471.TestTC52_Verify_mix_stateless_and_stateful',
        'testcases.ipv6_dhcp_server_tp2471.TestTC58_Restart_dut',

        # function test: Message Validation
        'testcases.ipv6_dhcp_server_tp2471.TestTC22_Message_validation_in_dmz_zone',
        'testcases.ipv6_dhcp_server_tp2471.TestTC23_Message_validation_in_custom_zone',
        'testcases.ipv6_dhcp_server_tp2471.TestTC24_Message_validation_with_domain_name_info',
        'testcases.ipv6_dhcp_server_tp2471.TestTC25_Message_validation_with_dns_name',
        'testcases.ipv6_dhcp_server_tp2471.TestTC26_Message_validation_with_valid_lifetime_info',
        'testcases.ipv6_dhcp_server_tp2471.TestTC27_Message_validation_with_preferred_lifetime_info',

        # function test : dhcpv6 relay
        'testcases.ipv6_dhcp_server_tp2471.TestTC50_Stateless_dhcpv6_server_works_fine_with_relay_agent',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
