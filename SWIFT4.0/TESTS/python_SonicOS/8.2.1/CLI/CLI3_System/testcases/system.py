from settings import *


class Test_01_show_status_check_1(Test):
    uuid = "SOSAIOT-TC-48447"
    description = show_testcase_info(TESTPLAN,
                                     "1", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_status(self):
        rs = statuscli.show_status()
        logger.info('show status result: {}'.format(rs))
        output = 'System Information' in rs
        Assertion.assert_equal(output, True, "ERR: show status failed")


class Test_02_configure_administration_2(Test):
    uuid = "SOSAIOT-TC-48448"
    description = show_testcase_info(TESTPLAN,
                                     "2", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_administration_http_port(self):
        rs = admincli.http_port(8888)
        logger.info('config http port result: {}'.format(rs))
        showrs = admincli.show_administration_search('match', '8888')
        logger.info('show admin setting result: {}'.format(showrs))
        output = True if 'http-port 8888' in showrs else False
        logger.info(output)
        if output:
            initrs = admincli.http_port(80)
            logger.info('reset http port result: {}'.format(initrs))
        Assertion.assert_equal(output, True, "ERR: modify administrator http port failed")


# skip because of not environment in openstack.
class Test_03_enable_fips_check_3(Test):
    """
    FIPS can not be used in openstack testbad
    """
    uuid = '906f9e4f-1599-469d-be89-6bddb8bde7cb'
    description = show_testcase_info(TESTPLAN,
                                     "3", description=True)['title']


class Test_04_nslookup_check_4(Test):
    uuid = "SOSAIOT-TC-48453"
    description = show_testcase_info(TESTPLAN,
                                     "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    # @repeat_method(5)
    def test_01_nslookup_check(self):
        flag = False
        for url in EXTERNAL_URL:
            rs = diagnosticscli.nslookup(url)
            searchrs = re.findall('Resolved Address:\s+\S+', rs)
            logger.info(searchrs)
            try:
                if searchrs[0].split(' ')[-1]:
                    flag = True
                else:    
                    logger.error('can not find resolved address in diag result.')
            except:
                print('Can not get the resolved address for the domain %s' % url)
        Assertion.assert_equal(flag, True, "ERR: nslookup check failed")


class Test_05_ping_check_5(Test):
    uuid = "SOSAIOT-TC-48449"
    description = show_testcase_info(TESTPLAN,
                                     "5", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    @repeat_method(5)
    def test_01_ping(self):
        flag = False
        for ip in pinglist:
            rs = diagnosticscli.ping(ip, 'X1')
            
            output = True if 'is alive' in rs else False
            if output:
                flag = True
                logger.info('diagnostic ping successful: {}'.format(rs))
            else:    
                logger.info('ip ping failed: {}'.format(ip))
        Assertion.assert_equal(flag, True, "ERR: ping check failed")


class Test_06_configure_schedule_7(Test):
    uuid = "SOSAIOT-TC-48451"
    description = show_testcase_info(TESTPLAN,
                                     "7", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_schedule(self):
        confrs = schedulecli.conf_schedule(**schedule_dict)
        logger.info('config schedule result: {}'.format(confrs))
        showrs = schedulecli.show_schedule(schedule_dict['name'])
        logger.info('show schedule result: {}'.format(showrs))
        if schedule_dict['rec-time'] in showrs:
            initrs = schedulecli.rem_schedule(schedule_dict['name'])
            logger.info('remove schedule result: {}'.format(initrs))
        output = True if schedule_dict['rec-time'] in showrs else False
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: modify schedule failed")


class Test_07_traceroute_check_8(Test):
    uuid = "SOSAIOT-TC-48454"
    description = show_testcase_info(TESTPLAN,
                                     "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_traceroute(self):
        json_input1 = {"stream":"enforceDropUnreachICMP=&enforceDropTimeExceedICMP="}
        response1 = diagcfg.config_raw_api(**json_input1)
        logger.info('disable enforceDropUnreachICMP result: {}'.format(response1))
        
        rs = diagnosticscli.traceroute(Parameter.X1_DNS1, 'X1')
        logger.info('diagnostic traceroute result: {}'.format(rs))
        #output = True if '10.214.0.1' in rs or '10.6.0.1' in rs else False
        output = True if '172.16.1.1' in rs else False

        json_input2 = {"stream":"enforceDropUnreachICMP=on&enforceDropTimeExceedICMP=on"}
        response2 = diagcfg.config_raw_api(**json_input2)
        logger.info('enable enforceDropUnreachICMP result: {}'.format(response2))

        Assertion.assert_equal(output, True, "ERR: traceroute check failed")


class Test_08_configure_time_9(Test):
    uuid = "SOSAIOT-TC-48452"
    description = show_testcase_info(TESTPLAN,
                                     "9", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_configure_time(self):
        time_dict = {'daylight-savings': False}
        rs = timecli.conf_time(**time_dict)
        logger.info('config time result: {}'.format(rs))
        showrs = timecli.show_time()
        logger.info('show time settings result: {}'.format(showrs))
        output = True if 'no daylight-savings' in showrs else False
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: modify time failed")


# Must be run in the final because of reset FW.
class Test_09_restore_defaults_check_6(Test):
    uuid = "SOSAIOT-TC-48450"
    description = show_testcase_info(TESTPLAN,
                                     "6", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_restore_defaults_check(self):
        rs = settingcli.restore(consvr, conport)
        logger.info('restore setting result: {}'.format(rs))
        time.sleep(300)
        showrs = interfaceclicfg.show_interface_status(interface='X1')
        logger.info('show interface status result: {}'.format(showrs))
        output = True if 'ip-assignment WAN dhcp' in showrs else False
        Assertion.assert_equal(output, True, "ERR: restore default failed")
