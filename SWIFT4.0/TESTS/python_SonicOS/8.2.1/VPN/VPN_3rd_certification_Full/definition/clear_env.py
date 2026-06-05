from definition.settings import *


class TestClearConfEnv1(Test):
    uuid = 'NonTC'
    description = "clear env config settings"
    goto_teardown = True

    @repeat_method(3)
    def test_00_01_remove_Cert_in_DUT(self):
        logger.info('-'*10+'Remove CA cert'+'-'*10)
        rc = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc &= LCACertObj.delete_ca_cert(ca_hash="hQoordDN72IZr88Rkc1f8A==")
        rc &= LCACertObj.delete_ca_cert(ca_hash="p3YySVaMEv5u4iYNGzNpVw==")
        rc &= LCACertObj.delete_local_cert(filename='my_cert')
        rc &= LCACertObj.delete_local_cert(filename='l2_cert')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'CA certificate' not in resp and 'Local certificate' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')

    @repeat_method(3)
    def test_00_02_Remove_Cert_in_Remote(self):
        logger.info('-'*10+'Remove local cert'+'-'*10)
        rc = RCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc &= RCACertObj.delete_ca_cert(ca_hash="hQoordDN72IZr88Rkc1f8A==")
        rc &= RCACertObj.delete_ca_cert(ca_hash="p3YySVaMEv5u4iYNGzNpVw==")
        rc &= RCACertObj.delete_local_cert(filename='my_cert')
        rc &= RCACertObj.delete_local_cert(filename='l2_cert')
        cmds = ['show certificates status imported']
        resp = rm_cli.do_cli_commands(cmds, 1)[1]
        if 'CA certificate' not in resp and 'Local certificate' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')


class TestClearConfEnv2(Test):
    uuid = 'NonTC'
    description = "clear env config settings"
    goto_teardown = True

    @repeat_method(3)
    def test_00_01_remove_Cert_in_DUT(self):
        logger.info('-'*10+'Remove CA cert'+'-'*10)
        rc1 = LCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc1 &= LCACertObj.delete_ca_cert(ca_hash="VWS7EkUs5ueUBrXsrA1CAg==")
        rc1 &= LCACertObj.delete_ca_cert(ca_hash="VaEBnKW5x8nJxfkbHOs9Yg==")
        rc2 = LCACertObj.delete_local_cert(filename='my_cert')
        rc2 &= LCACertObj.delete_local_cert(filename='validcert')
        rc2 &= LCACertObj.delete_local_cert(filename='revokecert')
        cmds = ['show certificates status imported']
        resp = fw_cli.do_cli_commands(cmds, 1)[1]
        if 'CA certificate' not in resp and 'Local certificate' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')

    @repeat_method(3)
    def test_00_02_Remove_Cert_in_Remote(self):
        logger.info('-'*10+'Remove local cert'+'-'*10)
        rc1 = RCACertObj.delete_ca_cert(ca_hash="p2A%2F1TcKHZ44xMpyXCH2Rw%3D%3D")
        rc1 &= RCACertObj.delete_ca_cert(ca_hash="VWS7EkUs5ueUBrXsrA1CAg==")
        rc1 &= RCACertObj.delete_ca_cert(ca_hash="VaEBnKW5x8nJxfkbHOs9Yg==")
        rc2 = RCACertObj.delete_local_cert(filename='my_cert')
        rc2 &= RCACertObj.delete_local_cert(filename='validcert')
        rc2 &= RCACertObj.delete_local_cert(filename='revokecert')
        cmds = ['show certificates status imported']
        resp = rm_cli.do_cli_commands(cmds, 1)[1]
        if 'CA certificate' not in resp and 'Local certificate' not in resp:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')