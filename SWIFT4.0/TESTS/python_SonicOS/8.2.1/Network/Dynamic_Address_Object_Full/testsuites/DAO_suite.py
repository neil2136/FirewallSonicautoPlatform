# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +
                '/Network/Dynamic_Address_Object_Full')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.register_fw',
        'definition.init_conf_pc',
        'definition.init_conf_fw',
        'testcases.DAO.TestMACAO_TC02',
        'testcases.DAO.TestMACAO_TC01',
        'testcases.DAO.TestMACAO_TC04',
        'testcases.DAO.TestMACAO_TC06',
        'testcases.DAO.TestMACAO_TC08',
        'testcases.DAO.TestMACAO_TC15',
        'testcases.DAO.TestMACAO_TC09',
        'testcases.DAO.TestMACAO_TC10',
        'testcases.DAO.TestMACAO_TC05',
        'testcases.DAO.TestMACAO_TC12',
        'testcases.DAO.TestMACAO_TC11',
        'testcases.DAO.TestMACAO_TC21',
        'testcases.DAO.TestMACAO_TC13',
        'testcases.DAO.TestMACAO_TC14',
        'testcases.DAO.TestMACAO_TC18',
        'testcases.DAO.TestRebootDAO_TC19_TC38',
        'testcases.DAO.TestACLDAO_TC29',
        'testcases.DAO.TestACLDAO_TC30',

        
        'testcases.DAO.TestFQDNDAO_TC22',
        'testcases.DAO.TestFQDNDAO_TC28',
        'testcases.DAO.TestFQDNDAO_TC23',
        'testcases.DAO.TestFQDNDAO_TC24',
        'testcases.DAO.TestFQDNDAO_TC33',
        'testcases.DAO.TestFQDNDAO_TC34',
        'testcases.DAO.TestFQDNDAO_TC25',
        'testcases.DAO.TestFQDNDAO_TC26',

        # 'testcases.DAO.TestFQDNDAO_TC_FQDN_03',
        'testcases.DAO.TestFQDNDAO_TC_FQDN_04',

        'testcases.DAO.TestFQDNDAO_TC32',
        'testcases.DAO.TestFQDNDAO_TC35',
        'testcases.DAO.TestFQDNDAO_TC46',
        'testcases.DAO.TestFQDNDAO_TC36',
        'testcases.DAO.TestFQDNDAO_TC37',
        'testcases.DAO.TestCLIDAO_TC42',
        'testcases.DAO.TestCLIDAO_TC43',
        'testcases.DAO.TestFQDNAO_TC40',
        # 'testcases.DAO.TestMAXDAO_TC41',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
