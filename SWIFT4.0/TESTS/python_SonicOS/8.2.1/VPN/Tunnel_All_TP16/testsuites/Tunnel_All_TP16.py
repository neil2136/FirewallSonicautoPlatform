import os
import sys
import unittest
from runner.unittest.suite import UnittestSuite

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/Tunnel_All_TP16')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.setup_network',
        'bin.conf_fw',
        'definition.conf_env.TestConfigTB',
        'testcases.Tunnel_All_TP16_TC.TestTunnel_All_TP16_01',
        'testcases.Tunnel_All_TP16_TC.TestTunnel_All_TP16_02',
        'testcases.Tunnel_All_TP16_TC.TestTunnel_All_TP16_03',
        'testcases.Tunnel_All_TP16_TC.TestTunnel_All_TP16_10',
        'testcases.Tunnel_All_TP16_TC.TestTunnel_All_TP16_08',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
