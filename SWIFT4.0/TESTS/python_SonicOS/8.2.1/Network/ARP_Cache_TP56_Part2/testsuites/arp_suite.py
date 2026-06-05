# __author__: ldu

import sys
import os
from runner.unittest.suite import UnittestSuite
import paramunittest
from runner.unittest.setup import Test
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP_Cache_TP56_Part2')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'testcases.arp_part2.Test_TC03',
        'testcases.arp_part2.Test_TC02',
        'testcases.arp_part2.Test_TC01',
        'testcases.arp_part2.Test_TC04',
        'testcases.arp_part2.Test_TC05',
        'testcases.arp_part2.Test_TC06',
        'testcases.arp_part2.Test_TC07',
        'testcases.arp_part2.Test_TC13',
        'testcases.arp_part2.Test_TC14',
        'testcases.arp_part2.Test_TC17',
        'testcases.arp_part2.Test_TC15',
        'testcases.arp_part2.Test_TC16',
        'testcases.arp_part2.Test_TC23',
        'testcases.arp_part2.Test_TC24',
        'testcases.arp_part2.Test_TC21',
        'testcases.arp_part2.Test_TC31',
        'testcases.arp_part2.Test_TC30',
        'testcases.arp_part2.Test_TC08',
        'testcases.arp_part2.Test_TC09',
        'testcases.arp_part2.Test_TC10',
        'testcases.arp_part2.Test_TC11',
        'testcases.arp_part2.Test_TC12',
        'testcases.arp_part2.Test_TC25',
        'testcases.arp_part2.Test_TC26',
        'testcases.arp_part2.Test_TC18',
        'testcases.arp_part2.Test_TC20',
        'testcases.arp_part2.Test_TC19',
        'testcases.arp_part2.Test_TC28',
        ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
