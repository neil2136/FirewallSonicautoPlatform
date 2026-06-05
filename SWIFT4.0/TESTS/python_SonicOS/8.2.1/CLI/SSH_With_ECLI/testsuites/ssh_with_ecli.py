#__Author__ = "xzhou"
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+"/CLI/SSH_With_ECLI")


def suite():
    testcases_list = [
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'bin.conf_fw',
        'definition.init_conf_fw',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC01',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC02',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC03',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC04',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC06',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC07',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC08', not support anymore
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC09',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC10',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC11',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC12',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC13',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC14',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC15',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC16',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC17',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC18',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC19',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC23',not support anymore
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC24',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC25',not support anymore
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC26',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC31',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC32',not support anymore
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC42',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC43',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC44',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC46',
        'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC47',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC48',
        # 'testcases.ssh_with_ecli.Test_SSH_With_ECLI_TC49',not support anymore

    ]
    suites=unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
