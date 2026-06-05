# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Upgrade/Feature_Upgrade_Gen7_VPN')


def suite():
    testcases_list = [
        'definition.init_conf_fw.Test_init_RemoteFW',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.Test_init_LocalFW',
        'testcases.Feature_Upgrade.TestUpgradeToPreviousFirmware',
        'testcases.Feature_Upgrade.TestConfigureOldFirmware',
        'definition.init_sslvpn_config',
        'testcases.Feature_Upgrade.Test_UpgradeUnderTestFirmwareViaUI',
        'testcases.Feature_Upgrade.TestWLB_TC031',
        'testcases.Feature_Upgrade.TestWLB_TC032',
        'testcases.Feature_Upgrade.TestTunnel_TC039',
        'testcases.Feature_Upgrade.TestTunnel_TC040',
        'testcases.Feature_Upgrade.TestS2S_VPN_TC043',
        'testcases.Feature_Upgrade.TestS2S_VPN_TC044',
        'testcases.Feature_Upgrade.TestSSLVPN_TC045',
        'testcases.Feature_Upgrade.TestSSLVPN_TC046',
        'testcases.Feature_Upgrade.TestULA_TC049',
        'testcases.Feature_Upgrade.TestULA_TC050',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
