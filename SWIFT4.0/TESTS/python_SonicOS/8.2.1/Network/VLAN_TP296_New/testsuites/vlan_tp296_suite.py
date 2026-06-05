import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/VLAN_TP296_New/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.vlan_tp296.TestVLAN_Maximum_numbers_of_VLAN_in_same_parent_interface',
        'testcases.vlan_tp296.TestVLAN_Maximum_numbers_of_VLAN_in_different_parent_interface',
        'testcases.vlan_tp296.TestVLAN_Non_TC_delete_sub_interface',
        'testcases.vlan_tp296.TestVLAN_Modifying_management_rules',
        'testcases.vlan_tp296.TestVLAN_VLAN_items_in_TSR',
        'testcases.vlan_tp296.TestVLAN_Parent_interface_in_WLAN_zone',
        'testcases.vlan_tp296.TestVLAN_Using_duplicate_VLAN_Tag',
        'testcases.vlan_tp296.TestVLAN_Using_invalid_VLAN_Tag',
        'testcases.vlan_tp296.TestVLAN_Using_Overlap_networks',
        'testcases.vlan_tp296.TestVLAN_Modifying_VLAN_Tag',
        'testcases.vlan_tp296.TestVLAN_Modifying_zone_assignment',
        'testcases.vlan_tp296.TestVLAN_Different_parent_interface_and_same_zone',
        'testcases.vlan_tp296.TestVLAN_Modifying_parent_interface',
        'testcases.vlan_tp296.TestVLAN_Modifying_IP_Address_Subnet_Mask',
        'testcases.vlan_tp296.TestVLAN_Modifying_user_login_rules',
        'testcases.vlan_tp296.TestVLAN_Different_parent_interface_and_different_zone',
        'testcases.vlan_tp296.TestVLAN_VLAN_Preference_support',
        'testcases.vlan_tp296.TestVLAN_Parent_interface_in_custom_zone',
        'testcases.vlan_tp296.TestVLAN_Parent_interface_in_Transparent_mode',
        'testcases.vlan_tp296.TestVLAN_Verify_traffic_statistics_of_vlan_interfaces',
        'testcases.vlan_tp296.TestVLAN_Management_traffic_PING',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    to_users = 'gkatti@sonicwall.com'
    cc_users = 'kskarkera@sonicwall.com'
    st = UnittestSuite(sys.argv, suite(), to_users)
    st.run()
