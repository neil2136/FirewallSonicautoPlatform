# __Author__: 'lezhang'
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Custom_Zones_TP440/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.custom_zones.TestNagetive_TC57832',
        'testcases.custom_zones.TestNagetive_TC57833',
        'testcases.custom_zones.TestCZones_TC01',
        'testcases.custom_zones.TestCZones_TC02',
        'testcases.custom_zones.TestCZones_TC03',
        'testcases.custom_zones.TestCZones_TC04',
        'testcases.custom_zones.TestCZones_TC06',
        'testcases.custom_zones.TestCZones_TC07',
        'testcases.custom_zones.TestCZones_TC08',
        'testcases.custom_zones.TestCZones_TC09',
        'testcases.custom_zones.TestCZones_TC10',
        'testcases.custom_zones.TestCZones_TC11',
        'testcases.custom_zones.TestCZones_TC12',
        'testcases.custom_zones.TestCZones_TC13',
        'testcases.custom_zones.TestCZones_TC14',
        'testcases.custom_zones.TestCZones_TC15',
        'testcases.custom_zones.TestCZones_TC16',
        'testcases.custom_zones.TestCZones_TC17',
        'testcases.custom_zones.TestCZones_TC18',
        'testcases.custom_zones.TestCZones_TC19',
        'testcases.custom_zones.TestCZones_TC20',
        'testcases.custom_zones.TestCZones_TC21',
        'testcases.custom_zones.TestCZones_TC22',
        'testcases.custom_zones.TestCZones_TC23',
        'testcases.custom_zones.TestCZones_TC24',
        'testcases.custom_zones.TestCZones_TC25',
        'testcases.custom_zones.TestCZones_TC26',
        'testcases.custom_zones.TestCZones_TC27',
        'testcases.custom_zones.TestCZones_TC28',
        'testcases.custom_zones.TestCZones_TC29',
        'testcases.custom_zones.TestCZones_TC30',
        'testcases.custom_zones.TestCZones_TC31',
        'testcases.custom_zones.TestCZones_TC32',
        'testcases.custom_zones.TestCZones_TC33',
        'testcases.custom_zones.TestCZones_TC34',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
