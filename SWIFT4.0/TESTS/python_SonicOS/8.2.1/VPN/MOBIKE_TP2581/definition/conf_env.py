from definition.settings import *


class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_01_Configure_Interface_X3(self):
        x3_static = {
            'if': 'X3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.DUTX3,
            'netmask': '255.255.255.0',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }

        rc = Linterface.config_interface(**x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_00_02_set_FW_time(self):
        curt_systime = os.popen("date +'%Y-%m-%d %H:%M:%S'").read()
        curt_date = curt_systime[0:10].replace('-',':')
        curt_time = curt_systime[-9:-1]
        logger.info("current system time {}".format(curt_systime))
        logger.info("current time {}".format(curt_time))
        logger.info("current date {}".format(curt_date))
        time_json = {
            "time": {
                "use_ntp": False,
                "time": curt_time,
                "date": curt_date,
                "time_zone": "pacific-time",
                "daylight_savings": True,
                "universal": False,
                "international_format": False,
                "only_custom_ntp": False,
                "ntp_update_interval": 60
            }
        }
        rc = LTimeObj.set_time(**time_json)
        Assertion.assert_equal(rc, True, 'set system time Failed.')

    @repeat_method(3)
    def test_00_03_Add_CA_Cert(self):
        logger.info('-'*10+'Add CA cert'+'-'*10)
        rc = LCACertObj.import_ca_cert(file=ca_cert)
        Assertion.assert_equal(rc, True, 'Add CA cert Failed.')

    @repeat_method(3)
    def test_00_04_Add_Local_Cert(self):
        logger.info('-'*10+'Add Local cert'+'-'*10)
        rc = LCACertObj.import_cert_local(cert_path='@' + local_cert, name='my_cert', password='123456')
        Assertion.assert_equal(rc, True, 'Add Local cert Failed.')
