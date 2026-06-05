# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/Dynamic_Route_Based_VPN-TP2438')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'testcases.DynamicRouteVPN.Test_addvpnenableOption_TC02',
        'testcases.DynamicRouteVPN.Test_disableOption_TC03',
        'testcases.DynamicRouteVPN.Test_enableOption_TC04',
        'testcases.DynamicRouteVPN.Test_enableOspf_TC08',
        'testcases.DynamicRouteVPN.Test_checkOspfPacket_TC59',
        'testcases.DynamicRouteVPN.Test_enableRip_TC06',
        'testcases.DynamicRouteVPN.Test_enableRip_TC37',
        'testcases.DynamicRouteVPN.Test_enableRip_TC30',
        'testcases.DynamicRouteVPN.Test_enableRip_TC21',
        'testcases.DynamicRouteVPN.Test_enableRip_TC28',
        'testcases.DynamicRouteVPN.Test_reboot_TC102',
        'testcases.DynamicRouteVPN.Test_disableVPN_TC10',
        'testcases.DynamicRouteVPN.Test_Ospf_TC68',
        'testcases.DynamicRouteVPN.Test_disableOspf_TC09',
        'testcases.DynamicRouteVPN.Test_disableRip_TC07',
        'testcases.DynamicRouteVPN.Test_enableRipBorrowedVlan_TC56',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
