# __author__: lezhang
import sys
import os
from runner.unittest.suite import UnittestSuite
import unittest

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"]+'/VPN/IKE_Preshared_Keys_TP30/')


def suite():
    testcases_list = [
        'definition.init_vpn_settings.Test_init_RemoteFW.test_01_init_remote_fw_via_asyncio',
        'config.init_testbed.TestRestoreDUT',
        'config.init_testbed.TestUploadFirmware',
        'definition.init_conf_fw',
        'definition.init_conf_pc.TestSetup_PCs',
        'definition.init_vpn_settings.Test_SetupVPN',

        # main mode test
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC13',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC14',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC17',
        'testcases.ike_preshared_keys_tp30.TestDomain_TC22',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC35',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC45',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC48',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC49',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC50',

        # aggressive mode test
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC24',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC25',
        'testcases.ike_preshared_keys_tp30.TestBaseFunc_TC28',
        'testcases.ike_preshared_keys_tp30.TestDomain_TC33',

        # netbios test
        'testcases.ike_preshared_keys_tp30.TestNETBIOS_TC20',
        'testcases.ike_preshared_keys_tp30.TestNETBIOS_TC31',

        # settings test
        'testcases.ike_preshared_keys_tp30.Testsettings_TC60',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC72',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC88',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC116',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC94',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC107',
        'testcases.ike_preshared_keys_tp30.Testsettings_TC102',

    ]
    suites = unittest.TestLoader().loadTestsFromNames(testcases_list)
    return suites


if __name__ == '__main__':
    st = UnittestSuite(sys.argv, suite())
    st.run()
