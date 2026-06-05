# __author__: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/NAT_Policies_TP167_2')


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.nat_policy.TestNatPolicies_GUI_TC16',
        'testcases.nat_policy.TestNatPolicies_GUI_TC17',
        'testcases.nat_policy.TestNatPolicies_GUI_TC23',
        'testcases.nat_policy.TestNatPolicies_GUI_TC14',
        'testcases.nat_policy.TestNatPolicies_GUI_TC21',
        'testcases.nat_policy.TestNatPolicies_GUI_TC19',
        'testcases.nat_policy.TestNatPolicies_GUI_TC20',
        'testcases.nat_policy.TestNatPolicies_GUI_TC22',
        'testcases.nat_policy.TestNatPolicies_GUI_TC24',
        'testcases.nat_policy.TestNatPolicies_GUI_TC15',
        'testcases.nat_policy.TestNatPolicies_GUI_TC25',
        'testcases.nat_policy.TestNatPolicies_Fun_TC26',
        'testcases.nat_policy.TestNatPolicies_Fun_TC46',
        'testcases.nat_policy.TestNatPolicies_Fun_TC27',
        'testcases.nat_policy.TestNatPolicies_Fun_TC45',
        'testcases.nat_policy.TestNatPolicies_Fun_TC35',
        'testcases.nat_policy.TestNatPolicies_Fun_TC28',
        'testcases.nat_policy.TestNatPolicies_Fun_TC29',
        'testcases.nat_policy.TestNatPolicies_Fun_TC30',
        'testcases.nat_policy.TestNatPolicies_Fun_TC31',
        'testcases.nat_policy.TestNatPolicies_Fun_TC32',
        'testcases.nat_policy.TestNatPolicies_Fun_TC33',
        'testcases.nat_policy.TestNatPolicies_Fun_TC34',
        'testcases.nat_policy.TestNatPolicies_Fun_TC36',
        'testcases.nat_policy.TestNatPolicies_Fun_TC37',
        'testcases.nat_policy.TestNatPolicies_Fun_TC38',
        'testcases.nat_policy.TestNatPolicies_Fun_TC39',
        'testcases.nat_policy.TestNatPolicies_Fun_TC40',
        'testcases.nat_policy.TestNatPolicies_Fun_TC41',
        'testcases.nat_policy.TestNatPolicies_Fun_TC42',
        'testcases.nat_policy.TestNatPolicies_Fun_TC43',
        'testcases.nat_policy.TestNatPolicies_Fun_TC44',
        'testcases.nat_policy.TestNatPolicies_Fun_TC49',
        'testcases.nat_policy.TestNatPolicies_Fun_TC47',
        'testcases.nat_policy.TestNatPolicies_Fun_TC48',
        'testcases.nat_policy.TestNatPolicies_Fun_TC50',
        'testcases.nat_policy.TestNatPolicies_Fun_TC51',
        'testcases.nat_policy.TestNatPolicies_Fun_TC66',
        'testcases.nat_policy.TestNatPolicies_Fun_TC67',
        'testcases.nat_policy.TestNatPolicies_Fun_TC68',
        'testcases.nat_policy.TestNatPolicies_Fun_TC69',
        'testcases.nat_policy.TestNatPolicies_Fun_TC74',
        'testcases.nat_policy.TestNatPolicies_GUI_TC18',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
