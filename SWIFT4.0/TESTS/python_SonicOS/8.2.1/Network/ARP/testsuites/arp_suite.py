import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/Network/ARP/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'arp.Test_01_Add_Interface_02',
        'arp.Test_02_Delete_ARP_03',
        'arp.Test_03_Edit_ARP_16',
        'arp.Test_04_Bind_MAC_20',
        'arp.Test_05_Delete_Static_ARP_23',
        ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites

if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
