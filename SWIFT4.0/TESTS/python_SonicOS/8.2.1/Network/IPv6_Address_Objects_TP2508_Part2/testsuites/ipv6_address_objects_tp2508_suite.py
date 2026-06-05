# __Author__: 'qshi'
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_Address_Objects_TP2508_Part2/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'testcases.ipv6_address_objects_add_ao',
        'testcases.ipv6_address_objects_others.TestPurgeAll_TC2195470',
        'testcases.ipv6_address_objects_others.TestDefaultGWIpv6AOForWan_TC2195470',
        'testcases.ipv6_address_objects_others.TestDefaultGWIpv6AOForUnassignedWan_TC2195471',
        'testcases.ipv6_address_objects_others.TestDeleteAoUsedInPB_TC1527168',
        'testcases.ipv6_address_objects_others.TestExportImportAo_TC1527171',
        'testcases.ipv6_address_objects_others.TestRefreshAo_TC1527162'
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
