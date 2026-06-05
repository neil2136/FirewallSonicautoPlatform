# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Upgrade/Feature_Upgrade_Gen7')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_conf_fw.TestConfigFW',
        'testcases.Feature_Upgrade.TestUpgradeToPreviousFirmware',
        'testcases.Feature_Upgrade.TestConfigureOldFirmware',
        'testcases.Feature_Upgrade.Test_UpgradeUnderTestFirmwareViaUI',
        'testcases.Feature_Upgrade.TestCFS_TC015',
        'testcases.Feature_Upgrade.TestCFS_TC016',
        'testcases.Feature_Upgrade.TestGAVIPSAntiSpyware_TC023',
        'testcases.Feature_Upgrade.TestGAVIPSAntiSpyware_TC024',
        'testcases.Feature_Upgrade.TestInterfacesZones_TC027',
        'testcases.Feature_Upgrade.TestInterfacesZones_TC028',
        'testcases.Feature_Upgrade.TestNat_TC035',
        'testcases.Feature_Upgrade.TestNat_TC036',
        'testcases.Feature_Upgrade.TestRoute_TC041',
        'testcases.Feature_Upgrade.TestRoute_TC042',
        'testcases.Feature_Upgrade.TestAccessrulesApprules_TC01',
        'testcases.Feature_Upgrade.TestAccessrulesApprules_TC02',
        'testcases.Feature_Upgrade.TestDPISSL01',
        'testcases.Feature_Upgrade.TestDPISSL02',
        'testcases.Feature_Upgrade.TestDNS_TC021',
        'testcases.Feature_Upgrade.TestDNS_TC022',
        'testcases.Feature_Upgrade.TestSyslog_TC063',
        'testcases.Feature_Upgrade.TestSyslog_TC064',
        'testcases.Feature_Upgrade.TestTime_TC065',
        'testcases.Feature_Upgrade.TestTime_TC066',
        'testcases.Feature_Upgrade.TestLogging_TC033',
        'testcases.Feature_Upgrade.TestLogging_TC034',
        'testcases.Feature_Upgrade.TestSNMP_TC067',
        'testcases.Feature_Upgrade.TestSNMP_TC068',
        'testcases.Feature_Upgrade.TestDHCPServer_TC019',
        'testcases.Feature_Upgrade.TestDHCPServer_TC020',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
