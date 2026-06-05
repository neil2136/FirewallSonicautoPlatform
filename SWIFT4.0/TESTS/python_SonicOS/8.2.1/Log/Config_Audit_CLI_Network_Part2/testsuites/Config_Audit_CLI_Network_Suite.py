# __Author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Log/Config_Audit_CLI_Network_Part2")

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestInitConfigFW',
        'definition.init_conf_pc.TestInitConfigPC',
        'testcases.Config_Audit_CLI_Network.TestIPHelper_TC01',
        'testcases.Config_Audit_CLI_Network.TestIPHelper_TC03',
        'testcases.Config_Audit_CLI_Network.TestIPHelper_TC06',
        'testcases.Config_Audit_CLI_Network.TestIPHelper_TC08',
        'testcases.Config_Audit_CLI_Network.TestWebProxy_TC13',
        'testcases.Config_Audit_CLI_Network.TestWebProxy_TC15',
        'testcases.Config_Audit_CLI_Network.TestDDNS_TC20',
        'testcases.Config_Audit_CLI_Network.TestDDNS_TC24',
        'testcases.Config_Audit_CLI_Network.TestDDNS_TC27',
        'testcases.Config_Audit_CLI_Network.TestNetworkMonitor_TC36',
        'testcases.Config_Audit_CLI_Network.TestNetworkMonitor_TC43',
        'testcases.Config_Audit_CLI_Network.TestNetworkMonitor_TC46',
        'testcases.Config_Audit_CLI_Network.TestNetworkMonitor_TC52',
        'testcases.Config_Audit_CLI_Network.TestMatchObjectsDynamicGroup_TC63',
        'testcases.Config_Audit_CLI_Network.TestMatchObjectsDynamicGroup_TC64',
        'testcases.Config_Audit_CLI_Network.TestMatchObjectsDynamicGroup_TC67',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
