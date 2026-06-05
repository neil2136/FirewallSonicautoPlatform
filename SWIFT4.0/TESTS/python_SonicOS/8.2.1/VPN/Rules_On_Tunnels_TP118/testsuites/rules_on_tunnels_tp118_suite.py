# __Author__:  jlian

import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + "/VPN/Rules_On_Tunnels_TP118")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_fw_conf',
        'definition.init_pc_conf',
        'definition.conf_vpn',
        'testcases.rules_on_tunnels_tp118.TestTC01_Deny_http_service_on_incoming_traffic_to_the_lan_zone',
        'testcases.rules_on_tunnels_tp118.TestTC13_Deny_http_service_on_incoming_traffic_to_the_dmz_zone',
        'testcases.rules_on_tunnels_tp118.TestTC03_Allow_ftp_service_on_incoming_traffic_to_the_LAN_zone',
        'testcases.rules_on_tunnels_tp118.TestTC07_Deny_ftp_service_on_incoming_traffic_to_the_LAN_zone',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
