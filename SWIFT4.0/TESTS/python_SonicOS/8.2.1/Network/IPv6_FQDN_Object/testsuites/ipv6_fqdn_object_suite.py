# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/IPv6_FQDN_Object")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.ipv6_fqdn_object.TestTC01_add_ipv6_fqdn_ao',
        'testcases.ipv6_fqdn_object.TestTC04_add_ipv6_fqdn_ao_conclude_wildcard',
        'testcases.ipv6_fqdn_object.TestTC05_Test_option_refresh_sub_domains_of_wildcard_fqdn_address_objects_in_diag_page',
        'testcases.ipv6_fqdn_object.TestTC07_Function_test_when_the_resolved_ipv6_addresses_increased',
        'testcases.ipv6_fqdn_object.TestTC08_Function_test_when_the_resolved_ipv6_addresses_decreased',
        'testcases.ipv6_fqdn_object.TestTC10_Test_option_manually_set_dns_entries_ttl_on_ipv6_fqdn_ao_page',
        'testcases.ipv6_fqdn_object.TestTC12_Test_host_ttl_has_expired',
        'testcases.ipv6_fqdn_object.TestTC18_Log_support_added_host_entry_to_dynamic_address_object',
        'testcases.ipv6_fqdn_object.TestTC25_ipv6_fqdn_acl_deny_acl_lan_to_wan',
        'testcases.ipv6_fqdn_object.TestTC26_ipv6_fqdn_acl_allow_acl_lan_to_wan',
        'testcases.ipv6_fqdn_object.TestTC28_Add_fqdn_based_ipv6_network_monitor_policy_with_newly_created_fqdn_aos',
        'testcases.ipv6_fqdn_object.TestTC30_Add_a_FQDN_based_ipv6_network_monitor_policy',
        'testcases.ipv6_fqdn_object.TestTC50_edit_delete_ipv6_fqdn_ao',
        'testcases.ipv6_fqdn_object.TestTC49_tsr_test',
        'testcases.ipv6_fqdn_object.TestTC48_Restart_test',
        'testcases.ipv6_fqdn_object.TestTC47_Prefs_export_and_import_test'
    
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
