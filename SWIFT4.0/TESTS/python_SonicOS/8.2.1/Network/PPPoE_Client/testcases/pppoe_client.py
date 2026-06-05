from settings import *
from utils import *


class Test_12_Assign_Primary_PPPoE(Test):
    uuid = "SOSAIOT-TC-57121"
    description = show_testcase_info(TESTPLAN, "12", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_x2_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x2_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoe ip failed!")

    @repeat_method(5)
    def test_02_verify_x2_get_pppoe_ip(self):
        time.sleep(10)
        x2_ip = interfaceapi.get_interface_ip('X2')
        logger.info('Interface X2 IP:' + x2_ip)
        server_ip = Parameter.PC2_SERVER_X2
        logger.info('PPPOE Server X2 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x2_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR:X2 failed to get pppoe IP!")

    def test_03_verify_traffic(self):
        time.sleep(10)
        res = ping_from_client(Parameter.PC2_SERVER_X2, 10)
        Assertion.assert_equal(res, True, "ERR: verify traffic failed!")


class Test_13_Assign_Primary_Static_and_Secondary_PPPoE(Test):
    uuid = "SOSAIOT-TC-57122"
    description = show_testcase_info(TESTPLAN,"13", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_x2_static(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x2_static_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 static ip failed!")

    def test_02_configure_x3_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x3_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X3 pppoe ip failed!")

    @repeat_method(5)
    def test_03_verify_x3_get_pppoe_ip(self):
        time.sleep(10)
        x3_ip = interfaceapi.get_interface_ip('X3')
        logger.info('Interface X3 IP:' + x3_ip)
        server_ip = Parameter.PC2_SERVER_X3
        logger.info('PPPOE Server X3 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x3_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR:X3 failed to get pppoe IP!")

    def test_04_verify_x2_static_ip(self):
        time.sleep(10)
        ip = interfaceapi.get_interface_ip('X2')
        Assertion.assert_regular(str(ip), str(x2_static_opt_dynamic_dict['ip']), "ERR: failed to assign X2 static IP")

    def test_05_verify_x3_traffic(self):
        time.sleep(10)
        res = ping_from_client(Parameter.PC2_SERVER_X3, 10)
        Assertion.assert_equal(res, True, "ERR: verify X3 traffic failed!")


class Test_14_Assign_both_PPPoE(Test):
    uuid = "SOSAIOT-TC-57123"
    description = show_testcase_info(TESTPLAN, "14", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_x2_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x2_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoe ip failed!")

    def test_02_configure_x3_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x3_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X3 pppoe ip failed!")

    @repeat_method(5)
    def test_03_verify_x3_get_pppoe_ip(self):
        time.sleep(10)
        x3_ip = interfaceapi.get_interface_ip('X3')
        logger.info('Interface X3 IP:' + x3_ip)
        server_ip = Parameter.PC2_SERVER_X3
        logger.info('PPPOE Server X3 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x3_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR:X3 failed to get pppoe IP!")

    @repeat_method(5)
    def test_04_verify_x2_get_pppoe_ip(self):
        time.sleep(10)
        x2_ip = interfaceapi.get_interface_ip('X2')
        logger.info('Interface X2 IP:' + x2_ip)
        server_ip = Parameter.PC2_SERVER_X2
        logger.info('PPPOE Server X2 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x2_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR:X2 failed to get pppoe IP!")

    def test_05_verify_x2_traffic(self):
        time.sleep(10)
        res = ping_from_client(Parameter.PC2_SERVER_X2, 10)
        Assertion.assert_equal(res, True, "ERR: verify X2 traffic failed!")

    def test_06_verify_x3_traffic(self):
        time.sleep(10)
        res = ping_from_client(Parameter.PC2_SERVER_X3, 10)
        Assertion.assert_equal(res, True, "ERR: verify X3 traffic failed!")


class Test_19_PPPoE_Inactivity_Connection(Test):
    uuid = "SOSAIOT-TC-57125"
    description = show_testcase_info(TESTPLAN, "19", description=True)['title']
    logidconnect = '131'
    logidterminal = '130'

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_x2_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x2_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoe ip failed!")

    @repeat_method(5)
    def test_02_verify_x2_get_pppoe_ip(self):
        time.sleep(10)
        x2_ip = interfaceapi.get_interface_ip('X2')
        logger.info('Interface X2 IP:' + x2_ip)
        server_ip = Parameter.PC2_SERVER_X2
        logger.info('PPPOE Server X2 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x2_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR: X2 failed to get pppoe IP!")

    def test_03_clear_pppoe_logs(self):
        res = False
        disconn = interfaceapi.click_pppoe_disconnect('X2')
        logger.info('disconnect pppoe interface X2: {}'.format(disconn))
        levelinfo = logcategoryapi.logging_level(False, 'inform')
        logger.info('config logging level to inform: {}'.format(levelinfo))
        clearlog = logmonitorapi.clear_log()
        logger.info('clear logs result: {}'.format(clearlog))
        getlogpre = logmonitorapi.get_log(self.logidconnect)
        res = True if not getlogpre else False
        Assertion.assert_equal(res, True, "ERR: Clear pppoe logs failed!")

    @repeat_method(5)
    def test_04_verify_x2_pppoe_terminated(self):
        res = False
        clearlog = logmonitorapi.clear_log()
        logger.info('=====>log clear res: {}'.format(clearlog))

        conn = interfaceapi.click_pppoe_connect('X2')
        logger.info('=====>connect pppoe interface X2: {}'.format(conn))
        # get pppoe connect log
        time.sleep(10)
        logconn = logmonitorapi.get_log(self.logidconnect)
        if logconn and ('time' in logconn.keys()):
            conntime = logconn['time']
            logger.info(f'=====>pppoe connect log time: {conntime}')
            # get pppoe terminal log after 2 minutes
            time.sleep(125)
            logtmn = logmonitorapi.get_log(self.logidterminal)
            if logtmn and isinstance(logtmn, list):
                logtmn = logtmn.pop()
            if logtmn and  ('time' in logtmn.keys()):
                tmntime = logtmn['time']
                logger.info(f'=====>pppoe terminate log time: {tmntime}')
                res = time_difference(conntime, tmntime)
            else:
                logger.error(f"=====>ERR: Get terminal log time error!\nterminal log is: {logconn}")
        else:
            logger.error(f"=====>ERR: Get connect log time error!\nconnect log is: {logconn}")
        Assertion.assert_equal(res, True, "ERR: pppoe terminated failed!")


class Test_39_Disconnecting_PPPoE_Connection(Test):
    uuid = "SOSAIOT-TC-57128"
    description = show_testcase_info(TESTPLAN, "39", description=True)['title']

    def test_00_show_testplan(self):
        show_testcase_info(TESTPLAN, '39')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_configure_x2_pppoe(self):
        time.sleep(6)
        res = interfaceapi.config_interface(**x2_pppoe_opt_dynamic_dict)
        Assertion.assert_equal(res, True, "ERR: Configure X2 pppoe ip failed!")

    @repeat_method(5)
    def test_02_verify_x2_get_pppoe_ip(self):
        time.sleep(10)
        x2_ip = interfaceapi.get_interface_ip('X2')
        logger.info('Interface X2 IP:' + x2_ip)
        server_ip = Parameter.PC2_SERVER_X2
        logger.info('PPPOE Server X2 IP:' + server_ip)
        res = verify_ip1_in_ip2_network(x2_ip, server_ip)
        Assertion.assert_equal(res, True, "ERR:X2 failed to get pppoe IP!")

    def test_03_disconnect_x2_pppoe(self):
        time.sleep(10)
        res = interfaceapi.click_pppoe_disconnect('X2')
        Assertion.assert_equal(res, True, "ERR: disconnected X2 pppoe ip failed!")

    def test_04_verify_x2_disconnected(self):
        time.sleep(10)
        x2_ip = interfaceapi.get_interface_ip('X2')
        Assertion.assert_regular(str(x2_ip), str(Parameter.disconnected_IP), "ERR: X2 still got IP address")
