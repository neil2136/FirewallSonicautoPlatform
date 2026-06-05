from definition.settings import *
from definition.guestservicestep import *
from definition.urlib import *


@paramunittest.parametrized(
    {'uuid': '1527010', 'zone': 'LAN', 'interface': 'X4'},
    {'uuid': '1527022', 'zone': 'cus_trust', 'interface': 'X4'},
)
class Test01_RedirectSMTP(Test):
    def setParameters(self, uuid, zone, interface):
        self.uuid = uuid
        self.zone = zone
        self.interface = interface
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']
        self.guesttest = guestteststep(self.zone, self.interface)
        # self.tb_hostname=PC1_host.send_command('hostname')

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_initial_disable_guest_service_for_zone(self):
        self.guesttest.initial_disable_guest_service_for_zone()

    def test_02_configure_interface(self):
        self.guesttest.configure_interface()

    def test_03_verify_pc_traffic_to_internet_passed(self):
        self.guesttest.verify_pc_traffic_to_internet_passed()

    def test_04_enable_smtp_redirect(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "smtp_redirect": {
                            "name": "smtp_redirect"
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_05_verify_guest_service_enabled(self):
        self.guesttest.verify_guest_service_enabled()

    def test_06_change_mail_server_hostname(self):
        try:
            start_mail_server.change_mail_server_host_name(PC1_host, "mail.sonicauto.com")
        except:
            pass
        else:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: change hostname Fail")

    def test_07_login_guest_user_from_pc(self):
        self.guesttest.login_guest_user_from_pc("login")

    def test_08_start_capture(self):
        start_capture()

    def test_09_send_mail_smtp(self):
        cmd = ('python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/definition/send_mail.py -protocol "smtp"')
        logger.info(f"works on PC2")
        out = PC4_host.send_command(cmd)
        logger.info("login with guest user\n" + out)
        res = "ERROR" not in out
        Assertion.assert_equal(res, True, "ERR: show testcase info failed")

    def test_10_verify_mail_smtp_packet_redirected(self):
        rc = verify_packet_in_capture("smtp")
        Assertion.assert_equal(rc, True, "ERR: verify packet fail")

    def test_11_start_capture(self):
        start_capture()

    def test_12_send_mail_pop3(self):
        cmd = ('python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/definition/send_mail.py -protocol "pop3"')
        logger.info(f"works on PC2")
        out = PC4_host.send_command(cmd)
        logger.info("login with guest user\n" + out)
        res = "ERROR" not in out
        Assertion.assert_equal(res, True, "ERR: show testcase info failed")

    def test_13_verify_mail_pop3_packet_redirected(self):
        rc = verify_packet_in_capture("pop3")
        Assertion.assert_equal(rc, True, "ERR: verify packet fail")

    def test_14_diable_smtp_redirect(self):
        payload = {
            "zones": [
                {
                    "name": self.zone,
                    "guest_services": {
                        "enable": True,
                        "smtp_redirect": {
                        }
                    }
                }
            ]
        }
        self.guesttest.edit_zone_with_guest_service(payload)

    def test_15_start_capture(self):
        start_capture()

    def test_16_send_mail_smtp(self):
        cmd = ('python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/definition/send_mail.py -protocol "smtp"')
        logger.info(f"works on PC2")
        out = PC4_host.send_command(cmd)
        logger.info("login with guest user\n" + out)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_17_verify_mail_smtp_packet_redirected(self):
        rc = False
        try:
            stopres = packetobj.stop_capture()
            logger.info(f'stop packets on FW result: {stopres}')
            packetobj.export_captured_packets_pcapng()
            filterdnscmd = f'tshark -r /tmp/packet-c.pcapng -Y "tcp.dstport==25" -V -T text'
            logger.info(f'filterdnscmd: {filterdnscmd}')
            filteredpackets = PC1_host.send_command(filterdnscmd)
            # logger.info(f'run packet monitor end...,filterpackets is {filteredpackets}')
        except:
            pass
        else:
            if "172.17.1.10" not in filteredpackets:
                rc = True
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: verify packet fail")

    def test_18_start_capture(self):
        start_capture()

    @repeat_method(2)
    def test_19_send_mail_pop3(self):
        cmd = ('python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/definition/send_mail.py -protocol "pop3"')
        logger.info(f"works on PC2")
        out = PC4_host.send_command(cmd)
        logger.info("login with guest user\n" + out)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_20_verify_mail_pop3_packet_redirected(self):
        rc = False
        try:
            stopres = packetobj.stop_capture()
            logger.info(f'stop packets on FW result: {stopres}')
            packetobj.export_captured_packets_pcapng()
            filterdnscmd = f'tshark -r /tmp/packet-c.pcapng -Y "tcp.dstport==110" -V -T text'
            logger.info(f'filterdnscmd: {filterdnscmd}')
            filteredpackets = PC1_host.send_command(filterdnscmd)
            # logger.info(f'run packet monitor end...,filterpackets is {filteredpackets}')
        except:
            pass
        else:
            if "172.17.1.10" not in filteredpackets:
                rc = True
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: verify packet fail")

    def test_21_change_mail_server_hostname(self):
        try:
            logger.info(f"tb_hostname is {tb_hostname}")
            start_mail_server.change_mail_server_host_name(PC1_host, tb_hostname)
        except:
            rc = False
        else:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: change hostname Fail")

    def test_22_logout_guest_user_from_client(self):
        self.guesttest.logout_guest_user_via_logout_button()
