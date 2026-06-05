__author__ = 'CHU'

from definition.settings import *

class TestSyslog_128_01(Test):
    uuid = "SOSAIOT-TC-55589"
    description= show_testcase_info(TESTPLAN, '6', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_add_syslog_server(self):
        logger.info(" Add syslog server ".center(40, '-'))
        rc = Log_obj.add_syslog_server(**syslog_opt)
        Assertion.assert_equal(rc, True, 'Add syslog server Failed.')

    def test_01_02_check_server(self):
        logger.info(" Check server ".center(40, '-'))

        ret = Log_obj.show_syslog_server()
        if syslog_opt['name'] in str(ret):
            rc = True
            logger.info(f'Find syslog server {syslog_opt["name"]}')
        else:
            rc = False
            logger.info(f'The server {syslog_opt["name"]} can\'t be found')
        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')

    def test_01_03_check_tsr(self):
        logger.info(" Check TSR ".center(40, '-'))
        kwd = 'Server Name'
        reline = 'Syslog Per Server Settings' + '(.*?)' + 'Syslog Field Settings'
        server = syslog_opt['name']

        rc = syslog_lib.check_tsr(kwd,reline,server)
        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')

    def test_01_04_delete_all_syslog_servers(self):
        rc = Log_obj.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'Delete all syslog server Failed.')


class TestSyslog_128_02(Test):
    uuid = "SOSAIOT-TC-55590"
    description= show_testcase_info(TESTPLAN, '7', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_add_syslog_server(self):
        logger.info(" Add syslog server ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        opt['name'] = logserver2
        opt['port'] = serverport

        rc = Log_obj.add_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Add syslog server Failed.')

    def test_02_02_edit_syslog_server(self):
        logger.info(" Edit syslog server ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        opt['name'] = logserver2
        opt['port'] = serverport1
        add_opt = {
            'new_name'  : logserver1,
            'id'        : 'SonicBoys',
            'profile'   : 1,
            'format'    : 'webtrends',
            'facility'  : 'local-use1',
            'en_erl'    : 'on',
            'en_drl'    : 'on',
            'evt_lmt'   : 999,
            'data_lmt'  : 100009,
        }
        opt.update(add_opt)

        rc = Log_obj.edit_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Edit syslog server Failed.')

    def test_02_03_check_server(self):
        logger.info(" Check server ".center(40, '-'))

        ret = Log_obj.show_syslog_server()
        if logserver1 in str(ret):
            rc = True
            logger.info(f'Success! Find syslog server {logserver1}')
        else:
            rc = False
            logger.info(f"The server {logserver1} can't be found")
        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')

    def test_02_04_check_tsr(self):
        logger.info(" Check TSR ".center(40, '-'))
        kwd = 'Server Name'
        reline = 'Syslog Per Server Settings' + '(.*?)' + 'Syslog Field Settings'
        server = syslog_opt['name']
        rc = syslog_lib.check_tsr(kwd,reline,server)

        Assertion.assert_equal(rc, True, 'Check syslog server Failed.')

    def test_02_05_delete_all_syslog_servers(self):
        rc = Log_obj.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'Delete all syslog server Failed.')


class TestSyslog_128_03(Test):
    uuid = "SOSAIOT-TC-55576"
    description= show_testcase_info(TESTPLAN, '22', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_add_syslog_servers(self):
        logger.info(" Add syslog server ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.add_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Add syslog servers Failed.')

    def test_03_02_edit_syslog_servers(self):
        logger.info(" Edit syslog servers ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        opt.update({'facility': facility})
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.edit_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Edit facility settings Failed.')

    def test_03_03_check_syslog_servers(self):
        logger.info(" Check facility settings ".center(40, '-'))
        rc = True
        out = Log_obj.show_syslog_server()
        servers = out['log']['syslog']['server']
        for log_server in servers:
            if facility == log_server['facility']:
                logger.info(f'Check facility {facility} successful!')
                rc &= True
        Assertion.assert_equal(rc, True, 'Check facility settings Failed.')

    def test_03_04_delete_all_syslog_servers(self):
        rc = Log_obj.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'Delete all syslog server Failed.')


class TestSyslog_128_04(Test):
    uuid = "SOSAIOT-TC-55586"
    description= show_testcase_info(TESTPLAN, '51', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '51')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_add_syslog_servers(self):
        logger.info(" Add syslog server ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.add_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Add syslog servers Failed.')

    def test_04_02_edit_syslog_servers(self):
        logger.info(" Edit syslog servers ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        opt.update({'id': syslog_id})
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.edit_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Edit id settings Failed.')

    def test_04_03_check_syslog_servers(self):
        logger.info(" Check id settings ".center(40, '-'))
        rc = True
        out = Log_obj.show_syslog_server()
        servers = out['log']['syslog']['server']
        for log_server in servers:
            if syslog_id == log_server['id']:
                logger.info(f'Check id {syslog_id} successful!')
                rc &= True
        Assertion.assert_equal(rc, True, 'Check id settings Failed.')

    def test_04_04_delete_all_syslog_servers(self):
        rc = Log_obj.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'Delete all syslog server Failed.')

class TestSyslog_128_05(Test):
    uuid = "SOSAIOT-TC-94178"
    description= show_testcase_info(TESTPLAN, '52', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '52')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_add_syslog_servers(self):
        logger.info(" Add syslog server ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.add_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Add syslog servers Failed.')

    def test_05_02_edit_syslog_servers(self):
        logger.info(" Edit syslog servers ".center(40, '-'))
        opt = copy.deepcopy(syslog_opt)
        rc = True
        opt.update({'format': syslog_format})
        for item in servers:
            opt['name'] = item
            opt['port'] = serverport
            rc &= Log_obj.edit_syslog_server(**opt)
        Assertion.assert_equal(rc, True, 'Edit format settings Failed.')

    def test_05_03_check_syslog_servers(self):
        logger.info(" Check format settings ".center(40, '-'))
        rc = True
        out = Log_obj.show_syslog_server()
        servers = out['log']['syslog']['server']
        for log_server in servers:
            if syslog_format == log_server['format']:
                logger.info(f'Check format {syslog_format} successful!')
                rc &= True
        Assertion.assert_equal(rc, True, 'Check format settings Failed.')

    def test_05_04_delete_all_syslog_servers(self):
        rc = Log_obj.delete_all_syslog_servers()
        Assertion.assert_equal(rc, True, 'Delete all syslog server Failed.')