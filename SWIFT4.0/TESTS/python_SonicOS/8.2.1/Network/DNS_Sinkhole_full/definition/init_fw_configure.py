from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'
    description = 'Initialize testbed'
    goto_teardown = True

    def test_01_config_X1(self):
        rc = interface_api.config_interface(**X1_static_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed!!")

    def test_02_enable_dns_sinkhole_logs(self):
        rc_mal = logSet_api.edit_event(event_id=str(CParam.Hit_Malicious_Pkt_log), **drop_log_dict)
        logger.info(f'Enable Log "Drop Hit DNS Sinkhole Malicious Database Packets" result...... {rc_mal}')
        drop_log_dict['log']['event'][0]['id'] = CParam.Forged_IP_log
        rc_fgd = logSet_api.edit_event(event_id=str(CParam.Forged_IP_log), **drop_log_dict)
        logger.info(f'Enable Log "Drop DNS Sinkhole Forged IP Packets" result...... {rc_fgd}')
        Assertion.assert_equal(rc_mal & rc_fgd, True, "ERR: Enable_dns_sinkhole_logs failed")

    @repeat_method(10)
    def test_03_register_fw(self):
        rc = license_cli.register("online")
        if not rc:
            time.sleep(20)
        Assertion.assert_equal(rc, True, "ERR: register fw failed")