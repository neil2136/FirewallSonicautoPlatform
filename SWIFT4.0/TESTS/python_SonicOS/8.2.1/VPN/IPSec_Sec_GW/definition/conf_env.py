from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    # goto_teardown = True

    def test_00_01_Conf_Local_DPD(self):
        logger.info('-'*10+'Config Local DPD'+'-'*10)
        rc = LAdv_obj.config_vpnadvanced(**Ldpd)
        rc &= RAdv_obj.config_vpnadvanced(**Rdpd)
        Assertion.assert_equal(rc, True, 'Config Local DPD Failed.')

    def test_00_02_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')

    def test_00_03_Conf_DNS_Server_in_PC3(self):
        configfilecmds = [
            'cp {}vpntestbed.com.db /var/named/chroot/var/named/'.format(conf_path),
            'cp {}named.conf /var/named/chroot/etc/'.format(conf_path),
            'service named restart',
        ]
        output = PC3_login.send_commands(configfilecmds)
        if re.search('Starting named', output):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add AO for DUT and RDUT Failed.')