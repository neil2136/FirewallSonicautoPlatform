from definition.settings import *


# Expected: [GUI] Verify the Export Database button works well
class TestSettings_1521169(Test):
    uuid = "SOSAIOT-TC-51533"
    description = show_testcase_info(TESTPLAN, '1521169', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521169')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_export_database_api(self):
        res = dnsFilter_api.export_dns_filtering_database_csv()
        logger.info(f'Export database result...... {res}')
        logger.info('Check csv file content......')
        csv_location = '/tmp/dnsfilterDB.csv'
        content = PC1_LOGIN.send_command(f'cat {csv_location}')
        rc = 'Category' in str(content)
        Assertion.assert_equal(rc, True, "ERR: export_database_and_check failed!!")


# Expected: [CLI] Verify the CLI Commends to export the database.
class TestSettings_1521170(Test):
    uuid = "SOSAIOT-TC-51534"
    description = show_testcase_info(TESTPLAN, '1521170', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521170')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_export_database_scp(self):
        res = dnsFilter_cli.export_dns_filtering_database_csv(**export_params_dict)
        logger.info(f'Export database via scp result...... {res}')
        content = PC1_LOGIN.send_command('cat dnsfilterDB_scp.csv')
        rc = 'Category' in str(content)
        Assertion.assert_equal(rc, True, "ERR: export_database_scp failed!!")

    def test_02_export_database_ftp(self):
        export_params_dict.update({'protocol': 'ftp', 'filepath': 'dnsfilterDB_ftp.csv'})
        res = dnsFilter_cli.export_dns_filtering_database_csv(**export_params_dict)
        logger.info(f'Export database via ftp result...... {res}')
        content = PC1_LOGIN.send_command('cat dnsfilterDB_ftp.csv')
        rc = 'Category' in str(content)
        Assertion.assert_equal(rc, True, "ERR: export_database_ftp failed!!")


# Expected: [FUNC] Verify the Database in Memory Storage will be cleared after rebooting.
class TestReboot_1521172(Test):
    uuid = "SOSAIOT-TC-51535"
    description = show_testcase_info(TESTPLAN, '1521172', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1521172')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed!!")

    def test_01_reboot(self):
        rc = sett_api.boot_fw(mode=1)
        Assertion.assert_equal(rc, True, "ERR: failed to reboot !!")

    def test_02_check_database(self):
        res = dnsFilter_api.get_dns_filtering_statistics()
        rc = res.get('total_category_counter')
        Assertion.assert_equal(rc, 0, "ERR: check_database failed!!")
