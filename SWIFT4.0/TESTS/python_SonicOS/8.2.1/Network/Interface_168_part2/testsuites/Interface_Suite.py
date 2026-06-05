# __author__: fnhu
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                '/Network/Interface_168_part2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW',
        'definition.init_conf_pc.TestSetup_PCs',
        'testcases.Interface.Test_http_login_with_LDAP_authtication_TC14',
        'testcases.Interface.Test_portshield_TC27',
        'testcases.Interface.Test_l2bridge_TC33',
        'testcases.Interface.Test_dmz_static_x4_TC62',
        'testcases.Interface.Test_dmz_transparent_x4_TC63',
        'testcases.Interface.Test_dmz_l2bridge_TC64',
        'testcases.Interface.Test_wan_static_TC55',
        'testcases.Interface.Test_wan_modify_TC56',
        'testcases.Interface.Test_dhcp_TC38',
        'testcases.Interface.Test_pppoe_connect_disconnect_TC41',
        'testcases.Interface.Test_pppoe_management_TC42',
        'testcases.Interface.Test_pptp_dhcp_TC46',
        'testcases.Interface.Test_pptp_connect_disconnect_TC48',
        'testcases.Interface.Test_l2tp_dhcp_TC52',
        'testcases.Interface.Test_l2tp_connect_disconnect_TC54',
        'testcases.Interface.Test_dhcp_x3_TC57',
        'testcases.Interface.Test_pppoe_x3_TC58',
        'testcases.Interface.Test_pptp_x3_TC59',
        'testcases.Interface.Test_l2tp_x3_TC60',
        'testcases.Interface.Test_ppp_lb_to_unassign_TC67',
        'testcases.Interface.Test_host_hearer_check_TC1000',


    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
