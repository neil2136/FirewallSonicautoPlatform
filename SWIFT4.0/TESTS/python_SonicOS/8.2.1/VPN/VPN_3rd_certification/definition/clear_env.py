from definition.settings import *


class TestClearConfEnv(Test):
    uuid = 'NonTC'
    description = "clear env config settings"
    goto_teardown = True

    def test_00_01_remove_CA_Cert(self):
        logger.info('-'*10+'Remove CA cert'+'-'*10)
        rc = LCACertObj.delete_ca_cert(ca_hash="nfB5Erd0dz1GD5B6eXXkdQ==")
        rc &= RCACertObj.delete_ca_cert(ca_hash="nfB5Erd0dz1GD5B6eXXkdQ==")
        Assertion.assert_equal(rc, True, 'Remove CA cert Failed.')

    def test_00_02_Remove_Local_Cert(self):
        logger.info('-'*10+'Remove local cert'+'-'*10)
        rc = LCACertObj.delete_local_cert(filename='my_cert')
        rc &= RCACertObj.delete_local_cert(filename='my_cert')
        Assertion.assert_equal(rc, True, 'Remove local cert Failed.')
