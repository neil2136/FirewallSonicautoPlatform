# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/IPv6_PPPoE_Client')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [        
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC012',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC020',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC013',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC021',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC014',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC109',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC029',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC074',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC054',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC059',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC022',
        # 'testcases.IPv6_PPPoE_Client.TestPPPoE_TC023',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC039',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC026',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC025',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC027',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC018',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC093',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC123',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC119',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC125',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC128',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC028',
        'testcases.IPv6_PPPoE_Client.TestPPPoE_TC058',
   ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()

