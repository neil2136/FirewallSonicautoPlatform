import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/Interface_168/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from testcases.Interface import *


def suite():
    testcases_list = [
       'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'testcases.Interface.Test_Interface_06',
        'testcases.Interface.Test_Interface_07',
        'testcases.Interface.Test_Interface_08',
        'testcases.Interface.Test_Interface_09',
        'testcases.Interface.Test_Interface_10',
        'testcases.Interface.Test_Interface_11',
        'testcases.Interface.Test_Interface_12',
        'testcases.Interface.Test_Interface_13',
        'testcases.Interface.Test_Interface_16',
        'testcases.Interface.Test_Interface_19',
        'testcases.Interface.Test_Interface_20',
        'testcases.Interface.Test_Interface_40',
        'testcases.Interface.Test_Interface_47',
        'testcases.Interface.Test_Interface_15',
        'testcases.Interface.Test_Interface_22',
        'testcases.Interface.Test_Interface_29',
        'testcases.Interface.Test_Interface_25',
        'testcases.Interface.Test_Interface_26',
        'testcases.Interface.Test_Interface_28',
        'testcases.Interface.Test_Interface_23',
        'testcases.Interface.Test_Interface_69',
        'testcases.Interface.Test_Interface_70',
        'testcases.Interface.Test_Interface_71',
        'testcases.Interface.Test_Interface_30',
        'testcases.Interface.Test_Interface_15',
        'testcases.Interface.Test_Interface_36',
        'testcases.Interface.Test_Interface_53',
    ]

    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

