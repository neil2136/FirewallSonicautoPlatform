# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_VPN_TP2335/')


def suite():
    testcases_list = [
        'definition.init_vpn_settings.Test_init_RemoteFW',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestInitFW',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_vpn_settings.Test_SetupVPN',
        'testcases.Tunnel_VPN.TestStaticRouteConfig_TC22',
        'testcases.Tunnel_VPN.TestStaticRouteConfig_TC23',
        'testcases.Tunnel_VPN.TestStaticRouteConfig_TC24',
        'testcases.Tunnel_VPN.TestACLConfig_TC27',
        'testcases.Tunnel_VPN.TestStaticRouteConfig_TC30',
        'testcases.Tunnel_VPN.TestStaticRouteConfig_TC34',
        'testcases.Tunnel_VPN.TestTITraffic_TC54',
        'testcases.Tunnel_VPN.TestDHCPTraffic_TC78',
        'testcases.Tunnel_VPN.TestDHCPTraffic_TC79',
        'testcases.Tunnel_VPN.TestBoundInterface_TC107',
        'testcases.Tunnel_VPN.TestDifferentBoundTo_TC89',
        'testcases.Tunnel_VPN.TestSameBoundTo_TC90',
        'testcases.Tunnel_VPN.TestDiffBoundToTraffic_TC94',
        'testcases.Tunnel_VPN.TestChangeBoundTo_TC1563926',
        'testcases.Tunnel_VPN.TestRekey_TC61',
        'testcases.Tunnel_VPN.TestUnnumberTIConfig_TC100',
        'testcases.Tunnel_VPN.TestUnnumberTIConfig_TC103',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
