# __Author__: lezhang
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Log/Configuration_Audit_General/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.initial_config_fw',
        'definition.initial_config_pc',
        'testcases.Configuration_Audit_General.TestUI_01',
        'testcases.Configuration_Audit_General.TestBaseMail_04',
        'testcases.Configuration_Audit_General.TestBaseExport_06',
        'testcases.Configuration_Audit_General.TestBaseConsole_08',
        'testcases.Configuration_Audit_General.TestBaseLog_30',
        'testcases.Configuration_Audit_General.TestBaseDisable_41',
        'testcases.Configuration_Audit_General.TestBaseEnable_44',
        'testcases.Configuration_Audit_General.TestBaseReboot_47',
        'testcases.Configuration_Audit_General.TestBaseEXP_56',
    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
