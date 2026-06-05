# __Author__: 'lezhang'
import os
import sys
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Interface_31bit_Addressing/')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.conf_fw',
        'definition.conf_remotefw',
        'testcases.interface_31bit_address.Test31bit_TC01',
        'testcases.interface_31bit_address.Test31bit_TC02',
        'testcases.interface_31bit_address.Test31bit_TC03',
        'testcases.interface_31bit_address.Test31bit_TC04',
        'testcases.interface_31bit_address.Test31bit_TC05',
        'testcases.interface_31bit_address.Test31bit_TC06',
        'testcases.interface_31bit_address.Test31bit_TC07',
        'testcases.interface_31bit_address.Test31bit_TC10',
        'testcases.interface_31bit_address.Test31bit_TC11',
        'testcases.interface_31bit_address.Test31bit_TC31',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
