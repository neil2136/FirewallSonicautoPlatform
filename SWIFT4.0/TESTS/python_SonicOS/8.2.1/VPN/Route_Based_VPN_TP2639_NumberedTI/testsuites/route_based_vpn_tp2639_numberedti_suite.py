# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/VPN/Route_Based_VPN_TP2639_NumberedTI")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC08_tunnel_interface_is_shown_on_network_interfaces_page',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC12_tunnel_interface_is_shown_in_dynamic_routing_page',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC20_defaut_route_for_tunnel_interface_is_deleted_after_delete_ti',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC30_configure_ospf_on_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC31_establish_ospf_through_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC32_verify_ospf_traffic_over_tunnel_interface_after_add_access_rule',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC35_disable_ospf_on_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC24_learn_rip_route_through_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC52_tunnel_interface_cannot_be_deleted_if_enable_routing_protocols_on_it',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC37_bgp_vpn_to_vpn_accessrule_is_auto_added_when_bgp_is_enabled',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC38_configure_bgp_on_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC39_bgp_establishes_session_on_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC40_bgp_establishes_session_on_tunnel_interface_zebos',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC41_bgp_status_is_shown_in_bgp_summary_window',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC42_verify_bgp_traffic_over_tunnel_interface_after_add_access_rule',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC48_configure_static_route_based_vpn_on_numbered_tunnel_interface',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC53_tunnel_interface_cannot_be_deleted_if_static_route_with_it_exist',
        'testcases.route_based_vpn_tp2639_numberedti.TestTC63_tunnel_vpn_policy_cannot_be_deleted_if_it_is_used_by_tunnel_interface',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
