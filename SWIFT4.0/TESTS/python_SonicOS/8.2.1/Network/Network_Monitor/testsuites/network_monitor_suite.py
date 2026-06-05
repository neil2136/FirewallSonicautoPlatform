# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/Network/Network_Monitor")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'testcases.network_monitor.TestTC57_Add_network_monitor_policy',
        'testcases.network_monitor.TestTC23_Edit_network_monitor_policy',
        'testcases.network_monitor.TestTC38_Probe_type_Ping',
        'testcases.network_monitor.TestTC40_Probe_type_ping_explicit',
        'testcases.network_monitor.TestTC39_Probe_type_TCP',
        'testcases.network_monitor.TestTC41_Probe_type_TCP_explicit',
        'testcases.network_monitor.TestTC42_Probe_target_of_host_type',
        'testcases.network_monitor.TestTC43_probe_target_of_range_type',
        'testcases.network_monitor.TestTC44_Probe_target_of_FQDN_type',
        'testcases.network_monitor.TestTC72_Add_nm_policy_in_cli',
        'definition.conf_vpn',
        'testcases.network_monitor.TestTC73_Verify_nm_over_vpn_numbered_ti',
        'testcases.network_monitor.TestTC74_Verify_nm_over_vpn_unnumbered_ti',
        'testcases.network_monitor.TestTC64_Import_and_export',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
