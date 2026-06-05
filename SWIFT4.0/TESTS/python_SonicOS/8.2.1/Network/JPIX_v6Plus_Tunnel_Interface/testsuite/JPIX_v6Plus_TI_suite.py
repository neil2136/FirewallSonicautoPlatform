import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ['PYTHON_SONICOS_HOME'])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/JPIX_v6Plus_Tunnel_Interface')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

def suite():
    testcases_list = [
        # 'config.init_testbed.TestRestoreDUT',
        # 'config.init_testbed.TestUploadFirmware',
        # 'definition.init_config_fw',
        # 'definition.init_config_pc',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC01',
        'testcases.JPIX_v6Plus_tunnel_interface.Test_TC02',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC03',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC04',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC05',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC06',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC07',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC08',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC09',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC10',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC11',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC12',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC13',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC14',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC15',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC17',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC18',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC19',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC20',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC21',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC16',
        # 'testcases.JPIX_v6Plus_tunnel_interface.Test_TC22',
    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()


# python3 Network/JPIX_v6Plus_Tunnel_Interface/testsuite/JPIX_v6Plus_TI_suite.py --console_ip 10.8.0.104 
# --console_port 2010 -sonicos_ver 8.2.1