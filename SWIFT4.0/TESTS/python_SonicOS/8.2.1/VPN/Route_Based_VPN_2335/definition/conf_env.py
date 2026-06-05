from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_set_FW_time(self):
        time_json = {
            "time": {
                "use_ntp": False,
                "time": "10:00:39",
                "date": "2022:01:01",
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    def test_00_01_Configure_Interface_in_DUT(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.DUTX2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = LintfaceObj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config DUT X2 failed")

    def test_00_02_Configure_Interface_in_Remote(self):
        x2_static = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTEX2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = RintfaceObj.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config Remote X2 failed")

    def test_00_03_Add_DUT_AddObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**remote_l)
        logger.info('-'*10+'Add AO for rm DUT'+'-'*10)
        rc &= RAddrOBJ.config_addressobject(**remote_r)
        Assertion.assert_equal(rc, True, 'Add AO for DUT and remote Failed.')

    def test_00_04_enable_dpd_on_Remote(self):
        rc = LAdv_obj.config_vpnadvanced(**En_dpd)
        rc &= RAdv_obj.config_vpnadvanced(**En_dpd)
        Assertion.assert_equal(rc, True, 'Config DPD on remote Failed.')

    def test_00_05_setup_ftp_server_on_remote_host(self):
        cmd_list = [
            "sed -i 's/^root/#root/' /etc/vsftpd/ftpusers",
            "sed -i 's/^root/#root/' /etc/vsftpd/user_list",
            'service vsftpd restart',
        ]
        output = PC2_login.send_commands(cmd_list)
        if re.search('Starting vsftpd for vsftpd.*OK', output, re.I|re.M):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Config DPD on remote Failed.')
