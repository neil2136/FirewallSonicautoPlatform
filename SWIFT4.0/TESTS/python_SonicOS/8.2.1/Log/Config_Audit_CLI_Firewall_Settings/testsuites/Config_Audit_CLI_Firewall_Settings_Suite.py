# __Author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/Log/Config_Audit_CLI_Firewall_Settings")

def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestInitConfigFW',
        'definition.init_conf_pc.TestInitConfigPC',
        'testcases.Firewall_Settings.TestDetectionPrevention_TC01',
        'testcases.Firewall_Settings.TestDynamicPorts_TC61',
        'testcases.Firewall_Settings.TestBWM_TC16',
        'testcases.Firewall_Settings.TestBWM_TC18',
        'testcases.Firewall_Settings.TestFloodProtectionTCP_TC20',
        'testcases.Firewall_Settings.TestFloodProtectionTCP_TC22',
        'testcases.Firewall_Settings.TestFloodProtectionTCP_TC25',
        'testcases.Firewall_Settings.TestFloodProtectionUDP_TC28',
        'testcases.Firewall_Settings.TestQoSMapping_TC45',
        'testcases.Firewall_Settings.TestQoSMapping_TC47',
        'testcases.Firewall_Settings.TestSSLControl_TC48',
        'testcases.Firewall_Settings.TestSSLControl_TC49',
        'testcases.Firewall_Settings.TestSSLControl_TC51',
        'testcases.Firewall_Settings.TestFloodProtection_TC30',
        'testcases.Firewall_Settings.TestFloodProtection_TC37',
        'testcases.Firewall_Settings.TestAddVLANTranslation_TC72',
        'testcases.Firewall_Settings.TestDelVLANTranslation_TC74',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
