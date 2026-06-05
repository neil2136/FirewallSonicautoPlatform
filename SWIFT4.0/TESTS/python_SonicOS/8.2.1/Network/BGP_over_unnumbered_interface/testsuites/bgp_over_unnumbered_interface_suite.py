# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/BGP_over_unnumbered_interface")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'definition.conf_vpn',
        'testcases.bgp_over_unnumbered_interface.TestTC01_ibgp_over_unnumbered_vpn_can_established',
        'testcases.bgp_over_unnumbered_interface.TestTC02_ebgp_over_unnumbered_vpn_can_established',
        'testcases.bgp_over_unnumbered_interface.TestTC03_verify_route_for_advertised_network_prefix_is_added_in_gui_and_nsm',
        'testcases.bgp_over_unnumbered_interface.TestTC04_check_routing_information_by_zebos_command',
        'testcases.bgp_over_unnumbered_interface.TestTC05_check_bgp_summary_on_gui',
        'testcases.bgp_over_unnumbered_interface.TestTC08_verify_traffic_between_dut_and_network_learned_from_bgp_over_unnumbered_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC13_verify_connected_networks_can_be_advertised_via_bgp_over_unnumbered_tunnel_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC11_verify_static_networks_can_be_advertised_via_bgp_over_unnumbered_tunnel_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC15_verify_redistribute_ospf_routes_via_bgp_over_unnumbered_tunnel_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC19_verify_advertise_route_via_network_command_over_unnumbered_tunnel_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC22_verify_bgp_routes_interface_name_change_after_vpn_policy_name_changed',
        'testcases.bgp_over_unnumbered_interface.TestTC23_Verify_bgp_over_unnumbered_tunnel_interface_can_be_re_established',
        'testcases.bgp_over_unnumbered_interface.TestTC28_check_settings_intact_after_fw_restart',
        'testcases.bgp_over_unnumbered_interface.TestTC30_check_tsr',
        'testcases.bgp_over_unnumbered_interface.TestTC38_verify_bgp_over_unnumbered_tunnel_interface_when_update_source_interface_is_vlan_interface',
        'testcases.bgp_over_unnumbered_interface.TestTC40_verify_bgp_works_well_when_both_bgp_over_numbered_and_unnumbered_interfaces_configured',
        'testcases.bgp_over_unnumbered_interface.TestTC43_verify_bgp_can_establishes_over_unnumbered_interface_between_distant_duts',
        'testcases.bgp_over_unnumbered_interface.TestTC29_export_and_import_prefs_file',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
