# __author__: fnhu
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest


sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                '/Network/Routed_Mode_part2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUTByUI',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw.TestConfigFW',
        'definition.init_conf_pc.TestSetup_PCs',
        'testcases.Routed_Mode.Test_Update_TC74',
        'testcases.Routed_Mode.Test_VLAN_TC75',
        'testcases.Routed_Mode.Test_Portshield_TC76',
        'testcases.Routed_Mode.Test_Ipv6_TC77',
        'testcases.Routed_Mode.Test_Reboot_TC78',
        'testcases.Routed_Mode.Test_TSR_TC79',
        'testcases.Routed_Mode.Test_EXP_TC80',
        'testcases.Routed_Mode.Test_CLI_TC_81',

    ]

    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
