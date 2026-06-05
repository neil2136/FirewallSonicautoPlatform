# Author: cyuan
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/SAML_Profile_Settings')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_config_fw',
        'definition.init_config_pc',
        "testcases.saml_profile_settings_part1.Test_TC01",  
        "testcases.saml_profile_settings_part1.Test_TC02",  
        "testcases.saml_profile_settings_part1.Test_TC03",  
        "testcases.saml_profile_settings_part1.Test_TC04",  
        "testcases.saml_profile_settings_part1.Test_TC05",  
        "testcases.saml_profile_settings_part1.Test_TC06",  
        "testcases.saml_profile_settings_part1.Test_TC07",  
        "testcases.saml_profile_settings_part1.Test_TC08",  
        "testcases.saml_profile_settings_part1.Test_TC09",  
        "testcases.saml_profile_settings_part1.Test_TC10",  
        "testcases.saml_profile_settings_part1.Test_TC11",
        "testcases.saml_profile_settings_part1.Test_TC12",
        "testcases.saml_profile_settings_part1.Test_TC13",
        "testcases.saml_profile_settings_part1.Test_TC14",
        "testcases.saml_profile_settings_part1.Test_TC15",
        "testcases.saml_profile_settings_part1.Test_TC16",
        "testcases.saml_profile_settings_part1.Test_TC17",
        "testcases.saml_profile_settings_part1.Test_TC18",
        "testcases.saml_profile_settings_part1.Test_TC19",
        "testcases.saml_profile_settings_part1.Test_TC20",
        "testcases.saml_profile_settings_part1.Test_TC21",
        "testcases.saml_profile_settings_part1.Test_TC22",
        "testcases.saml_profile_settings_part1.Test_TC23",
        "testcases.saml_profile_settings_part1.Test_TC24",
        "testcases.saml_profile_settings_part1.Test_TC25",
        "testcases.saml_profile_settings_part1.Test_TC26",
        "testcases.saml_profile_settings_part1.Test_TC27",
        "testcases.saml_profile_settings_part1.Test_TC28",
        "testcases.saml_profile_settings_part1.Test_TC29",
        "testcases.saml_profile_settings_part1.Test_TC30",
        "testcases.saml_profile_settings_part1.Test_TC31",
        "testcases.saml_profile_settings_part1.Test_TC32",
        "testcases.saml_profile_settings_part1.Test_TC33",
        "testcases.saml_profile_settings_part1.Test_TC34",
        "testcases.saml_profile_settings_part1.Test_TC35",
        "testcases.saml_profile_settings_part1.Test_TC36",
        "testcases.saml_profile_settings_part1.Test_TC37",
        "testcases.saml_profile_settings_part1.Test_TC38",
        "testcases.saml_profile_settings_part1.Test_TC39",
        "testcases.saml_profile_settings_part1.Test_TC40",
        "testcases.saml_profile_settings_part1.Test_TC41",
        "testcases.saml_profile_settings_part1.Test_TC42",
        "testcases.saml_profile_settings_part1.Test_TC43",
        "testcases.saml_profile_settings_part1.Test_TC44",
        "testcases.saml_profile_settings_part1.Test_TC45",
        "testcases.saml_profile_settings_part1.Test_TC46",
        "testcases.saml_profile_settings_part1.Test_TC47",
        "testcases.saml_profile_settings_part1.Test_TC48"
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
