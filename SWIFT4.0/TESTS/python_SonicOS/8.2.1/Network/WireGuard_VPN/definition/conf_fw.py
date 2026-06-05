from settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': MASK,
            'gateway': X1_GW,
            'dns1': X1_DNS1,
            'dns2': X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfaceipv4.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_add_adress_object(self):
        rc1 = ao.config_addressobject(**address_object1)
        rc2 = ao.config_addressobject(**address_object2)
        rc = True if rc1 and rc2 else False
        Assertion.assert_equal(rc, True, "ERR: add address object into Firewall failed.")

    # def test_02_import_sslcert(self):
    #     rc = certobj.import_cert_local(cert_path="@"+certpath, name='dovecot_1k', password='password')
    #     Assertion.assert_equal(rc, True, "ERR: Import SSL Certificate into Firewall failed.")
    #
    # def test_03_add_local_users(self):
    #     rc = userlocalcli.add_local_user(**local_user_dict)
    #     Assertion.assert_equal(rc, True, "ERR: add local users into Firewall failed.")

    # @repeat_method(5)
    # def test_03_Register_fw(self):
    #     time.sleep(10)
    #     rc = lc.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")
